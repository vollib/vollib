# -*- coding: utf-8 -*-
"""
    vollib.black.greeks.numerical
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



import numpy
from matplotlib import pyplot as plt
from vollib.black import black
from vollib.helper.numerical_greeks import delta as numerical_delta
from vollib.helper.numerical_greeks import vega as numerical_vega
from vollib.helper.numerical_greeks import theta as numerical_theta
from vollib.helper.numerical_greeks import rho as numerical_rho
from vollib.helper.numerical_greeks import gamma as numerical_gamma

from vollib.black.greeks.analytical import gamma as agamma
from vollib.black.greeks.analytical import delta as adelta
from vollib.black.greeks.analytical import vega as avega
from vollib.black.greeks.analytical import rho as arho
from vollib.black.greeks.analytical import theta as atheta

f = lambda flag, F, K, t, r, sigma, b: black(flag, F, K, t, r, sigma)

def delta(flag, F, K, t, r, sigma):
    
    """Returns the Black delta of an option.

    :param flag: 'c' or 'p' for call or put.
    :type flag: str
    :param F: underlying futures price
    :type F: float
    :param K: strike price
    :type K: float
    :param t: time to expiration in years
    :type t: float
    :param r: annual risk-free interest rate
    :type r: float
    :param sigma: volatility
    :type sigma: float

    :returns:  float 
    """    
    
    
    b = 0
    
    return numerical_delta(flag, F, K, t, r, sigma, b, f)

def theta(flag, F, K, t, r, sigma):

    """Returns the Black theta of an option.

    :param flag: 'c' or 'p' for call or put.
    :type flag: str
    :param F: underlying futures price
    :type F: float
    :param K: strike price
    :type K: float
    :param t: time to expiration in years
    :type t: float
    :param r: annual risk-free interest rate
    :type r: float
    :param sigma: volatility
    :type sigma: float

    :returns:  float 
    """   


    b = 0

    return numerical_theta(flag, F, K, t, r, sigma, b, f)

def vega(flag, F, K, t, r, sigma):


    """Returns the Black vega of an option.

    :param flag: 'c' or 'p' for call or put.
    :type flag: str
    :param F: underlying futures price
    :type F: float
    :param K: strike price
    :type K: float
    :param t: time to expiration in years
    :type t: float
    :param r: annual risk-free interest rate
    :type r: float
    :param sigma: volatility
    :type sigma: float

    :returns:  float 
    """   
    
    b = 0

    return numerical_vega(flag, F, K, t, r, sigma, b, f)

def rho(flag, F, K, t, r, sigma):

    """Returns the Black rho of an option.

    :param flag: 'c' or 'p' for call or put.
    :type flag: str
    :param F: underlying futures price
    :type F: float
    :param K: strike price
    :type K: float
    :param t: time to expiration in years
    :type t: float
    :param r: annual risk-free interest rate
    :type r: float
    :param sigma: volatility
    :type sigma: float

    :returns:  float 
    """   

    b = 0

    return numerical_rho(flag, F, K, t, r, sigma, b, f)

def gamma(flag, F, K, t, r, sigma):

    """Returns the Black gamma of an option.

    :param flag: 'c' or 'p' for call or put.
    :type flag: str
    :param F: underlying futures price
    :type F: float
    :param K: strike price
    :type K: float
    :param t: time to expiration in years
    :type t: float
    :param r: annual risk-free interest rate
    :type r: float
    :param sigma: volatility
    :type sigma: float

    :returns:  float 
    """   

    b = 0

    return numerical_gamma(flag, F, K, t, r, sigma, b, f)



def test():
    
    '''Tests by comparing the analytical and numerical greek values.
    
    >>> S =  49
    >>> K = 50 
    >>> r = .05
    >>> t = 0.3846
    >>> sigma = 0.2
    >>> flag = 'c'

    >>> epsilon = .0001

    >>> v1 = delta(flag, S, K, t, r, sigma)
    >>> v2 = adelta(flag, S, K, t, r, sigma)
    >>> abs(v1-v2)<epsilon
    True

    >>> v1 = gamma(flag, S, K, t, r, sigma)
    >>> v2 = agamma(flag, S, K, t, r, sigma)
    >>> abs(v1-v2)<epsilon
    True

    >>> v1 = rho(flag, S, K, t, r, sigma)
    >>> v2 = arho(flag, S, K, t, r, sigma)
    >>> abs(v1-v2)<epsilon
    True

    >>> v1 = vega(flag, S, K, t, r, sigma)
    >>> v2 = avega(flag, S, K, t, r, sigma)
    >>> abs(v1-v2)<epsilon
    True

    >>> v1 = theta(flag, S, K, t, r, sigma)
    >>> v2 = atheta(flag, S, K, t, r, sigma)
    >>> abs(v1-v2)<epsilon
    True
    '''
    pass



def plot_numerical_vs_analytical(greek, flag):

    f_analytical, f_numerical = {
    'd':(adelta,delta),
    'g':(agamma,gamma),
    't':(atheta,theta),
    'v':(avega,vega),
    'r':(arho, rho),
    }[greek]


    S_vals = numpy.linspace(10,250,2000)
    K = 100
    t = 1.0
    r = .1
    sigma = 0.3


    price, analytical, numerical = [],[],[]
    
    
    for S in S_vals:
        analytical.append(f_analytical(flag, S, K, t, r, sigma))
        numerical.append(f_numerical(flag, S, K, t, r, sigma))
        price.append(black(flag, S, K, t, r, sigma))
    plt.figure(1)
    plt.subplot(211)
    plt.plot(S_vals,analytical,label = 'Analytical')
    plt.plot(S_vals,numerical, label = 'Numerical')
    min_a, max_a = min(analytical), max(analytical)
    h = max_a-min_a
    plt.ylim(min_a - h*.05, max_a + h*.05)
    plt.grid()
    plt.legend(loc = 'best')
    
    plt.subplot(212)
    plt.plot(S_vals,price, label = 'Price')
    plt.ylim(min(min(price),-10), max(max(price),10))
    plt.grid()
    plt.legend(loc = 'best')


    plt.show()
    


# -----------------------------------------------------------------------------
# MAIN
if __name__=='__main__':  
    import doctest
    if not doctest.testmod().failed:
        print "Doctest passed"
