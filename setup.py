#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    readme = file.read()

requirements = [
    'beautifulsoup4==4.4.0',
    'netaddr==0.7.18',
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
]

setup(
    name='ipfromwebpage',
    version='0.1.0',
    description='Takes a webpage and outputs all ip address scope.',
    long_description=readme,
    author='Jay Shepherd',
    author_email='jdshep89@hotmail.com',
    url='https://github.com/shepherdjay/ip-from-webpage',

    packages=find_packages(include=['ipfromwebpage']),
    include_package_data=True,
    install_requires=requirements,
    license='MIT license',
    zip_safe=False,
    keywords='ipfromwebpage',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements
)
