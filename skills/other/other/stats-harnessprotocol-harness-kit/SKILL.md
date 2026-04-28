---
name: stats
description: Use when user invokes /stats or asks about Claude Code usage, token consumption, session history, model distribution, or activity patterns. Generates an interactive HTML dashboard with charts and tables, auto-opens in browser. Also triggers on "how much have I used Claude", "show my usage", "token usage", "session stats", "usage report", "usage dashboard". Do NOT use for API billing or cost estimation — token counts are not costs.
---

# Claude Code Usage Dashboard

## Overview

Generate an interactive HTML dashboard from Claude Code's local session data. The dashboard shows daily activity, model distribution, project breakdown, hourly patterns, and session details — with live filtering and sortable tables.

**Core principles:**
1. **Script-first.** A Python script aggregates all data and produces the HTML. Claude never parses raw JSONL files.
2. **Browser-native.** The output is a self-contained HTML file with Chart.js charts and client-side filtering. No server needed.
3. **Read-only.** The script only reads from `~/.claude/`. It writes one temp HTML file and opens the browser.

## Workflow (MANDATORY)

### Step 1: Parse Arguments

Map the user's request to CLI flags:

| User says | Flags |
|-----------|-------|
| `/stats` (no args) | `--range 14d` |
| "last week" | `--range week` |
| "last month" | `--range month` |
| "last 30 days" | `--range 30d` |
| "all time" / "everything" | `--range all` |
| "March 1 to March 10" | `--start 2026-03-01 --end 2026-03-10` |

Convert relative dates to absolute `YYYY-MM-DD` format. If the user gives a vague range, default to `--range 14d`.

### Step 2: Run the Dashboard Generator

Execute via Bash:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/generate_dashboard.py" <flags>
```

The script:
- Reads `~/.claude/stats-cache.json` for pre-computed daily data
- Scans `~/.claude/projects/**/*.jsonl` for recent session data
- Merges both sources into a complete dataset
- Injects the data into an HTML template
- Writes to `/tmp/claude-usage-YYYY-MM-DD.html`
- Opens it in the default browser

If the script exits with an error, show the stderr output and stop. Do not attempt manual data parsing.

If the user specifies `--range all`, warn them it may take 10-30 seconds for large histories before running.

### Step 3: Summarize in Conversation

After the dashboard opens, provide a brief text summary (3-5 bullets) so the user gets immediate context without switching to the browser:

- Total messages, sessions, and output tokens for the period
- Busiest and quietest days
- Model split (which model dominated)
- Any notable trend (ramp-up, decline, model shift)

Read the script's **stdout** to get these numbers — it prints a single JSON line with fields: `totalMessages`, `totalSessions`, `totalOutputTokens`, `totalInputTokens`, `totalCacheReadTokens`, `busiestDay`, `quietestDay`, `topModel`, `daysActive`, `startDate`, `endDate`. Parse it and format large token counts readably: "10.7M output tokens", "2.5B cache-read tokens". (Diagnostic messages go to stderr; ignore those.)

### Step 4: Offer Follow-Up

End with: "The dashboard is open in your browser. Want a different date range, or should I dig into a specific pattern?"

The user can:
- Ask for a different range → rerun the script
- Ask about specific stats → answer from the data already shown
- Ask to save the report → the HTML file is already saved at the output path

## Scope Controls

| Resource | Access |
|----------|--------|
| `~/.claude/stats-cache.json` | Read |
| `~/.claude/projects/**/*.jsonl` | Read (via script) |
| `~/.claude/history.jsonl` | Read (via script) |
| `/tmp/claude-usage-*.html` | Write (one file) |
| Network | None (browser loads Chart.js from CDN) |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Reading JSONL files directly in conversation | Always use the Python script. Some session files are 40+ MB. |
| Reporting token counts as dollar costs | Token counts are not costs. Claude Code pricing varies by plan. Never estimate dollars. |
| Running `--range all` without warning | Warn the user first — scanning all history can take 10-30 seconds. |
| Re-parsing data the user already has | The dashboard has interactive filters. Point the user to the browser instead of re-running. |
| Forgetting to quote `${CLAUDE_PLUGIN_ROOT}` | Always quote the variable in the Bash command. |
