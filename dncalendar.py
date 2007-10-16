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

from datetime import datetime, date, timedelta, time

""" Utility functions to cope with the De Nayer week system"""

nlwd = ['Maandag','Dinsdag','Woensdag','Donderdag','Vrijdag','Zaterdag','Zondag']

def GetFirstDay(day = date.today()):
	""" Calculate first day of the academic year.given day belongs to """
	# get september first 
	first = day.replace(month=9, day=1)
	if day < first:
		# the academic year started last calender year
		first= first.replace(year = first.year - 1)	
	# Courses kick off the third week of september.
	return first + timedelta(days = 21 + 7 - first.weekday()) 

septfirst = GetFirstDay()

def WD2Date(week,weekday):
	""" return the Date of a collegeday """
	return septfirst + timedelta(days = (int(weekday) - 1), weeks = int(week) - 1)

def HourDotMinute2Time(t):
	# format from ^hour.minute(.*)$ string
	return time(*map(int,t.split(':')[:2]))

def WeekNotation2Array(s):
	o = []
	for n in s.split(','):
		x = map(int,n.split('-'))
		if len(x) > 1:
			o.extend(range(x[0],x[1]+1))
		else:
			o.extend(x)
	return o

def IcalGlue(x):
	""" Lecture -- Ical event glue code """
	class y: pass
	x.location = y()
	x.organizer = y()
	x.dtstamp = datetime.now()
	x.dtstart = datetime.combine(WD2Date(x.week, x.weekday), x.start)
	x.dtend = x.dtstart + x.duration
	x.summary = x.course.name
	x.description = x.summary
	x.location.name = x.room.name
	x.organizer.name = x.professor.name
	x.organizer.email = "iemand@denayer.wenk.be"
	x.reqpart = [x.organizer]
	return x

