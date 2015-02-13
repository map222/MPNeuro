# -*- coding: utf-8 -*-
"""
Created on Tue Jun 03 15:19:53 2014

@author: palmiteradmin
"""


import numpy as np
import pdb
import matplotlib.pyplot as plt
import math

def plot_hist_firingrate(bins, firingrates, firing_sem = []):
    
    # setup
    bins2 = bins[:-1] + (bins[1]-bins[0])/2 # offset bins to center them
    fig = plt.figure(figsize = [12, 6])
    ax = fig.add_subplot(1,1,1)
    lw = 4 # linewidth
    colorj = ['g', 'b', 'k', 'r']
    
    rate_conversion = bins[1] - bins[0]
    
    # plot all the firing rates
    for i, rows in enumerate(firingrates):
        #rows = np.convolve(rows, [0.25, 0.5, 0.25], mode = 'same')    
        ax.errorbar(bins2, rows / rate_conversion, yerr = firing_sem[i,:] / rate_conversion,
            label = str(i), linewidth = math.ceil((i+4 )/ len(colorj)), color = colorj[i%len(colorj)])

    plt.legend(frameon = False)
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    

    plt.xlabel('Time (sec)', fontsize = 18)
    plt.ylabel('Firing Rate', fontsize = 18)
    plt.show()
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(14)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(14)
        
def raster(aligned_spikes): # copied from internet :)
    fig = plt.figure(figsize = [12, 6])
    ax = fig.add_subplot(1,1,1)
    for ith, trial in enumerate(aligned_spikes):
        ax.vlines(trial, ith + .5, ith + 1.5, color='black')
    plt.ylim(.5, len(aligned_spikes) + .5)
    
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    
    
    plt.xlabel('Time (sec)', fontsize = 18)
    plt.ylabel('Trial', fontsize = 18)
    return ax