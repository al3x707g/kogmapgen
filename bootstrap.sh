#!/usr/bin/env bash

# Delete existing venv if it exists
if [ -d "venv" ]; then
  rm -rf .venv
fi

# Create new venv and install dependencies
python -m venv .venv
pip install -r requirements.txt