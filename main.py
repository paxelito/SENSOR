#!/usr/bin/env python

import sys, os
import env as en
import random as ran

# get path for placing simulation
try:
	StrPath = sys.argv[1] # Here the path of the simulation
except:
	print "Usage:",sys.argv[0], "Error in the parameter introduction"; sys.exit(1)
	
varParList1 = [0.1, 0.2, 0.3, 0.4, 0.5]
varParList2 = [0.25]
nSeed = 10
nTech = 3

for sngParam1 in varParList1:
	for sngParam2 in varParList2:
	
		# Initialize environment
		envi = en.environment(StrPath)
		# Create folder simulation and store initial conditions
		envi.createFolderAndSaveInitialConditions(sngParam1, sngParam2)
		envi.printParams()
	
		# For each seed
		for ns in range(nSeed):
		
			envi.createPopulation()
			envi.createTechnologies()
			envi.createPolicies(sngParam1, sngParam2)
			
			
			# DYNAMICS
			for gen in range(1, envi.months+1):
				if gen % 10 == 0:
					try:
						print " \- feedIN: ", sngParam1, " Prop: ", sngParam2 ,"NSEED: ", ns, "MONTH NUMBER ", gen, " TOT CO2: ", \
						envi.totCO2[-1], " TOT COSTS: ", envi.totCosts[-1], " TOT DEBTS: ", envi.totDebt[-1]
					except:
						print " \- feedIN: ", sngParam1, " Prop: ", sngParam2 , " NSEED: ", ns, "MONTH NUMBER ", gen, " TOT CO2: ", \
						envi.totCO2, " TOT COSTS: ", envi.totCosts, " TOT DEBTS: ", envi.totDebt
				# Standard month activities
				envi.agentMonthEnergyActivity(gen)	
				# New Technology evaluation
				envi.newTechAssessment(gen)
				#raw_input('click any buttom to continue... ')
			# Save results on file 
			envi.saveOnFile(ns)
			envi.saveAgentsOnFile(ns)
			envi.saveTechsOnFile(ns)
			envi.savePoliciesOnFile(ns)
			
			# reset simulation 
			envi.resetSimulation()
			
		# Del environment
		envi.saveTotalOnFile(nTech)
		del envi
