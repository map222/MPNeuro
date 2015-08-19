# -*- coding: utf-8 -*-
"""
Created on Wed Mar 05 17:40:55 2014

@author: Michael Patterson, Palmiter Lab (map222@uw.edu)
"""
from __future__ import division
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math
import MPNeuro.nlxio.csv_parsing as cp
import pdb
import MPNeuro.plotting as MP_plot
    
def plot_spikes_feed_times( spike_times, exp_name , time_range = []):
    """ Plot spikes vs time for multiple neurons, with overlaid feeding data
    
    Arguments:
    spike_times is a vector of SpikeTImes
    exp_name is a string of format YYMMDDX for experiment name
    time_range is pair of [start, stop] times in seconds
    """
    
    # plot the spike times
    fig, spike_hist = plot_spikes(spike_times, time_range)
    
    reload(cp)
    
    feed_times, water_times, bed_times = cp.parse_feedtimes_csv( exp_name + ' feeding')
    
    feed_times_min = np.array(feed_times) / 60
    water_times_min = np.array(water_times) / 60
    bed_times_min = np.array(bed_times) / 60
    
    for feed_time in feed_times_min:
        plt.axvspan(feed_time[0], feed_time[1], facecolor =  'k', alpha = 0.15)
    for w in water_times_min:
        plt.axvspan(w[0], w[1], facecolor = 'b', alpha = 0.15)
    for b in bed_times_min:
        plt.axvspan(b[0], b[1], facecolor = 'r', alpha = 0.15)
    fig.canvas.manager.window.raise_()
    
    return np.corrcoef(spike_hist)
    
    
def plot_spikes_heat( spike_times, exp_name , time_range = []):
    """ Plot spikes vs time for multiple neurons with overlaid temperature for hot plate experiments
        spike_times is a vector of SpikeTImes
        exp_name is a string of format YYMMDDX for experiment name
        time_range is pair of [start, stop] times in seconds
    """
    
    fig, spike_hist = plot_spikes(spike_times, time_range)
    
    reload(cp)
    
    heat_times, heat_temps = cp.parse_heattimes_csv( exp_name + ' heating' )
    heat_times_min = np.array(heat_times ) / 60
    
    plt.plot(heat_times_min, heat_temps, linewidth = 2, color = 'k', label = 'Temp')
    plt.ylabel('Firing Rate (Hz) / Temp  (C)', fontsize = 18)
    plt.legend(frameon = False)
    
    
def plot_spikes(spike_times, time_range = []):
    """ This function is called by plot_spikes_feed_times, and plot_spikes_heat_times
        to plot all the spikes nicely """
    
    # if there was no specific time_range, it will go from 0 to max
    if len(time_range) == 0:
        time_range = [0, int(spike_times[0].max(0))]
        
    spike_hist = []
    binwidth = 5 # in seconds
    bins = np.array(range(time_range[0], time_range[1], binwidth))
    colorj = ['g', 'b', 'k', 'r']
    
    fig = plt.figure(figsize = [12, 6])
    ax = fig.add_subplot(1,1,1)
    for i, curspikes in enumerate( spike_times):
        temp, nothing = np.histogram(curspikes, bins=bins)
        spike_hist.append(temp)
        ax.plot(bins[:-1] / 60, spike_hist[i]/ (bins[1]-bins[0]), label = 'Neuron ' + str(i),
                 linewidth = math.ceil((i+3 )/ len(colorj)), color = colorj[i%len(colorj)])
    
    plt.legend(frameon = False)
    plt.xlabel('Time (min)', fontsize = 18)
    plt.ylabel('Firing Rate', fontsize = 18)
    plt.show()
    
    MP_plot.prettify_axes(ax)  
    plt.xlim(time_range[0]/60, time_range[1]/60)
    return fig, spike_hist