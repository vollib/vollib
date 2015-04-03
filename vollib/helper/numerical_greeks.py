# -*- coding: utf-8 -*-
"""
    vollib.helper.numerical_greeks
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A library for option pricing, implied volatility, and
    greek calculation.  vollib is based on lets_be_rational,
    a Python wrapper for LetsBeRational by Peter Jaeckel as 
    described below.

    :copyright: © 2015 Iota Technologies Pte Ltd    
    :license: MIT, see LICENSE for more details.

    About LetsBeRational:
    ~~~~~~~~~~~~~~~~~~~~~~~

    The source code of LetsBeRational resides at www.jaeckel.org/LetsBeRational.7z .

    ::

      ======================================================================================
      Copyright © 2013-2014 Peter Jäckel.

      Permission to use, copy, modify, and distribute this software is freely granted,
      provided that this notice is preserved.

      WARRANTY DISCLAIMER
      The Software is provided "as is" without warranty of any kind, either express or implied,
      including without limitation any implied warranties of condition, uninterrupted use,
      merchantability, fitness for a particular purpose, or non-infringement.
      ======================================================================================

"""


# -----------------------------------------------------------------------------
# IMPORTS

# Standard library imports

# Related third party imports

# Local application/library specific imports


# -----------------------------------------------------------------------------
# FUNCTIONS - GENERIC FUNCTIONS FOR NUMERICAL GREEK CALCULATION


dS = .01

def delta(flag, S, K, t, r, v, b, pricing_function):

    if t == 0.0:
        if S == K:
            return {'c':0.5, 'p':-0.5}[flag]
        elif S > K:
            return {'c':1.0, 'p':0.0}[flag]
        else:
            return {'c':0.0, 'p':-1.0}[flag]
    else:
        return (pricing_function(flag, S + dS, K, t, r, v, b) - \
                pricing_function(flag, S - dS, K, t, r, v, b)) / (2 * dS)

def theta(flag, S, K, t, r, v, b, pricing_function):

    if t <= 1. / 365.:
        return pricing_function(flag, S, K, 0.00001, r, v, b) - \
               pricing_function(flag, S, K, t, r, v, b)
    else:
        return pricing_function(flag, S, K, t - 1. / 365., r, v, b) - \
               pricing_function(flag, S, K, t, r, v, b)

def vega(flag, S, K, t, r, v, b, pricing_function):

    return (pricing_function(flag, S, K, t, r, v + 0.01, b) - \
            pricing_function(flag, S, K, t, r, v - 0.01, b)) / 2.

def rho(flag, S, K, t, r, v, b, pricing_function):

    return (pricing_function(flag, S, K, t, r + 0.01, v,  b ) - \
            pricing_function(flag, S, K, t, r - 0.01, v, b )) / (2)

def gamma(flag, S, K, t, r, v, b, pricing_function):

    if t == 0:
        return POSINF if S == K else 0.0        

    return (pricing_function(flag, S + dS, K, t, r, v, b) - 2. * \
            pricing_function(flag, S, K, t, r, v, b) + \
            pricing_function(flag, S - dS, K, t, r, v, b)) / dS ** 2.
