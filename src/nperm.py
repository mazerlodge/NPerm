#!/usr/bin/python 

import sys 
from ArgTools import ArgParser 

class NPermEngine: 

	bInDebug = False 
	targetVal = 0 
	nElements = 0 
	skipList = []
	useList = [] 
	workingList = []

	def __init__(self, argv): 

		if (not self.parseArgs(argv)): 
			self.showUsage()


	def showUsage(self):
		print("Usage: nperm -t targetVal -n numElements [-u csvList] [-debug]")

	def debugMsg(self, msg): 

		if (self.bInDebug): 
			print(msg)


	def parseArgs(self, argv): 
		bRval = True
		ap = ArgParser(argv) 
		self.bInDebug = False 

		# expected params are -t -n (-u optional) (-debug) 
		if (ap.isInArgs("-debug", False)):
			self.bInDebug = True 

		if (ap.isInArgs("-t", True)): 
			self.targetVal = int(ap.getArgValue("-t"))
		else: 
			bRval = False 
			self.debugMsg("Parse Arg -t failed.")

		if (ap.isInArgs("-n", True)): 
			self.nElements = int(ap.getArgValue("-n"))
		else: 
			bRval = False 
			self.debugMsg("Parse Arg -n failed.")
		
		if (ap.isInArgs("-s", True)): 
			skipRaw = ap.getArgValue("-s")
			skipListAsChar = skipRaw.split(",")
			for x in skipListAsChar:
				self.skipList.append(int(x))

		if (ap.isInArgs("-u", True)): 
			useRaw = ap.getArgValue("-u")
			useListAsChar = useRaw.split(",")
			for x in useListAsChar:
				self.useList.append(int(x))

		return(bRval)

	def showWorkingList(self):

		for e in self.workingList:
			print("%d ," % int(e)),

		print(" ")


	def sumWorkingList(self): 

		rval = 0 

		for e in self.workingList:
			rval += e

		return(rval) 

	def isElementListLengthValid(self): 

		bRval = False 

		wll = len(self.workingList)

		if (wll == self.nElements):
			bRval = True

		if (not bRval):
			self.debugMsg("Element list length %d is not valid" % wll)

		return bRval


	def isElementListSumValid(self): 

		bRval = False 

		wls = self.sumWorkingList()

		if (wls == self.targetVal):
			bRval = True

		if (not bRval):	
			self.debugMsg("Element list sum %d is not valid." % wls)

		return bRval

	def isSkipVal(self, val): 
		bRval = False 

		for av in self.skipList:
			if (av == val): 
				bRval = True 
				break 

		return(bRval) 
			
	def go(self): 

		for m in range(9,0,-1):
			self.debugMsg("Processing m=%d" % m) 
			r = self.targetVal 
			self.workingList = []
			for c in range(m,0,-1): 
				if (self.isSkipVal(c)):
					self.debugMsg("Skipping c=%d" % c) 
					continue 

				if (c>r):
					self.debugMsg("Skipping c>r w/ c=%d and r=%d" % (c, r)) 
					continue 
				else: 
					r -= c
					self.workingList.append(c) 
					self.debugMsg("Using c=%d" % c) 
				
				if (r==0):
					break
			
			if(self.isElementListLengthValid() and self.isElementListSumValid()):
				self.showWorkingList()


# Entry point 
np = NPermEngine(sys.argv)
np.go() 

