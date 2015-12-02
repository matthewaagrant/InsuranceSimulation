# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 18:30:19 2015

@author: matthewgrant
"""

import numpy as np
import scipy.stats as sp


#@TODO:
# - make a loss return object that can return total, and each by type; you choose which
# - make inputs to loss type an argument
# - adjust attritional loss type

class LineOfBusiness( object ):
    def __init__(self, name = None, 
                 catLoss = False, 
                 attLoss = False, 
                 largeLoss = True ):
        self.name = name
        self.lossTypes = { 'cat': catLoss, 'att': attLoss, 'large': largeLoss}
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
        largeLosses = []
        for i in range(nSims):
            if self.lossTypes['cat']:
                #do cat loss thing
                catLosses.append( self.catLoss.sevDist.rvs(size=self.catLoss.freqDist.rvs() )
                )
            if self.lossTypes['att']:
                #do att loss thing
                attLosses.append(
                self.attLoss.sevDist.rvs(size=self.attLoss.freqDist.rvs() )
                )
            if self.lossTypes['large']:
                #do large loss thing
                largeLosses.append( self.largeLoss.sevDist.rvs(size=self.largeLoss.freqDist.rvs() ) 
                )
        return largeLosses
    
    
class Loss( object ):
    def __init__(self, lossType = "Large", 
                 sevDist = ["lognorm", 0, 1],
                 freqDist = [ "poisson", 1 ]
                 ):
        if lossType == "Cat":
            #do the thing for cat losses
            self.sevDist = sp.lognorm(sevDist[2], scale = np.exp(sevDist[1]))
        elif lossType == "Att":
            self.sevDist = sp.lognorm(sevDist[2], scale = np.exp(sevDist[1]))
        elif lossType == "Large":
            self.sevDist = sp.lognorm(sevDist[2], scale = np.exp(sevDist[1]))
            self.freqDist = sp.poisson(freqDist[1])
                      