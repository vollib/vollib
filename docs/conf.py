# -*- coding: utf-8 -*-
#
# vollib documentation build configuration file, created by
# sphinx-quickstart on Wed Apr  1 19:21:03 2015.
#

import sys
import os

sys.path.append('..')


# -- General configuration ------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'matplotlib.sphinxext.plot_directive',
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest'  
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = u'vollib'
copyright = u'2015, Iota Technologies Pte Ltd'

version = '0.0.1'   #short version
release = '0.0.1'   #longer version w/ extra tags, e.g. 1.2.3-beta

exclude_patterns = ['_build',
    'apidoc/vollib.tests.rst',
    'apidoc/vollib.plots.rst',
    
    ]

# -- Options for HTML output ----------------------------------------------

html_theme = "scrolls"
html_logo = "vollib_60.png"
html_favicon = "favicon.png"
#html_static_path = ['~./vollib_sphinx_output/_static']

def maybe_skip_member(app, what, name, obj, skip, options):
    skip_list = [
        'plots',
        'plot_numerical_vs_analytical'
        'implied_volatility_of_discounted_option_price',
        'implied_volatility_of_undiscounted_option_price',
        'implied_volatility_of_undiscounted_option_price_limited_iterations',      
        'plot_numerical_vs_analytical',
        'normalised_black',
        'normalised_implied_volatility',
        'normalised_implied_volatility_limited_iterations',
        'black_call',
        'black_put', 
        'd1',
        'd2',
        'test_python_vs_c_values',
        'implied_volatility_brent',
        'implied_volatility_limited_iterations',
        'python_black_scholes',
        'f',
        'test',
        'hull_book_tests',
        'bsm_call',
        'bsm_put',
        'python_black_scholes_merton'
        
    ]
        
    
    if name in skip_list:
        print 'skipping:', name
        
        return True
    else:
        return False

def setup(app):
    app.connect('autodoc-skip-member', maybe_skip_member)