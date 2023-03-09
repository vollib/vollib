# `vollib`

`vollib` is a python library for calculating option prices, 
implied volatility and greeks. At its core is Peter Jäckel's 
source code for `LetsBeRational`, an extremely fast and accurate algorithm 
for obtaining Black's implied volatility from option prices.

Building on this solid foundation, `vollib` provides functions 
to calculate option prices, implied volatility and greeks using 
Black, Black-Scholes, and Black-Scholes-Merton. `vollib` 
implements both analytical and numerical greeks for each of the three pricing formulae.

### About the initial release

This is the initial release of `vollib`.  Tests and documentation are still incomplete.

### Dependencies

`vollib` was written in Python 2.7.  It depends on the ```lets_be_rational``` package, a simple (SWIG) wrapper around Peter Jäckel's original C source code.  

To install via pip, type the following:

```
>>> pip install vollib
```

Installing `vollib` via pip will automatically install the necessary dependencies,
except for SWIG, pip, and Python.  This has been tested to work on Windows, Linux and Macintosh OS X.

Python, pip and SWIG must be installed prior to installing ```vollib```. 


`lets_be_rational` is quite stable compared to `vollib`, which is likely to be updated frequently.

For those who wish to clone the vollib repo, you might prefer to install `lets_be_rational` 
separately with pip, since this takes care of the C compilation.

### About "Let's be Rational":

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

### Links:


  * [Let's Be Rational](http://www.pjaeckel.webspace.virginmedia.com/LetsBeRational.pdf)

  *  [pip](https://pypi.python.org/pypi/pip)

  *  [SWIG](http://www.swig.org/download.html)
  
  * [Licence](http://vollib.org/license)

  * [Vollib Home](http://vollib.org)

