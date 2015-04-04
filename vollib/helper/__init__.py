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

binary_flag = {CALL:1,PUT:-1}

def test_binary_flag():
    
    """
    ::
    
      ========================================================
    
      Note:  In "Let's be Rational," Peter Jäckel uses θ as a flag
      to distinguish between puts and calls.
      +1 represents a call, -1 represents a put.
    
      See page 1, Introduction, first paragraph.
      
      Throughout vollib this is replaced with 'c' and 'p'.
      ========================================================    
    
    >>> binary_flag['c']
    1
    >>> binary_flag['p']
    -1
    """

# -----------------------------------------------------------------------------
# FUNCTIONS

pdf = lambda x: ONE_OVER_SQRT_TWO_PI * numpy.exp(-.5*x*x)
"""the probability density function

    :param x: a continuous random variable
    :type S: float

"""


def forward_price(S,t,r):
    

    """Calculate the forward price of an underlying asset.

    :param S: underlying asset price
    :type S: float
    :param t: time to expiration in years
    :type t: float
    :param r: risk-free interest rate
    :type r: float
  

    >>> S = 95
    >>> t = .5
    >>> r = .02
    >>> F = forward_price(S,t,r)
    >>> pre_calculated = 95.95476587299596
    >>> abs(F-pre_calculated)<.000000001
    True
    """
    return S/numpy.exp(-r*t)



# -----------------------------------------------------------------------------
# MAIN
if __name__=='__main__':
    import doctest
    if not doctest.testmod().failed:
        print "Doctest passed"
