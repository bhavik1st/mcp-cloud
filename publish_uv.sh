#!/bin/bash

# Clean previous builds
rm -rf src/dist src/build src/*.egg-info

# Install uv if not already installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Build the package
cd src && uv pip install setuptools wheel build
python setup.py sdist bdist_wheel

# Upload to PyPI using .pypirc configuration
uv pip install twine
python -m twine upload dist/*

echo "Package published successfully using uv!" 