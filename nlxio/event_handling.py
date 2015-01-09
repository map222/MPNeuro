# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:08:25 2014

@author: palmiteradmin
"""

# my attempt at reading *.nev event files
# adapted from neurapy/neuralynx/lynxio.py by kghose

import pylab
import numpy as np
import csv
import pdb
import MPNeuro.nlxio as nlxio

# this is v2, that simply uses the nlxio package to load events
def load_nev( filename = 'Events.nev'):
    nev_data = nlxio.loadNev(filename)
    event_times = nev_data[0] / 1e6
    event_names = nev_data[3] # event names, unused for now
    
    # read in start event and get start time 
    start_time = event_times[0]    
    
    pulse_starts = event_times[1:-1:2] # alternate timestamps for TTL on and off
    pulse_starts2 = pulse_starts - start_time # subtract start time
    
    # repeat above for end of light pulse
    pulse_ends = event_times[2::2]
    pulse_ends2 = pulse_ends - start_time
    
    return pulse_starts2, pulse_ends2
    
# take timestamps (in seconds), and saves them to *.abc.evt file readable by neuroscope
def save_to_evt(timestamps, event_name = 'stim', filename = 'events.abc.evt'):
    # create "csv" file for opening
    evt_file = open(filename, 'wb')
    csv_writer = csv.writer(evt_file, delimiter = ' ')
    # write the events to the file; the format is simply time and label, whitespace separated
    for event in timestamps:
        csv_writer.writerow([(event * 1000).astype('str'), event_name]) # *1000 for conversion to ms