# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 18:56:44 2015

@author: matthewgrant
"""

import losses
import scipy.stats as sp
import numpy as np

myLoB = losses.LineOfBusiness(name = "Property", largeLoss = True)

x = myLoB.run()
print myLoB.name


