# -*- coding: utf-8 -*-
"""
    vollib.helper
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
import numpy
from numpy import log, sqrt, exp

# -----------------------------------------------------------------------------
# DATA

ONE_OVER_SQRT_TWO_PI = 0.3989422804014326779399460599343818684758586311649
CALL = 'c'
PUT = 'p'

'''
Note:  The paper "Let's be Rational" uses theta for q.
+1 represents a call, -1 represents a put.

See page 1, Introduction, first paragraph.
'''

binary_flag = {CALL:1,PUT:-1}

# -----------------------------------------------------------------------------
# FUNCTIONS

pdf = lambda x: ONE_OVER_SQRT_TWO_PI * numpy.exp(-.5*x*x)

def forward_price(S,t,r):
    

    """Calculate the forward price of an underlying asset.

    Keyword arguments:
    S -- spot price of the underlying asset
    t -- time to expiration in years
    r -- the risk-free interest rate

    >>> S = 95
    >>> t = .5
    >>> r = .02
    >>> forward_price(S,t,r)
    95.95476587299596
    """
    return S/numpy.exp(-r*t)



# -----------------------------------------------------------------------------
# MAIN
if __name__=='__main__':
    import doctest
    if not doctest.testmod().failed:
        print "Doctest passed"
