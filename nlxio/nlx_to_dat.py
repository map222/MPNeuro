# -*- coding: utf-8 -*-


"""
@author: Michael Patterson, Palmiter Lab (map222@uw.edu)

This script should be run in the directory you want to produce the .dat file in
Syntax: nlx_to_dat name numChan
e.g. nlx_to_dat 120220A 16
"""

import MPNeuro
import sys
import pdb

# load a neuralynx .nlx file and save as a binary .dat file (which can be read in Offline Sorter)
def load_nlx_save_dat(output_name, numChan):
    # output_name -- string for name of .dat file
    
    # load the neuralynx file
    allcsc = load_nlx(numChan)
    allcsc.tofile(output_name + '.dat')

# specific csc loading function
def load_nlx(numChan = 16):
    # numChan -- number of channels to be read
    #   if numChan is an integer, it reads channels 1-numChan
    #   if numChan is a range, it will read within the range

    # check type of numChan, and make range for loadTetrodeNcs
    if type(numChan) is int:
        channel_range = range(1, numChan+1)
    else:
        channel_range = range(numChan[0], numChan[1]+1)
    
    # load all of the tetrode data then save to .dat file
    allcsc, nothing = MPNeuro.nlxio.loadTetrodeNcs('CSC%C.ncs', channel_range, trim_zeros = False)
    return allcsc

# execution from BASH
if __name__ == "__main__":
    output_name = sys.argv[1]
    numChan = int(sys.argv[2])
    
    load_nlx_save_dat(output_name, numChan)