#!/usr/bin/python
import re
import urllib
from schedule import *
import schedparser



if __name__ == "__main__":
	a = RoosterCatalog()
	for i in a.tables:
		print i.name, i.__class__
