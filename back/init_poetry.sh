#!/bin/bash

# Script to install Poetry, set up the environment, and activate it

# Define the path to pyproject.toml
PYPROJECT_PATH="RpStudio/pyproject.toml"

# 1. Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 2. Add Poetry to PATH (you may want to add this to your .bashrc or .zshrc)
export PATH="$HOME/.local/bin:$PATH"

# 3. Check if pyproject.toml exists at the specified location
if [ ! -f "$PYPROJECT_PATH" ]; then
    echo "Error: pyproject.toml not found at $PYPROJECT_PATH"
    exit 1
fi

# 4. Change to the directory containing pyproject.toml
cd "$(dirname "$PYPROJECT_PATH")" || exit

# 5. Install dependencies
poetry install

# 6. Activate the virtual environment
poetry shell

echo "Poetry environment is set up and activated. You can now run your FastAPI app."