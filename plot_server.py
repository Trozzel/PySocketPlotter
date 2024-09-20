#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 17:23:28 2020

@author: jorge
"""

import numpy as np
import socket, pickle

from waveforms import Triangle, Sin, Square
from wvfm_array import Array

MY_HOST = ''
MY_PORT = 50007

#%%
def get_bin_array(bytedata):
    """
        Parameters
        ----------
        bytedata : binary (pickled) dictionary of Waveform data
            waveform  = bytedata['waveform']
            amplitude = bytedata['amplitude']
            offset    = bytedata['offset']
            length    = bytedata['length']
            phase     = bytedata['phase']

        Returns
        -------
        binary numpy waveform data array.

    """
    waveform  = bytedata['waveform']
    amplitude = bytedata['amplitude']
    offset    = bytedata['offset']
    length    = bytedata['length']
    phase     = bytedata['phase']
    arr = Array(waveform, amplitude, offset, length, phase).get_array()
    return bytes(arr)

#==============================================================================#
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((MY_HOST, MY_PORT))
    sock.listen(1)
    # Endless loop
    while True:
        conn, addr = sock.accept()
        with conn:
            loop_num = 0
            while True:
                data = conn.recv(1024)
                if not data: break
                # params - paramters for Waveform object in dictionary format
                params = pickle.loads(data)
                num_bytes_sent = conn.send(get_bin_array(params))
                print('Server loop[%d]\nBytes sent = %d, to %s' % 
                      (loop_num, num_bytes_sent, addr))
                loop_num += 1
            

    
