#!/bin/bash

echo "Setting up Streamlit Starter Template..."

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export STREAMLIT_ENV="development"

echo "Setup complete! Run 'streamlit run main.py' to start the application."
