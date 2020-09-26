from setuptools import find_packages, setup

# Read repository information. This will be used as the package description.
long_description = None
with open("README.md", "r") as fh:
    long_description = fh.read()
assert long_description is not None

setup(
    name='aida',
    version='0.1.0',
    description='Collection of utils (ML-oriented) aiming to reduce boilerplate code.',
    author='Alexandru Dinu',
    author_email='alex.dinu07@gmail.com',
    url='https://github.com/alexandru-dinu/aida',
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
