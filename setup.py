# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from sphinxcontrib.pandoc_markdown import __version__

# long_desc = open('README.md').read()

requires = ['Sphinx>=0.6', 'Markdown']

setup(
    name='sphinxcontrib-pandoc-markdown',
    version=__version__,
    url='https://github.com/pashango2/sphinxcontrib-pandoc-markdown/',
    license='BSD',
    author='Toshiyuki Ishii',
    author_email='pashango2@gmail.com',
    description='Yet another markdown processor for Sphinx',
    long_description="",
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
