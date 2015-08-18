# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 13:19:33 2015

@author: Michael Patterson, Palmiter Lab (map222@uw.edu)
"""

from __future__ import division
import numpy as np
import bisect
import matplotlib.pyplot as plt
import pdb

def extract_waveform_at_timestamp(wideband, timestamps, sampling_freq = 32000):
    ''' Extracts the spike waveforms from the wideband data at specific tiMPNeuro.analysis
    
    Arguments:
    wideband: wideband data from a tetrode, probably loaded in by nlxio...load_nlx
    time_stamps: a single numpy array of timestamps in units of seconds
    sampling_freq: sampling rate for acquisition
    '''
    
    # check validity of inputs
    assert wideband.shape[1] == 4, 'wideband must contain only one tetrode!'
    assert timestamps.ndim == 1, 'timestamps must be a single timestamp numpy array!'
    
    if hasattr(timestamps, 'unit'): # if timestamps is a SpikeTrain variable, convert to nd.array
        timestamps = np.array(timestamps)
    
    # convert timestamps to indices
    num_points = wideband.size
    ts = 1 / sampling_freq
    timepoints = np.arange(0, num_points * ts, ts)
    index_stamps = map(lambda x: bisect.bisect_left(timepoints, x), timestamps)
    
    # get all of the cutouts
    num_pre = 9 # how wide of a cutout to get
    num_post = 22
    cutouts = map(lambda x: wideband[x-num_pre:x+ num_post], index_stamps)
    return cutouts

def plot_all_cutouts(cutouts, num_pre = 9, num_plot = 100, sampling_freq = 32000):
    ''' Plots a list of tetrode waveform cutouts
    
    Arguments:
    cutouts: N x m x 4 matrix of cutout waveforms, where N is number of timestamps, and m is width of cutout
            -this probably comes from extract_waveform_at_timestamps
    num_pre: number of points before event
    num_plot: number of cutouts to plot
    sampling_freq: sampling rate for acquisition
    '''
    
    num_plot = min( np.shape(cutouts)[0], num_plot)
    
    cutout_length = cutouts[0].shape[0]
    ts = 1 / sampling_freq
    timepoints = np.arange(-num_pre * ts, (cutout_length -num_pre)* ts, ts)
    
    fig = plt.figure(figsize = [12, 6])
    ax = fig.add_subplot(4,1,1)
    map(lambda x: plot_cutout(timepoints, x), cutouts[0:num_plot])
    
    return fig

# plot a single cutout
def plot_cutout(timepoints, cutout):
    lw = 0.5
    for i in range(4): # hardcode 4 because I look at tetrodes
        plt.subplot(4, 1, i+1)
        plt.plot(timepoints, cutout[:,i], linewidth = lw, color = 'grey')
        
def assign_timestamp_type(event_stamps, spike_stamps, window = 0.01):
    ''' Assign spike timestamps into two categories depending on whether spikes occur just after an event
    
    Arguments:
    spike_stamps: timestamps of spikes in units of seconds
    event_stamps: timestamps of events in units of seconds
    window: window after an event for which spikes should be tagged to that event; default is 10ms
    '''
    
    
    
    pdb.set_trace()
    if hasattr(spike_stamps, 'unit'): # if timestamps is a SpikeTrain variable, convert to nd.array
        spike_stamps = np.array(spike_stamps)
    
    # create mask of tagged spikes
    tagged_mask = np.array( map(lambda x: calc_is_tagged(event_stamps, x, window), spike_stamps) )
    tagged_spike_stamps = spike_stamps[tagged_mask]
    untagged_spike_stamps = spike_stamps[~tagged_mask]
        
    return tagged_spike_stamps, untagged_spike_stamps
    
def calc_is_tagged(event_stamps, spike_time, window = 0.01):
    ''' Function to see whether a single spike is just after any of the events in eventstamps
    
    Arguments:
    event_stamps: numpy array of timepoints in seconds
    spike_time: scalar timepoint of an ev
    '''

    # find closest event to the spike    
    event_check_index= bisect.bisect_left(event_stamps, spike_time) - 1
    return spike_time - event_stamps[event_check_index] < window # return true if it's close