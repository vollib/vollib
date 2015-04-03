vollib
======

About the initial release
=========================

This is the initial release of vollib.  Tests and documentation are still incomplete.

Background
==========

Vollib is a python library for calculating option prices, 
implied volatility and greeks. At its core is Peter Jäckel's 
LetsBeRational, an extremely fast and accurate method for 
obtaining Black's implied from option prices with as 
little as two iterations to maximum attainable precision 
on standard (64 bit floating point) hardware for all possible 
inputs.

Building on this solid foundation, vollib provides functions 
to calculate option prices, implied volatility and greeks using 
Black, Black-Scholes, and Black-Scholes-Merton. vollib 
implements both analytical and numerical greeks.

Vollib depends on the lets_be_rational package, a simple 
(SWIG) wrapper for those only needed access to Peter Jäckel's 
C functions inside Python. Both lets_be_rational and vollib 
can be easily installed using the "pip" command on Windows, 
Linux, or Macintosh OS X

Dependencies
============

Vollib depends on numpy and lets_be_rational.  The easiest way to install is with pip.

lets_be_rational is quite stable compared to vollib, which is likely to be updated frequently.
For those who wish to clone the vollib repo, you might prefer to install lets_be_rational 
separately with pip, since this will take care of the C compilation.

Links:
======

  * [Licence](http://vollib.org/license)

  * [Vollib Home](http://vollib.org)

