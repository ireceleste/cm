#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 08:38:21 2022

@author: IreneCelestino
"""

# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Luca Baldini (luca.baldini@pi.infn.it)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Core logic for the pdf definition.
"""


import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
from matplotlib import pyplot as plt

import unittest 
import sys 

if sys.flags.interactive:
    plt.ion()
#serve a runnare in modalità interattiva dalla shell con comando -i (python -i nomefile.py)

class ProbabilityDensityFunction(InterpolatedUnivariateSpline):

    """Class describing a probability density function.
    Parameters
    ----------
    x : array-like
        The array of x values to be passed to the pdf. - Must be sorted!!
    y : array-like
        The array of y values to be passed to the pdf.
    k : int
        The order of the spline
    """

    def __init__(self, x, y, k=3):
        """Constructor.
        """
        norm = InterpolatedUnivariateSpline(x, y, k=k,).integral(x[0], x[-1])
        y/=norm
        InterpolatedUnivariateSpline.__init__(self, x, y, k=k) # k ordine spline
        ycdf = np.array([self.integral(x[0], xcdf) for xcdf in x])
        # nota: integral viene dalla Spline
        # ycdf è la cdf per ogni valore di x : integrale tra min e x
        self.cdf = InterpolatedUnivariateSpline(x, ycdf)
        # Need to make sure that the vector I am passing to the ppf spline as
        # the x values has no duplicates---and need to filter the y
        # accordingly.
        xppf, ippf = np.unique(ycdf, return_index=True)
        # unique prende un array e restituisce valori unici array con indici
        yppf = x[ippf]
        self.ppf = InterpolatedUnivariateSpline(xppf, yppf)

    def prob(self, x1, x2):
        """Return the probability for the random variable to be included
        between x1 and x2.
        Parameters
        ----------
        x1: float or array-like
            The left bound for the integration.
        x2: float or array-like
            The right bound for the integration.
        """
        return self.cdf(x2) - self.cdf(x1)

    def rnd(self, size=1000):
        """Return an array of random values from the pdf.
        Parameters
        ----------
        size: int
            The number of random numbers to extract.
        """
        return self.ppf(np.random.uniform(size=size))
    

class TestPdf(unittest.TestCase):
    def test_uniform(self):
        """ 
        Test per distribuzione uniforme
        """
        x = np.linspace(0., 1., 100)
        y = np.full(x.shape, 1.)
        
        pdf = ProbabilityDensityFunction(x,y)
        # ora voglio controllare che pdf(0.5) è 1  ( o circa 1 a meno di approx di 
        # numeri in virgola mobile)
        self.assertAlmostEqual(pdf(0.5), 1.)
        # verifichiamo ora che pdf sia normalizzata
        self.assertAlmostEqual(pdf.integral(0,1), 1) 
        # verifichiamo che funzioni prob cioè l'integrale della pdf tra 0.25 e 0.75
        self.assertAlmostEqual(pdf.prob(0.25, 0.75), 0.5)
        
        # verifichiamo la cdf ora 
        plt.figure('Uniform cdf')
        plt.plot(x, pdf.cdf(x))
    
    def test_triangular(self):
        x = np.linspace(0., 1., 100)
        y = 3.*x
        pdf = ProbabilityDensityFunction(x, y)
        
        self.assertAlmostEqual(pdf(0.5), 1.)
        self.assertAlmostEqual(pdf.integral(0,1), 1) 

        # verifichiamo la cdf ora : deve essere parabola 
        plt.figure('Triangular cdf')
        plt.plot(x, pdf.cdf(x))
        # verifichiamo la ppf ora 
        plt.figure('Triangular ppf')
        plt.plot(x, pdf.ppf(x))
        
        # verifichiamo la funzione rnd
        plt.figure('Triangular random')
        r = pdf.rnd(100000)
        plt.hist(r, bins = 200)
        
    def test_fancy(self):
        x = np.linspace(0., 1., 100)
        y = np.zeros(x.shape)
        y[x<=0.5] = 2.*x[x<=0.5]
        y[x>=0.75] = 3.
        pdf = ProbabilityDensityFunction(x, y, k=1)
        
        self.assertAlmostEqual(pdf.integral(0,1), 1) 

        plt.figure('Fancy function')
        plt.plot(x, pdf(x))
        # verifichiamo la cdf ora 
        plt.figure('Fancy cdf')
        plt.plot(x, pdf.cdf(x))
        # verifichiamo la ppf ora 
        plt.figure('Fancy ppf')
        plt.plot(x, pdf.ppf(x))
        
        # verifichiamo la funzione rnd
        plt.figure('Fancy random')
        r = pdf.rnd(1000000)
        plt.hist(r, bins = 200)

        

if __name__== '__main__':
    unittest.main(exit=not sys.flags.interactive)  
    # lui chiede di non uscire dal test se ad es c'è un plot, lo fa vedere dopo
    