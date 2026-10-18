#!/usr/bin/env bash
set -o errexit

echo "=== BUOC 1: Cai dat thu vien ==="
pip install -r requirements.txt

echo "=== BUOC 2: Thu thap file static ==="
python manage.py collectstatic --no-input

echo "=== BUOC 3: Chay migration ==="
python manage.py migrate

echo "=== BUOC 4: Nap du lieu vao database ==="
python seed_data.py

echo "=== BUILD HOAN TAT ==="
