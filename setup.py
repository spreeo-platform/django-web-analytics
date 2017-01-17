import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-web-analytics',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='Apache License 2.0',
    description='A simple Django app to store and query web analytics.',
    long_description=README,
    url='https://github.com/spreeo-platform/django-web-analytics',
    author='Dalia Daud',
    author_email='daliadaud@gmail.com',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
        ],
    install_requires=[
        "Django==1.10.5",
        "psycopg2==2.6.2"
        ],
)
