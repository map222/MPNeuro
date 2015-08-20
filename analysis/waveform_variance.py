# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 11:40:38 2015

@author: Michael Patterson, Palmiter Lab (map222@uw.edu)

When phototagging, light can evoke multi-unit wideband noise. This script compares the variance
of the wideband during light, and spontaneously.
"""

import numpy as np
import pdb

def calc_waveform_variance(tetrode, event_times, ground_electrode = [], plot_flag = False):
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
    wideband = nlxio.nlx_to_dat.load_nlx(channel_range)
    
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
    pdb.set_trace()
    light_cutouts = nlxio.helper_functions.extract_waveform_at_timestamp(
        wideband, event_times, sample_range = [0, light_samples])
        
    if plot_flag: # plot the cutouts if we want to
        pw.plot_all_cutouts(light_cutouts, 0 )
    
    # calculate std of light evoked 
    light_std = np.std(light_cutouts)
    print('Standard deviation during light: ' + str(light_std))
    
    return total_std, light_std, light_cutouts
    
def calc_spike_magnitude(spike_cutouts, ground_electrode = []):
    ''' Calculate the average, and std of the magnitude of spikes; for use in comparison to std
        of the wideband as calculated above
    
    Arguments:
    spike_cutouts: N x X x T np.array of spike waveforms
        -N spikes, with X samples, and T electrodes
    ground_electrode: delete this electrode from spike to avoid artifacts
        -often the ground electrode is on the same tetrode as the spikes; don't want to analyze that one
    '''
    # delete ground electrode if present
    good_electrodes = np.delete(np.arange(4), ground_electrode)
    spike_cutouts = spike_cutouts[:,:,good_electrodes]
    mean_spike = np.mean(np.array(spike_cutouts))