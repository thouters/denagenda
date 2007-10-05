#!/usr/bin/python

from datetime import datetime, timedelta, time
from dncalendar import *
import ical
from BeautifulSoup import BeautifulSoup
import weakref, urllib,re

class LinkClass:
	""" This class implements relational links between classes"""
	_instances = set()
	_refs = set()
	def __repr__(self):
		return "%s '%s'" % (self.__class__.__name__,self.name)

	def __iter__(self):
		""" Iterate the list of objects that refer to this instance """
		dead = set()
		for ref in cls._refs:
			obj = ref()
			if obj is not None:
				yield obj
			else:
				dead.add(ref)
		cls._instances -= dead

	@classmethod
	def link(cls,name,obj):
		x = cls.unique(name)
		x._refs.add(weakref.ref(obj))
		return x

	@classmethod
	def unique(cls,name):
		"""Obtain a reference to an instance of this class, wth name==name  """
		double = filter(lambda x: x.name == name,cls.getinstances())
		if double:
			return double[0]
		else:
			x = cls()
			x.name = name
			cls._instances.add(weakref.ref(x))
			return x
	@classmethod
	def getinstances(cls):
		""" get a list of instances """
		dead = set()
		for ref in cls._instances:
			obj = ref()
			if obj is not None:
				yield obj
			else:
				dead.add(ref)
		cls._instances -= dead

class WebsiteSource:
	""" This class should be a repository you can ask for timetables """
	tables = []	
	def UpdateCandidates(self):
		""" Build a list of timetables using data from sws.wenk.be """
		departments = [('IW','iw'),('Technologie','tech')] #['ArchitectuurSLB','ArchitectuurSLG']
		source = "http://sws.wenk.be/js/filter_%s.js"
		weekentry = r"""^\s+AddWeeks\s*\(\s*"(\d+)"\s*,\s*\"()\"\s*,\s*form.elements\["weeks"\]\);\s*$"""

		def JSarrayToList(source, varname, depth):
			""" obtain a javascript array defined with js sourcecode """
			ret = {}
			# Obtain a list of array store operations
			arrayentry = r"""%s\s*\[\s*(\d+)\s*\]\s*\[\s*(\d+)\s*\]\s*=\s*"(.*)"\s*;"""
			regex = re.compile(arrayentry % varname)
			ops = re.findall(regex, source)
			# Ensurance
			if len(ops) == 0:
				raise Exception("Parse error")
			if len(ops) % depth > 0:
				raise Exception("Parsed invalid number of entries")
			for x in ops:
				n = int(x[0])
				if not n in ret.keys():
					ret[n] = [None, None, None]
				ret[n][int(x[1])] = x[2]
			return ret.values()

		self.tables = []
		for department in departments:
			remotefile = urllib.urlopen(source % department[1])
			contents = remotefile.read()
			remotefile.close()
			
			for i in JSarrayToList(contents, 'roomarray', 3):
				self.tables.append(RoomParser(*[i[0],i[2]]))
			for i in JSarrayToList(contents, 'staffarray', 3):
				self.tables.append(ProfessorParser(*[i[0],i[2]]))
			for i in JSarrayToList(contents, 'studentsetarray', 3):
				self.tables.append(KlasParser(*[i[0],i[2]]))

	def getTable(self,id):
		""" return an iterator over lectures.
			@id the name of the klas/prof/room """
		if not self.tables:
			self.UpdateCandidates()
		x = filter(lambda x: x.name == id, self.tables)
		if len(x):
			return x[0]
		else:
			return None

class TableParser:
	""" Fetches, parses a timetable from the internet,
		provides an iterator over events				"""
	Lectures = []
	source = None
	def __init__(self,name,id):
		self.name = name
		self.id = id
	def getSource(self):
		"""	Update the database with new data from the internet
			@param what: instance of obj to update | list
		"""
		""" fetch and parse a table of given identifier and weeks
			weeks for semesters: 1-14, 22-36	
		"""
		url= "http://sws.wenk.be/get_timetable.php"
		getdict = {	"identifier[]": self.id, ##
					"weeks":"1-13", ## dit is mogelijk fout!!!!
					"type": self.objectclass,	
					"filter":"(None)",
					"dept":"IW",
		}
		remotefile = urllib.urlopen(url,urllib.urlencode(getdict))
		c = remotefile.read()
		remotefile.close()
		#f = open('./output.html','w')
		#f.write(c)
		#f.close()
		self.source = c

	class Klas(LinkClass): pass
	class Course(LinkClass): pass
	class Professor(LinkClass): pass
	class Room(LinkClass): pass

	def __iter__(self):
		return iter(self.Lectures)

	class Lecture(LinkClass):
		def __init__(self,klas,title,prof,room,start,duration,weekday,week):
			self.klas = TableParser.Klas.link(unicode(klas),self)
			self.course = TableParser.Course.link(unicode(title),self)
			self.professor = TableParser.Professor.link(unicode(prof),self)
			self.room = TableParser.Room.link(unicode(room),self)
			self.start = start
			self.duration = duration
			self.weekday = weekday
			self.week = week
		def __repr__(self):
			return "<Lecture %s >" % " ".join(map(repr,[self.klas.name,self.course.name,self.professor.name,self.room.name,self.start,self.duration,self.weekday,self.week]))

	def Parse(self):
		# find all timetables given and start work on them.
		#<table class="header-2-args" border="0" cellspacing="0" width="100%">
		if self.source == None:
			self.getSource()
		soup = BeautifulSoup(self.source)
		for ttheader in soup.html.body.findAll("table",{"class":"header-border-args"}):
			colday = []
			# HEADER - has some crucial data
			#<span class="header-2-1-0"> Studentenrooster: </span>
			ttype = ttheader.find('span',{'class':'header-2-1-0'}).string.strip()[:-1]
			#<span class="header-2-1-1">2PBEIE3</span>
			klas = ttheader.find('span',{'class':'header-2-1-1'}).string.strip()
			#<table cellspacing='0' border='0' width='100%' class='header-3-args'>
			#<span class="header-3-0-1"> 22 </span>
			#<span class="header-3-0-3"> 36 </span>
			wspan = [ttheader.find('span',{'class':'header-3-0-1'}).string.strip(),ttheader.find('span',{'class':'header-3-0-3'}).string.strip()]
			wspan = map(int,wspan)
			# TIMETABLE HEAD- actual schedule data
			# jump to the timetable
			#<table class="grid-border-args" cellspacing="0">
			ctable = ttheader.findNextSibling('table',{'class':'grid-border-args'})
			# iterate through columns of the header line
			header = ctable.find('tr')
			#<td class="col-label-one" colspan="3"> dinsdag </td>
			for i,col in enumerate(header.findAll('td',{'class':'col-label-one'})):
				#iterate through spanning column headers
				span = int(col['colspan'].strip())
				colday.extend([i+1]*span)
			print "colday= %s" %(repr(colday))
			# colday should now be like [0,0,0,1,1,2,3,3,3,3]
			# TIMETABLE datarows
			for row in header.findNextSiblings('tr'):
				#first column contains start hour of the row
				hourcell = row.find('td',{'class':'row-label-one'})
				newh = hourcell.string.strip()
				# support for events starting at :15 and :45 
				if newh != '':
					start = HourDotMinute2Time(newh)
				else:
					start = start + timedelta(minutes=15)
				# loop through columns, these can contain events starting at starthour
				for colnum, column in enumerate(hourcell.findNextSiblings('td')):
					# check the cell for presence of a table
					#<table class="object-cell-args" border="0" cellspacing="0" width="100%">
					container = column.find('table',{'class':'object-cell-args'})
					# If the cell has an event, we hit the bull
					if container:
						# we can determine the weekday from the value of colday
						weekday = colday[colnum]
						# rowspan count represents blocks of 15 minutes
						#<td class="object-cell-border" colspan="1" rowspan="12">
						duration = timedelta(minutes=int(column['rowspan']) * 30)
						(title,weeks,room,prof) = map(lambda x: x.string.strip(), column.findAll('td'))
						for week in WeekNotation2Array(weeks):
							self.Lectures.append(self.Lecture(klas,title,prof,room,start,duration,weekday,week))

class ProfessorParser(TableParser):
	objectclass = "staff"
	template = "DN+Docent+individueel"
	
class RoomParser(TableParser):
	objectclass = "room"
	template = "DN+Zaal+individueel"

class KlasParser(TableParser):
	objectclass = "student"
	template = "DN+Studentenset+individueel"

def preptimes(x):
	class y: pass
	x.dtstamp = datetime.now()
	x.dtstart = datetime.combine(WD2Date(x.week, x.weekday), x.start)
	x.dtend = x.dtstart + x.duration
	x.description = x.course.name
	x.summary = x.course.name
	x.location = y()
	x.location.name = x.room.name
	x.organizer = y()
	x.organizer.name = x.professor.name
	x.organizer.email = "iemand@denayer.wenk.be"
	x.reqpart = [x.organizer]
	return x

if __name__ == "__main__":
	s = WebsiteSource()
	s.UpdateCandidates()
	#print map(lambda x: x.name, s.tables)
	#p = filter(lambda x: x.name == 'Ma EI2',s.tables)[0]
	#p = filter(lambda x: x.name == 'SP1',s.tables)[0]
	p = s.getTable('SP1')
	p.getSource()
	p.Parse()
	print "\n".join(map(repr,filter(lambda x: x.start==time(hour=8),p.Lectures)))
	x = open('/home/thomas/test.ics','w')
	x.write(ical.IcalFile(map(preptimes,p)).toString().encode('utf-8'))
	x.close()
