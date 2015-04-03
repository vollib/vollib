# -----------------------------------------------------------------------------
# IMPORTS

# Standard library imports

# Related third party imports
import lets_be_rational
from scipy.optimize import brentq
import numpy

# Local application/library specific imports
from vollib.helper import forward_price
from vollib.black_scholes import black_scholes
from vollib.helper import binary_flag


e = numpy.e

# -----------------------------------------------------------------------------
# FUNCTIONS, FOR REFERENCE AND TESTING


def implied_volatility_brent(price, S, K, t, r, flag):

    """Calculate the Black-Scholes implied volatility
    using the Brent method.

    Keyword arguments:
    S -- spot price of the underlying asset
    K -- option strike price
    sigma -- annualized standard deviation, or volatility
    t -- time to expiration in years
    r -- the risk-free interest rate
    flag -- 'p' or 'c' for put or call
    
    
    >>> S = 100
    >>> K = 100
    >>> sigma = .2
    >>> r = .01
    >>> flag = 'c'
    >>> t = .5

    >>> price = black_scholes(flag, S, K, t, r, sigma)
    >>> iv = implied_volatility_brent(price, S, K, t, r, flag)

    >>> print price, iv
    5.87602423383 0.2
    """  

    def function_to_minimize(sigma):
        return price - black_scholes(flag, S, K, t, r, sigma)

    return brentq(function_to_minimize,0,10)  


def implied_volatility_limited_iterations(price, S, K, t, r, flag, N):

    """Calculate the Black-Scholes implied volatility with limited iterations.

    Keyword arguments:
    S -- spot price of the underlying asset
    K -- option strike price
    sigma -- annualized standard deviation, or volatility
    t -- time to expiration in years
    r -- the risk-free interest rate
    flag -- 'p' or 'c' for put or call
    N -- the maximum number of iterations to perform



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

    Keyword arguments:
    S -- spot price of the underlying asset
    K -- option strike price
    sigma -- annualized standard deviation, or volatility
    t -- time to expiration in years
    r -- the risk-free interest rate
    flag -- 'p' or 'c' for put or call
    
    
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