# -*- coding: utf-8 -*-
"""
Created on Sat Jan 17 17:56:55 2015

@author: palmiteradmin
"""

import sys

from PyQt4 import QtGui
from BioDAQGUI import Ui_MainWindow

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())