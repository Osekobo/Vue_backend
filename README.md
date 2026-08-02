# Vue Backend

A FastAPI-based backend service for a retail and sales workflow, with user authentication, product management, sales processing, receipt generation, payment integration, and observability support.

## Overview

This repository powers the backend API for the Vue frontend and provides the core business logic for:

- user registration and login
- product catalog operations
- sales and purchase flow
- receipt/PDF creation
- Cloudinary-based file uploads
- M-Pesa integration for payments
- Prometheus and Grafana monitoring

## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT-based authentication
- Docker Compose for local orchestration
- Prometheus + Grafana for monitoring

## Project Structure

- `main.py` — application entry point and API routes
- `models.py` — SQLAlchemy models and database schema
- `jsonmap.py` — request/response mapping schemas
- `myjwt.py` — JWT helpers, auth dependencies, and password utilities
- `mpesa.py` — M-Pesa STK push helpers
- `generate_pdf.py` — receipt/PDF generation
- `cloudinary_upload.py` — Cloudinary upload logic
- `send_email.py` — outbound email support
- `prometheus/` — Prometheus configuration
- `receipts/` — generated receipt output
- `docker-compose.yaml` — service orchestration for the app, database, Prometheus, and Grafana

## Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the application locally

```bash
python main.py
```

The API will typically be available at:

- `http://localhost:8000`

## Docker Setup

To start the full stack with Docker Compose:

```bash
docker-compose up --build
```

This brings up:

- the FastAPI backend
- PostgreSQL
- Prometheus
- Grafana
- Node Exporter

## API Documentation

Swagger/OpenAPI documentation is available at:

- `http://164.90.221.47:8000/docs`

## Monitoring

The project includes monitoring endpoints and dashboards for operational visibility:

- Grafana: `http://164.90.221.47:3000`
- Prometheus: `http://164.90.221.47:9090`

## Notes

This service is structured as a production-oriented FastAPI backend with authentication, commerce workflows, reporting helpers, and monitoring integration. It is well-suited for a business application that needs secure API access, payment handling, and operational observability.
