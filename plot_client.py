#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 18:24:05 2020

@author: jorge
"""

import numpy as np
import socket, pickle

from waveforms import Triangle, Sin, Square
from wvfm_array import Array

MY_HOST = 'localhost'
MY_PORT = 50007

def get_server_array(waveform, amplitude=1, offset=0, length=360, phase=0):
    """
        Description
        ----------------
        Receives parameters necessary for a Waveform object (see wvfm_array.py).
        Serializes the parameters and sends to plot_server.py
        Receives an array from plot_server.py based upon paramters sent.
        
        Parameters
        ----------------
            waveform:  waveform object (see wvfm_array.py)
            amplitude: amplitude of the array
            offset:    offset of the waveform
            length:    length of the array to create
            phase:     phase of the array (in degrees)
            
        
        Returns
        ----------------
        Returns the numpy array received from plot_server.py
    """     
    
    params = {'waveform':  waveform,
              'amplitude': amplitude,
              'offset':    offset,
              'length':    length,
              'phase':     phase}
    
    # RUN SERVER
    ############################################################################
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockobj:
        sockobj.connect((MY_HOST, MY_PORT))
        bin_params = pickle.dumps(params)
        sockobj.send(bin_params)
        
        sockobj.settimeout(0.05)
        
        count = 0
        while True:
            try:
                bin_arr = sockobj.recv(4096)
                if not bin_arr: return
            except socket.timeout:
                break
            else:
                if not count:
                    arr = np.frombuffer(bin_arr)
                else:
                    np.append(arr, np.frombuffer(bin_arr))
                count += 1

    return arr
