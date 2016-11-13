#!/bin/bash
ROOT=$(cd $(dirname $(dirname $0)); pwd)
set -ex
which python
python --version
pip install -qr $ROOT/config/requirements-docs.txt
sphinx-apidoc -f src/backend/rpaper -o docs
(cd docs; make html)
