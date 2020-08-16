"""Tiktalik Command Line Interface"""
from distutils.core import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="tiktalik-cli",
    version="1.9.3.1",
    python_requires=">=3.5",
    license="MIT",
    description="Tiktalik Computing command line interface",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Techstorage sp. z o.o.",
    author_email="kontakt@tiktalik.com",
    url="http://www.tiktalik.com",
    keywords=["Tiktalik", "CLI", "Terminal"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Users",
        "Topic :: Internet",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    packages=["tiktalik_cli", "tiktalik_cli.command"],
    entry_points={"console_scripts": ["tiktalik = tiktalik_cli.main:main"]},
    install_requires=["tiktalik>=1.6.3.1.1"],
)
