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
    
    verify_directory(filename)
    
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

def verify_directory(filestring):
    import os
    if os.path.isfile(filestring+'.plx'):
        return
    elif os.path.exists('E:/MP_Data/' + filestring):
        os.chdir('E:/MP_Data/' + filestring)
    elif os.path.exists('E:/MP_Data/Old_Data/' + filestring):
         os.chdir('E:/MP_Data/Old_Data/' + filestring)
    else:
         print('Cannot find data directory')
         
def load_feed_times(filestring):
    # filename is a string of the experiment number, format MPYYMMDDX    ; suffix is added in function
    verify_directory(filestring)
    
    full_filename = 'E:/MP_Data/' + filestring + '/' + filestring + ' feeding.csv'
    
    feed_times, water_times = cp.parse_feedtimes_csv(full_filename)
    return feed_times, water_times # times are in seconds