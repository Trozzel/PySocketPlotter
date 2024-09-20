#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 11:05:30 2020

Creates an array of data given a certain Waveform object

x, frequency, amplitude, offset):

@author: jorge
"""
import numpy as np

class Array:
    """
    Produces array with given waveform
    length: - length of desired waveform. Default = 0 
    phase:  -360 to 360 phase shift. Default = 0
    """
#%%
    def __init__(self, waveform, amplitude=1, offset=0, length=360, phase=0):
        self._waveform  = waveform
        self._amplitude = amplitude
        self._offset    = offset
        self._length    = length
        self._phase     = phase
        self.make_array()

#%%
    def __len__(self):
        return len(self._array)

#%%
    def make_array(self):
        self._array = np.zeros(self._length)        # initialize array
        for i in range(self._length):
            self._array[i] = self._amplitude * (self._waveform.set_angle(i+self._phase)) + self._offset

#%%
    def get_array(self):
        return self._array






















