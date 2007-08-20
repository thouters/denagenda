
class Rooster:
	pass

class Attendee:
	name = ""
	organisation = None
	key = ""

	def __init__(self,*a,**k):
		if (len(a) == 1):
			l = a[0]
			self.name = l[0]
			self.organisation = l[1]
			self.key = l[2]


class Lokaal (Attendee):
	pass

class Docent (Attendee):
	pass

class Klas (Attendee):
	pass

class Appointment:
	""" Representation of an Appointment """
	title = None
	location = None
	attendees = []
	President = None
	date = None
	# scheduled = [{weekday: None, hour: None, week: None}]

	#Lecture[(weekday, hour, weeks[]),..]
class Location:
	reference = None
	site = None
	id = None
	pass


