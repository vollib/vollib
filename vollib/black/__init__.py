# -*- coding: utf-8 -*-
"""
    vollib.black
    ~~~~~~~~~~~~~~~~
    
    Copyright © 2015 
    
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
from math import e
from math import log, sqrt

# Related third party imports
import lets_be_rational
import numpy
from numpy import log, sqrt, exp


# Local application/library specific imports
from vollib.helper import binary_flag
from vollib.helper import pdf
from lets_be_rational import norm_cdf as cnd

# -----------------------------------------------------------------------------
# FUNCTIONS - INTERNAL, FOR COMPARISON

'''
From John C. Hull, "Options, Futures and Other Derivatives," 
7th edition, Chapter 16.8, page 342
'''

def d1(F, K, t, r, sigma): # keep r argument for consistency
    
    """Calculate the d1 component of the Black PDE.

    :param F: underlying futures price
    :type F: float
    :param K: strike price
    :type K: float
    :param sigma: annualized standard deviation, or volatility
    :type sigma: float
    :param t: time to expiration in years
    :type t: float
    :param r: risk-free interest rate
    :type r: float  
        
        
    Doctest using Hull, page 343, example 16.6
    
    >>> F = 20
    >>> K = 20
    >>> r = .09
    >>> t = 4/12.0
    >>> sigma = 0.25
    
    >>> calculated_value = d1(F, K, t, r, sigma) 
    >>> #0.0721687836487
    >>> text_book_value = 0.07216
    >>> abs(calculated_value - text_book_value) < .00001
    True
    """

    sigma_squared = sigma*sigma
    numerator = log(F/float(K)) + sigma_squared*t/2.0
    denominator = sigma*sqrt(t)

    return numerator/denominator

def d2(F, K, t, r, sigma): # keep r argument for consistency
    
    """Calculate the d2 component of the Black PDE.

    :param F: underlying futures price
    :type F: float
    :param K: strike price
    :type K: float
    :param sigma: annualized standard deviation, or volatility
    :type sigma: float
    :param t: time to expiration in years
    :type t: float
    :param r: risk-free interest rate
    :type r: float    
    
    Hull, page 343, example 16.6

    >>> F = 20
    >>> K = 20
    >>> r = .09
    >>> t = 4/12.0
    >>> sigma = 0.25

    >>> calculated_value = d2(F, K, t, r, sigma) 
    >>> #-0.0721687836487
    >>> text_book_value = -0.07216
    >>> abs(calculated_value - text_book_value) < .00001
    True
    """
    
    return d1(F, K, t, r, sigma) - sigma*sqrt(t)


def black_call(F, K, t, r, sigma):  #Equation 16.9
    

    """Calculate the price of a call using Black.  (Python
    implementation for reference.)

    :param F: underlying futures price
    :type F: float
    :param K: strike price
    :type K: float
    :param sigma: annualized standard deviation, or volatility
    :type sigma: float
    :param t: time to expiration in years
    :type t: float
    :param r: risk-free interest rate
    :type r: float    
    
    
    
    Hull, page 343, example 16.7
    
    >>> F = 620
    >>> K = 600
    >>> r = .05
    >>> sigma = .2
    >>> t = 0.5
    >>> calculated_value = black_call(F, K, t, r, sigma)
    >>> #44.1868533121
    >>> text_book_value = 44.19
    >>> abs(calculated_value - text_book_value) < .01
    True
    """
    
    e_to_the_minus_rt = numpy.exp(-r*t)
    N_d1 = cnd(d1(F, K, t, r, sigma))
    N_d2 = cnd(d2(F, K, t, r, sigma))
    
    return e_to_the_minus_rt * (F * N_d1 - K * N_d2) 

def black_put(F, K, t, r, sigma):  #Equation 16.10


    """Calculate the price of a put using Black.  (Python
    implementation for reference.)

    :param F: underlying futures price
    :type F: float
    :param K: strike price
    :type K: float
    :param sigma: annualized standard deviation, or volatility
    :type sigma: float
    :param t: time to expiration in years
    :type t: float
    :param r: risk-free interest rate
    :type r: float        
    
    
    Hull, page 338, example 16.6

    >>> F = 20
    >>> K = 20
    >>> r = .09
    >>> sigma = .25
    >>> t = 4/12.0
    >>> calculated_value = black_put(F, K, t, r, sigma)
    >>> # 1.11664145656
    >>> text_book_value = 1.12
    >>> abs(calculated_value - text_book_value) < .01
    True
    """
    e_to_the_minus_rt = numpy.exp(-r*t)
    N_of_minus_d1 = cnd(-d1(F, K, t, r, sigma))
    N_of_minus_d2 = cnd(-d2(F, K, t, r, sigma))

    return e_to_the_minus_rt * ( -F * N_of_minus_d1 + K * N_of_minus_d2)


# -----------------------------------------------------------------------------
# FUNCTIONS - FROM LETS_BE_RATIONAL

def undiscounted_black(F, K, sigma, t, flag):

    """Calculate the **undiscounted** Black option price.

    :param F: underlying futures price
    :type F: float
    :param K: strike price
    :type K: float
    :param sigma: annualized standard deviation, or volatility
    :type sigma: float
    :param t: time to expiration in years
    :type t: float   

    >>> F = 100
    >>> K = 100
    >>> sigma = .2
    >>> flag = 'c'
    >>> t = .5
    >>> undiscounted_black(F, K, sigma, t, flag)
    5.637197779701664
    
    """

    q = binary_flag[flag]
    F = float(F)
    K = float(K)
    sigma = float(sigma)
    t = float(t)
    
    return lets_be_rational.black(F, K, sigma, t, q)


def black(flag, F, K, t, r, sigma):
    
    """Calculate the (discounted) Black option price.

    :param F: underlying futures price
    :type F: float
    :param K: strike price
    :type K: float
    :param sigma: annualized standard deviation, or volatility
    :type sigma: float
    :param t: time to expiration in years
    :type t: float  
        
    >>> F = 100
    >>> K = 100
    >>> sigma = .2
    >>> flag = 'c'
    >>> r = .02
    >>> t = .5
    >>> black(flag, F, K, t, r, sigma)
    5.5811067246048118

    """
    
    discount_factor = e_to_the_minus_rt = numpy.exp(-r*t)        
    return undiscounted_black(F, K, sigma, t, flag) * discount_factor
    


def normalised_black(x, s, flag):

    """Calculate the normalised Black value,
    a time invariant transformation
    of the Black pricing formula.

    :param x: ln(F/K) where K is the strike price, and F is the futures price
    :type x: float
    :param s: volatility times the square root of time to expiration
    :type s: float
    :param flag: 'p' or 'c' for put or call 
    :type flag: str   
    
    >>> F = 100.
    >>> K = 95.
    >>> x = log(F/K)
    >>> t = 0.5
    >>> v = 0.3
    >>> s = v * sqrt(t)    
    
    >>> normalised_black(x,s,'p')
    0.061296663817558904
    
    >>> normalised_black(x,s,'c')
    0.11259558142181655
    
    """

    q = binary_flag[flag]
    
    return lets_be_rational.normalised_black(x, s, q)


def test_python_vs_c_values():
    
    #comment
    
    """
    >>> F = 100
    >>> K = 90
    >>> sigma = .2
    >>> flag = 'c'
    >>> r = .02
    >>> t = .5
    
    >>> epsilon = .000000001
    
    >>> v1 = black('c', F, K, t, r, sigma)
    >>> v2 = black_call(F, K, t, r, sigma)
    
    >>> print abs(v1-v2) < epsilon
    True
    
    
    >>> v1 = black('p', F, K, t, r, sigma)
    >>> v2 = black_put(F, K, t, r, sigma)
    >>> print abs(v1-v2) < epsilon
    True
    """
    pass



# -----------------------------------------------------------------------------
# MAIN
if __name__=='__main__':
    import doctest
    if not doctest.testmod().failed:
        print "Doctest passed"
