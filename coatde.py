
class Room(Eoi):
	pass

class Lecturer(Eoi):
	pass

class Student(Eoi):
	pass

class Course:
	title = ""
	Lectures = []
	Attendents = []

	def getLectures(self):
		pass

class Lecture:
	Course = None
	LectureNumber = 0
	Location = None
	Start = None
	Duration = None
