---
name: api-test
description: Generate and run API integration tests with Hurl
argument-hint: "<endpoint-or-spec> [--generate] [--run]"
tags: [testing, api, integration, hurl]
user-invocable: true
---

# API Testing with Hurl

Generate and run HTTP API tests using Hurl (18K+ stars, plain-text HTTP test files).

## Install
```bash
choco install hurl    # Windows
brew install hurl      # macOS
```

## Write .hurl test files
```hurl
# tests/api/candidates.hurl

GET http://localhost:5000/api/candidates/{{candidate_id}}
HTTP 200
[Asserts]
jsonpath "$.id" == "{{candidate_id}}"
jsonpath "$.firstName" isString
jsonpath "$.skills" isCollection
duration < 100

POST http://localhost:5000/api/candidates
Content-Type: application/json
{
  "firstName": "Jean",
  "lastName": "Dupont",
  "email": "jean.dupont@example.com",
  "skills": ["CSharp", "Azure"]
}
HTTP 201
[Captures]
created_id: jsonpath "$.id"
[Asserts]
jsonpath "$.firstName" == "Jean"
```

## Run tests
```bash
hurl --test tests/api/*.hurl --report-junit report.xml --variable candidate_id=c-001
```

## Schemathesis (OpenAPI Fuzz Testing)
```bash
pip install schemathesis
schemathesis run http://localhost:5000/swagger/v1/swagger.json --checks all --stateful=links
```

## Arguments
- `<endpoint-or-spec>`: Base URL or OpenAPI spec path
- `--generate`: Generate .hurl files from OpenAPI spec
- `--run`: Execute existing .hurl test files