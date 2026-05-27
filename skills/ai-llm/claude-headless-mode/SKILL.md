---
name: claude-headless-mode
description: Guide for using claude CLI in headless mode with --print, output formats, and JSON schema
triggers:
  - claude --print
  - claude -p
  - headless mode
  - automation
  - scripting
---

# Claude Headless Mode

Use `claude -p` (or `--print`) for non-interactive execution in scripts, CI, and automation.

## Basic Usage

```bash
# Simple prompt
claude -p "Summarize this repo"

# With file input
claude -p "Review this code" < file.py

# Pipe output
claude -p "List all functions" | grep "def "
```

## Output Formats

| Format | Flag | Use Case |
|--------|------|----------|
| Text | `--output-format text` | Human-readable (default) |
| JSON | `--output-format json` | Single JSON result |
| Stream JSON | `--output-format stream-json --verbose` | Real-time streaming |

### Text Output (Default)

```bash
claude -p "What is 2+2?"
# Output: 4
```

### JSON Output

```bash
claude -p "What is 2+2?" --output-format json
```

Returns wrapper with metadata:
```json
{
  "type": "result",
  "subtype": "success",
  "result": "4",
  "duration_ms": 1234,
  "total_cost_usd": 0.01,
  "session_id": "...",
  "structured_output": null
}
```

Extract just the result:
```bash
claude -p "What is 2+2?" --output-format json | jq -r '.result'
```

### Stream JSON Output

```bash
claude -p "Long analysis" --output-format stream-json --verbose
```

- Streams newline-delimited JSON as execution progresses
- Shows tool calls, messages, progress in real-time
- Final line contains the result
- **Requires `--verbose` flag**

Extract final result:
```bash
claude -p "Analyze code" --output-format stream-json --verbose \
  | tee /dev/stderr \
  | tail -1 \
  | jq -r '.result'
```

## Structured Output with JSON Schema

Force Claude to return data matching a specific schema:

```bash
claude -p "Extract function names from auth.py" \
  --output-format json \
  --json-schema '{
    "type": "object",
    "properties": {
      "functions": { "type": "array", "items": { "type": "string" } }
    },
    "required": ["functions"]
  }'
```

Result appears in `structured_output` field:
```json
{
  "result": "...",
  "structured_output": {
    "functions": ["login", "logout", "verify_token"]
  }
}
```

### Schema Examples

**Simple object:**
```json
{
  "type": "object",
  "properties": {
    "answer": { "type": "integer" }
  },
  "required": ["answer"]
}
```

**Task result (success/failure):**
```json
{
  "type": "object",
  "properties": {
    "status": { "type": "string", "enum": ["success", "failure"] },
    "summary": { "type": "string" },
    "files_changed": { "type": "array", "items": { "type": "string" } },
    "error_category": { "type": "string" },
    "suggestion": { "type": "string" }
  },
  "required": ["status", "summary"]
}
```

**Extract from schema result:**
```bash
OUTPUT=$(claude -p "$PROMPT" --output-format json --json-schema "$SCHEMA")
STATUS=$(echo "$OUTPUT" | jq -r '.structured_output.status')
SUMMARY=$(echo "$OUTPUT" | jq -r '.structured_output.summary')
```

## Common Options

| Option | Description |
|--------|-------------|
| `-p, --print` | Headless mode (required) |
| `--output-format` | text, json, stream-json |
| `--json-schema` | Enforce output schema |
| `--verbose` | Required for stream-json |
| `--model` | Select model (sonnet, opus, haiku) |
| `--max-turns` | Limit agentic turns |
| `--permission-mode` | bypassPermissions, plan, etc. |
| `--allowedTools` | Restrict available tools |

## Permission Modes

```bash
# Skip all permission prompts (trusted environments only)
claude -p "Fix all linting errors" --permission-mode bypassPermissions

# Plan mode (read-only exploration)
claude -p "Analyze architecture" --permission-mode plan
```

## Examples

### CI/CD Integration

```bash
# Run tests and get structured result
RESULT=$(claude -p "Run tests and report results" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"passed":{"type":"boolean"},"failures":{"type":"array","items":{"type":"string"}}},"required":["passed"]}')

if [ "$(echo $RESULT | jq '.structured_output.passed')" = "true" ]; then
  echo "Tests passed"
else
  echo "Tests failed"
  exit 1
fi
```

### Batch Processing

```bash
for file in src/*.py; do
  claude -p "Review $file for security issues" \
    --output-format json \
    --json-schema '{"type":"object","properties":{"issues":{"type":"array"}},"required":["issues"]}' \
    | jq ".structured_output.issues"
done
```

### Fresh Context Task Execution

```bash
# Each invocation is independent (no conversation history)
claude -p "Task 1: Create migration" --output-format json
claude -p "Task 2: Add model" --output-format json
claude -p "Task 3: Write tests" --output-format json
```

## Notes

- Each `-p` invocation starts fresh (no context from previous runs)
- Use `--output-format json` for programmatic parsing
- `structured_output` field contains schema-validated data
- `result` field contains raw text response
- Stream JSON requires `--verbose` flag
- Cost info available in JSON output: `total_cost_usd`
