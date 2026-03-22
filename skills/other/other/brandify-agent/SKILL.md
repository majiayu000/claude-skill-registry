---
name: brandify-agent
description: "Convert agent log files (stream-json from Claude Code) into styled HTML reports using the Fenrir Ledger theme. Use when the user says 'brandify agent', 'agent report', 'prettify agent log', or wants to view agent execution logs as HTML."
---

# Brandify Agent — Agent Log to HTML Report

Converts Claude Code stream-json agent logs into styled, interactive HTML reports using the Fenrir Ledger visual system. Supports local HTML viewing and publishing as chronicles.

## Usage

```
/brandify-agent <session-id-or-log-path>
/brandify-agent <session-id-or-log-path> --publish
/brandify-agent --regen-assets
```

## Arguments

| Arg | Required | Description |
|-----|----------|-------------|
| `<session-id>` | Yes (unless `--regen-assets`) | Session ID (looks up `tmp/agent-logs/<id>.log`) or full path to `.log` file |
| `--publish` | No | Generate MDX output to `content/blog/` for chronicles publishing at `/chronicles/agent-{slug}` |
| `--regen-assets` | No | Regenerate shared CSS/JS files without processing a log |

## Workflow

### Step 1 — Download log from GKE cluster (ALWAYS try this first)

When given a session ID, **always** attempt to download the latest log from the GKE
cluster before falling back to any cached local copy. This ensures the report reflects
the most recent agent output, even if the agent is still running.

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
SESSION_ID="<session-id>"
LOG_DIR="$REPO_ROOT/tmp/agent-logs"
LOG_FILE="$LOG_DIR/$SESSION_ID.log"

# Always try to download fresh from GKE first
mkdir -p "$LOG_DIR"
kubectl logs "job/agent-$SESSION_ID" -n fenrir-agents --timestamps=false > "$LOG_FILE.tmp" 2>/dev/null
if [ -s "$LOG_FILE.tmp" ]; then
  mv "$LOG_FILE.tmp" "$LOG_FILE"
  echo "[ok] Downloaded fresh log from GKE: $LOG_FILE"
elif [ -f "$LOG_FILE" ]; then
  rm -f "$LOG_FILE.tmp"
  echo "[info] GKE download failed, using cached log: $LOG_FILE"
else
  rm -f "$LOG_FILE.tmp"
  echo "[error] No log available — GKE download failed and no cached copy"
  exit 1
fi
```

If the argument is a full file path (contains `/` or ends with `.log`), use it directly
(skip the download step — the user provided a specific file).

### Step 2 — Generate the report

**HTML mode (default):**
```bash
SCRIPT="$REPO_ROOT/.claude/skills/brandify-agent/scripts/generate-agent-report.mjs"
node "$SCRIPT" --input "$LOG_FILE"
```

Output goes to the same directory with `.html` extension (replacing `.log`).
Shared assets (`agent-report.css`, `agent-report.js`) are auto-generated alongside.

**Publish mode (`--publish`):**
```bash
SCRIPT="$REPO_ROOT/.claude/skills/brandify-agent/scripts/generate-agent-report.mjs"
BLOG_DIR="$REPO_ROOT/development/ledger/content/blog"
node "$SCRIPT" --input "$LOG_FILE" --publish --blog-dir "$BLOG_DIR"
```

Output: `content/blog/agent-{session-slug}.mdx` with frontmatter (title, date, rune, excerpt, slug, category: "agent"). Viewable at `/chronicles/agent-{slug}`. Uses `<details>`/`<summary>` for collapsible turns (no JS needed). Agent chronicles display with an "Agent" badge on the index and detail pages.

### Step 3 — Report

```
**Report generated:** `<html-path-or-mdx-path>`
**Turns:** N | **Tool calls:** N | **Errors:** N
**Verdict:** PASS/FAIL/none
Open: `open <html-path>` or view at `/chronicles/agent-{slug}`
```

## Metadata Detection

The report extracts session ID, branch, and model from multiple sources (in priority order):

1. **Entrypoint text lines** — GKE startup output before JSON events (Session:, Branch:, Model:)
2. **JSON `system/init` event** — Always present in stream-json logs (contains `model`, `session_id`)
3. **Filename** — Dispatch session ID pattern: `issue-<N>-step<S>-<agent>-<hash>.log`
4. **Git commands in log** — Branch name from `git branch --show-current` tool results

## Regenerate Assets

To regenerate shared CSS/JS without processing a log:

```bash
node "$SCRIPT" --regen-assets --output-dir tmp/agent-logs
```

## Output Structure

```
tmp/agent-logs/
  agent-report.css        ← shared theme (regenerable)
  agent-report.js         ← shared toggle logic (regenerable)
  issue-682-step2-loki-xxxx.log   ← raw log (input)
  issue-682-step2-loki-xxxx.html  ← styled report (output)
```

## Features

- Fenrir Ledger dark theme (void black, gold accents, Cinzel fonts)
- Collapsible turns with thinking, text, and tool blocks
- Color-coded tool badges (Bash=teal, Read=blue, Edit=amber, Write=gold, Todo=purple)
- Entrypoint section with color-coded status lines
- Summary bar with turn/tool/error counts
- Auto-detected QA verdict with PASS/FAIL styling
- Expand All / Collapse All controls
