#!/bin/bash

PYTHONPATH=$PWD:$PYTHONPATH py.test bagoftools/ tests/

rm -rf .pytest_cache