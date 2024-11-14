#!/bin/bash

python3 -m venv myenv
source myenv/bin/activate
pip3 install pyyaml openai

python3 add_question.py
