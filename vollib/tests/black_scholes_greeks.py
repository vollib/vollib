from matplotlib import pyplot as plt
import numpy
from numpy import log, sqrt, exp
from scipy.stats import norm
cnd = norm.cdf
pdf = norm.pdf


from vollib.black_scholes import black_scholes as swig
from cython_black_scholes import BlackScholes as cython_bs
from vollib.black_scholes.greeks import gamma, delta, theta, rho, vega, gamma_analytical


vollib_bs = lambda flag, S, K, t, r, v: swig(S, K, v, t, r, flag)


def d1(S,K,t,r,v):

    v_squared = v*v
    numerator = log(S/float(K)) + (r + v_squared/2.)*t
    denominator = v*sqrt(t)

    return numerator/denominator

def d2(S,K,t,r,v):

    return d1(S, K, t, r, v) - v*sqrt(t)

def black_scholes(flag, S, K, t, r, v):

    cnd_d1 = cnd(d1(S, K, t, r, v))
    cnd_d2 = cnd(d2(S, K, t, r, v))
    e_to_the_minus_rt = numpy.exp(-r*t)

    if flag == 'c':

        return S * cnd_d1 - K * e_to_the_minus_rt * cnd_d2

    else:

        return - S * cnd_d1 + K * e_to_the_minus_rt * cnd_d2


def analytical_delta(flag, S, K, t, r, v):

    d_1 = d1(S, K, t, r, v)

    if flag == 'p':
        return cnd(d_1) -1.0
    else:
        return cnd(d_1)


def analytical_gamma(flag, S, K, t, r, v):

    d_1 = d1(S, K, t, r, v)
    v_squared = v**2
    return pdf(d_1)/(S*v*sqrt(t))


def analytical_vega(flag, S, K, t, r, v):

    '''
    The text book analytical formula does not multiply by .01,
    but in practice vega is defined as the change in price
    for each 1 percent change in IV, hence we multiply by 0.01.
    '''

    d_1 = d1(S, K, t, r, v)
    return S * pdf(d_1) * sqrt(t) * 0.01


def analytical_rho(flag, S, K, t, r, v):

    d_2 = d2(S, K, t, r, v)

    e_to_the_minus_rt = numpy.exp(-r*t)
    if flag == 'c':
        return t*K*e_to_the_minus_rt * cnd(d_2) * .01
    else:
        -t*K*e_to_the_minus_rt * cnd(-d_2) * .01


def analytical_theta(flag, S, K, t, r, v):

    '''
    The text book analytical formula does not divide by 365,
    but in practice theta is defined as the change in price
    for each day change in t, hence we divide by 365.
    '''

    e_to_the_minus_rt = numpy.exp(-r*t)
    two_sqrt_t = 2 * sqrt(t)

    d_1 = d1(S, K, t, r, v)
    d_2 = d2(S, K, t, r, v)
    pdf_d1 = pdf(d_1)
    cnd_d2 = cnd(d_2)

    first_term = (-S * pdf_d1 * v) / two_sqrt_t
    second_term = r * K * e_to_the_minus_rt * cnd_d2

    return (first_term - second_term)/365.0



def plot_swig_delta_vs_cython_call_delta():

    S_vals = numpy.linspace(10,190,2000)
    K = 100
    t = 1.0
    r = .1
    v = 0.3
    flag = 'c'

    call_delta_haug, call_delta_jaeckel, analytical = [],[],[]

    for S in S_vals:
        call_delta_haug.append(delta(flag,S,K,t,r,v,cython_bs))
        call_delta_jaeckel.append(delta(flag,S,K,t,r,v,vollib_bs))
        analytical.append(analytical_delta(flag, S, K, t, r, v))
    plt.plot(S_vals,call_delta_haug,label = 'Haug')
    plt.plot(S_vals,call_delta_jaeckel, label = 'Jaeckel')
    plt.plot(S_vals,analytical,label = 'analytical')
    plt.grid()
    plt.legend(loc = 'best')
    plt.show()

    diff_jaeckel = numpy.array(analytical) - numpy.array(call_delta_jaeckel)
    plt.clf()
    plt.plot(S_vals,diff_jaeckel)
    plt.grid()
    plt.show()



def plot_swig_delta_vs_cython_put_delta():


    S_vals = numpy.linspace(10,190,2000)
    K = 100
    t = 0.25
    r = .1
    v = 0.3
    flag = 'p'

    call_delta_haug, call_delta_jaeckel = [],[]

    for S in S_vals:
        call_delta_haug.append(delta(flag,S,K,t,r,v,cython_bs))
        call_delta_jaeckel.append(delta(flag,S,K,t,r,v,vollib_bs))
    plt.plot(S_vals,call_delta_haug,label = 'Haug')
    plt.plot(S_vals,call_delta_jaeckel, label = 'Jaeckel')
    plt.grid()

    plt.legend(loc = 'best')
    plt.show()

    diff = numpy.array(call_delta_haug) - numpy.array(call_delta_jaeckel)
    plt.clf()
    plt.plot(S_vals,diff)
    plt.grid()
    plt.show()

def plot_swig_delta_vs_cython_call_gamma():

    S_vals = numpy.linspace(10,190,2000)
    K = 100
    t = 1
    r = .1
    v = 0.3
    flag = 'c'

    call_gamma_haug, call_gamma_jaeckel, analytical = [],[],[]

    for S in S_vals:
        call_gamma_haug.append(gamma(flag,S,K,t,r,v,cython_bs))
        call_gamma_jaeckel.append(gamma(flag,S,K,t,r,v,vollib_bs))
        analytical.append(analytical_gamma(flag, S, K, t, r, v))
    plt.plot(S_vals,call_gamma_haug,label = 'Haug')
    plt.plot(S_vals,call_gamma_jaeckel, label = 'Jaeckel')
    plt.plot(S_vals,analytical,label = 'analytical', linewidth = 5)
    plt.grid()
    plt.legend(loc = 'best')
    plt.show()

    diff = numpy.array(analytical) - numpy.array(call_gamma_jaeckel)
    plt.clf()
    plt.plot(S_vals,diff)
    plt.grid()
    plt.show()

def plot_swig_delta_vs_cython_vega():

    S_vals = numpy.linspace(10,190,2000)
    K = 100
    t = 1
    r = .1
    v = 0.3
    flag = 'c'

    haug, jaeckel, analytical = [],[],[]

    for S in S_vals:
        haug.append(vega(flag,S,K,t,r,v,cython_bs))
        jaeckel.append(vega(flag,S,K,t,r,v,vollib_bs))
        analytical.append(analytical_vega(flag, S, K, t, r, v))
    plt.plot(S_vals,haug,label = 'Haug')
    plt.plot(S_vals,jaeckel, label = 'Jaeckel')
    plt.plot(S_vals,analytical,label = 'analytical')
    plt.grid()
    plt.legend(loc = 'best')
    plt.show()

    diff = numpy.array(analytical) - numpy.array(jaeckel)
    plt.clf()
    plt.plot(S_vals,diff)
    plt.grid()
    plt.show()

def plot_swig_delta_vs_cython_theta():

    S_vals = numpy.linspace(10,190,2000)
    K = 100
    t = 1
    r = .1
    v = 0.3
    flag = 'c'

    haug, jaeckel, analytical, python = [],[],[],[]

    for S in S_vals:
        haug.append(theta(flag,S,K,t,r,v,cython_bs))
        jaeckel.append(theta(flag,S,K,t,r,v,vollib_bs))
        python.append(theta(flag, S, K, t, r, v, black_scholes))
        analytical.append(analytical_theta(flag, S, K, t, r, v))
    plt.plot(S_vals,haug,label = 'Haug')
    plt.plot(S_vals,jaeckel, label = 'Jaeckel')
    plt.plot(S_vals,analytical,label = 'analytical')
    plt.plot(S_vals,python,label = 'python')

    plt.grid()
    plt.legend(loc = 'best')
    plt.show()

    diff = numpy.array(haug) - numpy.array(jaeckel)
    plt.clf()
    plt.plot(S_vals,diff)
    plt.grid()
    plt.show()

def plot_swig_vs_cython_rho():

    S_vals = numpy.linspace(10,190,2000)
    K = 100
    t = 1
    r = .1
    v = 0.3
    flag = 'c'

    haug, jaeckel, analytical, python = [],[],[],[]

    for S in S_vals:
        haug.append(rho(flag,S,K,t,r,v,cython_bs))
        jaeckel.append(rho(flag,S,K,t,r,v,vollib_bs))
        python.append(rho(flag, S, K, t, r, v, black_scholes))
        analytical.append(analytical_rho(flag, S, K, t, r, v))
    plt.plot(S_vals,haug,label = 'Haug')
    plt.plot(S_vals,jaeckel, label = 'Jaeckel')
    plt.plot(S_vals,analytical,label = 'analytical')
    plt.plot(S_vals,python,label = 'python')

    plt.grid()
    plt.legend(loc = 'best')
    plt.show()

    diff = numpy.array(haug) - numpy.array(analytical)
    plt.clf()
    plt.plot(S_vals,diff)
    plt.grid()
    plt.show()


plot_swig_delta_vs_cython_theta()
