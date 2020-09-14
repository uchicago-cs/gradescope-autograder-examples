#!/bin/bash

rm -f gradescope.zip
cd files
zip -x \*.pytest_cache\* \*.cache\* \*__pycache__\* @../../../.gitignore -r ../gradescope.zip *
cd ..