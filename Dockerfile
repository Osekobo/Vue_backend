#        (This is for flask only)
# FROM tiangolo/uwsgi-nginx-flask:python3.11 
# COPY requirements.txt /tmp/
# RUN pip install -U pip
# RUN pip install -r /tmp/requirements.txt
# RUN apt-get update
# COPY . /app

#        (For FastAPI use this one)
FROM python:3.11-slim
WORKDIR /app
# Install build dependencies and clean up in one layer
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy application code
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]