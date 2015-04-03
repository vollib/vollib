# -*- coding: utf-8 -*-
"""
    vollib.black_scholes_merton.greeks.analytical
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
import numpy

# Local application/library specific imports
from lets_be_rational import norm_cdf as cnd
from vollib.helper import pdf
from vollib.black_scholes_merton import d1,d2

# -----------------------------------------------------------------------------
# FUNCTIONS - ANALYTICAL GREEKS
# -----------------------------------------------------------------------------
# IMPORTS

# Standard library imports


# Related third party imports
import numpy

# Local application/library specific imports
from lets_be_rational import norm_cdf as cnd
from vollib.helper import pdf
from vollib.black_scholes_merton import d1,d2, black_scholes_merton


# -----------------------------------------------------------------------------
# FUNCTIONS - ANALYTICAL GREEKS


def delta(flag, S, K, t, r, sigma, q):
    
    """Returns the Black-Scholes-Merton delta of an option.
    

    :param flag: 'c' or 'p' for call or put.
    :type flag: str
    :param S: underlying asset price
    :type S: float
    :param K: strike price
    :type K: float
    :param t: time to expiration in years
    :type t: float
    :param r: annual risk-free interest rate
    :type r: float
    :param sigma: volatility
    :type sigma: float
    :param q: annualized continuous dividend yield
    :type q: float
    
    :returns:  float 

    """

    D1 = d1(S, K, t, r, sigma, q)

    if flag == 'p':
        return -numpy.exp(-q*t) * cnd(-D1)
    else:
        return numpy.exp(-q*t) * cnd(D1)


def theta(flag, S, K, t, r, sigma, q):

    """Returns the Black-Scholes-Merton theta of an option.


    :param flag: 'c' or 'p' for call or put.
    :type flag: str
    :param S: underlying asset price
    :type S: float
    :param K: strike price
    :type K: float
    :param t: time to expiration in years
    :type t: float
    :param r: annual risk-free interest rate
    :type r: float
    :param sigma: volatility
    :type sigma: float
    :param q: annualized continuous dividend yield
    :type q: float

    :returns:  float 

    """


    D1 = d1(S, K, t, r, sigma, q)
    D2 = d2(S, K, t, r, sigma, q)

    first_term = (S * numpy.exp(-q*t) * pdf(D1) * sigma) / (2 * numpy.sqrt(t))

    if flag == 'c':

        second_term = -q * S * numpy.exp(-q*t) * cnd(D1)
        third_term = r * K * numpy.exp(-r*t) * cnd(D2)

        return - (first_term + second_term + third_term) / 365.0

    else:

        second_term = -q * S * numpy.exp(-q*t) * cnd(-D1)
        third_term = r * K * numpy.exp(-r*t) * cnd(-D2)

        return (-first_term + second_term + third_term) / 365.0



def gamma(flag, S, K, t, r, sigma, q):


    """Returns the Black-Scholes-Merton gamma of an option.


    :param flag: 'c' or 'p' for call or put.
    :type flag: str
    :param S: underlying asset price
    :type S: float
    :param K: strike price
    :type K: float
    :param t: time to expiration in years
    :type t: float
    :param r: annual risk-free interest rate
    :type r: float
    :param sigma: volatility
    :type sigma: float
    :param q: annualized continuous dividend yield
    :type q: float

    :returns:  float 

    """

    D1 = d1(S, K, t, r, sigma, q)
    numerator = numpy.exp(-q*t) * pdf(D1)
    denominator = S * sigma * numpy.sqrt(t)

    return numerator / denominator


def vega(flag, S, K, t, r, sigma, q):

    """Returns the Black-Scholes-Merton vega of an option.


    :param flag: 'c' or 'p' for call or put.
    :type flag: str
    :param S: underlying asset price
    :type S: float
    :param K: strike price
    :type K: float
    :param t: time to expiration in years
    :type t: float
    :param r: annual risk-free interest rate
    :type r: float
    :param sigma: volatility
    :type sigma: float
    :param q: annualized continuous dividend yield
    :type q: float

    :returns:  float 

    """

    D1 = d1(S, K, t, r, sigma, q)

    return S * numpy.exp(-q*t) * pdf(D1) * numpy.sqrt(t) * 0.01


def rho(flag, S, K, t, r, sigma, q):


    """Returns the Black-Scholes-Merton rho of an option.


    :param flag: 'c' or 'p' for call or put.
    :type flag: str
    :param S: underlying asset price
    :type S: float
    :param K: strike price
    :type K: float
    :param t: time to expiration in years
    :type t: float
    :param r: annual risk-free interest rate
    :type r: float
    :param sigma: volatility
    :type sigma: float
    :param q: annualized continuous dividend yield
    :type q: float

    :returns:  float 

    """


    D2 = d2(S, K, t, r, sigma, q)

    if flag == 'c':

        return t * K * numpy.exp(-r*t) * cnd(D2) * .01

    else:

        return -t * K * numpy.exp(-r*t) * cnd(-D2) * .01


# -----------------------------------------------------------------------------
# MAIN
if __name__=='__main__':  
    import doctest
    if not doctest.testmod().failed:
        print "Doctest passed"
        



