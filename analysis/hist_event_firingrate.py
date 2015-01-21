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
import scipy.stats as stats

def hist_event_firingrate(spike_times, event_list, plot = True):
    

    binwidth = 0.002
    bins = np.arange(-0.2, 0.6+binwidth, binwidth) # bins used for histogram
    
    num_units = np.shape(spike_times)[0] 
    
    all_hist_means = np.zeros([num_units, np.size(bins)-1])
    all_hist_sd = np.zeros([num_units, np.size(bins)-1])
    
    for j, cur_spikes in enumerate(spike_times):
        cur_hist = np.zeros([np.size(event_list), np.size(bins)-1])
        for i, cur_event in enumerate(event_list):
            
            # cut out spikes for current event, and align to zero
            # pdb.set_trace()
            temp_spikes = window_spike_times(cur_spikes, cur_event -0.5, cur_event+0.7) - cur_event * pq.s
            cur_hist[i,:] = np.histogram(temp_spikes, bins)[0] # create hist for each pulse
        
        all_hist_means[j, :] = np.mean(cur_hist, axis = 0) # take mean response
        #all_hist_sd[j, :] = stats.sem(cur_hist, axis=0)
        
    if plot:
        import MPNeuro.plotting as MPplot
        reload(MPplot)
        MPplot.plot_hist_firingrate(bins, all_hist_means, all_hist_sd)
        
    return all_hist_means, all_hist_sd
            
# helper function that cuts out a portion of time
            # timelist must be a np.array()
def window_spike_times(timelist, lowbound, upbound):
    return timelist[(timelist >lowbound) & (timelist < upbound)]