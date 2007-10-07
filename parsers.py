#!/usr/bin/python

from dncalendar import *
from datetime import datetime, date, timedelta, time
import ical
from BeautifulSoup import BeautifulSoup
import weakref, urllib,re

class LinkClass:
	""" This class implements relational links between classes"""
	_instances = set()
	_refs = set()
	def __repr__(self):
		return "< %s %s >" % (	self.__class__.__name__, self.name)

	def __iter__(self):
		""" Iterate the list of objects that refer to this instance """
		dead = set()
		for ref in self._refs:
			obj = ref()
			if obj is not None:
				yield obj
			else:
				dead.add(ref)
		self._refs -= dead

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

class ParseError(Exception): pass

class WebsiteSource:
	""" This class should be a repository you can ask for timetables """
	tables = []	
	departments = [('IW','iw'),('Tech','tech')] #['ArchitectuurSLB','ArchitectuurSLG']
	url= "http://sws.wenk.be/get_timetable.php"
	def UpdateCandidates(self):
		""" Build a list of timetables using data from sws.wenk.be """
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
		for department in self.departments:
			remotefile = urllib.urlopen(source % department[1])
			contents = remotefile.read()
			remotefile.close()
			
			for i in JSarrayToList(contents, 'roomarray', 3):
				self.tables.append(RoomTable(*[i[0],i[2],department[0]]))
			for i in JSarrayToList(contents, 'staffarray', 3):
				self.tables.append(ProfessorTable(*[i[0],i[2],department[0]]))
			for i in JSarrayToList(contents, 'studentsetarray', 3):
				self.tables.append(KlasTable(*[i[0],i[2],department[0]]))

	def getTable(self,id):
		return self.getTables([id])[0]

	def getTables(self,tlist):
		""" Fetch tables """
		if not tlist:
			raise Exception("no tables given")
		# tables need to be fetched one department at a time?
		#print [t.name for t in tlist]
		for dept in self.departments:
			print "any of these? ",dept
			tables = filter(lambda t: t.department == dept[0],tlist)
			print map(lambda x: x.department,tlist)
			#testing with one at a time for now
			table = tables[0]
			getdict = {	"identifier[]": table.id,
						"weeks":"1-13", "type": table.objectclass,
						"filter":"(None)", "dept": table.department}
			# do we have to close af file object?
			remotefile = urllib.urlopen(self.url,urllib.urlencode(getdict))
			source = remotefile.read()
			remotefile.close()
			# build tree
			soup = BeautifulSoup(source)
			# Iterate through all TIMETABLES in the HTML
			for ttheader in soup.html.body.findAll("table",{"class":"header-border-args"}):
				id = ttheader.find('span',{'class':'header-2-1-1'}).string.strip()
				try:
					x = filter(lambda x: x.name == id, tables)[0]
				except KeyError:
					raise ParseError, "Returned table not requested"
				x.Parse(ttheader)
		return tlist

	def byName(self,id):
		""" return an iterator over lectures.
			@id the name of the klas/prof/room """
		if not self.tables:
			self.UpdateCandidates()
		x = filter(lambda x: x.name == id, self.tables)
		return x

class TableParser:
	""" Fetches, parses a timetable from the internet,
		provides an iterator over events				"""
	Lectures = []
	source = None
	hasdata = False

	def __init__(self,name,id,dept):
		self.name = name
		self.id = id
		self.department = dept
	def __iter__(self):
		""" For now, iterate through lectures (FIX THIS) """
		return iter(self.Lectures)

	# Helper classes, to build relations between instances
	# this will allow to do basic queries on classes(tables)
	class Klas(LinkClass): pass
	class Course(LinkClass): pass
	class Professor(LinkClass): pass
	class Room(LinkClass): pass
	 
	class Lecture:
		""" Helper class """
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
			return "< %s >" % " ".join(	[self.__class__.__name__] + 
								map(repr,[	self.klas.name,
											self.course.name,
											self.professor.name,
											self.room.name,
											self.start,
											self.duration,
											self.weekday,
											self.week	]	)	)

	def Parse(self,ttheader):
			day_from_col = []
			# GENERIC HEADER - has some crucial data
			ttype = ttheader.find('span',{'class':'header-2-1-0'}).string.strip()[:-1]
			klas = ttheader.find('span',{'class':'header-2-1-1'}).string.strip()
			wspan = [ttheader.find('span',{'class':'header-3-0-1'}).string.strip(),ttheader.find('span',{'class':'header-3-0-3'}).string.strip()]
			wspan = map(int,wspan)
			# TIMEGRID HEAD - actual schedule data
			# => see how many columns each day has
			# build a list like: [0,0,0,1,1,2,3,3,3,3]
			headrow = ttheader.findNextSibling('table',{'class':'grid-border-args'}).find('tr')
			for i,col in enumerate(headrow.findAll('td',{'class':'col-label-one'})):
				day_from_col.extend([i+1]* int(col['colspan'].strip()))
			# TIMETABLE - scan each row for events
			for row in headrow.findNextSiblings('tr'):
				# Row's first column: contains the time events start at
				hourcell = row.find('td',{'class':'row-label-one'})
				newh = hourcell.string.strip()
				if newh != '':
					start = HourDotMinute2Time(newh)
				# loop through columns, these can contain events starting at starthour
				for nth, nthcell in enumerate(hourcell.findNextSiblings('td')):
					# check the cell for presence of a table
					container = nthcell.find('table',{'class':'object-cell-args'})
					# The cell holds an event? process it!
					if container:
						# we can determine the weekday from the value of colday
						weekday = day_from_col[nth]
						# rowspan -> 30 minute blocks
						duration = timedelta(minutes=int(nthcell['rowspan']) * 30)
						(title,weeks,room,prof) = map(lambda x: x.string.strip(), nthcell.findAll('td'))
						for week in WeekNotation2Array(weeks):
							self.Lectures.append(self.Lecture(klas,title,prof,room,start,duration,weekday,week))
			self.hasdata = True

class ProfessorTable(TableParser):
	objectclass = "staff"
class RoomTable(TableParser):
	objectclass = "room"
class KlasTable(TableParser):
	objectclass = "student"


def IcalGlue(x):
	""" Lecture -- Ical event glue code """
	class y: pass
	x.location = y()
	x.organizer = y()
	x.dtstamp = datetime.now()
	x.dtstart = datetime.combine(WD2Date(x.week, x.weekday), x.start)
	x.dtend = x.dtstart + x.duration
	x.description = x.summary = x.course.name
	x.location.name = x.room.name
	x.organizer.name = x.professor.name
	x.organizer.email = "iemand@denayer.wenk.be"
	x.reqpart = [x.organizer]
	return x

if __name__ == "__main__":
	source = WebsiteSource()
	source.UpdateCandidates()
	wanted = source.byName('SP1')
	timetable = source.getTables(wanted)[0]
	print "\n".join(map(repr,timetable.Lectures))
	#print "\n".join(map(repr,filter(lambda l: l.start==time(hour=8),timetable.Lectures)))
	#print "\n".join(map(repr,timetable.Room.unique("A102")))
	x = open('/home/thomas/test.ics','w')
	x.write(ical.IcalFile(map(IcalGlue,timetable.Lectures)).toString().encode('utf-8'))
	x.close()
