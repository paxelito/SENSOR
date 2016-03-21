#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''Class environment definition.

.. module:: env
   :platform: Unix, Windows
   :synopsis: The module containing the main class.
   
.. moduleauthor:: Alessandro Filisetti <alessandro.filisetti@unibo.it>

'''

import sys, os
import time
import agents as ag
import random as ran
import cPickle as pickle
import shutil
import numpy as np
from ..classes import policy
from ..classes import tech


class environment:
    '''Class environment definition.'''

    def __init__(self, tmpPath):
        '''
            constructor
        '''
        # Parameters file name and path
        paramFile = tmpPath + "/init.conf"  # Open Param file
        print paramFile + "\n"
        try:
            fid = open(paramFile, 'r')
        except:
            print 'impossible to load ', paramFile;
            sys.exit(1)

        self.simPath = os.path.abspath(tmpPath)

        for line in fid:
            strLine = line.split('=')
            if strLine[0] == "randomSeed":
                self.randomSeed = int(strLine[1]);
                continue
            if strLine[0] == "nSeed":
                self.nSeed = int(strLine[1]);
                continue
            if strLine[0] == "agents":
                self.Nagents = int(strLine[1]);
                continue
            if strLine[0] == "techCreationMethod":
                self.techCreationMethod = int(strLine[1]);
                continue
            if strLine[0] == "agentCreationMethod":
                self.agentCreationMethod = int(strLine[1]);
                continue
            if strLine[0] == "policyCreationMethod":
                self.policyCreationMethod = int(strLine[1]);
                continue
            if strLine[0] == "months":
                self.months = int(strLine[1]);
                continue
            if strLine[0] == "xMaxPos":
                self.xMaxPos = int(strLine[1]);
                continue
            if strLine[0] == "yMaxPos":
                self.yMaxPos = int(strLine[1]);
                continue
            if strLine[0] == "minIrradiation":
                self.minIrradiation = int(strLine[1]);
                continue
            if strLine[0] == "minNrgDim":
                self.minNrgDim = int(strLine[1]);
                continue
            if strLine[0] == "maxNrgDim":
                self.maxNrgDim = int(strLine[1]);
                continue
            if strLine[0] == "ratioInternalCapital":
                self.ratioInternalCapital = float(strLine[1]);
                continue
            if strLine[0] == "invLength":
                self.invLength = int(strLine[1]);
                continue
            if strLine[0] == "creditAssessment":
                self.creditAssessment = int(strLine[1]);
                continue
            if strLine[0] == "loanLength":
                self.loanLength = int(strLine[1]);
                continue
            if strLine[0] == "intRiskRate":
                self.intRiskRate = float(strLine[1]);
                continue
            if strLine[0] == "socialLobby_betadist_alpha":
                self.socialLobby_betadist_alpha = float(strLine[1]);
                continue
            if strLine[0] == "socialLobby_betadist_beta":
                self.socialLobby_betadist_beta = float(strLine[1]);
                continue
            if strLine[0] == "health":
                self.H = float(strLine[1]);
                continue
            if strLine[0] == "debugLevel":
                self.debugLevel = float(strLine[1]);
                continue
            if strLine[0] == "agroMaxDim":
                self.agroMaxDim = float(strLine[1]);
                continue
            if strLine[0] == "agroProfit":
                self.agroProfit = float(strLine[1]);
                continue

        # DEFAULT parameters
        if 'randomSeed' not in dir(self): self.randomSeed = 0
        if 'creditAssessment' not in dir(self): self.creditAssessment = 0

        if self.randomSeed == 1:
            # ! Set randomly the random state and store it in a file
            ran.seed(int(time.time()))
            self.saveRandomSeed()
        else:
            self.loadRandomSeed()

        # FitnessList and amountList and fitnessSigma have to be of the same length
        self.allAgents = []

        # Technologies
        self.allTechs = []
        self.allTechsID = []  # Useful to speed up the computation
        # Policies
        self.allPolicies = []
        self.overallEnergyNeed = 0

        # STAT VARIABLES
        self.totCO2 = []
        self.totDebt = []
        self.totCosts = []
        self.totAids = []
        self.tottotCO2 = []
        self.tottotDebt = []
        self.tottotCosts = []
        self.tottotAids = []
        self.totTechNRGdist = []
        self.totTechKWHdist = []
        self.totTechKWdist = []
        self.tottotTechNRGdist = []
        self.tottotTechKWHdist = []
        self.tottotTechKWdist = []

        # Solar summary
        self.totSolarBasedInstallation = []
        self.totSolarBasedKW = []
        self.totSolarBasedKWh = []

        # CREATE SIMULATION FOLDER
        self.simFolder = ''

    def resetSimulation(self):
        '''Function to reset simulation'''

        del self.allAgents[:]
        del self.allTechs[:]
        del self.allTechsID[:]  # Useful to speed up the computation
        del self.allPolicies[:]  # Useful to speed up the computation

        # STAT VARIABLES
        self.tottotCO2.append(self.totCO2)
        self.tottotDebt.append(self.totDebt)
        self.tottotCosts.append(self.totCosts)
        self.tottotAids.append(self.totAids)

        self.tottotTechNRGdist.append(self.totTechNRGdist)
        self.tottotTechKWHdist.append(self.totTechKWHdist)
        self.tottotTechKWdist.append(self.totTechKWdist)

        del self.totCO2[:]
        del self.totDebt[:]
        del self.totCosts[:]
        del self.totAids[:]
        del self.totTechNRGdist[:]
        del self.totTechKWHdist[:]
        del self.totTechKWdist[:]

    def saveRandomSeed(self):
        '''Function to save the random seed'''

        with open(os.path.join(self.simPath, "rndstate.dat"), 'wb') as f:
            pickle.dump(ran.getstate(), f)

    def loadRandomSeed(self):
        '''Function to load a previously saved random seed'''

        seedFile = os.path.join(self.simPath, "rndstate.dat")

        print seedFile

        if os.path.exists(seedFile):
            # Restore the previously saved sate
            print '\n|- Found rndstate.dat, initializing random module...\n'
            with open(seedFile, 'rb') as f:
                state = pickle.load(f)
            ran.setstate(state)
        else:
            # Use a well-known start state
            print 'No rndstate.dat, seeding a random state'
            ran.seed(int(time.time()))

    def createFolderAndSaveInitialConditions(self, tmpPar=None, tmpPar2=None, tmpPar3=None):
        '''
            Function to create the simulation folder and save the initial conditions

        '''
        #: this is the folder name
        self.simFolder = time.strftime("%y%m%d_%H_%M") + "_" + str(tmpPar) + "_" + str(tmpPar2) + "_" + str(tmpPar3)

        if not os.path.exists(os.path.join(self.simPath, self.simFolder)): os.makedirs(
            os.path.join(self.simPath, self.simFolder))
        # Copy file into results folder (copy2 because also file metadata are copied)
        shutil.copy2(os.path.join(self.simPath, "rndstate.dat"),
                     os.path.join(self.simPath, self.simFolder, "rndstate.dat"))
        shutil.copy2(os.path.join(self.simPath, "init.conf"), os.path.join(self.simPath, self.simFolder, "init.conf"))

    def printPopulation(self):
        ''' Function to output some parameters of the population

        >>> --------------
        - AGENT 4
        |- Coordinates: 12.3243 32.3432 - EN: 345

        :returns:  void.

        '''
        count = 1
        if self.debugLevel == 0:
            for i in self.allAgents:
                print "--------------"
                print "- AGENT ", i.ID
                print "\t|- Coordinates: ", i.x, " ", i.y, " - EN: ", i.totEnergyNeed
                count = count + 1

    def printParams(self):
        ''' Function to print all simulation parameters (e.g.)

        >>> |- SYSTEM PARAMS ---"
        |- Simulation results path: ~/path/of/the/sim
        |- PARAMETERS ---
        |- Random Seed: 0
        |- Number of Agents: 100
        |- Number of Months: 360
        |- X: 1000
        |- Y: 1000
        |- minIrradiation: 100
        |- minNrgDim: 1
        |- maxNrgDim: 100
        |- ratioInternalCapital: 23
        |- invLength: 20
        |- loanLength: 10
        |- intRiskRate: ", self.intRiskRate

        '''
        print "* SYSTEM PARAMS -----------------------------------------------"
        print ""
        print " |- Simulation results path: ", self.simPath
        print "|- Parameters"
        print " |- Random Seed: ", self.randomSeed
        print " |- Number of Agents: ", self.Nagents
        print " |- Number of Months: ", self.months
        print " |- X: ", self.xMaxPos
        print " |- Y: ", self.yMaxPos
        print " |- minIrradiation: ", self.minIrradiation
        print " |- minNrgDim: ", self.minNrgDim
        print "	|- maxNrgDim: ", self.maxNrgDim
        print "	|- ratioInternalCapital: ", self.ratioInternalCapital
        print "	|- invLength (years): ", self.invLength
        print "	|- loanLength (Month): ", self.loanLength
        print "	|- intRiskRate: ", self.intRiskRate

    def genDistanceLists(self):
        ''' Function to generate the distances matrix containing all the distances between agents'''

        # For each agents the distance from the other agents is computer and inserted in the matrix
        ID_r = 0;
        for singleAgent in self.allAgents:
            ID_c = 0;
            for ag_col in self.allAgents:
                # Pitagora to compute the distance between two different point
                singleAgent.distanceList.append(
                    pow(pow((singleAgent.x - ag_col.x), 2) + pow((singleAgent.y - ag_col.y), 2), 0.5))
                ID_c = ID_c + 1
            ID_r = ID_r + 1

            # 	def agentMonthEnergyActivity(self, tmpGen):
            # 		'''Bridge function from the main the agent class'''
            # 		for sngAgent in self.allAgents:
            # 			sngAgent.computeMonthNrgCostsAndPoll(self.allTechs, tmpGen, self.allPolicies)
            # 			sngAgent.performFinancialActivities()
            # 			sngAgent.updateEnergyPropAccordingToEfficiencyDrop(self.allTechs)
            # 		# Stat functions
            # 		self.statFunctions()

    def newTechAssessment(self, tmpTime):
        # According to the average investment evaluation time (once per year) and the agent wealth and policy aids are decreased
        tmp_tAids = 0
        for sngAgent in self.allAgents:
            polToUpdate = sngAgent.invAssessment(self.allTechs, self.allTechsID, tmpTime, self.allAgents,
                                                 self.allPolicies, self.agroProfit, self.creditAssessment)
            # Decrement the total amount of incentives to aid within the system
            if polToUpdate[0] > 0:
                self.allPolicies[polToUpdate[0]].residue -= polToUpdate[1]
                tmp_tAids += polToUpdate[1]
                # If incentives are vanished, standard no inc policy is attributed to all technologies using the vanish policy
                if self.allPolicies[polToUpdate[0]].residue <= 0:
                    for sngTech in self.allTechs:
                        if sngTech.policy == polToUpdate[0]:
                            sngTech.policy = 0
        self.totAids.append(tmp_tAids)

    def agentMonthNRGAct_and_newTechAss(self, tmpTime, tmpDynFileFID=None):
        '''
            This function perform all the activity of the agent during the month

            :param tmpTime: current time (month)
            :param tmpDynFileFID: Handle to the file containing dynamical data
        '''
        tmp_tAids = 0
        for sngAgent in self.allAgents:
            sngAgent.computeMonthNrgCostsAndPoll(self.allTechs, tmpTime, self.allPolicies)
            sngAgent.performFinancialActivities()
            sngAgent.updateEnergyPropAccordingToEfficiencyDrop(self.allTechs)

            polToUpdate = sngAgent.invAssessment(self.allTechs, self.allTechsID, tmpTime, self.allAgents,
                                                 self.allPolicies, \
                                                 self.agroProfit, tmpDynFileFID, self.creditAssessment)
            # Decrement the total amount of incentives to aid within the system
            if polToUpdate[0] > 0:
                self.allPolicies[polToUpdate[0]].residue -= polToUpdate[1]
                tmp_tAids += polToUpdate[1]
                # If incentives are vanished, standard no inc policy is attributed to all technologies using the vanish policy
                if self.allPolicies[polToUpdate[0]].residue <= 0:
                    for sngTech in self.allTechs:
                        if sngTech.policy == polToUpdate[0]:
                            sngTech.policy = 0
        self.totAids.append(tmp_tAids)
        # Stat functions
        self.statFunctions()

    def createTechnologies(self):
        '''Function to select, according to the techCreationMethod params, the technology creation function
        '''
        if self.techCreationMethod == 0:
            self.createThreeDefaultTechs()
        elif self.techCreationMethod == 1:
            self.importTechs()
        else:
            "an other function to implement... random technology creation"

        # self.promptTechs()
        self.numOfTechs = len(self.allTechs)

    def createThreeDefaultTechs(self):
        '''Function to create the three default technologies
               def __init__(self, tmpID = 0, tmpEff = 0, tmpST = 0, tmpTotTime = 0, tmpCost = 0, tmpPcost = 0, tmpRate = 0,\
                 tmpCo2 = 0, tmpTransportCosts = 0, tmpLoanLength = 10, tmpLifeDuration = 50, tmpPolicy = 0, tmpFromKWH2KW = 100, \
                 tmpSolarBased = 0, tmpX = 0, tmpY = 0):
        '''
        self.allTechs.append(
            tech.tech(0, 1, 0, 0, 0, self.months, 0, 0.08, 0, 0, 25, 0, self.loanLength, self.invLength, 0, 100, 0))
        self.allTechsID.append(0)
        self.allTechs.append(
            tech.tech(1, 1, 1, 0, 0, self.months, 0, 0.02, 4000, 0.04, 10, 0.003, self.loanLength, self.invLength, 1,
                      100, 0, ran.uniform(0, self.xMaxPos), ran.uniform(0, self.yMaxPos)))
        self.allTechsID.append(1)
        self.allTechs.append(
            tech.tech(2, 1, 1, 0, 0, self.months, 0, -0.07, 4000, 0.04, 5, 0, self.loanLength, self.invLength, 2, 100,
                      1))
        self.allTechsID.append(2)

    def createPopulation(self):
        '''
            Function to create the population

            To assign the social lobby parameter (1-sociallobby is the committiment) the beta distribution is used.
        '''
        # if agentCreationMethod is equal to 0 random population is created otherwise it is uploaded from file
        if self.agentCreationMethod == 0:
            sl = []
            for i in range(0, self.Nagents):
                if self.H == 1:
                    tmprndHealth = (0.1 * np.random.randn(1)) + 0.5
                    if tmprndHealth > 1: tmprndHealth = 1
                    if tmprndHealth < 0: tmprndHealth = 0
                else:
                    tmprndHealth = 0.5
                # Accordind to parameters alpha and beta, the social lobby is provided
                socialLobby = np.random.beta(self.socialLobby_betadist_alpha, self.socialLobby_betadist_beta)
                self.allAgents.append(
                    ag.agents(self.debugLevel, i, ran.uniform(0, self.xMaxPos), ran.uniform(0, self.yMaxPos), \
                              ran.randint(self.minNrgDim, self.maxNrgDim), ran.uniform(0, self.agroMaxDim), \
                              socialLobby, ran.uniform(self.minIrradiation, 1), self.intRiskRate, \
                              self.ratioInternalCapital, self.invLength, tmprndHealth))

        else:
            self.importAgents()

        self.genDistanceLists()
        # self.promptAgents()
        # Compute the overall energy need of the system
        self.computeTotEnergyNeed()

    def createPolicies(self, tmpP=None, tmpP2=None, tmpP3=None):
        '''Function to create the population
        '''
        # if agentCreationMethod is equal to 0 random population is created otherwise it is uploaded from file
        if self.policyCreationMethod == 0:
            self.allPolicies.append(policy.policy())
        # self.allPolicies.append(policy.policy(1,0,0.04,0,0,5,0,0,0,0,0))
        else:
            self.importPolicies()

        if tmpP != None:
            self.allPolicies[2].feedIN = tmpP

        if tmpP2 != None:
            self.allPolicies[2].taxCreditInv = tmpP2

        if tmpP3 != None:
            self.allPolicies[2].totalAmount = tmpP3

        for sngPol in self.allPolicies:
            # 100 is a temporary value representing the average transformation from kWh to kWp
            sngPol.defineTotFinance(self.overallEnergyNeed, 100)

            # self.promptPolicies()

    def createDefaultNoPolicy(self):
        '''Function to create the default policy, i.e. no incentives at all'''
        self.allPolicies.append(policy.policy())

    def importAgents(self):
        '''
            Function to import agents from a file previously prepared

        '''
        print '\n|- AGENTS IMPORT PROCESS...'
        # file name
        tmpFileName = os.path.join(self.simPath, 'initAgents.csv')

        try:
            fileFID = open(tmpFileName, 'r')
        except:
            print "Technology file has not been found: ", tmpFileName;
            sys.exit(1)

        # read file
        agents = fileFID.readlines()

        # for each Agent
        for a in agents:
            if a[0] != '#':
                tmpID, tmpX, tmpY, tmpEN, tmpHA, tmpSolPot, tmpCO2, tmpSocialLobby, tmpintCap, \
                tmpEquity, tmpBalance, tmpMbalance, tmpInvL, tmpHealth, tmpAge = a.split()
                # Insert Agent

                self.allAgents.append(
                    ag.agents(self.debugLevel, int(tmpID), float(tmpX), float(tmpY), float(tmpEN), float(tmpHA),
                              float(tmpSocialLobby), \
                              float(tmpSolPot), float(tmpEquity), float(tmpintCap), int(tmpInvL), float(tmpHealth), 55,
                              int(tmpAge), None, None, None, None, \
                              float(tmpBalance), float(tmpMbalance), None, None, None, None, None))

        fileFID.close()
        print ' |- done...'

    def importPolicies(self):
        '''Function to import policies from a file previously prepared'''
        print '\t\t|- Policies import process...'
        # file name
        tmpFileName = os.path.join(self.simPath, 'initPolicies.csv')
        try:
            fileFID = open(tmpFileName, 'r')
        except:
            print "Policies file has not been found: ", tmpFileName;
            sys.exit(1)
        # read file
        policies = fileFID.readlines()
        # for each technology
        for t in policies:
            if t[0] != '#':
                tmpID, tmpFI, tmpTC, tmpTCI, tmpCT, tmpL, tmpIT, tmpEnd, tmpA, tmpR, tmpIntroTech = t.split()
                self.allPolicies.append(policy.policy(int(tmpID), float(tmpFI), float(tmpTC), float(tmpTCI), \
                                                      float(tmpCT), int(tmpL), int(tmpIT), int(tmpEnd), float(tmpA),
                                                      float(tmpR), \
                                                      int(tmpIntroTech)))
        fileFID.close()

    def importTechs(self):
        '''Function to import technologies from a file previously prepared'''
        print '\t\t|- Technology import process...'
        # file name
        tmpFileName = os.path.join(self.simPath, 'initTechs.csv')
        try:
            fileFID = open(tmpFileName, 'r')
        except:
            print "Technology file has not been found: ", tmpFileName;
            sys.exit(1)
        # read file
        techs = fileFID.readlines()
        # for each technology
        for t in techs:
            if t[0] != '#':
                tmpID, tmpRen, tmpEFF, tmpST, tmpDim, tmpHA2KW, tmpCost, tmpTcost, tmpPcost, tmpRate, \
                tmpLoanLength, tmpDuration, tmpCO2, tmpSB, tmpP, tmpX, tmpY, tmpConversion = t.split()
                # Insert technology
                self.allTechs.append(
                    tech.tech(int(tmpID), int(tmpRen), float(tmpEFF), int(tmpST), int(tmpDim), int(tmpHA2KW),
                              self.months, float(tmpCost), float(tmpPcost), \
                              float(tmpRate), float(tmpCO2), float(tmpTcost), int(tmpLoanLength), int(tmpDuration), \
                              int(tmpP), float(tmpConversion), int(tmpSB), float(tmpX), float(tmpY)))
                self.allTechsID.append(int(tmpID))
        fileFID.close()

    def promptAgents(self):
        '''Function to prompt the present Agents'''
        print ""
        print "* LIST OF AGENTS ----------------------------------------"
        print ""
        for a in self.allAgents:
            print "|- AGENT ID ", a.ID, " - Pos X: ", a.x, " - Pos Y: ", a.y
            print " |- Energy Need ", a.totEnergyNeed
            print " |- Tech receipt ", a.nrgTechsReceipt
            print " |- Tech Policies ", a.techPolicy
            print " |- Agent Age ", a.age
            print " |- Tech Proportions ", a.nrgPropReceipt, " - Solar Potential ", a.solar_potential, " - CO2 production ", a.co2
            print " |- Social Lobby ", a.social_lobby, " - Internal Capital Ratio ", a.int_capital, " - Equity Cost ", a.equityCost
            print " |- Overall Balance ", a.balance, " - Monthly Balance ", a.month_balance, " - Investment Length ", a.invLength, " - Health ", a.health
        print "|- ---------------------"

    def promptTechs(self):
        '''Function to prompt the present technologies'''
        print ""
        print " |---------------------------- LIST OF TECHNOLOGIES ---------------------------------------"
        print " |"
        print " | ID\tRnw\tEff\tTime\tDim\tTechC\tTransC\tPlantC\tR\tLLength\tLTime", \
            "\tGHG\tpolicy\tSolar\tX\tY\tConvCoef"
        for t in self.allTechs:
            print ' | ', t.ID, '\t', t.renewable, '\t', t.efficiency, '\t', t.startTime, '\t', t.plantDimension, '\t', t.cost, '\t', \
                t.transportCosts, '\t', t.plantCost, '\t', t.interestRate, '\t', t.loanLength, '\t', t.duration, '\t', \
                t.co2, '\t', t.policy, '\t', t.solarBased, '\t', t.X, '\t', t.Y, '\t', t.fromKWH2KW
        print " |-------------------------------------------------------------------------------------------"

    def promptPolicies(self):
        '''Function to prompt the present policies'''
        print ""
        print " |---------------------------- LIST OF POLICIES ---------------------------------------"
        print " |"
        print ' | ID\tFeedIn\tTxc\tTxCinv\tCT\tPolLen\tIntro Time\tEnd Time\tAmount\tres\tIntroTech'
        for t in self.allPolicies:
            print ' | ', t.ID, '\t', t.feedIN, '\t', t.taxCredit, '\t', t.taxCreditInv, '\t', t.carbonTax, '\t', \
                t.length, '\t', t.introTime, '\t', t.endTime, '\t', t.totalAmount, '\t', t.residue, '\t', t.introTech

        print " |-------------------------------------------------------------------------------------\n\n"

    def saveAgentsOnFile(self, tmpSeed):
        '''Function to save agents on file'''
        # Filenames
        agentsFileName = 'agents_' + str(tmpSeed) + '.csv'
        listsFileName = 'agentLists_' + str(tmpSeed) + '.csv'
        # File handle
        saveFileStatFid = open(agentsFileName, 'w')
        listsFileFid = open(listsFileName, 'w')
        # File init
        strAgentInit = '#ID\tX\tY\tEnergyNeed\tha\tsolPot\tco2\tsocialLobby\tintCap\tequity\tbalance\tmBalance\tinvL\thealth\tage\n'
        strListInit = '#Agent\tTech\tProp\tage\n'
        # Save first row
        saveFileStatFid.write(strAgentInit)
        listsFileFid.write(strListInit)
        # For each agent
        for a in self.allAgents:
            strAgent = str(a.ID) + '\t' + str(a.x) + '\t' + str(a.y) + '\t' + str(a.totEnergyNeed) + '\t' + str(
                a.ha) + '\t' + \
                       str(a.solar_potential) + '\t' + str(a.co2) + '\t' + str(a.social_lobby) + '\t' + str(
                a.int_capital) + '\t' + \
                       str(a.equityCost) + '\t' + str(a.balance) + '\t' + str(a.month_balance) + '\t' + str(
                a.invLength) + '\t' + \
                       str(a.health) + '\t' + str(a.age) + '\n'

            saveFileStatFid.write(strAgent)
            # For each Technology
            for i, t in enumerate(a.nrgTechsReceipt):
                tmpAge = self.months - a.debtTime[i]
                strList = str(a.ID) + '\t' + str(t) + '\t' + str(a.nrgPropReceipt[i]) + '\t' + str(tmpAge) + '\n'
                listsFileFid.write(strList)

        saveFileStatFid.close()
        listsFileFid.close()

        os.rename(agentsFileName, os.path.join(self.simPath, self.simFolder, agentsFileName))
        os.rename(listsFileName, os.path.join(self.simPath, self.simFolder, listsFileName))

    def saveTechsOnFile(self, tmpSeed):
        '''Function to save tech on file'''
        # Filenames
        techFileName = 'techs_' + str(tmpSeed) + '.csv'
        # File handle
        saveFileStatFid = open(techFileName, 'w')
        # File init
        strTechInit = '#ID\tRnw\tEff\tStarttime\tplantDimension\tfromTons2kWhmese\tcost\ttCost\tpCost\trate\tloanLength\tduration\tco2\tsolarBased\tpolicy\tX\tY\tconversion\n'
        saveFileStatFid.write(strTechInit)
        for t in self.allTechs:
            strTech = str(t.ID) + '\t' + str(t.renewable) + '\t' + str(t.efficiency) + '\t' + str(
                t.startTime) + '\t' + str(t.plantDimension) + '\t' + \
                      str(t.fromTons2kWhmese) + '\t' + str(t.cost) + '\t' + str(t.transportCosts) + '\t' + str(
                t.plantCost) + '\t' + str(t.interestRate) + '\t' + \
                      str(t.loanLength) + '\t' + str(t.duration) + '\t' + str(t.co2) + '\t' + str(t.solarBased) + '\t' + \
                      str(t.policy) + '\t' + str(t.X) + '\t' + str(t.Y) + '\t' + str(t.fromKWH2KW) + '\n'

            saveFileStatFid.write(strTech)

        saveFileStatFid.close()
        os.rename(techFileName, os.path.join(self.simPath, self.simFolder, techFileName))

    def savePoliciesOnFile(self, tmpSeed):
        '''Function to save tech on file'''
        # Filenames
        FileName = 'policies_' + str(tmpSeed) + '.csv'
        # File handle
        saveFileFid = open(FileName, 'w')
        # File init
        strInit = '#ID\tFeedIn\tTaxCredit\tTaxCreditInv\tCarbonTax\tlength\tinitTime\tamountPerc\tResidue\tIntroTech\n'
        saveFileFid.write(strInit)
        for t in self.allPolicies:
            strInit = str(t.ID) + '\t' + str(t.feedIN) + '\t' + str(t.taxCredit) + '\t' + str(t.taxCreditInv) + '\t' + \
                      str(t.carbonTax) + '\t' + str(t.length) + '\t' + str(t.introTime) + '\t' + str(
                t.endTime) + '\t' + str(t.totalAmount) + '\t' + \
                      str(t.residue) + '\t' + str(t.introTech) + '\n'

            saveFileFid.write(strInit)

        saveFileFid.close()
        os.rename(FileName, os.path.join(self.simPath, self.simFolder, FileName))

    def statFunctions(self):

        tmp_tCO2 = 0
        tmp_totalDebt = 0
        tmp_totalCosts = 0
        tmp_totalRepayments = 0
        # For each agent
        for sngAgent in self.allAgents:
            tmp_tCO2 += sngAgent.co2
            tmp_totalDebt += sum(sngAgent.RemainingDebts)
            tmp_totalRepayments += sum(sngAgent.debtMonthRepayment)
            tmp_totalCosts += sngAgent.month_balance
        tmp_totalCosts -= tmp_totalRepayments

        # For each technology, is it is solar based the diffusion of the technology is registeres
        temp_current_diffusion = 0
        temp_kWh = 0
        temp_kW = 0
        for sT in self.allTechs:
            if sT.solarBased == 1:
                temp_current_diffusion += sT.currentDiffusion
                temp_kWh += sT.currentKWhinstalled
                temp_kW += sT.currentKWinstalled
        self.totSolarBasedInstallation.append(temp_current_diffusion)
        self.totSolarBasedKWh.append(temp_kWh)
        self.totSolarBasedKW.append(temp_kW)

        # STAT VARIABLES
        self.totCO2.append(tmp_tCO2)
        self.totDebt.append(tmp_totalDebt)
        self.totCosts.append(tmp_totalCosts)

    def saveOnFile(self, tmpSeed):
        # Store simulation data on file
        tmpStat = [self.totCO2, self.totDebt, self.totCosts, self.totAids]
        filename = 'stat_co2DebtCostsAids' + str(tmpSeed)
        self.writeSngStatOnFileWhereISay(filename, tmpStat, '%i')

        # Create list with all the technologies stats
        for t in self.allTechs:
            self.totTechNRGdist.append(t.techNRGdist)
            self.totTechKWHdist.append(t.techKWHdist)
            self.totTechKWdist.append(t.techKWdist)

        # Save overall stat on file
        filename = 'stat_nrgDist' + str(tmpSeed)
        self.writeSngStatOnFileWhereISay(filename, self.totTechNRGdist, '%d')
        filename = 'stat_kwhDist' + str(tmpSeed)
        self.writeSngStatOnFileWhereISay(filename, self.totTechKWHdist, '%f.2')
        filename = 'stat_kwDist' + str(tmpSeed)
        self.writeSngStatOnFileWhereISay(filename, self.totTechKWdist, '%f.2')

    def saveTotalOnFile(self):
        filename = '_overall_CO2'
        self.writeSngStatOnFileWhereISay(filename, self.tottotCO2, '%i')
        filename = '_overall_debt'
        self.writeSngStatOnFileWhereISay(filename, self.tottotDebt, '%i')
        filename = '_overall_costs'
        self.writeSngStatOnFileWhereISay(filename, self.tottotCosts, '%i')
        filename = '_overall_aids'
        self.writeSngStatOnFileWhereISay(filename, self.tottotAids, '%i')

        for tID, _ in enumerate(self.allTechs):
            tempTechList = [s[tID] for s in self.tottotTechNRGdist]
            # save technology
            filename = '_overall_tech_' + str(tID)
            self.writeSngStatOnFileWhereISay(filename, tempTechList, '%i')

    def writeSngStatOnFileWhereISay(self, tmpName, tmpStats, tmpFormat):
        '''
            Function to save statistic on file
        '''
        outFnameStat = tmpName + '.csv'
        saveFileStat = open(outFnameStat, 'w')
        cnt = 0
        for i in range(len(tmpStats[0])):
            strTypes = ''
            for j in range(len(tmpStats)):
                strTypes += str(tmpStats[j][i]) + '\t'
            strTypes += '\n'
            saveFileStat.write(strTypes)
            cnt += 1
        saveFileStat.close()
        os.rename(outFnameStat, os.path.join(self.simPath, self.simFolder, outFnameStat))

    def saveNet(self, tmpName):
        '''
            Save biomarket network
        '''
        outFnameStat = tmpName + '.csv'
        saveFileStat = open(outFnameStat, 'w')
        for sngAgent in self.allAgents:
            if len(sngAgent.client) > 0:
                for cl in sngAgent.client:
                    strTypes = str(sngAgent.ID) + '\t' + str(cl[0]) + '\t' + str(cl[1]) + '\n'
                    saveFileStat.write(strTypes)

        saveFileStat.close()
        os.rename(outFnameStat, os.path.join(self.simPath, self.simFolder, outFnameStat))

    def saveNoActiveAgent(self, tmpName):
        '''
            Agents not participating to the bio market
        '''
        outFnameStat = tmpName + '.csv'
        saveFileStat = open(outFnameStat, 'w')
        for sngAgent in self.allAgents:
            if len(sngAgent.client) == 0:
                if len(sngAgent.suppliers) == 0:
                    strTypes = str(sngAgent.ID) + '\n'
                    saveFileStat.write(strTypes)

        saveFileStat.close()
        os.rename(outFnameStat, os.path.join(self.simPath, self.simFolder, outFnameStat))

    def computeTotEnergyNeed(self):
        '''
            Compute overall Financiable amount
        '''
        for sngAgent in self.allAgents:
            self.overallEnergyNeed += sngAgent.totEnergyNeed

    def checkTimeAndSetPolicy(self, tmpTime):
        for pol in self.allPolicies:
            if pol.introTime == tmpTime:
                self.allTechs[pol.introTech].policy = pol.ID
            elif pol.endTime == tmpTime:
                self.allTechs[pol.introTech].policy = 0

    def saveAgentsXMLformat(self):
        '''
            Function to save statistic on file
        '''
        outFnameStat = os.path.join(self.simPath, self.simFolder, 'structures.xml')
        xmlFile = open(outFnameStat, 'w')
        tempstr = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xmlFile.write(tempstr)
        tempstr = '<xml>\n'
        xmlFile.write(tempstr)

        # AGENTS
        tempstr = '<agents>\n'
        xmlFile.write(tempstr)
        for agent in self.allAgents:
            tempstr = '\t<agent ID=\"' + str(agent.ID) + '\">\n'
            tempstr += '\t\t<x>' + str(agent.x) + '</x>\n'
            tempstr += '\t\t<y>' + str(agent.y) + '</y>\n'
            tempstr += '\t\t<age>' + str(agent.age) + '</age>\n'
            tempstr += '\t\t<totEnergyNeed>' + str(agent.totEnergyNeed) + '</totEnergyNeed>\n'
            tempstr += '\t\t<ha>' + str(agent.ha) + '</ha>\n'
            tempstr += '\t\t<nrgTechsReceipt>\n'
            for receipt in agent.nrgTechsReceipt:
                tempstr += '\t\t\t<nrgTech>' + str(receipt) + '</nrgTech>\n'
            tempstr += '\t\t</nrgTechsReceipt>\n'
            tempstr += '\t\t<nrgPropReceipt>\n'
            for receipt in agent.nrgPropReceipt:
                tempstr += '\t\t\t<nrgProp>' + str(receipt) + '</nrgProp>\n'
            tempstr += '\t\t</nrgPropReceipt>\n'
            tempstr += '\t\t<nrgAges>\n'
            for tmpAge in agent.nrgTechAges:
                tempstr += '\t\t\t<nrgAge>' + str(tmpAge) + '</nrgAge>\n'
            tempstr += '\t\t</nrgAges>\n'
            tempstr += '\t\t<techPolicy>\n'
            for receipt in agent.techPolicy:
                tempstr += '\t\t\t<policy>\n'
                tempstr += '\t\t\t\t<IDpolicy>' + str(receipt[0]) + '</IDpolicy>\n'
                tempstr += '\t\t\t\t<policyLength>' + str(receipt[1]) + '</policyLength>\n'
                tempstr += '\t\t\t</policy>\n'
            tempstr += '\t\t</techPolicy>\n'
            tempstr += '\t\t<solar_potential>' + str(agent.solar_potential) + '</solar_potential>\n'
            tempstr += '\t\t<co2>' + str(agent.co2) + '</co2>\n'
            tempstr += '\t\t<social_lobby>' + str(agent.social_lobby) + '</social_lobby>\n'
            tempstr += '\t\t<int_capital>' + str(agent.int_capital) + '</int_capital>\n'
            tempstr += '\t\t<equityCost>' + str(agent.equityCost) + '</equityCost>\n'
            tempstr += '\t\t<balance>' + str(agent.balance) + '</balance>\n'
            tempstr += '\t\t<month_balance>' + str(agent.month_balance) + '</month_balance>\n'
            tempstr += '\t\t<invLength>' + str(agent.invLength) + '</invLength>\n'
            tempstr += '\t\t<health>' + str(agent.health) + '</health>\n'
            tempstr += '\t\t<debts>\n'
            for debt in agent.debts:
                tempstr += '\t\t\t<debt>' + str(debt) + '</debt>\n'
            tempstr += '\t\t</debts>\n'
            tempstr += '\t\t<RemainingDebts>\n'
            for debt in agent.RemainingDebts:
                tempstr += '\t\t\t<remDebt>' + str(debt) + '</remDebt>\n'
            tempstr += '\t\t</RemainingDebts>\n'
            tempstr += '\t\t<debtTime>\n'
            for debt in agent.debtTime:
                tempstr += '\t\t\t<debtTime>' + str(debt) + '</debtTime>\n'
            tempstr += '\t\t</debtTime>\n'
            tempstr += '\t\t<debtLength>\n'
            for debt in agent.debtLength:
                tempstr += '\t\t\t<debtLength>' + str(debt) + '</debtLength>\n'
            tempstr += '\t\t</debtLength>\n'
            tempstr += '\t\t<debtMonthRepayment>\n'
            for debt in agent.debtMonthRepayment:
                tempstr += '\t\t\t<debtMonth>' + str(debt) + '</debtMonth>\n'
            tempstr += '\t\t</debtMonthRepayment>\n'
            tempstr += '\t</agent>\n'
            xmlFile.write(tempstr)
        tempstr = '</agents>\n'
        xmlFile.write(tempstr)

        # TECHNOLOGIES
        tempstr = '<technologies>\n'
        for tech in self.allTechs:
            tempstr += '\t<technology ID=\"' + str(tech.ID) + '\">\n'
            tempstr += '\t\t<renewable>' + str(tech.renewable) + '</renewable>\n'
            tempstr += '\t\t<efficiency>' + str(tech.efficiency) + '</efficiency>\n'
            tempstr += '\t\t<startTime>' + str(tech.startTime) + '</startTime>\n'
            tempstr += '\t\t<plantDimension>' + str(tech.plantDimension) + '</plantDimension>\n'
            tempstr += '\t\t<fromTons2kWhmese>' + str(tech.fromTons2kWhmese) + '</fromTons2kWhmese>\n'
            tempstr += '\t\t<cost>' + str(tech.cost) + '</cost>\n'
            tempstr += '\t\t<transportCosts>' + str(tech.transportCosts) + '</transportCosts>\n'
            tempstr += '\t\t<plantCost>' + str(tech.plantCost) + '</plantCost>\n'
            tempstr += '\t\t<interestRate>' + str(tech.interestRate) + '</interestRate>\n'
            tempstr += '\t\t<loanLength>' + str(tech.loanLength) + '</loanLength>\n'
            tempstr += '\t\t<duration>' + str(tech.duration) + '</duration>\n'
            tempstr += '\t\t<co2>' + str(tech.co2) + '</co2>\n'
            tempstr += '\t\t<policy>' + str(tech.policy) + '</policy>\n'
            tempstr += '\t\t<solarBased>' + str(tech.solarBased) + '</solarBased>\n'
            tempstr += '\t\t<X>' + str(tech.X) + '</X>\n'
            tempstr += '\t\t<Y>' + str(tech.Y) + '</Y>\n'
            tempstr += '\t</technology>\n'
        tempstr += '</technologies>\n'
        xmlFile.write(tempstr)

        # POLICIES
        tempstr = '<policies>\n'
        for pol in self.allPolicies:
            tempstr += '\t<policy ID=\"' + str(pol.ID) + '\">\n'
            tempstr += '\t\t<feedIN>' + str(pol.feedIN) + '</feedIN>\n'
            tempstr += '\t\t<taxCredit>' + str(pol.taxCredit) + '</taxCredit>\n'
            tempstr += '\t\t<taxCreditInv>' + str(pol.taxCreditInv) + '</taxCreditInv>\n'
            tempstr += '\t\t<carbonTax>' + str(pol.carbonTax) + '</carbonTax>\n'
            tempstr += '\t\t<length>' + str(pol.length) + '</length>\n'
            tempstr += '\t\t<introTime>' + str(pol.introTime) + '</introTime>\n'
            tempstr += '\t\t<endTime>' + str(pol.endTime) + '</endTime>\n'
            tempstr += '\t\t<totalAmount>' + str(pol.totalAmount) + '</totalAmount>\n'
            tempstr += '\t\t<residue>' + str(pol.residue) + '</residue>\n'
            tempstr += '\t\t<introTech>' + str(pol.introTech) + '</introTech>\n'
            tempstr += '\t</policy>\n'
        tempstr += '</policies>\n'
        xmlFile.write(tempstr)

        tempstr = '</xml>'
        xmlFile.write(tempstr)
        xmlFile.close()

    def resetAll(self):
        '''
            Reset all variables but of the initial system conditions
        '''

        del self.totSolarBasedInstallation[:]
        del self.totSolarBasedKWh[:]
        del self.totSolarBasedKW[:]

        del self.totCO2[:]
        del self.totDebt[:]
        del self.totCosts[:]
        del self.totAids[:]

        del self.totTechNRGdist[:]
        del self.totTechKWHdist[:]
        del self.totTechKWdist[:]

        del self.tottotTechNRGdist[:]
        del self.tottotTechKWHdist[:]
        del self.tottotTechKWdist[:]

        map(lambda x: x.resetAgentToInit(), self.allAgents)  # Reset agents
        map(lambda x: x.resetTechToInit(), self.allTechs)  # reset Techs
