#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2014, IOhannes m zmölnig, IEM

# This file is part of HDMIports
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HDMImatrix.  If not, see <http://www.gnu.org/licenses/>.
from PySide import QtGui, QtCore
class matrix(QtGui.QMainWindow):
    def __init__(self,
                 inputs=["IN1", "IN2", "IN3", "foo", "bar"],
                 outputs=["OUT1", "OUT2", "OUT3","OUT4"],
                 ):
        super(matrix, self).__init__()
        self.inputs=inputs
        self.outputs=outputs

        self.outgroup=[]
        self.out4in=[]


        self.setupUI()

    def setupUI(self):
        #self.resize(168, 146)
        self.centralwidget = QtGui.QWidget(self)
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setText("")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(self)
        #self.menubar.setGeometry(QtCore.QRect(0, 0, 168, 19))
        self.setMenuBar(self.menubar)

        self.menuFile = QtGui.QMenu(self.menubar)

        self.menuConfiguration = QtGui.QMenu(self.menubar)
        self.menuSerial_Ports = QtGui.QMenu(self.menuConfiguration)

        self.actionQuit = QtGui.QAction(self)
        self.actionNull = QtGui.QAction(self)
        self.actionRead_Settings = QtGui.QAction(self)
        self.actionRead_Settings.setObjectName("actionRead_Settings")

        self.menuFile.addAction(self.actionRead_Settings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuSerial_Ports.addAction(self.actionNull)
        self.menuSerial_Ports.addSeparator()
        self.menuConfiguration.addAction(self.menuSerial_Ports.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuConfiguration.menuAction())

        self.statusbar = QtGui.QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.setWindowTitle("MainWindow")
        self.groupBox.setTitle("HDMImatrix")
        self.menuFile.setTitle("File")
        self.menuConfiguration.setTitle("Configuration")
        self.menuSerial_Ports.setTitle("Serial Ports")
        self.actionQuit.setText("Quit")
        self.actionNull.setText("Rescan")
        self.actionRead_Settings.setText("Read Settings")

        self.setupDynamicUI()
    def setupDynamicUI(self):
        inputs=self.inputs
        outputs=self.outputs

        for innum, input in enumerate(inputs):
            inlabel = QtGui.QLabel(self.groupBox)
            #inlabel.setObjectName(input)
            self.gridLayout.addWidget(inlabel, 1+innum, 0, 1, 1)
            inlabel.setText(input)

        for outnum, output in enumerate(outputs):
            outgroup=QtGui.QButtonGroup(self.groupBox)
            self.outgroup+=[outgroup]
            outlabel = QtGui.QLabel(self.groupBox)
            #outlabel.setObjectName(output)
            self.gridLayout.addWidget(outlabel, 0, 1+outnum, 1, 1)
            outlabel.setText(output)
            self.out4in+=[-1]

            for innum, input in enumerate(inputs):
                butn=QtGui.QRadioButton(self.groupBox)
                butn.setText("")
                self.gridLayout.addWidget(butn, 1+innum, 1+outnum, 1, 1)
                outgroup.addButton(butn)
                outgroup.setId(butn, innum)
                butn.setToolTip("%s -> %s" % (input, output))
                outgroup.buttonClicked.connect(self.clickedRouting)
                #print("connected %s for %s" % (outgroup, butn))

        
    def clickedRouting(self, btn):
        btngrp=btn.group()
        innum=btngrp.checkedId()
        outnum=-1
        for on,og in enumerate(self.outgroup):
            if og is btngrp:
                outnum=on
                break
        if self.out4in[outnum] != innum:
            self.routeInput2Output(innum, outnum)

    def routeInput2Output(self, innum, outnum):
        self.out4in[outnum]=innum
        print("connecting: %s -> %s" % (innum, outnum))

    def rescanSerial(self):
        import serial.tools.list_ports
        ports=serial.tools.list_ports.comports()
        for p in ports:
            print("p=%s" % (p[0],))
        
    
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    window = matrix()
    window.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
