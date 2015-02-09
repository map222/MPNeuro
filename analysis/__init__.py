# -*- coding: utf-8 -*-
"""
Created on Mon Jun 02 11:29:41 2014

@author: palmiteradmin
"""

# placeholder

from __future__ import division
import MPNeuro.nlxio.helper_functions as hf
import pdb
import numpy as np
import matplotlib.pyplot as plt

class PhototagData:
    def __init__(self):
        # cell info in format of: name, cell_id, trial_start, trial_end
        self.cell_info = [['150202A', 3, 0, 149], # 0
                          ['150127C', 3, 0, 49],
                          ['150126C', 6, 0, 119],
                          ['150119B', 5, 120, 239],
                          ['150113B', 2, 120, 239],
                          ['150102A', 0, 0, 149], # 5
                          ['150121B', 2, 0, 119],
                          ['150203C', 0, 200, 399],
                          ['150204A', 0, 0, 199],
                          ['150205A', 0, 0, 199],
                          ['150205A', 6, 0, 199], # 10
                          ['150205A', 8, 0, 199],
                          ['150209A', 0, 0, 199]]
        self.spike_times = []
        self.laser_times = []
        
        
    # load the data from the .plx files; cell id info is declared in the __init__
    def load_data(self):
        for row in self.cell_info: # go through each cell
            cur_exp = hf.load_analyzed_exp(row[0])
            #pdb.set_trace()
            if np.size(cur_exp['spike_times']) >1:
                self.spike_times.append( cur_exp['spike_times'][row[1]] ) # get spike times for given cell
            else: # for single cell files, just append the single cell
                self.spike_times.append( cur_exp['spike_times'] )
            self.laser_times.append( cur_exp['laser_times'][row[2]:row[3]] ) # get laser times for range of trials
            
        # initialize some variables for calculation later
        self.num_cells = np.size(self.cell_info, 0)
        self.mean_pre_isi = np.zeros(self.num_cells)
        self.mean_first_spike = np.zeros(self.num_cells)
        self.std_first_spike = np.zeros(self.num_cells)
        self.first_firing_above_mean = np.zeros(self.num_cells)
        

def calc_phototag_metrics(phototag_data):
    """ phototagData is an MPNeuroData class with data already loaded in
        This function will calculate the metrics for determing whether a cell is phototagged"""
    binwidth = 0.002
    start_time = -1
    end_time = -1 * start_time# end_time should be symmetric with start_time
    bins = np.arange(start_time, end_time+binwidth, binwidth) # bins used for histogram
    
    for cur_index in range(phototag_data.num_cells): # go through each cell
        # get split spike times for before and after light
        cur_laser_times = phototag_data.laser_times[cur_index]      
        cur_spikes = [phototag_data.spike_times[cur_index]]
        pre_spikes, post_spikes = align_pre_post_spikes(cur_spikes, cur_laser_times, start_time, end_time)
        
        # calculate the expected first spike time based on average firing rate
        diffs = map(np.diff, pre_spikes)
        diffs2 = np.array([item for sublist in diffs for item in sublist]) # no idea what this does !
        phototag_data.mean_pre_isi[cur_index] = np.mean(diffs2) / 2
        
        # measure the actual first spike time (mean and std)
        mean_first_spike, std_first_spike = get_first_spike_metrics(post_spikes, phototag_data.laser_times[cur_index])
        phototag_data.mean_first_spike[cur_index] = mean_first_spike
        phototag_data.std_first_spike[cur_index] = std_first_spike
    
        phototag_data.first_firing_above_mean[cur_index] = calc_firing_over_threshold(cur_laser_times, pre_spikes, post_spikes, bins, binwidth)
        
    # create a mask for cells that meet all criteria    
    phototag_data.good_cell_mask = (phototag_data.first_firing_above_mean < 0.02) & (phototag_data.mean_first_spike < 0.02) & (phototag_data.std_first_spike < 0.01)
    return phototag_data
    

def calc_firing_over_threshold(cur_laser_times, pre_spikes, post_spikes, bins, binwidth):
    """ Calculate when the firing rate exceeds the mean firing rate + N standard deviations """
    num_bins = np.size(bins) -1
    pre_hist = np.nan * np.ones([np.size(cur_laser_times), num_bins])
    post_hist = np.nan * np.ones([np.size(cur_laser_times), num_bins])
    num_trials = np.size(cur_laser_times)
    
    # get all pre_spikes and post_spikes in one vector for easy histogram
    all_pre_spikes  = np.concatenate(pre_spikes) 
    all_post_spikes = np.concatenate(post_spikes)
    
    pre_hist  = np.histogram(all_pre_spikes,  bins)[0] / num_trials
    post_hist = np.histogram(all_post_spikes, bins)[0] / num_trials
    mean_pre_hist = max([np.mean(pre_hist[:(num_bins/2)], axis = 0), 3 * binwidth]) # set minimum threshold of 3 Hz
    std_pre_spikes = np.std(pre_hist)
    
    return np.min(np.where(post_hist[(num_bins/2):] > mean_pre_hist + std_pre_spikes*3) ) * binwidth


def align_pre_post_spikes(spiketrain, cur_laser_times, start_time, end_time):
    """ Align spike times to laser pulses
        return times before and after zero, within start_time and end_time """
    import MPNeuro.analysis.raster_spike_laser as rsl
    reload(rsl)
    
    # get aligned spikes; need to do weird [] around spike_times due to how rsl works
    aligned_spikes = rsl.raster_spike_laser(spiketrain, cur_laser_times, rast_start = -1, rast_end = 1, plot = False)
    
    # get the pre-light spikes, then calculate the mean ISI to get predicted first post-light spike time
    pre_spikes = map(lambda x: rsl.window_spike_times(x, start_time, 0), aligned_spikes)
    pre_spikes_np = map(np.array, pre_spikes)
    
    # get all spikes after light
    post_spikes = map(lambda x: rsl.window_spike_times(x, 0, end_time), aligned_spikes)
    post_spikes_np = map(np.array, post_spikes)
    
    return pre_spikes_np, post_spikes_np    


def get_first_spike_metrics(post_spikes, laser_times):
    """ Returns the mean latency and jitter of the first spike following light """
    
    # get first spikes
    # this was simple one line except for fucking empty lists
    num_trials = np.size(laser_times)
    first_spikes = np.zeros(num_trials)
    for i, j in enumerate(post_spikes):
        if np.size(j>0):
            first_spikes[i] = j[0]
        else:
            first_spikes[i] = np.NaN
    #pdb.set_trace()
    mean_first_spike = np.nanmean(first_spikes[first_spikes < 0.2])
    
    # jitter of first spike
    std_first_spike = np.nanstd(first_spikes[first_spikes < 0.2])
    
    return mean_first_spike, std_first_spike
    
    
def plot_phototag_data(phototag_data):
    """ phototagData is an MPNeuroData class; this function assumes
        This function will calculate the metrics for determing whether a cell is phototagged"""
        
    mask = phototag_data.good_cell_mask
    fig1 = plt.figure()
    plt.plot(mask * phototag_data.mean_first_spike * 1000, mask * phototag_data.mean_pre_isi * 1000, 'o')
    plt.plot(~mask * phototag_data.mean_first_spike * 1000, ~mask * phototag_data.mean_pre_isi * 1000, 's')
    plt.plot([0, 50], [0, 50])
    plt.ylabel('Expected spike time')
    plt.xlabel('Mean first spike latency with light (ms)')
    
    fig2 = plt.figure()
    plt.plot(phototag_data.mean_first_spike*1000, phototag_data.std_first_spike*1000, 'o')
    plt.plot(0, 0)
    plt.ylabel('Jitter (ms)')
    plt.xlabel('Mean first spike latency (ms)')
    
    fig3 = plt.figure()
    plt.plot(phototag_data.mean_first_spike * 1000, phototag_data.first_firing_above_mean *1000, 'o')
    plt.plot([0, 50], [0, 50])
    plt.xlabel('Mean first spike latency (ms)')
    plt.ylabel('Latency for avg firing rate > mean + 3SD (ms)')
