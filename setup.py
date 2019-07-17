from setuptools import setup

setup(
    name='Kannji DB Model',
    version='0.0.0',
    description='The database models for the Kannji app.',
    url='http://github.com/kannji/db',
    author='Jan-Luca Klees',
    author_email='email@janlucaklees.de',
    license='MIT',
    packages=['db'],
    install_requires=[
        'lxml == 4.3.4',
        'SQLAlchemy == 1.3.5'
    ],
    zip_safe=False
)

