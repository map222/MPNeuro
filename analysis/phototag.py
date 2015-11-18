# -*- coding: utf-8 -*-
"""
Created on Fri Mar 06 09:46:38 2015

@author: Michael Patterson

A class and functions to calculate the latency, jitter, and other metrics of spikes following light
"""


from __future__ import division
import MPNeuro.nlxio.helper_functions as hf
import pdb
import numpy as np
import matplotlib.pyplot as plt
import MPNeuro.plotting as MP_plot

exc_cells = [['150202A', 3, 0, 149], # 0
              ['150102A', 0, 0, 149], 
              # ['150113B', 2, 120, 239],
              ['150119B', 5, 120, 239],
              # ['150121B', 2, 0, 119],
              ['150126C', 6, 0, 119],
              ['150127C', 3, 0, 49],
              #['150119C', 0, 0, 119], # too few trials
              #['150127A', 8, 0, 119],
              ['150130A', 5, 0, 149], # 5
              ['150202A', 3, 0, 199],
              ['150203B', 1, 0, 199],
              ['150203C', 0, 200, 399],
              ['150204A', 0, 0, 199],
              ['150205A', 0, 0, 199], # 10
              ['150205A', 6, 0, 199], 
              ['150205A', 8, 0, 199],
              ['150210A', 0, 0, 199],
              ['150210B', 1, 0, 199],
              ['150212A', 0, 0, 199], # 15
              ['150212B', 0, 0, 199],
              ['150212C', 2, 200, 399],
              ['150209A', 0, 0, 199],
              ['150324A', 1, 0, 199],
              ['150326B', 2, 0, 199],
              ['150327A', 1, 0, 199], # 20
              ['150330B', 3, 0, 199],
              ['150402A', 2, 0, 199],
              ['150408A', 1, 0, 199],
              ['150408B', 1, 0, 199],
              ['150415A', 0, 0, 199], # 25
              ['150416C', 2, 0, 199]]
              
inhib_cells = [['150129A', 2, 0, 79],
               ['150127A', 1, 0, 119],
               ['150130A', 0, 0, 149],
               ['150130A', 6, 0, 149],
               ['150212C', 1, 200, 399],
               ['150206A', 2, 0, 199],        
               ['150306A', 1, 0, 199]]
               
figure_cells = [['150327A', 1, 0, 199], # solid feeding
                ['150330B', 3, 0, 199], # CCK
                ['150402A', 2, 0, 199], # ensure
                ['150406A', 3, 0, 199], # hotplate
                ['150713B', 2, 0, 199], # CCK
                ['150731A', 0, 0, 199], # solid feeding
                ['150803B', 0, 0, 199], # CCK
                ['150805A', 1, 0, 199], # ensure
                ['150812C', 0, 0, 99], # CCK
                ['150813A', 0, 0, 99], # hotplate
                #150814Y
                ['150819A', 0, 0, 99], # ensure
                ['150819A', 1, 0, 99], # ensure
                #150818Y
                ['150826B', 2, 0, 99], # CCK
                ['150827A', 2, 0, 99], # ensure
                ['150828A', 0, 0, 99], # ensure
                ['150902A', 3, 0, 99], # solid feeding
                ['150902A', 4, 0, 99], # solid feeding
                ['150921B', 0, 0, 49], # CCK
                ['150923B', 1, 100, 199], # ensure
              ]

class PhototagData:
    """ A class used to store phototag data, including spike times, laser times, and metrics """
    def __init__(self):
        self.spike_times = []
        self.laser_times = []
        
    def load_data(self, cell_list):
        
        self.cell_info = cell_list
        reload(hf)
        for row in cell_list: # go through each cell
            cur_exp = hf.load_analyzed_exp(row[0])
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
        self.inhib_latency = np.zeros(self.num_cells)
        self.failure_rate = np.zeros(self.num_cells)
        

def calc_phototag_metrics(phototag_data):
    """ phototagData is an PhototagData class with data already loaded in
        This function will calculate the metrics for determing whether a cell is phototagged:
        mean latency and jitter of first spike
        timing of average firing rate > mean + 3SD
        and inhibitory timing """
    binwidth = 0.001
    start_time = -1
    end_time = -1 * start_time # end_time should be symmetric with start_time
    bins = np.arange(start_time, end_time+binwidth, binwidth) # bins used for histogram
    
    for cur_index in range(  phototag_data.num_cells): # go through each cell
        print 'Processing cell #: ' + str(cur_index)
        # get split spike times for before and after light
        cur_laser_times = phototag_data.laser_times[cur_index]      
        cur_spikes = [phototag_data.spike_times[cur_index]]
        pre_spikes, post_spikes = align_pre_post_spikes(cur_spikes, cur_laser_times, start_time, end_time)
        
        # calculate the expected first spike time based on average firing rate
        diffs = map(np.diff, pre_spikes)
        diffs2 = np.array([item for sublist in diffs for item in sublist]) # no idea what this does !
        phototag_data.mean_pre_isi[cur_index] = np.mean(diffs2) /2
        
        # measure the actual first spike time (mean and std)
        mean_first_spike, std_first_spike, failure_rate = get_first_spike_metrics(post_spikes)
        phototag_data.mean_first_spike[cur_index] = mean_first_spike
        phototag_data.std_first_spike[cur_index] = std_first_spike
        phototag_data.failure_rate[cur_index] = failure_rate
    
        excite_latency, inhib_latency = calc_firing_changes(cur_laser_times, pre_spikes, post_spikes, bins, binwidth)
        phototag_data.first_firing_above_mean[cur_index] = excite_latency
        phototag_data.inhib_latency[cur_index] = inhib_latency

    # create a mask for cells that meet all criteria    
    phototag_data.good_cell_mask = ((phototag_data.first_firing_above_mean < 0.02) &
                                   (phototag_data.mean_first_spike < 0.02) & (phototag_data.std_first_spike < 0.006) &
                                   (phototag_data.failure_rate < 0.8))
    return phototag_data
    

def calc_firing_changes(cur_laser_times, pre_spikes, post_spikes, bins, binwidth):
    """ Calculate when the firing rate exceeds the mean firing rate + N standard deviations
        or when firing rate falls below 50% of mean - std"""
    num_bins = np.size(bins) -1
    pre_hist = np.nan * np.ones([np.size(cur_laser_times), num_bins])
    post_hist = np.nan * np.ones([np.size(cur_laser_times), num_bins])
    num_trials = np.size(cur_laser_times)
    
    # get all pre_spikes and post_spikes in one vector for easy histogram
    all_pre_spikes  = np.concatenate(pre_spikes) 
    all_post_spikes = np.concatenate(post_spikes)
    
    pre_hist  = np.histogram(all_pre_spikes,  bins)[0] / num_trials
    pre_hist_smooth = np.convolve(pre_hist, [0.25, 0.5, 0.25], mode = 'same')    # smoothing
    post_hist = np.histogram(all_post_spikes, bins)[0] / num_trials
    post_hist_smooth = np.convolve(post_hist, [0.25, 0.5, 0.25], mode = 'same')    # smoothing
    mean_pre_hist = np.mean(pre_hist_smooth[:(num_bins/2)], axis = 0) # set minimum threshold of 3 Hz
    min_threshold = max([mean_pre_hist, 3*binwidth])
    std_pre_spikes = np.std(pre_hist_smooth)

    above_threshold = np.where(post_hist_smooth[(num_bins/2):] > min_threshold + std_pre_spikes*3)
    if np.size(above_threshold) == 0: # if no points above threshold, return nan
        excite_latency = np.nan
    else:
        excite_latency = np.min( above_threshold ) * binwidth
    
    # this code finds the indices of all times where cell was inhibited, then searches for 3 consecutive timepoints
    inhib_latency = np.nan
    
    if mean_pre_hist > 0.01: # only look for inhibition if basal rate is 5Hz (this may be unnecessary with more trials)
        subthreshold = np.where(post_hist_smooth[(num_bins/2):] < (mean_pre_hist - std_pre_spikes / 2)/ 2)
        sub_diff = np.diff(subthreshold)[0]
        for i, k in enumerate(sub_diff[:-2]):
            if k == 1 & sub_diff[i+1] ==1 & sub_diff[i+2] == 1:
                inhib_latency = subthreshold[0][i] * binwidth
                break
            
    return excite_latency + binwidth / 2, inhib_latency + binwidth / 2


import MPNeuro.analysis.raster_spike_laser as rsl
def align_pre_post_spikes(spiketrain, cur_laser_times, start_time, end_time):
    """ Align spike times to laser pulses
        return times before and after zero, within start_time and end_time """
    reload(rsl)
    
    # get aligned spikes; need to do weird [] around spike_times due to how rsl works
    aligned_spikes = rsl.raster_spike_laser(spiketrain, cur_laser_times, rast_start = -1, rast_end = 1, plot_flag = False)
    
    # get the pre-light spikes, then calculate the mean ISI to get predicted first post-light spike time
    pre_spikes = map(lambda x: rsl.window_spike_times(x, start_time, 0), aligned_spikes)
    pre_spikes_np = map(np.array, pre_spikes)
    
    # get all spikes after light
    post_spikes = map(lambda x: rsl.window_spike_times(x, 0, end_time), aligned_spikes)
    post_spikes_np = map(np.array, post_spikes)
    
    return pre_spikes_np, post_spikes_np    


def get_first_spike_metrics(post_spikes):
    """ Returns the mean latency and jitter of the first spike following light """
    
    # get first spikes
    # this was simple one line except for fucking empty lists
    num_trials = np.size(post_spikes)
    first_spikes = np.zeros(num_trials)
    
    for cur_index, cur_spikes in enumerate(post_spikes):
        # make sure there are spikes in that trial, and that they are near the light
        if np.size(cur_spikes>0):
            if cur_spikes[0] < 0.012: # such ghetto nested ifs ; make sure first spike is around light
                first_spikes[cur_index] = cur_spikes[0]
                continue
        first_spikes[cur_index] = np.NaN # if no spikes there, assign NaN
    mean_first_spike = np.nanmean(first_spikes)
    failure_rate = np.count_nonzero(np.isnan(first_spikes)) / num_trials
    
    # jitter of first spike
    std_first_spike = np.nanstd(first_spikes)
    
    return mean_first_spike, std_first_spike, failure_rate
    

import matplotlib
def plot_phototag_data(phototag_data):
    """ phototagData is an MPNeuroData class; this function assumes
        This function will display various metrics for whether a cell is phototagged """
    
    font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 18}

    matplotlib.rc('font', **font)  
    
    mask = phototag_data.good_cell_mask
    fig1 = plt.figure(figsize = [12, 9])
    ax1 = fig1.add_subplot(2,2,1)
    plt.plot(mask * phototag_data.mean_first_spike * 1000, mask * phototag_data.mean_pre_isi * 1000, 'o')
    plt.plot(~mask * phototag_data.mean_first_spike * 1000, ~mask * phototag_data.mean_pre_isi * 1000, 'sr')
    plt.plot([0, 50], [0, 50])
    plt.ylabel('Expected spike time')
    plt.xlabel('Mean first spike latency (ms)')
    MP_plot.prettify_axes(ax1)
    
    # first spike latency and jitter
    ax2 = fig1.add_subplot(2,2,2)
    plt.plot(mask * phototag_data.mean_first_spike*1000, mask * phototag_data.std_first_spike*1000, 'o')
    plt.plot(~mask * phototag_data.mean_first_spike*1000, ~mask * phototag_data.std_first_spike*1000, 'sr')
    plt.plot(0, 0)
    plt.ylabel('Jitter (ms)')
    plt.xlabel('Mean first spike latency (ms)')
    MP_plot.prettify_axes(ax2)
    
    # first spike latency vs signal detection
    ax3 = fig1.add_subplot(2,2,3)
    plt.plot(phototag_data.mean_first_spike * 1000, phototag_data.first_firing_above_mean *1000, 'o')
    #plt.plot([0, 20], [0, 30])
    plt.xlabel('Mean first spike latency (ms)')
    plt.ylabel('Latency for\n firing rate > mean + 3SD (ms)')
    MP_plot.prettify_axes(ax3)
    
    # first spike latency vs signal detection
    ax4 = fig1.add_subplot(2,2,4)
    plt.plot(mask * phototag_data.mean_first_spike * 1000, mask * phototag_data.failure_rate * 100, 'o')
    plt.plot(~mask * phototag_data.mean_first_spike * 1000, ~mask * phototag_data.failure_rate * 100, 'sr')
    plt.xlabel('Mean first spike latency (ms)')
    plt.ylabel('Failure rate (%)')
    MP_plot.prettify_axes(ax4)
    
def plot_inhib_data(phototag_data):
    """ Plot inhibitory metrics for cells """
    
    fig = plt.figure(figsize = [6, 5])
    ax = fig.add_subplot(1,1,1)
    plt.plot(2 / phototag_data.mean_pre_isi, phototag_data.inhib_latency * 1000, 'o') # divide by 2 because the isi yields TWICE the expected spike rate due to how I define it above
    plt.plot(0, 0)
    
    plt.xlabel('Firing rate (Hz)' )
    plt.ylabel('Inhibitory latency (ms)' )
    MP_plot.prettify_axes(ax)

def get_info_for_cell(phototag_data, exp_name, cell_id):
    """ helper function that returns data for a given experiment and cell id """
    
    # get the id of a cell
    row_id = [j for j, i in enumerate(phototag_data.cell_info) if (i[0] is exp_name) & (i[1] == cell_id)]
    print 'First spike latency: ' + str(phototag_data.mean_first_spike[row_id])
    print 'First spike jitter: ' + str(phototag_data.std_first_spike[row_id])
    print 'Latency firing above threshold: ' + str(phototag_data.first_firing_above_mean[row_id])
    print 'Inhibitory latency: ' + str(phototag_data.inhib_latency[row_id])
    print 'Failure rate: ' + str(phototag_data.failure_rate[row_id])
    
def table_all_cells(phototag_data):
    """ Display decently-formatted table of data """

    print 'Exp_name  ID  Latency  Jitter  Mean + SD  Failure '
    for i in range(len(phototag_data.cell_info)):
        print (phototag_data.cell_info[i][0] + '   ' +
                str.format('{0:.2g}', phototag_data.cell_info[i][1]) + '   ' +
                str.format('{0:.2g}', phototag_data.mean_first_spike[i]) + '  ' +
                str.format('{0:.2g}', phototag_data.std_first_spike[i]) + '  ' + 
                str.format('{0:.2g}', phototag_data.first_firing_above_mean[i]) + '  ' +
                str.format('{0:.2g}', phototag_data.failure_rate[i]) + '\n' )

import MPNeuro.nlxio.load_plx as lp
import MPNeuro.plotting.plot_waveforms as pw
from scipy.stats.stats import pearsonr
def calc_pearson_tag_spont(cell_info, plot_flag = False):
    """ cell_info is a list that comes from a Phototag class; it has four members:
    [0]: cell_name
    [1]: cell_id
    [2]: start of phototag stim
    [3]: end of phototag stim
    """
    #pdb.set_trace()
    cur_exp = hf.load_analyzed_exp(cell_info[0], False)
    cell_id = cell_info[1]
    laser_times = cur_exp['laser_times'][cell_info[2]:cell_info[3]]
    
    unitinfo = lp.load_unit_info(cell_info[0])
    tetrode = unitinfo[cell_id][0]
    
    tagged, untagged = pw.load_plot_tagged_waveforms(tetrode, laser_times, cur_exp['spike_times'][cell_id], plot_flag)
    mean_tagged = np.mean(tagged, axis = 0)
    mean_spont = np.mean(untagged, axis = 0)
    return pearsonr(mean_tagged.ravel(), mean_spont.ravel())[0]