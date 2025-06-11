# !/bin/bash

wget -qO- https://astral.sh/uv/install.sh | sh
export PATH=/home/$USER/.local/bin:$PATH

uv venv
uv run pip install .

uv run python start_server.py