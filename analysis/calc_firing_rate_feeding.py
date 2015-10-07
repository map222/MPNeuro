# -*- coding: utf-8 -*-
"""
Created on Tue Dec 02 16:40:58 2014
Major modification 10-7-15

@author: Michael Patterson, Palmiter Lab (map222@uw.edu)

Contains functions that calculate average firing rate for experiments involving feeding (CCK,
ensure, and hungry chow eating)
"""

from __future__ import division
import numpy as np
import pdb
import matplotlib.pyplot as plt
    
def calc_all_feeding_metrics( all_exp_dict):
    """ Calculate metrics for feeding, specifically
        Baseline firing rate for hungry vs fed
        Change in firing during bouts of feeding
        Change in firing rate from CCK
        
        Arguments:
        all_exp is a dictionary of experiments
    """
    # list of experiments to go through
    CCK_cells = [['150330B', 3],
                 ['150713B', 2],
                 ['150803B', 0],
                 ['150812C', 0],
                 ['150826B', 2],
                 ['150921B', 0]]
    feeding_cells = [['150327A', 1],
                     ['150731A', 0],
                     ['150814A', 2],
                     ['150902A', 3],
                     ['150902A', 4]]
    ensure_cells = [['150402A', 2],
                    ['150819A', 0],
                    ['150819A', 1],
                    #150819Y
                    ['150827A', 2],
                    ['150923B', 1]]
                    
    hungry_fed_rates = calc_hungry_vs_fed(all_exp_dict, feeding_cells, CCK_cells)
    cck_change = calc_cck_changes(all_exp_dict, CCK_cells)
    
    return hungry_fed_rates
    
def calc_hungry_vs_fed(all_exp_dict, hungry_cells, fed_cells):
    """ Calculate the firing rate for paired locations when mice are hungry vs fed. By "paired locations"
        I mean that I will only do a single comparison for each time the drive moves.
        
        hungry_cells: List of cells, of format [<string name of cell>, cell_id]
        fed_cells: List of cells, of same format as hungry cells
    """
        
    hungry_rates = [calc_pre_exp_rate(all_exp_dict, x) for x in hungry_cells]
    fed_rates = [calc_pre_exp_rate(all_exp_dict, x) for x in fed_cells]
    
    return zip(hungry_rates, fed_rates)

def calc_pre_exp_rate(all_exp_dict, cell_info):
    """ Calculates the firing rate during first five minutes of an experiment
        Cell_info is a tuple containing experiment name, and cell_id """
        
    cur_exp = all_exp_dict[cell_info[0]]
    cell_id = cell_info[1]
    return calc_avg_rate_epoch(cur_exp['spike_times'][cell_id], [[0, 300]])
    
# calculate the average firing rate of point_process information in spike_times, between two timepoints in epoch_times
def calc_avg_rate_epoch(spike_times, epoch_times):
    total_spikes = 0
    total_time = 0
    
    for time_pairs in epoch_times:
        total_spikes += np.size( spike_times[(spike_times > time_pairs[0] ) & (spike_times < time_pairs[1] ) ])
        total_time   += time_pairs[1] - time_pairs[0]
    return total_spikes / total_time
    
def calc_cck_changes(all_exp_dict, cck_cells):
    """ Calculate pre-CCK firing vs late cck firing """
    
    pre_cck = [calc_pre_exp_rate(all_exp_dict, x) for x in cck_cells]
    post_cck = []
    
def plot_nonfeed_vs_feed(all_nonfeed_rates, all_feed_rates):
    fig = plt.figure(figsize = [7, 6])
    ax = fig.add_subplot(1,1,1)
    max_Hz = max(all_nonfeed_rates.max(), all_feed_rates.max() ) + 5
    x_range = np.arange(0, max_Hz)
    y_low = x_range * 0.9
    y_high = x_range * 1.1

    # plot unity axis and data    
    ax.fill_between(x_range, y_low, y_high, color = '0.8')
    ax.scatter(all_nonfeed_rates, all_feed_rates)
    
    # remove box
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    
    # increase axis label size
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(14)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(14)
    
    plt.xlim(0, max_Hz)
    plt.ylim(0, max_Hz)
    
    # labels
    plt.xlabel('Resting firing rate (Hz)', fontsize = 18)
    plt.ylabel('Feeding firing rate (Hz)', fontsize = 18)
    
def main(spike_times, feed_times, time_range ):
    """ spike_times is an N X spikes matrix of spike times
        feeding_times is a N X 2 matrix of epochs when mouse was feeding (units of seconds)
        time_range is a pair of [start, stop] times in seconds (to avoid pre-food when they eat bedding, and after food during unit identification)
        """

    assert feed_times.shape[1] == 2, 'feed_times must be an N x 2 matrix of times in seconds'

    # create time points for beginning and end of non-feeding times
    nonfeed_times = np.hstack(feed_times)
    nonfeed_times = np.insert(nonfeed_times, 0, time_range[0]) # I feel like this could be one line
    nonfeed_times = np.append(nonfeed_times, time_range[1]).reshape((-1, 2))
        
    # calculate firing rate by applying calc_avg_rate_epoch to each unit in spike_times
    # once for feeding times, and once for nonfeed_times
    # by mapping, you avoid problems for single spike_times
    avg_feed_rate = map(lambda x: calc_avg_rate_epoch(x, feed_times), spike_times)
    avg_nonfeed_rate = map(lambda x: calc_avg_rate_epoch(x, nonfeed_times), spike_times)
           
    return avg_feed_rate, avg_nonfeed_rate
