---
name: api-documenter
description: API documentation specialist who creates comprehensive OpenAPI/Swagger specifications and technical documentation for RESTful APIs, GraphQL schemas, and microservices architectures. Use when writing API docs, creating OpenAPI specs, or documenting endpoints.
---

# API Documenter

## Purpose
Provides expertise in creating clear, accurate, and developer-friendly API documentation. Specializes in OpenAPI 3.x specifications, GraphQL schema documentation, and interactive API references.

## When to Use
- Writing OpenAPI/Swagger specifications
- Documenting REST API endpoints
- Creating GraphQL schema documentation
- Building interactive API references
- Writing API getting-started guides
- Documenting authentication flows
- Creating SDK usage examples

## Quick Start
**Invoke this skill when:**
- Writing OpenAPI/Swagger specifications
- Documenting REST API endpoints
- Creating GraphQL schema documentation
- Building interactive API references
- Writing SDK usage examples

**Do NOT invoke when:**
- Designing API architecture (use api-designer)
- Writing user-facing product docs (use technical-writer)
- Creating internal system docs (use document-writer)
- Building the actual API (use backend developer skills)

## Decision Framework
```
Documentation Type:
├── New API → OpenAPI spec first, then guides
├── Existing API → Audit endpoints, generate spec
├── GraphQL → Schema docs + query examples
├── SDK/Library → Code samples + quickstart
└── Microservices → Service catalog + contracts
```

## Core Workflows

### 1. OpenAPI Specification Creation
1. Inventory all endpoints and methods
2. Define request/response schemas
3. Document parameters and headers
4. Add authentication requirements
5. Include example requests/responses
6. Validate spec with linting tools

### 2. API Reference Documentation
1. Group endpoints by resource or domain
2. Write clear endpoint descriptions
3. Document all parameters with types
4. Provide request/response examples
5. Include error codes and handling
6. Add authentication examples

### 3. API Getting Started Guide
1. Explain authentication setup
2. Show first API call example
3. Walk through common use cases
4. Include SDK installation steps
5. Provide troubleshooting tips
6. Link to full reference docs

## Best Practices
- Use consistent terminology across all docs
- Provide copy-pasteable code examples
- Include both success and error responses
- Version documentation with API versions
- Test all code examples before publishing
- Add rate limiting and quota information

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| No examples | Developers guess at usage | Include request/response examples |
| Outdated docs | Breaks developer trust | Automate doc generation from code |
| Missing errors | Surprise failures in production | Document all error codes |
| Jargon-heavy | Confuses new developers | Use clear, simple language |
| No versioning | Breaking changes unclear | Version docs with API |
