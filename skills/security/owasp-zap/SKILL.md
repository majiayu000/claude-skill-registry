---
name: owasp-zap
description: Run OWASP ZAP dynamic application security testing
argument-hint: "<target-url> [--mode=baseline|full]"
tags: [security, dast, owasp, zap, devsecops]
user-invocable: true
---

# OWASP ZAP DAST Scan

Run dynamic application security testing against a running API.

## What To Do

1. **Baseline scan** (fast, passive only):
   ```bash
   docker run -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://localhost:5000/swagger/v1/swagger.json -J zap-report.json
   ```

2. **API scan** (OpenAPI-aware):
   ```bash
   docker run -t ghcr.io/zaproxy/zaproxy:stable zap-api-scan.py -t http://localhost:5000/swagger/v1/swagger.json -f openapi -J zap-api-report.json
   ```

3. **Full scan** (active + passive):
   ```bash
   docker run -t ghcr.io/zaproxy/zaproxy:stable zap-full-scan.py -t http://localhost:5000 -J zap-full-report.json
   ```

4. **CI Integration**: Run baseline scan on every PR, full scan nightly.

## Arguments
- `<target-url>`: URL of running application or OpenAPI spec
- `--mode=<baseline|api|full>`: Scan intensity