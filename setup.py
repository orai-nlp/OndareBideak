from setuptools import setup, find_packages

setup(
    name = "KULTURBIDEAK",
    version = "2.0",
    url = '',
    license = 'BSD',
    description = "Ondarebideak",
    author = 'Elhuyar Fundazioa',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)
