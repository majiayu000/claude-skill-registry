---
name: Postman API Testing
description: API testing skill using Postman and Newman, covering collections, environments, pre-request scripts, test scripts, and CI/CD integration with Newman.
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [postman, newman, api-testing, rest, collections, ci-cd]
testingTypes: [api]
frameworks: [postman]
languages: [javascript]
domains: [api]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt]
---

# Postman API Testing Skill

You are an expert QA engineer specializing in API testing with Postman and Newman. When the user asks you to create, review, or debug Postman collections and test scripts, follow these detailed instructions.

## Core Principles

1. **Collections as documentation** -- Well-organized collections serve as living API documentation.
2. **Environment-agnostic** -- Collections must work across dev, staging, and production via environment files.
3. **Test every response** -- Every request must have test scripts validating status, body, and headers.
4. **Chain requests** -- Use variables to pass data between requests for workflow testing.
5. **CI-ready** -- Collections must run via Newman in CI/CD pipelines.

## Project Structure

```
postman/
  collections/
    users-api.postman_collection.json
    products-api.postman_collection.json
    auth-api.postman_collection.json
    e2e-workflows.postman_collection.json
  environments/
    local.postman_environment.json
    staging.postman_environment.json
    production.postman_environment.json
  globals/
    global-variables.postman_globals.json
  data/
    users.csv
    products.json
  scripts/
    run-tests.sh
    newman-config.js
```

## Collection Organization

### Folder Structure

```
API Collection
  ├── Auth
  │     ├── Login
  │     ├── Register
  │     ├── Refresh Token
  │     └── Logout
  ├── Users
  │     ├── Create User
  │     ├── Get User by ID
  │     ├── Update User
  │     ├── Delete User
  │     └── List Users
  ├── Products
  │     ├── Create Product
  │     ├── Get Product
  │     ├── Search Products
  │     └── Delete Product
  └── Workflows
        ├── User Registration Flow
        └── Complete Purchase Flow
```

## Environment Variables

```json
{
  "name": "Staging",
  "values": [
    { "key": "baseUrl", "value": "https://staging-api.example.com", "enabled": true },
    { "key": "apiVersion", "value": "v1", "enabled": true },
    { "key": "adminEmail", "value": "admin@example.com", "enabled": true },
    { "key": "adminPassword", "value": "AdminPass123!", "enabled": true },
    { "key": "authToken", "value": "", "enabled": true },
    { "key": "userId", "value": "", "enabled": true },
    { "key": "productId", "value": "", "enabled": true }
  ]
}
```

## Pre-Request Scripts

### Dynamic Data Generation

```javascript
// Generate unique email for user creation
const timestamp = Date.now();
pm.variables.set("uniqueEmail", `test-${timestamp}@example.com`);
pm.variables.set("uniqueName", `TestUser_${timestamp}`);
pm.variables.set("requestId", pm.variables.replaceIn("{{$guid}}"));

// Generate random data
pm.variables.set("randomPrice", (Math.random() * 100 + 1).toFixed(2));
pm.variables.set("randomQuantity", Math.floor(Math.random() * 10) + 1);
```

### Authentication Token Management

```javascript
// Pre-request script to ensure we have a valid token
const tokenExpiry = pm.environment.get("tokenExpiry");
const currentTime = Date.now();

if (!tokenExpiry || currentTime > parseInt(tokenExpiry)) {
    // Token is expired or missing, get a new one
    const loginRequest = {
        url: `${pm.environment.get("baseUrl")}/api/auth/login`,
        method: "POST",
        header: {
            "Content-Type": "application/json",
        },
        body: {
            mode: "raw",
            raw: JSON.stringify({
                email: pm.environment.get("adminEmail"),
                password: pm.environment.get("adminPassword"),
            }),
        },
    };

    pm.sendRequest(loginRequest, (error, response) => {
        if (error) {
            console.error("Login failed:", error);
            return;
        }

        const jsonResponse = response.json();
        pm.environment.set("authToken", jsonResponse.token);
        // Set expiry to 55 minutes from now (assuming 1-hour token)
        pm.environment.set("tokenExpiry", String(Date.now() + 55 * 60 * 1000));
        console.log("Token refreshed successfully");
    });
}
```

### Request Signing

```javascript
// HMAC signature for API requests
const crypto = require("crypto-js");
const apiSecret = pm.environment.get("apiSecret");
const timestamp = new Date().toISOString();
const body = pm.request.body ? pm.request.body.raw : "";

const signature = crypto.HmacSHA256(
    `${pm.request.method}${pm.request.url}${timestamp}${body}`,
    apiSecret
).toString(crypto.enc.Hex);

pm.request.headers.add({
    key: "X-Timestamp",
    value: timestamp,
});
pm.request.headers.add({
    key: "X-Signature",
    value: signature,
});
```

## Test Scripts

### Status Code Validation

```javascript
// Basic status code check
pm.test("Status code is 200", () => {
    pm.response.to.have.status(200);
});

// Status code in range
pm.test("Status code is success", () => {
    pm.expect(pm.response.code).to.be.oneOf([200, 201]);
});

// Specific status for specific operations
pm.test("Resource created successfully", () => {
    pm.response.to.have.status(201);
});
```

### Response Body Validation

```javascript
const jsonData = pm.response.json();

pm.test("Response has required fields", () => {
    pm.expect(jsonData).to.have.property("id");
    pm.expect(jsonData).to.have.property("email");
    pm.expect(jsonData).to.have.property("name");
    pm.expect(jsonData).to.have.property("createdAt");
});

pm.test("Email matches request", () => {
    pm.expect(jsonData.email).to.eql(pm.variables.get("uniqueEmail"));
});

pm.test("Data types are correct", () => {
    pm.expect(jsonData.id).to.be.a("string");
    pm.expect(jsonData.email).to.be.a("string");
    pm.expect(jsonData.active).to.be.a("boolean");
    pm.expect(jsonData.createdAt).to.match(/^\d{4}-\d{2}-\d{2}/);
});

pm.test("Nested object validation", () => {
    pm.expect(jsonData.address).to.be.an("object");
    pm.expect(jsonData.address.city).to.be.a("string");
    pm.expect(jsonData.address.zip).to.match(/^\d{5}/);
});

pm.test("Array validation", () => {
    pm.expect(jsonData.items).to.be.an("array");
    pm.expect(jsonData.items).to.have.lengthOf.at.least(1);
    jsonData.items.forEach((item) => {
        pm.expect(item).to.have.property("id");
        pm.expect(item).to.have.property("name");
        pm.expect(item.price).to.be.above(0);
    });
});
```

### Header Validation

```javascript
pm.test("Response has correct content type", () => {
    pm.response.to.have.header("Content-Type", "application/json; charset=utf-8");
});

pm.test("Security headers are present", () => {
    pm.response.to.have.header("X-Content-Type-Options");
    pm.response.to.have.header("X-Frame-Options");
    pm.expect(pm.response.headers.get("X-Content-Type-Options")).to.eql("nosniff");
});

pm.test("Response has request ID for tracing", () => {
    pm.response.to.have.header("X-Request-Id");
    pm.expect(pm.response.headers.get("X-Request-Id")).to.not.be.empty;
});
```

### Response Time Validation

```javascript
pm.test("Response time is under 500ms", () => {
    pm.expect(pm.response.responseTime).to.be.below(500);
});

pm.test("Response time is acceptable", () => {
    const threshold = pm.variables.get("responseTimeThreshold") || 2000;
    pm.expect(pm.response.responseTime).to.be.below(parseInt(threshold));
});
```

### JSON Schema Validation

```javascript
const schema = {
    type: "object",
    required: ["id", "email", "name", "role", "createdAt"],
    properties: {
        id: { type: "string", format: "uuid" },
        email: { type: "string", format: "email" },
        name: { type: "string", minLength: 1 },
        role: { type: "string", enum: ["admin", "user", "viewer"] },
        active: { type: "boolean" },
        createdAt: { type: "string" },
    },
    additionalProperties: false,
};

pm.test("Response matches JSON schema", () => {
    const jsonData = pm.response.json();
    const valid = tv4.validate(jsonData, schema);
    pm.expect(valid).to.be.true;
    if (!valid) {
        console.log("Schema validation error:", tv4.error);
    }
});
```

### Variable Chaining Between Requests

```javascript
// In "Create User" test script -- save the ID for subsequent requests
const jsonData = pm.response.json();

pm.test("Save user ID for next request", () => {
    pm.expect(jsonData.id).to.not.be.undefined;
    pm.environment.set("userId", jsonData.id);
    console.log("Saved userId:", jsonData.id);
});

// In "Get User" test script -- verify the retrieved user matches
pm.test("Retrieved user matches created user", () => {
    const jsonData = pm.response.json();
    pm.expect(jsonData.id).to.eql(pm.environment.get("userId"));
});
```

## Data-Driven Testing

### CSV Data File

```csv
email,name,role,expectedStatus
valid@example.com,Valid User,user,201
admin@example.com,Admin User,admin,201
,Missing Email,user,400
invalid-email,Bad Format,user,400
```

### Using Data in Request

In the request body:
```json
{
    "email": "{{email}}",
    "name": "{{name}}",
    "role": "{{role}}"
}
```

In the test script:
```javascript
const expectedStatus = parseInt(pm.iterationData.get("expectedStatus"));

pm.test(`Should return status ${expectedStatus}`, () => {
    pm.response.to.have.status(expectedStatus);
});

if (expectedStatus === 201) {
    pm.test("User created with correct data", () => {
        const jsonData = pm.response.json();
        pm.expect(jsonData.email).to.eql(pm.iterationData.get("email"));
        pm.expect(jsonData.name).to.eql(pm.iterationData.get("name"));
    });
}
```

## Newman CLI

### Basic Execution

```bash
# Run a collection
newman run collections/users-api.postman_collection.json \
  -e environments/staging.postman_environment.json

# Run with data file
newman run collections/users-api.postman_collection.json \
  -e environments/staging.postman_environment.json \
  -d data/users.csv \
  -n 5  # iterations

# Run specific folder
newman run collections/users-api.postman_collection.json \
  --folder "Users" \
  -e environments/staging.postman_environment.json

# Run with reporters
newman run collections/users-api.postman_collection.json \
  -e environments/staging.postman_environment.json \
  -r cli,json,htmlextra \
  --reporter-json-export results/report.json \
  --reporter-htmlextra-export results/report.html

# Run with timeout
newman run collections/users-api.postman_collection.json \
  -e environments/staging.postman_environment.json \
  --timeout-request 10000 \
  --timeout-script 5000
```

### Newman in CI/CD (GitHub Actions)

```yaml
name: API Tests
on: [push, pull_request]

jobs:
  api-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Newman
        run: |
          npm install -g newman
          npm install -g newman-reporter-htmlextra

      - name: Run API Tests
        run: |
          newman run postman/collections/users-api.postman_collection.json \
            -e postman/environments/staging.postman_environment.json \
            -r cli,htmlextra,json \
            --reporter-htmlextra-export reports/api-report.html \
            --reporter-json-export reports/api-results.json

      - name: Upload Test Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: api-test-results
          path: reports/
```

## Best Practices

1. **Use environment variables** -- Never hardcode URLs, credentials, or dynamic values.
2. **Test every request** -- Every request should have at least status code and body validation.
3. **Chain requests via variables** -- Use `pm.environment.set()` to pass data between requests.
4. **Document in request descriptions** -- Explain what each request tests and expects.
5. **Use folders for organization** -- Group related requests into logical folders.
6. **Auto-refresh tokens** -- Use pre-request scripts to handle token expiry automatically.
7. **Validate schemas** -- Use JSON schema validation for response structure verification.
8. **Use collection-level scripts** -- Set up common variables and auth in collection pre-request scripts.
9. **Export and version control** -- Always export collections and environments to source control.
10. **Use Newman for CI** -- Never rely on manual Postman runs for test verification.

## Anti-Patterns to Avoid

1. **Hardcoded URLs** -- Always use `{{baseUrl}}` variable.
2. **No test scripts** -- Requests without tests are just API calls, not tests.
3. **Console.log as testing** -- Use `pm.test()` for proper assertions.
4. **Sharing environments** -- Each developer should have their own environment file.
5. **Ignoring cleanup** -- Requests that create data should have corresponding cleanup.
6. **Order-dependent collections** -- While workflow tests need order, individual tests should not.
7. **Not testing error cases** -- Include 400, 401, 404, and 500 scenarios.
8. **Binary files in source control** -- Export as JSON, not Postman backup format.
9. **Stale environments** -- Keep environment files synchronized with actual API configuration.
10. **Not using data files** -- Repeating the same test with different data is what data files are for.
