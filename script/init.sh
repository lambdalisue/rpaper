#!/bin/bash
ROOT=$(cd $(dirname $(dirname $0)); pwd)
set -ex
pip install -r $ROOT/config/requirements.txt --upgrade
npm install
