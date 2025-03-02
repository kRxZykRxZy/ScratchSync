# setup.py

from setuptools import setup, find_packages

setup(
    name='ScratchSync',  # The name of your package
    version='0.1.0',
    packages=find_packages(),
    description='A library for interacting with the Scratch API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='kRxZy_kRxZy',
    author_email='your.email@example.com',
    url='https://github.com/kRxZykRxZy/ScratchSync',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'requests',  # List of dependencies
    ],
    python_requires='>=3.6',
)
