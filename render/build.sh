#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

pip install --upgrade pip
pip install -r requirements/production.txt
# python /app/manage.py collectstatic --noinput
python /app/manage.py migrate
