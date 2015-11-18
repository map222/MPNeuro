# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 16:25:55 2014

@author: Michael Patterson, Palmiter lab (map222@uw.edu)

generates raster plot of spike times, aligning them to laser onset

"""

import pdb
import numpy as np
import quantities as pq

def raster_spike_laser(spike_times, laser_list, rast_start = -0.1, rast_end = 0.5, plot_flag = True):
    ''' Plot raster of spike times locked to a series of events
    
    Arguments:
    spike_times: 1 x N spikes SpikeTrain array
    laser_list: python float list of event times, units of seconds [is this np.array?]
    rast_start: time of raster start, in units of seconds
    rast_end: time of raster end, in units of seconds
    plot_flag: whether to plot the raster, or simply return the results
    '''
    
    #assert np.shape(spike_times)[0] == 1, 'spike_times must be a single SpikeTrain array, not a matrix'

    # aligned_spikes is a list of numpy arrays
    aligned_spikes = [np.array(0) for a in enumerate(laser_list)]
    for i, cur_event in enumerate(laser_list):
        
        # cut out spikes for current event, and align to zero
        aligned_spikes[i] = window_spike_times(spike_times[0], cur_event + rast_start, cur_event+rast_end) - cur_event * pq.s

    # pdb.set_trace()
    if plot_flag:
        import MPNeuro.plotting as MPplot
        reload(MPplot)
        MPplot.raster(aligned_spikes)
        
    return aligned_spikes
    
    
# helper function that cuts out a portion of time
            # timelist must be a np.array()
def window_spike_times(timelist, lowbound, upbound):
    return timelist[(timelist >lowbound) & (timelist < upbound)]