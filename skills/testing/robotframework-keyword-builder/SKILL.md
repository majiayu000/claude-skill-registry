---
name: robotframework-keyword-builder
description: Generate Robot Framework user keywords from structured intent. Use when asked to create keywords, add arguments, documentation, tags, setup/teardown, or to apply embedded-argument style based on existing project conventions.
---

# Robot Framework Keyword Builder

Create user keywords in Robot Framework syntax from structured input. Output JSON only.

## Input (JSON)

Provide input via `--input` or stdin. Example:

```json
{
  "keyword_name": "Create User",
  "description": "Creates a new user via the UI.",
  "arguments": [
    {"name": "username", "type": "str"},
    {"name": "role", "default": "viewer"}
  ],
  "tags": ["ui", "smoke"],
  "setup": {"keyword": "Open Browser", "args": ["${URL}", "chromium"]},
  "teardown": {"keyword": "Close Browser"},
  "style": "simple",
  "steps": [
    {"keyword": "Click", "args": ["Add User"]},
    {"keyword": "Input Text", "args": ["Username", "${username}"]},
    {"keyword": "Click", "args": ["Save"]}
  ]
}
```

## Command

```bash
python scripts/keyword_builder.py --input keyword.json
```

Detect embedded-argument style from an existing project:

```bash
python scripts/keyword_builder.py --input keyword.json --project-root . --detect-embedded
```

## Output (JSON)
- `artifact`: keyword block
- `warnings` and `suggestions`
- `meta`: any detected project conventions
