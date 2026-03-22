---
name: review-static-history
description: Mine git history for bug patterns that static analysis could have caught
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Mine git history for bugs that shipped and were later fixed, to find patterns a static analysis check could have prevented. This is evidence-driven — only propose checks backed by real bug occurrences.

## Methodology

### Step 1 — Gather evidence

Review the last 50 commits (or more if the repo is active) for fix commits. Look for:
- Commit messages containing "fix", "bug", "crash", "revert", "missing", "forgot", "wrong"
- Diffs that add a `global` declaration, add `Critical "Off"`, fix a DllCall signature, correct a variable name, etc.

For each fix commit, categorize the root cause:
- What class of bug was it? (missing declaration, wrong type, unguarded state, resource leak, etc.)
- Could a regex or source parser have detected it before the commit?
- Is the pattern already caught by an existing check?

### Step 2 — Tally patterns

Group fix commits by root cause class. Use occurrence count as a signal, not a hard gate:

- **3+ occurrences** → strong signal, propose with confidence
- **1–2 occurrences** → still valid if the check is cheap (fits in a batch, simple regex) AND the bug was painful (silent corruption, shipped to users, caused a long debugging session)
- **0 occurrences but obvious risk** → note as speculative, lower priority

### Step 3 — Filter against existing checks

Cross-reference each pattern against the current pre-gate inventory:

**Already caught** (validate these are working):
- Missing `global` declaration → `check_batch_simple_b.ps1` (switch_global sub-check) + `query_global_ownership.ps1 -Check`
- Cross-file private function calls → `query_function_visibility.ps1 -Check`
- Ownership violations → `query_global_ownership.ps1 -Check`

If a pattern IS already caught but the bug still shipped, that's a different problem — the check may have a gap or the developer bypassed pre-gate. Flag it.

### Step 4 — Propose checks

For surviving patterns (not already caught, statically detectable):

**Feasibility test for each**:
- Write the detection regex/logic sketch
- Run it mentally against the current codebase — what would it flag?
- Estimate false positive rate (>20% false positives = not worth it)
- Estimate maintenance cost (will this break when code is refactored?)
- For low-occurrence patterns: is the check cheap enough (batch sub-check, simple regex) to justify the low frequency?

**Hard limit: propose at most 2 new checkers.** Keep the plan focused on the highest-value patterns.

## Placement Guidance

For each proposed check, specify placement:
- **Existing batch** — if short and fits theme (e.g., a simple pattern check → `check_batch_simple.ps1`)
- **New standalone** — if complex or needs specialized parsing
- See `review-static-speed` for batch architecture context if needed

## Plan Format

**Section 1 — Evidence table** (all fix commits analyzed):

| Commit | Message | Root Cause Class | Already Caught? |
|--------|---------|-----------------|----------------|
| `abc1234` | Fix missing global in foo | Missing declaration | Yes — check_batch_simple |
| `def5678` | Fix Critical not released on early return | Unmatched Critical | No |

**Section 2 — Pattern frequency**:

| Pattern | Occurrences | Commits | Already Caught? | Severity |
|---------|-------------|---------|----------------|----------|
| Unmatched `Critical "Off"` | 4 | abc, def, ghi, jkl | No | Silent corruption |

**Section 3 — Proposed checks** (max 2, highest-value patterns):

| Pattern | Detection Sketch | False Positive Est. | Placement | Evidence |
|---------|-----------------|--------------------|-----------|---------|
| Unmatched Critical | Track `Critical "On"` → scan for `return`/`continue` without prior `Critical "Off"` | Low — structural | `check_batch_guards.ps1` | 4 bugs in last 50 commits |

Ignore any existing plans — create a fresh one.
