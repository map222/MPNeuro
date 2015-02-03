# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 16:25:55 2014

@author: palmiteradmin

generates raster plot of spike times, aligning them to laser onset

usage: raster_spike_laser(spike_times, event_list)
    spike_times is a 1 x N np.array of spike_times (N) (units of seconds)
    event_list is np.array of event times (e.g. light pulse) (units of seconds)
"""

import pdb
import numpy as np
import quantities as pq
import scipy.stats as stats

def raster_spike_laser(spike_times, laser_list, plot = True):
    # spike_times is a single SpikeTrain array
    # laser_list is a simple float list
    rast_start = -1
    rast_end = 1

    # aligned_spikes is a list of numpy arrays
    aligned_spikes = [np.array(0) for a in enumerate(laser_list)]
    for i, cur_event in enumerate(laser_list):
        
        # cut out spikes for current event, and align to zero
        aligned_spikes[i] = window_spike_times(spike_times[0], cur_event + rast_start, cur_event+rast_end) - cur_event * pq.s

    # pdb.set_trace()
    if plot:
        import MPNeuro.plotting as MPplot
        reload(MPplot)
        MPplot.raster(aligned_spikes)
        
    return aligned_spikes
    
    
# helper function that cuts out a portion of time
            # timelist must be a np.array()
def window_spike_times(timelist, lowbound, upbound):
    return timelist[(timelist >lowbound) & (timelist < upbound)]