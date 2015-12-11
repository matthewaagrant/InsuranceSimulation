# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 18:56:44 2015

@author: matthewgrant
"""

import losses
import scipy.stats as sp
import numpy as np

myLoB = losses.LineOfBusiness(name = "Property", largeLoss = True,
                              premiumPattern = np.array([[1.5, 0.25],[0.85, 0.75]]))

x = myLoB.run(1000)
x.largeInfo()




