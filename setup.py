"""
Setup script for lifelog server

"""

from setuptools import setup, find_packages

setup(
        name = "Lifelog Server",
        version = "0.1",
        packages = find_packages(),
        install_requires=['Flask>=0.9',
            'pymongo>=2.5.1']
        )
