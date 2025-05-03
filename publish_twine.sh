#!/bin/bash

# Clean previous builds
rm -rf src/dist src/build src/*.egg-info

# Install required packages
pip install --upgrade build twine setuptools wheel

# Build the package
cd src && python setup.py sdist bdist_wheel

# Upload to PyPI using .pypirc configuration
python -m twine upload dist/*

echo "Package published successfully using twine!" 