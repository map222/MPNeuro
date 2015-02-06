# -*- coding: utf-8 -*-
"""
Created on Mon Jun 02 11:29:41 2014

@author: palmiteradmin
"""

# placeholder

import MPNeuro.nlxio.helper_functions as hf
import pdb
import numpy as np
import matplotlib.pyplot as plt

class MPNeuroData:
    def __init__(self):
        # cell info in format of: name, cell_id, trial_start, trial_end
        self.cell_info = [['150202A', 3, 0, 149],
                          ['150127C', 3, 0, 49],
                          ['150126C', 6, 0, 119],
                          ['150119B', 5, 120, 239],
                          ['150113B', 2, 120, 239],
                          ['150102A', 0, 0, 149],
                          ['150121B', 2, 0, 119],
                          ['150203C', 0, 200, 399],
                          ['150204A', 0, 0, 199],
                          ['150205A', 0, 0, 199],
                          ['150205A', 6, 0, 199],
                          ['150205A', 8, 0, 199]]
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
        self.num_cells = np.size(self.cell_info, 0)
        self.mean_pre_isi = np.zeros(self.num_cells)
        self.mean_first_spike = np.zeros(self.num_cells)
        self.std_first_spike = np.zeros(self.num_cells)
        self.first_firing_above_mean = np.zeros(self.num_cells)
        self.calc_first_spike()
            
    def calc_first_spike(self):
        import MPNeuro.analysis.raster_spike_laser as rsl
        reload(rsl)
        binwidth = 0.002
        bin_start = -1
        bin_end = 1
        bins = np.arange(bin_start, bin_end+binwidth, binwidth) # bins used for histogram
        num_bins = np.size(bins) -1
        
        for cur_index in range(self.num_cells): # go through each cell
            cur_laser_times = self.laser_times[cur_index]
        
            num_trials = np.size(self.laser_times[cur_index])
            # get aligned spikes; need to do weird [] around spike_times due to how rsl works
            aligned_spikes = rsl.raster_spike_laser([self.spike_times[cur_index]], cur_laser_times, plot = False)
            
            # get the pre-light spikes, then calculate the mean ISI to get predicted first post-light spike time
            pre_spikes = map(lambda x: rsl.window_spike_times(x, bin_start, 0), aligned_spikes)
            pre_spikes2 = map(np.array, pre_spikes)
            diffs = map(np.diff, pre_spikes2)
            diffs2 = np.array([item for sublist in diffs for item in sublist])
            self.mean_pre_isi[cur_index] = np.mean(diffs2) / 2
            
            # get all spikes after light
            post_spikes = map(lambda x: rsl.window_spike_times(x, 0, bin_end), aligned_spikes)
            post_spikes2 = map(np.array, post_spikes)
            
            # get first spikes
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
            
            pre_hist = np.nan * np.ones([np.size(cur_laser_times), num_bins])
            post_hist = np.nan * np.ones([np.size(cur_laser_times), num_bins])
            for i, cur_event in enumerate(cur_laser_times):
                  pre_hist[i,:] = np.histogram(pre_spikes2[i], bins)[0] # create hist for each pulse
                  post_hist[i,:] = np.histogram(post_spikes2[i], bins)[0] # create hist for each pulse
            mean_pre_hist = np.mean(pre_hist[:, 0:(num_bins/2)], axis = 0) # take mean response
            mean_pre_spikes = max([np.mean(mean_pre_hist), 3 * binwidth]) # set minimum threshold of 3 Hz
            std_pre_spikes = np.std(mean_pre_hist)
            mean_post_hist = np.mean(post_hist[:, (num_bins/2):], axis = 0) # take mean response
            self.first_firing_above_mean[cur_index] = np.min(np.where(mean_post_hist > mean_pre_spikes + std_pre_spikes*3)) * binwidth
            
    def plot_data(self):
        fig1 = plt.figure()
        plt.plot(self.mean_first_spike * 1000, self.mean_pre_isi * 1000, 'o')
        plt.plot([0, 0.05], [0, 0.025])
        plt.ylabel('Expected spike time')
        plt.xlabel('Mean first spike latency with light (ms)')
        
        fig2 = plt.figure()
        plt.plot(self.mean_first_spike*1000, self.std_first_spike*1000, 'o')
        plt.ylabel('Jitter (ms)')
        plt.xlabel('Mean first spike latency (ms)')
        
        fig3 = plt.figure()
        plt.plot(self.mean_first_spike * 1000, self.first_firing_above_mean *1000, 'o')
        plt.xlabel('Mean first spike latency (ms)')
        plt.ylabel('Latency for avg firing rate > mean + 3SD (s)')