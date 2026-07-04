---
name: explanation-traces
description: "Query and display structured decision traces from routing, agent selection, and skill execution."
user-invocable: true
argument-hint: "<optional: specific decision to explain>"
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
routing:
  triggers:
    - "why did you"
    - "explain routing"
    - "show trace"
    - "decision log"
    - "why that agent"
    - "explain decision"
    - "show decisions"
    - "trace log"
  force_route: true
  not_for: "general 'why did the test fail' debugging, explaining concepts to a user, code documentation, stack traces — only for querying recorded routing/agent decisions"
  pairs_with: []
  complexity: Simple
  category: analysis
---

# Explanation Traces: Structured Decision Query

## Overview

This skill reads the per-dispatch route event log and presents routing decisions and their outcomes as a human-readable timeline. It answers "why did I get routed here?" from what was recorded at decision time — never from post-hoc reconstruction or rationalization.

**The log**: `<CLAUDE_LEARNING_DIR>/route-events.jsonl`, default `~/.claude/learning/route-events.jsonl`. Append-only JSONL — one JSON object per line. Written via `hooks/lib/route_events.py` by two producers:

| Producer | Fires on | Appends |
|---|---|---|
| `hooks/routing-decision-recorder.py` | PostToolUse (Agent dispatch) | One DECISION event per /do-routed dispatch |
| `hooks/routing-outcome-finalizer.py` | UserPromptSubmit | One OUTCOME event when it finalizes a pending dispatch |

The log is auxiliary instrumentation: writes are failure-safe (worst case one lost line), and the aggregate routing rows in learning.db stay authoritative for the confidence loop.

**Key constraints baked into the workflow:**
- Read-only: this skill never modifies the log or any other file
- Answers must come from recorded events, not from memory or inference about what "probably happened"
- If no log exists, name the real path and the real producing hook rather than guessing at decisions
- When the user asks about a specific decision, filter to that decision — skip the full dump
- `ts` (epoch seconds) and recorded fields are authoritative; keep their precision
- `request_snippet` is private session data: show it to this session's own user, and keep it out of anything that leaves the session (PR bodies, issues, exports) — report counts there instead

---

## Instructions

### Phase 1: LOCATE

**Goal**: Find the route event log.

**Step 1: Resolve the path and check it**

```bash
LOG="${CLAUDE_LEARNING_DIR:-$HOME/.claude/learning}/route-events.jsonl"
wc -l "$LOG"
```

`CLAUDE_LEARNING_DIR` redirects the log (tests and redirected DBs use it); unset means the default `~/.claude/learning/`.

**Step 2: Handle missing log**

If the file is absent or empty, stop and inform the user:

```
No route event log found at ~/.claude/learning/route-events.jsonl
(or $CLAUDE_LEARNING_DIR/route-events.jsonl when that variable is set).

The log is created on the first /do-routed dispatch by the
routing-decision-recorder hook (hooks/routing-decision-recorder.py).
An empty or missing log means no /do-routed dispatch has been recorded
yet — or merged hook changes were never synced to ~/.claude; run
hooks/sync-to-user-claude.py or restart the session.
```

Recorded events are the only source this skill reads. Reconstructing decisions from memory or conversation history defeats its purpose — with no log, there is nothing to read, and the honest answer is exactly that.

**GATE**: Log found and non-empty. Proceed only when gate passes.

### Phase 2: PARSE

**Goal**: Extract events and filter to the user's query.

**Step 1: Read the events**

Parse each line as one JSON object. Two event types (full semantics: `references/trace-schema.md`; source of truth: `hooks/lib/route_events.py`).

DECISION — one per /do-routed dispatch:

| Field | Meaning |
|---|---|
| `ts` | Epoch seconds (float) when the dispatch was recorded |
| `session` | Session id (`""` when unknown) |
| `request_snippet` | First 200 chars of the routed request |
| `agent`, `skill`, `complexity` | The chosen route |
| `health_at_decision` | Picked pair's confidence at decision time; `null` = no weight row or never evaluated (disambiguate with `gate_inputs_present`) |
| `n`, `failure` | The other demote-floor inputs, snapshotted with health |
| `action` | Step-1.5 health-gate outcome: `keep`, `demote`, or `tiebreak` |
| `alternates` | Keys offered as alternatives; `null` when none recorded |
| `gate_inputs_present` | `true` = the marker carried a `health=` token; `false`/absent = legacy marker, health never read |

OUTCOME — one per finalized dispatch:

| Field | Meaning |
|---|---|
| `ts` | Epoch seconds when the outcome was finalized |
| `session` | Session id |
| `key` | Routing key `{agent}:{skill}` (agent-only `{agent}:` when skill unknown) |
| `outcome` | `success`, `failure`, or `neutral` |
| `reason` | Short cause (e.g. `tool-errors`, `rejection`, `acceptance`, `neutral-new-topic`); absent in older events |
| `routing_relevant` | `true` = a signal the confidence loop acts on; absent = relevance not asserted |

Additive-field history: older lines may lack `n`, `failure`, `action`, `alternates`, `gate_inputs_present`, `reason`, `routing_relevant`. An absent field means "not recorded then", never corruption.

**Step 2: Filter to the user's query**

| User signal | Filter strategy |
|-------------|-----------------|
| Names an agent or skill | DECISION events where `agent` or `skill` matches, or the name appears in `alternates`; OUTCOME events whose `key` contains it |
| "Why did I get routed here" / latest dispatch | Most recent DECISION events (tail of the log), current session first |
| Asks about outcome ("did it work", "why failure") | OUTCOME events, joined back to their decisions |
| Names a session | Filter both types on `session` |
| No specific target | Chronological timeline of the most recent session |

**Step 3: Join outcomes to decisions**

Match an OUTCOME to its DECISION on the same `session` AND `key == "{agent}:{skill}"`. A decision with no matched outcome is pending (the finalizer runs on a later user prompt) or was never finalized — report that state as-is.

**GATE**: At least one decision event parsed and filtered. Proceed only when gate passes.

### Phase 3: PRESENT

**Goal**: Format events as a human-readable decision timeline.

**Step 1: Build the timeline**

Sort by `ts` (numeric — concurrent appends can interleave lines out of order). Convert `ts` to local ISO time for display; show raw `ts` on request. For each decision:

```
[TIME] {agent} + {skill} ({complexity})
  Request: "{request_snippet}"
  Health at decision: {health line — see below}
  Alternates: {alternates, or "none recorded"}
  Outcome: {outcome} ({reason})   — or "pending: not yet finalized"
```

Health line — three recorded states, rendered distinctly:

| Recorded | Render as |
|---|---|
| Numeric `health_at_decision` | `0.62 (n=7, failure=1) → action=keep` |
| `null` + `gate_inputs_present: true` | `no weight row at decision time (new pair)` |
| `null` + `gate_inputs_present` false/absent | `health gate not instrumented for this dispatch (legacy marker)` |

Group entries by session when the timeline spans more than one, to prevent wall-of-text.

**Step 2: Lead with the answer to the user's question**

If the user asked "why did I get routed here?", lead with the matching decision, then offer surrounding context:

```
You asked: "Why did I get the governance agent?"

Decision at [TIME]:
  Route: toolkit-governance-engineer + pr-workflow (Complex)
  Request: "ship the explanation-traces repoint as a green-CI PR..."
  Health at decision: no weight row at decision time (new pair)
  Alternates: none recorded
  Outcome: pending — not yet finalized

--- Session timeline (3 dispatches) ---
[... remaining entries ...]
```

**Step 3: Flag gaps honestly**

When entries lack additive fields or matched outcomes, say so explicitly:

```
Note: [N] decision(s) predate the health-gate instrumentation — they show
WHAT was routed but carry no health data. [M] decision(s) have no matched
outcome: pending or never finalized.
```

Incomplete data presented honestly beats complete-looking data that includes fabrication. Leave gaps as gaps.

**GATE**: Timeline presented. User's question answered from recorded events. Done.

---

## Examples

### Example 1: General session review
User says: "Show me the decision log"
```
skill: explanation-traces
```
Actions:
1. Locate route-events.jsonl (Phase 1)
2. Parse decisions and outcomes for the most recent session (Phase 2)
3. Present chronological timeline with joined outcomes (Phase 3)
Result: Session dispatch history — route, health at decision, outcome — per entry

### Example 2: Specific routing question
User says: "Why did I get routed to that agent?"
```
skill: explanation-traces "why that agent?"
```
Actions:
1. Locate route-events.jsonl (Phase 1)
2. Tail the decision events; filter to the latest dispatch in this session (Phase 2)
3. Lead with that decision — route, request snippet, health gate inputs, alternates — then the session timeline (Phase 3)
Result: Evidence-backed routing explanation from the recorded event, never post-hoc rationalization

### Example 3: Outcome investigation
User says: "Why was that dispatch marked a failure?"
```
skill: explanation-traces "failure outcome"
```
Actions:
1. Locate route-events.jsonl (Phase 1)
2. Filter to `outcome: failure` events; join each to its decision by session + key (Phase 2)
3. Present the outcome's `reason` (e.g. `tool-errors`, `rejection`) with the originating decision (Phase 3)
Result: The recorded failure cause, with the route and request that produced it

---

## Patterns to Detect and Fix

### Pattern 1: Evidence-Backed Trace Reading
**Wrong**: Reconstructing "why" from memory when the log is missing.
**Right**: If no log exists, say so, name the real path and producing hook, and stop. Never fabricate an explanation.

### Pattern 2: Distinguish the Three Health States
**Wrong**: Rendering every `null` health as "no data".
**Right**: `null` + `gate_inputs_present: true` = pick had no weight row (new pair). `null` + false/absent = legacy marker, health never read. Different facts; render them differently.

### Pattern 3: Join by Session and Key
**Wrong**: Pairing an outcome with "the decision right above it" in the file.
**Right**: Match on `session` + `key == "{agent}:{skill}"`. Interleaved sessions make file adjacency meaningless.

### Pattern 4: Absent Field Is Not Corruption
**Wrong**: Flagging pre-instrumentation lines as malformed because `gate_inputs_present` is missing.
**Right**: Fields were added over time; treat absence as "not recorded then" and say so.

### Pattern 5: Answer the Specific Question First
**Wrong**: Always dumping the full timeline regardless of what the user asked.
**Right**: Lead with the specific answer, then offer full context as supplementary detail.

---

## Error Handling

### Error: No Log File Found
**Cause**: No /do-routed dispatch recorded yet, hooks never synced to `~/.claude`, or `CLAUDE_LEARNING_DIR` points elsewhere.
**Solution**: Report the resolved path and the producing hook (`hooks/routing-decision-recorder.py`). Suggest `hooks/sync-to-user-claude.py` when hook changes were merged mid-session. Skip any reconstruction from conversation history.

### Error: Malformed JSONL Line
**Cause**: Truncated append (rare — per-line appends are atomic) or manual edit.
**Solution**: Skip the bad line, keep parsing the rest, and report the count and line numbers of skipped lines. JSONL fails per line, never whole-file.

### Error: Log Has No Decision Events
**Cause**: File exists but every line is an OUTCOME, or the recorder's marker parsing is failing.
**Solution**: Report counts by `type`. Point to `references/error-handling.md` for the recorder diagnosis steps.

### Error: User Asks About a Dispatch Not in the Log
**Cause**: The recorder only records /do-routed top-level dispatches — nested fan-out and manual Agent calls are deliberately excluded.
**Solution**: Show what IS recorded and explain the exclusion. Full mapping: `references/error-handling.md`.

---

## References

### Reference Loading Table

| Task type | Signals | Reference file |
|---|---|---|
| Reading or explaining event fields | "health_at_decision", "gate_inputs_present", "alternates", "key", "schema" | `references/trace-schema.md` |
| Diagnosing wrong or thin trace data | "health null", "no alternates", "legacy marker", "not instrumented" | `references/preferred-patterns.md` |
| Handling parse or read errors | "malformed", "missing field", "no decisions", "not found", "pending" | `references/error-handling.md` |
| Presenting filtered timeline | "why did you", "show trace", "decision log", "explain routing" | `references/trace-schema.md` |

### Reference Files
- `references/trace-schema.md`: Real event schema for route-events.jsonl — DECISION and OUTCOME fields, health states, join rules, examples
- `references/preferred-patterns.md`: Failure mode catalog for reading the log — join mistakes, health-state conflation, privacy — with detection commands
- `references/error-handling.md`: Error-fix mappings — missing log, malformed lines, no decisions, unmatched outcomes, unrecorded dispatches
