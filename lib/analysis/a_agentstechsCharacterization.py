#!/usr/bin/env python
# -*- coding: latin-1 -*-
'''Function to characterize agents and technologies
'''

import sys, os  # Standard library
import datetime as dt
import linecache as lc
import glob
import numpy as np  # Scientific library
from numpy import *

try:
    from pylab import *
except:
    pass


# -- FUNCTIONS

def zeroBeforeStrNum(tmpl, tmpL):
    strZero = ''
    nZeros = len(str(tmpL)) - len(str(tmpl))
    if nZeros > 0:
        for i in range(0, nZeros): strZero = strZero + '0'
    return strZero


def importAgents(tmpDir, tmpSeed):
    '''Function to import agents from a file previously prepared'''
    # file name
    fileName = "agents_" + str(tmpSeed) + ".csv"
    tmpFileName = os.path.join(tmpDir, fileName)
    try:
        fileFID = open(tmpFileName, 'r')
    except:
        print "Agent file has not been found: ", tmpFileName;
        sys.exit(1)
    fileFID = open(tmpFileName, 'r')
    # read file
    agents = fileFID.readlines()

    # for each Agent
    cnt = 0
    for a in agents:
        if a[0] != '#':
            tmpID, tmpX, tmpY, tmpEN, tmpSolPot, tmpCO2, tmpSocialLobby, tmpintCap, \
            tmpEquity, tmpBalance, tmpMbalance, tmpInvL, tmpHealth, tmpAge = a.split()

            dimension = int(tmpEN);
            health = float(tmpHealth);
            equity = float(tmpintCap);
            lobby = float(tmpSocialLobby)
            id = int(tmpID)
            # Insert Agent
            if cnt == 0:
                retAgentMtx = np.array([[id, dimension, health, equity, lobby]])
            else:
                retAgentMtx = np.vstack([retAgentMtx, (id, dimension, health, equity, lobby)])
            cnt += 1

    fileFID.close()

    return retAgentMtx


def importAgentTechList(tmpDir, tmpSeed):
    '''Function to import agents from a file previously prepared'''
    # file name
    fileName = "agentLists_" + str(tmpSeed) + ".csv"
    tmpFileName = os.path.join(tmpDir, fileName)
    try:
        fileFID = open(tmpFileName, 'r')
    except:
        print "Agent Tech file has not been found: ", tmpFileName;
        sys.exit(1)
    fileFID = open(tmpFileName, 'r')
    # read file
    retAgentTechList = fileFID.readlines()

    fileFID.close()

    return retAgentTechList


# -- SCRIPTS
# get path for placing simulation
try:
    StrPath = sys.argv[1]  # Here the path of the simulation output file
except:
    print "Usage:", sys.argv[0], "infile outfile";
    sys.exit(1)

print "Simulation Results Path: ", StrPath

StrPath = os.path.abspath(StrPath)

print '\n|--------------------------------------|'
print '| AGENTS TECHNOLOGIES CHARACTERIZATION |'
print '|--------------------------------------|\n'

tmpDirs = sort(os.listdir(StrPath))

for tmpDir in tmpDirs:
    os.chdir(StrPath)
    totDirName = os.path.join(StrPath, tmpDir)
    if os.path.isdir(totDirName):
        print " |- Processing Directory --> ", totDirName
        # Move to the directory
        os.chdir(totDirName)
        print "  |- Select files to process..."
        agentListFiles = sorted(glob.glob(os.path.join(totDirName, 'agentLists_*')))
        agentFiles = sorted(glob.glob(os.path.join(totDirName, 'agents_*')))
        for seed, fileS in enumerate(agentListFiles):
            print "  |- Load agents file..."
            agentMtx = importAgents(totDirName, seed)
            print "  |- Load Agent Tech List..."
            agentTechs = importAgentTechList(totDirName, seed)
            print "  |- Agents and Technologies characterization process..."
            cnt = 0
            for sngRow in agentTechs:
                if sngRow[0] != '#':
                    tmpAgent, tmpTech, tmpProp, tmpAge = sngRow.split()
                    agentID = int(tmpAgent);
                    tech = int(tmpTech);
                    prop = float(tmpProp);
                    age = int(tmpAge)
                    if cnt == 0:
                        finalMtx = np.array([[agentMtx[agentID, 0], agentMtx[agentID, 1], agentMtx[agentID, 2],
                                              agentMtx[agentID, 3], agentMtx[agentID, 4], \
                                              tech, prop, age]])
                    else:
                        finalMtx = np.vstack([finalMtx, (
                        agentMtx[agentID, 0], agentMtx[agentID, 1], agentMtx[agentID, 2], agentMtx[agentID, 3],
                        agentMtx[agentID, 4], \
                        tech, prop, age)])
                    cnt += 1

            print "  |- Save processed structure..."
            tmpFileName = '__agentTechs_' + str(seed) + '.csv'
            tmpFileNameFID = open(tmpFileName, 'w')
            ID = 0
            tmpStr = "#ID\tdimension\thealth\tequity\tlobby\ttech\tprop\tage\n"
            tmpFileNameFID.write(tmpStr)
            for sngCnt in finalMtx:
                tmpStr = str(sngCnt[0]) + '\t' + str(sngCnt[1]) + '\t' + str(sngCnt[2]) + '\t' + str(sngCnt[3]) + '\t' + \
                         str(sngCnt[4]) + '\t' + str(sngCnt[5]) + '\t' + str(sngCnt[6]) + '\t' + str(sngCnt[7]) + '\n'
                tmpFileNameFID.write(tmpStr)
                ID += 1
            tmpFileNameFID.close()
