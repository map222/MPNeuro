# -*- coding: utf-8 -*-
"""
Created on Sat Jan 17 17:56:55 2015

@author: palmiteradmin
"""

import sys

from PyQt4 import QtGui
from BioDAQGUI import Ui_MainWindow
import pdb
import pandas as pd
import numpy as np

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.LoadButton.clicked.connect(self.LoadFile)
        self.ui.GraphButton.clicked.connect(self.GraphData)
        self.ui.SaveCSVButton.clicked.connect(self.SaveCSV)
        self.raw_data = pd.DataFrame()
        self.analyzed_data = pd.DataFrame(columns = ['date', 'id_cage', 'n_bouts', 'mean_bout_dur', 'change_grams'])

    # load a .tab file into the program        
    def LoadFile(self):
        # get filename and load it
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open .tab file')    
        self.raw_data = pd.read_csv( str(filename), delim_whitespace = True, header = None, parse_dates=[[0,1]])
        self.raw_data.columns = ['datetime', 'bout_dur', 'g_start', 'g_change', 'n_cage']
        self.raw_data = self.raw_data.set_index('datetime')
                            
        # update GUI to get data
        # pdb.set_trace()
        self.ui.FileLabel.setText(filename)
        self.ui.StartDateEdit.setDate( self.raw_data.index[0] )
        self.ui.EndDateEdit.setDate( self.raw_data.index[0] )
        
        # skipped setting time since this is tricky
        #self.ui.StartDateEdit.setTime
        
    def GraphData(self):
        cur_data = self.selectData()
        
        
    # select data based on date, time, and cage (values from Gui)
    def selectData(self):
        
        # select cage
        cur_cage = self.ui.StartCageBox.value()
        cur_data = self.raw_data.query('n_cage == cur_cage')
        
        # select time
        start_time = self.ui.StartTimeEdit.time()
        end_time = self.ui.EndTimeEdit.time()
        cur_data = cur_data.between_time(start_time.toPyTime(), end_time.toPyTime())
        
        # select date:
        start_date = self.ui.StartDateEdit.date()
        start_date2 = start_date.toPyDate()
        cur_data = cur_data[start_date2.isoformat()]
        
        # filter out bad data
        min_change = -0.1
        max_change = 1
        cur_data = cur_data.query('g_change > min_change & g_change < max_change')
        return cur_data
        
    def SaveCSV(self):
        pdb.set_trace()
        start_date = self.ui.StartDateEdit.date()
        end_date = self.ui.EndDateEdit.date()
        
        start_cage = self.ui.StartCageBox.value()
        end_cage = self.ui.EndCageBox.value()
        
        # go through all cages and dates, and get data
        for cur_cage in range(start_cage, end_cage+1):
            
            # loop through dates
            for i, date in enumerate( pd.date_range( start = start_date.toPyDate(), end = end_date.toPyDate() ) ):
                # get data for current date
                cur_data = self.selectData()
                cur_index = self.analyzed_data.count()[0] # because of i and j looping, need index
                self.analyzed_data.loc[cur_index] = [date, cur_cage, cur_data.count()[0], cur_data.mean()['bout_dur'],
                    (cur_data['g_start'][0] - cur_data['g_start'][-1]) ]
                    
                # increment the date on the ui
                cur_date = self.ui.StartDateEdit.date()
                self.ui.StartDateEdit.setDate(cur_date.addDays(1))
                
            # for next cage, start at first date
            self.ui.StartDateEdit.setDate(start_date)
                
            # after going through all dates for a cage, increment the cage on the gui
            self.ui.StartCageBox.setValue(cur_cage+1)
            
        self.analyzed_data.to_csv('test.csv')

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())