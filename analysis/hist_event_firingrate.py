# -*- coding: utf-8 -*-
"""
Created on Mon Jun 02 10:41:08 2014

@author: palmiteradmin
plots a histogram of firing rate before and after event

usage: hist_event_firigrate(spike_times, event_list)
    spike_times is a U x N np.array of spike_times (N) for U neurons (units of seconds)
    event_list is np.array of event times (e.g. light pulse) (units of seconds)
"""

import pdb
import numpy as np
import quantities as pq

def hist_event_firingrate(spike_times, event_list, plot_flag= True, labels = ' '):
    ''' Calculate the PSTH for each event, then display it if desired
    
    Arguments:
    spike_times: N x X array of N SpikeTrains, in units of seconds
    event_list: np.array of M events, here laser pulses, in units of seconds
    plot_flag: whether to plot the histogram
    labels: labels for neurons that can be passed to the plotting function
    
    Returns (in order):
    all_hist_means: a histogram of mean spikes / trial near the event
    all_hist_sd: standard deviation spikes / trial near an event; currently not used
    '''
    
    # parameters for histogram bins
    binwidth = 0.002
    t_start = -0.2
    t_end = 0.4
    bins = np.arange(t_start, t_end+binwidth, binwidth) # bins used for histogram
    
    num_units = np.shape(spike_times)[0] 
    
    all_hist_means = np.zeros([num_units, np.size(bins)-1])
    
    for j, cur_spikes in enumerate(spike_times): # loop through each unit in the spike_times
        cur_hist = np.zeros([np.size(event_list), np.size(bins)-1])
        for i, cur_event in enumerate(event_list):
            
            # cut out spikes for current event, and align to zero
            pre_window = 0.5
            post_window = 0.7
            temp_spikes = window_spike_times(cur_spikes, cur_event -pre_window, cur_event+post_window)
            temp_spikes -= cur_event * pq.s
            cur_hist[i,:] = np.histogram(temp_spikes, bins)[0] # create hist for each pulse
        
        all_hist_means[j, :] = np.mean(cur_hist, axis = 0) # take mean response
        #all_hist_sd[j, :] = stats.sem(cur_hist, axis=0)

    if plot_flag:
        import MPNeuro.plotting as MPplot
        reload(MPplot)
        MPplot.plot_hist_firingrate(bins, all_hist_means, labels)
        
    return all_hist_means
            
# helper function that cuts out a portion of time
            # timelist must be a np.array()
def window_spike_times(timelist, lowbound, upbound):
    return timelist[(timelist >lowbound) & (timelist < upbound)]