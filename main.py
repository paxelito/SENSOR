#!/usr/bin/env python
"""@package SENSOR
   \mainpage SENSOR
   \author Alessandro Filisetti
     
	More details.
"""

import sys, os
import env as en
import random as ran

# get path for placing simulation
try:
	StrPath = sys.argv[1] # Here the path of the simulation
except:
	print "Usage:",sys.argv[0], "Error in the parameter introduction"; sys.exit(1)
	
	
StrPath = os.path.abspath(StrPath)
	
varParList1 = [0.25, 0.5, 0.75, 1]
varParList2 = [0.25, 0.5, 0.75, 1]
varParList3 = [0.25, 0.5, 0.75, 1]

print "\n* * * * * * * * * * * * * * * * * * * * * * * * * *"
print "\tWELCOME, SIMULATION IS GOING TO START..."
print "* * * * * * * * * * * * * * * * * * * * * * * * * * * \n"

for sngParam1 in varParList1:
	for sngParam2 in varParList2:
		for sngParam3 in varParList3:
		
			# Initialize environment
			envi = en.environment(StrPath)
			# Create folder simulation and store initial conditions
			envi.createFolderAndSaveInitialConditions(sngParam1, sngParam2, sngParam3)
			envi.printParams()
		
			# For each seed
			for ns in range(envi.nSeed):
			
				envi.createPopulation()
				envi.createTechnologies()
				envi.createPolicies(sngParam1, sngParam2, sngParam3)
				
				
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
					envi.checkTimeAndSetPolicy(gen)
					#raw_input('click any buttom to continue... ')
				# Save results on file 
				envi.saveAgentsXMLformat()
				envi.saveOnFile(ns)
				envi.saveAgentsOnFile(ns)
				envi.saveTechsOnFile(ns)
				envi.savePoliciesOnFile(ns)
				
				# reset simulation 
				envi.resetSimulation()
				
			# Del environment
			envi.saveTotalOnFile()
			del envi
