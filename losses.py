# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 18:30:19 2015

@author: matthewgrant
@author: eddielongdon

Python style guide: https://google.github.io/styleguide/pyguide.html
"""

import numpy as np
import scipy.stats as sp

#@TODO:
# - was thinking of using sphinx for auto documentation from docstrings: 
#   http://sphinx-doc.org
# - make a loss return object that can return total, and each by type; you choose which
# - make inputs to loss type an argument


class PaymentPattern( object ):
    """
    Represents a payments pattern - this can be for e.g. premium, losses etc
    """
    def __init__(self, times = 1, amounts = 1):
        
        self.times = np.array([times]).flatten()
        self.amounts = np.array([amounts]).flatten()
        if np.sum(self.amounts) != 1:
            print "Error: amounts are fractions - must sum to 1"
        if len(self.times) != len(self.amounts):
            print "Error: different numbers of times and amounts."
        #merge and sort by time
        unsrt = np.transpose(np.vstack([times, amounts]))
        self.value = unsrt[unsrt[:,0].argsort()]
        self.times, self.amounts = self.value[:,0], self.value[:,1]
        
class LineOfBusiness( object ):
    """
    Represents a Line of Business with exposures and losses.
    
    The LineOfBusiness object represents a particular line of business which
    may be exposed to any combination of the following types of losses:
         - Catastrophe (Cat) Losses
         - Large Losses
         - Attritional Losses
    """
    
    def __init__(self, name = None, 
                 catLoss = False, 
                 attLoss = False, 
                 largeLoss = True,
                 premium = 100,
                 premiumPattern = np.array([[0.5, 1]])):
        
        self.name = name
        self.premium = premium
        self.premiumPattern = PaymentPattern(times = premiumPattern[:,0], 
                                             amounts = premiumPattern[:,1])
        
        self.lossTypes = { 'cat': catLoss, 'att': attLoss, 'large': largeLoss}
        
        # Get attribute errors later if these aren't initialised.
        self.catLoss = None
        self.attLoss = None
        self.largeLoss = None
        
        if catLoss:
            self.catLoss = Loss(lossType = "Cat")
        if attLoss:
            self.attLoss = Loss(lossType = "Att")
        if largeLoss:
            self.largeLoss = Loss(lossType = "Large")
    
    
    def run( self, nSims = 100):
        #want this to return an object with a total, and a breakdown
                
        catLosses = []
        attLosses = []
        largeLossesByTrial = []                     
        
        for i in range(nSims):
            
            # The use of the carriage return '\r' and the comma at the end of
            # the line are important as they will print things to the same line
            # in Terminal.
            # The comma at the end suppresses the newline.
            # The carriage return returns the cursor to the start of the line.
            # See: http://stackoverflow.com/questions/5419389/python-how-to-overwrite-the-previous-print-to-stdout
            print 'Sim: {0}/{1}\r'.format(i + 1, nSims),
            
            if self.lossTypes['cat']:
                #do cat loss thing
                catLosses.append( 
                    self.catLoss.sevDist.rvs(size=self.catLoss.freqDist.rvs() )
                )
            
            if self.lossTypes['att']:
            #attritional losses just come as a lump, not as f-s so just need
            #one number            
                attLosses.append(
                    self.attLoss.sevDist.rvs(1)
                )
            
            if self.lossTypes['large']:
                #do large loss thing
                """
                curSimLoss = self.largeLoss.sevDist.rvs(
                    size=self.largeLoss.freqDist.rvs()
                )
                
                largeLosses = np.append(largeLosses, curSimLoss)
                
                """
                #store the large losses grouped by trial - can then easily
                #convert into one array, but pull out more detailed trial info
                #if needed
                largeLossesByTrial.append(
                     self.largeLoss.sevDist.rvs(size=self.largeLoss.freqDist.rvs() ) 
                )                
        
        #collapse into one block of losses
        largeLosses = np.hstack(largeLossesByTrial)
        
        runResult = SimResult(self.catLoss, self.attLoss, self.largeLoss, catLosses, attLosses, largeLosses)
        
        
        
        print # Needed to advance to the next line after showing the sim status on the same line
        # See: http://stackoverflow.com/questions/5419389/python-how-to-overwrite-the-previous-print-to-stdout
        
        
        return runResult
    
    
class Loss( object ):
    """
    A loss object. Types are cat, large (default) or attritional. If large need 
    frequency and severity. If attritional just need severity. If cat need some
    sort of loss table?!
    
    Lognormal parameterisation is \mu, \sigma
    Gamma parameterisation is the k (shape, param 1), \theta (scale, param 2) 
    one found on wikipedia
    """
    def __init__(self, lossType = "Large", 
                 sevDist = ["lognorm", 0, 1],
                 freqDist = [ "poisson", 1 ]
                 ):
        self.sevDist = None
        self.freqDist = None
        
        if lossType == "Cat":
            #do the thing for cat losses
            self.sevDist = sp.lognorm(sevDist[2], scale = np.exp(sevDist[1]))
        elif lossType == "Att":
            self.sevDist = sp.lognorm(sevDist[2], scale = np.exp(sevDist[1]))
            self.freqDist = None
        elif lossType == "Large":
            if sevDist[0] == "lognorm" or sevDist[0] == "lognormal":
                self.sevDist = sp.lognorm(sevDist[2], scale = np.exp(sevDist[1]))
            elif sevDist[0] == "gamma":
                self.sevDist = sp.gamma(sevDist[1], scale = sevDist[2])
            self.freqDist = sp.poisson(freqDist[1])

class SimResult( object ):
    
    def __init__(self, catLoss, attLoss, largeLoss, catLosses, attLosses, largeLosses):
        self.catLoss = catLoss
        self.attLoss = attLoss
        self.largeLoss = largeLoss
        self.catLosses = catLosses
        self.attLosses = attLosses
        self.largeLosses = largeLosses
        
    def catInfo(self):
        print self.catLosses
    
    def attInfo(self):
        print self.attLosses
    
    def largeInfo(self):
        mean = np.mean(self.largeLosses)
        std = np.std(self.largeLosses)
        print "Sev Mean: {0}".format(mean)
        print "Expected Sev Mean: {0}".format(self.largeLoss.sevDist.mean())
        print "Sev Std Dev: {0}".format(std) 
        print "Expected Sev Std Dev: {0}".format(self.largeLoss.sevDist.std())
        

        
