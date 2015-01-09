# -*- coding: utf-8 -*-
"""
Created on Thu May 08 12:24:10 2014

@author: palmiteradmin
"""

import matplotlib.pyplot as plt

stimdays = [1, 2]
indices = [ -1, -0, 1, 2, 3]
plt.plot(indices, y)
plt.plot(indices, z)

# plot background for stim/ CNO
for i in stimdays:
    plt.axvspan(i-0.5, i+0.5, color = 'c')

plt.ylim(0, 1.2)
plt.ylabel('Food consumed in 60 min (g)')
plt.xlabel('Day')
plt.ylim(0, 2.2)