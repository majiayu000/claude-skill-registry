---
name: bruno-api
description: >
  Generate comprehensive API endpoint documentation from Bruno (.bru) files by
  mapping requests to a Django4Lyfe/Diversio-style backend implementation
  (Django REST Framework or Django Ninja), including auth/permissions,
  multi-tenant filtering, request/response schemas, and line-numbered code
  references. Use for single endpoints, directory scans of .bru files, or when
  writing docs to a specific output path.
allowed-tools:
  - Bash
  - Read
  - Edit
  - Glob
  - Grep
---

# Bruno API Documentation Generator Skill

## Inputs & Modes

This Skill expects one of:

- A path to a single Bruno file (usually `*.bru`), OR
- `--scan <dir>` to analyze all `.bru` files under a directory.

Optional flags:

- `--dry-run` – produce an analysis plan only (no deep codebase search).
- `--output <path>` – write the generated markdown documentation to a file.

If inputs are missing or ambiguous, ask the user to confirm:

- Which `.bru` file(s) to analyze.
- Whether they want `--dry-run` or full documentation.
- Whether an output file should be written.

## Output Shape & Severity Tags

### Dry-run output

Return a short plan containing:

- Endpoint summary: method, URL, auth, and any detected params/body.
- Where you will look in the Django codebase (specific file paths/directories).
- Which documentation sections will be generated.
- Complexity notes (e.g., “DRF ViewSet + serializer” vs “Ninja router + schema”).

### Full documentation output

Generate a single markdown document for each endpoint using this structure:

- `# <Endpoint Name>`
- ``<METHOD> <URL Pattern>``
- **Authentication**, **Permissions**, **Multi-tenant**
- `## Overview`
- `## Request` (headers + params/body with types/validation)
- `## Response` (success example + common error cases)
- `## Implementation Details` (URL config + view + serializer/schema; always with `file.py:line`)
- `## Business Logic` (step-by-step, include side effects like tasks/external calls)
- `## Frontend Integration` (TypeScript types + call example + React Query hook example)
- `## Testing` (Bruno tests + edge cases + required fixtures/data)
- `## Notes` (perf considerations, related endpoints, rollout notes)

Use severity tags only when something prevents correctness/completeness:

- `[BLOCKING]` – cannot locate the endpoint implementation or critical auth/permission logic.
- `[SHOULD_FIX]` – documentation gaps due to missing/incomplete source details (e.g., response shape unclear).
- `[NOTE]` – optional improvements, related endpoints, refactors, or performance observations.

## Workflow

### Step 1 — Parse the Bruno file(s)

For each `.bru` file:

- Extract:
  - HTTP method
  - URL / path pattern
  - Headers
  - Query parameters
  - Path parameters (from the URL pattern)
  - Request body (and infer a schema where possible)
- Detect authentication intent:
  - JWT / token headers
  - Session/cookie usage
  - Explicit “no auth” signals
- Capture any Bruno test/assert blocks as testing hints.

### Step 2 — Locate the Django route & implementation

Treat these repo conventions as first-class when present:

- If the URL starts with `/api/v2/`:
  - Check `dashboardapp/v2_urls.py`.
  - Check `dashboardapp/views/v2/` for the view/viewset.
- If the URL starts with `/api/v2/pulse/`:
  - Check `pulse_iq/api/` for Django Ninja routers/endpoints.
- Otherwise:
  - Search app-level `urls.py` modules for the path prefix.
  - If needed, `Grep` for a distinctive path segment from the Bruno URL.

Once the route is found, identify the implementation type:

- **DRF**
  - View / ViewSet class and handler method (`list`, `retrieve`, `create`, custom actions).
  - Serializer(s) used (including nested serializers) and validation rules.
  - Permissions / authentication classes.
  - Queryset and filtering (especially company/org scoping).
- **Ninja**
  - Router and endpoint function.
  - Pydantic schema(s) and validation.
  - Auth configuration/decorators.
  - Multi-tenant scoping and access control.

Always record code references with line numbers (`path/to/file.py:123`).

### Step 3 — Extract behavior and contracts

For the located endpoint:

- Summarize the business purpose and any key invariants.
- Document validation and error behavior:
  - Common 400 reasons (schema/serializer validation).
  - Auth failures (401) and permission failures (403).
  - Not-found cases (404) and domain-specific error cases.
- Identify multi-tenant constraints:
  - How company/org is inferred (JWT claims, request context, URL param).
  - Which queryset filters enforce scoping.
- Note side effects:
  - Background tasks (Celery), emails, webhooks, external service calls.
  - Writes to critical models and any transactional boundaries.

### Step 4 — Generate documentation

Write the markdown doc per “Full documentation output”.

Rules:

- Prefer precise types over “string/number” when you can infer them.
- Include at least one realistic example request and success response.
- If response shape is dynamic or large, document the stable contract and
  include a representative sample, not the entire universe of fields.
- When you’re unsure, be explicit about assumptions and mark with `[SHOULD_FIX]`.

### Step 5 — Handle `--output` and `--scan`

- If `--scan <dir>`:
  - Find all `.bru` files recursively under that directory.
  - Generate one markdown doc per file.
  - If no `--output` is provided, return docs in the response (grouped by file).
- If `--output <path>` is provided:
  - Write output to that path.
  - If scanning multiple files, either:
    - Write a single combined doc (with a clear table of contents), OR
    - Write multiple files under an output directory (ask the user which they want).

## Compatibility Notes

This skill is designed to work with both **Claude Code** and **OpenAI Codex**.

For Codex users:
- Install via skill-installer with `--repo DiversioTeam/agent-skills-marketplace
  --path plugins/bruno-api/skills/bruno-api`.
- Use `$skill bruno-api` to invoke.

For Claude Code users:
- Install via `/plugin install bruno-api@diversiotech`.
- Use `/bruno-api:docs` to invoke.

