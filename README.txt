SENSOR (Socioeconomic ENergy System simulatOR)

Plaftorms: MacOS, Linux, Windows
Language: Python
Libraries:
	SIMULATION: Built-in python libraries
	ANALYSIS (a_* files): numpy-scipy python scientific libraries.  
	
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


2014 - 02 - 19 ver.1.0
- The introduction time is now considered for each technology