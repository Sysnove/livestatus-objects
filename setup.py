#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
 
setup(
    name='livestatus-objects',
    version='0.3',
    packages=find_packages(),
    author="Guillaume Subiron",
    author_email="maethor+pip@subiron.org",
    description="Query MK Livestatus and return results as objects.",
    long_description=read('README.md'),
    include_package_data=True,
    url='http://github.com/sysnove/livestatus-objects',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3.3",
    ],
    license="WTFPL",
)
