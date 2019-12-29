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

	def isRemainderZeroPremature(self, c, r): 
		# Return true if the candidate value would drive the remainder to zero prematurely 
		bRval = False

		if (r-c == 0) and (len(self.workingList) < self.nElements-1):
			bRval = True 

		self.debugMsg("\t\tiRZP w/ c/r/len %d / %d / %d / %s" % (c, r, len(self.workingList), bRval))

		return(bRval) 
			
	def go(self): 

		# set up single digit skipping in range 8 - 3 
		for skipDigit in range(9, 2, -1): 
			# on first cycle (where skipDigit = 9) don't skip anything
			# Note: user input skip values via -s parameter will still apply on first cycle only.
			if (skipDigit < 9): 
				self.skipList = [skipDigit]

			for m in range(9,0,-1):
				self.debugMsg("Processing m=%d" % m) 
				r = self.targetVal 
				self.workingList = []
				for c in range(m,0,-1): 
					if (self.isSkipVal(c)):
						self.debugMsg("\tSkipping skipVal c=%d" % c) 
						continue 

					if (c>r):
						self.debugMsg("\tSkipping c>r w/ c=%d and r=%d" % (c, r)) 
						continue 
					else: 
						# c fits, but would it drive to zero prematurely.
						if (self.isRemainderZeroPremature(c,r)):
							self.debugMsg("Skipping premature zero w/ c=%d and r=%d" % (c, r)) 
							continue
						r -= c
						self.workingList.append(c) 
						self.debugMsg("\tUsing c=%d" % c) 
					
					if (r==0):
						break
				
				if(self.isElementListLengthValid() and self.isElementListSumValid()):
					self.showWorkingList()


# Entry point 
np = NPermEngine(sys.argv)
np.go() 

