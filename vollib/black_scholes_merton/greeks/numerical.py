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
import numpy

# Related third party imports
from matplotlib import pyplot as plt

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


def plot_numerical_vs_analytical(greek, flag):
    
    """Displays a plot comparing analytically and numerically
    computed values of a given greek and option type.
    
    
    :param flag: 'd','g','t','r', or 'v'
    :type flag: str
    :param flag: 'c' or 'p' for call or put.
    :type flag: str
    
    
        """


    f_analytical, f_numerical = {
        'd':(adelta,delta),
        'g':(agamma,gamma),
        't':(atheta,theta),
        'v':(avega,vega),
        'r':(arho, rho),
        }[greek]


    S_vals = numpy.linspace(10,250,2000)
    K=100
    t =.5
    q =.05
    sigma = 0.2
    r = .01


    price, analytical, numerical = [],[],[]


    for S in S_vals:
        analytical.append(f_analytical(flag, S, K, t, r, sigma, q))
        numerical.append(f_numerical(flag, S, K, t, r, sigma, q))
        price.append(black_scholes_merton(flag, S, K, t, r, sigma, q))
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


#plot_numerical_vs_analytical('v','c')




# -----------------------------------------------------------------------------
# MAIN
if __name__=='__main__':  
    print 'running doctests'
    import doctest
    if not doctest.testmod().failed:
        print "Doctest passed"
