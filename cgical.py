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
from swsparser import OnlineTables,iCalFace
import os

def normalize(s):
	s = s.replace(".","")
	s = s.replace("%20","")
	return s.lower()

class icFatSummary(iCalFace):
	""" put location in summary """
	def _summary(self,i):
		return i.title + "@" + i.room[0]

if __name__ == "__main__":
	id = os.environ["REQUEST_URI"].split("?")[0].split('/')[-1:][0]
	id = normalize(id)
	if os.environ["REQUEST_URI"].find('@') >0:
		face = icFatSummary
	else:
		face = iCalFace
	source = OnlineTables()
	source.UpdateCandidates()
	try:
		timetable = source.getTable(source.byMouth(id))
		result = ical.IcalFile(map(lambda x: face(x),timetable.Lectures)).toString().encode('utf-8')
		#statistics
		if not cgi.FieldStorage().getvalue("dev"):
			db=MySQLdb.connect(**dict(zip(['user','passwd','db'],open('../../dbcredentials').read().strip().split('.'))))
			try:
				c = db.cursor()
				if not c.execute("""UPDATE stats SET count=count+1 where id=%s;""", db.escape_string(id)):
					r = c.execute("""INSERT INTO stats (`id`, `count`) VALUES (%s, '1');""" , db.escape_string(id))
				r = c.execute("""SELECT * FROM stats where id=%s;""" , db.escape_string(id))
			except Exception, e:
				pass

		print "Content-type: text/calendar"
		print 
		print result 
	except Exception,e:
		print "Content-type: text/html"
		print 
		print "<html><body><h1>ongeldige id: %s</h1></body></html>" % id
