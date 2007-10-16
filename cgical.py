#!/usr/local/bin/python2.4
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
		
