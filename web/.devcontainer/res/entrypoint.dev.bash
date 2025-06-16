# !/bin/bash

python3.12 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install .

python main.py
