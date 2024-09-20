# -*- coding: utf-8 -*-
"""
Classes for various kinds of waveforms. This can be expanded
as long the implementation of the class does not change in the derived
classes

"""
import numpy as np

class Waveform:
    
    """
    Base Class for all Waveform objects
    """  
    def __init__(self, angle):
        """
            Parameters
            ----------
            angle : double
                Like a sine wave, it is the angle of the waveform in degrees
            mode : string
                key for dictionary containing parameters for radians or degrees

            Returns
            -------
            double representing the y value.

        """
        self._angle = angle
        self._y     = None
        
        # Get name of class for auto populating / instantiating
        newstr = str(self.__class__)[str(self.__class__).find('.')+1:]
        newstr = newstr[0:newstr.find("'")]
        self.__name = newstr
        
    def angle(self): return self._angle
    
    def y(self, angle=None):
        if angle:
            self._angle = angle
            self._set_y()
        return self._y
    
    def set_angle(self, angle): 
        self._angle = angle
        self._set_y()
        return self._y
        
    def _set_y(self)   : pass

    def name(self)     : return self.__name

#%%
class Triangle(Waveform):
    def __init__(self, angle=0):
        Waveform.__init__(self, angle)
        self._set_y()
    
    def _set_y(self):
        # break triangle wave into four sections, each section called phi
        #       /\      
        #      /  \    
        #          \  /
        #           \/
        # phi: 0|1|2|3
        ######################################################################
        phi = (self._angle % 360) // (360 / 4) # will be 0, 1, 2, 3
        
        if phi == 0: 
            slope  = 1
            offset = 0
        elif phi == 1:
            slope  = -1
            offset = 1
        elif phi == 2:
            slope  = -1
            offset = 0
        elif phi == 3:
            slope  = 1
            offset = -1
        else:
            AssertionError("Your calculations for phi are incorrect")       
        
        x = (self._angle % 90) / 90
        
        self._y = (slope * x) + offset
        
#%%
class Sin(Waveform):
    def __init__(self, angle=0):
        Waveform.__init__(self, angle)
        self._set_y()
        
    def _set_y(self):
        self._y = np.sin(self._angle * (2*np.pi / 360))
          
#%%
class Square(Waveform):
    def __init__(self, angle=0):
        Waveform.__init__(self, angle)
        self._set_y()
    
    def _set_y(self):  
        phi = (self._angle % 360) // (360 / 2)
        
        if phi == 0:
            self._y = 1
        elif phi == 1:
            self._y = -1
        else:
            AssertionError("Your calculations for phi are incorrect")
            
waveforms = [Triangle, Sin, Square]   
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
