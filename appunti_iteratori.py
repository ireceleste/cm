#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 09:40:15 2022

@author: IreneCelestino
"""

# =============================================================================
# ASSEGNAMENTO 5 2021 - appunti
# =============================================================================

"""
Module: advanced Python
Assignment #5 (October 18, 2021)


--- Goal
Write a class to handle a sequence of voltage measurements at different times.

--- Specifications
- the class name must be VoltgeData
- the class must be initialized with two generic iterables of the same length
  holding the numerical values of times and voltages
- alternatively the class can be initialized from a text file
- the class must expose two attributes: 'times' and 'voltages', each returning
  a numpy array of type numpy.float64 of the corresponding quantity.
- the values should be accessible with the familiar square parenthesis syntax:
  the first index must refer to the entry, the second selects time (0) or 
  voltage (1). Slicing must also work.
- calling the len() function on a class instance must return the number of 
  entries
- the class must be iterable: at each iteration, a numpy array of two 
  values (time and voltage) corresponding to an entry in the file must be
  returned
- the print() function must work on class instances. The output must show one
  entry (time and voltage), as well as the entry index, per line.
- the class must also have a debug representation, printing just the values 
  row by row
- the class must be callable, returning an interpolated value of the tension 
  at a given time
- the class must have a plot() method that plots data using matplotlib.
  The plot function must accept an 'ax' argument, so that the user can select
  the axes where the plot is added (with a new figure as default). The user
  must also be able to pass other plot options as usual
- [optional] rewrite the run_tests() function in sandbox/test_voltage_data.py
  as a sequence of proper UnitTests
- [optional] support a third optional column for the voltage errors
 
"""

import numpy as np
from scipy import interpolate
from matplotlib import pyplot as plt

class VoltageData: 
    """
    Class for handling a sequence of voltage measurements at different times.
    """

    def __init__(self, times, voltages):
        """ Times and Voltages must be iterables of the same length"""
        times = np.array(times, dtype=np.float64)
        voltages = np.array(voltages, dtype=np.float64)
         # if len(self.times) != len(self.voltages):
            # raise ValueError('Times and Voltages must be of the same length')
        # conviene usare column_stack per avere matrice a 2 colonne con dati
        self.data = np.column_stack([times, voltages])
        self._spline = interpolate.InterpolatedUnivariateSpline(times, voltages, k=3)
    
    @classmethod
    def from_file(cls, file_path):
         times,voltages = np.loadtxt(file_path, unpack = True)
         return cls(times, voltages)

    @property
    def times(self): 
        return self.data[:,0]
        
    @property
    def voltages(self): 
        return self.data[:,1]
    
    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data[:,0])

    def __iter__(self):
        return iter(self.data)
    
    def __str__(self):
        """
        output_str = ''
        for i, row in enumerate(self):
            line = f'{i} -> {row[0]:.1f}, {row[1]:.2f}\n'
            output_str += line
        return output_str
        """
        header = 'Row -> Time [s], Voltage mV \n'
        return header + '\n'.join(f'{i} -> {row[0]:.1f}, {row[1]:.2f}' 
                                  for i, row in enumerate(self))
    def __call__(self, time):
        """Interpola dati e restituisce V associato a time"""
        return self._spline(time)
    
    def plot(self, ax = None, draw_spline=False, **plot_opts):
        if ax is None: 
            plt.figure('Voltage_vs_Time')
        else:
            plt.sca(ax)
        if draw_spline: 
            x = np.linspace(min(self.times), max(self.times), 100)
            plt.plot(x, self(x), '-', label='spline')
        plt.plot(self.times, self.voltages, **plot_opts, label='data')
        plt.legend()


if __name__ == '__main__':
    vdata = VoltageData.from_file('sample_data_file.txt')
    print(vdata.times, '\n',  vdata.voltages)
    assert vdata[5, 0] == 0.6
    assert vdata[3, 1] == 0.77
    print(len(vdata))
    print(vdata)
    print(vdata(0.63))
    vdata.plot(color = 'k', linestyle = '', marker = 'o', draw_spline=True)
    plt.show()