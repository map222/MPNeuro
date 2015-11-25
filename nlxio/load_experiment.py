# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 09:49:17 2015

@author: Michael Patterson, Palmiter Lab (map222@uw.edu)
"""

import MPNeuro.nlxio.load_plx as lp
import MPNeuro.nlxio.event_handling as eh

# load spiketimes and event times for an experiment with a complete *.plx
def load_analyzed_exp(filename, bool_histogram = False):
    '''
    Loads experiment analyzed by Offline Sorter, specifically the spike times, and  laser (event) times
    
    filename: string of the experiment number, format MPYYMMDDX   ; .plx is added by function
        -for standard names like MP150812B, can be run in any directoy; for non-standard, needs to be in directory
    '''
        
    spike_times = lp.load_spike_times(filename)[0] # extra [0] for funky indexing
    
    laser_times = eh.load_nev()[0]
    
    binned_spikes = []
    if bool_histogram:
        #pdb.set_trace()
        import MPNeuro.analysis.hist_event_firingrate as hef
        reload(hef)
        binned_spikes = hef.hist_event_firingrate(spike_times, laser_times, plot_flag=True)
    
    return dict(spike_times = spike_times, laser_times = laser_times, binned_spikes = binned_spikes)
