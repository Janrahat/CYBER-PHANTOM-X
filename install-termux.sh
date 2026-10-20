#!/data/data/com.termux/files/usr/bin/bash
set -e
pkg update -y
pkg install -y python
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo 'Installed. Run: python main.py'
