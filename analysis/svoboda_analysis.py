# -*- coding: utf-8 -*-
"""
Created on Wed May 13 01:17:54 2015

@author: palmiteradmin
"""
import numpy as np
import pdb
import scipy.io as scio
import matplotlib.pyplot as plt
import pyfnnd
import MPNeuro.plotting as MP_plot
import MPNeuro.analysis as MP_analy

class CalciumData:
    def __init__(self, df_f, fluor_time, spike_train, spike_time, voltage):
        self.df_f = df_f                # DF / F of the ROI
        self.fluor_time = fluor_time    # timescale of fluorescence
        self.spike_train = spike_train  # a timeseries containing whether spike happened
        self.spike_time = spike_time    
        self.voltage = voltage
        
    def plot_calcium_spikes(self):
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)

        plt.plot(self.fluor_time, self.df_f)
        resampled_spikes = MP_analy.downsample_spike_train(self.spike_train, self.spike_time, self.fluor_time)
        plt.plot(self.fluor_time, resampled_spikes - 0.5)

        plt.xlabel( 'Time (s)', fontsize = 18)
        plt.ylabel('DF / F // spike probability', fontsize = 18)

        MP_plot.prettify_axes(ax)
        

def load_svoboda_cell(date_string, cell_id, start_id, end_id):
    """ Loads in the fluorescence and spike times from an experiment from Chen 2013
    date_string is a MMDD string, e.g. '0521'
    cell_id is number of the cell
    start_id and end_id are the start and end for the files
    """
    df_f = np.array([])
    ca_time = np.array([])
    spike_train = np.array([])
    spike_time = np.array([])
    voltage = np.array([])
    time_offset = 0
    
    for cur_cell in np.arange(start_id, end_id+1):
        cell_string = 'data_2012' + date_string + '_cell' + str(cell_id) + '_00' + str(cur_cell)
        
        matlab_data = scio.loadmat(cell_string, squeeze_me = True, struct_as_record = False)
        obj_data = matlab_data['obj']
        
        cur_fluor = obj_data.timeSeriesArrayHash.value[0].valueMatrix
        f0 = cur_fluor.mean()
        
        df_f = np.append(df_f, (cur_fluor - f0) / f0 )
        ca_time = np.append(ca_time, obj_data.timeSeriesArrayHash.value[0].time + time_offset)
        spike_train = np.append(spike_train, obj_data.timeSeriesArrayHash.value[4].valueMatrix)
        spike_time = np.append(spike_time, obj_data.timeSeriesArrayHash.value[4].time + time_offset)
        voltage = np.append(voltage, obj_data.timeSeriesArrayHash.value[3].valueMatrix)
        
        time_offset = max(ca_time)
    
    cur_data = CalciumData(df_f, ca_time, spike_train, spike_time, voltage)
    cur_data.plot_calcium_spikes()    
    
    return cur_data
    
def compare_truth_pyfnnd( ca_data, learn_theta = (0, 1, 1, 1, 0), tau = 0.6 ):
    from fit_neuron.evaluate import spkd_lib as spkd
    
    n_best, c_best, LL, theta_best = pyfnnd.deconvolve( ca_data.df_f.reshape(-1, 1).T, 
        dt=0.0166, verbosity=1, learn_theta=learn_theta, #tau = tau,
        spikes_tol=1E-5, params_tol=1E-5 )
        
    resamp_spikes = MP_analy.downsample_spike_train(ca_data.spike_train, ca_data.spike_time, ca_data.fluor_time)
    resamp_spikes[resamp_spikes > 1 ] = 1
    n_best = np.roll(n_best, -1)
    
    pyfnnd.plotting.plot_fit(ca_data.df_f.reshape(-1, 1).T, n_best, c_best, theta_best, 0.0166)

#    from sklearn.metrics import roc_curve, auc
#    fpr, tpr, thresholds = roc_curve(resamp_spikes, n_best, pos_label = 1)
#    my_auc = auc(fpr, tpr)

#    plt.figure()
#    plt.plot(fpr, tpr)
#    plt.xlabel('False Positive Rate', fontsize = 18)
#    plt.ylabel('True Positive Rate', fontsize = 18)
#    plt.title('AUC = ' + str(my_auc))
    
    
    thresholds = np.arange(0.01, 1, 0.01)
    true_spk_times = ca_data.spike_time[ca_data.spike_train>0.5]
    max_dist = 2* len(true_spk_times ) # maximum distance for victor purpura
    vp = max_dist * np.ones(99) # victor-purpura
    vp_cost = 5
    
    for i, thresh in enumerate(thresholds):
        if np.sum(n_best > thresh) > max_dist: # is you have a lot of bad spikes, calculating vp can be long
            continue
        else:
            vp[i] = spkd.victor_purpura_dist(ca_data.fluor_time[n_best >thresh], true_spk_times, vp_cost)
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    plt.plot(thresholds, 2 * vp / max_dist )
    plt.xlabel('Threshold', fontsize = 18)
    plt.ylabel('Normalized VP distance ', fontsize = 18)
    plt.title('Minimum distance: ' + str(min(2 * vp / max_dist)) )
    MP_plot.prettify_axes(ax)


    example_spikes = threshold_spike_prob(n_best, 0.07)
    ca_data.plot_calcium_spikes() # makes a new figure
    plt.plot( ca_data.fluor_time, example_spikes + 0.5)
    
    return np.min(2 * vp / max_dist)

def threshold_spike_prob(spike_prob, thresh):
    spike_prob[spike_prob >= thresh] = 1
    spike_prob[spike_prob < thresh] = 0
    return spike_prob
    
def load_all_GCaMP6s():
    all_cells = []
    all_cells.append( load_svoboda_cell('0416', 1, 1, 2) )
    all_cells.append( load_svoboda_cell('0417', 1, 2, 2) )
    all_cells.append( load_svoboda_cell('0417', 3, 1, 3) )
    all_cells.append( load_svoboda_cell('0417', 4, 1, 3) )
    all_cells.append( load_svoboda_cell('0417', 5, 2, 2) )
    all_cells.append( load_svoboda_cell('0515', 1, 3, 6) )
    all_cells.append( load_svoboda_cell('0627', 2, 1, 2) )
    all_cells.append( load_svoboda_cell('0627', 3, 1, 2) )
    all_cells.append( load_svoboda_cell('0627', 4, 4, 5) )
    
    return all_cells
    
def analyze_all_GCaMP6s(bunch_o_cells):
    np_mins = []
    for i in range(len(bunch_o_cells)):
        np_mins.append( compare_truth_pyfnnd(bunch_o_cells[i]) )
        
    return np_mins