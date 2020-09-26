from setuptools import find_packages, setup

# Read repository information. This will be used as the package description.
long_description = None
with open("README.md", "r") as fh:
    long_description = fh.read()
assert long_description is not None

setup(
    name='ml_utils',
    version='0.1.0',
    description='Collection of ML utils aiming to reduce boilerplate code.',
    author='alexandru-dinu',
    author_email='alex.dinu07@gmail.com',
    url='https://github.com/alexandru-dinu/ml-utils',
    license='Apache 2.0',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
