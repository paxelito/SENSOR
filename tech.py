'''Class tech definition.

.. module:: tech
   :platform: Unix, Windows
   :synopsis: The module containing the tech class, the class describing the different technologies
   
.. moduleauthor:: Alessandro Filisetti <alessandro.filisetti@unibo.it>

'''
import os
import shutil as sh

class tech:
	'''Class tech definition.	
	'''
	def __init__(self, tmpID = 0, tmpEff = 0, tmpST = 0, tmpTotTime = 0, tmpDecay = 0, tmpCost = 0, tmpPcost = 0, tmpRate = 0,\
	             tmpCo2 = 0, tmpTransportCosts = 0, tmpLoanLength = 10, tmpLifeDuration = 50, tmpIncList = None, tmpFromKWH2KW = 100, \
	             tmpSolarBased = 0, tmpX = 0, tmpY = 0):
		''' Constructor '''
		
		self.ID = tmpID
		self.efficiency = tmpEff
		self.startTime = tmpST
		self.decay = tmpDecay
		self.cost = tmpCost # Cost euro/KwH
		self.transportCosts = tmpTransportCosts # Cost for Kwh like with biomass energy
		self.plantCost = tmpPcost # cost of the investment for each KWh
		self.interestRate = tmpRate # Cost of the debit capital
		self.loanLength = tmpLoanLength # Loan length (years)
		self.duration = tmpLifeDuration # Total life time of the technology
		self.co2 = tmpCo2 # total amount of CO2 produced per Kw/h	
		if tmpIncList == None:
			self.incPach = [0,0,0,0,0] # Possible policies to be applied, [feed-in-tarif, tax-credit-inv, tax-credit-debt, carbon-tax, years]
		else:
			self.incPach = tmpIncList
		self.solarBased = tmpSolarBased
			
		self.X = tmpX
		self.Y = tmpY
				
		self.fromKWH2KW = tmpFromKWH2KW
			
		self.techNRGdist = [0] * tmpTotTime
		self.techKWHdist = [0] * tmpTotTime
		self.techKWdist = [0] * tmpTotTime
	
	def getFeedInTariff(self):
		return self.incPach[0]
		
	def getTaxCreditInv(self):
		return self.incPach[1]
		
	def getTaxCreditDebt(self):
		return self.incPach[2]
		
	def getCarbonTax(self):
		return self.incPach[3]

	def getIncYears(self):
		return self.incPach[4]
		
	def incrementNRGdist(self, tmpPos):
		self.techNRGdist[tmpPos] += 1
    
        	
	def incrementKWHdist(self, tmpPos, tmpInc):
		self.techKWHdist[tmpPos] += tmpInc
		self.techKWdist[tmpPos] += (tmpInc / self.fromKWH2KW)
		
