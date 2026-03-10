FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc default-libmysqlclient-dev pkg-config && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY api_gateway/ /app/
CMD sh -c "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"
