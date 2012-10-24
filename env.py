'''Class environment definition.

.. module:: env
   :platform: Unix, Windows
   :synopsis: The module containing the main class.
   
.. moduleauthor:: Alessandro Filisetti <alessandro.filisetti@unibo.it>

'''

import sys, os
import time
import agents as ag
import tech
import random as ran
import cPickle as pickle
import shutil 
import copy
import csv
from xml.dom.minidom import Document

class environment:
	'''Class environment definition.	
	'''
	
	def __init__(self, tmpPath):
		'''Constructor '''
		# Parameters file name and path
		paramFile = tmpPath + "init.conf"

		# Open Param file 
		try:
			fid = open(paramFile, 'r')
		except:
			print 'impossible to load ', paramFile; sys.exit(1)
			
		self.simPath = os.path.abspath(tmpPath)

		# Read reaction probability from configuration file
		for line in fid:
			strLine = line.split('=')
			if strLine[0] == "randomSeed":
				self.randomSeed = int(strLine[1])
			if strLine[0] == "agents":
				self.Nagents = int(strLine[1])				
			if strLine[0] == "months":
				self.months = int(strLine[1])	
			if strLine[0] == "xMaxPos":
				self.xMaxPos = int(strLine[1])	
			if strLine[0] == "yMaxPos":
				self.yMaxPos = int(strLine[1])
			if strLine[0] == "minIrradiation":
				self.minIrradiation = int(strLine[1])
			if strLine[0] == "minNrgDim":
				self.minNrgDim = int(strLine[1])
			if strLine[0] == "maxNrgDim":
				self.maxNrgDim = int(strLine[1])
			if strLine[0] == "ratioInternalCapital":
				self.ratioInternalCapital = float(strLine[1])
			if strLine[0] == "invLength":
				self.invLength = int(strLine[1])
			if strLine[0] == "loanLength":
				self.loanLength = int(strLine[1])	
			if strLine[0] == "intRiskRate":
				self.intRiskRate = float(strLine[1])
			if strLine[0] == "socialLobby":
				self.socialLobby = float(strLine[1])
			if strLine[0] == "debugLevel":
				self.debugLevel = float(strLine[1])									
				
		if self.randomSeed == 0:
			#! Set randomly the random state and store it in a file
			ran.seed(int(time.time()))
			self.saveRandomSeed()
		else:
			self.loadRandomSeed()																																														
																				
		# FitnessList and amountList and fitnessSigma have to be of the same length
		self.allAgents = []
		
		# Technologies
		self.allTechs = []
		self.allTechsID = [] # Useful to speed up the computation
		
		# STAT VARIABLES
		self.totCO2 = []
		self.totDebt = []
		self.totCosts = []
		self.tottotCO2 = []
		self.tottotDebt = []
		self.tottotCosts = []
		self.totTechNRGdist = []
		self.totTechKWHdist = []
		self.totTechKWdist = []
		self.tottotTechNRGdist = []
		self.tottotTechKWHdist = []
		self.tottotTechKWdist = []
		
		# CREATE SIMULATION FOLDER
		self.simFolder = ''
	
	# --------------------------------------------------------------|
	# FUNCTION TO RESET SIMULATIONS (USED WITH DIFFERENT RANDOM SEED|
	# --------------------------------------------------------------|
	def resetSimulation(self):	
		'''Function to reset simulation'''

		self.allAgents = []
		
		# Technologies
		self.allTechs = []
		self.allTechsID = [] # Useful to speed up the computation
		
		# STAT VARIABLES
		self.tottotCO2.append(self.totCO2)
		self.tottotDebt.append(self.totDebt)
		self.tottotCosts.append(self.totCosts)
		
		self.tottotTechNRGdist.append(self.totTechNRGdist)
		self.tottotTechKWHdist.append(self.totTechKWHdist)
		self.tottotTechKWdist.append(self.totTechKWdist)
		
		self.totCO2 = []
		self.totDebt = []
		self.totCosts = []	
		self.totTechNRGdist = []
		self.totTechKWHdist = []
		self.totTechKWdist = []
			
				
	# --------------------------------------------------------------|
	# SAVE RANDOM SEED 												|
	# --------------------------------------------------------------|
	
	def saveRandomSeed(self):
		'''Function to save the random seed'''
		
		with open('rndstate.dat', 'wb') as f:
			pickle.dump(ran.getstate(), f)
			
			
	
	# --------------------------------------------------------------|
	# LOAD RANDOM SEED  											|	
	# --------------------------------------------------------------|
	
	def loadRandomSeed(self):
		'''Function to load a previously saved random seed'''
		
		if os.path.exists('rndstate.dat'):
			# Restore the previously saved sate
			print 'Found rndstate.dat, initializing random module'
			with open('rndstate.dat', 'rb') as f:
				state = pickle.load(f)
			ran.setstate(state)
		else:
			# Use a well-known start state
			print 'No rndstate.dat, seeding a random state'
			ran.seed(int(time.time()))
	
	
	
	# --------------------------------------------------------------|
	# CREATE POPULATION 											|	
	# --------------------------------------------------------------|	
	
	def createFolderAndSaveInitialConditions(self, tmpPar):
		'''Function to create the simulation folder and save the initial conditions'''
		
		#: this is the folder name
		self.simFolder = time.strftime("%y%m%d_%H_%M") + "_" + str(tmpPar)
		
		if not os.path.exists(os.path.join(self.simPath,self.simFolder)): os.makedirs(os.path.join(self.simPath,self.simFolder)) 
		#Copy file into results folder (copy2 because also file metadata are copied)
		shutil.copy2("./rndstate.dat",os.path.join(self.simPath,self.simFolder,"rndstate.dat"))
		shutil.copy2("./init.conf",os.path.join(self.simPath,self.simFolder,"init.conf"))
	
	
	
	# --------------------------------------------------------------|
	#: CREATE POPULATION 											|
	# --------------------------------------------------------------|
	
	def createPopulation(self):
		'''Function to create the population
    	'''
		for i in range(0,self.Nagents):
			self.allAgents.append(ag.agents(self.debugLevel,i, ran.uniform(0,self.xMaxPos),ran.uniform(0,self.yMaxPos), \
			                                ran.randint(self.minNrgDim, self.maxNrgDim),ran.uniform(0,self.socialLobby),\
			                                ran.uniform(self.minIrradiation,1), self.intRiskRate, self.ratioInternalCapital, self.invLength ) )
			
		self.genDistanceLists()
	
	
	
	# --------------------------------------------------------------|		
	# SHOW POPULATION 												|
	# --------------------------------------------------------------|	
	
	def printPopulation(self):
		''' Function to output some parameters of the population
		
		>>> --------------
		- AGENT 4
		|- Coordinates: 12.3243 32.3432 - EN: 345
		
		:returns:  void.

		'''
		count = 1
		if self.debugLevel == 0:
			for i in self.allAgents:
				print "--------------"
				print "- AGENT ", i.ID
				print "\t|- Coordinates: ", i.x, " ", i.y, " - EN: ", i.totEnergyNeed
				count = count + 1
			
		
		
	# --------------------------------------------------------------|
	# PRINT PARAMETERS 												|
	# --------------------------------------------------------------|
			
	def printParams(self):
		''' Function to print all simulation parameters (e.g.)
		
		>>> |- SYSTEM PARAMS ---"
		  |- Simulation results path: ~/path/of/the/sim
		  |- PARAMETERS ---
		  |- Random Seed: 0
		  |- Number of Agents: 100
		  |- Number of Months: 360
		  |- X: 1000
		  |- Y: 1000
		  |- minIrradiation: 100
		  |- minNrgDim: 1
		  |- maxNrgDim: 100
		  |- ratioInternalCapital: 23
		  |- invLength: 20
		  |- loanLength: 10
		  |- intRiskRate: ", self.intRiskRate

		'''
		print "|- SYSTEM PARAMS ---"
		print " |- Simulation results path: ", self.simPath
		print "|- PARAMETERS ---"
		print " |- Random Seed: ", self.randomSeed
		print " |- Number of Agents: ", self.Nagents
		print " |- Number of Months: ", self.months
		print " |- X: ", self.xMaxPos
		print " |- Y: ", self.yMaxPos
		print " |- minIrradiation: ", self.minIrradiation
		print " |- minNrgDim: ", self.minNrgDim
		print "	|- maxNrgDim: ", self.maxNrgDim
		print "	|- ratioInternalCapital: ", self.ratioInternalCapital
		print "	|- invLength: ", self.invLength
		print "	|- loanLength: ", self.loanLength
		print "	|- intRiskRate: ", self.intRiskRate
		
		
		
	# --------------------------------------------------------------|
	# Function to generate the distance matrix between agents 		|
	# --------------------------------------------------------------|
	
	def genDistanceLists(self):
		''' Function to generate the distances matrix containing all the distances between agents'''
		
		# For each agents the distance from the other agents is computer and inserted in the matrix
		ID_r = 0;
		for singleAgent in self.allAgents:
			ID_c = 0;
			for ag_col in self.allAgents:
				# Pitagora to compute the distance between two different point
				singleAgent.distanceList.append(pow(pow((singleAgent.x - ag_col.x),2) + pow((singleAgent.y - ag_col.y),2),0.5))
				ID_c = ID_c + 1
			ID_r = ID_r + 1 
		
	# --------------------------------------------------------------|
	# Function to create the three default technologies				|
	# --------------------------------------------------------------|
		
	def createThreeDefaultTechs(self, tmpPar):
		'''Function to create the three default technologies
		   	def __init__(self, tmpID = 0, tmpEff = 0, tmpST = 0, tmpTotTime = 0, tmpDecay = 0, tmpCost = 0, tmpPcost = 0, tmpRate = 0,\
	             tmpCo2 = 0, tmpTransportCosts = 0, tmpLoanLength = 10, tmpLifeDuration = 50, tmpIncList = None, tmpFromKWH2KW = 100, \
	             tmpSolarBased = 0, tmpX = 0, tmpY = 0):
	    '''
		#self.allTechs.append(tech.tech(0,1,0,self.months,0,0.25,0,0,25,0,self.loanLength,self.invLength,[0,0,0,0,0],100,0))
		#self.allTechsID.append(0)
		#self.allTechs.append(tech.tech(1,1,0,self.months,0,0.01,3000,0.04,10,0.003,self.loanLength,self.invLength,[0,0.05,0,0,10],100,0,ran.uniform(0,self.xMaxPos),ran.uniform(0,self.yMaxPos)))
		#self.allTechsID.append(1)
		#self.allTechs.append(tech.tech(2,1,0,self.months,0,-0.3,3000,0.04,5,0,self.loanLength,self.invLength,[0,0.05,0,0,10],100,1))
		#self.allTechsID.append(2)
		self.allTechs.append(tech.tech(0,1,0,self.months,0,0.08 ,  0,0   ,25,0    ,self.loanLength,self.invLength,[0,0,0,0,0],100,0))
		self.allTechsID.append(0)
		self.allTechs.append(tech.tech(1,1,0,self.months,0,0.02 ,300,0.04,10,0.003,self.loanLength,self.invLength,[0,0,0,0,0],100,0,ran.uniform(0,self.xMaxPos),ran.uniform(0,self.yMaxPos)))
		self.allTechsID.append(1)
		self.allTechs.append(tech.tech(2,1,0,self.months,0,-0.07,tmpPar,0.04, 5,0    ,self.loanLength,self.invLength,[0,0,0,0,0],100,1))
		self.allTechsID.append(2)
				
	# --------------------------------------------------------------|
	# AGENTS NORMAL MONTH FINANCIAL ENERGETIC ACTIVITY
	# --------------------------------------------------------------|
	
	def agentMonthEnergyActivity(self, tmpGen):
		'''Bridge function from the main the agent class'''
		for sngAgent in self.allAgents: 
			sngAgent.computeMonthNrgCostsAndPoll(self.allTechs, tmpGen)
			sngAgent.performFinancialActivities()
		# Stat functions
		self.statFunctions()

	# --------------------------------------------------------------|
	# NEW TECHNOLOGY EVALUATION
	# --------------------------------------------------------------|
			
	def newTechAssessment(self,tmpTime):
		# According to the average investment evaluation time (once per year) and the agent wealth 
		for sngAgent in self.allAgents:
			sngAgent.invAssessment(self.allTechs, self.allTechsID,tmpTime,self.allAgents)
	
	# --------------------------------------------------------------|
	# STATISTIC FUNCTIONS
	# --------------------------------------------------------------|
				
	def statFunctions(self):
	 	
	 	tmp_tCO2 = 0
	 	tmp_totalDebt = 0
	 	tmp_totalCosts = 0
	 	tmp_totalRepayments = 0
	 	for sngAgent in self.allAgents:
	 		tmp_tCO2 += sngAgent.co2
	 		tmp_totalDebt += sum(sngAgent.RemainingDebts)
	 		tmp_totalRepayments += sum(sngAgent.debtMonthRepayment)
	 		tmp_totalCosts += sngAgent.month_balance
	 	tmp_totalCosts -= tmp_totalRepayments
	 	
	 	# STAT VARIABLES
		self.totCO2.append(tmp_tCO2)
		self.totDebt.append(tmp_totalDebt)
		self.totCosts.append(tmp_totalCosts)
	 		
	
	# --------------------------------------------------------------|
	# Save results on file
	# --------------------------------------------------------------|		
	def saveOnFile(self, tmpSeed): 
		# Store simulation data on file
		tmpStat = [self.totCO2, self.totDebt, self.totCosts]
		filename = 'stat_co2DebtCosts' + str(tmpSeed)
		self.writeSngStatOnFileWhereISay(filename,tmpStat,'%i')
		
		# Create list with all the technologies stats
		for t in self.allTechs:
			self.totTechNRGdist.append(t.techNRGdist)
			self.totTechKWHdist.append(t.techKWHdist)
			self.totTechKWdist.append(t.techKWdist) 
			
		# Save overall stat on file 
		filename = 'stat_nrgDist' + str(tmpSeed)
		self.writeSngStatOnFileWhereISay(filename,self.totTechNRGdist,'%d')
		filename = 'stat_kwhDist' + str(tmpSeed)
		self.writeSngStatOnFileWhereISay(filename,self.totTechKWHdist,'%f.2')
		filename = 'stat_kwDist' + str(tmpSeed)
		self.writeSngStatOnFileWhereISay(filename,self.totTechKWdist,'%f.2')
		
	# --------------------------------------------------------------|
	# Function to save outcomes after different seeds runs
	# --------------------------------------------------------------|
	def saveTotalOnFile(self, nTech):
		filename = '_overall_CO2'
		self.writeSngStatOnFileWhereISay(filename,self.tottotCO2,'%i')
		filename = '_overall_debt'
		self.writeSngStatOnFileWhereISay(filename,self.tottotDebt,'%i')
		filename = '_overall_costs'
		self.writeSngStatOnFileWhereISay(filename,self.tottotCosts,'%i')
		
		#print self.tottotTechNRGdist
		#print self.tottotTechKWHdist
		#print self.tottotTechKWdist
		
		
		for tID in range(nTech):
			tempTechList = []
			for s in self.tottotTechNRGdist:
				tempTechList.append(s[tID])
			#save technology
			filename = '_overall_tech_' + str(tID)
			self.writeSngStatOnFileWhereISay(filename,tempTechList,'%i')

	# --------------------------------------------------------------|
	# Function to save files
	# --------------------------------------------------------------|
	def writeSngStatOnFileWhereISay(self, tmpName, tmpStats, tmpFormat):
		'''Function to save statistic on file'''
		outFnameStat = tmpName + '.csv'
		saveFileStat = open(outFnameStat, 'w')
		cnt = 0
		for i in range(len(tmpStats[0])):
			strTypes = ''
			for j in range(len(tmpStats)):
				strTypes += str(tmpStats[j][i]) + '\t'	
			strTypes += '\n'
			saveFileStat.write(strTypes)
			cnt += 1
		saveFileStat.close()	
		os.rename(outFnameStat, os.path.join(self.simPath,self.simFolder,outFnameStat))

	# --------------------------------------------------------------|
	# Function to save agents on file
	# --------------------------------------------------------------|
	def saveAgentsOnFile(self, tmpSeed):
		'''Function to save agents on file'''
		# Filenames
		agentsFileName = 'agents_' + str(tmpSeed) + '.csv'
		listsFileName = 'agentLists_' + str(tmpSeed) + '.csv'
		# File handle
		saveFileStatFid = open(agentsFileName, 'w')
		listsFileFid = open(listsFileName, 'w')
		# File init
		strAgentInit = 'ID\tX\tY\tEnergyNeed\tsolPot\tco2\tsocialLobby\tintCap\tequity\tbalance\tmBalance\tinvL\thealth\n'
		strListInit = 'Agent\tTech\tProp\tage\n'
		# Save first row
		saveFileStatFid.write(strAgentInit)
		listsFileFid.write(strListInit)
		# For each agent
		for a in self.allAgents:
			strAgent = str(a.ID) + '\t' + str(a.x) + '\t' + str(a.y) + '\t' + str(a.totEnergyNeed) + '\t' + \
			str(a.solar_potential) + '\t' + str(a.co2) + '\t' + str(a.social_lobby) + '\t' + str(a.int_capital) + '\t' + \
			str(a.equityCost) + '\t' + str(a.balance) + '\t' + str(a.month_balance) + '\t' + str(a.invLenght) + '\t' + \
			str(a.health) + '\n'
			
			saveFileStatFid.write(strAgent)
			# For each Technology
			for i, t in enumerate(a.nrgTechsReceipt):
				tmpAge = self.months - a.debtTime[i]
				strList = str(a.ID) + '\t' + str(t) + '\t' + str(a.nrgPropReceipt[i]) + '\t' + str(tmpAge) + '\n'
				listsFileFid.write(strList)
			
		saveFileStatFid.close()
		listsFileFid.close()
		
		self.fromCVStoXML([agentsFileName,'agentsFileNameXML'])
		os.rename(agentsFileName, os.path.join(self.simPath,self.simFolder,agentsFileName))
		os.rename(listsFileName, os.path.join(self.simPath,self.simFolder,listsFileName))

	# --------------------------------------------------------------|
	# Function to save technologies on file
	# --------------------------------------------------------------|
	def saveTechsOnFile(self, tmpSeed):
		'''Function to save tech on file'''
		# Filenames
		techFileName = 'techs_' + str(tmpSeed) + '.csv'
		# File handle
		saveFileStatFid = open(techFileName, 'w')
		# File init
		strTechInit = 'ID\tEff\tStarttime\tdecay\tcost\ttCost\tpCost\trate\tloanLength\tduration\tco2\tsolarBased\tfeed-in-tarif\ttax-credit-inv\ttax-credit-debt\tcarbon-tax\tyears\tX\tY\tconversion\n'
		saveFileStatFid.write(strTechInit)
		for t in self.allTechs:
			strTech = str(t.ID) + '\t' + str(t.efficiency) + '\t' + str(t.startTime) + '\t' + str(t.decay) + '\t' + \
			str(t.cost) + '\t' + str(t.transportCosts) + '\t' + str(t.plantCost) + '\t' + str(t.interestRate) + '\t' + \
			str(t.loanLength) + '\t' + str(t.duration) + '\t' + str(t.co2) + '\t' + str(t.solarBased) + '\t' + \
			str(t.incPach[0]) + '\t' + str(t.incPach[1]) + '\t' + str(t.incPach[2]) + '\t' + str(t.incPach[3]) + '\t' + \
			str(t.incPach[4]) + '\t' + str(t.X) + '\t' + str(t.Y) + '\t' + str(t.fromKWH2KW) + '\n'
			
			saveFileStatFid.write(strTech)
			
		saveFileStatFid.close()
		os.rename(techFileName, os.path.join(self.simPath,self.simFolder,techFileName))
			

	def fromCVStoXML(self,args):
	  
	  try:
		filename = args[0]
		safe_filename = str.replace(filename[:-4], " ", "_").lower()
	  except IndexError:
		print "ERROR: Please provide a filename.csv as the first argument"
		sys.exit()	
	  try:
		single_item = args[1]
	  except IndexError:
		print "ERROR: Please provide a name to be used for each row node"
		sys.exit()
	  
	  f = csv.reader(open(filename, 'rb'))
	  
	  doc = Document()
	  root_element = doc.createElement(safe_filename)
	  doc.appendChild(root_element)
	  
	  columns = f.next()
	  
	  for row in f:
		item = doc.createElement(single_item)
		root_element.appendChild(item)
		for c in enumerate(create_col_nodes(columns, item, doc)):
		  c[1].appendChild(doc.createTextNode(row.pop(0)))
	  
	  output_file = safe_filename + ".xml"
	  doc.writexml(open(output_file, 'w')) # Write file
	  
	  print "Done: Created %s" % output_file
	  
	def create_col_nodes(cols, item, doc):
	  nodes = []
	  for col in cols:
		node = doc.createElement(str.replace(col, " ", "_").lower())
		item.appendChild(node)
		nodes.append(node)
	  
	  return nodes
	
	if __name__ == "__main__":
	  sys.exit(main(sys.argv))
			
			
