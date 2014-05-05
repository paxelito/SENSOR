SENSOR (Socioeconomic ENergy System simulatOR)

Plaftorms: MacOS, Linux, Windows
Language: Python

*****************
* RELEASE NOTES *
*****************

2014 - 05 - 05 ver.1.2
	- Source cose has been arranged in folder (a code library has been created) 

2014 - 04 - 16 ver.1.1
	- The technology awareness behavior has been added
	- The acceptance of the financial investment has been implemented
	- Several bugs fixed

2014 - 02 - 19 ver.1.0
- The introduction time is now considered for each technology

*****************




Libraries:
	lib folder:
		SIMULATION: Built-in python libraries
		ANALYSIS (a_* files in lib.analysis folder): numpy-scipy python scientific libraries.  
	
'modelDataDemo' FOLDER:
 |- INPUT 
 	|- init.conf		Configuration file
 	|- initAgents.csv 	Initial agent file (if agentCreationMethod=0 random)
 	|- initPolicies.csv Initial policies file (if policyCreationMethod=0 random)
 		|- .ID = Policy ID
        |- .feedIN = Feed-In tariff (Û/kWh produced)
        |- .taxCredit = Tax Credit Incentive (affect WACC computation)
        |- .taxCreditInv = Credit Incentive (percentage of plant investment)
        |- .carbonTax = Carbon Tax (Û/GHG)
        |- .length = Length of the policy, after this time policy becames no longer availabe  
        |- .introTime = Time (months) of the introduction of the policy
        |- .totalAmount = Percentage of the theoretical overall possibile incentives
        |- .residue = Remaining funds
        |- .introTech = Technology to be equipped with policy as soon as the policy becames active
 	|- initTechs.csv 	Initial technologies file (if techCreationMethod=0 random)
 	
 |- OUTPUT
 	|- 