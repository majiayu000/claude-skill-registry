---
name: api-testing
description: Generate and run REST API tests using Postman collections and Newman CLI. Use when asked to test APIs, verify endpoints, validate responses, or run Postman tests in CI.
---

# API Testing with Postman + Newman

Generate API tests as Postman collections. Run them with Newman CLI.

## Setup

```bash
npm install -g newman
```

## Test Pattern

Each request gets tests in the Tests tab:

```javascript
// Assert status code
pm.test("Status is 200", function () {
    pm.response.to.have.status(200);
});

// Assert response body
pm.test("Returns user name", function () {
    pm.expect(pm.response.json().name).to.eql("Test User");
});

// Assert response time
pm.test("Response under 2s", function () {
    pm.expect(pm.response.responseTime).to.be.below(2000);
});

// Validate schema
pm.test("Matches schema", function () {
    pm.response.to.have.jsonSchema({
        type: "object",
        required: ["id", "name", "email"],
        properties: {
            id: { type: "number" },
            name: { type: "string" },
            email: { type: "string" }
        }
    });
});
```

## Pass Data Between Requests

Save a value from one response, use it in the next:

```javascript
// In POST /users Tests tab — save created ID
const id = pm.response.json().id;
pm.environment.set("created_id", id);

// In GET /users/{{created_id}} — it auto-resolves
```

## Negative Tests

```javascript
// Missing required field → expect 400 or 422
pm.test("Rejects missing field", function () {
    pm.expect(pm.response.code).to.be.oneOf([400, 422]);
});

// No auth token → expect 401
pm.test("Rejects unauthorized", function () {
    pm.response.to.have.status(401);
});
```

## Run with Newman

```bash
# Basic run
newman run collection.json

# With environment
newman run collection.json -e environment.json

# Override variables
newman run collection.json --env-var "base_url=https://staging.example.com"

# Data-driven from CSV
newman run collection.json -d testdata.csv

# CI report
newman run collection.json -r junit --reporter-junit-export report.xml
```

## Guidelines

- Use environment variables for `base_url` and secrets, never hardcode.
- One assertion per `pm.test` block.
- Assert status code first, then body.
- Export collections as v2.1 format.
