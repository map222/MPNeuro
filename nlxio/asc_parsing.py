# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 15:48:49 2015

@author: Michael Patterson, Palmiter Lab (map222@uw.edu)
"""
import pandas as pd
import numpy as np

def load_asc(asc_name):
    '''
    Loads .asc file used by transponder
    
    '''
    with open(asc_name) as asc_file:
        # load the asc
        all_mice = pd.read_csv(asc_file, sep = '\t', skiprows = 39)
        
        # create index column of datetimes
        all_mice.iloc[:,0] = pd.to_datetime(all_mice.iloc[:,0], format='%y/%m/%d %H:%M:%S')        
        col_names = all_mice.columns
        all_mice.set_index(col_names[0], inplace = True)
        all_mice.index.name = 'datetime'

        # cut out extra datetime columns, and rename something more sensible
        # could be more sensible yet!
        mice_indices = np.arange(0, len(all_mice.columns), 2)
        all_mice = all_mice.iloc[:, mice_indices]
        all_mice.columns = ['Col' + str(x) for x in np.arange(len(all_mice.columns))]
        all_mice.head()
    return all_mice