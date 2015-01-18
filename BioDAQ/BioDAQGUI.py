# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BioDAQGUI.ui'
#
# Created: Sat Jan 17 18:07:53 2015
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.matplotlibwidget = MatplotlibWidget(self.centralwidget)
        self.matplotlibwidget.setGeometry(QtCore.QRect(90, 140, 400, 300))
        self.matplotlibwidget.setObjectName(_fromUtf8("matplotlibwidget"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QtGui.QDockWidget(MainWindow)
        self.dockWidget.setObjectName(_fromUtf8("dockWidget"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.layoutWidget = QtGui.QWidget(self.dockWidgetContents)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 240, 96, 22))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.CageLabel = QtGui.QLabel(self.layoutWidget)
        self.CageLabel.setObjectName(_fromUtf8("CageLabel"))
        self.horizontalLayout.addWidget(self.CageLabel)
        self.spinBox = QtGui.QSpinBox(self.layoutWidget)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(32)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.horizontalLayout.addWidget(self.spinBox)
        self.widget = QtGui.QWidget(self.dockWidgetContents)
        self.widget.setGeometry(QtCore.QRect(30, 400, 140, 22))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.EndTimeLabel = QtGui.QLabel(self.widget)
        self.EndTimeLabel.setObjectName(_fromUtf8("EndTimeLabel"))
        self.horizontalLayout_2.addWidget(self.EndTimeLabel)
        self.timeEdit_2 = QtGui.QTimeEdit(self.widget)
        self.timeEdit_2.setObjectName(_fromUtf8("timeEdit_2"))
        self.horizontalLayout_2.addWidget(self.timeEdit_2)
        self.widget1 = QtGui.QWidget(self.dockWidgetContents)
        self.widget1.setGeometry(QtCore.QRect(30, 370, 146, 22))
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget1)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.StartTimeLabel = QtGui.QLabel(self.widget1)
        self.StartTimeLabel.setObjectName(_fromUtf8("StartTimeLabel"))
        self.horizontalLayout_3.addWidget(self.StartTimeLabel)
        self.timeEdit = QtGui.QTimeEdit(self.widget1)
        self.timeEdit.setObjectName(_fromUtf8("timeEdit"))
        self.horizontalLayout_3.addWidget(self.timeEdit)
        self.widget2 = QtGui.QWidget(self.dockWidgetContents)
        self.widget2.setGeometry(QtCore.QRect(30, 330, 135, 22))
        self.widget2.setObjectName(_fromUtf8("widget2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.widget2)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.EndDateLabel = QtGui.QLabel(self.widget2)
        self.EndDateLabel.setObjectName(_fromUtf8("EndDateLabel"))
        self.horizontalLayout_4.addWidget(self.EndDateLabel)
        self.dateEdit_2 = QtGui.QDateEdit(self.widget2)
        self.dateEdit_2.setObjectName(_fromUtf8("dateEdit_2"))
        self.horizontalLayout_4.addWidget(self.dateEdit_2)
        self.widget3 = QtGui.QWidget(self.dockWidgetContents)
        self.widget3.setGeometry(QtCore.QRect(30, 290, 141, 22))
        self.widget3.setObjectName(_fromUtf8("widget3"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.widget3)
        self.horizontalLayout_5.setMargin(0)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.StartDateLabel = QtGui.QLabel(self.widget3)
        self.StartDateLabel.setObjectName(_fromUtf8("StartDateLabel"))
        self.horizontalLayout_5.addWidget(self.StartDateLabel)
        self.dateEdit = QtGui.QDateEdit(self.widget3)
        self.dateEdit.setObjectName(_fromUtf8("dateEdit"))
        self.horizontalLayout_5.addWidget(self.dateEdit)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.CageLabel.setText(_translate("MainWindow", "Cage #", None))
        self.EndTimeLabel.setText(_translate("MainWindow", "End Time", None))
        self.StartTimeLabel.setText(_translate("MainWindow", "Start Time", None))
        self.EndDateLabel.setText(_translate("MainWindow", "End Date", None))
        self.StartDateLabel.setText(_translate("MainWindow", "Start Date", None))

from matplotlibwidget import MatplotlibWidget
