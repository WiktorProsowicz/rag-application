#!/bin/bash

# This script should be run after the devcontainer is created.
# It's role is to establish the necessary environment for the
# user to start developing.

mkdir /home/appuser/data

python3.12 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -e .[dev]

cat .devcontainer/res/.bash_aliases >> ~/.bash_aliases
cat .devcontainer/res/.bashrc >> ~/.bashrc

