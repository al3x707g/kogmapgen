#!/usr/bin/env bash

# Delete existing venv if it exists
if [ -d "venv" ]; then
  rm -rf .venv
fi

# Create new venv and install dependencies
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt