#!/usr/bin/env python
'''
This file contains useful procedure to analyse outcomes of SENSOR model.
'''

import sys, os  # Standard library
import datetime as dt
import glob
import numpy as np  # Scientific library
from argparse import ArgumentParser
from numpy import *

try:
    from pylab import *
except:
    pass

# Input parameters definition 
if __name__ == '__main__':
    parser = ArgumentParser(
        description='ELDA (Emergent Levell Dynamic	 Assessment).'
        , epilog='''Copyright Alessandro Filisetti 2013 ''')
    parser.add_argument('-p', '--StrPath', help='Path where files are stored', default='./')
    args = parser.parse_args()

    print "Simulation Results Path: ", args.StrPath

    # Convert path in absolute path
    StrPath = os.path.abspath(args.StrPath)

    # Result DIRS
    tmpDirs = sort(os.listdir(StrPath))

    # For each set of simulations
    print '** SENSOR OUTCOMES ANALYSIS **'
    for fold in tmpDirs:
        os.chdir(StrPath)
        totDirName = os.path.join(StrPath, fold)
        if os.path.isdir(totDirName):
            print '|- Folder: ', fold
