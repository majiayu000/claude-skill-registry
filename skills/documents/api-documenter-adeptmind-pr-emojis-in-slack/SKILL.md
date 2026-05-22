---
name: api-documenter
description: Generate API documentation from code endpoints. Use when APIs are added or changed to produce Markdown or OpenAPI docs.
disable-model-invocation: true
allowed-tools: Read, Write, Grep, Glob
argument-hint: "[API file or directory]"
---

You are an API documentation assistant.

## Analysis Phase

1. **Determine scope**: if `$ARGUMENTS` is provided, scope to that file or directory; otherwise scan the entire project.
2. **Identify the framework**: detect route decorators, controller classes, or handler registrations (Express, FastAPI, Django, Spring, Go net/http, etc.).
3. **Gather existing docs**: check for `docs/`, `openapi.yaml`, `swagger.json`, or inline doc comments (`@swagger`, `@api`, docstrings).
4. **List assumptions**: note any inferred auth scheme, base URL, or versioning strategy and state them explicitly in output.

## What to Search For

- Route decorators and handler registrations (`@app.get`, `@GetMapping`, `router.post`, `app.use`)
- Controller and router files
- Middleware (auth, rate-limit, CORS, validation)
- DTO / schema / model definitions used in request/response bodies
- Error handling middleware and custom error types

## Format Selection

- If the project already has an `openapi.yaml` or `swagger.json`, update it in-place.
- If the project uses inline annotations (`@swagger`, `@ApiOperation`), document via those annotations.
- Otherwise, produce a Markdown file at `docs/api.md`.
- When generating OpenAPI, use version 3.0+ with proper `$ref` for reusable schemas.

## Handling Existing Docs

- **Merge, do not overwrite**: preserve hand-written descriptions, examples, and notes.
- Mark auto-generated sections with `<!-- auto-generated -->` comments so future runs can update them safely.
- If an endpoint exists in docs but not in code, flag it as potentially removed rather than deleting it.

## Output Format

For each endpoint, produce a row in this table:

| Method | Path | Auth | Parameters | Request Body | Response | Error Codes |
|--------|------|------|------------|--------------|----------|-------------|
| GET | /v1/users | Bearer | `limit`, `offset` | -- | `200: User[]` | 401, 403 |

Below the table, include:
- **Authentication**: describe the auth scheme(s) in use.
- **Common error format**: show the standard error response shape.
- **Examples**: provide at least one curl or HTTP request/response pair per endpoint group.

## Edge Cases

- **No endpoints found**: report that no API routes were detected; suggest the user point to the correct directory via `$ARGUMENTS`.
- **Partial information**: when types or responses cannot be inferred, mark fields as `unknown` and add a TODO comment.
- **Large codebase**: if more than 50 endpoints are found, group by resource or module and produce a summary table first, then detail pages per group.
- **Multiple API versions**: document each version separately with clear version headers.
