---
disable-model-invocation: false
name: cli-sentry
user-invocable: true
description: This skill should be used when the user asks to "fetch Sentry issues", "check Sentry errors", "triage Sentry", "categorize Sentry issues", "resolve Sentry issue", "mute Sentry issue", "unresolve Sentry issue", "sentry-cli", or mentions Sentry API, Sentry project issues, error monitoring, issue triage, Sentry stack traces, or browser extension errors in Sentry.
---

# Sentry CLI Issue Management

> **Compatibility**: This skill is compatible with `sentry-cli` v3 only.
>
> **Important**: `sentry-cli api` was removed in v3. Do **not** use `sentry-cli api` for anything. Use `scripts/sentry-api.sh` for API calls (see [API Access](#api-access) and [API Fallbacks](#api-fallbacks)).

## Overview

Expert guidance for managing Sentry issues via the CLI and API. Use this skill for fetching, triaging, categorizing, and resolving Sentry issues.

**Key capabilities:**

- Preflight validation of sentry-cli installation and auth
- List and filter issues by status, time period, and query
- Categorize issues (Valid, False Positive, Already Resolved, Third Party)
- Resolve, mute, and unresolve issues (individually or in bulk)

## Safety Rules

**Prohibited operations:**

- `sentry-cli api` — Removed in v3. Use `sentry-api.sh` instead
- `DELETE /issues/{id}/` - Issue deletion (irreversible)
- Project or release deletion
- Bulk status changes without explicit user confirmation
- Modifying alert rules, notification settings, or project configuration

**Allowed operations:**

- Listing and viewing issues (read-only)
- Resolving issues (reversible via unresolve)
- Muting/ignoring issues (reversible via unmute)
- Fetching event details and stack traces

## API Access

> **NEVER manually parse `~/.sentryclirc` or construct `Authorization` headers.**
> All Sentry API calls MUST go through one of these scripts:
>
> - `scripts/fetch-issues.sh` — list unresolved issues with rich JSON
> - `scripts/sentry-api.sh` — general-purpose authenticated API wrapper
>
> These scripts handle credential resolution internally. Do not use `$SENTRY_AUTH_TOKEN` directly.

### `sentry-api.sh` Usage

```bash
bash scripts/sentry-api.sh METHOD PATH [BODY]
```

- `METHOD`: GET, PUT, POST (DELETE is rejected)
- `PATH`: Sentry API path — `{org}` and `{project}` placeholders are auto-substituted from config
- `BODY`: optional JSON string for PUT/POST

## Prerequisites

### Configuration (`~/.sentryclirc`)

Sentry credentials are stored in `~/.sentryclirc` (the native sentry-cli config file):

```ini
[auth]
token=sntrys_...

[defaults]
org=your-org-slug
project=your-project-slug
```

- **`token`** — Org token (`sntrys_`) or user token (`sntryu_`). Both use `Authorization: Bearer`. Generate at https://sentry.io/settings/account/api/auth-tokens/
- **`org`** — Your organization slug in Sentry
- **`project`** — Your project slug in Sentry

> Environment variables (`SENTRY_AUTH_TOKEN`, `SENTRY_ORG`, `SENTRY_PROJECT`) override rc file values when set. The rc file is the primary persistent store.

### Setup: Missing Configuration

Before running any Sentry operation, run the preflight check:

```bash
bash scripts/check-sentry.sh -v
```

If the preflight check fails with exit code 4 (missing config), prompt the user for each missing value using `AskUserQuestion`, then write the values to `~/.sentryclirc`:

- If the file doesn't exist, create it with `[auth]` and `[defaults]` sections
- If the file exists, add missing keys under the appropriate section (`token` → `[auth]`, `org`/`project` → `[defaults]`)
- Re-run the preflight check to confirm

### Configuration Resolution Order

Settings resolve in this order (first wins):

1. CLI flags (`--org`, `--project`)
2. Environment variables (`SENTRY_ORG`, `SENTRY_PROJECT`, `SENTRY_AUTH_TOKEN`)
3. `~/.sentryclirc`

## Issue Management

### List Issues (CLI)

```bash
# List all issues
sentry-cli issues list --project <project>

# List with status filter
sentry-cli issues list --project <project> --status unresolved

# Full search syntax (Sentry query language)
sentry-cli issues list --project <project> --query "is:unresolved browser.name:Chrome"

# Pagination control (default: 5 pages)
sentry-cli issues list --project <project> --pages 10
```

### List Issues (API - Richer Data)

Use `scripts/fetch-issues.sh` for triage-quality JSON with metadata, culprit, event counts, and timestamps:

```bash
bash scripts/fetch-issues.sh --org=<org> --project=<project>
bash scripts/fetch-issues.sh --org=<org> --project=<project> --stats-period=7d --limit=50
```

### Get Issue Details (API)

```bash
bash scripts/sentry-api.sh GET /issues/{issue_id}/ | jq
```

### Get Latest Event / Stack Trace (API)

```bash
bash scripts/sentry-api.sh GET /issues/{issue_id}/events/latest/ | jq '.exception // {note: "no exception data"}'
```

### Resolve / Mute / Unresolve (CLI)

```bash
# Resolve
sentry-cli issues resolve --project <project> -i <issue_id>

# Mute (ignore)
sentry-cli issues mute --project <project> -i <issue_id>

# Unresolve
sentry-cli issues unresolve --project <project> -i <issue_id>

# Resolve in next release only
sentry-cli issues resolve --project <project> -i <issue_id> --next-release
```

## Issue Categorization

Categorize each issue into one of four categories:

### 1. Valid

Genuine application errors requiring investigation and fixes.

**Indicators:**

- Stack trace points to application code (`src/`, `app/`, `webpack://`)
- Error originates from application logic, not external code
- Reproducible user-facing issues
- API errors from application endpoints

### 2. False Positive

Errors that appear as issues but are not actual problems.

**Indicators:**

- Network errors from user connectivity issues (timeouts, DNS failures)
- Browser-specific quirks not affecting functionality
- Expected errors (e.g., 401 for unauthenticated users, 404 for deleted resources)
- Errors from automated bots/crawlers

### 3. Already Resolved

Issues that have been fixed in subsequent deployments.

**Indicators:**

- Last seen date predates a known fix
- No recent occurrences (check `lastSeen` field)
- Related code has been refactored or removed
- Issue matches a closed GitHub issue or merged PR

### 4. Third Party

Errors originating from browser extensions or external scripts. See `references/extension-patterns.md` for comprehensive detection patterns.

**Indicators:**

- Stack trace contains extension URLs (`chrome-extension://`, `moz-extension://`, etc.)
- Error from injected scripts (`inpage.js`, `content.js`, `inject.js`)
- Known extension error messages (`ResizeObserver loop`, `Extension context invalidated`)
- Stack trace mentions known extensions (MetaMask, Grammarly, LastPass, etc.)

## Triage Workflow

1. **Preflight** - Run `bash scripts/check-sentry.sh -v` to verify config and auth. If missing, prompt the user and write to `~/.sentryclirc`
2. **Fetch** - Run `bash scripts/fetch-issues.sh --org=<org> --project=<project>` to get all unresolved issues
3. **Inspect** - For each issue, fetch its latest event to examine the stack trace:
   ```bash
   bash scripts/sentry-api.sh GET /issues/{issue_id}/events/latest/ \
     | jq '.exception.values[0].stacktrace.frames // empty'
   ```
   Check `culprit`, `title`, `metadata`, `lastSeen`, and event count
4. **Categorize** - Assign each issue to Valid, False Positive, Already Resolved, or Third Party
5. **Present** - Summarize in a triage report table:

```markdown
## Sentry Issue Triage Report

### Valid (N issues)

| Issue | Title | Events | Last Seen |
| --- | --- | --- | --- |
| PROJ-123 | TypeError in Component | 45 | 2h ago |

### Third Party (N issues)

| Issue | Title | Source | Events |
| --- | --- | --- | --- |
| PROJ-126 | ResizeObserver loop | Browser Extension | 234 |

### False Positives (N issues)

| Issue | Title | Reason |
| --- | --- | --- |
| PROJ-128 | Network Error | User connectivity |

### Already Resolved (N issues)

| Issue | Title | Last Seen | Notes |
| --- | --- | --- | --- |
| PROJ-130 | Hydration mismatch | 14d ago | Fixed in v2.3.1 |
```

## Bulk Actions

After triage, resolve or mute issues in bulk. Always confirm with the user before executing.

```bash
# Bulk resolve via API
bash scripts/sentry-api.sh PUT \
  "/projects/{org}/{project}/issues/?id=123&id=456&id=789" \
  '{"status": "resolved"}'

# Bulk ignore/mute via API
bash scripts/sentry-api.sh PUT \
  "/projects/{org}/{project}/issues/?id=123&id=456&id=789" \
  '{"status": "ignored"}'
```

## Quick Reference

| Operation          | Method | Command / Endpoint                                                                                  |
| ------------------ | ------ | --------------------------------------------------------------------------------------------------- |
| List issues        | CLI    | `sentry-cli issues list --project <p>`                                                              |
| List issues (rich) | Script | `bash scripts/fetch-issues.sh --org=<o> --project=<p>`                                              |
| Issue details      | Script | `bash scripts/sentry-api.sh GET /issues/{id}/`                                                      |
| Latest event       | Script | `bash scripts/sentry-api.sh GET /issues/{id}/events/latest/`                                        |
| Event list         | Script | `bash scripts/sentry-api.sh GET /issues/{id}/events/`                                               |
| Resolve            | CLI    | `sentry-cli issues resolve --project <p> -i <id>`                                                   |
| Mute               | CLI    | `sentry-cli issues mute --project <p> -i <id>`                                                      |
| Unresolve          | CLI    | `sentry-cli issues unresolve --project <p> -i <id>`                                                 |
| Bulk update        | Script | `bash scripts/sentry-api.sh PUT "/projects/{org}/{project}/issues/?id=..." '{"status":"resolved"}'` |

## Tips

1. Run `sentry-cli info` to verify configuration and auth status from any source
2. Pipe API responses through `jq` for readable output: `... | jq '.[] | {shortId, title, count, lastSeen}'`
3. Triage Third Party issues first - they are the easiest to identify and often the most numerous
4. Check `references/extension-patterns.md` before categorizing ambiguous stack traces
