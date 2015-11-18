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
#import MPNeuro.nlxio.helper_functions as hf

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
                
feeding_other_cells = [['150327A2', 0],
                       ['150731A', 4],
                       ['150814A', 3], # units 0 & 1 may be weakly phototagged
                       ['150902A', 2]] # unit 1 is weakly phototagged
CCK_other_cells = [['150330B', 4],
                   ['150803B2', 0],
                   ['150803B2', 2],
                   ['150803B2', 3],
                   ['150812C2', 2],
                   ['150812C2', 3],
                   ['150826B', 2],
                   ['150921B', 1],
                   ['150921B2', 0],
                   ['150921B2', 1]]
ensure_other_cells = [['150402A2', 0],
                      ['150827A', 0],
                      ['150923B', 2],
                      ['150923B', 3]]
                      
def calc_all_feeding_metrics( all_exp_dict):
    """ Calculate metrics for feeding, specifically
        Baseline firing rate for hungry vs fed
        Change in firing during bouts of feeding
        Change in firing rate from CCK
        
        Arguments:
        all_exp is a dictionary of experiments
        This can be found in the iPython notebook for these analyses in the python 2.7 folder
    """
                    
    hungry_rates, fed_rates = calc_hungry_vs_fed(all_exp_dict, feeding_cells, CCK_cells)
    pre_cck, post_cck, cck_pvalue = calc_cck_changes(all_exp_dict, CCK_cells)
    non_eat_rates, eat_rates = calc_feed_change_all(all_exp_dict, feeding_cells)
    non_ensure, ensure = calc_feed_change_all(all_exp_dict, ensure_cells)
    
    return hungry_rates, fed_rates, pre_cck, post_cck, cck_pvalue, non_eat_rates, eat_rates, non_ensure, ensure
    
def calc_other_feeding_metrics(all_exp_dict):
    """ Same as calc_all_feeding_metrics, except for non phototagged cells
    """
    
    hungry_rates, fed_rates = calc_hungry_vs_fed(all_exp_dict, feeding_other_cells, CCK_other_cells)
    pre_cck, post_cck, cck_pvalue = calc_cck_changes(all_exp_dict, CCK_other_cells)
    non_eat_rates, eat_rates = calc_feed_change_all(all_exp_dict, feeding_other_cells)
    non_ensure, ensure = calc_feed_change_all(all_exp_dict, ensure_other_cells)
    
    return hungry_rates, fed_rates, pre_cck, post_cck, cck_pvalue, non_eat_rates, eat_rates, non_ensure, ensure
    
def calc_hungry_vs_fed(all_exp_dict, hungry_cells, fed_cells):
    """ Calculate the firing rate for paired locations when mice are hungry vs fed. By "paired locations"
        I mean that I will only do a single comparison for each time the drive moves.
        
        hungry_cells: List of cells, of format [<string name of cell>, cell_id]
        fed_cells: List of cells, of same format as hungry cells
    """
        
    hungry_rates = [calc_fire_rate_wrap(all_exp_dict, x) for x in hungry_cells]
    fed_rates = [calc_fire_rate_wrap(all_exp_dict, x) for x in fed_cells]
    
    pre_rates = list(zip(*hungry_rates)[0])
    post_rates = list(zip(*fed_rates)[0])

    pvalue = []
    for i in range(len(hungry_rates)):
        pvalue.append( c_test( hungry_rates[i][0], fed_rates[i][0], hungry_rates[i][1], fed_rates[i][1] ) )
        
    return pre_rates, post_rates

def calc_fire_rate_wrap(all_exp_dict, cell_info, time_range = [0, 300]):
    """ Calculates the firing rate in a time_range for an experiment
        Cell_info is a tuple containing experiment name, and cell_id
        
        time_range: tuple of firing rate; defaults to first 5 minutes
        """
        
    cur_exp = all_exp_dict[cell_info[0]]
    cell_id = cell_info[1]
    return calc_fire_rate_epoch(cur_exp['spike_times'][cell_id], [time_range])
    
# calculate the average firing rate of point_process information in spike_times, between two timepoints in epoch_times
def calc_fire_rate_epoch(spike_times, epoch_times):
    total_spikes = 0
    total_time = 0

    for time_pairs in epoch_times:
        total_spikes += np.size( spike_times[(spike_times > time_pairs[0] ) & (spike_times < time_pairs[1] ) ])
        total_time   += time_pairs[1] - time_pairs[0]
    return [total_spikes / total_time, total_time]

def calc_cck_changes(all_exp_dict, cck_cells):
    """ Calculate pre-CCK firing vs late cck firing """
    
    pre_cck = [calc_fire_rate_wrap(all_exp_dict, x, [120, 540]) for x in cck_cells] # from 2-7 min.
    post_cck = [calc_fire_rate_wrap(all_exp_dict, x, [720, 1040]) for x in cck_cells] # from 14-19 min
    
    pre_rates = list(zip(*pre_cck)[0])
    post_rates = list(zip(*post_cck)[0])

    pvalue = []
    for i in range(len(pre_cck)):
        pvalue.append( c_test( pre_cck[i][0], post_cck[i][0], pre_cck[i][1], post_cck[i][1] ) )
    
    return pre_rates, post_rates, pvalue

def calc_feed_change_all(all_exp_dict, feeding_cells):
    """ Calculate the feeding changes for all experiments """
    return zip(*[calc_feed_changes_wrapper(all_exp_dict, x) for x in feeding_cells] )

import MPNeuro.nlxio.csv_parsing as cp
def calc_feed_changes_wrapper(all_exp_dict, cell_info):
    reload(cp)
    cur_exp = all_exp_dict[cell_info[0]]
    cell_id = cell_info[1]
    
    feed_times, water_times, bed_times = cp.parse_feedtimes_csv( cell_info[0] + ' feeding')
    avg_nonfeed_rate, avg_feed_rate =  calc_feed_changes(cur_exp['spike_times'][cell_id], feed_times, [600, 3600])  
    return avg_nonfeed_rate[0], avg_feed_rate[0]

def calc_feed_changes(spike_times, feed_times, time_range ):
    """ spike_times is one neuron's spike times
        feeding_times is a N X 2 matrix of epochs when mouse was feeding (units of seconds)
        time_range is a pair of [start, stop] times in seconds (to avoid pre-food when they eat bedding, and after food during unit identification)
        """

    assert feed_times.shape[1] == 2, 'feed_times must be an N x 2 matrix of times in seconds'

    # create time points for beginning and end of non-feeding times
    nonfeed_times = np.hstack(feed_times)
    nonfeed_times = np.insert(nonfeed_times, 0, time_range[0]) # I feel like this could be one line
    nonfeed_times = np.append(nonfeed_times, time_range[1]).reshape((-1, 2))

    avg_feed_rate = calc_fire_rate_epoch(spike_times, feed_times)
    avg_nonfeed_rate = calc_fire_rate_epoch(spike_times, nonfeed_times)
           
    return avg_nonfeed_rate, avg_feed_rate
    
def c_test(mu1, mu2, n1, n2):
    """ Poisson conditional test: test whether mean firing rate is different
    
    Arguments: spikes1 and spikes2 are lists of binned spikes
    """
    if mu1 ==0:
        mu1 = 0.001
    if mu2 ==0:
        mu2 = 0.001
    
    return ( n1 / n2) * (mu1 / mu2) / (1 + (n1 / n2) * (mu1 / mu2))