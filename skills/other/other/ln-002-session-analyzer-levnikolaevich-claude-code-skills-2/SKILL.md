---
name: ln-002-session-analyzer
description: "Analyzes current or recent session for errors, inefficiencies, and improvement opportunities across skills, tools, hooks, and communication. Use after completing a task or periodically."
license: MIT
allowed-tools: "Bash, Read, Glob, Grep, Agent, mcp__hex-line__read_file, mcp__hex-line__grep_search, mcp__hex-line__outline"
model: claude-sonnet-4-6
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Session Analyzer (Standalone Utility)

**Type:** Standalone Utility
**Category:** 0XX Shared

Analyzes a session for errors, inefficiencies, and improvement opportunities. Produces actionable fixes for skills, tools, hooks, and communication style.

**Scope:** Single-session deep analysis (10 dimensions). Broader than protocol self-audit, narrower than `/audit-sessions` batch.
For skill self-audit: `shared/references/meta_analysis_protocol.md` §7. For multi-day patterns: `/audit-sessions`.

---

## When to Use This Skill

- After completing a task — find what went wrong and how to improve
- Periodically — audit recent sessions for patterns
- After a skill run — analyze how well the skill instructions worked
- When debugging tool/hook issues — find root causes in session data

---

## Input

`$ARGUMENTS`:
- (empty) — analyze current session (conversation context)
- `recent` — scan latest JSONL session per agent (Claude, Codex, Gemini)
- `{skill-name}` — focus analysis on that skill's execution within the session

---

## Dimensions

| # | Dimension | Scan for | Improvement target |
|---|-----------|---------|-------------------|
| D1 | Tool Errors | NOOP_EDIT, TEXT_NOT_FOUND, hash mismatch, out of range | SKILL.md steps — add paths, anchors |
| D2 | Tool Waste | Full reads without outline, repeated reads, bash fallbacks | SKILL.md — "outline first", name MCP tools |
| D3 | Process Issues | Tool loops 3+, retry storms, dead ends, wrong targets | SKILL.md phases — decompose |
| D4 | Script Extraction | Ad-hoc bash/python scripts written each run | `references/scripts/` |
| D5 | Hook & Permission | Hook blocks, permission denials, built-in instead of MCP | Hook config, `allowed-tools` |
| D6 | Communication | Over-explaining, missing status, unnecessary confirmations | CLAUDE.md prefs, skill output notes |
| D7 | Decision Quality | Dead ends before pivot, trial-and-error, slow error detection | SKILL.md decision trees, step clarity |
| D8 | Context Pressure | Re-reading same files, re-asking resolved, thread loss | Caching notes, compact instructions |
| D9 | Subagent Quality | Empty results, timeouts, overbroad prompts | Agent prompts, timeout settings |
| D10 | Scope Drift | Deviation from goal, accidental expansion, pivot without reason | Scope guards, goal gates |

---

## Phase 1: Collect Session Data

Determine source based on `$ARGUMENTS`:

### Current session (empty args)

Scan conversation context directly. You have access to all tool call results, errors, and messages.

### Recent sessions (`recent` arg)

Find latest session per agent:

```bash
echo "=== LATEST SESSIONS ==="

echo "## Claude"
CLAUDE_LATEST=$(stat -c '%Y %n' ~/.claude/projects/*/*.jsonl 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)
[ -n "$CLAUDE_LATEST" ] && echo "  $CLAUDE_LATEST ($(wc -l < "$CLAUDE_LATEST") lines)" || echo "  No sessions found"

echo "## Claude Active Sessions"
for f in "$HOME/.claude/sessions"/*.json; do
  [ -f "$f" ] || continue
  PID=$(basename "$f" .json)
  kill -0 "$PID" 2>/dev/null && echo "  ACTIVE: $(cat "$f")" || echo "  STALE: PID=$PID"
done

echo "## Codex"
CODEX_LATEST=$(stat -c '%Y %n' ~/.codex/sessions/????/??/??/rollout-*.jsonl 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)
[ -n "$CODEX_LATEST" ] && echo "  $CODEX_LATEST ($(wc -l < "$CODEX_LATEST") lines)" || echo "  No sessions found"

echo "## Gemini"
# JSON path (Linux/macOS) or protobuf path (Windows)
GEMINI_LATEST=$(stat -c '%Y %n' ~/.gemini/tmp/*/chats/session-*.json ~/.gemini/antigravity/implicit/*.pb 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)
[ -n "$GEMINI_LATEST" ] && echo "  $GEMINI_LATEST (note: .pb files are protobuf, not grep-parseable)" || echo "  No sessions found"
```

### Extract raw data from JSONL session

Run for each found session file (`$F`):

```bash
echo "=== TOOL CALLS ==="
grep -oE '"name"\s*:\s*"[^"]*"' "$F" 2>/dev/null | sed 's/"name"\s*:\s*"//;s/"//' | sort | uniq -c | sort -rn | head -30

echo "=== ERRORS ==="
grep -oE 'NOOP_EDIT|TEXT_NOT_FOUND|FILE_NOT_FOUND|HASH_HINT|DANGEROUS|out of range|mismatch|tool_use_error|permission denied' "$F" 2>/dev/null | sort | uniq -c | sort -rn

echo "=== TOOL LOOPS (3+ consecutive) ==="
grep -oE '"name"\s*:\s*"[^"]*"' "$F" 2>/dev/null | sed 's/"name"\s*:\s*"//;s/"//' | uniq -c | sort -rn | awk '$1 >= 3'

echo "=== BUILT-IN vs MCP ==="
grep -oE '"name"\s*:\s*"(Read|Edit|Write|Grep|mcp__hex-line__\w+)"' "$F" 2>/dev/null | sed 's/.*"name"\s*:\s*"//;s/"//' | sort | uniq -c | sort -rn

echo "=== HOOK EVENTS ==="
grep -oE 'hook_progress|blocking error|PreToolUse|PostToolUse|hex-confirmed|Obligatory use|Use mcp__hex-line' "$F" 2>/dev/null | sort | uniq -c | sort -rn

echo "=== SKILL/COMMAND INVOCATIONS ==="
grep -oE '"display":\s*"/[a-z-]+' "$F" 2>/dev/null | sed 's/"display":\s*"//' | sort | uniq -c | sort -rn
```

### Extract token statistics from Claude JSONL

Run for Claude session file (`$F`) to get real token usage:

```bash
echo "=== TOKEN STATS ==="
TOTAL_IN=$(grep -oE '"input_tokens":[0-9]+' "$F" | grep -oE '[0-9]+' | paste -sd+ | bc 2>/dev/null)
TOTAL_OUT=$(grep -oE '"output_tokens":[0-9]+' "$F" | grep -oE '[0-9]+' | paste -sd+ | bc 2>/dev/null)
CACHE_CREATE=$(grep -oE '"cache_creation_input_tokens":[0-9]+' "$F" | grep -oE '[0-9]+' | paste -sd+ | bc 2>/dev/null)
CACHE_READ=$(grep -oE '"cache_read_input_tokens":[0-9]+' "$F" | grep -oE '[0-9]+' | paste -sd+ | bc 2>/dev/null)
echo "in=${TOTAL_IN:-0} out=${TOTAL_OUT:-0} cache_create=${CACHE_CREATE:-0} cache_read=${CACHE_READ:-0}"
```

---

## Phase 2: Analyze by Dimensions

Apply D1-D10 to collected data. Classify each finding:

| Severity | Dimensions | Meaning |
|----------|-----------|---------|
| **Error** | D1, D5 | Something broke — tool failed, permission denied |
| **Waste** | D2, D4, D8 | Unnecessary work — redundant reads, ad-hoc scripts, re-gathering |
| **Pattern** | D3, D6, D7, D9, D10 | Improvable behavior — loops, communication, decisions |

### D1: Tool Errors
Count by type: NOOP_EDIT, TEXT_NOT_FOUND, hash mismatch, out of range, FILE_NOT_FOUND. For each, identify which step/phase caused it.

### D2: Tool Waste
- Reads without preceding outline (file >100 lines)
- Same file read 3+ times
- Bash `cat`/`grep`/`head`/`sed` when MCP equivalent exists

### D3: Process Issues
- Tool loops: same tool on same file 3+ times without progress
- Retry storms: 3+ attempts with different parameters
- Dead ends: approach explored then abandoned
- Wrong target: looked at file X when needed Y

### D4: Script Extraction
- Bash/Python scripts written during session
- If script would be needed on every run of the skill → candidate for `references/scripts/`

### D5: Hook & Permission
- Hook blocks (PreToolUse/PostToolUse blocking errors)
- Built-in Read/Edit/Write/Grep used when MCP enforced
- `hex-confirmed` bypasses — were they justified?

### D6: Communication
- Message length distribution (over-explaining vs terse)
- Unnecessary confirmations ("shall I proceed?")
- Missing status updates at milestones
- Redundant summaries

### D7: Decision Quality
- Time to detect error and pivot (tool calls between error and correction)
- Trial-and-error sequences vs targeted approach
- Tool selection reasoning (used wrong tool first)

### D8: Context Pressure
- Same file read multiple times across phases
- Information re-gathered that was already available
- Signs of thread loss (re-asking resolved questions)

### D9: Subagent Quality
- Agent tool invocations with empty or low-value results
- Agent timeouts
- Overbroad prompts (agent did too much or too little)

### D10: Scope Drift
- Initial goal vs actual deliverables — any deviation?
- Unplanned additions during execution
- Pivots without explicit reason

---

## Phase 3: Map to Fixes

For each finding, determine specific target and fix:

| Target type | Example |
|------------|---------|
| SKILL.md step | "ln-400 Step 2: add file path `src/config.ts`" |
| SKILL.md phase | "ln-300 Phase 3: decompose into 3a-3c sub-steps" |
| `allowed-tools` | "ln-400: add `mcp__hex-line__edit_file`" |
| Hook config | "settings.json: add exception for `npm test`" |
| `references/scripts/` | "ln-520: move `test_harness.sh` to references/scripts/" |
| CLAUDE.md | "Add preference: terse responses, no trailing summaries" |
| MCP tool | "hex-line edit_file: hash mismatch on concurrent edits" |
| Agent prompt | "ln-310 Agent A: narrow scope to security-only" |
| Scope guard | "ln-400: add Goal Articulation Gate at Phase 1" |

---

## Phase 4: Report

Output to chat per `shared/references/meta_analysis_protocol.md` format.

```
### Session Analysis: {session identifier}

#### Improvements
| # | Dim | Finding | Target | Fix |
|---|-----|---------|--------|-----|
| 1 | D1 | 3 edit failures Phase 4 | ln-400 Step 2 | Add file path |
| 2 | D4 | test.sh written ad-hoc | ln-520 | Move to references/scripts/ |
| 3 | D6 | Over-explained 5 times | CLAUDE.md | Add "terse" pref |
| 4 | D5 | Hook blocked Read 4x | settings.json | Add MCP permission |

#### Session Errors
| Problem Type | Count | Examples |
|-------------|-------|---------|
| Retry storm | 4 | 3x edit_file on config.ts |
| Wrong target | 2 | Read utils.ts not helpers.ts |

#### Subagent Errors: {Agent Name}  (per agent, if any)
| Problem Type | Count | Examples |
|-------------|-------|---------|
| {type} | {N} | {brief} |

IF no findings AND no errors: "Session analysis: clean run."
```

---

## Anti-Patterns

| Do NOT | Instead |
|--------|---------|
| Define own output template | Reference protocol format |
| Analyze files not in session | Only analyze what was actually used |
| Generic recommendations | Each fix tied to specific file + location |
| Report OK dimensions | Only findings with issues |

---

## Phase 5: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Analyze this session per protocol §7. Output per protocol format.

---

## Definition of Done

- [ ] D1-D10 dimensions checked
- [ ] JSONL scanning works (`recent` mode)
- [ ] Each finding has specific Target + Fix
- [ ] Output per protocol format (improvements-only)
- [ ] No template duplication
- [ ] Meta-Analysis run

---

**Version:** 1.1.0
**Last Updated:** 2026-04-05
