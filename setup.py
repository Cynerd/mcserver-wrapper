#!/usr/bin/env python3
from os import path
from setuptools import setup

readme_file = path.join(path.abspath(path.dirname(__file__)), 'README.md')
long_description = ""
try:
    import pypandoc
    long_description = pypandoc.convert(readme_file, 'rst', format='md')
except (IOError, ImportError):
    print("Pandoc not found. Long_description conversion failure.")


setup(
    name='mcserver-wrapper',
    version='0.3.6',
    description="Minecraft server wrapper",
    long_description=long_description,
    url="https://github.com/Cynerd/mcserver-wrapper",
    author="Cynerd",
    author_email="cynerd@email.cz",
    license="GPLv2",

    classifiers=[
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
