'''Class tech definition.

.. module:: policy
   :platform: Unix, Windows
   :synopsis: The module containing the policy class, the class defining the different policies
   
.. moduleauthor:: Alessandro Filisetti <alessandro.filisetti@unibo.it>

'''
import os
import shutil as sh

class policy:
	''' class policy definition
	'''
	
	def __init__(self, tmpID=0, tmpFeedIn=0, tmpTcred=0, tmpTcredInv=0, tmpCT=0, tmpL=0, tmpIntroTime=0):
		'''Constructor'''
		
		self.ID = tmpID
		self.feedIN = tmpFeedIn
		self.taxCredit = tmpTcred
		self.taxCreditInv = tmpTcredInv
		self.carbonTax = tmpCT
		self.length = tmpL
		self.introTime = tmpIntroTime
		
		