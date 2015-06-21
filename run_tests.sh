#!/bin/bash
apt-get update
apt-get -y install curl python
curl -s https://bootstrap.pypa.io/get-pip.py | python -
pip install -r requirements.txt
pip install coverage pytest
python setup.py test
