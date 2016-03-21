#!/usr/bin/env python
'''Function to compute policy post-ante analysis
'''

import sys, os  # Standard library
import datetime as dt
import linecache as lc
import glob
from argparse import ArgumentParser
import numpy as np  # Scientific library
from numpy import *

try:
    from pylab import *
except:
    pass


# --------------------------------------------------------------------------------------
# Function to create string zero string vector before graph filename. 
# According to the total number of reactions N zeros will be add before the instant reaction number 
# (e.g. reaction 130 of 10000 the string became '00130')
def zeroBeforeStrNum(tmpl, tmpL):
    strZero = ''
    nZeros = len(str(tmpL)) - len(str(tmpl))
    if nZeros > 0:
        for i in range(0, nZeros): strZero = strZero + '0'
    return strZero


# Input parameters definition
if __name__ == '__main__':
    parser = ArgumentParser(
        description='ELDA (Emergent Levell Dynamic	 Assessment).'
        , epilog='''Copyright Alessandro Filisetti 2013 ''')
    parser.add_argument('-p', '--StrPath', help='Path where files are stored', default='./')
    parser.add_argument('-t', '--tech', help='Technology to Analyse', default='2')
    args = parser.parse_args()

    print "Simulation Results Path: ", args.StrPath

    StrPath = os.path.abspath(args.StrPath)

    today = dt.date.today()

    StrPath = os.path.abspath(StrPath)

    print ''
    print 'POLICIES ANALYSIS'
    print ''

    tmpX = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    tmpY = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    tmpDirs = sort(os.listdir(StrPath))

    results = []

    for tmpDir in tmpDirs:
        print "Directory ", tmpDir
        os.chdir(StrPath)
        totDirName = os.path.join(StrPath, tmpDir)
        if os.path.isdir(totDirName):
            # Move to the directory
            os.chdir(totDirName)

            # POLICIES
            tmpFileName = os.path.join(totDirName, 'policies_0.csv')
            try:
                fileFID = open(tmpFileName, 'r')
            except:
                print "Policies file has not been found: ", tmpFileName;
                sys.exit(1)
            fileFID = open(tmpFileName, 'r')
            # read file
            policies = fileFID.readlines()
            # for each policy
            FIlist = [];
            TCIList = [];
            AmountList = [];
            for t in policies:
                if t[0] != '#':
                    # tmpID, tmpFI, tmpTC, tmpTCI, tmpCT, tmpL, tmpIT, tmpA, tmpR, tmpIT = t.split()
                    tmpID, tmpFI, tmpTC, tmpTCI, tmpCT, tmpL, tmpIT, tmpA, tmpR = t.split()
                    # Insert technology
                    FIlist.append(float(tmpFI))
                    TCIList.append(float(tmpTCI))
                    AmountList.append(float(tmpA))
            fileFID.close()

            tmpFnane = '_overall_tech_' + args.tech + '.csv'
            tmpFileName = os.path.join(totDirName, tmpFnane)
            try:
                fileFID = open(tmpFileName, 'r')
            except:
                print tmpFnane, " file has not been found: ", tmpFileName;
                sys.exit(1)
            fileFID = open(tmpFileName, 'r')
            # read file
            solarN = fileFID.readlines()
            # for each time number of agents
            nAgentsSolar = []
            for t in solarN:
                if t[0] != '#':
                    nAgentsSolar.append(int(t))
            fileFID.close()

            # OVERALL AIDS
            tmpFileName = os.path.join(totDirName, '_overall_aids.csv')
            try:
                fileFID = open(tmpFileName, 'r')
            except:
                print "_overall_aids file has not been found: ", tmpFileName;
                sys.exit(1)
            fileFID = open(tmpFileName, 'r')
            # read file
            aids = fileFID.readlines()
            # for each time number of agents
            tmpTotAids = 0
            for t in aids:
                if t[0] != '#':
                    tmpTotAids += float(t)
            fileFID.close()

            # OVERALL C02
            tmpFileName = os.path.join(totDirName, '_overall_CO2.csv')
            try:
                fileFID = open(tmpFileName, 'r')
            except:
                print "_overall_CO2 file has not been found: ", tmpFileName;
                sys.exit(1)
            fileFID = open(tmpFileName, 'r')
            # read file
            CO2file = fileFID.readlines()
            # for each time number of agents
            nCO2List = []
            for t in CO2file:
                if t[0] != '#':
                    nCO2List.append(float(t))
            fileFID.close()

            # OVERALL DEBT
            tmpFileName = os.path.join(totDirName, '_overall_debt.csv')
            try:
                fileFID = open(tmpFileName, 'r')
            except:
                print "_overall_debt file has not been found: ", tmpFileName;
                sys.exit(1)
            fileFID = open(tmpFileName, 'r')
            # read file
            debtfile = fileFID.readlines()
            # for each time number of agents
            debtList = []
            for t in debtfile:
                if t[0] != '#':
                    debtList.append(float(t))
            fileFID.close()

            # OVERALL COSTS
            tmpFileName = os.path.join(totDirName, '_overall_costs.csv')
            try:
                fileFID = open(tmpFileName, 'r')
            except:
                print "_overall_costs file has not been found: ", tmpFileName;
                sys.exit(1)
            fileFID = open(tmpFileName, 'r')
            # read file
            costfile = fileFID.readlines()
            # for each time number of agents
            costsList = []
            for t in costfile:
                if t[0] != '#':
                    costsList.append(float(t))
            fileFID.close()

            results.append((FIlist[-1], TCIList[-1], nAgentsSolar[-1], tmpTotAids, \
                            nCO2List[-1], nCO2List[0] - nCO2List[-1], 1 - (float(nCO2List[-1]) / float(nCO2List[0])), \
                            debtList[-1], costsList[-1]))

    # print results
    tempDim = int(pow(len(results), 0.5))
    agents_N_perc = np.zeros((tempDim, tempDim))
    agents_N = np.zeros((tempDim, tempDim))
    aids_N = np.zeros((tempDim, tempDim))
    CO2_N = np.zeros((tempDim, tempDim))
    CO2_N_saved = np.zeros((tempDim, tempDim))
    CO2_N_saved_perc = np.zeros((tempDim, tempDim))
    debt_N = np.zeros((tempDim, tempDim))
    costs_N = np.zeros((tempDim, tempDim))
    Xmatrix = np.zeros((tempDim, tempDim))
    Ymatrix = np.zeros((tempDim, tempDim))

    FIlistFINAL = [];
    TCIListFINAL = [];
    nAgentsSolarFINAL = [];
    for sr in results:
        agents_N_perc[tmpX.index(sr[0])][tmpY.index(sr[1])] = float(sr[2]) / 1000
        agents_N[tmpX.index(sr[0])][tmpY.index(sr[1])] = float(sr[2])
        aids_N[tmpX.index(sr[0])][tmpY.index(sr[1])] = int(sr[3])
        CO2_N[tmpX.index(sr[0])][tmpY.index(sr[1])] = int(sr[4])
        CO2_N_saved[tmpX.index(sr[0])][tmpY.index(sr[1])] = int(sr[5])
        CO2_N_saved_perc[tmpX.index(sr[0])][tmpY.index(sr[1])] = float(sr[6])
        debt_N[tmpX.index(sr[0])][tmpY.index(sr[1])] = int(sr[7])
        costs_N[tmpX.index(sr[0])][tmpY.index(sr[1])] = int(sr[8])
        FIlistFINAL.append(sr[0])
        TCIListFINAL.append(sr[1])
        nAgentsSolarFINAL.append(sr[2])

    os.chdir(StrPath)

    print '   |- Saving RESULTS...'
    outFnameStat = '0_results.csv'
    saveFileStat = open(outFnameStat, 'w')
    strTypes = '# FEED_IN\tTAX_CRED_INV\tnAGENT_SOLAR\tAIDS\tCO2\tCO2saved\tCO2savedperc\tDEBT\tCOSTS\n'
    saveFileStat.write(strTypes)
    for i in results:
        strTypes = ''
        for j in i:
            strTypes += str(j) + '\t'
        strTypes += '\n'
        saveFileStat.write(strTypes)
    saveFileStat.close()

    print '   |- Saving THE PERCENTAGE OF AGENTS ADOPTING THE INNOVATION...'
    outFnameStat = '0_agents_perc_' + args.tech + '.csv'
    saveFileStat = open(outFnameStat, 'w')
    for i in range(tempDim):
        strTypes = ''
        for j in range(tempDim):
            strTypes += str(agents_N_perc[i, j]) + '\t'
        strTypes += '\n'
        saveFileStat.write(strTypes)
    saveFileStat.close()

    print '   |- Saving NUMBER OF AGENTS ADOPTING THE INNOVATION...'
    outFnameStat = '0_agents_N_' + args.tech + '.csv'
    saveFileStat = open(outFnameStat, 'w')
    for i in range(tempDim):
        strTypes = ''
        for j in range(tempDim):
            strTypes += str(agents_N[i, j]) + '\t'
        strTypes += '\n'
        saveFileStat.write(strTypes)
    saveFileStat.close()

    print '   |- Saving CO2...'
    outFnameStat = '0_CO2.csv'
    saveFileStat = open(outFnameStat, 'w')
    for i in range(tempDim):
        strTypes = ''
        for j in range(tempDim):
            strTypes += str(CO2_N[i, j]) + '\t'
        strTypes += '\n'
        saveFileStat.write(strTypes)
    saveFileStat.close()

    print '   |- Saving CO2 saved...'
    outFnameStat = '0_CO2_saved.csv'
    saveFileStat = open(outFnameStat, 'w')
    for i in range(tempDim):
        strTypes = ''
        for j in range(tempDim):
            strTypes += str(CO2_N_saved[i, j]) + '\t'
        strTypes += '\n'
        saveFileStat.write(strTypes)
    saveFileStat.close()

    print '   |- Saving CO2 saved...'
    outFnameStat = '0_CO2_saved_perc.csv'
    saveFileStat = open(outFnameStat, 'w')
    for i in range(tempDim):
        strTypes = ''
        for j in range(tempDim):
            strTypes += str(CO2_N_saved_perc[i, j]) + '\t'
        strTypes += '\n'
        saveFileStat.write(strTypes)
    saveFileStat.close()

    print '   |- Saving debt...'
    outFnameStat = '0_debt.csv'
    saveFileStat = open(outFnameStat, 'w')
    for i in range(tempDim):
        strTypes = ''
        for j in range(tempDim):
            strTypes += str(debt_N[i, j]) + '\t'
        strTypes += '\n'
        saveFileStat.write(strTypes)
    saveFileStat.close()

    print '   |- Saving costs...'
    outFnameStat = '0_costs.csv'
    saveFileStat = open(outFnameStat, 'w')
    for i in range(tempDim):
        strTypes = ''
        for j in range(tempDim):
            strTypes += str(costs_N[i, j]) + '\t'
        strTypes += '\n'
        saveFileStat.write(strTypes)
    saveFileStat.close()

    print '   |- Saving OVERALL AIDS...'
    outFnameStat = '0_aids.csv'
    saveFileStat = open(outFnameStat, 'w')
    for i in range(tempDim):
        strTypes = ''
        for j in range(tempDim):
            strTypes += str(aids_N[i, j]) + '\t'
        strTypes += '\n'
        saveFileStat.write(strTypes)
    saveFileStat.close()
