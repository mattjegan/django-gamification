#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This setup.py is based off https://github.com/kennethreitz/setup.py

import io
import os
import sys
from shutil import rmtree

from setuptools import setup, Command

# Package meta-data.
NAME = 'django_gamification'
DESCRIPTION = 'The missing gamification plugin for Django'
URL = 'https://github.com/mattjegan/django-gamification'
EMAIL = 'matthewj.egan@hotmail.com'
AUTHOR = 'Matthew Egan'

REQUIRED = []

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


class PublishCommand(Command):
    """Support setup.py publish."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except FileNotFoundError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'
                  .format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload --repository-url ' +
                  'https://upload.pypi.org/legacy/ dist/*')

        sys.exit()


setup(
    name=NAME,
    version='0.3.0',
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=['django_gamification'],
    install_requires=REQUIRED,
    include_package_data=True,
    license='BSD',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
    ],
    cmdclass={
        'publish': PublishCommand,
    },
)
