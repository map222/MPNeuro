# -*- coding: utf-8 -*-
"""
Created on Tue Jun 03 15:59:52 2014

@author: palmiteradmin
"""
import MPNeuro.nlxio.csv_parsing as cp
import pdb

# load spiketimes and event times for an experiment with a complete *.plx
def load_analyzed_exp(filename, bool_histogram = False):
    # filename is a string of the experiment number, format MPYYMMDDX    ; .plx is added later
    
    verify_directory(filename, '.plx')
    
    import MPNeuro.nlxio.load_plx as lp
    spike_times = lp.load_spike_times(filename)[0] # extra [0] for funky indexing
    
    import MPNeuro.nlxio.event_handling as eh
    laser_times = eh.load_nev()[0]
    
    binned_spikes = []
    if bool_histogram:
        #pdb.set_trace()
        import MPNeuro.analysis.hist_event_firingrate as hef
        reload(hef)
        binned_spikes = hef.hist_event_firingrate(spike_times, laser_times, plot=True)
    
    return dict(spike_times = spike_times, laser_times = laser_times, binned_spikes = binned_spikes)

# verify file is present in directory
# if not, change directory to probably one based on filename
def verify_directory(filename, suffix):
    ''' Checks whether the file filename.suffix exists in a directory;
        If not, will change directory to probable ones based on exp_name
    '''
    # for long filenames like '150812C feeding.csv', just want first 7 characters
    exp_name = filename[0:7]
    
    import os
    if os.path.isfile(filename + suffix): # check for file; if it's there, all good!
        return
    elif os.path.exists('E:/MP_Data/' + exp_name): # check for directory and go there
        os.chdir('E:/MP_Data/' + exp_name)
    elif os.path.exists('E:/MP_Data/Old_Data/' + exp_name): # maybe it's an old file
         os.chdir('E:/MP_Data/Old_Data/' + exp_name)
    else:
         print('Cannot find data directory')
         
def load_feed_times(filestring):
    ''' filename is a string of the experiment number, format MPYYMMDDX
        .csv suffix is added in function '''
    verify_directory(filestring)
    
    full_filename = 'E:/MP_Data/' + filestring + '/' + filestring + ' feeding.csv'
    
    feed_times, water_times = cp.parse_feedtimes_csv(full_filename)
    return feed_times, water_times # times are in seconds