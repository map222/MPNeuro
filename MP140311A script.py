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
import MPNeuro.nlxio.textparsing as tp
import pdb

spikehist = []
binwidth = 2 # in seconds
bins = np.array(range(0,a[0].max(0), binwidth))
lw = 3 # linewidth
colorj = ['g', 'b', 'k', 'r']

fig = plt.figure(figsize = [12, 6])
ax = fig.add_subplot(1,1,1)
for i, curspikes in enumerate(a):
    temp, nothing = np.histogram(curspikes, bins=bins)
    spikehist.append(temp)
    ax.plot(bins[:-1] / 60, spikehist[i]/ (bins[1]-bins[0]), label = str(i),
             linewidth = math.ceil((i+3 )/ len(colorj)), color = colorj[i%len(colorj)])
max_Hz = 25
ax.plot([10, 10], [0, max_Hz], '-k', linewidth=1)

plt.legend(frameon = False)
plt.xlabel('Time (min)', fontsize = 18)
plt.ylabel('Firing Rate', fontsize = 18)
plt.show()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(14)
for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(14)
plt.xlim(15, 90)

# hardcoded feed and water times; I switched to csv parsing later
MP140311A_feedtimes = feedtimes = [[688, 840], [878, 907], [995, 1060], [1080, 1100], [1210, 1350],
                                  [1370, 1410], [1440, 1470], [1490, 1513], [1610, 1640], [1745, 1800]]
MP140314A_feedtimes = [[649, 785], [825, 882], [900, 978], [987, 1014], [1022, 1025], [1142, 1163],
                       [1320, 1423], [1506, 1529], [1691, 1776], [1987, 2211]]
MP140314A_watertimes = [[1050, 1065], [1180,1200], [1538, 1545],[1561, 1565], [1861, 1883]]
MP140320A_feedtimes = [[618, 627], [644, 657], [664, 736], [743, 841], [909, 1002], [1021, 1078],
                       [1100, 1108], [1280, 1297], [1328, 1384], [1414, 1444], [1450, 1544], [1620, 1627],
                    [1773, 1917], [1941, 2065], [2173, 2304], [2350, 2390]]
MP140320A_watertimes = [[888, 898], [1118, 1133], [1302, 1318], [1633, 1635], [1654, 1663], [1668, 1672], [1710, 1717], [2125, 2145]]
MP140328A_feedtimes = [[626, 628], [634, 645], [671, 684],[690, 717], [721, 825],[893, 901],[946, 1094],
                       [1193, 1201], [1253, 1336],[1371, 1394],[1557, 1724], [1750, 1760], [1853, 1901], [1931, 1941]]
MP140328A_watertimes = [[1137, 1141]]
MP140402A_feedtimes = [[622, 674], [687, 817], [835, 980], [1002, 1095], [1244, 1250], [1347, 1547],
                       [1681, 1743], [1785, 1835], [1855, 2092], [2469, 2676]]
MP140402A_watertimes = [[1174, 1199], [1558, 1575], [1653, 1658], [2144, 2168], [2237, 2243], [2260, 2267]]
#MP140404A_feedtimes, MP140404A_watertimes = tp.parse_feedtimes_csv('E:\\MP_Data\\Q12014\\140404A\\140404A feeding.csv')
MP140708B_feedtimes, MP140708B_watertimes = tp.parse_feedtimes_csv('E:\\MP_Data\\140708B\\140708B feeding.csv')
MP140709A_feedtimes, MP140709A_watertimes = tp.parse_feedtimes_csv('E:\\MP_Data\\140709A\\140709A feeding.csv')
MP140710A_feedtimes, MP140710A_watertimes = tp.parse_feedtimes_csv('E:\\MP_Data\\140710A\\140710A feeding.csv')
MP140716A_feedtimes, MP140716A_watertimes = tp.parse_feedtimes_csv('E:\\MP_Data\\140716A\\140716A feeding.csv')
MP140718A_feedtimes, MP140718A_watertimes = tp.parse_feedtimes_csv('E:\\MP_Data\\140718A\\140718A feeding.csv')
MP140722A_feedtimes, MP140722A_watertimes = tp.parse_feedtimes_csv('E:\\MP_Data\\140722A\\140722A feeding.csv')
MP140729B_feedtimes, MP140729B_watertimes = tp.parse_feedtimes_csv('E:\\MP_Data\\140729B\\140729B feeding.csv')
MP140807B_feedtimes, MP140807B_watertimes = tp.parse_feedtimes_csv('E:\\MP_Data\\140807B\\140807B feeding.csv')
MP140812B_feedtimes, MP140812B_watertimes = tp.parse_feedtimes_csv('E:\\MP_Data\\140812B\\140812B feeding.csv')
MP140813B_feedtimes, MP140813B_watertimes = tp.parse_feedtimes_csv('E:\\MP_Data\\140813B\\140813B feeding.csv')
MP140819B_feedtimes, MP140819B_watertimes = tp.parse_feedtimes_csv('E:\\MP_Data\\140819B\\140819B feeding.csv')
MP140821A_feedtimes, MP140821A_watertimes = tp.parse_feedtimes_csv('E:\\MP_Data\\140821A\\140821A feeding.csv')
MP140924A_feedtimes, MP140924A_watertimes = tp.parse_feedtimes_csv('E:\\MP_Data\\140924A\\140924A feeding.csv')
MP141010A_feedtimes, MP141010A_watertimes = tp.parse_feedtimes_csv('E:\\MP_Data\\141010A\\141010A feeding.csv')
MP141016B_feedtimes, MP141016B_watertimes = tp.parse_feedtimes_csv('E:\\MP_Data\\141016B\\141016B feeding.csv')
MP150127B_feedtimes, MP150127B_watertimes = tp.parse_feedtimes_csv('E:\\MP_Data\\150127B\\150127B feeding.csv')
MP150129A_feedtimes, MP150129A_watertimes = tp.parse_feedtimes_csv('E:\\MP_Data\\150129A\\150129A feeding.csv')
MP150206A_feedtimes, MP150206A_watertimes = tp.parse_feedtimes_csv('E:\\MP_Data\\150206A\\150206A feeding.csv')

feedtimes = np.array(MP150206A_feedtimes) / 60
watertimes = np.array(MP150206A_watertimes) / 60

for j in feedtimes:
    plt.plot(j, [max_Hz-6, max_Hz-6], color =  'k', linewidth = lw)
for w in watertimes:
    plt.plot(w, [max_Hz-1, max_Hz-1], color = 'b', linewidth = lw)
fig.canvas.manager.window.raise_()