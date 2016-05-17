import numpy
import unittest

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


epsilon = .01
epsilon_for_theta = 0.1

class testGreeks(unittest.TestCase):
    
    def test_prices(self):
        S = 100.0
        for flag in ['c','p']:
            for K in numpy.linspace(20,200,10):
                for r in numpy.linspace(0,0.2,10):
                    for sigma in numpy.linspace(0.1,0.5,10):
                        for t in numpy.linspace(0.01,2,10):
                            
                            for i in range(5):
                                val1 = black_scholes(flag, S, K, t, r, sigma)
                                val2 = python_black_scholes(flag, S, K, t, r, sigma)
                                results_match = abs(val1-val2)<epsilon
                                if not results_match:
                                    print 'price mismatch:', flag, val1, val2
                                self.assertTrue(results_match)    
    
    def test_theta(self):
        
        S = 100.0
        for flag in ['c','p']:
            for K in numpy.linspace(20,200,10):
                for r in numpy.linspace(0,0.2,10):
                    for sigma in numpy.linspace(0.1,0.5,10):
                        for t in numpy.linspace(0.01,2,10):
                            
                            for i in range(5):
                                val1 = theta(flag, S, K, t, r, sigma)
                                val2 = ntheta(flag, S, K, t, r, sigma)
                                results_match = abs(val1-val2)<epsilon_for_theta
                                if not results_match:
                                    print 'theta mismatch:', flag, val1, val2
                                self.assertTrue(results_match)


    def test_delta(self):
        

        S = 100.0
        for flag in ['c','p']:
            for K in numpy.linspace(20,200,10):
                for r in numpy.linspace(0,0.2,10):
                    for sigma in numpy.linspace(0.1,0.5,10):
                        for t in numpy.linspace(0.01,2,10):
                            
                            for i in range(5):
                                val1 = delta(flag, S, K, t, r, sigma)
                                val2 = ndelta(flag, S, K, t, r, sigma)
                                results_match = abs(val1-val2)<epsilon
                                if not results_match:
                                    print flag, val1, val2
                                self.assertTrue(results_match)
                    
    def test_gamma(self):
        
        S = 100.0
        for flag in ['c','p']:
            for K in numpy.linspace(20,200,10):
                for r in numpy.linspace(0,0.2,10):
                    for sigma in numpy.linspace(0.1,0.5,10):
                        for t in numpy.linspace(0.01,2,10):
                            
                            for i in range(5):
                                val1 = gamma(flag, S, K, t, r, sigma)
                                val2 = ngamma(flag, S, K, t, r, sigma)
                                results_match = abs(val1-val2)<epsilon
                                if not results_match:
                                    print flag, val1, val2
                                self.assertTrue(results_match)

    def test_vega(self):
        
        S = 100.0
        for flag in ['c','p']:
            for K in numpy.linspace(20,200,10):
                for r in numpy.linspace(0,0.2,10):
                    for sigma in numpy.linspace(0.1,0.5,10):
                        for t in numpy.linspace(0.01,2,10):
                            
                            for i in range(5):
                                val1 = vega(flag, S, K, t, r, sigma)
                                val2 = nvega(flag, S, K, t, r, sigma)
                                results_match = abs(val1-val2)<epsilon
                                if not results_match:
                                    print flag, val1, val2
                                self.assertTrue(results_match)


    def test_rho(self):
        
        S = 100.0
        for flag in ['c','p']:
            for K in numpy.linspace(20,200,10):
                for r in numpy.linspace(0,0.2,10):
                    for sigma in numpy.linspace(0.1,0.5,10):
                        for t in numpy.linspace(0.01,2,10):
                            
                            for i in range(5):
                                val1 = rho(flag, S, K, t, r, sigma)
                                val2 = nrho(flag, S, K, t, r, sigma)
                                results_match = abs(val1-val2)<epsilon
                                if not results_match:
                                    print flag, val1, val2
                                self.assertTrue(results_match)
                            
if __name__ == '__main__':
    unittest.main()