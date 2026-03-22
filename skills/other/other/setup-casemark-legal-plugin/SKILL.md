---
name: setup
description: Installs and configures the case.dev CLI for legal AI workflows including document vaults, OCR, transcription, and search. Use when the user mentions "case.dev", "casedev", needs to authenticate with case.dev, run diagnostics, set focus targets, list API routes, track jobs, or make raw API calls. Gateway skill for all case.dev skills.
---

# case.dev CLI

The `casedev` CLI is the interface to [case.dev](https://case.dev), a legal AI platform providing encrypted document vaults, production OCR, audio transcription, and legal/web/patent search.

This skill covers installation, authentication, diagnostics, and general CLI usage. For domain-specific workflows, see the companion skills: `vaults`, `ocr`, `transcription`, `search`.

## Installation

```bash
# macOS (Homebrew)
brew install casemark/casedev/casedev

# macOS + Linux (shell script)
curl -fsSL https://raw.githubusercontent.com/CaseMark/homebrew-casedev/main/install.sh | sh
```

Or run the bundled setup script:
```bash
bash scripts/setup.sh
```

Verify: `casedev --version`

## Authentication

Three methods, in order of preference:

```bash
# 1. Environment variable (best for agents)
export CASE_API_KEY=sk_case_YOUR_KEY

# 2. Store key in config
casedev auth set-key --api-key sk_case_YOUR_KEY

# 3. Browser device-flow login (interactive, use --no-open for headless)
casedev auth login --no-open
```

Check auth status:
```bash
casedev auth status --json
```

Logout:
```bash
casedev auth logout
```

API keys start with `sk_case_`. Config is stored at `~/.config/case/config.json`.

## Diagnostics

Run `casedev doctor` to check connectivity, service health, and auth:

```bash
casedev doctor --json
```

Checks: API URL format, root reachability, vault/OCR/voice/compute/skills health endpoints, API key validity. Use `--strict` to fail on warnings.

## Focus (Default Targets)

Set default vault/object/project so you can omit `--vault` flags:

```bash
# Set focus
casedev focus set --vault VAULT_ID --object OBJECT_ID --project PROJECT_ID

# Show current focus
casedev focus show --json

# Clear
casedev focus clear --vault
casedev focus clear --all
```

## Job Tracker

Unified job tracker for OCR and transcription jobs:

```bash
# List all tracked jobs (auto-refreshes status)
casedev jobs list --json

# Filter
casedev jobs list --type ocr --status completed --json
casedev jobs list --type transcribe --vault VAULT_ID --json

# Get details
casedev jobs get JOB_ID --type ocr --json

# Watch until complete
casedev jobs watch JOB_ID --type transcribe --interval 5 --timeout 600 --json
```

Use `--no-refresh` on `jobs list` to skip live status checks.

## API Routes

Browse and call any case.dev API endpoint by operationId:

```bash
# List available routes
casedev routes list --json
casedev routes list --tag vault --json
casedev routes list --search "upload" --json

# Call by operationId
casedev call getVaultList --json
casedev call createVault --body '{"name":"test"}' --json
casedev call getVaultObjects --param vaultId=VAULT_ID --json
```

## Raw API Access

For endpoints not covered by named commands:

```bash
casedev api GET /vault --json
casedev api POST /vault --body '{"name":"new-vault"}' --json
casedev api GET /ocr/v1/health --no-auth --json
casedev api POST /legal/v1/find --body '{"query":"breach of contract"}' --json
```

Flags: `--header "name:value"`, `--no-auth`, `--body <json>`.

## Global Flags

All commands accept:
- `--json` — machine-readable JSON output (always use this in agent workflows)
- `--api-url <url>` — override API base URL
- `--api-key <key>` — override API key for this invocation

## Troubleshooting

**"No API key set"**: Run `casedev auth set-key --api-key sk_case_...` or set `CASE_API_KEY` env var.

**Doctor shows FAIL on a health check**: The specific service may be temporarily unavailable. Check the message for which service (vault, OCR, voice, compute).

**"Invalid API key format"**: Keys must start with `sk_case_`.

**Auth login times out**: Use `--timeout 120` for slower connections, or use `auth set-key` instead.
