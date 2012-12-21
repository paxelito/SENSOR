'''Class tech definition.

.. module:: policy
   :platform: Unix, Windows
   :synopsis: The module containing the policy class, the class defining the different policies
   
.. moduleauthor:: Alessandro Filisetti <alessandro.filisetti@unibo.it>

'''
import os
import shutil as sh

class policy:
    def __init__(self, tmpID=0, tmpFeedIn=0, tmpTcred=0, tmpTcredInv=0, tmpCT=0, tmpL=0, tmpIntroTime=0, tmpA=0, tmpRes=0, tmpIntroTech=0):
        self.ID = tmpID
        self.feedIN = tmpFeedIn
        self.taxCredit = tmpTcred
        self.taxCreditInv = tmpTcredInv
        self.carbonTax = tmpCT
        self.length = tmpL # Length of the policy
        self.introTime = tmpIntroTime # month intro time
        self.totalAmount = tmpA # Percentage of theoretical total possbile amount
        self.residue = tmpRes # Remaining funds
        self.introTech = tmpIntroTech # Technology to be equipped with policy as soon as policy becames active
            
    def defineTotFinance(self, tmpTotEnergy, tmpConversion):
		self.residue = (tmpTotEnergy * self.feedIN * self.totalAmount) + (tmpTotEnergy / tmpConversion * self.taxCreditInv * self.totalAmount)
		
		
		