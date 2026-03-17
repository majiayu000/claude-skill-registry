---
name: ai-session-tools
description: Search, recover, and analyze AI session histories across Claude Code, AI Studio, and Gemini CLI. Use when user asks to "find that file from last week", "search sessions", "recover context after compaction", "what did the AI do", "export session to markdown", "find corrections", "analyze session quality", "improve CLAUDE.md from past mistakes", or "turn AI mistakes into rules". Contains session search, file recovery, correction detection, self-improvement workflow.
version: "0.10.0"
user-invocable: true
disable-model-invocation: false
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# AI Session Tools

Search, recover, and analyze AI session histories across Claude Code, AI Studio, and Gemini CLI.

**Invoke with:** `/ar:ai-session-tools` or natural language like "find that file from last week", "search sessions for authentication", "recover context from session ab841016"

After a context compaction, a lost file, or a confusing session — `aise` finds it. In under a minute you can recover a file the AI (e.g. Claude / Gemini) wrote, restore the sequence of user requests, search every conversation you've ever had, or export a full session to markdown. Works across Claude Code, AI Studio, and Gemini CLI sessions simultaneously.

**Full flag reference:** `aise COMMAND --help`

## How It Works

1. **Find sessions** — `aise list` discovers sessions from `~/.claude/projects/` (Claude Code), AI Studio exports, and Gemini CLI. Filter by `--provider`, `--project`, `--since`.
2. **Search and recover** — `aise messages search`, `aise files search`, `aise tools search` find content across all sessions. `aise files extract` recovers files missing from disk.
3. **Analyze patterns** — `aise messages corrections` detects where users corrected the AI. `aise commands list/context` tracks slash command usage. `aise analyze` runs the full qualitative coding pipeline.
4. **Improve from mistakes** — Turn recurring corrections into permanent CLAUDE.md rules, skill updates, or hook blocks. Compare before/after correction counts to verify fixes worked (see Workflow 6).

---

## Quick Reference

All commands accept `--format json` for machine-readable output and `--full-uuid` for full 36-char session IDs.

| Goal | Action | Command | Key Options |
|------|--------|---------|-------------|
| How much history is indexed? | Count sessions, files, versions | `aise stats` | `--since 7d` `--provider claude` |
| Know which session contains the work you need | List all sessions, newest first | `aise list` | `--project P` `--since 7d` `--limit 20` |
| Narrow to Claude Code sessions only, excluding AI Studio / Gemini | Filter by provider | `aise list --provider claude` | `--since` `--until` `--full-uuid` |
| What did the user ask for in this session? | User request sequence — primary context signal | `aise messages get SESSION_ID --type user` | `--limit 10` |
| Restore the full conversation context | Every message in a session | `aise messages get SESSION_ID` | `--type user\|assistant` `--limit 10` |
| See what the user was asking for across recent sessions | User messages from the last N days | `aise messages search "" --type user --since 7d` | `--project P` `--context 3` `--no-compaction` |
| Find when a specific topic was discussed | Search all messages with surrounding context | `aise messages search "query"` | `--type user` `--context-after 3` `--regex` `--limit 20` |
| What tools did the AI (e.g. Claude / Gemini) call and how often? | Tool counts and files touched | `aise messages inspect SESSION_ID` | `--format json` |
| Reconstruct the exact sequence of events in a session | Chronological timeline with timestamps | `aise messages timeline SESSION_ID` | `--since 14:00` `--preview-chars 80` |
| Which sessions touched a specific file? | Search writes/edits by filename pattern | `aise files search --pattern "name.py"` | `--min-edits 2` `--include-sessions ID` `--include-extensions py ts` |
| See every version of a file the AI (e.g. Claude / Gemini) produced across sessions | Every saved version with session and date | `aise files history filename.py` | `--export` (write versioned files) `--stdout` (pipe all versions) |
| Recover a file missing from disk | Print latest saved version to stdout | `aise files extract filename.py` | `--version 3` `--restore` `--output-dir ./backup` |
| Did the AI's (e.g. Claude / Gemini) edits actually land on disk? | Present vs. missing edit check | `aise files cross-ref ./file.py` | `--session ID` `--format json` |
| See every file change the AI made to a specific file | Search tool calls by filename | `aise tools search Write "filename"` | `aise tools search Edit "file"` `aise tools search Read` |
| See every shell command the AI ran | Search Bash calls by substring | `aise tools search Bash "git commit"` | `--format json` `--limit 20` |
| Recover clipboard content the AI prepared | Extract pbcopy content | `aise messages extract SESSION_ID pbcopy` | `--format json` |
| Produce a persistent readable record of a session | Export session to markdown | `aise export session SESSION_ID` | `--output file.md` `--dry-run` |
| Document a sprint of AI-assisted work | Export last N days to a file | `aise export recent 7 --output week.md` | `--project myproject` |
| Find something that could be in a file or a message | Cross-domain search (`aise find` is an alias) | `aise search --pattern "*.py" --query "error"` | `--tool Write` `--query only` `--pattern only` |
| Identify where the AI (e.g. Claude / Gemini) went wrong and the user had to correct it | Detect correction patterns by category | `aise messages corrections` | `--pattern 'LABEL:regex'` `--project P` `--since` |
| Measure how consistently planning workflows were followed | Count planning invocations across sessions | `aise messages planning` | `--commands '/custom,/cmd'` |
| List every slash command invocation with metadata | When/where was each command used? | `aise commands list` | `--command /ar:plannew` `--ids-only` `--since 14d` |
| See what happened after a slash command | Context window post-invocation | `aise commands context /ar:plannew` | `--context-after 5` `--format json` |
| Pipe session IDs to another command | Composable workflows with xargs | `aise list --since 7d --ids-only` | `\| xargs -I{} aise messages get {}` |
| Filter to slash command messages only | Find real command invocations | `aise messages search "" --type slash` | `--since 14d` |
| Search with asymmetric context windows | See what came before/after a match | `aise messages search "error" --context-after 5` | `--context-before 2` |
| Exclude compaction summaries from search | Focus on real messages only | `aise messages search "query" --no-compaction` | |
| Search with regex pattern | Complex pattern matching with \| for OR | `aise messages search "forgot\|missed" --regex` | |
| Filter timeline events by pattern | Grep within a session timeline | `aise messages timeline SID --grep "error"` | `--regex` |
| Identify recurring AI mistakes across all sessions | Qualitative analysis pipeline | `aise analyze` | `--step analyze\|graph` `--org-dir DIR` `--status` `--force` |
| Turn recurring mistakes into permanent fixes | Apply corrections to CLAUDE.md, skills, or hooks | See Workflow 6 | Decision table: finding → target → example |
| Verify a fix actually reduced a failure | Compare correction counts before/after | `aise messages corrections --since 7d` | Compare to `--since 30d` baseline |
| Narrow analyze to one provider | Provider goes at root level | `aise --provider claude analyze` | `aise --provider aistudio analyze` |
| Stop indexing sessions from a removed or unwanted directory | Deregister a session source | `aise source remove /path/to/dir` | `aise source disable claude` |
| What date formats work with --since? | Date format examples and shorthands | `aise dates` | |

For multi-step tasks, follow a workflow below.

---

## Workflows

### 1. Recover lost context after compaction

```bash
# Find the session
aise list --since 7d

# Get the user request sequence — what was being accomplished, without assistant noise
# This is the primary context signal: ordered user intent, compact, no assistant verbosity
aise messages get SESSION_ID --type user

# Read the full conversation if more detail is needed
aise messages get SESSION_ID

# Find files the AI was editing in that session
aise files search --include-sessions SESSION_ID

# Restore a specific file to its original path on disk
aise files extract filename.py --restore

# Export session to markdown for persistent reference
aise export session SESSION_ID --output session-context.md
```

---

### 2. Recover a file the AI (e.g. Claude / Gemini) wrote that is missing from disk

```bash
# Find which sessions wrote or edited the file
aise files search --pattern "filename.py"

# Every version: how many edits, which sessions, which dates
aise files history filename.py
aise files history filename.py --export   # write versioned files: filename_v1.py, filename_v2.py, ...
aise files history filename.py --stdout   # all versions to stdout for piping

# Preview a specific version
aise files extract filename.py --version 3

# Restore the latest version to its original path on disk
aise files extract filename.py --restore

# Or write to a backup directory instead
aise files extract filename.py --output-dir ./backup
```

---

### 3. Audit what the AI (e.g. Claude / Gemini) did in a session

```bash
# Find the session
aise list --project myproject

# Tool counts, files touched — quick overview without reading everything
aise messages inspect SESSION_ID

# Chronological event timeline with timestamps
aise messages timeline SESSION_ID

# Read the full conversation
aise messages get SESSION_ID
```

---

### 4. Turn recurring AI mistakes into permanent fixes in skills, prompts, and guidelines

Use this to find what the AI gets wrong repeatedly, extract corrections, and turn them into
skill rules, CLAUDE.md additions, or hook integrations to prevent recurrence (see Workflow 6).

```bash
# Find messages where the user corrected the AI
# Built-in categories: regression, skip_step, misunderstanding, incomplete
aise messages corrections

# Filter to a specific project, session, or date range
aise messages corrections --project myproject --since 2026-01-01
aise messages corrections --session ab841016

# Add a custom pattern to detect a specific failure type (LABEL:regex)
aise messages corrections --pattern 'tool_misuse:you used the wrong'
aise messages corrections --pattern 'context_loss:you forgot'

# Pipe correction session IDs to another command
aise messages corrections --since 14d --ids-only | \
    xargs -I{} aise messages search "you deleted" --session {} --context-after 3

# How often were planning commands used? (add --commands to count custom slash commands)
aise messages planning
aise messages planning --commands '/myteam:plan,/myteam:review'

# Full qualitative analysis across all sessions:
#   - technique taxonomy, error graph, project classification
#   - use output to extract effective prompts, find recurring failure types,
#     build new skills, update CLAUDE.md rules, hook integrations, or skills (see Workflow 6)
aise analyze --status                  # check which stages are stale before running
aise analyze                           # run the full pipeline
aise --provider claude analyze         # scope to one source only (--provider is a root flag)
aise analyze --step analyze            # run one stage: analyze | graph
aise analyze --force                   # re-run all stages regardless of staleness
aise analyze --org-dir ~/my-org        # override output directory for this run
```

To make custom patterns permanent across all future runs, add them to `correction_patterns`
in the config file — see Workflow 5.

---

### 5. Make custom failure categories permanent across all future sessions

```bash
aise config path    # find the config file location
aise config show    # view all current values
aise config init    # create a starter config if it doesn't exist yet
```

**`correction_patterns`** — persistent failure categories for `aise messages corrections`.
Format: `"LABEL:regex"` — label names the category, regex matches in message text.

```json
"correction_patterns": [
  "regression:you deleted",
  "regression:you removed",
  "skip_step:you forgot",
  "skip_step:you missed",
  "misunderstanding:that's wrong",
  "incomplete:also need",
  "tool_misuse:you used the wrong tool",
  "context_loss:you forgot what we were working on",
  "overengineered:that's too complex"
]
```

**`planning_commands`** — which slash commands count toward `aise messages planning`.
Add your own project-specific planning commands:

```json
"planning_commands": ["/ar:plannew", "/ar:planrefine", "/ar:planupdate", "/myteam:plan"]
```

**`keyword_maps`** — classify sessions by project, task type, and workflow for `aise analyze` taxonomy.
Empty by default — fill in to get meaningful session categorization:

```json
"keyword_maps": {
  "project_map": {
    "myproject": ["myproject", "my-project", "myproj"]
  },
  "task_categories": {
    "auth": ["login", "jwt", "oauth", "token"],
    "api": ["endpoint", "rest", "graphql"],
    "testing": ["pytest", "unittest", "test suite"]
  }
}
```

**`scoring_weights.corrected_bonus`** (default: 25) — sessions where the user corrected the AI
score higher in the `aise analyze` pipeline, making them more prominent in the output taxonomy.
Increase to weight corrected sessions more heavily when looking for improvement signals.

---

### 6. Act on analysis — turn findings into permanent improvements

After running `aise messages corrections` or `aise analyze`, apply what you found.
The goal: each recurring failure becomes a rule that prevents it in future sessions.

**Where to apply fixes (pick the right target):**

| Finding | Target | Example |
|---------|--------|---------|
| AI uses wrong tool repeatedly | CLAUDE.md rule | "Always use Read tool, never cat" |
| AI skips a step in workflow | Skill update | Add step to existing skill's workflow |
| AI runs dangerous command | Hook integration | Add to DEFAULT_INTEGRATIONS in config.py |
| AI misunderstands domain term | CLAUDE.md definition | "In this project, 'deploy' means..." |
| AI pattern applies to many projects | New skill | Extract via /claude-skill-builder |

**CLAUDE.md — add rules from corrections:**

```bash
# Find what you corrected the AI about most
aise messages corrections --since 30d

# Example output: 5x "you used cat instead of Read"
# → Add to CLAUDE.md:
#   "Never use cat/head/tail in Bash. Use the Read tool instead."

# Example output: 3x "you forgot to run tests"
# → Add to CLAUDE.md:
#   "After every code change, run the test suite before committing."
```

Rules go in your project's `CLAUDE.md` (checked into git) or `~/.claude/CLAUDE.md` (global).
One concrete sentence per rule. Avoid vague guidance — state exactly what to do or not do.

**Hook integrations — block dangerous commands:**

If corrections show repeated dangerous command usage, add a block:
```bash
/ar:globalno 'dangerous-command'   # block globally across sessions
```

**Skills — extract reusable workflows:**

When corrections reveal a missing workflow (not just a single rule), create a skill:
```bash
/claude-skill-builder
```

**Verify the fix worked:**

```bash
# After adding a rule, check if the same correction reappears
aise messages corrections --since 7d --pattern 'LABEL:the pattern you fixed'

# Compare before/after counts
aise messages corrections --since 30d   # before: 5 occurrences
# ... wait a week of sessions ...
aise messages corrections --since 7d    # after: 0 occurrences = success
```

---

### 7. Composable pipelines — pipe session IDs between commands

Use `--ids-only` to chain aise commands via xargs for multi-step analysis.

```bash
# Find sessions with corrections, then search each for specific patterns
aise messages corrections --since 14d --ids-only | \
    xargs -I{} aise messages search "you deleted" --session {} --context-after 3

# Find sessions using a specific slash command, export each
aise commands list --command /ar:plannew --since 14d --ids-only | \
    xargs -I{} aise export session {} --output {}.md

# List sessions, search each for error patterns
aise list --since 7d --ids-only | \
    xargs -I{} aise messages search "error|failed|bug" --session {} --regex
```

---

### 8. Analyze slash command patterns across sessions

Track slash command usage and post-invocation context with `commands list` and
`commands context`.

```bash
# List all slash command invocations (auto-discovers all commands)
aise commands list --since 14d

# Filter to a specific command
aise commands list --command /ar:plannew --since 14d

# See what Claude did after each invocation of a command (context window)
aise commands context /ar:plannew --context-after 5

# JSON output for scripting
aise commands list --format json --since 14d

# Count unique commands used
aise commands list --since 30d --format json | python3 -c "
import json, sys; from collections import Counter
d = json.load(sys.stdin)
print(Counter(r['command'] for r in d).most_common())"
```

---

## Sources

Claude Code sessions are auto-discovered from `~/.claude/projects/`. AI Studio and Gemini CLI
require configuration:

```bash
aise source scan --save                        # scan standard locations; --save writes found paths to config
aise source add /path/to/aistudio              # add AI Studio export directory (type auto-detected)
aise source add /path/to/aistudio --type aistudio  # add with explicit type
aise source add ~/.gemini/tmp --type gemini    # add Gemini CLI directory
aise source remove /path/to/dir               # remove a source directory from config by path
aise source disable aistudio                  # disable AI Studio auto-discovery (also: gemini_cli)
aise source enable aistudio                   # re-enable auto-discovery (also: gemini_cli)
aise source list                              # show all active sources (auto-detected + configured)
```

---

## Configuration

The config file controls persistent failure detection patterns (`correction_patterns`), planning command tracking (`planning_commands`), session taxonomy keywords (`keyword_maps`), and analysis scoring weights — see Workflow 5 for details.

Config file location (priority order):
1. `--config /path/config.json` CLI flag — per-invocation override
2. `AI_SESSION_TOOLS_CONFIG=/path/config.json` env var — session-wide override
3. OS default: `~/Library/Application Support/ai_session_tools/config.json` (macOS) or `~/.config/ai_session_tools/config.json` (Linux)

Override `~/.claude` location: `--claude-dir /path` or `CLAUDE_CONFIG_DIR=/path`

```bash
aise config show                             # view full config + resolved path
aise config path                             # print config file path only
aise config init                             # create default config (safe — errors if file exists)
aise config init --force                     # overwrite existing config
aise --config /custom/path.json config init  # create config at a specific path
```

---

## Date Filtering

Three flags control date ranges on all commands that support them:

| Flag | Purpose | Example |
|------|---------|---------|
| `--since` | Lower bound (inclusive) | `--since 7d` `--since 2026-01-15` |
| `--until` | Upper bound (inclusive) | `--until 2026-03-01` |
| `--when` | Set both bounds at once — for EDTF period patterns | `--when 202X` `--when 2026-01` |

Accepted formats (all three flags):

| Format | Example | Matches |
|--------|---------|---------|
| Duration shorthand | `7d` `2w` `1m` `24h` | Last N days/weeks/months/hours |
| ISO date | `2026-01-15` | That exact day |
| Partial date | `2026-01` `2026` | All of January 2026 / all of 2026 |
| EDTF unspecified digit | `202X` `2026-01-1X` | 2020s decade / Jan 10–19 2026 |
| EDTF interval (`--since` only) | `2026-01/2026-03` | Jan through Mar 2026 (sets both bounds) |

Use `--when` for decade/month/partial-date patterns where a single expression sets the full window.
Use `--since` + `--until` for explicit asymmetric ranges.

Run `aise dates` for the full reference.

---

## Output Formats

All commands support `--format` / `-f`:

| Format | Use When |
|--------|----------|
| `table` | Default — human-readable in terminal |
| `json` | Scripting, piping to `jq`, programmatic use |
| `csv` | Spreadsheet import |
| `plain` | Raw text, minimal formatting |

---

## Session File Location

`~/.claude/projects/<ENCODED-PATH>/<SESSION-ID>.jsonl`

Path encoding: all non-alphanumeric characters → `-`
- `/Users/alice/myproject` → `-Users-alice-myproject`
- `/Users/alice/.claude` → `-Users-alice--claude` (dot → dash)

Each JSONL line is a JSON object with `type` (`user`/`assistant`/`system`), `timestamp`, and `message` containing tool calls and text content.

See `references/session-format.md` for the full format reference.

---

## Full Flag Reference

`aise COMMAND --help` — every subcommand has a `--help` flag with full option descriptions.

**`aise` not found?** Run `autorun --install --force` or `uv tool install ai-session-tools`.
