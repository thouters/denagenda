
from sqlobject import SQLObject, StringCol, IntCol, DateCol, PickleCol,ForeignKey,MultipleJoin,RelatedJoin,DatabaseIndex

__connection__ = "sqlite://:memory:"

class Room(SQLObject):
	roomid			= StringCol(length=4,alternateID=True)

class Lecture(SQLObject):
	course			= ForeignKey('Course')
	location		= ForeignKey('Room')
	presidents		= RelatedJoin('Professor')
	audience		= RelatedJoin('StudyGroup')
	SessionNumber	= IntCol()	
	#Duration		= Timedelta() (minutes?)
	#date, begintime, week, weekday

class Professor(SQLObject):
	pass

class StudyGroup(SQLObject):
	pass
	

class Course(SQLObject):
	pass
	
class Klas(SQLObject):
	pass

class Study(SQLObject):
	pass
