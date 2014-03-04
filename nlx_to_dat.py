# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 14:16:19 2014

@author: palmiteradmin
"""

import nlxio
import sys
import numpy

"""
This program should be run in the directory you want to produce the .dat file in
Syntax: nlx_to_dat name numChan
e.g. nlx_to_dat 120220A 16
"""

filename = sys.argv[1]
numChan = int(sys.argv[2])

allcsc, nothing = nlxio.loadTetrodeNcs('CSC%C.ncs', numChan)
allcsc.tofile(filename + '.dat')