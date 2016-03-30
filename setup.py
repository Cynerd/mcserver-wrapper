#!/usr/bin/env python3
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='mcserver-wrapper',
    version='0.3.0',
    description="Minecraft server wrapper",
    long_description=long_description,
    url="https://github.com/Cynerd/mcserver-wrapper",
    author="Cynerd",
    author_email="cynerd@email.cz",
    license="GPLv2",

    clasifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        ],
    keywords='Minecraft wrapper server',

    packages=['mcwrapper'],
    entry_points={
        'console_scripts': [
            'mcwrapper=mcwrapper:main'
            ]
        }
    )
