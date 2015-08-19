# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 13:19:33 2015

@author: Michael Patterson, Palmiter Lab (map222@uw.edu)

Functions to plot waveforms from cutouts, either for single spikes, or for wideband
"""

from __future__ import division
import numpy as np
import bisect
import matplotlib.pyplot as plt
import MPNeuro.nlxio as nlxio
import pdb

def load_plot_tagged_waveforms( tetrode, event_times, spike_times ):
    ''' Load wideband data, cutout waveforms you care about, and then plot them
    
    Arguments:
    tetrode: number of the tetrode you care about (tetrode 1 = channels 1-4)
    event_times: 1 x N np.array of event_stamps
    spike_times: SpikeTrain array
    '''
    
    if hasattr(spike_times, 'unit'): # if spike_times is a SpikeTrain variable, convert to nd.array
        spike_times = np.array(spike_times)
    
    # load wideband
    channel_range = [(tetrode-1)*4 +1, tetrode*4]
    wideband = nlxio.nlx_to_dat.load_nlx(channel_range)
    
    # tag the spikes
    tagged, spont = assign_timestamp_type(event_times, spike_times)
    
    # extract the spike cutouts
    tagged_waveforms = nlxio.helper_functions.extract_waveform_at_timestamp(wideband, tagged)
    spont_waveforms = nlxio.helper_functions.extract_waveform_at_timestamp(wideband, spont)
    
    # plot the tagged and spontaneous spikes
    tagged_fig = plot_all_cutouts(tagged_waveforms)
    tagged_fig.suptitle('Tagged waveforms')
    spont_fig = plot_all_cutouts(spont_waveforms)    
    spont_fig.suptitle('Spontaneous waveforms')

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
    
    fig = plt.figure(figsize = [5, 7])
    ax = fig.add_subplot(4,1,1)
    map(lambda x: plot_cutout(timepoints, x), cutouts[0:num_plot])
    plt.subplot(4, 1, 4)
    plt.xlabel('Time (ms)')
    #pdb.set_trace()
    
    return fig

# plot a single cutout
def plot_cutout(timepoints, cutout):
    lw = 0.5
    for i in range(4): # hardcode 4 because I look at tetrodes
        plt.subplot(4, 1, i+1)
        plt.plot(timepoints*1000, cutout[:,i] / 1000, linewidth = lw, color = 'grey')
        
def assign_timestamp_type(event_stamps, spike_stamps, window = 0.01):
    ''' Assign spike timestamps into two categories depending on whether spikes occur just after an event
    
    Arguments:
    spike_stamps: timestamps of spikes in units of seconds
    event_stamps: timestamps of events in units of seconds
    window: window after an event for which spikes should be tagged to that event; default is 10ms
    '''
    
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

    #pdb.set_trace()
    # find closest event to the spike    
    event_check_index= bisect.bisect_left(event_stamps, spike_time) - 1
    if event_check_index == -1:
        return False
    else:
        return spike_time - event_stamps[event_check_index] < window # return true if it's close