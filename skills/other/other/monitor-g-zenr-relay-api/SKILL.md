---
name: monitor
description: Set up observability — structured logging, health probes, metrics, and alerting (Marcus Chen's workflow)
disable-model-invocation: true
---

Set up monitoring and observability: $ARGUMENTS

## 1. Structured Logging Audit
Verify the current logging setup:
- [ ] Consistent log format across all modules
- [ ] Level: `INFO` by default, `DEBUG` when debug mode enabled
- [ ] No `print()` statements in source root
- [ ] All loggers use `logging.getLogger(__name__)`
- [ ] Project's audit logger used for state changes

### Log levels used correctly:
| Level | Used For |
|-------|----------|
| DEBUG | Verbose troubleshooting (protocol commands, request details) |
| INFO | Normal operations (startup, shutdown, state changes) |
| WARNING | Recoverable issues (resource not found, degraded mode) |
| ERROR | Failures that need attention (communication errors) |

## 2. Health Endpoint Verification
Verify the health endpoint returns appropriate status information:
- [ ] Responds within 200ms (load balancer requirement)
- [ ] Bypasses authentication
- [ ] Returns degraded status when external resource is disconnected
- [ ] Returns correct version from config

## 3. Readiness Probe
Consider adding a readiness endpoint that checks:
- Service is initialized
- External resource is connected and responsive
- Rate limiter is functional

## 4. Request Logging Middleware
Consider adding request/response logging for production debugging:
- Log method, path, status code, and response time for every request
- Don't log request/response bodies (may contain sensitive data)
- Use a dedicated access logger

## 5. Metrics Endpoint (optional)
If Prometheus/metrics are needed:
- Request count by endpoint and status code
- Request latency histogram
- External resource connection state gauge
- Active entity states gauge

## 6. Docker Health Integration
Verify Dockerfile HEALTHCHECK matches the health endpoint URL (see project config).

## Output
For each section, report:
- **CONFIGURED**: Already in place and working
- **ADDED**: New monitoring capability implemented
- **RECOMMENDED**: Optional improvement (describe what and why)