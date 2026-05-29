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

Check auth status: `casedev auth status --json`

API keys start with `sk_case_`. Config is stored at `~/.config/case/config.json`.

## Diagnostics

```bash
casedev doctor --json
```

Checks: API URL format, root reachability, vault/OCR/voice/compute/skills health endpoints, API key validity. Use `--strict` to fail on warnings.

## Focus (Default Targets)

Set default vault/object/project so you can omit `--vault` flags:

```bash
casedev focus set --vault VAULT_ID --object OBJECT_ID --project PROJECT_ID
casedev focus show --json
casedev focus clear --all
```

## Job Tracker

Unified job tracker for OCR and transcription jobs:

```bash
casedev jobs list --json
casedev jobs list --type ocr --status completed --json
casedev jobs get JOB_ID --type ocr --json
casedev jobs watch JOB_ID --type transcribe --interval 5 --timeout 600 --json
```

## API Routes

Browse and call any case.dev API endpoint by operationId:

```bash
casedev routes list --json
casedev routes list --tag vault --json
casedev call getVaultList --json
casedev call createVault --body '{"name":"test"}' --json
```

## Raw API Access

```bash
casedev api GET /vault --json
casedev api POST /vault --body '{"name":"new-vault"}' --json
casedev api GET /ocr/v1/health --no-auth --json
```

Flags: `--header "name:value"`, `--no-auth`, `--body <json>`.

## Global Flags

All commands accept:
- `--json` — machine-readable JSON output (always use this in agent workflows)
- `--api-url <url>` — override API base URL
- `--api-key <key>` — override API key for this invocation

## Troubleshooting

**"No API key set"**: Run `casedev auth set-key --api-key sk_case_...` or set `CASE_API_KEY` env var.

**Doctor shows FAIL**: The specific service may be temporarily unavailable. Check the message for which service.

**"Invalid API key format"**: Keys must start with `sk_case_`.
