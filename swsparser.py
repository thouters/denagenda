#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Thomas Langewouters
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from dncalendar import *
from datetime import datetime, date, timedelta, time
import ical
from BeautifulSoup import BeautifulSoup
import weakref, urllib,re

class ParseError(Exception): pass

class FreshLectureTable:
	""" Freshly parsed Timetable """
	Lectures = []
	source = None
	hasdata = False

	def __init__(self,name,id,dept):
		self.name = name
		self.id = id
		self.department = dept
	def __iter__(self):
		""" Iterate over Lectures """
		return iter(self.Lectures)

	def __repr__(self):
		return "Timetable of \'%s\', dept \'%s\'" % (self.name,self.department)

	class Lecture:
		""" Helper class """
		def __init__(self,reldata,timedata):
			for (n,i) in	list(reldata.iteritems())+ \
							list(timedata.iteritems()):
				setattr(self,n,i)
		def __repr__(self):
			s = '< %s \'%s\'\n' % (self.__class__.__name__,self.title)
			s += "t= %s at %s for %s minutes\n" % \
				(nlwd[self.weekday], repr(self.start),
				repr(self.duration))
			s += "Students: %s \n" % repr(self.student)
			s += "Staff: %s \n" % repr(self.staff)
			s += "Rooms: %s \n" % repr(self.room)
			return s

	def Parse(self,ttheader):
			day_from_col = []
			# GENERIC HEADER - has some crucial data
			id = ttheader.find('span',{'class':'header-2-1-1'}).string.strip()
			wspan = [	ttheader.find('span',{'class':'header-3-0-1'}).string.strip(),
						ttheader.find('span',{'class':'header-3-0-3'}).string.strip()]
			self.wspan = map(int,wspan)
			# TIMEGRID HEAD - actual schedule data
			# => see how many columns each day has
			# build a list like: [0,0,0,1,1,2,3,3,3,3]
			headrow = ttheader.findNextSibling('table',{'class':'grid-border-args'}).find('tr')
			for i,col in enumerate(headrow.findAll('td',{'class':'col-label-one'})):
				day_from_col.extend([i+1]* int(col['colspan'].strip()))
			colcount = len(day_from_col)
			vspanc = [0]*colcount
			# TIMETABLE - scan each row for events
			for row in headrow.findNextSiblings('tr'):
				# Row's first column: contains the time events start at
				hourcell = row.find('td',{'class':'row-label-one'})
				newh = hourcell.string.strip()
				if newh != '':
					start = HourDotMinute2Time(newh)
				vspand = [0]*colcount
				# which columns will these td elements map to
				td_col = map(lambda x: x[0],filter(lambda y: y[1] == 0,enumerate(vspanc)))
				# loop through columns, these can contain events starting at starthour
				for nth, nthcell in enumerate(hourcell.findNextSiblings('td')):
					# check the cell for presence of a table
					container = nthcell.find('table',{'class':'object-cell-args'})
					# No event inside? next!
					if not container:
						continue
					colnum = td_col[nth]
					(timedata,reldata) = (dict(),dict())
					# we can determine the weekday from the value of colnum
					timedata['weekday'] = day_from_col[colnum]
					rowspan = int(nthcell['rowspan'])
					# this event makes td tags absent for the next n rows
					vspand[colnum] = rowspan
					# each row is a 30 minute block
					timedata['duration'] = timedelta(minutes=rowspan * 30)
					timedata['start'] = start
					# Map the contents of the event cell to a dict
					fields = map(lambda x: x.string, nthcell.findAll('td'))
					# place the name of this table's EOI in staff/room/student 
					reldata[self.typeid] = [id]
					for field in self.eventconstr:
						c = fields[self.eventconstr.index(field)]
						if c == None:
							c = "Unknown"
						if field == 'weeks':
							# weeks is list(int)
							c = WeekNotation2Array(c)
						elif field != 'title':
							# split reflist and remove whitespace
							c = map(lambda s: s.strip(),c.split(','))
						reldata[field] = c 
					# yield individual lectures
					for week in reldata['weeks']:
						timedata['week'] = week
						y = self.Lecture(reldata,timedata)
						self.Lectures.append(y)
				# add vspan delta to vspanc, and decrement vspanc if possible
				for i in range(colcount):
					vspanc[i] += vspand[i]
					if vspanc[i] >0:
						vspanc[i] = vspanc[i] - 1
			self.hasdata = True


class ProfessorTable(FreshLectureTable):
	clistfilter = "staffarray"
	typeid = "staff"
	eventconstr = ['title','student','weeks','room']
class RoomTable(FreshLectureTable):
	clistfilter = "roomarray"
	typeid = "room"
	eventconstr = ['title','student','weeks','staff']
class KlasTable(FreshLectureTable):
	clistfilter = "studentsetarray"
	typeid = "student"
	eventconstr = ['title','weeks','room','staff']

class OnlineTables:
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
			contents = remotefile.read().decode('latin-1')
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
				# generic post variables
				request = urllib.urlencode({"weeks":"22-36", # FIXME
											"type": tabletype,	
											"filter":"(None)",
											"cbxAvond":"on",
											"cbxZaterdag":"on",
											"dept":dept})
				# add a list of identifiers to the post request
				request = "&".join([request]+map(lambda t: urllib.urlencode({"identifier[]": t.id}),tables))
				# fetch html and parse
				remotefile = urllib.urlopen(self.geturl,request)
				source = remotefile.read()
				remotefile.close()
				soup = BeautifulSoup(source)
				# debug -- save to disk
				#x = open("".join(map(lambda x: x.name,tables)),'w')
				#x.write(soup.prettify())
				#x.close()
				# Iterate through all TIMETABLES in the HTML
				for ttheader in soup.html.body.findAll("table",{"class":"header-border-args"}):
					id = ttheader.find('span',{'class':'header-2-1-1'}).string.strip()
					if id == "":
						id = ttheader.find('span',{'class':'header-2-1-2'}).string.strip()
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

	def byMouth(self,name):
		""" ignore case and spaces """
		if not self.tables:
			self.UpdateCandidates()
		matches = filter(lambda t: t.name.lower().replace(' ','') == name, self.tables)[:1]
		if len(matches):
			return matches[0]
		else:
			return None

class iCalFace:
	""" Lecture -- Ical event glue code """
	class dataobject:
		def __init__(self,**k):
			for (a,b) in k.iteritems():
				setattr(self,a,b)
	class person:
		def __init__(self,name):
			self.name = name
			self.email = name.replace(" ",'') + "@invalid.denayer.be"
	def __init__(self,i):
		self.prep(i)
		todo = ["dtstamp","dtstart","dtend","description", "summary","location","organizer","reqpart"]
		for f in todo:
			g = getattr(self,"_"+f,None)
			if g:
				setattr(self,f,g(i))
	def prep(self,i):
		from dncalendar import WD2Date
		self.staff = map(self.person,i.staff)
		self.students = map(self.person,i.student) 
		self.dtstart = datetime.combine(WD2Date(i.week, i.weekday), i.start)
	def _dtstamp(self,i):
		return datetime.now()
	def _dtstart(self,i):
		return self.dtstart 
	def _dtend(self,i):
		return self.dtstart + i.duration
	def _summary(self,i):
		return i.title
	def _description(self,i):
		return i.title
	def _organizer(self,i):
		return self.staff[0]
	def _reqpart(self,i):
		return self.staff + self.students
	def _location(self,i):
		return self.person(i.room[0])


if __name__ == "__main__":
#if None:
	source = OnlineTables()
	source.UpdateCandidates()
	#['K103'])#['CRAUWELS Herman'])#['Ma EMEM2'])#['SP1'])#['1PBEIE1'])#,
#	for x in iter(source.tables):
#		print repr(x).decode('utf-8')
	timetable = source.getTable(source.byMouth('k104'))
	x = open('/home/thomas/test.ics','w')
	x.write(ical.IcalFile(map(lambda l: iCalFace(l),timetable.Lectures)).toString().encode('utf-8'))
	x.close()
	print "\n".join(map(repr,timetable.Lectures))
# basic unittesting: test all cases
#if None: #__name__ == "__main__":
if __name__ == "__main__":
	source = OnlineTables()
	source.UpdateCandidates()
	timetables = source.getTables(source.tables)

