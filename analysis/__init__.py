# -*- coding: utf-8 -*-
"""
Created on Mon Jun 02 11:29:41 2014

@author: palmiteradmin
"""

import numpy as np

def downsample_spike_train(spike_timeseries, spike_time_indices, target_times):
    """ take a spike timeseries at a high sample rate (e.g. 10kHz), and outputs
        a spike timeseries at a lower sample rate (e.g. 100 Hz)
        """
    spike_timestamps = spike_time_indices[spike_timeseries > 0.5] # convert timeseries to timestamps
    bins = np.append(target_times, target_times[1] - target_times[0] + target_times[-1]) # create bins for histogram
    
    resampled_spike_timeseries, blank = np.histogram( spike_timestamps, bins = bins)
    
    return resampled_spike_timeseries