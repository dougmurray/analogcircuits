#!/usr//bin/env zsh
# Script to test module via python virtual environment
# Run as source moduletest.sh
echo "Module test running..."
python3 -m venv .venv
source .venv/bin/activate
pip3 install numpy
pip3 install matplotlib
pip3 install -e .
# pip3 freeze
# python3
# import analogcircuits
# exit()
# deactivate
# rm -R .venv/