import re
from setuptools import find_packages, setup

# Read repository information. This will be used as the package description.
long_description = None
with open("README.md", "r") as fh:
    long_description = fh.read()
assert long_description is not None

# Read version
version = None
with open('bagoftools/__init__.py', 'rt') as fh:
    version = re.search(r"([0-9\.]+)", fh.read().strip()).group()
assert version is not None


setup(
    name='bagoftools',
    version=version,
    description='Collection of utils (ML-oriented) aiming to reduce boilerplate code.',
    author='Alexandru Dinu',
    author_email='alex.dinu07@gmail.com',
    url='https://github.com/alexandru-dinu/bagoftools',
    license='Apache 2.0',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering"
    ],
)
