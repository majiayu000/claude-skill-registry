---
name: session-scan
description: Compute metrics for Claude Code sessions. Discovers via ccrider, filters trivial, computes friction/opportunity/fingerprint scores. Use for broad session triage.
argument-hint: "[--since DATE] [--project NAME] [--limit N] [--list] [--rescan]"
disable-model-invocation: true
---

# Session Scan (Tier 1)

Compute deterministic metrics for sessions discovered via ccrider MCP.

## STOP — Read Before Executing

**NEVER call `mcp__ccrider__get_session_messages` in main context.**
Each response is 5-50KB of JSON. Fetching N sessions directly = context crash.

**You MUST delegate all scoring to subagents.** The main context only does:
discovery, deduplication, subagent spawning, and result collection.

## Requirements

Requires **ccrider MCP**. If not available:

> ccrider MCP is required. See: <https://github.com/neilberkman/ccrider>

## Usage

```
/session-scan                         # Last 7 days, up to 50 sessions
/session-scan --since 2026-02-01      # Since specific date
/session-scan --project enaia         # Filter by project name
/session-scan --limit 20              # Cap session count
/session-scan --list                  # Discovery only, no scoring
/session-scan --rescan                # Recompute already-scanned sessions
```

## What Main Context Does

### 1. Parse Arguments

Extract from `$ARGUMENTS`:

- **`--since DATE`**: ISO date filter (default: 7 days ago)
- **`--project NAME`**: Filter by project path substring
- **`--limit N`**: Max sessions to process (default: 50)
- **`--list`**: Discovery only — show table, skip scoring
- **`--rescan`**: Recompute metrics for already-scanned sessions

### 2. Discover Sessions (safe — response is ~1KB)

```
mcp__ccrider__list_recent_sessions(limit: N, project: PROJECT, after_date: SINCE)
```

Filter out sessions with < 10 messages. If `--list`: show table and stop.

### 3. Deduplicate

Read `.claude/session-metrics/metrics.jsonl` (if exists).
Skip sessions already scanned unless `--rescan` flag is set.
Report: "N new sessions to scan (M already in ledger)"

### 4. Resolve Scorer Path

```
Glob: **/session-scan/references/compute-metrics.py
```

Store as `SCORER_PATH` (absolute). `PROJECT_ROOT` = current working directory.

### 5. Spawn ONE Subagent Per Session

**DO NOT fetch messages yourself. DO NOT run Python yourself.**
**You MUST use the Task tool to spawn subagents.**

For EACH unscanned session, spawn a haiku subagent using this template:

```
Task(subagent_type="general-purpose", model="haiku", mode="bypassPermissions", prompt="""
Score one Claude Code session. Steps:

1. Fetch messages:
   mcp__ccrider__get_session_messages(session_id: "{SESSION_ID}", last_n: 200)

2. Write the full tool result (messages JSON) to:
   {PROJECT_ROOT}/.claude/session-metrics/_tmp_{SHORT_ID}.json

3. Run scorer and capture result in ONE Bash command:
   python3 {SCORER_PATH} {PROJECT_ROOT}/.claude/session-metrics/_tmp_{SHORT_ID}.json --session-id {SESSION_ID} --project {PROJECT_NAME} > {PROJECT_ROOT}/.claude/session-metrics/_result_{SHORT_ID}.json && rm {PROJECT_ROOT}/.claude/session-metrics/_tmp_{SHORT_ID}.json

4. Report back: "Scored {SHORT_ID}: friction=X.XX fingerprint=Y"

If ccrider fails, report the error and exit.
""")
```

**Spawn ALL subagents in parallel.** Wait for all to complete.

### 6. Collect Results

```bash
for f in .claude/session-metrics/_result_*.json; do
  cat "$f" >> .claude/session-metrics/metrics.jsonl
  rm "$f"
done
```

### 7. Display Results

Show summary table sorted by friction (descending):

```
| ID       | Project | Date       | Type        | Friction | Opportunity | Tier2? |
|----------|---------|------------|-------------|----------|-------------|--------|
| ffa155ee | enaia   | 2026-02-18 | bug-fix     | 0.42     | 0.65        | Yes    |
| 90a74843 | wedding | 2026-02-17 | feature     | 0.15     | 0.20        | No     |
```

If Tier 2 eligible: suggest `/session-deep-dive --from-scan`.

### 8. Update Scan Metadata

Write `.claude/session-metrics/latest-scan.json`:

```json
{
  "scanned_at": "2026-02-20T14:30:00Z",
  "sessions_discovered": 25,
  "sessions_scanned": 18,
  "sessions_skipped": 7,
  "tier2_eligible": 5
}
```

## Scoring Reference

See `references/scoring-guide.md` for full algorithm documentation.

- **Friction Score** (0-1): Weighted signals, sigmoid-normalized
- **Fingerprint**: Rule-based classifier (6 types)
- **Plugin Opportunity** (0-1): Missed `/phx:` commands
- **Tier 2 Eligible**: friction > 0.35 OR opportunity > 0.5 OR plugin used OR msgs > 50

## Iron Laws

1. **NEVER call `get_session_messages` in main context** — WILL crash context
2. **ONE subagent per session** — each fetches exactly ONE session
3. **`mode="bypassPermissions"` on every Task** — subagents need Write+Bash
4. **Absolute paths in subagent prompts** — subagents don't inherit context
5. **Result files, not direct append** — avoid jsonl race conditions
6. **NEVER modify existing metrics.jsonl entries** — append-only ledger
7. **ALWAYS delete temp and result files** after processing
