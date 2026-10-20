#!/usr/bin/env bash
set -e
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo 'Installed. Run: source .venv/bin/activate && python main.py'
