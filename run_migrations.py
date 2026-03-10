#!/usr/bin/env python
"""
Run migrations for all microservices.
Usage: python run_migrations.py
"""
import subprocess
import os
import sys

SERVICES = [
    'staff_service',
    'manager_service',
    'customer_service',
    'catalog_service',
    'book_service',
    'cart_service',
    'order_service',
    'ship_service',
    'pay_service',
    'comment_rate_service',
    'recommender_ai_service',
    'api_gateway',
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_migrations():
    for service in SERVICES:
        service_dir = os.path.join(BASE_DIR, service)
        manage_py = os.path.join(service_dir, 'manage.py')
        if not os.path.exists(manage_py):
            print(f"[SKIP] {service} - manage.py not found")
            continue

        print(f"\n{'='*50}")
        print(f"[MIGRATE] {service}")
        print(f"{'='*50}")

        result = subprocess.run(
            [sys.executable, manage_py, 'makemigrations'],
            cwd=service_dir,
        )
        if result.returncode != 0:
            print(f"[ERROR] makemigrations failed for {service}")
            continue

        result = subprocess.run(
            [sys.executable, manage_py, 'migrate'],
            cwd=service_dir,
        )
        if result.returncode != 0:
            print(f"[ERROR] migrate failed for {service}")
            continue

        print(f"[OK] {service} migrated successfully")


if __name__ == '__main__':
    run_migrations()
