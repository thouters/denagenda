#!/usr/bin/python
import schedule
import Eoi

class RosterListIterator:
	""" Iterates over html and yields roster iterators """	
	#hak html in stukken
	pass

class RosterIterator:
	""" Iterates over a Roster and yields dicts representing lectures """
	# instantieer parser
	# herken type rooster
	pass

class RosterSource:
	class __metaclass__(type):
		def UpdateCandidates(self):
			"""	Populate the database tables with lists of Rosters
				that can be requested
			"""
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
	
			tables = []
	
			for department in departments:
				remotefile = urllib.urlopen(source % department)
				contents = remotefile.read()
				remotefile.close()
				
				for i in JSarrayToList(contents, 'roomarray', 3):
					tables.append(Lokaal(i))

				for i in JSarrayToList(contents, 'staffarray', 3):
					tables.append(Docent(i))
				
				for i in JSarrayToList(contents, 'studentsetarray', 3):
					tables.append(Klas(i))

		def getSource(self, what=None):
			"""	Update the database with new data from the internet
				@param what: instance of obj to update | list
			"""
			""" fetch and parse a table of given identifier and weeks
				weeks for semesters: 1-14, 22-36	
			"""
			if what == None:
				raise AttributeError
			elif what.__class__ != list:
				what = [what]

			url= "http://sws.wenk.be/common/get_timetable.php"
		
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

		def Update(self, what = None):
			"""	Update the database with new data from the internet
				@param what: instance of obj to update | list
			"""
			for roster in rosterListIterator(self.getSource(what))
				for lecture in roster:
					print lecture
					# verify with database
			
class TableParser:
	idtype='id'
	days='1-6'
	rooster_re = r""" table th th tr td td tr table """
	
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
	RosterSource.UpdateCandidates()	

