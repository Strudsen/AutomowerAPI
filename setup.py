from setuptools import setup

setup(
   name='AutomowerAPI',
   version='0.0.1',
   description='python API to connect to Husqvarna Automower',
   author='Kasper Kristensen',
   author_email='kk@kasperk.it',
   packages=['AutomowerAPI'],
   install_requires=['requests', 'json', 'logging'],
)