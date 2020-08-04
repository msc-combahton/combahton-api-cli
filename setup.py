from setuptools import setup, find_packages

setup(
    name = 'cbcli',
    version='0.1',
    packages=find_packages(),
    install_requires = [
        'Click', 'json', 'configparser'
    ],
    entry_points='''
        [console_scripts]
        main=main:cli
    '''
)