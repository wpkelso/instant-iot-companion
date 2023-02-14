#!/bin/bash

mkdir log

python3 -m venv venv
source venv/bin/activate

venv/bin/pip install PyQt5 pyserial hatch
