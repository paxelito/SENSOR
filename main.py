#!/usr/bin/env python
"""@package SENSOR
   \mainpage SENSOR
   \author Alessandro Filisetti
     
	More details.
"""

import sys, os
import random as ran
from time import time
from argparse import ArgumentParser
from lib.classes import env as en

# Input parameters definition 
if __name__ == '__main__':
	parser = ArgumentParser(
				description='ELDA (Emergent Levell Dynamic	 Assessment).'
				, epilog='''Copyright Alessandro Filisetti 2013 ''') 
	parser.add_argument('-p', '--StrPath', help='Path where configuration files are stored', default='./')
	args = parser.parse_args()
	
	StrPath = os.path.abspath(args.StrPath)
	
	initTime = time()
		
	#varParList1 = [0.25, 0.5, 0.75, 1]
	#varParList2 = [0.25, 0.5, 0.75, 1]
	#varParList3 = [0.25, 0.5, 0.75, 1]
	varParList1 = [None]
	varParList2 = [None]
	varParList3 = [None]
	
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
					
					# Create file where dynamical activity will be saved
					tmpFileName = '_dynamicaActivity_' + str(ns) + '.csv'
					dynActFid = open(os.path.join(StrPath,envi.simFolder,tmpFileName), 'w')
					
					# DYNAMICSopen(os.path.join(newdirAllResults,tmpFluxFile), 'w')
					for gen in range(1, envi.months+1):
						if gen % 10 == 0:
							try:
								print " \- feedIN: ", sngParam1, " Prop: ", sngParam2 ,"NSEED: ", ns, "MONTH NUMBER ", gen, " TOT CO2: ", \
								envi.totCO2[-1], " TOT COSTS: ", envi.totCosts[-1], " TOT DEBTS: ", envi.totDebt[-1], " dt: ", time()-initTime
							except:
								print " \- feedIN: ", sngParam1, " Prop: ", sngParam2 , " NSEED: ", ns, "MONTH NUMBER ", gen, " TOT CO2: ", \
								envi.totCO2, " TOT COSTS: ", envi.totCosts, " TOT DEBTS: ", envi.totDebt, " dt: ", time()-initTime
						
						# Standard month activities and New Technology evaluation
						envi.agentMonthNRGAct_and_newTechAss(gen,dynActFid)
						envi.checkTimeAndSetPolicy(gen)
					
					dynActFid.close()
						
					# Save results on file 
					envi.saveAgentsXMLformat()
					envi.saveOnFile(ns)
					envi.saveAgentsOnFile(ns)
					envi.saveTechsOnFile(ns)
					envi.savePoliciesOnFile(ns)
					envi.saveNet('net')
					envi.saveNoActiveAgent('noActive')
					
					# reset simulation 
					envi.resetSimulation()
					
				# Del environment
				envi.saveTotalOnFile()
				del envi
