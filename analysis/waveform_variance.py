# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 11:40:38 2015

@author: Michael Patterson, Palmiter Lab (map222@uw.edu)

When phototagging, light can evoke multi-unit wideband noise. This script compares the variance
of the wideband during light, and spontaneously.
"""

import numpy as np
import pdb
import MPNeuro.nlxio as nlxio

def calc_waveform_variance(tetrode, event_times, ground_electrode):
    '''
    Load the wideband data, extract the waveform during all the light times, then calculate
    the variance of each
        
    Arguments:
    tetrode: number of the tetrode to be loaded
    event_times: 1 x N np.array of when the light happens (units of seconds)
    ground_electrode: which electrode to ignore when calculating variance
    '''
    
    channel_range = [(tetrode-1)*4 +1, tetrode*4]
    wideband = nlxio.nlx_to_dat.load_nlx(channel_range)
    
    # delete the ground electrode
    good_electrodes = np.delete(np.arange(0, 4), ground_electrode)
    wideband = wideband[:, good_electrodes]
    
    # calculate std of all wideband
    total_std = np.std(wideband.ravel())
    
    # get the wideband during light
    light_duration = 0.01
    sampling_freq = 32000
    light_samples = sampling_freq * light_duration
    light_cutouts = nlxio.helper_functions.extract_waveform_at_timestamp(
        wideband, event_times, sample_range = [0, light_samples])