#!/usr/bin/env python
'''
This file contains useful procedure to analyse outcomes of SENSOR model.
'''

import sys, os # Standard library
import datetime as dt
import glob
import numpy as np # Scientific library
from numpy import * 

try:
    from pylab import *
except:
    pass
   
# get path for placing simulation
try:
	StrPath = sys.argv[1] # Here the path of the simulation output file
except:
	print "Usage:",sys.argv[0], "infile outfile"; sys.exit(1)
	
print "Simulation Results Path: ", StrPath

# Convert path in absolute path
StrPath = os.path.abspath(StrPath)

# Result DIRS
tmpDirs = sort(os.listdir(StrPath))

# For each set of simulations
print '** SENSOR OUTCOMES ANALYSIS **'
for fold in tmpDirs:
	os.chdir(StrPath)
	totDirName = os.path.join(StrPath,fold)
	if os.path.isdir(totDirName):
		print '|- Folder: ', fold
	
	
	

