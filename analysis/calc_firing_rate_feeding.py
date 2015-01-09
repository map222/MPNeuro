# -*- coding: utf-8 -*-
"""
Created on Tue Dec 02 16:40:58 2014

@author: Michael Patterson, Palmiter Lab (map222@uw.edu)
"""

from __future__ import division
import numpy as np
import math
import pdb
    
def main(spike_times, feed_times):
    # spike_times is an N X spikes matrix of spike times
    # feeding_times is a 2 x N matrix of epochs when mouse was feeding (units of seconds)

    # create time points for beginning and end of non-feeding times
    max_time = int(max([max(z) for z in spike_times])) +1
    nonfeed_times = np.hstack(feed_times)
    nonfeed_times = np.insert(nonfeed_times, 0, 0) # I feel like this could be one line
    nonfeed_times = np.append(nonfeed_times, max_time).reshape((-1, 2))
    
    num_units = np.size(spike_times)
    avg_feed_rate = np.zeros(num_units)
    avg_nonfeed_rate = np.zeros(num_units)

#    pdb.set_trace()
    
    for i, cur_spikes in enumerate(spike_times):
        avg_feed_rate[i] = calc_avg_rate_epoch(cur_spikes, feed_times)
        avg_nonfeed_rate[i] = calc_avg_rate_epoch(cur_spikes, nonfeed_times)
           
    return avg_feed_rate, avg_nonfeed_rate

# calculate the average firing rate of point_process information in spike_times, between two timepoints in epoch_times
def calc_avg_rate_epoch(spike_times, epoch_times):
    total_spikes = 0
    total_time = 0
    
    for time_pairs in epoch_times:
        total_spikes += np.size( spike_times[(spike_times > time_pairs[0] ) & (spike_times < time_pairs[1] ) ])
        total_time   += time_pairs[1] - time_pairs[0]
    return total_spikes / total_time