# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 16:23:54 2014

@author: palmiteradmin
calculates the inter-spike interval for points process data
    -then plots it

usage: calc_ISI(spike_times)
    spiketimes is a U x N np.array of spiketimes (N) for U neurons (units of seconds)
"""

import numpy as np
import matplotlib.pyplot as plt
import pdb

def calc_ISI(spike_times):
    
    for i, row in enumerate(spike_times):
        diff_spike_times = np.diff(row)
        
        #pdb.set_trace()
        # create bins based on average firing rate
        firing_rate =diff_spike_times.mean()
        bin_max = firing_rate.magnitude * 4
        bin_width = firing_rate.magnitude / 5
        ISI_bins = np.arange(0, bin_max + bin_width, bin_width)
        
        # calculate the histrogram and plot it
        binned_ISI =np.empty([ len(spike_times), bin_max / bin_width ]) # bin_max must be divisible by bin_width
        
        plt.figure()
        binned_ISI[i,] = plt.hist(diff_spike_times, bins = ISI_bins)[0]
        