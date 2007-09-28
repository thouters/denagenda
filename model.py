from sqlobject import *
import datetime

__connection__ = "sqlite:/:memory:"

# Calculate first day of the current academic year.
first = datetime.date.today().replace(month=9, day=1)
# 1sept dit jaar reeds voorbij is, academiejaar begon vorig jaar
if datetime.date.today() < first:
	first= first.replace(year = first.year - 1)	
# 3 weken na de eerste werkdag van september (FIXME)
first = first + datetime.timedelta(days = 21 + 7 - first.weekday()) 

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
		self.mtime = datetime.datetime.now()
		day = first + datetime.timedelta(days = (int(self.weekday) - 1), weeks = int(self.week) - 1)
		self.dtstart = datetime.datetime.combine(day,datetime.time(self.begin/60,self.begin%60))
		self.dtend = self.dtstart + datetime.timedelta(minutes = self.span)

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

