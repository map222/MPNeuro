# -*- coding: utf-8 -*-
"""
Created on Wed Dec 03 14:19:12 2014

@author: Michael Patterson, Palmiter Lab (map222@uw.edu)
"""

import MPNeuro.nlxio.helper_functions as hf
import MPNeuro.analysis.calc_firing_rate_feeding as cfrf
import numpy as np
import pdb
import matplotlib.pyplot as plt

def main(bool_plot = True):
    reload(hf)
# list of experiments to go through
    exp_list = ['140819B', '140813B', '140812B', '140729B', '140722A', '140718A', '140710A', '140708B']
    
    all_feed_rates = np.empty(0)
    all_nonfeed_rates = np.empty(0)
    
    for cur_exp in exp_list:
        #$pdb.set_trace()
        # load current experiment in list
        cur_data = hf.load_analyzed_exp(cur_exp)
        cur_spike_times = cur_data['spike_times']
        feed_times, water_times = hf.load_feed_times(cur_exp)
        
        # calculate average firing rate for experiment and add to list
        feed_avg, nonfeed_avg = cfrf.main(cur_spike_times, feed_times)
        all_feed_rates = np.append(all_feed_rates, feed_avg)
        all_nonfeed_rates = np.append(all_nonfeed_rates, nonfeed_avg)
    
    
    if bool_plot:
       plot_nonfeed_vs_feed(all_nonfeed_rates, all_feed_rates)
    return all_feed_rates, all_nonfeed_rates
    
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