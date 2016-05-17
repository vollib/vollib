# -*- coding: utf-8 -*-
"""
    vollib.black_scholes_merton.implied_volatility
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Copyright © 2015 Iota Technologies Pte Ltd

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
from lets_be_rational import implied_volatility_from_a_transformed_rational_guess as iv
import numpy

# Local application/library specific imports
from vollib.helper import forward_price
from vollib.black_scholes_merton import black_scholes_merton
from vollib.black_scholes_merton import python_black_scholes_merton
from vollib.helper import binary_flag

# -----------------------------------------------------------------------------
# FUNCTIONS, FOR REFERENCE AND TESTING


# -----------------------------------------------------------------------------
# FUNCTIONS


def implied_volatility(price, S, K, t, r, q, flag):


    """Calculate the Black-Scholes-Merton implied volatility.


    :param S: underlying asset price
    :type S: float
    :param K: strike price
    :type K: float
    :param sigma: annualized standard deviation, or volatility
    :type sigma: float
    :param t: time to expiration in years
    :type t: float
    :param r: risk-free interest rate
    :type r: float
    :param q: annualized continuous dividend rate
    :type q: float 
    :param flag: 'c' or 'p' for call or put.
    :type flag: str
    
    
    >>> S = 100
    >>> K = 100
    >>> sigma = .2
    >>> r = .01
    >>> flag = 'c'
    >>> t = .5
    >>> q = .02
    
    >>> reference_price = python_black_scholes_merton(flag, S, K, t, r, sigma, q)
    >>> price = black_scholes_merton(flag, S, K, t, r, sigma, q)

    >>> abs(reference_price - price) < .00000001
    True
    >>> iv = implied_volatility(price, S, K, t, r, q, flag)

    """  
    conversion_factor = numpy.exp(-r*t)
    adjusted_price = price / conversion_factor
    S = S * numpy.exp((r-q)*t)
    return iv(adjusted_price, S, K, t, binary_flag[flag])
    
# -----------------------------------------------------------------------------
# MAIN
if __name__=='__main__':
    import doctest
    if not doctest.testmod().failed:
        print "Doctest passed"
