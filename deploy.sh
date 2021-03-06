#!/bin/bash

clean () {
    rm -rf build dist bagoftools.egg-info
}

clean

pipreqs . --force --no-pin && sort -o requirements.txt requirements.txt
sleep 1

python setup.py sdist bdist_wheel
sleep 1

twine check dist/* && twine upload --repository pypi dist/*

clean
