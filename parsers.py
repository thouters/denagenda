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

class LectureTable:
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
			self.klas = LectureTable.Klas.link(unicode(klas),self)
			self.course = LectureTable.Course.link(unicode(title),self)
			self.professor = LectureTable.Professor.link(unicode(prof),self)
			self.room = LectureTable.Room.link(unicode(room),self)
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
			# hier type herkennen en magie doen
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
						# student:   title -- weeks -- room -- prof
						# docent:    title -- klassen -- weeks -- lokalen
						# room:      title -- klassen -- weeks -- docent
						(title,weeks,room,prof) = map(lambda x: x.string.strip(), nthcell.findAll('td'))
						for week in WeekNotation2Array(weeks):
							y = self.Lecture(klas,title,prof,room,start,duration,weekday,week)
							y.debug = str(nth)+repr(day_from_col)
							self.Lectures.append(y)
			self.hasdata = True

class ProfessorTable(LectureTable):
	typeid = "staff"
	clistfilter = "staffarray"
class RoomTable(LectureTable):
	typeid = "room"
	clistfilter = "roomarray"
class KlasTable(LectureTable):
	typeid = "student"
	clistfilter = "studentsetarray"

class WebsiteSource:
	""" This class should be a repository you can ask for timetables """
	departments = ['IW','TECH']
	ttypes = [ProfessorTable, RoomTable, KlasTable]
	geturl= "http://sws.wenk.be/get_timetable.php"
	listurl = "http://sws.wenk.be/js/filter_%s.js"
	tables = []	

	def UpdateCandidates(self):
		""" Build a list of available timetables using data from sws.wenk.be """

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
			# each department has its own list with staff, groups,...
			# from this, build a list of instances of tabletypes
			remotefile = urllib.urlopen(self.listurl % department.lower())
			contents = remotefile.read()
			remotefile.close()
			for tabletype in self.ttypes:
				# filter the entities that go by this tabletype
				for i in JSarrayToList(contents, tabletype.clistfilter, 3):
					# add an instance of this 
					self.tables.append(tabletype(*[i[0],i[2],department]))

	def getTable(self,id):
		return self.getTables([id])[0]

	def getTables(self,wanted):
		""" Fetch tables """
		# get rid of None's in te list
		wanted = filter(lambda t: t != None, wanted)
		# tables need to be fetched one department at a time.
		for dept in self.departments:
			indept = filter(lambda t: t.department == dept,wanted)
			# fetch tables with the same tabletype together. 
			for tabletype in map(lambda x: x.typeid, self.ttypes): 
				# filter tables with this type from the wanted list
				tables = filter(lambda t: t.typeid == tabletype,indept)
				if not tables:
					continue
				#print "debug tables=", map(lambda x: x.department,tables)
				# generic post variables
				request = urllib.urlencode({	"weeks":"1-13", # FIXME
										"type": tabletype,	
										"filter":"(None)",
										"dept":dept})
				# add a list of identifiers to the post request
				request = "&".join([request]+map(lambda t: urllib.urlencode({"identifier[]": t.id}),tables))
				# fetch html and parse
				remotefile = urllib.urlopen(self.geturl,request)
				source = remotefile.read()
				remotefile.close()
				soup = BeautifulSoup(source)
				# debug -- save to disk
				x = open("".join(map(lambda x: x.name,tables)),'w')
				x.write(soup.prettify())
				x.close()
				# Iterate through all TIMETABLES in the HTML
				for ttheader in soup.html.body.findAll("table",{"class":"header-border-args"}):
					id = ttheader.find('span',{'class':'header-2-1-1'}).string.strip()
					try:
						x = filter(lambda x: x.name == id, tables)[0]
					except KeyError:
						raise ParseError, "Returned table not requested"
					x.Parse(ttheader)
		return wanted

	def byName(self,name):
		""" return an timetable that matches this name """
		if not self.tables:
			self.UpdateCandidates()
		matches = filter(lambda t: t.name == name, self.tables)[:1]
		if len(matches):
			return matches[0]
		else:
			return None

def IcalGlue(x):
	""" Lecture -- Ical event glue code """
	class y: pass
	x.location = y()
	x.organizer = y()
	x.dtstamp = datetime.now()
	x.dtstart = datetime.combine(WD2Date(x.week, x.weekday), x.start)
	x.dtend = x.dtstart + x.duration
	x.summary = x.course.name
	x.description = x.debug
	x.location.name = x.room.name
	x.organizer.name = x.professor.name
	x.organizer.email = "iemand@denayer.wenk.be"
	x.reqpart = [x.organizer]
	return x

if __name__ == "__main__":
	source = WebsiteSource()
	source.UpdateCandidates()
	wanted = map(lambda x: source.byName(x),['SP1'])#,'1PBEIE1'])
	timetables = source.getTables(wanted)
	x = open('/home/thomas/test.ics','w')
	x.write(ical.IcalFile(map(IcalGlue,timetables[0].Lectures)).toString().encode('utf-8'))
	x.close()
