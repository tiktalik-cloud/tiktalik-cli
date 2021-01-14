"""Tiktalik Command Line Interface"""
import sys
import setuptools

try:
    import tiktalik_cli
except ImportError:
    print("error: tiktalik-cli requires Python 3.5 or greater.")
    sys.exit(1)

LONG_DESC = open('README.md').read()
DOWNLOAD = "https://github.com/tiktalik-cloud/tiktalik-cli/archive/v1.9.3.2.tar.gz"

setuptools.setup(
    name="tiktalik-cli",
    version="1.9.3.2",
    python_requires=">=3.5",
    license="MIT",
    description="Tiktalik Computing command line interface",
    long_description_content_type="text/markdown",
    long_description=LONG_DESC,
    author="Techstorage sp. z o.o.",
    author_email="kontakt@tiktalik.com",
    url="http://www.tiktalik.com",
    download_url=DOWNLOAD,
    keywords=["Tiktalik", "CLI", "Terminal", "VPS"],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 6 - Mature",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Internet",
        "Topic :: Utilities",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
    ],
    packages=["tiktalik_cli", "tiktalik_cli.command"],
    entry_points={"console_scripts": ["tiktalik = tiktalik_cli.main:main"]},
    install_requires=["tiktalik>=1.6.3.1.1"],
)
