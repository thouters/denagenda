#!/usr/bin/python
# from model import *
import ical
import weakref
from dncalendar import *
from datetime import datetime, timedelta, time

class STP:
	class KeyClass:
		""" test implementation of table with no double values """
		email = 'example@email.com'
		_instances = set()
		@classmethod
		def unique(cls,name):
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
	class Room(KeyClass): pass
	class Course(KeyClass): pass
	class Professor(KeyClass): pass

	class Klas: pass
	class Lecture: pass
	class Event: pass
	Events = []
	
	def totime(t):
		# format from ^hour.minute(.*)$ string
		return time(*map(int,t.split('.')[:2]))
	
	linelayout = (	# chop list of weeks separated by ';', convert to int
					('weeks',	lambda x: map(int,x.split(';'))),
					# weeknumber is an integer
					('weekday',	int),
					# conventional time notation to time object
					('start',totime),
					('end',totime),
					# one-to-many relations
					('room',Room.unique),
					('course',Course.unique),
					('professor',Professor.unique)	)

	def __init__(self,file = None):
		if file:
			self.ParseFromFile(file)
	def __iter__(self):
		return iter(self.Events)
		
	def ParseFromFile(self,fname):
		x = open(fname)
		y = x.read()
		x.close()
		self.ParseFromString(y)

	def ParseFromString(self,sContents):
		# split string into lines (discard 'line' between last \n and EOF)
		lines = sContents.split('\n')[:-1]
		# chop each line on comma's
		clines = map(lambda x: x.split(','),lines)
		# process each line with ProcessLine	
		self.lectures = []
		self.lectures = map(self.ProcessLine,clines)

	def ProcessLine(self,line):
		l = self.Lecture()
		for el,rule in zip(line,self.linelayout):
			setattr(l,rule[0],rule[1](el))
		self.lectures.append(l)
		
		for w in l.weeks:
			e = self.Event()
			e.week = w
			for rule in self.linelayout:
				setattr(e,rule[0],getattr(l,rule[0]))
			e.dtstamp = datetime.now()
			e.location = e.room
			e.organizer = e.professor
			day = WD2Date(e.week, e.weekday)
			e.dtstart = datetime.combine(day, e.start)
			e.dtend = datetime.combine(day, e.end)
			e.description = e.course.name
			e.summary = e.course.name
			e.reqpart = [e.professor]
			self.Events.append(e)

if __name__=="__main__":
	s = STP('txtsrc/sp1.txt')
	print ical.IcalFile(s)
