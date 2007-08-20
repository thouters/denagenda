#!/usr/bin/python
import schedule
import Eoi

class LectureTableParser:
	idtype='id'
	days='1-6'
	url= "http://sws.wenk.be/common/get_timetable.php"
	rooster_re = r""" table th th tr td td tr table """
	def fetchone(self,TimeTable):
		""" fetch and parse a table of given identifier and weeks
			weeks for semesters: 1-14, 22-36	"""
		
		getdict = {	"name":"swsform",
					"identifier[]":id, ##
					"weeks":"",
					"objectclass": self.objectclass,	
					"idtype":"id",
					"periods":self.periods,
					"days":"1-6",
					"template": self.template
		}

		remotefile = urllib.urlopen(url,urllib.urlencode(getdict))
		c = remotefile.read()
		remotefile.close()
		f = open('./output.html','w')
		f.write(c)
		f.close()

		raise NotImplementedError

class StaffRoosterParser(TableParser):
	objectclass = "staff"
	periods = "1-56"
	template = "DN+Docent+individueel"
	
class LocationRoosterParser(TableParser):
	objectclass = "location"
	periods = "1-56"
	template = "DN+Zaal+individueel"

class StudentRoosterParser(TableParser):
	objectclass = "location"
	periods = "1-40"
	template = "DN+Studentenset+individueel"


if __name__ == "__main__":
	a = StaffRoosterParser()
	a.fetchone()
	
