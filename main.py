#!/usr/bin/env python

import sys, os
import env as en
import random as ran

# get path for placing simulation
try:
	StrPath = sys.argv[1] # Here the path of the simulation
except:
	print "Usage:",sys.argv[0], "Error in the parameter introduction"; sys.exit(1)
	
varParList = [50, 100, 200, 300, 400, 500, 600]
nSeed = 25
nTech = 3

for sngParam in varParList:

	# Initialize environment
	envi = en.environment(StrPath, sngParam)
	envi.printParams()

	# FOr each seed
	for ns in range(nSeed):
	
		envi.createPopulation()
		#envi.printPopulation()
		envi.createThreeDefaultTechs(sngParam)
		
		# DYNAMICS
		for gen in range(1, envi.months+1):
			try:
				print " \- PARAM: ", sngParam, " NSEED: ", ns, "MONTH NUMBER ", gen, " TOT CO2: ", envi.totCO2[-1], " TOT COSTS: ", envi.totCosts[-1], " TOT DEBTS: ", envi.totDebt[-1]
			except:
				print " \- PARAM: ", sngParam, " NSEED: ", ns, "MONTH NUMBER ", gen, " TOT CO2: ", envi.totCO2, " TOT COSTS: ", envi.totCosts, " TOT DEBTS: ", envi.totDebt
			# Standard month activities
			envi.agentMonthEnergyActivity(gen)	
			# New Technology evaluation
			envi.newTechAssessment(gen)
		# Save results on file 
		envi.saveOnFile(ns)
		
		# reset simulation 
		envi.resetSimulation()
		
	# Del environment
	envi.saveTotalOnFile(nTech)
	del envi
