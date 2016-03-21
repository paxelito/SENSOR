#!/usr/bin/env python
"""@package SENSOR
   \mainpage SENSOR
   \author Alessandro Filisetti
     
	More details.
	Fitting http://davidakenny.net/cm/fit.htm
"""

import sys, os
from time import time
import numpy as np
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

    _TIMEPROMPT_ = 12

    print "\n* * * * * * * * * * * * * * * * * * * * * * * * * *"
    print "\tWELCOME, SIMULATION IS GOING TO START..."
    print "* * * * * * * * * * * * * * * * * * * * * * * * * * * \n"

    # DATI SOLARE PERIODO 2000 - 2012 (MEGAWATT)
    ERmw = [0, 0, 0, 0, 0, 0, 0, 0, 39.8, 95, 364, 1267, 1610]  # EMILIA ROMAGNA
    PUmw = [0, 0, 0, 0, 0, 0, 0, 0, 53.3, 214.4, 683.4, 2186.2, 2449]  # PUGLIA
    LOmw = [0, 0, 0, 0, 0, 0, 0, 0, 49.8, 126.3, 372, 1321.6, 1822]  # LOMBARDIA
    CAmw = [0, 0, 0, 0, 0, 0, 0, 0, 15.5, 31.7, 84.4, 376, 546]  # CALABRIA
    # COMPUTE TOTAL MAX
    totmaxmw = max(max(ERmw), max(PUmw), max(LOmw), max(CAmw))
    # DATI NORMALIZZATI DA 0 a 1
    ERNmw = [float(x) / totmaxmw for x in ERmw]
    PUNmw = [float(x) / totmaxmw for x in PUmw]
    LONmw = [float(x) / totmaxmw for x in LOmw]
    CANmw = [float(x) / totmaxmw for x in CAmw]

    # DATI SOLARE PERIODO 2000 - 2012 (IMPIANTI)
    ERi = [0, 0, 0, 0, 0, 0, 0, 0, 3420, 6657, 14486, 31010, 44940]  # EMILIA ROMAGNA
    PUi = [0, 0, 0, 0, 0, 0, 0, 0, 2496, 5290, 9679, 22926, 33562]  # PUGLIA
    LOi = [0, 0, 0, 0, 0, 0, 0, 0, 5148, 10814, 23274, 48692, 68434]  # LOMBARDIA
    CAi = [0, 0, 0, 0, 0, 0, 0, 0, 627, 1710, 4006, 10071, 16571]  # LOMBARDIA
    # COMPUTE TOTAL MAX
    totmaxi = max(max(ERi), max(PUi), max(LOi), max(CAi))

    # DATI NORMALIZZATI DA 0 a 1
    ERNi = [float(x) / totmaxi for x in ERi]
    PUNi = [float(x) / totmaxi for x in PUi]
    LONi = [float(x) / totmaxi for x in LOi]
    CANi = [float(x) / totmaxi for x in CAi]

    # Initialization of alpha and beta vectors
    alphalist = np.arange(0.5, 10.5, 0.5)
    betalist = np.arange(0.5, 10.5, 0.5)

    # Initialize environment
    envi = en.environment(StrPath)
    # Create folder simulation and store initial conditions
    envi.createFolderAndSaveInitialConditions()
    envi.printParams()

    # Create population
    envi.createPopulation()
    envi.createTechnologies()
    envi.createPolicies(None, None, None)

    # create numpy arrays for results
    mdim = len(alphalist)
    ERmwmatrix = np.zeros([mdim, mdim], dtype=float)
    ERplantmatrix = np.zeros([mdim, mdim], dtype=float)
    PUmwmatrix = np.zeros([mdim, mdim], dtype=float)
    PUplantmatrix = np.zeros([mdim, mdim], dtype=float)
    LOmwmatrix = np.zeros([mdim, mdim], dtype=float)
    LOplantmatrix = np.zeros([mdim, mdim], dtype=float)
    CAmwmatrix = np.zeros([mdim, mdim], dtype=float)
    CAplantmatrix = np.zeros([mdim, mdim], dtype=float)

    # For each ALPHA and BETA of the BETA function
    for alphaid, temp_alpha in enumerate(alphalist):
        for betaid, temp_beta in enumerate(betalist):

            singleMWvector = []  # Vector containing the different megavat installed with this alpha and beta
            singleIvactor = []  # Vector containing the different plants installed with this alpha and beta

            yMW, allyMW = [], []
            yP, allyP = [], []
            for nseed in range(envi.nSeed):
                print "\t|- alpha: {0} - beta: {1} - Run number {2} ".format(temp_alpha, temp_beta, nseed)

                # Update commitments and social lobby values
                print "\t\t|- Update agents committment"
                map(lambda x: x.set_new_socialobby_and_committiment(np.random.beta(temp_alpha, temp_beta)),
                    envi.allAgents)

                # set MW array and PLANTS array
                del yMW[:]
                del yP[:]
                for gen in range(1, envi.months + 1):

                    if gen == 1:
                        del envi.allTechs[:]
                        del envi.allPolicies[:]
                        envi.createTechnologies()
                        envi.createPolicies(None, None, None)

                    if gen % _TIMEPROMPT_ == 0: print "\t\t|- Month ", gen,

                    # Standard month activities and New Technology evaluation
                    envi.agentMonthNRGAct_and_newTechAss(gen)
                    envi.checkTimeAndSetPolicy(gen)

                    if gen % _TIMEPROMPT_ == 0:
                        if len(envi.totSolarBasedInstallation) > 0:
                            print " - number of agents adopting a solar based tech: {0} - Total kWh: {1} - Total kW: {2}".format(
                                envi.totSolarBasedInstallation[-1], \
                                envi.totSolarBasedKWh[-1], \
                                envi.totSolarBasedKW[-1])
                        # for sTech in envi.allTechs:
                        #	print "\t\t\t|- Tech: {0}, Solar Based: {1}, Total Amount: {2}".format(sTech.ID, sTech.solarBased, sum(sTech.techKWHdist))

                    # Sto annual values
                    if (gen % 12 == 0) or (gen == 1):
                        yMW.append(envi.totSolarBasedInstallation[-1])
                        yP.append(envi.totSolarBasedKW[-1])

                # normalization of arrays
                if max(yMW) > 0:
                    yMWn = [float(x) / max(yMW) for x in yMW]
                else:
                    yMWn = [0 for x in yMW]
                if max(yP) > 0:
                    yPn = [float(x) / max(yP) for x in yP]
                else:
                    yPn = [0 for x in yP]

                allyMW.append(yMWn[:])
                allyP.append(yPn[:])

                envi.resetAll()

            # Compute average behavior
            alluMW_mean = map(np.mean, [[allyMW[j][i] for j in range(len(allyMW))] for i in range(len(allyMW[0]))])
            allallyP_mean = map(np.mean, [[allyP[j][i] for j in range(len(allyP))] for i in range(len(allyP[0]))])

            ERmwmatrix[alphaid][betaid] = st.curveFitting(alluMW_mean, ERNmw)
            ERplantmatrix[alphaid][betaid] = st.curveFitting(allallyP_mean, ERNi)

            PUmwmatrix[alphaid][betaid] = st.curveFitting(alluMW_mean, PUNmw)
            PUplantmatrix[alphaid][betaid] = st.curveFitting(allallyP_mean, PUNi)

            LOmwmatrix[alphaid][betaid] = st.curveFitting(alluMW_mean, LONmw)
            LOplantmatrix[alphaid][betaid] = st.curveFitting(allallyP_mean, LONi)

            CAmwmatrix[alphaid][betaid] = st.curveFitting(alluMW_mean, CANmw)
            CAplantmatrix[alphaid][betaid] = st.curveFitting(allallyP_mean, CANi)

    # Save all on file
    np.savetxt(os.path.join(StrPath, envi.simFolder, 'ERmwmatrix.csv'), ERmwmatrix, fmt='%.4f')
    np.savetxt(os.path.join(StrPath, envi.simFolder, 'ERplantmatrix.csv'), ERplantmatrix, fmt='%.4f')
    np.savetxt(os.path.join(StrPath, envi.simFolder, 'PUmwmatrix.csv'), PUmwmatrix, fmt='%.4f')
    np.savetxt(os.path.join(StrPath, envi.simFolder, 'PUplantmatrix.csv'), PUplantmatrix, fmt='%.4f')
    np.savetxt(os.path.join(StrPath, envi.simFolder, 'LOmwmatrix.csv'), LOmwmatrix, fmt='%.4f')
    np.savetxt(os.path.join(StrPath, envi.simFolder, 'LOplantmatrix.csv'), LOplantmatrix, fmt='%.4f')
    np.savetxt(os.path.join(StrPath, envi.simFolder, 'CAmwmatrix.csv'), CAmwmatrix, fmt='%.4f')
    np.savetxt(os.path.join(StrPath, envi.simFolder, 'CAplantmatrix.csv'), CAplantmatrix, fmt='%.4f')

    MIN_ERmwmatrix = np.where(ERmwmatrix == np.min(ERmwmatrix))
    MIN_ERplantmatrix = np.where(ERplantmatrix == np.min(ERplantmatrix))
    MIN_PUmwmatrix = np.where(PUmwmatrix == np.min(PUmwmatrix))
    MIN_PUplantmatrix = np.where(PUplantmatrix == np.min(PUplantmatrix))
    MIN_LOmwmatrix = np.where(LOmwmatrix == np.min(LOmwmatrix))
    MIN_LOplantmatrix = np.where(LOplantmatrix == np.min(LOplantmatrix))
    MIN_CAmwmatrix = np.where(CAmwmatrix == np.min(CAmwmatrix))
    MIN_CAplantmatrix = np.where(CAplantmatrix == np.min(CAplantmatrix))

    # Extract beta distribution params selected
    fidalphabetafid = open(os.path.join(StrPath, envi.simFolder, 'betaparams.csv'), 'w')
    fidalphabetafid.write('Region\ttype\talpha\tbeta\n')
    fidalphabetafid.write(
        ('Emilia Romagna\tMW\t{0}\t{1}\n').format(alphalist[MIN_ERmwmatrix[0]], betalist[MIN_ERmwmatrix[1]]))
    fidalphabetafid.write(
        ('Emilia Romagna\tPs\t{0}\t{1}\n').format(alphalist[MIN_ERplantmatrix[0]], betalist[MIN_ERplantmatrix[1]]))
    fidalphabetafid.write(('Puglia\tMW\t{0}\t{1}\n').format(alphalist[MIN_PUmwmatrix[0]], betalist[MIN_PUmwmatrix[1]]))
    fidalphabetafid.write(
        ('Puglia\tPs\t{0}\t{1}\n').format(alphalist[MIN_PUplantmatrix[0]], betalist[MIN_PUplantmatrix[1]]))
    fidalphabetafid.write(
        ('Lombardia\tMW\t{0}\t{1}\n').format(alphalist[MIN_LOmwmatrix[0]], betalist[MIN_LOmwmatrix[1]]))
    fidalphabetafid.write(
        ('Lombardia\tPs\t{0}\t{1}\n').format(alphalist[MIN_LOplantmatrix[0]], betalist[MIN_LOplantmatrix[1]]))
    fidalphabetafid.write(
        ('Campania\tMW\t{0}\t{1}\n').format(alphalist[MIN_CAmwmatrix[0]], betalist[MIN_CAmwmatrix[1]]))
    fidalphabetafid.write(
        ('Campania\tPs\t{0}\t{1}\n').format(alphalist[MIN_CAplantmatrix[0]], betalist[MIN_CAplantmatrix[1]]))

    fidalphabetafid.close()

    del envi
