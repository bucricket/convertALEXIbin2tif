#!/usr/bin/env python

import shutil
import os
try:
    from setuptools import setup
    setup_kwargs = {'entry_points': {'console_scripts':['alexi_bin2tif=convertALEXIbin2tif.processALEXIbin2tif:main']}}
except ImportError:
    from distutils.core import setup
    setup_kwargs = {'scripts': ['bin/processALEXIbin2tif']}
    
setup(
    name="alexi_bin2tif",
    version="0.1.0",
    description="Convert all ALEXI bin to geotiffs",
    author="Mitchell Schull",
    author_email="mitch.schull@noaa.gov",
    #url="https://github.com/bucricket/projectMAS.git",
    packages= ['convertALEXIbin2tif'],
    platforms='Posix; MacOS X; Windows',
    license='BSD 3-Clause',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        # Uses dictionary comprehensions ==> 2.7 only
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: GIS',
    ],  
    **setup_kwargs
)
