from sqlobject import *
import datetime
from dncalendar import *
from datetime import datetime, timedelta, time

__connection__ = "sqlite:/:memory:"


class Klas(SQLObject):
	name = StringCol()
	groups = MultipleJoin('Group')
	courses = MultipleJoin('Course')

class Group(SQLObject):
	part = IntCol()
	klas = ForeignKey("Klas")
	lectures = MultipleJoin('Lecture')

class Professor(SQLObject):
	name = StringCol()
	courses = MultipleJoin('Course')
	lectures = MultipleJoin('Lecture')
	
class Course(SQLObject):
	name = StringCol()
	enrolled = MultipleJoin('Klas')
	staff = MultipleJoin('Professor')
	lectures = MultipleJoin('Lecture')

class Lecture(SQLObject):
	# General
	course = ForeignKey('Course')
	audience = MultipleJoin('Group')
	room = ForeignKey('Room')
	# Raw data
	# begin, span = minutes.
	week = IntCol()
	weekday = IntCol()
	begin = IntCol()
	span = IntCol()
	# Buffered
	dtstamp = DateTimeCol(default=None)
	dtstart = DateTimeCol(default=None)
	dtend = DateTimeCol(default=None)
	def SetUpdated(self):
		""" Update timestamps and mtime """
		#FIXME, doe dit in toewijzing _set_mtime
		#hash hier ook in verwerken???
		self.mtime = datetime.now()
		self.dtstart = datetime.combine(	WD2Date(self.week, self.weekday),
											time(self.begin / 60, self.begin % 60)	)
		self.dtend = self.dtstart + timedelta(minutes = self.span)

	# iCal-glue code
	def _get_description(self):
		""" Print much info, like attendents, profs,... """
		pass
	def _get_summary(self):
		return self.course.name
	def _get_location(self):
		return self.room
	def _get_reqpart(self):
		return list(self.audience) + list(self.course.staff)
	def _get_organizer(self):
		class organizer: pass
		x = organizer()
		x.name = "put organizer here"
		x.email = "email@example.com"
		return x
		
class Room(SQLObject):
	name = StringCol()
	lectures = MultipleJoin('Lecture')

