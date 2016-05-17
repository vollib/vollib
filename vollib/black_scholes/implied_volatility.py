# -*- coding: utf-8 -*-
"""
    vollib.black_scholes.implied_volatility
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
import lets_be_rational

import numpy

# Local application/library specific imports
from vollib.helper import forward_price
from vollib.black_scholes import black_scholes
from vollib.helper import binary_flag


e = numpy.e

# -----------------------------------------------------------------------------
# FUNCTIONS, FOR REFERENCE AND TESTING





def implied_volatility_limited_iterations(price, S, K, t, r, flag, N):

    """Calculate the Black-Scholes implied volatility with limited iterations.

    :param price: the Black-Scholes option price
    :type price: float
    :param S: underlying asset price
    :type S: float
    :param K: strike price
    :type K: float
    :param t: time to expiration in years
    :type t: float
    :param r: risk-free interest rate
    :type r: float
    :param flag: 'c' or 'p' for call or put.
    :type flag: str  
    :param N: the maximum number of iterations to perform
    :type N: int

    >>> S = 100
    >>> K = 100
    >>> sigma = .232323232
    >>> r = .01
    >>> flag = 'c'
    >>> t = .5

    >>> price = black_scholes(flag, S, K, t, r, sigma)
    >>> iv = implied_volatility_limited_iterations(price, S, K, t, r, flag,1)

    >>> print price, iv    
    6.78242400926 0.232323232
    """  

    adjusted_price = price / e**(-r*t)

    return lets_be_rational.implied_volatility_from_a_transformed_rational_guess_with_limited_iterations(
        adjusted_price, 
        forward_price(S, t, r), 
        K, 
        t, 
        binary_flag[flag],
        N
    )


# -----------------------------------------------------------------------------
# FUNCTIONS


def implied_volatility(price, S, K, t, r, flag):


    """Calculate the Black-Scholes implied volatility.

    :param price: the Black-Scholes option price
    :type price: float
    :param S: underlying asset price
    :type S: float
    :param K: strike price
    :type K: float
    :param t: time to expiration in years
    :type t: float
    :param r: risk-free interest rate
    :type r: float
    :param flag: 'c' or 'p' for call or put.
    :type flag: str 
    
    >>> S = 100
    >>> K = 100
    >>> sigma = .2
    >>> r = .01
    >>> flag = 'c'
    >>> t = .5

    >>> price = black_scholes(flag, S, K, t, r, sigma)
    >>> iv = implied_volatility(price, S, K, t, r, flag)

    >>> print price, iv
    5.87602423383 0.2
    """  

    adjusted_price = price / e**(-r*t)

    return lets_be_rational.implied_volatility_from_a_transformed_rational_guess(
        adjusted_price, 
        forward_price(S, t, r), 
        K, 
        t, 
        binary_flag[flag]
    )
    
# -----------------------------------------------------------------------------
# MAIN
if __name__=='__main__':
    import doctest
    if not doctest.testmod().failed:
        print "Doctest passed"