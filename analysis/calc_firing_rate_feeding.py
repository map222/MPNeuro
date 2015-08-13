# -*- coding: utf-8 -*-
"""
Created on Tue Dec 02 16:40:58 2014

@author: Michael Patterson, Palmiter Lab (map222@uw.edu)
"""

from __future__ import division
import numpy as np
import pdb
    
def main(spike_times, feed_times, time_range ):
    """ spike_times is an N X spikes matrix of spike times
        feeding_times is a 2 x N matrix of epochs when mouse was feeding (units of seconds)
        time_range is a pair of [start, stop] times in seconds (to avoid pre-food when they eat bedding, and after food during unit identification)
        """
        
    # create time points for beginning and end of non-feeding times
    nonfeed_times = np.hstack(feed_times)
    nonfeed_times = np.insert(nonfeed_times, 0, time_range[0]) # I feel like this could be one line
    nonfeed_times = np.append(nonfeed_times, time_range[1]).reshape((-1, 2))
    
    pdb.set_trace()
        
    # calculate firing rate by applying calc_avg_rate_epoch to each unit in spike_times
    # once for feeding times, and once for nonfeed_times
    # by mapping, you avoid problems for single spike_times
    avg_feed_rate = map(lambda x: calc_avg_rate_epoch(x, feed_times), spike_times)
    avg_nonfeed_rate = map(lambda x: calc_avg_rate_epoch(x, nonfeed_times), spike_times)
           
    return avg_feed_rate, avg_nonfeed_rate

# calculate the average firing rate of point_process information in spike_times, between two timepoints in epoch_times
def calc_avg_rate_epoch(spike_times, epoch_times):
    total_spikes = 0
    total_time = 0
    
    for time_pairs in epoch_times:
        total_spikes += np.size( spike_times[(spike_times > time_pairs[0] ) & (spike_times < time_pairs[1] ) ])
        total_time   += time_pairs[1] - time_pairs[0]
    return total_spikes / total_time