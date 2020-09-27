#!/bin/bash

clean () {
    rm -rf build dist bagoftools.egg-info
}

clean

python setup.py sdist bdist_wheel
twine check dist/* && twine upload --repository pypi dist/*

clean

sleep 10

pip install --upgrade bagoftools
