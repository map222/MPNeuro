# -*- coding: utf-8 -*-
"""
To do: allow times past midnight
    allow binning of output - probably can resample data by bin; sum some, average others, then combine after
        -need to figure out how to get the bin range

Created on Sat Jan 17 17:56:55 2015

@author: palmiteradmin

# to make .py file from .ui
c:\pyuic4.bat BioDAQGUI.ui -o BioDAQGUI.py

# to compile the .py file into an .exe, run the following in the directory with the .py file:
C:\Users\palmiteradmin\Desktop\WinPython-64bit-2.7.6.3\python-2.7.6.amd64\Scripts\pyinstaller.exe BioDAQmain.py -w
"""

import sys

from PyQt4 import QtGui
from BioDAQGUI import Ui_MainWindow
import pdb
import pandas as pd
#import numpy as np

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.LoadButton.clicked.connect(self.LoadFile)
        self.ui.GraphButton.clicked.connect(self.GraphData)
        self.ui.SaveCSVButton.clicked.connect(self.SaveCSV)
        self.ui.StartCageBox.valueChanged.connect(self.UpdateGui)
        self.ui.StartDateEdit.dateChanged.connect(self.UpdateGui)
        self.ui.StartTimeEdit.timeChanged.connect(self.UpdateGui)
        self.raw_data = pd.DataFrame()
        self.analyzed_data = pd.DataFrame(columns = ['date', 'id_cage', 'n_bouts', 'mean_bout_dur', 'change_grams'])

    # load a .tab file into the program        
    def LoadFile(self):
        # get filename and load it
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open .tab file', "", 'Tab files (*.tab)')
        self.expname = os.path.basename(str(filename))[:-4]
        self.raw_data = pd.read_csv( str(filename), delim_whitespace = True, header = None, parse_dates=[[0,1]])
        self.raw_data.columns = ['datetime', 'bout_dur', 'g_start', 'g_change', 'n_cage']
        self.raw_data = self.raw_data.set_index('datetime')
                            
        # update GUI to get data
        self.ui.FileLabel.setText(filename)
        self.ui.StartDateEdit.setDate( self.raw_data.index[0] )
        self.ui.EndDateEdit.setDate( self.raw_data.index[0] )
        
        # skipped setting time since this is tricky
        #self.ui.StartDateEdit.setTime
        
    def GraphData(self):
        # initialize zero point
        #pdb.set_trace()
        start_time = self.ui.StartTimeEdit.time().toPyTime()
        start_date = self.ui.StartDateEdit.date().toPyDate()
        start_frame = pd.DataFrame(columns = ['datetime', 'bout_dur', 'g_start', 'g_change', 'n_cage'])
        start_frame.loc[0] = [datetime.datetime.combine(start_date, start_time)] +[0]*4
        start_frame = start_frame.set_index('datetime')
        
        cur_data = self.selectData()
        cur_data = pd.concat([start_frame, cur_data])
        changesum = cur_data.g_change.cumsum()
        #end_time = self.ui.EndTimeEdit.time().toPyTime()
        #bin_num = 10
        #timerange = 
        sumplot = changesum.plot()
        sumplot.axes.set_ylabel('Cumulative grams eaten')
        
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
        min_change = self.ui.BoutMinBox.value() # -0.1
        max_change = self.ui.BoutMaxBox.value()
        cur_data = cur_data.query('g_change > min_change & g_change < max_change')
        return cur_data
        
    def SaveCSV(self):
        start_date = self.ui.StartDateEdit.date()
        end_date = self.ui.EndDateEdit.date()
        
        start_cage = self.ui.StartCageBox.value()
        end_cage = self.ui.EndCageBox.value()
        
        # go through all cages and dates, and get data
        for cur_cage in range(start_cage, end_cage+1):
            
            # loop through dates
            for date in  pd.date_range( start = start_date.toPyDate(), end = end_date.toPyDate() ):
                print cur_cage, date
                # get data for current date
                cur_data = self.selectData()
                cur_index = self.analyzed_data.count()[0] # because of i and j looping, need index
                                
                if cur_data.empty:
                    self.analyzed_data.loc[cur_index] = [date, cur_cage ] + [0]*3
                else:
                    self.analyzed_data.loc[cur_index] = [date, cur_cage, cur_data.count()[0], cur_data.mean()['bout_dur'],
                        cur_data.sum()['g_change'] ] # sum the changes
                        #(cur_data['g_start'][0] - cur_data['g_start'][-1]) ] #subtract end from start
                        
                # increment the date on the ui
                cur_date = self.ui.StartDateEdit.date()
                self.ui.StartDateEdit.setDate(cur_date.addDays(1))
                
            # for next cage, start at first date
            self.ui.StartDateEdit.setDate(start_date)
                
            # after going through all dates for a cage, increment the cage on the gui
            self.ui.StartCageBox.setValue(cur_cage+1)
            
        self.ui.StartCageBox.setValue(start_cage)
        self.analyzed_data.to_csv(self.expname + '.csv', mode='a') # append so it still writes if file there
        QtGui.QMessageBox.about(self, 'Csv saved!', "Csv saved to: " + self.expname + '.csv')

    # when start boxes are changed, update the end box #s to be after start
    def UpdateGui(self):
        # cage #s
        if self.ui.StartCageBox.value() > self.ui.EndCageBox.value():
            self.ui.EndCageBox.setValue( self.ui.StartCageBox.value() )
        # dates
        elif self.ui.StartDateEdit.date() > self.ui.EndDateEdit.date():
            self.ui.EndDateEdit.setDate( self.ui.StartDateEdit.date() )
        # times
        elif self.ui.StartTimeEdit.time() > self.ui.EndTimeEdit.time():
            self.ui.EndTimeEdit.setTime( self.ui.StartTimeEdit.time() )
            self.ui.EndTimeEdit.stepBy(1)
            
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())