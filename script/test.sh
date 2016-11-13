#!/bin/bash
ROOT=$(cd $(dirname $(dirname $0)); pwd)
set -ex
which python
python --version
pip install -qr $ROOT/config/requirements-test.txt
mypy --silent-imports src/backend/rpaper/core
mypy --silent-imports src/backend/rpaper/apps
flake8
coverage run --source=src/backend/rpaper src/backend/manage.py test rpaper
coverage report
