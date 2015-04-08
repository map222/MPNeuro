# -*- coding: utf-8 -*-


"""
@author: Michael Patterson, Palmiter Lab (map222@uw.edu)


This script should be run in the directory you want to produce the .dat file in
Syntax: nlx_to_dat name numChan
e.g. nlx_to_dat 120220A 16
"""

import MPNeuro
import sys


def load_nlx_save_dat(output_name, numChan = 16):
    
    allcsc, nothing = MPNeuro.nlxio.loadTetrodeNcs('CSC%C.ncs', nCh = numChan, trim_zeros = False)
    allcsc.tofile(output_name + '.dat')

if __name__ == "__main__":
    output_name = sys.argv[1]
    numChan = int(sys.argv[2])
    
    load_nlx_save_dat(output_name, numChan)