# -*- coding: utf-8 -*-
"""
    vollib.black_scholes_merton
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

# Related third party imports


# Local application/library specific imports
from lets_be_rational import black
from lets_be_rational import norm_cdf as cnd
from vollib.helper import forward_price
from vollib.helper import binary_flag
from vollib.helper import pdf

# -----------------------------------------------------------------------------
# FUNCTIONS, FOR REFERENCE AND TESTING

def d1(S, K, t, r, sigma, q):
    
    """Calculate the d1 component of the Black-Scholes-Merton PDE.

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
    
    
    From Espen Haug, The Complete Guide To Option Pricing Formulas
    Page 4

    >>> S=100
    >>> K=95
    >>> q=.05
    >>> t = 0.5
    >>> r = 0.1
    >>> sigma = 0.2
    
    >>> d1_published_value = 0.6102
    >>> d1_calc = d1(S,K,t,r,sigma,q)
    >>> abs(d1_published_value - d1_calc) < 0.0001
    True
    
    """
    
    numerator = numpy.log(S/float(K)) + (r - q + sigma*sigma/2.0)*t
    denominator = sigma * numpy.sqrt(t)
    return numerator/denominator
    
    
def d2(S, K, t, r, sigma, q):
    
    """Calculate the d2 component of the Black-Scholes-Merton PDE.

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
    

    From Espen Haug, The Complete Guide To Option Pricing Formulas
    Page 4

    >>> S=100
    >>> K=95
    >>> q=.05
    >>> t = 0.5
    >>> r = 0.1
    >>> sigma = 0.2

    >>> d2_published_value = 0.4688
    >>> d2_calc = d2(S,K,t,r,sigma,q)
    >>> abs(d2_published_value - d2_calc) < 0.0001
    True

    """    
    
    return d1(S, K, t, r, sigma, q) - sigma*numpy.sqrt(t)


def bsm_call(S, K, t, r, sigma, q):

    """Return the Black-Scholes-Merton call price
    implemented in python (for reference).
    
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
    """
   
    D1 = d1(S, K, t, r, sigma, q)
    D2 = d2(S, K, t, r, sigma, q)    
    
    return S * numpy.exp(-q*t) * cnd(D1) - K * numpy.exp(-r*t) * cnd(D2)


def bsm_put(S, K, t, r, sigma, q):

    
    """Return the Black-Scholes-Merton put price
    implemented in python (for reference).

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
  
    
    
    From Espen Haug, The Complete Guide To Option Pricing Formulas
    Page 4

    >>> S=100
    >>> K=95
    >>> q=.05
    >>> t = 0.5
    >>> r = 0.1
    >>> sigma = 0.2

    >>> p_published_value = 2.4648
    >>> p_calc = bsm_put(S, K, t, r, sigma, q)
    >>> abs(p_published_value - p_calc) < 0.0001
    True

    """     
    
    D1 = d1(S, K, t, r, sigma, q)
    D2 = d2(S, K, t, r, sigma, q)
    return K * numpy.exp(-r*t) * cnd(-D2) - S * numpy.exp(-q*t) * cnd(-D1)



def python_black_scholes_merton(flag, S, K, t, r, sigma, q):
    
    """Return the Black-Scholes-Merton call price implemented in
    python (for reference).

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

    From Espen Haug, The Complete Guide To Option Pricing Formulas
    Page 4

    >>> S=100
    >>> K=95
    >>> q=.05
    >>> t = 0.5
    >>> r = 0.1
    >>> sigma = 0.2

    >>> p_published_value = 2.4648
    >>> p_calc = python_black_scholes_merton('p', S, K, t, r, sigma, q)
    >>> abs(p_published_value - p_calc) < 0.0001
    True

    >>> c1 = python_black_scholes_merton('c', S, K, t, r, sigma, q)
    >>> c2 = black_scholes_merton('c', S, K, t, r, sigma, q)
    >>> abs(c1-c2) < .0001
    True
    
    >>> p1 = python_black_scholes_merton('p', S, K, t, r, sigma, q)
    >>> p2 = black_scholes_merton('p', S, K, t, r, sigma, q)
    >>> abs(p1-p2) < .0001
    True
    
    """    
    
    if flag == 'c':
        return bsm_call(S, K, t, r, sigma, q)
    else:
        return bsm_put(S, K, t, r, sigma, q)




def black_scholes_merton(flag, S, K, t, r, sigma, q):

    """Return the Black-Scholes-Merton option price.

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

    From Espen Haug, The Complete Guide To Option Pricing Formulas
    Page 4

    >>> S=100
    >>> K=95
    >>> q=.05
    >>> t = 0.5
    >>> r = 0.1
    >>> sigma = 0.2

    >>> p_published_value = 2.4648
    >>> p_calc = black_scholes_merton('p', S, K, t, r, sigma, q)
    >>> abs(p_published_value - p_calc) < 0.0001
    True
    
    >>> c1 = bsm_call(S, K, t, r, sigma, q)
    >>> c2 = black_scholes_merton('c', S, K, t, r, sigma, q)
    >>> abs(c1-c2) < .0001
    True
    """
    
    S = S * numpy.exp((r-q)*t)
    p = black(S, K, sigma, t, binary_flag[flag])
    conversion_factor = numpy.exp(-r*t)
    return p * conversion_factor


# -----------------------------------------------------------------------------
# MAIN
if __name__=='__main__':
    import doctest
    if not doctest.testmod().failed:
        print "Doctest passed"
