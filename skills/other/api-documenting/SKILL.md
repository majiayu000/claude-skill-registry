---
name: api-documenting
description: Generate API documentation from code. Use when the user wants to document APIs, create API reference, generate endpoint documentation, or needs help with OpenAPI/Swagger specs.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
---

# API Documentation Generator

Generate comprehensive API documentation from source code.

## Quick Reference

For common documentation patterns, see `PATTERNS.md`.

## Documentation Standards

See `STANDARDS.md` for our documentation conventions.

## Process

### Step 1: Identify API Endpoints

Look for:
- Route definitions (Express, FastAPI, etc.)
- Controller methods
- Handler functions

### Step 2: Extract Information

For each endpoint, extract:
- HTTP method (GET, POST, PUT, DELETE, etc.)
- Path/route
- Parameters (path, query, body)
- Request/response schemas
- Authentication requirements

### Step 3: Generate Documentation

Use the template in `templates/endpoint.md` for consistent formatting.

### Step 4: Create Overview

Generate an index of all endpoints with the template in `templates/index.md`.

## Output Formats

### Markdown (Default)
Generate markdown documentation suitable for README or docs site.

### OpenAPI/Swagger
If requested, generate OpenAPI 3.0 spec. See `templates/openapi.yaml` for structure.

## Examples

See `EXAMPLES.md` for sample inputs and outputs.

## Scripts

To auto-detect routes in common frameworks:
```bash
python scripts/detect_routes.py <source_directory>
```

To validate generated OpenAPI spec:
```bash
./scripts/validate_openapi.sh <spec_file>
```
