#!/usr/local/bin/python2.4
import cgi
import cgitb; cgitb.enable()
import ical
import dncalendar
from parsers import WebsiteSource
if __name__ == "__main__":
	id = cgi.FieldStorage().getfirst("id")
	source = WebsiteSource()
	source.UpdateCandidates()
	wanted = [source.byName(id)]
	timetable = source.getTables(wanted)
	if not timetable:
		print "Content-type: text/html"
		print 
		print "ongeldige id: %s" % id
	else:
		result = ical.IcalFile(map(dncalendar.IcalGlue,timetable[0].Lectures)).toString().encode('utf-8')
		print "Content-type: text/calendar"
		print 
		print result 
		
