# -*- coding: utf-8 -*-
"""
Created on Tue Jul 07 12:03:07 2015

@author: palmiteradmin
"""
import matplotlib.pyplot as plt
import numpy as np
import MPNeuro.plotting as MP_plot
import pandas as pd

SR57_data = np.array([[0.5, 0.6, 0.45, 0.55, 0.74, 0.63, 0.57],
             [0.29, 0.29, 0.1, 0.29, 0.12, 0.03, 0.12],
             [0.15, 0.25, 0.26, 0.43, 0.12, 0.14, 0.06]]) # data from Google Doc
SR57_males = SR57_data[:, 0:4]
SR57_females = SR57_data[:, 4:]
# plot indices
x = np.ones([3, 4])
x[0] = 0
x[2] = 2

fig, ax = plt.subplots()
plt.xlim([-0.5, 2.5])
SR57_line = plt.plot(x, SR57_males, color = 'b',  linewidth = 2)
SR57_line = plt.plot(x, SR57_females, color = 'r',  linewidth = 2)
plt.ylim([0, 0.75])
plt.ylabel('Food intake in 60 min. (g)', fontsize = 18)
ax.xaxis.set_ticklabels(['', 'Ctl', '', 'SR 10mg/kg', '', 'SR 20mg/kg', ])
MP_plot.prettify_axes(ax)