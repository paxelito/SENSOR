#!/usr/bin/env python
# -*- coding: latin-1 -*-

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
	             tmpCo2 = 0, tmpTransportCosts = 0, tmpLoanLength = 20, tmpLifeDuration = 50, tmpPolicy = 0, tmpFromKWH2KW = 100, \
	             tmpSolarBased = 0, tmpX = 0, tmpY = 0):
		''' Constructor '''
		
		self.ID = tmpID
		self.efficiency = tmpEff # Technology efficiency drop per year. 
		self.startTime = tmpST
		self.decay = tmpDecay
		self.cost = tmpCost # Cost euro/KwH
		self.transportCosts = tmpTransportCosts # Cost for Kwh like with biomass energy
		self.plantCost = tmpPcost # cost of the investment for each KWh
		self.interestRate = tmpRate # Cost of the debit capital
		self.loanLength = tmpLoanLength # Loan length (years)
		self.duration = tmpLifeDuration # Total life time of the technology
		self.co2 = tmpCo2 # total amount of CO2 produced per Kw/h
		self.policy = tmpPolicy
		self.solarBased = tmpSolarBased
			
		self.X = tmpX
		self.Y = tmpY
				
		self.fromKWH2KW = tmpFromKWH2KW
		
		# Technology distribution in time
		self.techNRGdist = [0] * tmpTotTime
		self.techKWHdist = [0] * tmpTotTime
		self.techKWdist = [0] * tmpTotTime
		
	def incrementNRGdist(self, tmpPos):
		self.techNRGdist[tmpPos] += 1
    
        	
	def incrementKWHdist(self, tmpPos, tmpInc):
		self.techKWHdist[tmpPos] += tmpInc
		self.techKWdist[tmpPos] += (tmpInc / self.fromKWH2KW)
		
