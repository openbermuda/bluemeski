from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '0.0.1'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if 'git+' not in x]

setup(
    name='bluemeski',
    version=__version__,
    description='Work with oases',
    long_description=long_description,
    url='https://github.com/openbermuda/bluemeski',
    download_url='https://github.com/openbermuda/bluemeski/tarball/' + __version__,
    license='GPL v 3',
    classifiers = [
      'Development Status :: 3 - Alpha',
      'Intended Audience :: End Users/Desktop',
      'Programming Language :: Python :: 3.6.1',
    ],
    entry_points = {
        'console_scripts': [
            'blume = bluemeski.blue:main',
            ],
        },
    keywords='data pi karma oasis',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Johnny Gill',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email='swfiua@gmail.com'
)
