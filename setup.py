from setuptools import setup

setup(
	name="tiktalik-cli",
	version="1.5",
	description="Tiktalik Computing command line interface",
	author="Techstorage sp. z o.o.",
	author_email="kontakt@tiktalik.com",
	url="http://www.tiktalik.com",
	classifiers=[
		"Programming Language :: Python",
		"Topic :: Internet",
		"Topic :: Utilities",
		"License :: OSI Approved :: MIT License",
	],

	packages=["tiktalik_cli", "tiktalik_cli.command"],
	entry_points={
		"console_scripts": [
			"tiktalik = tiktalik_cli.main:main"
			]
		},

	install_requires=["tiktalik>=1.3"]
)
