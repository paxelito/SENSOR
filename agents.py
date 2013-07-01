#!/usr/bin/env python
# -*- coding: latin-1 -*-

import sys, os
import random as ran
import copy

class agents:
	def __init__(self, tmpDL = 0, tmpID = 0, tmpX = 0, tmpY = 0, tmpNrgDim = 100, tmpSocialLobby = 0, tmpSolPot = ran.uniform(0.5,1), tmpEquityCost = 0.05, \
	             tmpIntCap = 0.5, tmpInvLength = 50, tmpHealth = 1, tmpAge = 0, tmpNrgTech = None, tmpNrgTechProp = None, tmpTechPolicy = None, tmpTechAges = None, \
	             tmpBalance = 0, tmpMBalance = 0, tmpDebts = None, tmpRemDebt = None, tmpDebtTime = None, tmpDebtLen = None, tmpMrep = None):
		'''Constructor of the agent class'''
		# General Agent Attributes
		self.ID = tmpID
		self.x = tmpX
		self.y = tmpY
		self.totEnergyNeed = tmpNrgDim # Energetic dimension of the agent
		self.debugLevel = tmpDL
		self.age = tmpAge
		
		# Technology Parameters
		if tmpNrgTech == None:
			self.nrgTechsReceipt = [0] # technologies vectors
		if tmpNrgTechProp == None:
			self.nrgPropReceipt = [self.totEnergyNeed] # KW provided by the different technologies. 
		if tmpTechPolicy == None:
			self.techPolicy = [[0,0]] # tmpPolicy tmpPolicyLength. 
		if tmpTechAges == None:
			self.nrgTechAges = [0] # technology ages. Time elapsed from the installation 
		self.flagFree = True
		
		# Physical Parameters of the agent
		self.solar_potential  = tmpSolPot # Proportion of solar irradiation according to the place where agent is (from 0 to 1) 
		self.co2 = 0
		self.social_lobby  = tmpSocialLobby # How much the agent can be influenced by the neighborhoods
		
		# FINANCIAL PARAMETERS
		self.int_capital = tmpIntCap
		self.equityCost = tmpEquityCost
		self.balance = tmpBalance
		self.month_balance = tmpMBalance
		self.invLength = tmpInvLength
		self.health = tmpHealth # This parameter represents the health of the agent. Once that the agent has assessed the possible investment, this is the probability to actually invest
		if tmpDebts == None:
			self.debts = [0] # initial debts list of the agent
		if tmpRemDebt == None:
			self.RemainingDebts = [0] # List of the remaining part of the debt for each technology
		if tmpDebtTime == None:
			self.debtTime = [0] # Time elapsed from the beginning of the investment for each technology
		if tmpDebtLen == None:
			self.debtLength = [0] # length of the different investments
		if tmpMrep == None:
			self.debtMonthRepayment = [0] # month payment for each investment
		
		self.distanceList = [] # initialize distance list 
		self.attraction = [] # define social attraction of the other technologies. 
		
	# --------------------------------------------------------------|
	# NEW TECHNOLOGY INTRODUCTION
	# --------------------------------------------------------------|	
	def newTech(self, tmpTechID, tmpProp, tmpDistance, tmpPolicy, tmpPolicyLength):
		'''Function to inser a new technology in the agent receipt'''
		self.nrgTechsReceipt.append(tmpTechID)
		self.nrgPropReceipt.append(self.totEnergyNeed * tmpProp)
		self.techPolicy.append([tmpPolicy,tmpPolicyLength])
		
	# --------------------------------------------------------------| 
	# NEW INVESTMENT ASSESSMENT
	# --------------------------------------------------------------|		
	def invAssessment(self,tmpTechs,tmpTechsID,tmpTime,tmpAgents,tmpPolicies):
		'''Function to assess the possible investment'''
		# first position the policy, second position the total amount of incentive used. To update only if a new technology is used. 
		tmpPolicyAmountToRemove = [0,0]
		if 12 - ran.randint(1,12) == 0: 
			if self.debugLevel < 0:
				print "\t	\_ AGENT ", self.ID, " is assessing its strategy"
			if self.debugLevel < -1:
				print "\t  	 \_ Total balance: ", u"\u20AC", "%.2f" % self.balance, " M: ", u"\u20AC", "%.2f" % self.month_balance, " CO2: ", "%.4f" %self.co2
			# If the agent is in health
			if self.flagFree == True:
				# Define technology attraction list
				relativeAttractions = self.defineTechAttraction(tmpTechs, tmpAgents)
				# Create a list with all the available technologies (not already used by the agent)
				tmpAvaiableTechs = list(set(tmpTechsID).difference(set(self.nrgTechsReceipt)))
				cnt = 0 # counter	
				tmpCurrentAnnualCosts = self.month_balance * 12 # Compute current annual costs
				# .. If there are available technologies 
				if len(tmpAvaiableTechs) > 0:
					npvList = [] # List of all net present values
					pbpList = [] # List of all payback periods
					recList = [] # List of all the possible technology recepits
					polList = [] # List of all the total amount of policy used. 
					
					# FOR EACH NEW TECHNOLOGY....
					for sngTechID in tmpAvaiableTechs:	
						tmpHypCosts = 0	# hypothetical costs according to this new technology
						tmpPolAmount = 0 # temporary variable containing the total amount of policy theoretically used with this tech	
						# Compute the hypothetic annual costs due to the new technology implementation
						# .. New tech max energy production, the size of the energy partition changes according to the solar orientation of the agent
						tmpNewNrgProp = int(round(ran.randint(1,self.totEnergyNeed) * (pow(self.solar_potential,tmpTechs[sngTechID].solarBased))))
						if tmpNewNrgProp > 0:
							tmpNrgPropReceipt = self.rearrangeTechPropList(tmpNewNrgProp) # Create a temporary new energy proportion list 
							# Compute the overall cost of the plan according to the relation between kWh and kW. 
							tmpOverallPlantCost = float(tmpNewNrgProp) / tmpTechs[sngTechID].fromKWH2KW * tmpTechs[sngTechID].plantCost
							
							# For the years of the investment 
							netPresentValue = 0
							payBackPeriod = 0
							cashFlow = 0
							for y in range(1,self.invLength + 1):
								# Compute costs and intentives of the year
								tmpCostsAndIncs = self.computeAnnualCostandIncs(sngTechID, tmpNewNrgProp, tmpNrgPropReceipt, tmpTechs, tmpPolicies, relativeAttractions, tmpOverallPlantCost, y)
								
								tmpHypCosts = tmpCostsAndIncs[0]
								tmpPolAmount += tmpCostsAndIncs[1]
								tmpEXTplantCost = tmpCostsAndIncs[2]
								tmpINTplantCost = tmpCostsAndIncs[3]
								wacc = tmpCostsAndIncs[4]
								# Reset cash flow for this year
								cashFlow = 0
								# Compute the tax-credit-investment for the years of the incentive
								tmpCredInv = 0
								if (y <= (tmpPolicies[tmpTechs[sngTechID].policy].length / 12)) & (tmpPolicies[tmpTechs[sngTechID].policy].taxCreditInv > 0):
									tmpCredInv += tmpOverallPlantCost * tmpPolicies[tmpTechs[sngTechID].policy].taxCreditInv / (tmpPolicies[tmpTechs[sngTechID].policy].length / 12)
									# (3) Since tax credit investment has been theoretically used, it is updated
									tmpPolAmount += tmpCredInv
									
								# Compute annual interest to pay for the YEARS of the loan
								if y <= (tmpTechs[sngTechID].loanLength / 12):
									# Compute clean annual interest
									tmpAnnualInterest = self.computeLoanAnnualInterest(tmpEXTplantCost, (tmpTechs[sngTechID].loanLength / 12), tmpTechs[sngTechID].interestRate)
									# If there is an incentive on the interest
									if (y <= (tmpPolicies[tmpTechs[sngTechID].policy].length / 12)) & (tmpPolicies[tmpTechs[sngTechID].policy].taxCredit > 0):
										tmpIntRate = tmpTechs[sngTechID].interestRate * (1 - tmpPolicies[tmpTechs[sngTechID].policy].taxCredit)
										tmpAnnualInterestWithInc = self.computeLoanAnnualInterest(tmpEXTplantCost, (tmpTechs[sngTechID].loanLength / 12), tmpIntRate) 
										# (4) Since tax credit interest has been theoretically used, it is updated
										tmpPolAmount += tmpAnnualInterest - tmpAnnualInterestWithInc
										tmpAnnualInterest = tmpAnnualInterestWithInc
									
									# Investment credit + annual savings - interests - credit capital 
									cashFlow = tmpCredInv + (tmpCurrentAnnualCosts - tmpHypCosts) - tmpAnnualInterest - (tmpEXTplantCost / (tmpTechs[sngTechID].loanLength / 12))
								else:
									# Investment credit + annual savings
									cashFlow = tmpCredInv + (tmpCurrentAnnualCosts - tmpHypCosts)
									
								# if there is equity capital it is spent in the first year
								if ((y == 1) & (tmpINTplantCost > 0)): cashFlow -= tmpINTplantCost
								# Compute in progress NPV
								netPresentValue += cashFlow / (pow(1+wacc,y))
								#print "CF: ", cashFlow, " cred: ", tmpCredInv, " + (HC: ",tmpCurrentAnnualCosts, " - h: ", tmpHypCosts, ") - INT ", tmpAnnualInterest,\
								#      " = NPV: ", netPresentValue, " - PLANT: ", tmpOverallPlantCost, " delta: %.2f" % (netPresentValue - tmpOverallPlantCost), " dim: ", tmpNewNrgProp
								# Compute paybackPeriod
								if (netPresentValue >= tmpOverallPlantCost) & (payBackPeriod == 0):
									payBackPeriod = y
									
							# .. Compute final net present value
							netPresentValue -= tmpOverallPlantCost
							
							# Append analysis value in lists 
							npvList.append(netPresentValue)
							pbpList.append(payBackPeriod)
							recList.append(tmpNrgPropReceipt)
							polList.append(tmpPolAmount)
							
							if self.debugLevel < -1:
								print "\t  	  |- Tech: ", cnt, " NPV: %10.2f" % netPresentValue, " PBP: ", payBackPeriod
						
						cnt = cnt + 1 # Available technology Counter update
					
					# .. Compute the better technology
					betterTechPos = 0
					betterNPV = 0
					betterPayBack = 0
					if len(npvList) > 1:
						tmpFinID = 0
						for sngPbpList in pbpList:
							if (sngPbpList > 0) & (sngPbpList < self.invLength):
								if npvList[tmpFinID] > betterNPV: 
									betterNPV = npvList[tmpFinID]
									betterTechPos = tmpFinID
									betterPayBack = sngPbpList
							tmpFinID += 1
					
					if betterNPV > 0:
						tmpRnd = ran.random()
						#print self.invLength, " ", betterPayBack, " ", self.health
						#print tmpRnd
						if tmpRnd < self.genLogFun((self.invLength - betterPayBack), self.health):
							
							# .. If a BETTER new technology exist, it is added to the agent
							
							self.flagFree = False # Technology search is blocked
							self.nrgTechsReceipt.append(tmpTechsID[tmpAvaiableTechs[betterTechPos]])
							self.nrgPropReceipt = recList[betterTechPos]
							self.nrgTechAges.append(0)
							self.techPolicy.append([tmpTechs[tmpTechsID[tmpAvaiableTechs[betterTechPos]]].policy,\
												tmpPolicies[tmpTechs[tmpTechsID[tmpAvaiableTechs[betterTechPos]]].policy].length])
							# ... Compute total interest
							totInterestsToPay = 0
							for iyears in range(0,(tmpTechs[tmpAvaiableTechs[betterTechPos]].loanLength / 12)):
								if iyears < (tmpPolicies[tmpTechs[tmpTechsID[tmpAvaiableTechs[betterTechPos]]].policy].length / 12):
									tmpIntRate = tmpTechs[self.nrgTechsReceipt[-1]].interestRate * (1 - tmpPolicies[tmpTechs[tmpTechsID[tmpAvaiableTechs[betterTechPos]]].policy].taxCredit)
									tmpAnnualInterest = self.computeLoanAnnualInterest(tmpEXTplantCost, (tmpTechs[self.nrgTechsReceipt[-1]].loanLength / 12), tmpIntRate) 
								else:
									tmpAnnualInterest = self.computeLoanAnnualInterest(tmpEXTplantCost, (tmpTechs[self.nrgTechsReceipt[-1]].loanLength / 12), tmpTechs[sngTechID].interestRate)	
								totInterestsToPay += tmpAnnualInterest
																				
							tmpTotalDept = tmpEXTplantCost + totInterestsToPay
							self.debts.append(tmpTotalDept)
							self.RemainingDebts.append(tmpTotalDept)
							self.debtTime.append(tmpTime) 
							self.debtLength.append((tmpTechs[tmpAvaiableTechs[betterTechPos]].loanLength / 12))
							self.debtMonthRepayment.append(tmpTotalDept / tmpTechs[tmpAvaiableTechs[betterTechPos]].loanLength)
							# Init Inv Payment
							self.month_balance = tmpINTplantCost
							self.balance += self.month_balance
							
							tmpPolicyAmountToRemove = [tmpTechs[tmpTechsID[tmpAvaiableTechs[betterTechPos]]].policy, polList[betterTechPos]]
							
							if self.debugLevel < -1:
								print "\t 	    |- Agent ", self.ID, " has invested in a new technology:"
								print "\t 	     \_ New Technology List: ", self.nrgTechsReceipt
								print "\t 	     \_ New Technology Receipt List: ", self.nrgPropReceipt
								print "\t 	     \_ New Debts List: ", self.debts
								print "\t 	     \_ New Residual Debts List: ", self.RemainingDebts
								print "\t 	     \_ New Initial Debts Time List: ", self.debtTime
								print "\t 	     \_ New Debts Lengths List: ", self.debtLength
								print "\t 	     \_ New Debts Month Repayment List: ", self.debtMonthRepaymen
								
		return tmpPolicyAmountToRemove
								
	# --------------------------------------------------------------|
	# Compute annual costs and policy amount
	# --------------------------------------------------------------|
	def computeAnnualCostandIncs(self, tmpSngTechID, tmp_newNrgProp, tmp_NrgPropReceipt, tmp_techs, tmp_policies, tmpRelativeAttractions, tmp_overallPlantCost, tmpTime):
		'''This function computes annual costs and annual feed-in incentives according to the technology energy drops'''
		# .. According to the temporary new tech energy proportion the annual cost is computed
		tmpCnt = 0
		tmpCosts = 0
		tmpIncsAmount = 0
		# Update values within tmp_NrgPropReceipt according to the year of the theoretical investment
		tmpNewPropWithDrop = tmp_newNrgProp * (tmp_techs[tmpSngTechID].efficiency**tmpTime)
		# Update the proportion technology list according to the efficiency drop and the year computed
		dynNrgPropReceipt = copy.deepcopy(tmp_NrgPropReceipt)
		for tmpID, tmpUpdateProp in enumerate(dynNrgPropReceipt):
			tmpValue = dynNrgPropReceipt[tmpID] * (tmp_techs[tmpID].efficiency**tmpTime)
			dynNrgPropReceipt[tmpID] = tmpValue
			if tmpID > 0:
				dynNrgPropReceipt[0] += tmpValue
						
		# For each already present technology according to the new temporary distribution
		for tmpNewSngProp in tmp_NrgPropReceipt[:-1]:
			# Compute distance from source, if distance is 0 this term is 0 and the multiplier does not affect the computation
			tmpDistanceFromSourceMultiplier = pow(pow(abs(self.x - tmp_techs[self.nrgTechsReceipt[tmpCnt]].X),2) + pow(abs(self.y - tmp_techs[self.nrgTechsReceipt[tmpCnt]].Y),2),0.5)
			tmpDistanceFromSourceMultiplier *= tmp_techs[self.nrgTechsReceipt[tmpCnt]].transportCosts
			
			tmpCosts += tmpNewSngProp * (tmp_techs[self.nrgTechsReceipt[tmpCnt]].cost +\
										 tmp_policies[self.techPolicy[tmpCnt][0]].carbonTax +\
										 tmpDistanceFromSourceMultiplier - tmp_policies[self.techPolicy[tmpCnt][0]].feedIN)
			# (1) Since feedIn has been theoretically used, it is updated
			tmpIncsAmount += tmpNewSngProp * tmp_policies[self.techPolicy[tmpCnt][0]].feedIN
			
			if tmp_techs[self.nrgTechsReceipt[tmpCnt]].cost <= 0:
				# If the cost is negative the energy is sold, so the cost of the traditional energy has to be added 
				tmpCosts += tmpNewSngProp * tmp_techs[0].cost
			tmpCnt += 1
			
		# .. The cost associated to the new technologies are added
		tmpCosts += tmpNewPropWithDrop * (tmp_techs[tmpSngTechID].cost + tmp_policies[tmp_techs[tmpSngTechID].policy].carbonTax - tmp_policies[tmp_techs[tmpSngTechID].policy].feedIN)
		
		# (2) Since feedIn has been theoretically used, it is updated
		tmpIncsAmount += tmpNewPropWithDrop * tmp_policies[tmp_techs[tmpSngTechID].policy].feedIN
		
		if tmp_techs[tmpSngTechID].cost <= 0:
			# If the cost is negative the energy is sold, so the cost of the traditional energy has to be added
			tmpCosts += tmpNewPropWithDrop * tmp_techs[0].cost
		# .. from month to year
		tmpCosts *= 12
		
		# .. SOCIAL ATTRACTIVENESS
		# .. Cost are rescaled according to the imitation list (note that if the socialLobby parameter is 0 the list remains the same)
	
		for RAcnt, sngLobby in enumerate(tmpRelativeAttractions):
			if tmpSngTechID == RAcnt:
				tmpCosts -= tmpCosts * sngLobby * self.social_lobby
			else:
				tmpCosts += tmpCosts * sngLobby * self.social_lobby
			
		# WACC (Weighted Average Cost of Capital) Computation (incentive amount on interests is computed later)
		# the equity capital is randomly modified to create variability 
		self.int_capital = ran.uniform(self.int_capital * 0.9, self.int_capital * 1.1)
		if self.int_capital < 0: self.int_capital = 0
		if self.int_capital > 1: self.int_capital = 1
		tmp_INTplantCost = tmp_overallPlantCost * self.int_capital
		tmp_EXTplantCost = tmp_overallPlantCost - tmp_INTplantCost
		tmp_wacc = (tmp_INTplantCost / tmp_overallPlantCost * self.equityCost) + \
			   ((tmp_EXTplantCost / tmp_overallPlantCost * tmp_techs[tmpSngTechID].interestRate) * (1-tmp_policies[tmp_techs[tmpSngTechID].policy].taxCredit))
		
		# define and initialize the list containing the output variables
		outList = [tmpCosts,tmpIncsAmount,tmp_EXTplantCost,tmp_INTplantCost,tmp_wacc]
		return outList
	
	# --------------------------------------------------------------|
	# Re-arrange technologies proportion list. 
	# --------------------------------------------------------------|							
	def rearrangeTechPropList(self,tmpNewProp):
		'''Function to rearrange the proportion of the different technology according to a possibile new one'''
		cnt = 0
		newList = []
		goon = 1	
		tmpNewPropResidue = copy.deepcopy(tmpNewProp)
		for sngTech in self.nrgPropReceipt:
			tmpValue = sngTech - tmpNewPropResidue # Compute the different between the extant proportion and the new one
			if goon == 1: 
				if tmpValue >= 0:
					newList.append(tmpValue)
					goon = 0
				else:
					newList.append(0)
					tmpNewPropResidue -= sngTech
			else:
				newList.append(sngTech)
		
		newList.append(tmpNewProp)
		
		return newList

	# --------------------------------------------------------------|
	# Update technologies energy proportion list.
	# --------------------------------------------------------------|
	def updateEnergyPropAccordingToEfficiencyDrop(self, tmpAllTechs):
		'''Update energy tech proportions list according to the efficiency prop parameter of the technologies'''
		for IDtech, tech in enumerate(self.nrgPropReceipt):
			if (self.nrgTechAges[IDtech] % 12 == 0) & (self.nrgPropReceipt[IDtech] > 0):
				# Compute new technology energy contribute
				tmpNewTechProp = round(self.nrgPropReceipt[IDtech] * tmpAllTechs[self.nrgTechsReceipt[IDtech]].efficiency)
				# Compute the difference with the old contribute
				tmpDelta = self.nrgPropReceipt[IDtech] - tmpNewTechProp
				# Update energy prop list removing inefficiency and adding the energy drop to the traditional energy
				self.nrgPropReceipt[0] += tmpDelta
				if IDtech != 0:
					self.nrgPropReceipt[IDtech] -= tmpDelta
				
		
	# --------------------------------------------------------------|
	# Compute Investment interest
	# --------------------------------------------------------------|
	def computeLoanAnnualInterest(self, tmpCapital, tmpYears, tmpRate):

		'''Compute investment annual interests'''
		annualInt = (tmpCapital * tmpYears * tmpRate) / tmpYears
		return annualInt
		
	# --------------------------------------------------------------|
	# Pay month debits 
	# --------------------------------------------------------------|
	def performFinancialActivities(self):
		'''This procedure performs all the month financial activities, monthly debts payments'''
		cnt = 0
		for sngDept in self.RemainingDebts:
			if sngDept > 0:
				self.RemainingDebts[cnt] -= self.debtMonthRepayment[cnt]
				if self.RemainingDebts[cnt] < 0:
					self.RemainingDebts[cnt] = 0
			else:
				self.RemainingDebts[cnt] = 0
				self.debtMonthRepayment[cnt] = 0
			cnt += 1
		if sum(self.RemainingDebts) == 0:
			self.flagFree = True
				
	# --------------------------------------------------------------|
	# Month energy costs  
	# --------------------------------------------------------------|
	def computeMonthNrgCostsAndPoll(self, tmpTechs, tmpTime, tmpPolicies):
		'''Function to assess the monthly energy costs according to the monthly energy needs'''
		tempMonthCosts = 0
		tempPoll = 0
		counter = 0
		for tech in self.nrgTechsReceipt:
		
			# .. compute costs and revenues
			tmpDistanceFromSourceMultiplier = pow(pow(abs(self.x - tmpTechs[tech].X),2) + pow(abs(self.y - tmpTechs[tech].Y),2),0.5)
			tmpDistanceFromSourceMultiplier *= tmpTechs[tech].transportCosts
									
			tempMonthCosts += self.nrgPropReceipt[counter]\
						   * (tmpTechs[tech].cost\
							  + tmpDistanceFromSourceMultiplier\
							  + tmpPolicies[self.techPolicy[counter][0]].carbonTax\
							  - tmpPolicies[self.techPolicy[counter][0]].feedIN)\
						   + self.debtMonthRepayment[counter]
			
			# If the incentive is still valid the tax credit on the investment is computed	
			if (tmpPolicies[self.techPolicy[counter][0]].taxCreditInv > 0) & (self.techPolicy[counter][1] > 0):
					tempMonthCosts -= (self.nrgPropReceipt[counter] / tmpTechs[tech].fromKWH2KW * tmpTechs[tech].plantCost) \
									  * tmpPolicies[self.techPolicy[counter][0]].taxCreditInv /  tmpPolicies[self.techPolicy[counter][0]].length
			
			# If the technology has a negative price (e.g. solar), then it means that the agent sells energy and it has to buy normal energy
			if tmpTechs[tech].cost <= 0:
				tempMonthCosts += tmpTechs[0].cost * self.nrgPropReceipt[counter]
							
			# Check policy validity 
			if self.techPolicy[counter][1] > 0:
				self.techPolicy[counter][1] -= 1
			if self.techPolicy[counter][1] == 0:
				self.techPolicy[counter] = [0,0]
				
			# Update technology age
			self.nrgTechAges[counter] += 1
				
			#raw_input("...")
				
			# .. update statistic variables
			if self.nrgPropReceipt[counter] > 0:
				tmpTechs[tech].incrementNRGdist((tmpTime - 1))
				tmpTechs[tech].incrementKWHdist((tmpTime - 1), self.nrgPropReceipt[counter])
			
			# .. compute pollution
			tempPoll = tempPoll + (tmpTechs[tech].co2 * self.nrgPropReceipt[counter])
			counter = counter + 1
			
			
		# ... Update agent variables. 
		self.month_balance = tempMonthCosts
		self.balance = self.balance + self.month_balance
		self.co2 = tempPoll
		self.age += 1
		
		

	# --------------------------------------------------------------|
	# DEFINE TECHNOLOGIES ATTRACTION
	# --------------------------------------------------------------|		
	def defineTechAttraction(self, tmpTechs, tmpAgents):
		'''Define technology attraction according to the neighborhood characteristics'''
		
		tmpTotTech = [0]*len(tmpTechs)
		tmpRelTech = [0]*len(tmpTechs)
		
		for sngT in tmpTechs: # For each tech
			for sngA in tmpAgents: # For each agent
				if self.ID != sngA.ID: # if the agent is not me
					if sngT.ID in sngA.nrgTechsReceipt: # For each technology used by the agent
						if sngA.nrgPropReceipt[sngA.nrgTechsReceipt.index(sngT.ID)] > 0:
							tmpTotTech[sngT.ID] += (float(sngA.totEnergyNeed) / pow(self.distanceList[sngA.ID],2))
		cnt = 0
		for relT in tmpRelTech:
			tmpRelTech[cnt] = tmpTotTech[cnt] / float(sum(tmpTotTech))
			cnt += 1	
			
		return tmpRelTech
	
	# --------------------------------------------------------------|
	# DEFINE TECHNOLOGIES ATTRACTION
	# --------------------------------------------------------------|
	def genLogFun(self, tmpX, tmpExp=1, tmpM=4, tmpUpper=1, tmpLower=0, tmpGrowth=1, tmpQ=1):
		'''Function to return the general logistic value according to the different paramerts
		   Default values are those of the logistic function'''
		e = 2.71828182845904523536
		tmpY = 0
		valToAdd = tmpM
		M = ((1-tmpExp) * 10) + valToAdd
		tmpQ = tmpExp
		try:
			tmpY = tmpLower + ( (tmpUpper - tmpLower) / \
						( pow(1 + (tmpQ * pow(e,(-tmpGrowth*(tmpX-M)))),(1/tmpExp)) ) )
		except:
			tmpY = 0
		return tmpY
	
	