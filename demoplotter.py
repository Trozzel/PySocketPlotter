#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 11:54:39 2020

@author: jorge
"""

import sys
import time

from waveforms import Triangle, Sin, Square, waveforms
from wvfm_array import Array
from plot_client import get_server_array

import numpy as np

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

QPushButton = QtWidgets.QPushButton
QSlider     = QtWidgets.QSlider
QComboBox   = QtWidgets.QComboBox

#*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^# 
class ApplicationWindow(QtWidgets.QMainWindow):
################################################################################
    def __init__(self, title="Plots"):
        super().__init__()
        self._xmin = 0
        self._xmax = 10
        self.setWindowTitle("Plots")
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)        
        self.macro_init()
        
################################################################################
    def macro_init(self):
        """
        Calls initialization functions to be run at initialization
        """
        self.axes_init()
        self.widgets_init()

################################################################################
    def axes_init(self, x_data=None, y_data=None):
        """
        Place axes within the central layout
        """   
        self.main_layout = QtWidgets.QVBoxLayout(self._main)
        
        cntr_layout = QtWidgets.QHBoxLayout()
        left_cntr_layout = QtWidgets.QVBoxLayout()
        cntr_layout.addLayout(left_cntr_layout)
        self.main_layout.addLayout(cntr_layout)
        
        # Layout to the right of the axes
        # AMPLITUDE SLIDER
        slider = QSlider(2)
        self._amplitudeval = 1
        slider.setRange(0, 100)
        slider.valueChanged.connect(self.amplitudeSlider_moved)
        cntr_layout.addWidget(slider)
        
        # OFFSET SLIDER
        slider = QSlider(2)
        self._offsetval = 0
        slider.setRange(-100, 100)
        slider.valueChanged.connect(self.offsetSlider_moved)
        cntr_layout.addWidget(slider)

        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        left_cntr_layout.addWidget(dynamic_canvas)
        self.addToolBar(QtCore.Qt.BottomToolBarArea,
                        NavigationToolbar(dynamic_canvas, self))

        self._dynamic_ax = dynamic_canvas.figure.subplots()
        self._timer = dynamic_canvas.new_timer(
            250, [(self._update_canvas, (), {})])
        
        # (_pause) ? turn off canvas draw : continue to draw
        self._pause = False
        
        # phase shift will increase to give effect of moving
        self._phaseshift = 0
        self._timer.start()
        
################################################################################
    def widgets_init(self):
        """
        Place the widgets in the appropriate layout (center, right left, 
        or bottom)
        """
        # Layout below the axes (Pushbuttons)
        self.btm_layout  = QtWidgets.QHBoxLayout()
        
        ### CREATE QLISTWIDGET WITH WAVEFORM TYPES ###
        self._wvfrmCombo = QComboBox()
        for wave in waveforms:
            item = self._wvfrmCombo.addItem(wave().name(), wave)
        self.btm_layout.addWidget(self._wvfrmCombo)
        
        ### ADD HORIZONTAL SPACER ###
        hSpacer = QtWidgets.QSpacerItem(200, 
                                        0, 
                                        QtWidgets.QSizePolicy.Minimum, 
                                        QtWidgets.QSizePolicy.Expanding) 
        self.btm_layout.addSpacerItem(hSpacer)
        
        btn1 = QPushButton("Pause")
        self.btm_layout.addWidget(btn1)
        btn2 = QPushButton("Cancel")
        self.btm_layout.addWidget(btn2)
        self.main_layout.addLayout(self.btm_layout)
        #connect buttons to slots
        btn1.clicked.connect(self.pauseBtn_clicked)
        btn2.clicked.connect(self.cancelBtn_clicked)
    
################################################################################
    def pauseBtn_clicked(self):
        print("Pausing plot")
        self._pause = not self._pause
        
################################################################################
    def cancelBtn_clicked(self):
        print("Cancel Button Clicked")
        self.close()
        
################################################################################
    def amplitudeSlider_moved(self, value):
        self._amplitudeval = value
        
################################################################################
    def offsetSlider_moved(self, value):
        self._offsetval = value
        
################################################################################
    def _update_canvas(self):
        """
        Call back for canvas. timer object
        """

        self._dynamic_ax.clear()
        t = np.linspace(self._xmin, self._xmax, 360)
        x_range    = self._xmax - self._xmin
        self._xmin = self._xmax + 1
        self._xmax = self._xmax + x_range + 1
        # Use fixed vertical limits to prevent autoscaling changing the scale
        # of the axis.
        self._dynamic_ax.set_ylim(-100.1, 100.1)
        # Shift the sinusoid as a function of time.
        
        # wfm = Sin() # defaults to 0
        # array = Array(self._wvfrmCombo.currentData(), 
        array = get_server_array(
                      self._wvfrmCombo.currentData()(),
                      amplitude=self._amplitudeval, 
                      offset=self._offsetval,
                      length=360,
                      phase=self._phaseshift)
        self._phaseshift += 10
        # self._dynamic_ax.plot(t, array.get_array())
        self._dynamic_ax.plot(array)                  
        # self._dynamic_ax.plot(t, self._sliderval * np.sin(t + time.time()))
        if not self._pause:
            self._dynamic_ax.figure.canvas.draw()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -# 
if __name__ == "__main__":
    # Check whether there is already a running QApplication (e.g., if running
    # from an IDE).
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec_()
