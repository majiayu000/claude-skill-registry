---
name: endpoint-validator
description: "Deterministic API endpoint validation with pass/fail reporting."
user-invocable: false
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Edit
routing:
  triggers:
    - "validate endpoints"
    - "smoke test API"
    - "health check endpoints"
    - "test endpoint"
    - "check API"
    - "smoke test"
  category: infrastructure
  not_for: "process/service uptime or daemon liveness (use service-health-check); only HTTP/API endpoint request validation"
  pairs_with:
    - service-health-check
    - e2e-testing
---

# Endpoint Validator Skill

Deterministic HTTP endpoint validation following a **Discover, Validate, Report** pattern. Finds endpoints, tests each against expectations, and produces machine-readable results with clear pass/fail verdicts and CI-compatible exit codes.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| Security header WARNs, HSTS/CSP/X-Frame issues | `security-headers.md` | Routes to the matching deep reference |
| Config errors, hardcoded IPs, timeout problems | `endpoint-config-preferred-patterns.md` | Routes to the matching deep reference |
| 401/403 failures, Bearer/API-key/cookie auth | `auth-endpoint-patterns.md` | Routes to the matching deep reference |

## Instructions

### Phase 1: DISCOVER

**Goal**: Locate or receive endpoint definitions before making any requests.

**Step 1: Read repository CLAUDE.md**

Check for and follow any repository-level CLAUDE.md before running validation. It may contain base URL conventions, environment variable names, or endpoint paths relevant to the project.

**Step 2: Search for endpoint configuration**

Look for definitions in priority order:
1. `endpoints.json` in project root
2. `tests/endpoints.json`
3. Inline specification provided by user or calling agent

Prefer config files checked into version control over ad-hoc endpoint lists. Manually listing endpoints every run leads to drift and missed endpoints.

**Step 3: Parse and validate configuration**

Configuration must contain `base_url` and at least one endpoint:

```json
{
  "base_url": "http://localhost:8000",
  "endpoints": [
    {"path": "/health", "expect_status": 200},
    {"path": "/api/v1/users", "expect_key": "data", "timeout": 10},
    {"path": "/api/v1/search?q=test", "max_time": 2.0}
  ]
}
```

Each endpoint supports these fields:
- `path` (required): URL path appended to base_url
- `expect_status` (default: 200): Expected HTTP status code
- `expect_key` (optional): Top-level JSON key that must exist in response. Only top-level key presence is checked -- full JSON schema validation is out of scope.
- `timeout` (default: 5): Request timeout in seconds. The 5-second default prevents hanging on unresponsive endpoints.
- `max_time` (optional): Fail if response exceeds this threshold in seconds
- `method` (optional): HTTP method. Defaults to GET. POST/PUT/DELETE require explicit configuration with a request body -- send mutating requests only when the user explicitly configures them.
- `headers` (optional): Additional headers per endpoint (e.g., Accept, Content-Type, Authorization)

If `base_url` points to a production host and the config includes POST/PUT/DELETE endpoints, warn the user before proceeding. Mutating production data or triggering rate limits during a smoke test is a serious risk. Use staging environments for write operations; reserve production for GET-only health checks.

Use hostnames or environment variables instead of hardcoded IP addresses in `base_url` (e.g., `http://192.168.1.42:8000`). They break on every other machine and CI environment. Use `localhost` with a configurable port or environment variables instead.

**Step 4: Confirm base URL is reachable**

Make a single request to `base_url` before running the full suite. If unreachable, report immediately rather than failing every endpoint individually.

**Gate**: Configuration parsed, base URL reachable, at least one endpoint defined. Proceed only when gate passes.

### Phase 2: VALIDATE

**Verification means execution, not reasoning.** Run the command. Do not reason about whether the command would pass. Do not summarize the expected output. Execute the check, paste the exit code, paste the relevant output. A verification phase that produces a verdict without an observed tool result is not a verification — it is a guess with a rigor aesthetic.

**Goal**: Test each endpoint against its expected criteria and collect structured results.

**Step 1: Execute requests sequentially**

Test endpoints one at a time for predictable, reproducible output. For each endpoint:
1. Construct full URL from `base_url` + `path`
2. Send request with configured method (GET by default) and timeout
3. Record status code, response time, and body
4. Display each result as it completes so the user sees progress

This skill sends one request per endpoint. It is not a load tester or stress tester -- it validates contract compliance, not throughput.

**Step 2: Evaluate against expectations**

For each response, check in order:
1. **Status code**: Does it match `expect_status`? If not, mark FAIL.
2. **JSON key**: If `expect_key` set, parse JSON and check key exists. If missing or not valid JSON, mark FAIL.
3. **Response time**: If `max_time` set and elapsed exceeds it, mark SLOW. Flag slow endpoints -- they indicate degradation that becomes failure under load.
4. **Security headers**: Check response headers for common security headers. Report missing headers as WARN (not FAIL):
   - `Strict-Transport-Security` -- HSTS enforcement (expected on HTTPS endpoints)
   - `Content-Security-Policy` -- XSS mitigation
   - `X-Content-Type-Options` -- should be `nosniff`
   - `X-Frame-Options` -- clickjacking prevention (or CSP `frame-ancestors`)

Skip security header checks for localhost/127.0.0.1 endpoints (development environments typically omit these). Only check on non-localhost base URLs unless explicitly configured.

**Step 3: Handle failures gracefully**

- Connection refused: Record as FAIL with "Connection refused" error
- Timeout exceeded: Record as FAIL with "Timeout after Ns" error
- Invalid JSON when `expect_key` set: Record as FAIL with "Invalid JSON response"
- Unexpected exception: Record as FAIL with exception message

**Gate**: All endpoints tested. Every result has a clear PASS, FAIL, or SLOW verdict. Proceed only when gate passes.

### Phase 3: REPORT

**Goal**: Produce structured, machine-readable output with summary statistics.

**Step 1: Format individual results**

```
ENDPOINT VALIDATION REPORT
==========================
Base URL: http://localhost:8000
Endpoints: 15 tested

RESULTS:
  /api/health                    200 OK      45ms
  /api/users                     200 OK     123ms
  /api/products                  500 FAIL   "Internal Server Error"
  /api/slow                      200 SLOW   3.2s > 2.0s threshold

SECURITY HEADERS (non-localhost only):
  /api/health                    WARN  Missing: Content-Security-Policy, X-Frame-Options
  /api/users                     OK    All security headers present
  /api/products                  SKIP  (endpoint failed)
```

**Step 2: Produce summary**

```
SUMMARY:
  Passed: 13/15 (86.7%)
  Failed: 1 (status error)
  Slow: 1 (exceeded threshold)
  Security header warnings: 3 endpoints missing headers
```

**Step 3: Set exit code**

- Exit 0 if all endpoints passed (SLOW counts as pass unless `max_time` was set)
- Exit 1 if any endpoint failed

**Gate**: Report printed, exit code set. Validation complete.

### Examples

#### Example 1: Pre-Deployment Health Check
User says: "Validate all endpoints before we deploy"
Actions:
1. Find `endpoints.json` in project root (DISCOVER)
2. Test each endpoint, collect status codes and times (VALIDATE)
3. Print report, exit 0 if all pass (REPORT)
Result: Structured pass/fail report with CI-compatible exit code

#### Example 2: Smoke Test After Migration
User says: "Check if the API is still working after the database migration"
Actions:
1. Read endpoint config, confirm base URL reachable (DISCOVER)
2. Hit each endpoint, check status and expected keys (VALIDATE)
3. Surface any failures with error details (REPORT)
Result: Quick verification that migration did not break API contracts

---

## Error Handling

### Error: "Base URL Unreachable"
Cause: Service not running, wrong port, or network issue
Solution:
1. Verify service is running (`ps aux`, `docker ps`, or equivalent)
2. Confirm port matches config (`netstat -tlnp` or `ss -tlnp`)
3. Check for firewall rules or container networking issues

### Error: "All Endpoints Timeout"
Cause: Service overwhelmed, wrong host, or proxy misconfiguration
Solution:
1. Test a single endpoint manually with `curl -v`
2. Increase timeout values in config if service is legitimately slow
3. Check if a reverse proxy or load balancer is intercepting requests

### Error: "JSON Parse Failure on expect_key Check"
Cause: Endpoint returns HTML, XML, or empty body instead of JSON
Solution:
1. Verify endpoint actually returns JSON (check Content-Type header)
2. Remove `expect_key` if endpoint legitimately returns non-JSON
3. Check if authentication is required (HTML login page returned)

---

## Reference Loading

| Task Type | Load This Reference |
|-----------|-------------------|
| Security header WARNs, HSTS/CSP/X-Frame issues | `references/security-headers.md` |
| Config errors, hardcoded IPs, timeout problems | `references/endpoint-config-preferred-patterns.md` |
| 401/403 failures, Bearer/API-key/cookie auth | `references/auth-endpoint-patterns.md` |

---

## References

### CI/CD Integration

```yaml
# GitHub Actions example
# TODO: scripts/validate_endpoints.py not yet implemented
# Manual alternative: use curl to validate endpoints from endpoints.json
- name: Validate API endpoints
  run: |
    jq -r '.endpoints[].path' endpoints.json | while read path; do
      curl -sf "$BASE_URL$path" > /dev/null && echo "PASS: $path" || echo "FAIL: $path"
    done
```

```bash
# Pre-deployment gate
# TODO: scripts/validate_endpoints.py not yet implemented
# Manual alternative: iterate endpoints.json with curl
jq -r '.endpoints[].path' endpoints.json | while read path; do
  curl -sf "http://localhost:8000$path" > /dev/null || { echo "FAIL: $path"; exit 1; }
done
```
