#!/bin/bash

# Script to launch the FastAPI app

# Define the path to the project directory
PROJECT_DIR="RpStudio"

# Check if main.py exists in the project directory
if [ ! -f "$PROJECT_DIR/main.py" ]; then
    echo "Error: main.py not found in $PROJECT_DIR. Please create your FastAPI application in main.py"
    exit 1
fi

# Change to the project directory
cd "$PROJECT_DIR" || exit

# Activate the Poetry virtual environment and run the FastAPI app
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000