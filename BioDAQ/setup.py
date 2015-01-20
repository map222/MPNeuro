# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 18:59:50 2015

@author: palmiteradmin
"""

from distutils.core import setup
import py2exe
import numpy

setup(console=['BioDAQmain.py'], options={
        'py2exe': {
            'includes': ['zmq.backend.cython'],
            'excludes': ['zmq.libzmq'],
            'dll_excludes': ['libzmq.pyd'],
            'packages' : ['matplotlib', 'pytz'],
        }
    })