#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 10:18:32 2022

@author: IreneCelestino
"""

import random
import time
import matplotlib.pyplot as plt
import numpy as np


N = int(1e6)
lambda_gamma = 0.1  # mm
THICKNESS = 0.2  # mm



def eff_simple(num_events):
    t0 = time.time()

    num_abs = 0.
    z_array = []
    
    for i in range(num_events):
        length = random.expovariate(1./lambda_gamma)
        z_array.append(length)
        if length < THICKNESS:
            num_abs += 1.
    
    quantum_efficiency = num_abs/num_events
    print(f'Eff quant :  {quantum_efficiency}')
    elapsed_time = time.time() - t0
    
    print(f'Elapsed time 1 : {elapsed_time} s')
    
    #plt.hist(z_array, bins = 100)
    return  quantum_efficiency



def eff_vectorized(num_events):
    t0 = time.time()
    abs_z = np.random.exponential(lambda_gamma, size = num_events)
    abs_z = abs_z[abs_z <= THICKNESS]  # questa è una maschera
    quantum_efficiency = len(abs_z)/num_events
    print(f'Eff quant :  {quantum_efficiency}')
    
    elapsed_time = time.time() - t0
    print(f'Elapsed time 2 : {elapsed_time} s')
    
    
    return quantum_efficiency
    
def example_mask():
    print('\nESEMPIO: Maschera\n')
    a = np.random.uniform(size = 10)
    print(a)
    mask = a > 0.5  # maschera è array booleano di True e False
    print(mask)
    print(mask.sum())
    print(a[mask])
    

quantum_efficiency = eff_simple(N)
quantum_efficiency = eff_vectorized(N)
example_mask()
#plt.show()


# =============================================================================
# APPUNTI ASSEGNAMENTO
# =============================================================================
from scipy.interpolate import InterpolatedUnivariateSpline


class ProbabilityDensityFunction(InterpolatedUnivariateSpline):
    def __init__(self, x, y):
        """Constructor
        x e y sono una griglia di punti, dove y = f(x)
        lei deve interpolare: associare y a x diversi da input
        Restituisce la funzione f(x) che interpola la relazione y=f(x)
        """
        super().__init__(x,y)
# ha creato la spline = polinomio di grado k (in genere 3) che interpola
# ora bisogna normalizzare la funzione usando il metodo integral delle spline
"""
vediamo come generare numeri random con questa pdf

data pdf f(x), si chiama F(x) la cumulative function (cdf)
l'inversa della cdf è la ppf (percentual point function):
    se q è distribuito uniformemente in [0,1] => F^-1(q) è distrubuito con f(x)
    generiamo array di numeri random tra 0 e 1, applichiamo la ppf e array 
    è distribuito con f(x)
"""

if __name__ == '__main__':
    x = np.linspace(0., np.pi, 20)
    y = np.sin(x)
    f = ProbabilityDensityFunction(x, y)
    
    plt.plot(x, y, 'o')
    _x = np.linspace(0., np.pi, 200)
    plt.plot(_x, f(_x))
    plt.show()


