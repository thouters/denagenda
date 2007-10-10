#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()
import ical
from parsers import WebsiteSource

if __name__ == "__main__":
	id = cgi.FieldStorage().getfirst("id")
	source = WebsiteSource()
	source.UpdateCandidates()
	wanted = [source.byName(id)]
	timetables = source.getTables(wanted)
	print "Content-type: text/calendar"
	print 
	print ical.IcalFile(map(ical.IcalGlue,timetables[0].Lectures)).toString().encode('utf-8')
