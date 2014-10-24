#!/usr/bin/env python
"""@package SENSOR
   \mainpage SENSOR
   \author Alessandro Filisetti
     
	More details.
"""

import sys, os
from time import time
from argparse import ArgumentParser
from lib.classes import env as en
from lib.analysis import statistics as st

_SENSORVERSION_ = '1.2b20140508'

# Input parameters definition 
if __name__ == '__main__':
	parser = ArgumentParser(
				description='ELDA (Emergent Levell Dynamic Assessment). Version ' + _SENSORVERSION_
				, epilog='''Copyright Alessandro Filisetti 2013 ''') 
	parser.add_argument('-p', '--StrPath', help='Path where configuration files are stored', default='./')
	args = parser.parse_args()
	
	StrPath = os.path.abspath(args.StrPath)
	
	initTime = time()
		
	_TIMEPROMPT_ = 10
	
	print "\n* * * * * * * * * * * * * * * * * * * * * * * * * *"
	print "\tWELCOME, SIMULATION IS GOING TO START..."
	print "* * * * * * * * * * * * * * * * * * * * * * * * * * * \n"

			
	# Initialize environment
	envi = en.environment(StrPath)
	# Create folder simulation and store initial conditions
	envi.createFolderAndSaveInitialConditions(None, None, None)
	envi.printParams()

	# For each seed
	for ns in range(envi.nSeed):
	
		envi.createPopulation()
		envi.createTechnologies()
		envi.createPolicies(None, None, None)
		
		# Create file where dynamical activity will be saved
		tmpFileName = '_dynamicaActivity_' + str(ns) + '.csv'
		dynActFid = open(os.path.join(StrPath,envi.simFolder,tmpFileName), 'w')
		
		# DYNAMICSopen(os.path.join(newdirAllResults,tmpFluxFile), 'w')
		for gen in range(1, envi.months+1):
			if gen % _TIMEPROMPT_ == 0:
				try:
					print " \t- MONTH NUMBER ", gen, " TOT CO2: ", \
					envi.totCO2[-1], " TOT COSTS: ", envi.totCosts[-1], " TOT DEBTS: ", envi.totDebt[-1]#, " dt: ", time()-initTime
				except:
					print " \t- MONTH NUMBER ", gen, " TOT CO2: ", \
					envi.totCO2, " TOT COSTS: ", envi.totCosts, " TOT DEBTS: ", envi.totDebt#, " dt: ", time()-initTime
			
			# Standard month activities and New Technology evaluation
			envi.agentMonthNRGAct_and_newTechAss(gen,dynActFid)
			envi.checkTimeAndSetPolicy(gen)
			
			if gen % _TIMEPROMPT_ == 0:
				if len(envi.totSolarBasedInstallation) > 0:
					print "\t|- TOT SOLAR BASED DIFFUSION"
					print "\t\t|- Number of agents adopting a solar based tech: {0} - Total kWh: {1} - Total kW: {2}".format(envi.totSolarBasedInstallation[-1],\
																													 envi.totSolarBasedKWh[-1],\
																													 envi.totSolarBasedKW[-1])
				for sTech in envi.allTechs:
					print "\t\t\t|- Tech: {0}, Solar Based: {1}, Total Amount: {2}".format(sTech.ID, sTech.solarBased, sum(sTech.techKWHdist))	
		
		print envi.totSolarBasedKW
		
		dynActFid.close()
		
		# LINEAR REGRESSION METHOD 2
		st.linearregression(envi.months, envi.totSolarBasedKW)
		st.polynomialregression(range(envi.months), envi.totSolarBasedKW, 2)

		
	del envi