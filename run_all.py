#!/usr/bin/env python
"""
Start all microservices on their designated ports.
Usage: python run_all.py
"""
import subprocess
import sys
import os
import time

SERVICES = [
    ('staff_service', 8001),
    ('manager_service', 8002),
    ('customer_service', 8003),
    ('catalog_service', 8004),
    ('book_service', 8005),
    ('cart_service', 8006),
    ('order_service', 8007),
    ('ship_service', 8008),
    ('pay_service', 8009),
    ('comment_rate_service', 8010),
    ('recommender_ai_service', 8011),
    ('auth_service', 8012),
    ('api_gateway', 8000),
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    processes = []
    for service, port in SERVICES:
        service_dir = os.path.join(BASE_DIR, service)
        manage_py = os.path.join(service_dir, 'manage.py')
        if not os.path.exists(manage_py):
            print(f"[SKIP] {service}")
            continue
        print(f"[START] {service} on port {port}")
        proc = subprocess.Popen(
            [sys.executable, manage_py, 'runserver', f'0.0.0.0:{port}'],
            cwd=service_dir,
        )
        processes.append((service, proc))
        time.sleep(0.5)

    print(f"\n{'='*50}")
    print("All services started. Press Ctrl+C to stop.")
    print(f"{'='*50}")
    print("API Gateway: http://localhost:8000/api/")
    print("Health Check: http://localhost:8000/api/health/")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping all services...")
        for name, proc in processes:
            proc.terminate()
        for name, proc in processes:
            proc.wait()
        print("All services stopped.")


if __name__ == '__main__':
    main()
