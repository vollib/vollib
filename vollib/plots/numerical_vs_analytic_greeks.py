# -----------------------------------------------------------------------------
# IMPORTS

# Standard library imports


# Related third party imports
from matplotlib import pyplot as plt
import numpy

# Local application/library specific imports
from vollib.black_scholes import black_scholes
from vollib.black_scholes import python_black_scholes

from vollib.black_scholes.greeks.analytical import delta
from vollib.black_scholes.greeks.analytical import gamma
from vollib.black_scholes.greeks.analytical import theta
from vollib.black_scholes.greeks.analytical import vega
from vollib.black_scholes.greeks.analytical import rho

from vollib.black_scholes.greeks.numerical import delta as ndelta
from vollib.black_scholes.greeks.numerical import gamma as ngamma
from vollib.black_scholes.greeks.numerical import theta as ntheta
from vollib.black_scholes.greeks.numerical import vega as nvega
from vollib.black_scholes.greeks.numerical import rho as nrho



def plot_numerical_vs_analytical(greek, flag):
    
    """Displays a plot comparing analytically and numerically
    computed values of a given greek and option type.
    
    
    :param flag: 'd','g','t','r', or 'v'
    :type flag: str
    :param flag: 'c' or 'p' for call or put.
    :type flag: str
    
    
        """


    f_analytical, f_numerical = {
        'd':(delta,ndelta),
        'g':(gamma,ngamma),
        't':(theta,ntheta),
        'v':(vega,nvega),
        'r':(rho, nrho),
        }[greek]


    S_vals = numpy.linspace(10,250,2000)
    K=100
    t =.5
    q =.05
    sigma = 0.2
    r = .01


    price, analytical, numerical = [],[],[]


    for S in S_vals:
        analytical.append(f_analytical(flag, S, K, t, r, sigma))
        numerical.append(f_numerical(flag, S, K, t, r, sigma))
        price.append(black_scholes(flag, S, K, t, r, sigma))
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
 
#plot_numerical_vs_analytical('t','c')