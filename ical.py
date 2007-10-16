#!/usr/bin/env python
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

# iCal implementation 
# (see http://www.ietf.org/rfc/rfc2445.txt for reference)

import datetime, socket, string

class IcalEvent:
	""" An event, use constructor or populate with data,
		retrieve it's repr() to get data 

		@dtstamp, dtstart, dtend: datetime.Datetime instances
		@description,summary: string instances
		@location: obj w/name
		@organizer: obj w/name email
		@reqpart: [<obj w/name email>] """

	interface = ["dtstamp","dtstart","dtend","description",
				"summary","location","organizer","reqpart"]

	template = """BEGIN:VEVENT
UID:$idhash@$hostname
ORGANIZER;CN=$orgname:MAILTO:$orgemail
$reqpart
DTSTAMP:$dtstamp
DTSTART;TZID="Brussel, Kopenhagen, Madrid, Parijs":$dtstart
DTEND;TZID="Brussel, Kopenhagen, Madrid, Parijs":$dtend
SEQUENCE:0
TRANSP:OPAQUE
SUMMARY;LANGUAGE=nl;ENCODING=QUOTED-PRINTABLE:$summary 
SUMMARY:$summary 
LOCATION:$location
DESCRIPTION;LANGUAGE=nl;ENCODING=QUOTED-PRINTABLE:$description
DESCRIPTION:$description
CATEGORIES:School
CLASS:PUBLIC
STATUS:CONFIRMED
END:VEVENT
"""
	def __init__(self,m = None):
		""" Pass a model instance to this function if you like """
		if m: self.link(m)

	def link(self,m):
		""" Link instance attributes to model """
		for i in self.interface:
			setattr(self,i,getattr(m,i))
	def __repr__(self):
		return self.toString()

	def toString(self):
		""" display text representation of instance attributes """
		# verify all requirements are met
		if None in [getattr(self, x,None) for x in self.interface]:
			return "<incomplete IcalEvent>"
		# Convert timestamps to UTC ascii repr 
		# (thus not having to send along timezone information...)
		dtstamp = self.dtstamp.strftime("%Y%m%dT%H%M%SZ"),
		dtstart = self.dtstart.strftime("%Y%m%dT%H%M%S"),
		dtend   = self.dtend.strftime("%Y%m%dT%H%M%S"),
		# create new strings with result of retrieval of said attrs.
		description =	 "%s" % self.description
		summary =		 "%s" % self.summary
		location =		 "%s" % self.location.name
		# build a string with participant lines glued with newlines
		reqpart = "\n".join("ATTENDEE;ROLE=REQ-PARTICIPANT;CN=%s:MAILTO:%s" % \
							(p.name, p.email) for p in self.reqpart	)
		orgname =	"%s" % self.organizer.name
		orgemail =	"%s" % self.organizer.email
		# create a hash of key 
		hostname = socket.getfqdn()
		idhash = hash((dtstart, dtend, description, summary, location))
		# substitute local variables in the template string where possible
		return string.Template(self.template).substitute(locals())

class IcalFile:
	mime = "Content-type: text/calendar"
	timezone = """BEGIN:VTIMEZONE
TZID:Brussel\, Kopenhagen\, Madrid\, Parijs
BEGIN:STANDARD
DTSTART:20001029T030000
RRULE:FREQ=YEARLY;INTERVAL=1;BYDAY=-1SU;BYMONTH=10
TZNAME:Romance (standaardtijd)
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:20000326T020000
RRULE:FREQ=YEARLY;INTERVAL=1;BYDAY=-1SU;BYMONTH=3
TZNAME:Romance (zomertijd)
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
END:DAYLIGHT
END:VTIMEZONE
"""
	def __init__(self,list = None):
		self.list = list
	def __repr__(self):
		self.toString()

	def toString(self):
		if not self.list:
			return "<Empty Ical File>"
		out = "BEGIN:VCALENDAR\n"
		out += "PRODID:-//TL//PyIcalCode//EN\n"
		out += "VERSION:2.0\n"
		out += "METHOD:REQUEST\n"
		out += self.timezone
		out += "".join(map(lambda x: x.toString(),map(IcalEvent,self.list)))
		out += "END:VCALENDAR"
		return out

class testEvent:
	""" example data model, for test purposes """
	class exampleparticipant: 
		""" example participant model, pass it a number """
		def __init__(self,n):
			self.name = "participant%i" % n
			self.email = "participant%i@email.com" % n
	class o: pass

	def __init__(self,hour):
		""" Create a test event at april first 2007, at the hour given"""
		# our dummy organizer
		self.organizer = self.o()
		self.organizer.name = "Johndoe"
		self.organizer.email = "Johndoe@email.com"
		# ten dummy participants
		self.reqpart = map(self.exampleparticipant,range(10))
		# modstamp today
		self.dtstamp = datetime.datetime.today()
		# april first, hour given
		self.dtstart = datetime.datetime(2007,4,1,hour)
		# event takes one hour
		self.dtend = self.dtstart + datetime.timedelta(hours=1)
		self.description = "Example event"
		self.summary = "Summarytext goes here"
		self.location = self.o()
		self.location.name = "Conference room"


if __name__ == '__main__':
	# output an icalfile with two testevents, one at 10am and one at 12
	print IcalFile([IcalEvent(testEvent(10)),IcalEvent(testEvent(12))])
