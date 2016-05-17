#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages


setup(
    name='vollib',
    version='0.1.5',
    description='',
    url='http://vollib.org',
    # download_url='git+https://github.com/vollib/vollib.git#egg=vollib',
    maintainer='vollib',
    maintainer_email='support@quantycarlo.com',
    license='MIT',
    install_requires = [
        'lets_be_rational',
        'simplejson',
        'numpy',
        'pandas'
    ],
    packages=find_packages(exclude=['docs', 'vollib/tests'])
)
