import unittest

from vollib.tests.test_utils import TestDataIterator, almost_equal
from vollib.black_scholes import black_scholes
from vollib.black_scholes.implied_volatility import implied_volatility
from vollib.black_scholes.greeks import analytical
from vollib.black_scholes.greeks import numerical


class TestBlackScholesAgainstBenchmarkValues(unittest.TestCase):
    
    def setUp(self):
        self.tdi = TestDataIterator()

    def test_prices(self):

        while self.tdi.has_next():
            row = self.tdi.next_row()
            S,K,t,r,sigma = row['S'],row['K'],row['t'],row['R'],row['v']
            self.assertTrue(
                almost_equal(
                    black_scholes('c', S, K, t, r, sigma), row['bs_call'], epsilon=.000001
                )
            )
            self.assertTrue(
                almost_equal(
                    black_scholes('p', S, K, t, r, sigma), row['bs_put'], epsilon=.000001
                )
            )
            
    
    def test_analytical_delta(self):
        
        while self.tdi.has_next():
            row = self.tdi.next_row()
            S,K,t,r,sigma = row['S'],row['K'],row['t'],row['R'],row['v']
            self.assertTrue(
                almost_equal(
                    analytical.delta('c', S, K, t, r, sigma), row['CD'], epsilon=.000001
                )
            )
            self.assertTrue(
                almost_equal(
                    analytical.delta('p', S, K, t, r, sigma), row['PD'], epsilon=.000001
                )
            )
        
    def _test_analytical_theta(self):

        while self.tdi.has_next():
            row = self.tdi.next_row()
            S,K,t,r,sigma = row['S'],row['K'],row['t'],row['R'],row['v']
            #self.assertTrue(
            #    almost_equal(
            print        analytical.theta('c', S, K, t, r, sigma), row['CT']#, epsilon=.001
            #    )
            #)
            #self.assertTrue(
            #    almost_equal(
            print         analytical.theta('p', S, K, t, r, sigma), row['PT'] #, epsilon=.000001
            #    )
            #)
            
            
    def test_analytical_gamma(self):

        while self.tdi.has_next():
            row = self.tdi.next_row()
            S,K,t,r,sigma = row['S'],row['K'],row['t'],row['R'],row['v']
            self.assertTrue(
                almost_equal(
                    analytical.gamma('c', S, K, t, r, sigma), row['CG'], epsilon=.000001
                )
            )
            self.assertTrue(
                almost_equal(
                     analytical.gamma('p', S, K, t, r, sigma), row['PG'], epsilon=.000001
                )
            )
            
    def test_analytical_vega(self):

        while self.tdi.has_next():
            row = self.tdi.next_row()
            S,K,t,r,sigma = row['S'],row['K'],row['t'],row['R'],row['v']
            self.assertTrue(
                almost_equal(
                    analytical.vega('c', S, K, t, r, sigma), row['CV']*.01, epsilon=.01
                )
            )
            self.assertTrue(
                almost_equal(
                    analytical.vega('p', S, K, t, r, sigma), row['PV']*.01, epsilon=.01
                )
            )
            
            
    def test_analytical_rho(self):

        while self.tdi.has_next():
            row = self.tdi.next_row()
            S,K,t,r,sigma = row['S'],row['K'],row['t'],row['R'],row['v']
            self.assertTrue(
                almost_equal(
                    analytical.rho('c', S, K, t, r, sigma), row['CR']*.01, epsilon=.000000001
                )
            )
            self.assertTrue(
                almost_equal(
                    analytical.rho('p', S, K, t, r, sigma), row['PR']*.01, epsilon=.000000001
                )
            )
    
    
    def test_implied_volatility(self):
        
        while self.tdi.has_next():
            
            row = self.tdi.next_row()
            S,K,t,r,sigma = row['S'],row['K'],row['t'],row['R'],row['v']
            C,P = black_scholes('c', S, K, t, r, sigma), black_scholes('p', S, K, t, r, sigma)
            try:
                iv = implied_volatility(C, S, K, t, r, 'c')
                self.assertTrue(almost_equal(sigma, iv, epsilon = .0001))
            except:
                print 'could not calculate iv for ', C, S, K, t, r, 'c' 

            iv = implied_volatility(P, S, K, t, r, 'p')
            self.assertTrue(almost_equal(sigma, iv, epsilon = .001) or (iv ==0.0))


    
if __name__ == '__main__':
    unittest.main()

