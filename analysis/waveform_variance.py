# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 11:40:38 2015

@author: Michael Patterson, Palmiter Lab (map222@uw.edu)

When phototagging, light can evoke multi-unit wideband noise. This script compares the variance
of the wideband during light, and spontaneously.
"""

from __future__ import division
import numpy as np
import pdb

def do_it_all( event_times, spike_times, tetrode, ground_electrode ):
    import MPNeuro.plotting.plot_waveforms as pw
    reload(pw)
    spont_std, light_std, _ = calc_wideband_variance( event_times, tetrode, ground_electrode)
    tag_cutouts, spont_cutouts = pw.load_plot_tagged_waveforms( event_times, spike_times, tetrode )
    
    tag_magnitude = calc_spike_magnitude(tag_cutouts, ground_electrode)
    spont_magnitude = calc_spike_magnitude(spont_cutouts, ground_electrode)
    
    a, b, c = calc_spike_detectability(spont_std, light_std,  tag_magnitude, spont_magnitude)
    return a,b,c
        

def calc_wideband_variance(event_times, tetrode, ground_electrode = [], plot_flag = False):
    '''
    Load the wideband data, extract the waveform during all the light times, then calculate
    the variance of each
        
    | Arguments:
    | tetrode: number of the tetrode to be loaded
    | event_times: 1 x N np.array of when the light happens (units of seconds)
    | ground_electrode: which electrode to ignore when calculating variance (1 of 1-4)
    |
    | Returns:
    | total_std: standard deviation of all wideband
    | light_std: standard deviation while light is on
    | light_cutouts: N x X np.array of the wideband waveform during N light stimuli, for easy
      plotting with plotting.plot_waveforms
    '''
    
    import MPNeuro.nlxio as nlxio
    import MPNeuro.plotting.plot_waveforms as pw
    
    # load wideband data
    channel_range = [(tetrode-1)*4 +1, tetrode*4]
    wideband = nlxio.nlx_to_dat.load_nlx(channel_range) / 1000
    
    # delete the ground electrode
    good_electrodes = np.delete(np.arange( 4), ground_electrode)
    wideband = wideband[:, good_electrodes]
    
    # calculate std of all wideband
    total_std = np.std(wideband.ravel())
    print('Standard deviation of entire recording: ' + str(total_std))

    # get the wideband during light
    light_duration = 0.01
    sampling_freq = 32000
    light_samples = sampling_freq * light_duration
    light_cutouts = nlxio.helper_functions.extract_waveform_at_timestamp(
        wideband, event_times, sample_range = [0, light_samples])
        
    if plot_flag: # plot the cutouts if we want to
        pw.plot_all_cutouts(light_cutouts, 0 )
    
    # calculate std of light evoked 
    light_std = np.std(light_cutouts)
    print('Standard deviation during light: ' + str(light_std))
    
    return total_std, light_std, wideband
    
def calc_spike_magnitude(spike_cutouts, ground_electrode = []):
    ''' Calculate the average, and std of the magnitude of spikes; for use in comparison to std
        of the wideband as calculated above
    
    Arguments:
    spike_cutouts: N x X x T np.array of spike waveforms
        -N spikes, with X samples, and T electrodes
    ground_electrode: delete this electrode from spike to avoid artifacts
        -often the ground electrode is on the same tetrode as the spikes; don't want to analyze that one
    '''
    
    assert np.ndim(spike_cutouts) >1, 'Spike cutouts should be waveforms, not timestamps!'
    if abs(np.mean(spike_cutouts)) > 100:
        spike_cutouts /= 1000
    
    # delete ground electrode if present
    good_electrodes = np.delete(np.arange(4), ground_electrode)
    spike_cutouts = np.array(spike_cutouts[:,:,good_electrodes])
    
    # calculate spike magnitude
    spike_maxes = spike_cutouts.max(axis = 1).max(axis = 1)
    spike_mins = spike_cutouts.min(axis = 1).min(axis = 1)
    spike_mags = np.maximum(spike_maxes, abs(spike_mins))
        
    return spike_mags
    
def calc_spike_detectability( spont_std, light_std, tag_spike_mags, spont_spike_mags):
    '''
    Calculate how many spikes can be detected during light
    '''
    import matplotlib.pyplot as plt
    from scipy.stats import norm

    # plot the 3sd noise for spontaneous and light evoked times
    fig = plt.figure(figsize = [9, 6])
    hist, bins, __ = plt.hist(spont_spike_mags, 20, normed = True, alpha = 0.5)
    hist2, _, __ = plt.hist(tag_spike_mags, bins, normed = True, alpha = 0.5)
    plt.xlabel( 'Spike magnitude')
    plt.ylabel('# of spikes')
    plt.plot([3*light_std, 3*light_std], [0, np.max(hist)])
    plt.plot([3*spont_std, 3*spont_std], [0, np.max(hist)])
    
    # calculate flase spike rate
    spike_above_spont_noise = norm.cdf((np.mean(spont_spike_mags) - 3 * spont_std) / np.std(spont_spike_mags))
    spike_above_light_noise = norm.cdf((np.mean(spont_spike_mags) - 3 * light_std) / np.std(spont_spike_mags))
    
    lost_spikes = hist - hist2
    return spike_above_spont_noise, spike_above_light_noise, sum(lost_spikes[lost_spikes > 0])