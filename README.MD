# vollib


### About the initial release


This is the initial release of vollib.  Tests and documentation are still incomplete.

### Background


Vollib is a python library for calculating option prices, 
implied volatility and greeks. At its core is Peter Jäckel's 
source code for LetsBeRational, an extremely fast and accurate algorithm 
for obtaining Black's implied volatility from option prices.

#### About "Let's be Rational":

["Let's Be Rational"](http://www.pjaeckel.webspace.virginmedia.com/LetsBeRational.pdf) is a paper by [Peter Jäckel](http://jaeckel.org) showing *"how Black's volatility can be implied from option prices with as little as two iterations to maximum attainable precision on standard (64 bit floating point) hardware for all possible inputs."*

The paper is accompanied by the full C source code, which resides at [www.jaeckel.org/LetsBeRational.7z](www.jaeckel.org/LetsBeRational.7z).

```
Copyright © 2013-2014 Peter Jäckel.

Permission to use, copy, modify, and distribute this software is freely granted,
provided that this notice is preserved.

WARRANTY DISCLAIMER
The Software is provided "as is" without warranty of any kind, either express or implied,
including without limitation any implied warranties of condition, uninterrupted use,
merchantability, fitness for a particular purpose, or non-infringement.
```




Building on this solid foundation, vollib provides functions 
to calculate option prices, implied volatility and greeks using 
Black, Black-Scholes, and Black-Scholes-Merton. vollib 
implements both analytical and numerical greeks.

Vollib depends on the ```lets_be_rational``` package, a simple 
(SWIG) wrapper for those only needed access to Peter Jäckel's 
C functions inside Python. Both lets_be_rational and vollib 
can be easily installed using the "pip" command on Windows, 
Linux, or Macintosh OS X

### Dependencies


SWIG must be installed prior to installing ```vollib```. Download and 
install [SWIG](http://www.swig.org/download.html).

Vollib depends on numpy, pandas and lets_be_rational.  The easiest way to install is with pip.

lets_be_rational is quite stable compared to vollib, which is likely to be updated frequently.

For those who wish to clone the vollib repo, you might prefer to install lets_be_rational 
separately with pip, since this will take care of the C compilation.

### Links:


  * [Licence](http://vollib.org/license)

  * [Vollib Home](http://vollib.org)

