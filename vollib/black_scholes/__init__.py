# -----------------------------------------------------------------------------
# IMPORTS

# Standard library imports
from math import e

# Related third party imports
import numpy

# Local application/library specific imports
from vollib.helper import forward_price
from vollib.black import black as vollib_black
from vollib.black import undiscounted_black
from vollib.helper import pdf
from lets_be_rational import norm_cdf as cnd

# -----------------------------------------------------------------------------
# FUNCTIONS - REFERENCE PYTHON IMPLEMENTATION, FOR COMPARISON


def d1(S,K,t,r,sigma):  # see Hull, page 292
    
    """
    John C. Hull, "Options, Futures and Other Derivatives," 
    7th edition, Example 13.6, page 294
    
    >>> S = 42
    >>> K = 40
    >>> r = .10
    >>> sigma = .20
    >>> t = 0.5
    >>> calculated_d1 = d1(S,K,t,r,sigma)
    >>> text_book_d1 = 0.7693
    >>> abs(calculated_d1 - text_book_d1) < 0.0001
    True
    """

    sigma_squared = sigma*sigma
    numerator = numpy.log( S/float(K) ) + ( r + sigma_squared/2.) * t
    denominator = sigma * numpy.sqrt(t)

    return numerator/denominator

def d2(S,K,t,r,sigma):  # see Hull, page 292

    """
    John C. Hull, "Options, Futures and Other Derivatives," 
    7th edition, Example 13.6, page 294

    >>> S = 42
    >>> K = 40
    >>> r = .10
    >>> sigma = .20
    >>> t = 0.5
    >>> calculated_d2 = d2(S,K,t,r,sigma) #0.627841271869
    >>> text_book_d2 = 0.6278
    >>> abs(calculated_d2 - text_book_d2) < 0.0001
    True
    """
    
    return d1(S, K, t, r, sigma) - sigma*numpy.sqrt(t)

def python_black_scholes(flag, S, K, t, r, sigma):
    
    """
    >>> S,K,t,r,sigma = 60,65,.25,.08,.3
    >>> c1 = black_scholes('c',S,K,t,r,sigma) 
    >>> c2 = python_black_scholes('c',S,K,t,r,sigma)    
    >>> abs(c1 - c2) < .00001
    True
    >>> abs(c1 - 2.13336844492) < .00001
    True
    """
    

    e_to_the_minus_rt = numpy.exp(-r*t)
    D1 = d1(S, K, t, r, sigma)
    D2 = d2(S, K, t, r, sigma)
    if flag == 'c':
        return S * cnd(D1) - K * e_to_the_minus_rt * cnd(D2)
    else:
        return - S * cnd(-D1) + K * e_to_the_minus_rt * cnd(-D2)

# -----------------------------------------------------------------------------
# FUNCTIONS 

def black_scholes(flag, S, K, t, r, sigma): 

    """Calculate the Black-Scholes option price.

    Keyword arguments:
    S -- the underlying asset (spot) price
    K -- option strike price
    sigma -- annualized standard deviation, or volatility
    t -- time to expiration in years
    r -- the risk-free interest rate
    flag -- 'p' or 'c' for put or call
    
    >>> c = black_scholes('c',100,90,.5,.01,.2) 
    >>> abs(c - 12.111581435) < .000001
    True

    >>> p = black_scholes('p',100,90,.5,.01,.2) 
    >>> abs(p - 1.66270456231) < .000001
    True
    
    >>> flag, S, K, t, r, sigma = 'c',100,90,.5,.01,.2
    >>> c = black_scholes(flag, S, K, t, r, sigma) 
    >>> python_c = python_black_scholes(flag, S, K, t, r, sigma)
    >>> abs(c - python_c) < .000001
    True


    >>> flag, S, K, t, r, sigma = 'p',100,90,.5,.01,.2
    >>> p = black_scholes(flag, S, K, t, r, sigma) 
    >>> python_p = python_black_scholes(flag, S, K, t, r, sigma)
    >>> abs(p - python_p) < .000001
    True
    
    """   
    
    discount_factor = numpy.exp(-r*t)
    F = S / discount_factor
    return undiscounted_black(F, K, sigma, t, flag) * discount_factor

# -----------------------------------------------------------------------------
# MAIN
if __name__=='__main__':  
    import doctest
    if not doctest.testmod().failed:
        print "Doctest passed"
