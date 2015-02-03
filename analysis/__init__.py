# -*- coding: utf-8 -*-
"""
Created on Mon Jun 02 11:29:41 2014

@author: palmiteradmin
"""

# placeholder

import MPNeuro.nlxio.helper_functions as hf
import pdb
import MPNeuro.analysis.raster_spike_laser as rsl
import numpy as np

class MPNeuroData:
    def __init__(self):
        # cell info in format of: name, cell_id, trial_start, trial_end
        self.cell_info = [['150202A', 3, 0, 149],
                          ['150127C', 3, 0, 49],
                          ['150126C', 6, 0, 119]]
        self.spike_times = []
        self.laser_times = []
        
    # load the data from the .plx files; cell id info is declared in the __init__
    def load_data(self):
        for row in self.cell_info: # go through each cell
            cur_exp = hf.load_analyzed_exp(row[0])
            self.spike_times.append( cur_exp['spike_times'][row[1]] ) # get spike times for given cell
            self.laser_times.append( cur_exp['laser_times'][row[2]:row[3]] ) # get laser times for range of trials
        self.num_cells = np.size(self.cell_info, 0)
        self.mean_pre_isi = np.zeros(self.num_cells)
        self.mean_first_spike = np.zeros(self.num_cells)
        self.std_first_spike = np.zeros(self.num_cells)
        self.first_firing_above_mean = np.zeros(self.num_cells)
        self.calc_first_spike()
            
    def calc_first_spike(self):
        reload(rsl)
        binwidth = 0.002
        bin_start = -1
        bin_end = 0.5
        bins = np.arange(bin_start, bin_end+binwidth, binwidth) # bins used for histogram
        
        for cur_index in range(self.num_cells): # go through each cell
            cur_laser_times = self.laser_times[cur_index]
        
            num_trials = np.size(self.laser_times[cur_index])
            # get aligned spikes; need to do weird [] around spike_times due to how rsl works
            aligned_spikes = rsl.raster_spike_laser([self.spike_times[cur_index]], cur_laser_times, plot = False)
            # get the pre-light spikes, then calculate the mean ISI to get predicted first post-light spike time
            pre_spikes = map(lambda x: rsl.window_spike_times(x, -1, 0), aligned_spikes)
            pre_spikes2 = map(np.array, pre_spikes)
            diffs = map(np.diff, pre_spikes2)
            diffs2 = np.array([item for sublist in diffs for item in sublist])
            self.mean_pre_isi[cur_index] = np.mean(diffs2)
            
            # get all spikes after light
            post_spikes = map(lambda x: rsl.window_spike_times(x, 0, 1), aligned_spikes)
            post_spikes2 = map(np.array, post_spikes)
            # get first spikes using fun for syntax
            # this was simple one line except for fucking empty lists
            first_spikes = np.zeros(num_trials)
            for i, j in enumerate(post_spikes2):
                if np.size(j>0):
                    first_spikes[i] = j[0]
                else:
                    first_spikes[i] = np.NaN
            self.mean_first_spike[cur_index] = np.nanmean(first_spikes)
            
            # jitter of first spike
            self.std_first_spike[cur_index] = np.nanstd(first_spikes)
            
            pre_hist = np.zeros([np.size(cur_laser_times), np.size(bins)-1])
            post_hist = np.zeros([np.size(cur_laser_times), np.size(bins)-1])
            for i, cur_event in enumerate(cur_laser_times):
                  pre_hist[i,:] = np.histogram(pre_spikes2[i], bins)[0] # create hist for each pulse
                  post_hist[i,:] = np.histogram(post_spikes2[i], bins)[0] # create hist for each pulse
            pdb.set_trace()
            mean_pre_hist = np.mean(pre_hist, axis = 0) # take mean response
            mean_pre_spikes = np.mean(mean_pre_hist)
            std_pre_spikes = np.std(mean_pre_hist)
            mean_post_hist = np.mean(post_hist, axis = 0) # take mean response
            self.first_firing_above_mean[cur_index] = np.min(np.where(mean_post_hist > mean_pre_spikes + std_pre_spikes*3)) * binwidth -1