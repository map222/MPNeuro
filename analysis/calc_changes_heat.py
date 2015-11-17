# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 11:11:45 2015

@author: Michael Patterson, Palmiter Lab (map222@uw.edu)

This is alarmingly similar to calc_firing_rate_feeding. Functions should probably be
generalized / abstracted more thoughtfully.

"""
import numpy as np
import pdb

def calc_all_fear_metrics( all_exp_dict):
    """ Calculate metrics for fear, specifically:
        Change in firing rate during hot-plate
        
        Arguments:
        all_exp_dict: dictionary of experiments, each of which has spike_times and laser_times
        This can be found in the iPython notebook for these analyses in the python 2.7 folder
    """
    
    heat_cells = [['150406A', 3],
                  ['150813A', 0],
                  ['150828A', 0],
                  ['150923A', 0]]
    
    pre_rate, heat_rate, post_rate, t_tests = calc_heat_response_all(all_exp_dict, heat_cells)
    return pre_rate, heat_rate, post_rate, t_tests
    
def calc_other_fear_metrics( all_exp_dict):
    heat_other_cells = [['150406A', 2],
                        ['150828A', 1],
                        ['150923A2', 0],
                        ['150923A2', 1]
                        # 150813A - other two are semi-identified                    
                    ]
                    
    pre_rate, heat_rate, post_rate, t_tests = calc_heat_response_all(all_exp_dict, heat_other_cells)
    return pre_rate, heat_rate, post_rate, t_tests
    
def calc_heat_response_all(all_exp_dict, heat_cells):
    return zip(*[calc_heat_wrap(all_exp_dict, x) for x in heat_cells] )

def calc_heat_wrap(all_exp_dict, cell_info, time_range = [0, 60]):
    """ extract the specific spike_times we are interested in
        then calculate time ranges we are interested in
        Finally, pass that info to the function that calculates the metrics
    """     
    cur_exp = all_exp_dict[cell_info[0]] # string name of experiment
    cell_id = cell_info[1]
    
    hot_times = parse_max_heat_time(cell_info[0])    
    
    return calc_heat_response(cur_exp['spike_times'][cell_id], hot_times)

import MPNeuro.nlxio.csv_parsing as cp
def parse_max_heat_time( exp_name):
    """ Returns three tuples, containing second 
    """
    heat_times, heat_temps = cp.parse_heattimes_csv(exp_name + ' heating')
    
    max_heat_time = heat_times[np.argmax(heat_temps)] # time in seconds of maximum heat
    return max_heat_time-30, max_heat_time+5

import MPNeuro.analysis.hist_event_firingrate as hef
from scipy import stats
def calc_heat_response(spike_times, hot_times):
    """ Calculate the average firing rate before heat, around peak heat, and after heat
        Also, calculate statistics of whether firing rate changed """
    
    pre_heat_times = [0, 30]
    post_times = [hot_times[1] + 60, hot_times[1] + 120]
    pre_heat_hist, _ = np.histogram(hef.window_spike_times(spike_times, pre_heat_times[0], pre_heat_times[1]),
                                    bins = np.arange(pre_heat_times[1]) )
    
    heat_hist, _ = np.histogram(hef.window_spike_times(spike_times, hot_times[0], hot_times[1]),
                                    bins = np.arange(hot_times[0], hot_times[1]) )
                                    
    post_heat_hist, _ = np.histogram(hef.window_spike_times(spike_times, hot_times[0]+60, hot_times[1]+120),
                                    bins = np.arange(hot_times[0]+60, hot_times[1]+120) )
    
    pre_rate = np.sum(pre_heat_hist) / pre_heat_times[1]
    heat_rate = np.sum(heat_hist) / (hot_times[1] - hot_times[0])
    post_rate = np.sum(heat_hist) / (post_times[1] - post_times[0])
    
    t_test = stats.ttest_ind(pre_heat_hist, heat_hist)
    
    return pre_rate, heat_rate, post_rate, t_test