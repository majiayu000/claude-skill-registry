---
name: api-dev
description: Scaffold, test, document, and debug REST and GraphQL APIs. Use when the user needs to create API endpoints, write integration tests, generate OpenAPI specs, test with curl, mock APIs, or troubleshoot HTTP issues.
metadata: {"clawdbot":{"emoji":"🔌","requires":{"anyBins":["curl","node","python3"]},"os":["linux","darwin","win32"]}}
---

# API Development

Build, test, document, and debug HTTP APIs from the command line. Covers the full API lifecycle: scaffolding endpoints, testing with curl, generating OpenAPI docs, mocking services, and debugging.

## When to Use

- Scaffolding new REST or GraphQL endpoints
- Testing APIs with curl or scripts
- Generating or validating OpenAPI/Swagger specs
- Mocking external APIs for development
- Debugging HTTP request/response issues
- Load testing endpoints

## Testing APIs with curl

### GET requests

```bash
# Basic GET
curl -s https://api.example.com/users | jq .

# With headers
curl -s -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  https://api.example.com/users | jq .

# With query params
curl -s "https://api.example.com/users?page=2&limit=10" | jq .

# Show response headers too
curl -si https://api.example.com/users
```

### POST/PUT/PATCH/DELETE

```bash
# POST JSON
curl -s -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "Alice", "email": "alice@example.com"}' | jq .

# PUT (full replace)
curl -s -X PUT https://api.example.com/users/123 \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Updated", "email": "alice@example.com"}' | jq .

# PATCH (partial update)
curl -s -X PATCH https://api.example.com/users/123 \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice V2"}' | jq .

# DELETE
curl -s -X DELETE https://api.example.com/users/123

# POST form data
curl -s -X POST https://api.example.com/upload \
  -F "file=@document.pdf" \
  -F "description=My document"
```

### Debug requests

```bash
# Verbose output (see full request/response)
curl -v https://api.example.com/health 2>&1

# Show only response headers
curl -sI https://api.example.com/health

# Show timing breakdown
curl -s -o /dev/null -w "DNS: %{time_namelookup}s\nConnect: %{time_connect}s\nTLS: %{time_appconnect}s\nFirst byte: %{time_starttransfer}s\nTotal: %{time_total}s\n" https://api.example.com/health

# Follow redirects
curl -sL https://api.example.com/old-endpoint

# Save response to file
curl -s -o response.json https://api.example.com/data
```

## API Test Scripts

### Bash test runner

```bash
#!/bin/bash
# api-test.sh - Simple API test runner
BASE_URL="${1:-http://localhost:3000}"
PASS=0
FAIL=0

assert_status() {
  local method="$1" url="$2" expected="$3" body="$4"
  local args=(-s -o /dev/null -w "%{http_code}" -X "$method")
  if [ -n "$body" ]; then
    args+=(-H "Content-Type: application/json" -d "$body")
  fi
  local status
  status=$(curl "${args[@]}" "$BASE_URL$url")
  if [ "$status" = "$expected" ]; then
    echo "PASS: $method $url -> $status"
    ((PASS++))
  else
    echo "FAIL: $method $url -> $status (expected $expected)"
    ((FAIL++))
  fi
}

assert_json() {
  local url="$1" jq_expr="$2" expected="$3"
  local actual
  actual=$(curl -s "$BASE_URL$url" | jq -r "$jq_expr")
  if [ "$actual" = "$expected" ]; then
    echo "PASS: GET $url | jq '$jq_expr' = $expected"
    ((PASS++))
  else
    echo "FAIL: GET $url | jq '$jq_expr' = $actual (expected $expected)"
    ((FAIL++))
  fi
}

# Health check
assert_status GET /health 200

# CRUD tests
assert_status POST /api/users 201 '{"name":"Test","email":"test@test.com"}'
assert_status GET /api/users 200
assert_json /api/users '.[-1].name' 'Test'
assert_status DELETE /api/users/1 204

# Auth tests
assert_status GET /api/admin 401
assert_status GET /api/admin 403  # with wrong role

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
```

### Python test runner

```python
#!/usr/bin/env python3
"""api_test.py - API integration test suite."""
import json, sys, urllib.request, urllib.error

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"
PASS = FAIL = 0

def request(method, path, body=None, headers=None):
    """Make an HTTP request, return (status, body_dict, headers)."""
    url = f"{BASE}{path}"
    data = json.dumps(body).encode() if body else None
    hdrs = {"Content-Type": "application/json", "Accept": "application/json"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        resp = urllib.request.urlopen(req)
        body = json.loads(resp.read().decode()) if resp.read() else None
    except urllib.error.HTTPError as e:
        return e.code, None, dict(e.headers)
    return resp.status, body, dict(resp.headers)

def test(name, fn):
    """Run a test function, track pass/fail."""
    global PASS, FAIL
    try:
        fn()
        print(f"  PASS: {name}")
        PASS += 1
    except AssertionError as e:
        print(f"  FAIL: {name} - {e}")
        FAIL += 1

def assert_eq(actual, expected, msg=""):
    assert actual == expected, f"got {actual}, expected {expected}. {msg}"

# --- Tests ---
print(f"Testing {BASE}\n")

test("GET /health returns 200", lambda: (
    assert_eq(request("GET", "/health")[0], 200)
))

test("POST /api/users creates user", lambda: (
    assert_eq(request("POST", "/api/users", {"name": "Test", "email": "t@t.com"})[0], 201)
))

test("GET /api/users returns array", lambda: (
    assert_eq(type(request("GET", "/api/users")[1]), list)
))

test("GET /api/notfound returns 404", lambda: (
    assert_eq(request("GET", "/api/notfound")[0], 404)
))

print(f"\nResults: {PASS} passed, {FAIL} failed")
sys.exit(0 if FAIL == 0 else 1)
```

## OpenAPI Spec Generation

### Generate from existing endpoints

```bash
# Scaffold an OpenAPI 3.0 spec from curl responses
# Run this, then fill in the details
cat > openapi.yaml << 'EOF'
openapi: "3.0.3"
info:
  title: My API
  version: "1.0.0"
  description: API description here
servers:
  - url: http://localhost:3000
    description: Local development
paths:
  /health:
    get:
      summary: Health check
      responses:
        "200":
          description: Service is healthy
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: ok
  /api/users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        "200":
          description: List of users
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: "#/components/schemas/User"
    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateUser"
      responses:
        "201":
          description: User created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "400":
          description: Validation error
  /api/users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        "200":
          description: User details
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "404":
          description: Not found
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        email:
          type: string
          format: email
        createdAt:
          type: string
          format: date-time
    CreateUser:
      type: object
      required:
        - name
        - email
      properties:
        name:
          type: string
        email:
          type: string
          format: email
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
EOF
```

### Validate OpenAPI spec

```bash
# Using npx (no install needed)
npx @redocly/cli lint openapi.yaml

# Quick check: is the YAML valid?
python3 -c "import yaml; yaml.safe_load(open('openapi.yaml'))" && echo "Valid YAML"
```

## Mock Server

### Quick mock with Python

```python
#!/usr/bin/env python3
"""mock_server.py - Lightweight API mock from OpenAPI-like config."""
import json, http.server, re, sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

# Define mock routes: (method, path_pattern) -> response
ROUTES = {
    ("GET", "/health"): {"status": 200, "body": {"status": "ok"}},
    ("GET", "/api/users"): {"status": 200, "body": [
        {"id": "1", "name": "Alice", "email": "alice@example.com"},
        {"id": "2", "name": "Bob", "email": "bob@example.com"},
    ]},
    ("POST", "/api/users"): {"status": 201, "body": {"id": "3", "name": "Created"}},
    ("GET", r"/api/users/\w+"): {"status": 200, "body": {"id": "1", "name": "Alice"}},
    ("DELETE", r"/api/users/\w+"): {"status": 204, "body": None},
}

class MockHandler(http.server.BaseHTTPRequestHandler):
    def _handle(self):
        for (method, pattern), response in ROUTES.items():
            if self.command == method and re.fullmatch(pattern, self.path.split('?')[0]):
                self.send_response(response["status"])
                if response["body"] is not None:
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(response["body"]).encode())
                else:
                    self.end_headers()
                return
        self.send_response(404)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"error": "Not found"}).encode())

    do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = _handle

    def log_message(self, fmt, *args):
        print(f"{self.command} {self.path} -> {args[1] if len(args) > 1 else '?'}")

print(f"Mock server on http://localhost:{PORT}")
http.server.HTTPServer(("", PORT), MockHandler).serve_forever()
```

Run: `python3 mock_server.py 8080`

## Node.js Express Scaffolding

### Minimal REST API

```javascript
// server.js - Minimal Express REST API
const express = require('express');
const app = express();
app.use(express.json());

// In-memory store
const items = new Map();
let nextId = 1;

// CRUD endpoints
app.get('/api/items', (req, res) => {
  const { page = 1, limit = 20 } = req.query;
  const all = [...items.values()];
  const start = (page - 1) * limit;
  res.json({ items: all.slice(start, start + +limit), total: all.length });
});

app.get('/api/items/:id', (req, res) => {
  const item = items.get(req.params.id);
  if (!item) return res.status(404).json({ error: 'Not found' });
  res.json(item);
});

app.post('/api/items', (req, res) => {
  const { name, description } = req.body;
  if (!name) return res.status(400).json({ error: 'name required' });
  const id = String(nextId++);
  const item = { id, name, description: description || '', createdAt: new Date().toISOString() };
  items.set(id, item);
  res.status(201).json(item);
});

app.put('/api/items/:id', (req, res) => {
  if (!items.has(req.params.id)) return res.status(404).json({ error: 'Not found' });
  const item = { ...req.body, id: req.params.id, updatedAt: new Date().toISOString() };
  items.set(req.params.id, item);
  res.json(item);
});

app.delete('/api/items/:id', (req, res) => {
  if (!items.has(req.params.id)) return res.status(404).json({ error: 'Not found' });
  items.delete(req.params.id);
  res.status(204).end();
});

// Error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal server error' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`API running on http://localhost:${PORT}`));
```

### Setup

```bash
mkdir my-api && cd my-api
npm init -y
npm install express
node server.js
```

## Debugging Patterns

### Check if port is in use

```bash
# Linux/macOS
lsof -i :3000
# or
ss -tlnp | grep 3000

# Kill process on port
kill $(lsof -t -i :3000)
```

### Test CORS

```bash
# Preflight request
curl -s -X OPTIONS https://api.example.com/users \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -I
```

### Watch for response time regressions

```bash
# Quick benchmark (10 requests)
for i in $(seq 1 10); do
  curl -s -o /dev/null -w "%{time_total}\n" http://localhost:3000/api/users
done | awk '{sum+=$1; if($1>max)max=$1} END {printf "Avg: %.3fs, Max: %.3fs\n", sum/NR, max}'
```

### Inspect JWT tokens

```bash
# Decode JWT payload (no verification)
echo "$TOKEN" | cut -d. -f2 | base64 -d 2>/dev/null | jq .
```

## Tips

- Use `jq` for JSON response processing: `curl -s url | jq '.items[] | {id, name}'`
- Set `Content-Type` header on every request with a body - missing it causes silent 400s
- Use `-w '\n'` with curl to ensure output ends with a newline
- For large response bodies, pipe to `jq -C . | less -R` for colored paging
- Test error paths: invalid JSON, missing fields, wrong types, unauthorized, not found
- For WebSocket testing: `npx wscat -c ws://localhost:3000/ws`
