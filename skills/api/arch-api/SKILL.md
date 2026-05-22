---
name: arch-api
cluster: se-architecture
description: "API architecture: REST design, versioning, HATEOAS, auth patterns, OpenAPI docs, gateway patterns"
tags: ["api-design","rest","openapi","architecture"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "api architecture design rest versioning openapi gateway hateoas"
---

## Purpose

This skill enables OpenClaw to design, document, and implement API architectures with a focus on REST principles, versioning strategies, HATEOAS, authentication patterns, OpenAPI specifications, and API gateway designs. It ensures APIs are scalable, secure, and standards-compliant.

## When to Use

Use this skill when designing new RESTful APIs, migrating legacy APIs to modern standards, implementing versioning for backward compatibility, or integrating HATEOAS for hypermedia-driven responses. Apply it in microservices environments, when generating OpenAPI docs for Swagger UI, or evaluating auth patterns like JWT for protected endpoints.

## Key Capabilities

- REST design: Generates URI structures (e.g., /resources/{id}) and maps HTTP methods (GET, POST) with specific response codes (200 OK, 404 Not Found).
- Versioning: Supports URI-based (e.g., /v1/resources) or header-based (e.g., Accept: application/vnd.myapi.v1+json) versioning.
- HATEOAS: Adds self-links and related resource links in JSON responses, e.g., {"_links": {"self": "/users/1"}}.
- Auth patterns: Implements JWT or OAuth2 flows, including token validation and scopes (e.g., read:users).
- OpenAPI docs: Auto-generates OpenAPI 3.0 YAML/JSON specs from code or designs, including schemas and endpoints.
- Gateway patterns: Designs API gateways for routing, e.g., using patterns like Kong or AWS API Gateway for load balancing.

## Usage Patterns

Invoke this skill via OpenClaw CLI with the command structure: `openclaw arch-api <subcommand> [flags]`. Always set the auth key via environment variable: `export OPENCLAW_API_KEY=your_api_key` before running commands. For interactive use, pipe outputs to other tools, e.g., `openclaw arch-api design --rest | jq .`. Use JSON config files for complex inputs, formatted as: {"endpoints": [{"path": "/users", "method": "GET"}]}.

To design a REST API, run: `openclaw arch-api design --type rest --version v1 --hateoas`. For OpenAPI generation, provide a source file: `openclaw arch-api docs --input api-spec.json --output openapi.yaml`.

## Common Commands/API

- Command: `openclaw arch-api design --rest --endpoints users/get,users/post --version v1`
  Flags: --hateoas to enable HATEOAS links; --auth jwt for adding JWT auth.
  Code snippet:
  ```
  openclaw arch-api design --rest > api_design.json
  cat api_design.json | grep "uri"
  ```

- Command: `openclaw arch-api generate-openapi --from-code ./src/api/controllers.py --output docs/openapi.yaml`
  Flags: --validate to check for errors; --gateway kong for gateway-specific patterns.
  Code snippet:
  ```
  export OPENCLAW_API_KEY=abc123
  openclaw arch-api generate-openapi --from-code .
  ```

- API Endpoint: If using OpenClaw's internal API, POST to /v1/arch-api/design with body: {"type": "rest", "version": "v1"}. Response includes JSON like {"endpoints": [{"path": "/users", "method": "GET"}]}.
  Config format: Use YAML for inputs, e.g.:
  ```
  endpoints:
    - path: /users
      method: GET
      auth: jwt
  ```

- Command: `openclaw arch-api validate --spec openapi.yaml --check hateoas`
  Flags: --check versioning to verify version headers.

## Integration Notes

Integrate this skill with other OpenClaw skills by chaining commands, e.g., `openclaw chain arch-api se-deployment --input api_design.json`. For external tools, export outputs as files: `openclaw arch-api design > input_for_deployment.txt`. If auth is required, always use the env var pattern: `$OPENCLAW_API_KEY` in scripts, e.g., in a bash script:
```
#!/bin/bash
export OPENCLAW_API_KEY=your_key
openclaw arch-api design --rest
```
For config sharing, use JSON files compatible with tools like Swagger Editor, ensuring fields match OpenAPI schemas.

## Error Handling

Check command exit codes: if `openclaw arch-api design` returns non-zero, parse stderr for messages like "Invalid endpoint format". For API calls, handle HTTP errors: if status == 401, retry with refreshed $OPENCLAW_API_KEY. Use try-catch in scripts:
```
try {
  openclaw arch-api generate-openapi --input invalid.json
} catch (e) {
  if (e.includes("Validation error")) { console.log("Fix JSON schema"); }
}
```
Common errors: 400 for malformed inputs (e.g., missing --version flag); 403 if $OPENCLAW_API_KEY is invalid. Log errors with: `openclaw arch-api design 2>> error.log`.

## Concrete Usage Examples

1. Designing a REST API for a user management system: First, set your auth key: `export OPENCLAW_API_KEY=your_key`. Then, run: `openclaw arch-api design --rest --endpoints users/get,users/post --version v1 --auth jwt --hateoas`. This outputs a JSON file with endpoints like {"path": "/users", "method": "GET", "_links": {"self": "/users/1"}}, which you can use to build the API in code.

2. Generating OpenAPI docs for an existing codebase: Export your key: `export OPENCLAW_API_KEY=your_key`. Execute: `openclaw arch-api generate-openapi --from-code ./src/api --gateway aws --output api_docs.yaml`. This creates a YAML file with specs, e.g., including paths for /users and security schemes for JWT, ready for integration with Swagger UI.

## Graph Relationships

- Related to: se-deployment (for deploying designed APIs via gateway patterns).
- Connected via: se-architecture cluster (shares tags like "api-design" for collaborative skills).
- Links to: se-auth (for detailed auth implementations in APIs).
- Associated with: openapi-tool (for extending OpenAPI doc generation).
