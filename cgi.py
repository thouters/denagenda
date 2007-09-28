#!/usr/bin/env python

# * ----------------------------------------------------------------------------
# * "THE BEER-WARE LICENSE" (Revision 42):
# * <thomas.langewouters@skynet.be> wrote this file. As long as you retain this notice you
# * can do whatever you want with this stuff. If we meet some day, and you think
# * this stuff is worth it, you can buy me a beer in return.
# * Thomas Langewouters
# * ---------------------------------------------------------------------------


import cgi
import cgitb; cgitb.enable()

def uurrooster2ical(uurrooster):
	calitem = ICalEvent()
	output = ""
	for les in uurrooster.lessen:
		#organizer
		calitem.organizer = les['docenten'][0]
		#organizermail
		calitem.organizermail = les['docenten'][0] + "@docent.denayer.wenk.be"
		
		#reqpart {name: email}
		rp = {}

		if les['groepen'] == range(1,13):
			# klasvak
			klas_groep = str(uurrooster.jaar) + str(uurrooster.richting)
			rp[klas_groep] = klas_groep + "@denayer.wenk.be"
		else:
			for nummer in les['groepen']:
				klas_groep = str(uurrooster.jaar) + str(uurrooster.richting) + str(nummer)
				rp[klas_groep] = klas_groep + "@denayer.wenk.be"

		calitem.reqpart = rp
		#uid		unieke ID
		#?
		#dtstamp		tijd waarop het event gepland werd
		calitem.dtstamp = datetime.now(les['begin'].tzinfo)
		#dtstart		begintijd (datetime obj)
		calitem.dtstart = les['begin']
		#dtend		eindtijd (datetime obj)
		calitem.dtend = les['einde'] 
		#summary
		calitem.summary = les['naam']
		#location
		calitem.location = les['lokaal']
		#description
		calitem.description = les["type"] + " door " + calitem.organizer + " in " + les['lokaal']
		output += calitem.put()
	return output

klas = cgi.FieldStorage().getfirst("klas")
mijnklas = Uurrooster(klas)
mijnklas.retrieve()
print "Content-type: text/calendar"
print 
print out
