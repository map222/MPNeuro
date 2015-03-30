# -*- coding: utf-8 -*-
"""
Created on Mon Apr 07 16:58:09 2014

@author: palmiteradmin
"""

from __future__ import division
import csv
import numpy
import pdb

def parse_feedtimes_csv(filename):
    with open(filename) as csv_file:
        csvreader = csv.reader(csv_file, quoting=csv.QUOTE_NONNUMERIC, delimiter = ' ')
    
        # initiliaze the feedtimes and watertimes counters
        feedtimes = []
        watertimes = []
        bed_times = []
        # go through all ines of csv, and append times to proper place
        #pdb.set_trace()
        for row in csvreader:
            if row[0] == 'f':
                feedtimes.append(int(row[1]))
                feedtimes.append(int(row[2]))
            elif row[0] == 'w':
                watertimes.append(int(row[1]))
                watertimes.append(int(row[2]))
            elif row[0] == 'b':
                bed_times.append(int(row[1]))
                bed_times.append(int(row[2]))
    
    # convert the format
    feedtimes_sec = map(convert_mmss_to_sec, feedtimes)
    watertimes_sec = map(convert_mmss_to_sec, watertimes)
    bed_times_sec = map(convert_mmss_to_sec, bed_times)
    
    # need to do this INELEGANT mapping and reshaping because I can't figure out python
    feedtimes_sec = numpy.reshape(feedtimes_sec, [numpy.size(feedtimes_sec) / 2, 2])
    watertimes_sec = numpy.reshape(watertimes_sec, [numpy.size(watertimes_sec) / 2, 2])
    bed_times_sec = numpy.reshape(bed_times_sec, [numpy.size(bed_times_sec) / 2, 2])
    
            
    return feedtimes_sec, watertimes_sec, bed_times_sec
    
    # this function converts a timestamp of form mmss to simply number of seconds
def convert_mmss_to_sec(mmss):
    return numpy.floor(mmss / 100) * 60 + mmss % 100
    
    
def get_times_from_csv_name( csv_name ):
    """ csv_name is a string containing csv name in format of YYMMDDX
        Returns the output of parse_feedtimes_csv, namely feed_times, water_times, and bedding_times """
    return parse_feedtimes_csv('E:\\MP_Data\\' + csv_name + '\\' + csv_name + ' feeding.csv')

#    # hardcoded feed and water times; I switched to csv parsing later; kept for posterity here
#    MP140311A_feedtimes = feedtimes = [[688, 840], [878, 907], [995, 1060], [1080, 1100], [1210, 1350],
#                                      [1370, 1410], [1440, 1470], [1490, 1513], [1610, 1640], [1745, 1800]]
#    MP140314A_feedtimes = [[649, 785], [825, 882], [900, 978], [987, 1014], [1022, 1025], [1142, 1163],
#                           [1320, 1423], [1506, 1529], [1691, 1776], [1987, 2211]]
#    MP140314A_watertimes = [[1050, 1065], [1180,1200], [1538, 1545],[1561, 1565], [1861, 1883]]
#    MP140320A_feedtimes = [[618, 627], [644, 657], [664, 736], [743, 841], [909, 1002], [1021, 1078],
#                           [1100, 1108], [1280, 1297], [1328, 1384], [1414, 1444], [1450, 1544], [1620, 1627],
#                        [1773, 1917], [1941, 2065], [2173, 2304], [2350, 2390]]
#    MP140320A_watertimes = [[888, 898], [1118, 1133], [1302, 1318], [1633, 1635], [1654, 1663], [1668, 1672], [1710, 1717], [2125, 2145]]
#    MP140328A_feedtimes = [[626, 628], [634, 645], [671, 684],[690, 717], [721, 825],[893, 901],[946, 1094],
#                           [1193, 1201], [1253, 1336],[1371, 1394],[1557, 1724], [1750, 1760], [1853, 1901], [1931, 1941]]
#    MP140328A_watertimes = [[1137, 1141]]
#    MP140402A_feedtimes = [[622, 674], [687, 817], [835, 980], [1002, 1095], [1244, 1250], [1347, 1547],
#                           [1681, 1743], [1785, 1835], [1855, 2092], [2469, 2676]]
#    MP140402A_watertimes = [[1174, 1199], [1558, 1575], [1653, 1658], [2144, 2168], [2237, 2243], [2260, 2267]]
#    #MP140404A_feedtimes, MP140404A_watertimes = tp.parse_feedtimes_csv('E:\\MP_Data\\Q12014\\140404A\\140404A feeding.csv')