from setuptools import find_packages
from setuptools import setup

setup(
    name='Curling League Manager',
    version='1.0.0',
    description="this package contains league management software",
    author='Kevin Carter',
    author_email='kmc0156@auburn.edu',
    url='https://github.com/kmc0156/CurlingLeagueManager',
    packages=find_packages(),
    py_modules=['curling_league', 'ui'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'league-manager-client = module6.ui.main_window:main'
            #'league-manager-client = main:main'
        ]
    }
)
