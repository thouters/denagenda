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

	def UpdateCandidates(cls):
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
	# find all timetables given and start work on them.
	#<table class="header-border-args" border="0" cellspacing="0" width="100%">
	for ttheader in contents.find('table',attrs={'class':'header-border-args'}):
		colday = []
		# HEADER - has some crucial data
		#<span class="header-3-0-1"> 22 </span>
		#<span class="header-3-0-3"> 36 </span>
		wspan = (ttheader.find('span',attrs={'class':'header-3-0-1'}),ttheader.find('span',attrs={'class':'header-3-0-3'})
		#<span class="header-2-1-0"> Studentenrooster: </span>
		ttype = ttheader.find('span',attrs={'class':'header-2-1-0'})
		#<span class="header-2-1-1">2PBEIE3</span>
		tname = ttheader.find('span',attrs={'class':'header-2-1-1'})
		# TIMETABLE HEAD- actual schedule data
		# jump to the timetable
		#<table class="grid-border-args" cellspacing="0">
		ctable = ttheader.findNextSibling('table',attrs={'class':'grid-border-args'})
		# iterate through columns of the header line
		header = ctable.find('tr')
		#<td class="col-label-one" colspan="3"> dinsdag </td>
		for i,col in enumerate(header.findAll('td',attrs={'class':'col-label-one'})):
			#iterate through spanning column headers
			span = int(col['colspan'].strip())
			colday.extend([i]*span)
		# colday should now be like [0,0,0,1,1,2,3,3,3,3]
		# TIMETABLE datarows
		for row in header.findNextSiblings('tr'):
			#first column contains start hour of the row
			sh = row.find('td')
			newsh = sh.contents.strip()
			# support for events starting at :15 and :45 
			if newsh != '':
				starthour = starthour + timedelta(minutes=15)
			else:
				starthour = newsh
			# loop through columns, these can contain events starting at starthour
			for colnum, column in enumerate(sh.findNextSiblings('td')):
				# check the cell for presence of a table
				#<table class="object-cell-args" border="0" cellspacing="0" width="100%">
				container = column.find('table',attrs={'class':'object-cell-args'})
				# If the cell has an event, we hit the bull
				if container:
					# we can determine the weekday from the value of colday
					weekday = colday[colnum]
					# rowspan count represents blocks of 15 minutes
					#<td class="object-cell-border" colspan="1" rowspan="12">
					duration = int(column['rowspan'].strip()) * 15
	
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

