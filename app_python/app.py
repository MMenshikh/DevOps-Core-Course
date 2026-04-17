import os
import socket
import platform
import logging
import time
from datetime import datetime, timezone
from flask import Flask, jsonify, request
from pythonjsonlogger import jsonlogger
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from threading import Lock

# ---------------- LOGGING ----------------
logger = logging.getLogger(__name__)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# ---------------- APP ----------------
app = Flask(__name__)

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

START_TIME = datetime.now(timezone.utc)

# ---------------- VISITS STORAGE ----------------

DATA_DIR = "/data"
VISITS_FILE = os.path.join(DATA_DIR, "visits")

lock = Lock()

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

def read_visits():
    ensure_data_dir()
    if not os.path.exists(VISITS_FILE):
        return 0
    try:
        with open(VISITS_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 0

def write_visits(count):
    with open(VISITS_FILE, "w") as f:
        f.write(str(count))

def increment_visits():
    with lock:
        count = read_visits()
        count += 1
        write_visits(count)
        return count

# ---------------- METRICS ----------------

http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

http_requests_in_progress = Gauge(
    'http_requests_in_progress',
    'HTTP requests currently in progress'
)

endpoint_calls = Counter(
    'devops_info_endpoint_calls',
    'Endpoint calls',
    ['endpoint']
)

# ---------------- HELPERS ----------------

def get_uptime():
    delta = datetime.now(timezone.utc) - START_TIME
    seconds = int(delta.total_seconds())
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return {
        "seconds": seconds,
        "human": f"{hours} hours, {minutes} minutes"
    }

def get_system_info():
    return {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "cpu_count": os.cpu_count(),
        "python_version": platform.python_version()
    }

# ---------------- MIDDLEWARE ----------------

@app.before_request
def before_request():
    request.start_time = time.time()
    http_requests_in_progress.inc()

@app.after_request
def after_request(response):
    duration = time.time() - request.start_time

    http_requests_total.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code
    ).inc()

    http_request_duration_seconds.labels(
        method=request.method,
        endpoint=request.path
    ).observe(duration)

    http_requests_in_progress.dec()

    return response

# ---------------- ROUTES ----------------

@app.route("/")
def index():
    logger.info("request received", extra={
        "method": request.method,
        "path": request.path,
        "client_ip": request.remote_addr
    })

    endpoint_calls.labels(endpoint="/").inc()

    visits = increment_visits()
    uptime = get_uptime()

    return jsonify({
        "service": {
            "name": "devops-info-service",
            "version": "1.1.0",
            "description": "DevOps course info service",
            "framework": "Flask"
        },
        "visits": visits,
        "system": get_system_info(),
        "runtime": {
            "uptime_seconds": uptime["seconds"],
            "uptime_human": uptime["human"],
            "current_time": datetime.now(timezone.utc).isoformat(),
            "timezone": "UTC"
        },
        "request": {
            "client_ip": request.remote_addr,
            "user_agent": request.headers.get("User-Agent"),
            "method": request.method,
            "path": request.path
        }
    })

@app.route("/visits")
def visits():
    count = read_visits()

    endpoint_calls.labels(endpoint="/visits").inc()

    return jsonify({
        "visits": count
    })

@app.route("/health")
def health():
    uptime = get_uptime()

    logger.info("health check", extra={
        "status": "healthy",
        "uptime": uptime["seconds"]
    })

    endpoint_calls.labels(endpoint="/health").inc()

    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": uptime["seconds"]
    })

# ---------------- METRICS ENDPOINT ----------------

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

# ---------------- ERRORS ----------------

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "message": "Endpoint does not exist"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred"
    }), 500

# ---------------- MAIN ----------------

if __name__ == "__main__":
    logger.info("Starting DevOps Info Service...")
    app.run(host=HOST, port=PORT, debug=DEBUG)