import re
from setuptools import find_packages, setup

# Read repository information - use as the package description
with open("README.md", "r") as fh:
    long_description = fh.read()

# Read version
with open('bagoftools/__init__.py', 'rt') as fh:
    version = re.search(r"([0-9\.]+)", fh.read().strip()).group()

# Read requirements
with open('requirements.txt', 'rt') as fh:
    reqs = [x.strip() for x in fh.readlines()]

setup(
    name='bagoftools',
    version=version,
    description='Collection of utility functions aiming to reduce boilerplate code.',
    author='Alexandru Dinu',
    author_email='alex.dinu07@gmail.com',
    url='https://github.com/alexandru-dinu/bagoftools',
    license='Apache 2.0',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=reqs,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering"
    ],
)
