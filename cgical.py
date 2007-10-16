#!/usr/local/bin/python2.4
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

import cgi
import cgitb; cgitb.enable()
import ical
import dncalendar
import MySQLdb
from swsparser import OnlineTables

if __name__ == "__main__":
	db=MySQLdb.connect(user="dauser",passwd="dapasswd",db="denagenda")
	c = db.cursor()
	id = cgi.FieldStorage().getfirst("id")
	r = c.execute("UPDATE stats SET count=count+1 where id='%s';" % db.escape_string(id))

	c=	r.fetchone()
	print "Content-type: text/html"
	print 
	print "result: %s" % repr(c)
	if None:
		source = OnlineTables()
		source.UpdateCandidates()
		wanted = [source.byName(id)]
		timetable = source.getTables(wanted)
		if not timetable:
			print "Content-type: text/html"
			print 
			print "ongeldige id: %s" % id
		else:
			result = ical.IcalFile(map(lambda x: x.iCalFace(),timetable[0].Lectures)).toString().encode('utf-8')
			print "Content-type: text/calendar"
			print 
			print result 
		
