# -*- coding: utf-8 -*-
"""
To do:
    allow times past midnight
    meal calculations
    -give user error messages for stupid shit like wrong cage or wrong date
    
    -graph in .exe version

Created on Sat Jan 17 17:56:55 2015

@author: palmiteradmin

# to make .py file from .ui
c:\pyuic4.bat BioDAQGUI.ui -o BioDAQGUI.py

# to compile the .py file into an .exe, run the following in the directory below with the .py file
(C:\users\palmiteradmin\documents\github\mpneuro\biodaq):
C:\Users\palmiteradmin\Desktop\WinPython-64bit-2.7.6.3\python-2.7.6.amd64\Scripts\pyinstaller.exe BioDAQmain.py -w
"""

from __future__ import division
import sys

from PyQt4 import QtGui
from BioDAQGUI import Ui_MainWindow
import pdb
import pandas as pd
import numpy as np
import datetime
import os

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # connect ui elements to functions
        self.ui.LoadButton.clicked.connect(self.LoadFile)
        self.ui.GraphButton.clicked.connect(self.GraphData)
        self.ui.SaveCSVButton.clicked.connect(self.SaveCSV)
        self.ui.StartCageBox.valueChanged.connect(self.UpdateGui)
        self.ui.StartDateEdit.dateChanged.connect(self.UpdateGui)
        self.ui.StartTimeEdit.timeChanged.connect(self.UpdateGui)
        
        # structures with data in them
        self.raw_data = pd.DataFrame()
        self.analyzed_data = pd.DataFrame(columns = ['datetime', 'id_cage', 'n_bouts', 'mean_bout_dur',
                                                     'bout_change_g', 'num_meals', 'avg_meal_dur', 'avg_meal_g'])

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
        start_frame = self.create_empty_frame()        
        
        # get data and concatenate the zero point, then turn into cum sum plot
        cur_data = self.selectData()
        cur_data = pd.concat([start_frame, cur_data])
        changesum = cur_data.g_change.cumsum()
        
        #plot stuff
        sumplot = changesum.plot()
        sumplot.axes.set_ylabel('Cumulative grams eaten')
        
    # select data based on date, time, and cage (values from Gui)
    def selectData(self):
        
        # parameter definitions
        start_date = self.ui.StartDateEdit.date()
        start_date2 = start_date.toPyDate()
        start_time = self.ui.StartTimeEdit.time()
        end_time = self.ui.EndTimeEdit.time()
       # pdb.set_trace()

        # select date, then cage, then time
        try:
            if start_time < end_time: # it all happens on a single day
                cur_data = self.raw_data[start_date2.isoformat()].between_time( start_time.toPyTime(), end_time.toPyTime() )
            else: # end_time is next day
                first_day = self.raw_data[start_date2.isoformat()].between_time( start_time.toPyTime(), datetime.time(23, 59, 59) )
                second_day = self.raw_data[ (start_date2 + datetime.timedelta(1)).isoformat()].between_time( datetime.time(0, 0, 0), end_time.toPyTime() )
                cur_data = first_day.append( second_day)
        except:
            # if there is no data for a date, tell user, and return empty dataframe
            QtGui.QMessageBox.about(self, 'No data!', "No data for the selected date: " + str(start_date2) )
            return []
            
        cur_cage = self.ui.StartCageBox.value()
        cur_data = cur_data.query('n_cage == cur_cage')
    
        # filter out bad data
        min_change = self.ui.BoutMinBox.value()
        max_change = self.ui.BoutMaxBox.value()
        cur_data = cur_data.query('g_change >= min_change & g_change <= max_change')
        return cur_data

    def create_empty_frame(self, empty_value = 0, start_bool = True):
        # whether to create empty frame at start or end
        if start_bool:
            empty_time = self.ui.StartTimeEdit.time().toPyTime()
            empty_date = self.ui.StartDateEdit.date().toPyDate()
        else:
            empty_time = self.ui.EndTimeEdit.time().toPyTime()
            empty_date = self.ui.StartDateEdit.date().toPyDate()
            # subtract a minute
            dummy_datetime = datetime.datetime.combine(empty_date, empty_time)
            new_datetime = dummy_datetime - datetime.timedelta(minutes=1)
            empty_time = new_datetime.time()
        empty_frame = pd.DataFrame(columns = ['datetime', 'bout_dur', 'g_start', 'g_change', 'n_cage'])
        empty_frame.loc[0] = [datetime.datetime.combine(empty_date, empty_time)] +[empty_value]*4
        empty_frame = empty_frame.set_index('datetime')
        return empty_frame
    
    def calc_bout_info(self):
        start_date = self.ui.StartDateEdit.date()
        end_date = self.ui.EndDateEdit.date()
        start_time = self.ui.StartTimeEdit.time().toPyTime()
        
        start_cage = self.ui.StartCageBox.value()
        end_cage = self.ui.EndCageBox.value()
        bin_size = self.ui.BinSizeBox.value()
        
        # go through all cages and dates, and get data
        for cur_cage in range(start_cage, end_cage+1):
            for date in  pd.date_range( start = start_date.toPyDate(), end = end_date.toPyDate() ):
                #print cur_cage, date
                # get data for current date
                cur_data = self.selectData()
                meal_data = cur_data
                
                # if there is no data for the date, create an empty row
                if cur_data.empty:
                    empty_frame = pd.DataFrame(columns = self.analyzed_data.columns)
                    empty_frame.loc[0] = [start_date.toPyDate(), cur_cage, 0, 0, 0, 0, 0, 0]
                    self.analyzed_data = pd.concat([self.analyzed_data, empty_frame])
                else:
                    # create a start and end point for the resampling
                    start_frame = self.create_empty_frame(np.NaN, True)
                    end_frame = self.create_empty_frame(np.NaN, False)
                    # increment the date on the ui
                    cur_data = pd.concat([start_frame, cur_data, end_frame])
                    base_time = start_time.hour*60 + start_time.minute
                    
                    # resample (bin) the data
                    df_n_bouts =  cur_data['g_change'].resample( str(bin_size) +'Min', how='count', base= base_time )
                    df_n_bouts.name = 'n_bouts'
                    df_bout_dur = cur_data['bout_dur'].resample( str(bin_size) +'Min', how='mean', base= base_time )
                    df_bout_dur.name = 'mean_bout_dur'
                    df_g_change = cur_data['g_change'].resample( str(bin_size) +'Min', how='sum', base= base_time)
                    df_g_change.name = 'bout_change_g'
                    df_cage = df_bout_dur.copy() # copy to keep date info
                    df_cage[:] = cur_cage
                    df_cage.name = 'id_cage'
                    
                    # meals section; start by initiating values
                    meal_isi = datetime.timedelta(0, self.ui.MealBox.value())
                    bout_starts = meal_data.index.tolist()
                    durs = meal_data['bout_dur'].values
                    bout_ends = []

                    # calculate meal end times
                    for i, row in enumerate(bout_starts):
                        bout_ends.append( row + datetime.timedelta( 0, int(durs[i] )))

                    prev_meal_start_index = 0
                    num_meals = 1
                    meal_dur = []
                    meal_grams = []

                    # find each meal
                    for i, bout_end in enumerate(bout_ends[0:-1]):
                        if bout_end < bout_starts[i+1] - meal_isi:
                            
                            num_meals += 1
                            meal_dur.append( meal_data.ix[prev_meal_start_index:i+1]['bout_dur'].sum() )
                            meal_grams.append( meal_data.ix[prev_meal_start_index:i+1]['g_change'].sum() )
                            prev_meal_start_index = i + 1
                    
                    # add data for last meal
                    meal_dur.append( meal_data.ix[prev_meal_start_index:]['bout_dur'].sum() )
                    meal_grams.append( meal_data.ix[prev_meal_start_index:]['g_change'].sum() )

                    # make meals dataframe
                    df_meals = pd.DataFrame(index = df_cage.index, columns = ['num_meals', 'avg_meal_dur', 'avg_meal_g'])
                    df_meals['num_meals'][0] = num_meals
                    df_meals['avg_meal_dur'][0] = np.mean(meal_dur)
                    df_meals['avg_meal_g'][0] = np.mean(meal_grams)
                    
                    # create dataframe to append to analyzed_data
                    df_bouts = pd.concat([df_cage, df_n_bouts, df_bout_dur, df_g_change], axis = 1)
                    df_append = pd.concat([df_bouts, df_meals], axis = 1)
                    df_append.fillna(0)
                    df_append.reset_index(level=0, inplace=True)

                    self.analyzed_data = pd.concat([self.analyzed_data, df_append])

                cur_date = self.ui.StartDateEdit.date()
                self.ui.StartDateEdit.setDate(cur_date.addDays(1))
                
            # for next cage, start at first date
            self.ui.StartDateEdit.setDate(start_date)
                
            # after going through all dates for a cage, increment the cage on the gui
            self.ui.StartCageBox.setValue(cur_cage+1)
        
        # reset the ui 
        self.ui.StartCageBox.setValue(start_cage)
        self.ui.EndCageBox.setValue(end_cage)
        self.ui.EndDateEdit.setDate(end_date)    
    
    def SaveCSV(self):
        self.calc_bout_info()
       
        # save the data to the csv
        self.analyzed_data.to_csv(self.expname + '.csv', mode='a') # append so it still writes if file there
        QtGui.QMessageBox.about(self, 'Csv saved!', "Csv saved to: " + self.expname + '.csv')
        
        # reset the analyzed data so people don't have to quit
        self.analyzed_data = pd.DataFrame(columns = ['datetime', 'id_cage', 'n_bouts', 'mean_bout_dur',
                                                     'bout_change_g', 'num_meals', 'avg_meal_dur', 'avg_meal_g'])

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