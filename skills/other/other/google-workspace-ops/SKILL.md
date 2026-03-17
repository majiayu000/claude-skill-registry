---
name: google-workspace-ops
version: 0.11.0
description: Google Workspace CLI automation via gogcli. Gmail, Calendar, Drive, Docs, Slides, Sheets, and 9 more services. JSON-first output, composable pipelines.
tools_required:
  - gog (gogcli v0.11.0+)
triggers:
  - email, gmail, send email, read email, inbox
  - calendar, events, schedule, meeting, create event
  - drive, upload, download, search files, google docs, slides, sheets
  - contacts, tasks, google workspace
---

# Google Workspace Ops

Automates Google Workspace work using the `gog` CLI with machine-parseable JSON output, from email and calendar operations to Drive/docs/sheets workflows. Use it when you need repeatable workspace automation, but avoid it for non-Google services or ad hoc UI workflows.

Terminology used in this file:
- **OAuth:** Google's delegated login/authorization flow used to grant CLI access without sharing your password.
- **GCP:** Google Cloud Platform, where you create the project and OAuth credentials.
- **RFC3339:** Standard date-time format used by Google APIs (for example, `2026-02-18T09:00:00+00:00`).

## Setup

```bash
brew tap steipete/tap
brew install gogcli
gog login YOUR_EMAIL --services all
```

- **Claude Code:** copy this skill folder into `.claude/skills/google-workspace-ops/`
- **Codex CLI:** append this SKILL.md content to your project's root `AGENTS.md`

For the full installation walkthrough (prerequisites, OAuth setup, verification, troubleshooting), see [references/installation-guide.md](references/installation-guide.md).

**Credential management:** `GOG_KEYRING_PASSWORD` is required for all `gog` operations using the file-based keyring (headless/SSH environments, or desktop when opting out of system keychain). We strongly recommend managing it via the [vault skill](../vault/) -- see [references/auth-setup.md](references/auth-setup.md#credential-management) for all options including vault, custom secret managers, and plain export.

## Staying Updated

This skill ships with an `UPDATES.md` changelog and `UPDATE-GUIDE.md` for your AI agent.

After installing, tell your agent: "Check `UPDATES.md` in the google-workspace-ops skill for any new features or changes."

When updating, tell your agent: "Read `UPDATE-GUIDE.md` and apply the latest changes from `UPDATES.md`."

Follow `UPDATE-GUIDE.md` so customized local files are diffed before any overwrite.

---

## Quick Start

Run one read-only Gmail flow end-to-end:

```bash
gog auth status
gog gmail search "is:unread" --max 5 --json --no-input
gog gmail thread get THREAD_ID --json --no-input
```

Use this baseline pattern for automation:
- read/list/search: `--json --no-input`
- send/create/modify/delete: run `--dry-run` first, then ask user approval

## Decision Tree: When to Use gog

```text
Need to interact with Google Workspace?
  |
  +-- Is it email? (read, search, send, labels, drafts)
  |     YES --> gog gmail ...
  |
  +-- Is it calendar? (events, create, conflicts, freebusy)
  |     YES --> gog calendar ...
  |
  +-- Is it files? (search, upload, download, share)
  |     YES --> gog drive ...
  |
  +-- Is it document editing? (create, read, write Google Docs)
  |     YES --> gog docs ...
  |
  +-- Is it presentations? (create from markdown, export)
  |     YES --> gog slides ...
  |
  +-- Is it spreadsheets? (read cells, update, append)
  |     YES --> gog sheets ...
  |
  +-- Is it people? (contacts, directory search, tasks)
        YES --> gog contacts / gog tasks / gog people ...
```

**Rule of thumb:** if it touches Google Workspace, `gog` is the right entry point.

## Security: Approval Rules

**State-modifying operations require explicit user approval before execution.**

| Operation Type | Examples | Autonomous? |
|---------------|----------|-------------|
| **Read / List / Search** | `gmail messages list`, `drive ls`, `calendar list`, `docs cat` | YES — run freely |
| **Send / Create** | `gmail send`, `docs create`, `calendar create`, `drive upload` | NO — ask user first |
| **Modify / Update** | `gmail modify`, `sheets update`, `docs write`, `contacts update` | NO — ask user first |
| **Delete / Trash** | `gmail trash`, `drive trash`, `tasks delete` | NO — ask user first |
| **Draft** | `gmail drafts create` | YES — drafts are safe, not sent |

The rule is simple: if an action changes workspace state visible to others or is hard to undo, get approval first. Reading is okay.

Automation and scripts should present intent (recipient, subject, summary, account, target IDs) and wait for explicit confirmation before send/modify/delete operations.

## Global Flags (All Commands)

Every `gog` command accepts these flags. Know them -- they control output format and safety.

| Flag | Short | Purpose | When to Use |
|------|-------|---------|-------------|
| `--json` | `-j` | JSON output to stdout | **Always for agent use** -- structured, parseable |
| `--plain` | `-p` | TSV output (no colors) | When piping to awk/cut |
| `--results-only` | | Drop envelope (nextPageToken etc.) | Cleaner JSON for single-page results |
| `--select=FIELDS` | | Pick only needed fields (dot paths) | Reduce token cost on large responses |
| `--account=EMAIL` | `-a` | Target specific account | Multi-account setups |
| `--dry-run` | `-n` | Preview without executing | **Always before destructive ops** |
| `--force` | `-y` | Skip confirmations | Non-interactive pipelines |
| `--no-input` | | Fail instead of prompting | Agent automation (never interactive) |
| `--verbose` | `-v` | Debug logging | Troubleshooting |

**Agent-critical pattern:** use `--json --no-input` for automation. JSON keeps automation deterministic. `--no-input` prevents prompt hangs.

## Services Overview

| Service | Command | Aliases | Key Operations |
|---------|---------|---------|----------------|
| Gmail | `gog gmail` | `mail`, `email` | search, get, send, thread, labels, drafts, batch |
| Calendar | `gog calendar` | `cal` | events, create, search, conflicts, freebusy |
| Drive | `gog drive` | `drv` | ls, search, upload, download, share, mkdir |
| Docs | `gog docs` | `doc` | create, cat, write, insert, find-replace |
| Slides | `gog slides` | `slide` | create, create-from-markdown, export, read-slide |
| Sheets | `gog sheets` | `sheet` | get, update, append, clear, format, metadata |
| Contacts | `gog contacts` | `contact` | search, list, create, update |
| Tasks | `gog tasks` | `task` | lists, list, add, done, update |
| Chat | `gog chat` | | spaces, messages, threads, dm |
| People | `gog people` | `person` | me, search, get, relations |
| Forms | `gog forms` | `form` | get, create, responses |
| Groups | `gog groups` | `group` | list, members |
| Classroom | `gog classroom` | `class` | courses, students, coursework, submissions |
| Apps Script | `gog appscript` | `script` | get, content, run, create |
| Keep | `gog keep` | | list, get, search (Workspace only) |

**Top-level shortcuts** (save keystrokes):

| Shortcut | Expands To |
|----------|------------|
| `gog send` | `gog gmail send` |
| `gog ls` | `gog drive ls` |
| `gog search` | `gog drive search` |
| `gog download` | `gog drive download` |
| `gog upload` | `gog drive upload` |
| `gog login` | `gog auth add` |
| `gog logout` | `gog auth remove` |
| `gog status` | `gog auth status` |
| `gog me` / `gog whoami` | `gog people me` |

## 10x Workflows

These are the highest-leverage patterns. Use these before inventing new scripts.

### 1. Read and Summarize Recent Emails

```bash
# Get last 5 unread emails with full content
gog gmail search "is:unread" --max 5 --json | jq '.[].messages[0] | {subject: .subject, from: .from, snippet: .snippet}'

# Get a specific thread with all messages
gog gmail thread get THREAD_ID --json
```

### 2. Send Email (with Safety)

```bash
# Preview first (dry-run)
gog send --to "person@example.com" --subject "Meeting notes" --body "Here are the notes..." --dry-run

# Then send
gog send --to "person@example.com" --subject "Meeting notes" --body "Here are the notes..." --no-input
```

### 3. Today's Calendar at a Glance

```bash
# Today's events across all calendars
gog cal events --today --all --json

# This week
gog cal events --week --json

# Next 3 days
gog cal events --days 3 --json
```

### 4. Create Calendar Event from Natural Language

```bash
# The agent translates natural language to RFC3339 times
gog cal create primary \
  --summary "Team standup" \
  --from "2026-02-18T09:00:00+00:00" \
  --to "2026-02-18T09:30:00+00:00" \
  --description "Daily sync" \
  --with-meet \
  --json
```

### 5. Search Drive and Get Links

```bash
# Full-text search
gog search "quarterly report" --max 5 --json | jq '.[].webViewLink'

# List files in a folder
gog ls --parent FOLDER_ID --json
```

### 6. Create a Google Doc from Markdown

```bash
# Create doc with markdown content
gog docs create "Meeting Notes 2026-02-17" --file notes.md --json

# Or write markdown to existing doc
gog docs write DOC_ID --file notes.md --replace --markdown
```

### 7. Read a Google Doc as Plain Text

```bash
# Dump doc as text (great for agent consumption)
gog docs cat DOC_ID

# Read specific tab
gog docs cat DOC_ID --tab "Notes"

# All tabs
gog docs cat DOC_ID --all-tabs
```

### 8. Create Slides from Markdown

```bash
# One command: markdown -> Google Slides
gog slides create-from-markdown "Q1 Review" --content-file presentation.md --json
```

### 9. Spreadsheet Operations

```bash
# Read a range
gog sheets get SHEET_ID "Sheet1!A1:D10" --json

# Append a row
gog sheets append SHEET_ID "Sheet1!A:D" "value1" "value2" "value3" "value4"

# Update specific cells
gog sheets update SHEET_ID "Sheet1!B2" "new value"
```

### 10. Multi-Service Pipeline

```bash
# Find a doc, read it, email a summary
DOC_ID=$(gog search "project brief" --max 1 --json | jq -r '.[0].id')
CONTENT=$(gog docs cat "$DOC_ID")
gog send --to "team@example.com" --subject "Project Brief Summary" --body "$CONTENT" --no-input
```

## Output Modes

`gog` supports three output modes. Choose based on consumer.

| Mode | Flag | Best For |
|------|------|----------|
| Human | (default) | Terminal, interactive use, colored tables |
| JSON | `--json` | Automation, scripting, `jq` pipelines |
| TSV | `--plain` | `awk`, `cut`, spreadsheet import |

For automation: **always `--json`**. Add `--results-only` to trim envelopes.

**Field selection** reduces token use:
```bash
# Only get subject and date from emails
gog gmail search "is:unread" --json --select "subject,date,from"
```

## Exit Codes

Stable exit codes for automation.

| Code | Name | Meaning |
|------|------|---------|
| 0 | ok | Success |
| 1 | error | General error |
| 2 | usage | Invalid arguments / bad syntax |
| 3 | empty_results | No results found (use with `--fail-empty`) |
| 4 | auth_required | OAuth token missing or expired |
| 5 | not_found | Resource not found |
| 6 | permission_denied | Insufficient permissions |
| 7 | rate_limited | Google API rate limit hit |
| 8 | retryable | Transient error, retry is safe |
| 10 | config | Configuration problem |
| 130 | cancelled | User cancelled (Ctrl-C) |

**Agent error handling pattern:**
```bash
gog gmail search "is:unread" --json --fail-empty
EXIT=$?
if [ $EXIT -eq 3 ]; then echo "No unread emails"; fi
if [ $EXIT -eq 4 ]; then echo "Auth expired -- run: gog login EMAIL"; fi
if [ $EXIT -eq 7 ]; then sleep 5 && retry; fi
```

## Multi-Account

`gog` supports multiple Google accounts. Use `-a EMAIL` to target a specific account.

```bash
# List authenticated accounts
gog auth list

# Target specific account
gog gmail search "is:unread" -a work@company.com --json
gog cal events --today -a personal@gmail.com --json

# Set default account
gog config set default_account work@company.com
```

## Common Gotchas

| Issue | Cause | Fix |
|-------|-------|-----|
| `auth_required` (exit 4) | Token expired or missing | Run `gog login EMAIL --services all` |
| `config` (exit 10) | No OAuth credentials JSON | Download from Google Cloud Console, run `gog auth credentials set FILE.json` |
| Gmail search returns threads, not messages | Gmail groups by thread by default | Use `gog gmail get MSG_ID` for individual messages |
| Calendar times wrong | Missing timezone in RFC3339 | Include timezone offset, e.g. `2026-02-18T09:00:00+00:00` |
| `rate_limited` (exit 7) | Too many API calls | Wait and retry. Use `--max` to limit results per call. |
| Docs markdown not rendering | Missing `--markdown` flag | Use `gog docs write DOC_ID --replace --markdown` |
| `--select` returns empty | Field path wrong | Run once with `--json` first to inspect schema |
| Slides from markdown: empty | Missing `--content` or `--content-file` | Provide content inline or via file |

## Error Handling

| Symptom | Exit code / signal | Recovery |
|---------|---------------------|----------|
| No results when data is expected | `3` (`empty_results`) | Re-run without `--fail-empty` to inspect envelope; broaden query or change filters |
| OAuth expired or missing | `4` (`auth_required`) | Run `gog login EMAIL --services all`, then `gog auth status` |
| API permission denied | `6` (`permission_denied`) | Re-auth with the needed scopes and verify API is enabled in Google Cloud |
| Rate limit hit | `7` (`rate_limited`) | Back off (`sleep`), reduce `--max`, retry with jitter |
| Transient backend error | `8` (`retryable`) | Retry with exponential backoff; keep idempotent operations safe |
| Invalid command/flags | `2` (`usage`) | Re-check command syntax in `references/gog-commands.md` |

## Anti-Patterns

| Do Not | Do Instead |
|--------|------------|
| Use `gog` without `--json` in automation | Always use `--json --no-input` |
| Send email without `--dry-run` first | Preview with `--dry-run`, then send |
| Fetch all pages of large results | Use `--max N`; paginating blindly wastes tokens |
| Hardcode account email in scripts | Use `-a EMAIL` or `default_account` config |
| Use `gog` for non-Google services | Use the right tool for the job |
| Skip `--no-input` in automation | Scripts cannot answer prompts |
| Use `--force` on delete without `--dry-run` | Always preview destructive operations |
| Ignore exit codes | Handle them explicitly (see table above) |

## Sandboxed / CI Environments

`gog` makes HTTPS calls to Google APIs. In sandboxed or CI environments, ensure network access is available.

| Operation Type | Sandbox Requirements |
|---------------|---------------------|
| Read-only (search, list, get) | Read-only sandbox + network access |
| Write operations (send, create, modify) | Write sandbox + network access |
| Complex pipelines with local file I/O | Full access (write + network) |

If your sandbox blocks outbound HTTPS, `gog` commands will fail with network errors. Ensure your environment allows connections to `*.googleapis.com`.

## Bundled Resources Index

| Path | What | When to Load |
|------|------|-------------|
| `./UPDATES.md` | Structured changelog for AI agents | When checking for new features or updates |
| `./UPDATE-GUIDE.md` | Instructions for AI agents performing updates | When updating this skill |
| `./references/installation-guide.md` | Detailed install walkthrough for Claude Code and Codex CLI | First-time setup or environment repair |
| `./references/gog-commands.md` | Full command reference for all 15 services | Need exact command syntax and flags |
| `./references/pipeline-patterns.md` | Composable patterns: `gog` + jq + multi-service workflows | Building complex automation |
| `./references/auth-setup.md` | OAuth setup, credentials, token handling, multi-account, headed + headless auth | First-time setup or auth troubleshooting |
