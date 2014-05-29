# -*- coding: utf-8 -*-
"""
Created on Thu May 08 12:24:10 2014

@author: palmiteradmin
"""

stimdays = [1, 2]
indices = [-3, -2, -1, 1, 2]
plot.plot(indices, a)
plt.plot(indices, b)

# plot background for stim/ CNO
for i in stimdays:
    plot.axvspan(i-0.5, i+0.5, color = 'c')

plt.ylim(0, 1.2)
plt.ylabel('Food consumed in 60 min (g)')
plt.xlabel('Day')
plt.ylim(0, 1.2)