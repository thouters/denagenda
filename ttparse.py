#!/usr/bin/python
from model import *
import ical

class STP:
	def __init__(self,file = None):
		if file:
			self.ParseFromFile(file)

	def ParseFromFile(self,fname):
		x = open(fname)
		y = x.read()
		x.close()
		self.ParseFromString(y)
	def ParseFromString(self,y):
		a = y.split('\n')[:-1]
		b = map(lambda x: x.split(','),a)
		c = map(lambda x: [x[0].split(';')]+x[1:],b)

		for i in c:
			weken = map(int,i[0])
			wdag = int(i[1])
			start = i[2]
			stop = i[3]
			b = int(start.split('.')[0]) *60 + int(start.split('.')[1])
			e = int(stop.split('.')[0]) *60 + int(stop.split('.')[1])
			s = e - b
			lokaal = i[4]
			titel = i[5]
			docent = i[6]
			#print weken, wdag, start, stop, b, e, s, lokaal, titel, docent
			# professor en lokaal ophalen
			p = Professor.select(Professor.q.name==docent)
		 	p = ((p.count() and p.getOne()) or Professor(name=docent))
			r = Room.select(Room.q.name==lokaal)
 			r = ((r.count() and r.getOne()) or Room(name=lokaal))
			# lecture ophalen (als ze j
			c = Course.select(AND(Course.q.name==titel))
 			c = ((c.count() and c.getOne()) or Course(name=titel))
			if not p in c.staff:
				c.staff.append(p)
			#print p,r,c
			for w in weken:
				l = Lecture.select(AND(	Lecture.q.week == w,
										Lecture.q.begin == b,
										Lecture.q.span == s,
										Lecture.q.weekday == wdag,
										Course.q.name == titel,
										Room.q.name == lokaal))

		 		l = ((l.count() and l.getOne()) or Lecture(week=w, begin=b,span=s,weekday=wdag,course=c,room=r))
				l.SetUpdated()
				#print l

if __name__=="__main__":
	Course.createTable()
	Professor.createTable()
	Room.createTable()
	Lecture.createTable()
	Klas.createTable()
	Group.createTable()

	s = STP('lessenrooster.txt')
	print "----------------------------"
	x = list(Lecture.select(AND(Room.q.name=="A014", Lecture.q.week==2)))
	n = ical.IcalFile(x)
	print list(Professor.select())
	print list(Room.select())
	print list(Lecture.select())
	print "----------------------------"
	print n	


