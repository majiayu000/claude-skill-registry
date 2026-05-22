---
name: web-api-tester
description: Test API endpoints for correctness, edge cases, auth handling, and OpenAPI contract compliance.
compatibility: codex, claude-code, claude-ai, agent-skills
license: Apache-2.0
allowed-tools:
  - read_file
  - write_file
  - run_terminal_cmd
  - web_search
metadata:
  category: web-builder
  stage: 7-api-testing
  pipeline: web-builder
---

# Web API Tester

## Objective

Run endpoint-level testing against `openapi.yaml` and produce API quality
coverage artifacts.

## Required Workflow

1. Read `openapi.yaml` from `web-backend-builder`.
2. Build API collections for Bruno or Hoppscotch.
3. Optionally generate automated tests in Vitest, Jest, or pytest.
4. For each endpoint test:
   - happy path
   - edge cases (missing fields, invalid types, max payloads)
   - auth failures (`401`, `403`)
   - rate limiting behavior
5. Validate response contracts against OpenAPI using Zod (TS) or Pydantic (Python).
6. Add frontend-backend contract tests for API call compatibility.
7. Generate endpoint and edge-case coverage percentages.
8. Output `api-test-report.json`.

## Execution

```bash
python skills/web-api-tester/scripts/api_tester.py --input <workspace> --output <out.json> --format json
```

## References

- `references/tools.md`
