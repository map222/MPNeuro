# -*- coding: utf-8 -*-
"""
Created on Tue Jun 03 15:59:52 2014

@author: palmiteradmin
"""

from __future__ import division
import pdb
import bisect
import numpy as np
def verify_directory(filename):
    '''
    Checks whether the file filename exists in a directory. filename should be the complete
    filename. If the file is not present, verify_directory will change directory to probable
    ones based on the filename stub (first 7 characters)
        
    filename: whole filename (e.g. '150812C feeding.csv')
    '''
    # for long filenames like '150812C feeding.csv', just want first 7 characters
    exp_name = filename[0:7]
    
    import os
    if os.path.isfile(filename ): # check for file; if it's there, all good!
        return
    elif os.path.exists('E:/MP_Data/' + exp_name): # check for directory and go there
        os.chdir('E:/MP_Data/' + exp_name)
    elif os.path.exists('E:/MP_Data/Old_Data/' + exp_name): # maybe it's an old file
         os.chdir('E:/MP_Data/Old_Data/' + exp_name)
    else:
         print('Cannot find data directory')


def extract_waveform_at_timestamp(wideband, timestamps, sample_range = [9, 20], sampling_freq = 32000):
    ''' Extracts the spike waveforms from the wideband data at specific times
    
    | Arguments:
    | wideband: wideband data from a tetrode, probably loaded in by nlxio...load_nlx
    | time_stamps: a single numpy array of timestamps in units of seconds
    | sample_range: number of samples before and after an event (units of samples)
    |    -both values should be positive!
    | sampling_freq: sampling rate for acquisition
    '''

    # check validity of inputs
    assert wideband.shape[1] < 5, 'wideband must contain only one tetrode!'
    assert timestamps.ndim == 1, 'timestamps must be a single timestamp numpy array!'
    assert sample_range[0] > -1, 'pre-event sample range should be positive!'

    if hasattr(timestamps, 'unit'): # if timestamps is a SpikeTrain variable, convert to nd.array
        timestamps = np.array(timestamps)
    
    # convert timestamps to indices
    num_points = wideband.size
    ts = 1 / sampling_freq
    timepoints = np.arange(0, num_points * ts, ts)
    index_stamps = map(lambda x: bisect.bisect_left(timepoints, x), timestamps)
    
    # get all of the cutouts
    num_pre = sample_range[0] # how wide of a cutout to get
    num_post = sample_range[1]
    #cutouts = map(lambda x: wideband[x-num_pre:x+ num_post], index_stamps)
    cutouts = [wideband[x-num_pre:x+ num_post] for x in index_stamps]
    return cutouts