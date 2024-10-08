#!/bin/bash

# Check if Node.js is installed
if ! command -v node &> /dev/null
then
    echo "Node.js is not installed. Please install Node.js before running this script."
    exit 1
fi


# Install Angular CLI
echo "Installing Angular CLI..."
npm install -g @angular/cli

# Check if installation was successful
if ! command -v ng &> /dev/null
then
    echo "Angular CLI installation failed. Please check your npm configuration and try again."
    exit 1
fi

echo "Angular CLI installed successfully."

# Navigate to the project directory
# Replace 'your-project-directory' with the actual path to your Angular project
cd "./RpStudio" || exit

# Install project dependencies
echo "Installing project dependencies..."
npm install

# Launch the local development server
echo "Launching the Angular development server..."
ng serve
