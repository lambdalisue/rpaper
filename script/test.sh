#!/bin/bash
ROOT=$(cd $(dirname $(dirname $0)); pwd)
set -ex
which python
python --version
pip install -qr $ROOT/config/requirements-test.txt
mypy --silent-imports src/rpaper/core
mypy --silent-imports src/rpaper/apps
flake8
coverage run --source=src/rpaper src/manage.py test rpaper
coverage report
