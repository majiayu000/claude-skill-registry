---
name: gsuite
description: "Google Suite integration for Sheets, Docs, Slides, Gmail, Calendar, Tasks with multi-account support. Orchestrates operations via CLI tools. Triggers on keywords: google sheets, google docs, google slides, gsuite, gdrive, spreadsheet, document, gmail, google calendar, google tasks"
project-agnostic: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Skill
  - Task
---

# GSuite Skill

Google Suite integration for Claude Code with multi-account support (enterprise + personal).

## Capabilities

- Sheets: Read/write cells, create spreadsheets, append rows, manage sheets (list/add/rename/delete tabs)
- Docs: Read/write documents, create docs, export to PDF/DOCX, manage tabs (list/create/rename/delete)
- Slides: Read presentations, create slides, add content
- Drive: List files, share, manage permissions, create folders
- Gmail: Read/send/draft messages, search, manage labels
- Calendar: List/create/update/delete events, manage calendars
- Tasks: List/create/complete/delete tasks
- People: Search contacts, resolve names to emails before operations
- Comments: List/reply/resolve comments on any file type (Docs, Sheets, Slides) via Drive API, `@ac` convention for agent-directed comments
- Auth: Multi-account management with account switching

## Execution Mode

**Use platform-native subagents when available (`Task()` / subagent tool). Legacy spawn-command flows are not supported.**

Fallback: if subagent tooling is unavailable in the current runtime, execute GSuite tools directly via Bash.

| Complexity | Model Tier | Use For |
|------------|------------|---------|
| Simple reads | Low-tier (haiku/flash-lite) | `auth.py status`, `gmail.py list`, single API calls |
| Moderate | Medium-tier (sonnet/flash) | Multi-step operations, data processing, summarization |
| Complex | High-tier (opus/pro) | Cross-service operations, analysis requiring judgment |

Execution patterns and examples are in `cookbook/orchestration.md`. Use direct CLI calls with explicit inputs/outputs.

## Conventions

**Tools:** All PEP 723 uv scripts in `tools/` (skill-relative). All support `--help` and `--account/-a <email>`. Verify exact tool names first (`ls tools/`) - naming is inconsistent (e.g., `gcalendar` vs `docs`).

**Cookbook:** `<tool>.py` -> `cookbook/<tool>.md` (MANDATORY read before executing). If cookbook missing, check `<tool>.py --help` directly.

**Customization:** `<tool>.py` -> `~/.agents/customization/gsuite/<tool>.md`

**Comment Loop Workflow:** For agent-directed comment workflows, see `cookbook/comments.md`. Default filter: `@ac` (agent-directed comments).

**Large Content Strategy:** For multi-line or complex content (e.g.: docs, emails, slides):
1. Write content to temp file first (e.g., `/tmp/content.md`)
2. Pipe/cat file to CLI tool: `cat /tmp/content.md | uv run <tool>.py write ...`
3. Benefits: Avoids shell escaping issues, handles large content reliably, easier to debug

## Workflow

### 1. Initialize
- Get date context: `date "+%Y-%m-%dT%H:%M:%S %Z"`
- Check auth: `uv run auth.py status --json`
- Resolve account (ask if ambiguous, remember for session)

### 2. Load Preferences (BLOCKING)
**STOP. Check customization BEFORE any tool execution or API search.**
Check `~/.agents/customization/gsuite/` for:
- `index.md` (always)
- `<tool>.md` (if exists)
- `people.md` (if name mentioned)

### 3. Resolve People (BLOCKING)
**NEVER search People API before checking customization.**
If name (not email) mentioned:
1. **FIRST**: Check `~/.agents/customization/gsuite/people.md`
2. **ONLY IF NOT FOUND**: Fall back to People API via `cookbook/people.md`
3. Handle ambiguous matches via AskUserQuestion

### 4. Read Cookbook (BLOCKING)
**STOP. Read cookbook before executing any tool.**
1. Verify exact tool name: `ls tools/` (e.g., `docs.py` not `gdocs.py`)
2. Check `cookbook/<tool>.md` (exact match)
3. If no cookbook: `<tool>.py --help`

### 5. Execute & Report
Run tool, report results (status, data, errors).

### 6. Learn Preferences (Post-Execution)
On user correction -> read `cookbook/preferences.md` for storage flow.

## Anti-Patterns (NEVER DO)

- **NEVER create public assets** - All Drive files, Docs, Sheets, Slides must remain private. Never use `role: anyone`, `type: anyone`, or public visibility settings unless user explicitly requests AND confirms.
- Assuming tool names without verifying (`ls tools/` first)
- Searching People API before reading `people.md` customization
- Executing tools before reading their cookbook
- Skipping `index.md` preferences check

## Configuration

Config directory: `~/.agents/gsuite/`

```
~/.agents/gsuite/
  credentials.json          # OAuth client credentials
  service-account.json      # Enterprise service account (optional)
  config.yml                # Confirmation settings (optional)
  active_account            # Current active account
  accounts/<email>/token.json
```

### Confirmation Settings

Write operations require confirmation by default. Configure in `config.yml`:

```yaml
confirmation:
  default: true    # Global default
  gmail: true      # Per-tool override
  tasks: false     # Disable for specific tools
```

Use `--yes` or `-y` flag to bypass confirmation.

## Customization Framework

User-side behavior customizations live in `~/.agents/customization/`:

```
~/.agents/customization/
  <skill-name>/           # Per-skill customizations
    <tool>.md             # Tool-specific output format
```

- **NOT tracked in git** - user-local configuration
- Skills check for customizations before execution
- Example: `~/.agents/customization/gsuite/gcalendar.md` for calendar output format

## Extended API Access

For `--extra` parameter usage (recurring events, CC/BCC, subtasks, etc.), see `cookbook/extra.md`.

## Deprecated

- `comments.py` is deprecated. Use `drive.py comments`, `drive.py reply`, `drive.py resolve` instead.

## Error Handling

- No credentials: Read `cookbook/auth.md` for interactive setup
- Token expired: Auto-refresh via google-auth library
- Rate limit (429): Exponential backoff with retry
- Permission denied: Verify account has access to resource
