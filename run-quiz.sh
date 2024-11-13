#!/bin/bash

python3 -m venv myenv
source myenv/bin/activate
pip3 install pyyaml 

python3 ./tfquiz.py questions.yaml --total_questions "$1"
