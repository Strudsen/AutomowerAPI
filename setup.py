import io
from setuptools import setup

setup(
   name='AutomowerAPI',
   version='0.0.3',
   description='python API to connect to Husqvarna Automower',
   long_description=io.open('README.md', encoding='UTF-8').read(),
   author='Kasper Kristensen',
   author_email='kk@kasperk.it',
   packages=['AutomowerAPI'],
   url='https://github.com/Strudsen/AutomowerAPI/',
)