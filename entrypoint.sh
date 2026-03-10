#!/bin/bash
set -e

echo "Waiting for MySQL to be ready..."
until python -c "
import os, MySQLdb
MySQLdb.connect(
    host=os.environ.get('DB_HOST', 'mysql'),
    port=int(os.environ.get('DB_PORT', '3306')),
    user=os.environ.get('DB_USER', 'root'),
    passwd=os.environ.get('DB_PASSWORD', '123456'),
)
" 2>/dev/null; do
    echo "MySQL not ready, retrying in 2s..."
    sleep 2
done
echo "MySQL is ready!"

echo "Running migrations..."
python manage.py makemigrations --noinput 2>/dev/null || true
python manage.py migrate --noinput

echo "Starting server..."
exec "$@"
