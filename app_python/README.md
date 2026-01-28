# DevOps Info Service

A lightweight web service that provides detailed information about
itself and its runtime environment.\

------------------------------------------------------------------------

## Overview

DevOps Info Service is a Python-based web application that exposes REST
API endpoints for retrieving:

-   Service metadata
-   System information (OS, CPU, Python version, hostname)
-   Runtime statistics (uptime, current time, timezone)
-   Request details (client IP, HTTP method, user agent)

The service is designed to be simple, extensible, and production-ready,
following best DevOps and software engineering practices.

------------------------------------------------------------------------

## Prerequisites

-   Python **3.11+**
-   pip
-   Virtual environment support (`venv`)

### Dependencies

All dependencies are listed in `requirements.txt`:

-   Flask 3.1.0

------------------------------------------------------------------------

## Installation

Create and activate a virtual environment, then install dependencies:

``` bash
python -m venv venv
source venv/bin/activate    # Linux / macOS
# venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

------------------------------------------------------------------------

## Running the Application

Run the service using the default configuration:

``` bash
python app.py
```

Run with custom configuration:

``` bash
PORT=8080 python app.py
HOST=127.0.0.1 PORT=3000 python app.py
```

Once running, the service will be available at:

    http://localhost:5000

------------------------------------------------------------------------

## API Endpoints

### GET /

Returns detailed service, system, runtime, and request information.

**Example:**

``` bash
curl http://localhost:5000/
```

------------------------------------------------------------------------

### GET /health

Simple health-check endpoint used for monitoring and readiness probes.

**Example:**

``` bash
curl http://localhost:5000/health
```

------------------------------------------------------------------------

## Configuration

The application is configured via environment variables:

  Variable   Default   Description
  ---------- --------- -------------------------
  HOST       0.0.0.0   Server bind address
  PORT       5000      Server listening port
  DEBUG      False     Enable Flask debug mode

**Example:**

``` bash
HOST=127.0.0.1 PORT=8080 DEBUG=true python app.py
```