# LAB02 — Docker Containerization

## Docker Best Practices Applied

### Non-root User
Container runs as non-root user for better security and reduced attack surface.

### Layer Caching
requirements.txt copied before application code to cache dependency installation layers.

### Minimal Base Image
python:3.13-slim chosen for smaller image size and reduced vulnerabilities.

### .dockerignore
Unnecessary files excluded from build context to reduce image size and speed up builds.

---

## Image Information & Decisions

Base Image: python:3.13-slim  
Reason: lightweight, secure, production-friendly.

Estimated Final Image Size: ~150-200MB depending on system.

Layer Structure:
1. Base image
2. Dependencies installation
3. Application copy
4. Runtime execution

---

## Build & Run Process

### Build

docker build -t devops-info-service .

### Run

docker run -p 5000:5000 devops-info-service

### Test

curl http://localhost:5000/
curl http://localhost:5000/health

Docker Hub URL:
https://hub.docker.com/r/maksimmenshikh/devops-info-service

---

## Technical Analysis

Layer order improves caching efficiency and reduces rebuild times.

Running containers as non-root prevents privilege escalation risks.

.dockerignore reduces build context size, speeding up builds.

---

## Challenges & Solutions

### Docker Engine Not Running
Solved by starting Docker Desktop.

### Authorization Errors
Solved by using docker login before pulling or pushing images.
