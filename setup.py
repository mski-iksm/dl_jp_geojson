# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


def load_requires_from_file(fname):
    if not os.path.exists(fname):
        raise IOError(fname)
    return [pkg.strip() for pkg in open(fname, 'r')]

setup(
    name='dl_jp_geojson',
    version='0.0.3',
    description='Python library for downloading Japanese prefecture/city\
     boarder geojson files, and import to geopandas table.',
    long_description=readme,
    author='Daiki Ikeshima',
    author_email='9000000000000000091e@gmail.com',
    url='https://github.com/mski-iksm/dl_jp_geojson',
    license=license,
    install_requires=load_requires_from_file('requirements.txt'),
    packages=find_packages(".", exclude=('tests', 'docs')),
    include_package_data=True,
    # data_files=[('data', ['dl_jp_geojson/data/prefecture_city.csv']
    #             )
    #            ],
)
