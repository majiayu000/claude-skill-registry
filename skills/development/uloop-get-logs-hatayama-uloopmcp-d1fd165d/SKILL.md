---
name: uloop-get-logs
description: 'Retrieve Unity Console logs via uloop CLI. Use when you need to: (1)
  Check for errors or warnings after operations, (2) Debug runtime issues in Unity
  Editor, (3) Investigate unexpected behavior or exc'
---

---
name: uloop-get-logs
description: Retrieve Unity Console logs via uloop CLI. Use when you need to: (1) Check for errors or warnings after operations, (2) Debug runtime issues in Unity Editor, (3) Investigate unexpected behavior or exceptions.
---

# uloop get-logs

Retrieve logs from Unity Console.

## Usage

```bash
uloop get-logs [options]
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--log-type` | string | `All` | Log type filter: `Error`, `Warning`, `Log`, `All` |
| `--max-count` | integer | `100` | Maximum number of logs to retrieve |
| `--search-text` | string | - | Text to search within logs |
| `--include-stack-trace` | boolean | `true` | Include stack trace in output |
| `--use-regex` | boolean | `false` | Use regex for search |
| `--search-in-stack-trace` | boolean | `false` | Search within stack trace |

## Examples

```bash
# Get all logs
uloop get-logs

# Get only errors
uloop get-logs --log-type Error

# Search for specific text
uloop get-logs --search-text "NullReference"

# Regex search
uloop get-logs --search-text "Missing.*Component" --use-regex
```

## Output

Returns JSON array of log entries with message, type, and optional stack trace.
