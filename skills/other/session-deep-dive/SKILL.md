---
name: session-deep-dive
description: Deep qualitative analysis of high-signal sessions. Spawns subagents with v2 template, synthesizes patterns, compares against known findings. Use after /session-scan.
argument-hint: "<session-id> | --last | --from-scan [--compare REPORT.md]"
disable-model-invocation: true
---

# Session Deep Dive (Tier 2)

Qualitative analysis of high-signal sessions identified by `/session-scan`.
Spawns subagents with pre-computed metrics context for focused analysis.

## Requirements

Requires **ccrider MCP**. If not available:

> ccrider MCP is required. See: <https://github.com/neilberkman/ccrider>

## Usage

```
/session-deep-dive ffa155ee-ed8a-492c-8797-878fcbec4d9e
/session-deep-dive --last                    # Most recent Tier 2 eligible
/session-deep-dive --from-scan               # All Tier 2 eligible from last scan
/session-deep-dive --from-scan --compare .claude/UPDATED_PLUGIN_REPORT_160_SESSIONS.md
```

## Pipeline

### Step 1: Resolve Target Sessions

From `$ARGUMENTS`:

- **Session ID**: Single session to analyze
- **`--last`**: Most recent Tier 2 eligible session from metrics.jsonl
- **`--from-scan`**: All sessions where `tier2_eligible: true` AND
  `tier2_completed: false` in `.claude/session-metrics/metrics.jsonl`
- **`--compare REPORT.md`**: Previous report to compare against
  (default: most recent `.claude/session-analysis/insights-*.md`)

If no metrics.jsonl exists, tell the user:

> No metrics found. Run `/session-scan` first to discover and score sessions.

### Step 2: Load Pre-computed Metrics

For each target session, read its entry from `metrics.jsonl`.
Format the metrics as a context block for subagent prompts:

```
## Pre-computed Metrics (from /session-scan)

- Friction: 0.42 (retry_loops: 1, user_corrections: 3, approach_changes: 2)
- Fingerprint: bug-fix (confidence: 0.85)
- Plugin opportunity: 0.65 (could use: investigate, quick)
- Tool profile: Read 28.7%, Edit 15.2%, Bash 19.3%, Tidewave 22.8%
- Duration: 78 minutes, 19 user messages, 171 tool calls
```

Determine `PROJECT_ROOT` from current working directory.

### Step 3: Fetch Transcripts — One Subagent Per Session

**CRITICAL: One ccrider call = one subagent.** Full transcripts are
5-30KB each. Even 3 per worker floods the worker's context.

For EACH session, spawn a **haiku** subagent:

```
Task(subagent_type="general-purpose", model="haiku", mode="bypassPermissions", prompt="""
Fetch one session transcript and save it.

1. mcp__ccrider__get_session_messages(session_id: "{SESSION_ID}")
   If > 200 messages: use last_n: 200

2. Write transcript to {PROJECT_ROOT}/.claude/session-analysis/{SHORT_ID}-transcript.md
   Format:
   # Session: {SHORT_ID}
   Project: {PROJECT}
   Date: {DATE}
   Messages: {COUNT}

   ## Messages
   ### User (seq N)
   {content}
   ### Assistant (seq N)
   {content}

3. Report: "Wrote {SHORT_ID}-transcript.md ({N} messages)"
""")
```

**Spawn ALL fetch subagents in parallel.** Wait for all to complete.

### Step 4: Analyze Sessions

Read the analysis template — inline it into subagent prompts:

```
Glob: **/session-deep-dive/references/analysis-template-v2.md
```

**ALWAYS use subagents** — never analyze in main context.

- **1-6 sessions**: Spawn **sonnet** subagents (one per session)
- **7+ sessions**: Spawn **haiku** subagents for speed

Each analysis subagent prompt:

> Read the session transcript at {transcript_path}.
> Apply the analysis template below to analyze this session.
> The pre-computed metrics below give you quantitative context —
> validate them and add qualitative depth.
>
> {metrics_context_block}
>
> {analysis_template_content}
>
> Write your report (under 200 lines) to {report_path}.

Reports go to `.claude/session-analysis/{short_id}-report.md`.

### Step 5: Compress (if 3+ sessions)

If 3+ sessions analyzed, spawn context-supervisor (haiku) to compress:

> Read all report files in `.claude/session-analysis/*-report.md`.
> Write a consolidated summary to `.claude/session-analysis/summaries/consolidated.md`.
> Preserve: friction patterns, plugin opportunities, evidence strength tags.
> Remove: per-file details, generic observations, repeated context.

### Step 6: Synthesize

Read the synthesis template:

```
Glob: **/session-deep-dive/references/synthesis-template.md
```

Read the `--compare` report (or latest insights file).
Read `MEMORY.md` for known findings.

If 3+ sessions: read `summaries/consolidated.md` (NOT individual reports).
If 1-2 sessions: read individual reports directly.

Produce synthesis comparing:

- New findings vs known patterns from MEMORY.md
- Confirmed patterns (seen before, still present)
- New patterns (not in previous reports)
- Resolved patterns (previously noted, no new occurrences)

### Step 7: Update Ledger

Use Python to safely update `metrics.jsonl` — never manually
read/modify/rewrite in the LLM context:

```bash
python3 -c "
import json
ids = {SESSION_IDS_SET}  # e.g., {'ffa155ee-...', '90a74843-...'}
lines = open('{PROJECT_ROOT}/.claude/session-metrics/metrics.jsonl').readlines()
with open('{PROJECT_ROOT}/.claude/session-metrics/metrics.jsonl', 'w') as f:
    for line in lines:
        entry = json.loads(line)
        if entry.get('session_id') in ids:
            entry['tier2_completed'] = True
        f.write(json.dumps(entry) + '\n')
"
```

### Step 8: Write Output

Write synthesis to `.claude/session-analysis/insights-{date}.md`

Present key findings directly in conversation. Tell user:

> Full report: `.claude/session-analysis/insights-{date}.md`
> Per-session reports: `.claude/session-analysis/{id}-report.md`

## Output Files

| File | Purpose |
|------|---------|
| `.claude/session-analysis/{id}-transcript.md` | Raw transcript |
| `.claude/session-analysis/{id}-report.md` | Per-session analysis |
| `.claude/session-analysis/summaries/consolidated.md` | Compressed reports |
| `.claude/session-analysis/insights-{date}.md` | Cross-session synthesis |

## Iron Laws

1. **ONE ccrider call = ONE subagent** — never batch multiple fetches
2. **NEVER fetch or analyze in main context** — always subagents
3. **Absolute paths in subagent prompts** — subagents don't inherit skill context
4. **Python for jsonl updates** — never manually rewrite in LLM context
5. **ALWAYS pass pre-computed metrics to analysis subagents** — don't re-derive
6. **NEVER skip synthesis** — cross-session patterns are the real value
7. **TAG evidence strength** — every finding must be STRONG/MODERATE/WEAK
