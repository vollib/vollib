# -*- coding: utf-8 -*-
"""
    vollib.black_scholes.greeks.analytical
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
from vollib.black_scholes import d1,d2

# -----------------------------------------------------------------------------
# FUNCTIONS - ANALYTICAL GREEKS


def delta(flag, S, K, t, r, sigma):
    
    """Return Black-Scholes delta of an option.
    
    
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
    :param flag: 'c' or 'p' for call or put.
    :type flag: str      
    
    
    Example 17.1, page 355, Hull:
    
    >>> S = 49
    >>> K = 50 
    >>> r = .05
    >>> t = 0.3846
    >>> sigma = 0.2
    >>> flag = 'c'
    >>> delta_calc = delta(flag, S, K, t, r, sigma)
    >>> # 0.521601633972
    >>> delta_text_book = 0.522
    >>> abs(delta_calc - delta_text_book) < .01
    True
    """

    d_1 = d1(S, K, t, r, sigma)

    if flag == 'p':
        return cnd(d_1) - 1.0
    else:
        return cnd(d_1)


def theta(flag, S, K, t, r, sigma):

    """Return Black-Scholes theta of an option.
    
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
    :param flag: 'c' or 'p' for call or put.
    :type flag: str      
    
    
    The text book analytical formula does not divide by 365,
    but in practice theta is defined as the change in price
    for each day change in t, hence we divide by 365.

    Example 17.2, page 359, Hull:

    >>> S = 49
    >>> K = 50 
    >>> r = .05
    >>> t = 0.3846
    >>> sigma = 0.2
    >>> flag = 'c'
    >>> annual_theta_calc = theta(flag, S, K, t, r, sigma) * 365
    >>> # -4.30538996455
    >>> annual_theta_text_book = -4.31
    >>> abs(annual_theta_calc - annual_theta_text_book) < .01
    True
    
    
    Using the same inputs with a put.
    >>> S = 49
    >>> K = 50 
    >>> r = .05
    >>> t = 0.3846
    >>> sigma = 0.2
    >>> flag = 'p'
    >>> annual_theta_calc = theta(flag, S, K, t, r, sigma) * 365
    >>> # -1.8530056722
    >>> annual_theta_reference = -1.8530056722
    >>> abs(annual_theta_calc - annual_theta_reference) < .000001
    True
    
    
    """
    
    two_sqrt_t = 2 * numpy.sqrt(t)

    D1 = d1(S, K, t, r, sigma)
    D2 = d2(S, K, t, r, sigma)

    first_term = (-S * pdf(D1) * sigma) / two_sqrt_t 

    if flag == 'c':

        second_term = r * K * numpy.exp(-r*t) * cnd(D2)
        return (first_term - second_term)/365.0
    
    if flag == 'p':
    
        second_term = r * K * numpy.exp(-r*t) * cnd(-D2)
        return (first_term + second_term)/365.0


def gamma(flag, S, K, t, r, sigma):
    
    """Return Black-Scholes gamma of an option.
    
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
    :param flag: 'c' or 'p' for call or put.
    :type flag: str      
    
    Example 17.4, page 364, Hull:

    >>> S = 49
    >>> K = 50 
    >>> r = .05
    >>> t = 0.3846
    >>> sigma = 0.2
    >>> flag = 'c'
    >>> gamma_calc = gamma(flag, S, K, t, r, sigma)
    >>> # 0.0655453772525
    >>> gamma_text_book = 0.066
    >>> abs(gamma_calc - gamma_text_book) < .001
    True
    """
    

    d_1 = d1(S, K, t, r, sigma)
    v_squared = sigma**2
    return pdf(d_1)/(S*sigma*numpy.sqrt(t))


def vega(flag, S, K, t, r, sigma):

    """Return Black-Scholes vega of an option.
    
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
    :param flag: 'c' or 'p' for call or put.
    :type flag: str      
    
    
    The text book analytical formula does not multiply by .01,
    but in practice vega is defined as the change in price
    for each 1 percent change in IV, hence we multiply by 0.01.


    Example 17.6, page 367, Hull:
    
    >>> S = 49
    >>> K = 50 
    >>> r = .05
    >>> t = 0.3846
    >>> sigma = 0.2
    >>> flag = 'c'
    >>> vega_calc = vega(flag, S, K, t, r, sigma)
    >>> # 0.121052427542
    >>> vega_text_book = 0.121
    >>> abs(vega_calc - vega_text_book) < .01
    True

    """

    d_1 = d1(S, K, t, r, sigma)
    return S * pdf(d_1) * numpy.sqrt(t) * 0.01


def rho(flag, S, K, t, r, sigma):

    """Return Black-Scholes rho of an option.
    
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
    :param flag: 'c' or 'p' for call or put.
    :type flag: str      
    
    The text book analytical formula does not multiply by .01,
    but in practice rho is defined as the change in price
    for each 1 percent change in r, hence we multiply by 0.01.


    Example 17.7, page 368, Hull:

    >>> S = 49
    >>> K = 50 
    >>> r = .05
    >>> t = 0.3846
    >>> sigma = 0.2
    >>> flag = 'c'
    >>> rho_calc = rho(flag, S, K, t, r, sigma)
    >>> # 0.089065740988
    >>> rho_text_book = 0.0891
    >>> abs(rho_calc - rho_text_book) < .0001
    True

    """

    d_2 = d2(S, K, t, r, sigma)
    e_to_the_minus_rt = numpy.exp(-r*t)
    if flag == 'c':
        return t*K*e_to_the_minus_rt * cnd(d_2) * .01
    else:
        return -t*K*e_to_the_minus_rt * cnd(-d_2) * .01


# -----------------------------------------------------------------------------
# MAIN
if __name__=='__main__':  
    import doctest
    if not doctest.testmod().failed:
        print "Doctest passed"
