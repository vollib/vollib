# -----------------------------------------------------------------------------
# IMPORTS

# Standard library imports

# Related third party imports
import numpy
from matplotlib import pyplot as plt
from scipy.optimize import brent

# Local application/library specific imports
from vollib.black import black

# -----------------------------------------------------------------------------
# FUNCTIONS - IMPLIED UNDERLYING PRICE AND INTEREST RATE

def find_r_and_F(K,C,P,t):
    
    """
    We assume that the interest rate r and futures price F
    are unknown, and all we know is are the option prices
    and the time till expiration t.
    We seek r as the value which minimizes the standard 
    deviation of the resultant futures prices, calculated
    per strike as F = (C-P)/e^-rt + K.
    
    >>> K,C,P,t = make_test_data(100, .2, .015, .5, 0.0)
    >>> r, F = find_r_and_F(K, C, P, t)
    >>> abs(r - .015) <.000001
    True
    >>> abs(F - 100) <.000001
    True
    
    """

    def function_to_minimize(r):
        e_to_the_minus_rt = numpy.exp(-r*t)
        F = []
        for i in range(len(K)):
            F.append(
                C[i]/e_to_the_minus_rt - P[i]/e_to_the_minus_rt + K[i]
            )
        return numpy.std(F)

    r = brent(function_to_minimize)
    e_to_the_minus_rt = numpy.exp(-r*t)
    F =[]
    for i in range(len(K)):
        F.append(
            C[i]/e_to_the_minus_rt - P[i]/e_to_the_minus_rt + K[i]
        )
    F_mean = numpy.average(F)
    return r, F_mean

# -----------------------------------------------------------------------------
# FUNCTIONS - TEST

def make_test_data(F, sigma, r, t, noise):
    
    '''
    Returns a test option chain with up to 100 strikes 
    surrounding the futures price F.
    '''
    
    K= range(max(1,F-50),F+50)
    
    calls, puts = [],[]

    for Ki in K:
        P, C = black(F, Ki, sigma, r, t, 'p'), black(F, Ki, sigma,r, t,'c')
        P += numpy.random.rand() * noise * numpy.random.choice([-1,1])
        C += numpy.random.rand() * noise * numpy.random.choice([-1,1])
        calls.append(C)
        puts.append(P)

    return K, calls, puts, t


def plot_error():
    r = .03
    F = 100
    noise = numpy.linspace(0,2,1000)
    r_error, F_error = [],[]
    for n in noise:
        K, C, P, t = make_test_data(
            F=F, sigma=0.3, r=r, t=.5, noise=n)
        r_estimate, F_estimate = find_r_and_F(K, C, P, t)
        r_error.append(r_estimate-r)
        F_error.append(F_estimate-F)
    
    plt.title('Option Implied Futures Price')
    plt.plot(noise,r_error,label = 'r error', color = 'red')
    plt.plot(noise,F_error, label = 'F error',alpha = 0.6)
    plt.legend(loc = 'best')
    plt.grid()
    plt.ylim(-.2,.2)
    plt.xlabel('noise amount')
    plt.ylabel('error')
    plt.show()
plot_error()

# -----------------------------------------------------------------------------
# MAIN
if __name__=='__main__':
    import doctest
    if not doctest.testmod().failed:
        print "Doctest passed"
