#!/usr/bin/python
import schedule
import Eoi

class EoiCatalog:
	_tables = []

	def __getattr__(self,name):
		if name != 'tables':
			raise AttributeError
		if self._tables == []:
			self.Update()
		return self._tables

	def Update(self):
		""" Download catalogfiles """
		departments = ['IW','Technologie'] #['ArchitectuurSLB','ArchitectuurSLG']
		source = "http://sws.wenk.be/%s/js/filter.js"
		weekentry = r"""^\s+AddWeeks\s*\(\s*"(\d+)"\s*,\s*\"()\"\s*,\s*form.elements\["weeks"\]\);\s*$"""

		def JSarrayToList(source, varname, depth):
			ret = {}
			# Obtain a list of array store operations
			arrayentry = r"""%s\s*\[\s*(\d+)\s*\]\s*\[\s*(\d+)\s*\]\s*=\s*"(.*)"\s*;"""
			regex = re.compile(arrayentry % varname)
			ops = re.findall(regex, source)
			# Ensurance
			if len(ops) == 0:
				raise Exception("Parse error")
			if len(ops) % depth > 0:
				raise Exception("Parsed invalid number of entries")
			for x in ops:
				n = int(x[0])
				if not n in ret.keys():
					ret[n] = [None, None, None]
				ret[n][int(x[1])] = x[2]
			return ret.values()

		self._tables = []

		for department in departments:
			remotefile = urllib.urlopen(source % department)
			contents = remotefile.read()
			remotefile.close()
			
			for i in JSarrayToList(contents, 'roomarray', 3):
				self._tables.append(Lokaal(i))

			for i in JSarrayToList(contents, 'staffarray', 3):
				self._tables.append(Docent(i))
				
			for i in JSarrayToList(contents, 'studentsetarray', 3):
				self._tables.append(Klas(i))

class LectureListRequest
	pass


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
	
