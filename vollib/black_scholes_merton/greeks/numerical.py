# -*- coding: utf-8 -*-
"""
    vollib.black_scholes_merton.greeks.numerical
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
from vollib.black_scholes_merton import black_scholes_merton

# numerical greeks
from vollib.helper.numerical_greeks import delta as numerical_delta
from vollib.helper.numerical_greeks import vega as numerical_vega
from vollib.helper.numerical_greeks import theta as numerical_theta
from vollib.helper.numerical_greeks import rho as numerical_rho
from vollib.helper.numerical_greeks import gamma as numerical_gamma

# analytical greeks
from vollib.black_scholes_merton.greeks.analytical import gamma as agamma
from vollib.black_scholes_merton.greeks.analytical import delta as adelta
from vollib.black_scholes_merton.greeks.analytical import vega as avega
from vollib.black_scholes_merton.greeks.analytical import rho as arho
from vollib.black_scholes_merton.greeks.analytical import theta as atheta

# -----------------------------------------------------------------------------
# FUNCTIONS - NUMERICAL GREEK CALCULATION

f = lambda flag, S, K, t, r, sigma, q: black_scholes_merton(flag, S, K, t, r, sigma, q)

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


    return numerical_delta(flag, S, K, t, r, sigma, q, f)

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

    return numerical_theta(flag, S, K, t, r, sigma, q, f)

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
    return numerical_vega(flag, S, K, t, r, sigma, q, f)

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
    return numerical_rho(flag, S, K, t, r, sigma, q, f)

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
    return numerical_gamma(flag, S, K, t, r, sigma, q, f)


plot_numerical_vs_analytical('t','p')




# -----------------------------------------------------------------------------
# MAIN
if __name__=='__main__':  
    print 'running doctests'
    import doctest
    if not doctest.testmod().failed:
        print "Doctest passed"
