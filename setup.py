from setuptools import setup

setup(
	name="tiktalik-cli",
	version="0.1",
	description="Tiktalik commandline utility",
	author="Tiktalik.com",
	author_email="kontakt@tiktalik.com",
	url="http://tiktalik.com",

	packages=["tiktalik_cli", "tiktalik_cli.command"],
	entry_points={
		"console_scripts": [
			"tiktalik = tiktalik_cli.main:main"
			]
		},

	install_requires=["tiktalik-python"]
)
