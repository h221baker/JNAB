# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='jnab',

    version='0.0.0',

    description='James Need A Budget',
    long_description="",

    # Author details
    author='James Z',
    author_email='oahzjh@gmail.com',

    # Choose your license
    license='MIT',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
)
