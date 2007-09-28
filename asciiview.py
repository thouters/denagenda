#!/bin/env python
from uurrooster import Uurrooster
from datetime import date, timedelta

weekdagen = ["Maandag","Dinsdag","Woensdag","Donderdag","Vrijdag","Zaterdag","Zondag"]

for groep in ("2pbei1","2pbei2","2pbei3"):
	groepdata = Uurrooster(groep)
	groepdata.retrieve()
	teller = 0
	for les in groepdata.lessen:
		if les['begin'].hour == 8:
			teller = teller + 1
		if les['groepen'] == range(1,13):
			print les['groepen'] 
	print "%s heeft %i lessen om 8 uur dit semester" %(groep, teller)
		
