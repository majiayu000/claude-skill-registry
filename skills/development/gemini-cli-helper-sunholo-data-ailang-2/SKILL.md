---
name: Gemini CLI Helper
description: Run Gemini CLI commands from Claude with correct Node version. Use when user asks to run Gemini CLI, test Gemini traces, or debug Gemini telemetry.
---

# Gemini CLI Helper

Run Gemini CLI commands with the correct Node.js version and configuration.

## Quick Start

**Run a Gemini prompt:**
```bash
.claude/skills/gemini-cli-helper/scripts/gemini_run.sh "Your prompt here"
```

**Check Gemini CLI status:**
```bash
.claude/skills/gemini-cli-helper/scripts/gemini_status.sh
```

## When to Use This Skill

Invoke this skill when:
- User asks to run Gemini CLI
- User wants to test Gemini trace visibility
- User asks to debug Gemini telemetry
- User mentions "gemini" CLI commands
- Coordinator needs to execute Gemini tasks

## Available Scripts

### `scripts/gemini_run.sh <prompt> [--json]`
Run a Gemini CLI prompt with correct Node version.

**Usage:**
```bash
# Simple prompt
.claude/skills/gemini-cli-helper/scripts/gemini_run.sh "Say hello"

# With JSON output
.claude/skills/gemini-cli-helper/scripts/gemini_run.sh "Say hello" --json

# Complex prompt with quotes
.claude/skills/gemini-cli-helper/scripts/gemini_run.sh "List 3 things about AILANG"
```

### `scripts/gemini_status.sh`
Check Gemini CLI installation and configuration status.

**Usage:**
```bash
.claude/skills/gemini-cli-helper/scripts/gemini_status.sh
```

**Output:**
```
Gemini CLI Status
━━━━━━━━━━━━━━━━━
Node Version: v22.20.0 (required: v20+)
Gemini CLI: /Users/mark/.nvm/versions/node/v22.20.0/bin/gemini
Version: 0.21.1
GCP Project: multivac-internal-dev
Telemetry: Enabled (GCP Cloud Trace)
```

## Critical Knowledge

### Node Version Requirement

**Gemini CLI requires Node.js v20 or higher** due to regex flag syntax.

```bash
# WRONG - Will fail with "Invalid regular expression flags"
gemini --version  # Uses default Node which may be v18

# CORRECT - Use full path with Node v22
/Users/mark/.nvm/versions/node/v22.20.0/bin/node \
  /Users/mark/.nvm/versions/node/v22.20.0/lib/node_modules/@google/gemini-cli/dist/index.js \
  --version
```

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Invalid regular expression flags` | Node < v20 | Use full Node v22 path |
| `MODULE_NOT_FOUND` | Wrong CLI path | Check actual symlink target |
| `Cannot find module` | Incorrect dist path | Use `dist/index.js` not `bin/cli.mjs` |

### Telemetry Configuration

**⚠️ CRITICAL: Telemetry is DISABLED by default!**

To enable Gemini CLI traces in AILANG Observatory:

#### Option 1: Direct to GCP (Recommended)

Create or edit `~/.gemini/settings.json`:
```json
{
  "telemetry": {
    "enabled": true,
    "target": "gcp",
    "logPrompts": true
  }
}
```

Or use environment variables:
```bash
export GEMINI_TELEMETRY_ENABLED=true
export GEMINI_TELEMETRY_TARGET=gcp
export GOOGLE_CLOUD_PROJECT=multivac-internal-dev
```

#### Option 2: Via OTLP Collector

For more control (e.g., sending to multiple backends):

1. Create `~/.gemini/collector-config.yaml`:
```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

exporters:
  googlecloud:
    project: multivac-internal-dev
  otlp/ailang:
    endpoint: localhost:1957
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [googlecloud, otlp/ailang]
```

2. Enable collector mode in settings:
```json
{
  "telemetry": {
    "enabled": true,
    "target": "local",
    "useCollector": true,
    "otlpEndpoint": "http://localhost:4317"
  }
}
```

Traces appear in:
- GCP Cloud Trace Console
- AILANG Observatory (via composite backend or direct OTLP)

## Workflow

### 1. Check Status First
```bash
.claude/skills/gemini-cli-helper/scripts/gemini_status.sh
```

### 2. Run Prompt
```bash
.claude/skills/gemini-cli-helper/scripts/gemini_run.sh "Your prompt"
```

### 3. Verify Traces (Optional)
```bash
curl -s "http://localhost:1957/api/observatory/traces?limit=10" | jq '.[].service_name' | sort -u
```

## Resources

### Reference Guide
See [`resources/reference.md`](resources/reference.md) for:
- Full path configuration
- nvm setup instructions
- Troubleshooting guide
- GCP telemetry details

## Notes

- Always use the scripts in this skill instead of direct `gemini` command
- Scripts handle Node version detection automatically
- Telemetry goes to GCP Cloud Trace, then imported to Observatory
- JSON output mode recommended for programmatic use
