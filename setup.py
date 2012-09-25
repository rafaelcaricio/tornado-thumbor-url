#!/usr/bin/python
# -*- coding: utf-8 -*-

# libthumbor - python extension to thumbor
# http://github.com/heynemann/libthumbor

# Licensed under the MIT license: 
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2012 Rafael Caricio rafael@caricio.com

'''Module that configures setuptools to package tornado-thumbor-url'''

from setuptools import setup, find_packages
from tornado_thumbor_url import __version__

setup(
    name = 'tornado_thumbor_url',
    version = __version__,
    description = "tornado-thumbor-url is a python extension to tornado for encrypted thumbor url generation",
    long_description = """
tornado-thumbor-url is a python extension to tornado
for encrypted thumbor url generation
It allows users to generate safe urls easily.
""",    
    keywords = 'imaging face detection feature thumbor thumbnail' + \
               ' imagemagick pil opencv',
    author = 'Rafael Caricio',
    author_email = 'rafael@caricio.com',
    url = 'http://github.com/rafaelcaricio/tornado-thumbor-url',
    license = 'MIT',
    classifiers = ['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: MacOS',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 2.6',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
                   'Topic :: Multimedia :: Graphics :: Presentation'
    ],
    packages = find_packages(),
    package_dir = {"tornado_thumbor_url": "tornado_thumbor_url"},
    include_package_data = True,
    package_data = {
    },

    install_requires=[
        "libthumbor",
        "tornado"
    ],
)

