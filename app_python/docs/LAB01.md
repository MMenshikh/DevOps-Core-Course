# LAB01 --- DevOps Info Service

## Framework Selection

For this lab, **Flask 3.1.0** was selected as the web framework.

### Why Flask?

Flask is a lightweight, flexible, and beginner-friendly Python web
framework. It allows rapid development of REST APIs with minimal
boilerplate while still being powerful enough for production use.

Key reasons for choosing Flask: - Simple and clean API - Minimal setup
and configuration - Large community and ecosystem - Easy integration
with Docker, CI/CD, and Kubernetes - Ideal for microservices and
DevOps-oriented projects

### Comparison with Alternatives

  ------------------------------------------------------------------------------
  Framework           Pros             Cons         Reason Not Chosen
  ------------------- ---------------- ------------ ----------------------------
  Flask               Simple,          No built-in  **Chosen**
                      lightweight,     async, fewer 
                      flexible         built-ins    

  FastAPI             Async, auto      More         Overkill for current lab
                      OpenAPI docs,    complex,     
                      high performance async        
                                       complexity   

  Django              Full-featured,   Heavy,       Too heavy for microservice
                      ORM, admin panel complex,     
                                       monolithic   
  ------------------------------------------------------------------------------

Flask provides the perfect balance between simplicity and production
readiness for this lab.

------------------------------------------------------------------------

## Best Practices Applied

### 1. Clean Code Organization

Functions were separated logically: - `get_system_info()` --- collects
system information - `get_uptime()` --- calculates service uptime -
Endpoint handlers contain minimal logic

**Code Example:**

``` python
def get_system_info():
    return {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "architecture": platform.machine(),
        "cpu_count": os.cpu_count(),
        "python_version": platform.python_version()
    }
```

**Why Important:**\
Improves readability, maintainability, and testability of the code.

------------------------------------------------------------------------

### 2. Configuration via Environment Variables

``` python
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
```

**Why Important:**\
Allows flexible configuration across different environments (local,
Docker, CI/CD, Kubernetes) without changing the code.

------------------------------------------------------------------------

### 3. Logging

``` python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

**Why Important:**\
Logging is critical for debugging, monitoring, and incident
investigation in production systems.

------------------------------------------------------------------------

### 4. Error Handling

``` python
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "message": "Endpoint does not exist"
    }), 404
```

**Why Important:**\
Provides predictable API behavior and improves client-side debugging.

------------------------------------------------------------------------

## API Documentation

### GET /

Returns full service, system, runtime, and request information.

**Request Example:**

``` bash
curl http://localhost:5000/
```

**Response Example:**

``` json
{
  "service": {...},
  "system": {...},
  "runtime": {...},
  "request": {...},
  "endpoints": [...]
}
```

------------------------------------------------------------------------

### GET /health

Health-check endpoint used for monitoring and readiness probes.

**Request Example:**

``` bash
curl http://localhost:5000/health
```

**Response Example:**

``` json
{
  "status": "healthy",
  "timestamp": "...",
  "uptime_seconds": 120
}
```

------------------------------------------------------------------------

## Testing Evidence

The following screenshots demonstrate the correct functioning of the
application:

-   Main endpoint (`/`) returning full JSON output
-   Health check endpoint (`/health`) returning service health
-   Pretty-printed formatted JSON output

Screenshots are available in:

    docs/screenshots/

------------------------------------------------------------------------

## Challenges & Solutions

### Challenge 1 --- JSON Structure Consistency

**Problem:**\
Ensuring that the returned JSON exactly matches the required structure.

**Solution:**\
Careful comparison with the provided specification and manual testing
using browser and curl to validate field names and structure.

------------------------------------------------------------------------

### Challenge 2 --- Uptime Calculation

**Problem:**\
Accurately calculating service uptime since application start.

**Solution:**\
Saved application start time using `datetime.now(timezone.utc)` and
calculated the difference on every request.

------------------------------------------------------------------------

### Challenge 3 --- Cross-platform Compatibility

**Problem:**\
Ensuring the application works consistently on Windows, Linux, and
macOS.

**Solution:**\
Used only standard Python libraries (`platform`, `socket`, `os`) which
are fully cross-platform.

------------------------------------------------------------------------

## GitHub Community

Starring repositories helps support open-source developers and improves
project visibility, encouraging community contributions.

Following developers and classmates helps build professional
connections, discover new tools and projects, and learn from others'
experience, which is essential for growth in software engineering and
DevOps.

------------------------------------------------------------------------

## Conclusion

This lab established a solid foundation for future DevOps tasks
including containerization, CI/CD pipelines, monitoring, and Kubernetes
deployments. The implemented service follows clean code principles,
production-ready practices, and proper documentation standards.
