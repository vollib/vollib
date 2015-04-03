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

    Note about the parameter "b":
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    ::

      ======================================================================================
       from Espen Gaarder Haug's 
      "The Complete Guide to Option Pricing Formulas," Second Edition, 
      page 90.

      +-----------+------------------------------------------------------+
      | b = r     |  gives the Black and Scholes (1973) stock option     |
      |           |  model                                               |
      +-----------+------------------------------------------------------+
      | b = r -q  |  gives the Merton (1973) stock option model with     |
      |           |  continuous dividend yield q                         |
      +-----------+------------------------------------------------------+
      | b = 0     |  gives the Black (1976) futures option model         | 
      +-----------+------------------------------------------------------+
      | b = 0 and |  gives the Asay (1982) margined futures option model |
      | r = 0     |                                                      |
      +-----------+------------------------------------------------------+
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

def delta(flag, S, K, t, r, sigma, b, pricing_function):

    """Calculate option delta using numerical integration. 

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
        :param b: see above
        :type b: float 
        :param flag: 'c' or 'p' for call or put.
        :type flag: str
        :param pricing_function: any function returning the price of an option
        :type pricing_function: python function object

    """
    if t == 0.0:
        if S == K:
            return {'c':0.5, 'p':-0.5}[flag]
        elif S > K:
            return {'c':1.0, 'p':0.0}[flag]
        else:
            return {'c':0.0, 'p':-1.0}[flag]
    else:
        return (pricing_function(flag, S + dS, K, t, r, sigma, b) - \
                pricing_function(flag, S - dS, K, t, r, sigma, b)) / (2 * dS)

def theta(flag, S, K, t, r, sigma, b, pricing_function):

    """Calculate option theta using numerical integration. 

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
        :param b: see above
        :type b: float 
        :param flag: 'c' or 'p' for call or put.
        :type flag: str
        :param pricing_function: any function returning the price of an option
        :type pricing_function: python function object

    """



    if t <= 1. / 365.:
        return pricing_function(flag, S, K, 0.00001, r, sigma, b) - \
               pricing_function(flag, S, K, t, r, sigma, b)
    else:
        return pricing_function(flag, S, K, t - 1. / 365., r, sigma, b) - \
               pricing_function(flag, S, K, t, r, sigma, b)

def vega(flag, S, K, t, r, sigma, b, pricing_function):

    """Calculate option vega using numerical integration. 

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
        :param b: see above
        :type b: float 
        :param flag: 'c' or 'p' for call or put.
        :type flag: str
        :param pricing_function: any function returning the price of an option
        :type pricing_function: python function object

    """


    return (pricing_function(flag, S, K, t, r, sigma + 0.01, b) - \
            pricing_function(flag, S, K, t, r, sigma - 0.01, b)) / 2.

def rho(flag, S, K, t, r, sigma, b, pricing_function):

    """Calculate option rho using numerical integration. 

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
        :param b: see above
        :type b: float 
        :param flag: 'c' or 'p' for call or put.
        :type flag: str
        :param pricing_function: any function returning the price of an option
        :type pricing_function: python function object

    """


    return (pricing_function(flag, S, K, t, r + 0.01, sigma,  b ) - \
            pricing_function(flag, S, K, t, r - 0.01, sigma, b )) / (2)

def gamma(flag, S, K, t, r, sigma, b, pricing_function):


    """Calculate option gamma using numerical integration. 

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
        :param b: see above
        :type b: float 
        :param flag: 'c' or 'p' for call or put.
        :type flag: str
        :param pricing_function: any function returning the price of an option
        :type pricing_function: python function object

    """

    if t == 0:
        return POSINF if S == K else 0.0        

    return (pricing_function(flag, S + dS, K, t, r, sigma, b) - 2. * \
            pricing_function(flag, S, K, t, r, sigma, b) + \
            pricing_function(flag, S - dS, K, t, r, sigma, b)) / dS ** 2.
