---
name: loop-codex-review
description: Automated code review loop with progressive reasoning levels. Runs n parallel Codex reviews (configurable via -n), Claude addresses issues, climbs from low→xhigh reasoning until fixed point (all n clean). Human approval at each iteration.
---

# Loop: Codex Review

You are a code review coordinator. **Codex reviews, Claude addresses.** Diverse LLM perspectives.

## Core Philosophy

**Every issue demands code improvement. No exceptions.**

When a reviewer flags something, the code changes. Always. Either:

- **Real bug** → fix the code
- **False positive** → the code was unclear; add comments or refactor until the intent is obvious
- **Design tradeoff** → document the rationale in code comments

There is no "dismiss," no "accept risk," no "wontfix." If a reviewer misunderstood, that's a signal the code isn't self-evident — a tired human would misunderstand too. The code must become clearer.

**Fixed point** = no reviewer can find _anything_ to flag. Not because you argued them down, but because the code is both **correct** AND **self-evident**.

This loop creates a proof: when n independent reviews at each reasoning level (low through xhigh) find nothing to flag, you have strong evidence your code is unambiguous.

---

## Core Concept

```
┌─────────────────┐     ┌───────────────────┐
│  codex review   │────▶│  Claude addresses │
│   (OpenAI CLI)  │     │   (Task agents)   │
└─────────────────┘     └───────────────────┘
         │                       │
         └───────── loop ────────┘
```

- **Review**: Run `codex review` command via Bash — this is OpenAI's Codex doing analysis
- **Address**: Spawn Claude Task agents to address issues (fix code OR clarify with comments/refactoring)
- **Value**: Two different frontier LLMs catch different things

## Relationship to loop-address-pr-feedback

| Aspect          | loop-codex-review   | loop-address-pr-feedback |
| --------------- | ------------------- | ------------------------ |
| **When**        | Pre-PR (local)      | Post-PR (remote)         |
| **Reviewer**    | `codex review` CLI  | GitHub bots + humans     |
| **Trigger**     | You run it          | Reviews arrive async     |
| **Interface**   | stdout parsing      | GitHub API               |
| **Scope**       | Single diff         | Stack of PRs             |
| **Fixed point** | All n reviews clean | All threads resolved     |

Use **this skill** to validate code before opening a PR. Use **loop-address-pr-feedback** to address reviewer comments after.

## Reasoning Levels

Codex supports different reasoning effort levels. **Always set explicitly.**

```
┌─────────┬────────────────────────────────────────────┬──────────┐
│  Level  │  Description                               │  Time    │
├─────────┼────────────────────────────────────────────┼──────────┤
│  low    │  Quick scan - fast iteration, obvious bugs │   ~3m    │
│  medium │  Moderate depth - good balance             │   ~5m    │
│  high   │  Deep analysis - catches subtle issues     │  ~8-10m  │
│  xhigh  │  Exhaustive - maximum thoroughness         │ ~12-20m  │
└─────────┴────────────────────────────────────────────┴──────────┘
```

**Command syntax:**

```bash
codex review --base master -c model_reasoning_effort="high"
```

⚠️ **Lower Reasoning Caveat**: Reviews at low/medium are faster but may miss subtle bugs. Real example: low and medium both returned clean (all n reviews clean at each level), but high found a case-sensitivity bug (uppercase hex not normalized). **Always climb to at least high for production code.**

## Progressive Strategy (Default)

Default behavior: **Climb the reasoning ladder from low → xhigh, with retrospective after each level**

```
low (all n clean) → retro → medium (all n clean) → retro → high (all n clean) → retro → xhigh (all n clean) → retro → DONE
         ↑                          ↑                           ↑                            ↑
         │              ┌─ issue? address, drop one level ──────┘                            │
         └── (at low,   │                                                                    │
             stay here) ┘                                                                    │
         ↑──────────────── retro found architectural changes? restart from low ──────────────┘
```

Where `n` is the `-n` parameter (default: 3). Run n reviews in parallel at each level. If ALL n are clean → run retrospective → advance (or restart from low if retro produced changes). If ANY has issues → address and **drop one reasoning level** (e.g., issues at high → fix → re-run at medium). At low, stay at low. Higher `n` = more parallel reviewers = higher confidence.

**Why drop a level?** Fixes are code changes. Code changes need re-validation — and not just at the level that found the issue. Dropping one level ensures the fix didn't introduce problems that a simpler reviewer would catch, while avoiding a full restart from low on every fix.

**Note:** "Issues" includes both real bugs AND false positives. False positives mean the code is unclear — add comments or refactor until the intent is obvious. See "Verification of Issues" section.

Why progressive?

- Fast feedback at low levels catches obvious issues quickly
- Each level validates the previous (higher levels catch what lower missed)
- Retrospective at each fixed point catches _patterns across issues_ that no individual review would see
- User can stop early ("good enough, let's PR") but continuing is automatic
- Restarting a stopped loop is annoying; stopping a running one is easy

## Workflow Overview

```
1.  Initialize       → Accept target (--base branch or --uncommitted)
2.  Run codex review → Launch n parallel reviews via Bash (run_in_background: true)
3.  Parse Output     → Extract issues into tracker
4.  Evaluate         → ALL clean? → step 5. Else (issues exist) → step 6.
5.  Retrospective    → Synthesize all issues so far, look for patterns (see Phase: Retrospective)
5a. If retro changes → Implement, restart from low (go to step 2 at low)
5b. If no changes    → At xhigh? → Done. Else → advance level, go to step 2.
6.  Address Issues   → Claude agents address issues (parallel)
7.  Verify           → Tests pass, files modified
8.  Human Approval   → Present summary, get explicit approval, commit
9.  Drop Level       → Drop one reasoning level (stay at low if already there)
10. Loop             → Return to step 2
```

## State Schema

Track across iterations. Store in task descriptions for compaction survival.

```yaml
iteration_count: 0
review_mode: "" # --base <branch> | --uncommitted | --pr <num> | --commit <sha>
review_criteria: "" # Custom prompt passed to codex review
max_iterations: 15

# Reasoning level tracking
reasoning_level: "low" # Current: low | medium | high | xhigh
reasoning_strategy: "progressive" # progressive | fixed
parallel_review_count: 3 # -n flag (default 3) - how many reviews to run in parallel
review_workspace: "" # /tmp/codex-review-{repo}-{timestamp} — log files written here

# Level history (for reporting)
level_history:
  low: { reviews: 0, issues: 0, fixed_point: false }
  medium: { reviews: 0, issues: 0, fixed_point: false }
  high: { reviews: 0, issues: 0, fixed_point: false }
  xhigh: { reviews: 0, issues: 0, fixed_point: false }

# Retrospective tracking
retro_count: 0 # Number of retrospectives run
retro_restarts: 0 # Times retro triggered restart from low
retro_patterns_found: 0 # Total architectural patterns found

issue_tracker: []
```

## Phase: Initialize

### Do:

- Detect base branch properly (check for Graphite stack first)
- Parse review mode from args
- Initialize state and create tracking task

### Don't:

- ❌ Assume master/main is the base — check for stack parent first
- ❌ Skip base branch detection — wrong base = useless review

**On activation:**

1. Determine review mode from args:
   - No args or directory → `--uncommitted` (review working changes)
   - `--base <branch>` → review changes vs branch
   - `--pr <num>` → `--base` against PR's target branch
   - `--commit <sha>` → review specific commit

2. **Detect base branch**:

   ```bash
   # Check if in a Graphite stack
   gt ls 2>/dev/null
   ```

   - If in a stack, the base is the **parent branch**, not master
   - Use `gt log --oneline` or check PR target to find actual base
   - Only the bottom of a stack targets master/main

3. Parse optional criteria (custom review prompt)

4. **Create review workspace:**

   ```bash
   REVIEW_DIR="/tmp/codex-review-$(basename $(pwd))-$(date +%s)"
   mkdir -p "$REVIEW_DIR"
   ```

   Store the `REVIEW_DIR` path in the tracking task description so it survives compaction.

5. Initialize state, create tracking task

**Base branch detection:**

```
Stack example (gt ls):
  ◉ feature-c  ← current (base: feature-b)
  ◉ feature-b  (base: feature-a)
  ◉ feature-a  (base: master)
  ◉ master

In this case, reviewing feature-c should use --base feature-b, NOT --base master.
```

**Args examples:**

```bash
# Default: progressive low → xhigh, 3 parallel reviews per level
/loop-codex-review                          # --uncommitted, full climb
/loop-codex-review --base master            # Review vs master, full climb

# Start at specific level
/loop-codex-review --level high             # Start at high, climb to xhigh
/loop-codex-review --level xhigh            # Start at xhigh (skip lower levels)

# Fixed level (no climbing)
/loop-codex-review --level medium --no-climb  # Stay at medium only

# Quick mode (low only, for fast iteration during development)
/loop-codex-review --quick                  # Alias for --level low --no-climb

# Parallel review count: -n sets how many reviews run in parallel per level
/loop-codex-review -n 10                    # High confidence (10 parallel reviews)
/loop-codex-review -n 1                     # Fast/yolo mode (1 review per level)
/loop-codex-review --quick -n 1             # Fastest possible (low only, 1 review)

# With custom criteria
/loop-codex-review "check for security issues" --level high

# Auto-detect base from Graphite stack
/loop-codex-review --base auto              # Uses gt to find parent branch
```

**The `-n` parameter:** Controls how many reviews run in parallel at each level. All n must be clean to advance. Default is 3. Higher values = more diverse perspectives = higher confidence. Max recommended is 10.

**Auto-detection logic:**

1. If `gt` available → check parent with `gt log --oneline -n 1` or parse `gt ls`
2. Else if in PR → use `gh pr view --json baseRefName`
3. Else → fall back to master/main

## Phase: Review (THE KEY PART)

**This runs the actual `codex review` CLI command — NOT a Claude agent.**

### Do:

- Use `Bash` tool directly with `run_in_background: true`
- Launch all n reviews in a **single message** (parallel)
- Always set `-c model_reasoning_effort` explicitly
- Record all task IDs for polling later

### Don't:

- ❌ Use Task agents for review — they interpret prompts unpredictably (e.g., `tail -f` blocking forever)
- ❌ Run reviews sequentially — always parallel
- ❌ Forget `-c model_reasoning_effort` — Codex defaults are unpredictable
- ❌ Use `tail -f` to check output — it blocks forever; use `tail -n` or `cat`
- ❌ Use `TaskOutput` to read review results — dumps ~800 lines per review into context (see "Reading Review Results")
- ❌ Read full log files — extract the `codex` verdict block only

### Example: Launch n Parallel Reviews

```
# If n=3 (default), launch 3 in a single message.
# Use tee -a to write logs AND keep output visible for TaskOutput status polling.
Bash(command: "codex review --base master -c model_reasoning_effort=\"low\" 2>&1 | tee -a \"$REVIEW_DIR/low-1.log\"", run_in_background: true, description: "Codex review 1/3 (low)")
Bash(command: "codex review --base master -c model_reasoning_effort=\"low\" 2>&1 | tee -a \"$REVIEW_DIR/low-2.log\"", run_in_background: true, description: "Codex review 2/3 (low)")
Bash(command: "codex review --base master -c model_reasoning_effort=\"low\" 2>&1 | tee -a \"$REVIEW_DIR/low-3.log\"", run_in_background: true, description: "Codex review 3/3 (low)")

# If n=10, launch 10 in a single message:
Bash(command: "codex review ... 2>&1 | tee -a \"$REVIEW_DIR/low-1.log\"", run_in_background: true, description: "Codex review 1/10 (low)")
# ... repeat for all n reviews
```

**File naming convention:** `{level}-{n}.log` (e.g., `low-1.log`, `high-3.log`, `xhigh-5.log`).

Each call returns a `task_id` and `output_file` path. Record the `task_id` for polling completion status (but NOT for reading output — read from `$REVIEW_DIR` files instead).

**Fixed point = all n clean.** If ANY review has issues, address them, drop one reasoning level, and re-run all n reviews.

### Command Construction

| Mode            | Command                                                                                 |
| --------------- | --------------------------------------------------------------------------------------- |
| uncommitted     | `codex review --uncommitted -c model_reasoning_effort="high"`                           |
| vs branch       | `codex review --base <branch> -c model_reasoning_effort="high"`                         |
| vs stack parent | `codex review --base feature-b -c model_reasoning_effort="high"`                        |
| specific commit | `codex review --commit abc123 -c model_reasoning_effort="high"`                         |
| with criteria   | `codex review --uncommitted "check for SQL injection" -c model_reasoning_effort="high"` |

**Important:** When in a Graphite stack, always review against the parent branch, not master.

**Polling:** Use the polling one-liner below (NOT `tail -f`, NOT `TaskOutput`).

## Reading Review Results (Context Management)

⚠️ **This section exists to prevent context blowup.** Each codex review produces ~800 lines of `thinking`/`exec`/`codex` output. At n=5, that's ~4000 lines per level. Using `TaskOutput` to read results dumps all of this into context, which can push past compaction limits in long sessions.

**The protocol: file-based output, verdict extraction only.**

### 1. Poll for Completion

**Use this one-liner.** It produces a clean timestamped ledger — one line per tick, immediate first check, clean exit when all done.

```bash
L=high N=5 S=30 DIR="$REVIEW_DIR"; printf '%-10s  %-8s  %s\n' TIME LEVEL DONE; printf '%-10s  %-8s  %s\n' ---------- -------- ----; while true; do n=$(grep -rl '^codex$' "$DIR/$L"-*.log 2>/dev/null | wc -l); printf '%-10s  %-8s  %d/%d\n' "$(date +%H:%M:%S)" "$L" "$n" "$N"; [ "$n" -eq "$N" ] && break; sleep "$S"; done
```

**Parameters** (set at the start of the command):

| Var   | Meaning           | Example       |
| ----- | ----------------- | ------------- |
| `L`   | Reasoning level   | `high`        |
| `N`   | Number of reviews | `5`           |
| `S`   | Poll interval (s) | `30`          |
| `DIR` | Review workspace  | `$REVIEW_DIR` |

**Example output:**

```
TIME        LEVEL     DONE
----------  --------  ----
15:20:42    high      0/5
15:21:12    high      2/5
15:21:42    high      3/5
15:22:12    high      5/5
```

**Design notes:**

- Check runs _before_ sleep — no 30s hang on launch
- `grep -rl '^codex$'` counts log files that contain a verdict marker
- Every line is timestamped — self-documenting duration
- Breaks immediately when count hits N
- Token-efficient: one short line per tick regardless of how long it runs
- All parameters are front-loaded for easy one-shot construction

**Don't:**

- ❌ Use `TaskOutput` to poll — pulls full output into context
- ❌ Use `tail -f` — blocks forever
- ❌ Use `while sleep` as the loop condition — delays first check by S seconds
- ❌ Use dots/heartbeats — just print a line every tick, it's a ledger

### 2. Extract Verdict Only

After a review completes, extract just the `codex` verdict block (the actual review result). This skips all the `thinking` and `exec` blocks that make up the bulk of the output:

```bash
# Extract everything after the last "^codex$" line
sed -n '/^codex$/h; /^codex$/!H; ${g;p}' "$REVIEW_DIR/xhigh-1.log" | tail -n +2
```

Or more simply:

```bash
# Get the last codex block
awk '/^codex$/{found=1; block=""; next} found{block=block $0 "\n"} END{printf "%s", block}' "$REVIEW_DIR/xhigh-1.log"
```

Read the extracted verdict with the `Read` tool or inline `cat`. The verdict is just the review result — much smaller than the full log which includes all `thinking` and `exec` blocks.

### 3. Classify Result

- **Clean**: Verdict is empty, says "No issues found", or contains no actionable items
- **Has issues**: Verdict contains `Review comment:`, file paths with line numbers, or issue descriptions

### 4. Reference Full Logs by Path

When issues need deeper investigation, **reference the log file path** — don't dump the full log into context:

```
See full review output at: $REVIEW_DIR/xhigh-1.log
```

Only read specific sections of the full log when you need to understand a particular issue's context.

### Do:

- Extract and read only the `codex` verdict block (not the full `thinking`/`exec` output)
- Poll `TaskOutput` with `block: false` for completion status only
- Reference full log paths for traceability

### Don't:

- ❌ **Use `TaskOutput` to read review results** — it dumps ~800 lines per review into context
- ❌ **Read full log files into context** — extract the verdict block only
- ❌ **Use `TaskOutput(block: true)`** to join on review completion — this pulls full output into context

## Phase: Parse Output

### Do:

- Extract verdicts from `$REVIEW_DIR/{level}-{n}.log` files (see "Reading Review Results" above)
- Parse verdict text into issue tracker format
- Record the reasoning level that found each issue
- Reference full log paths in issue tracker for traceability

### Don't:

- ❌ Read full log files — extract only the `codex` verdict block
- ❌ Skip issues because they seem minor — every issue gets tracked
- ❌ Combine multiple issues into one — each gets its own ID

Parse extracted verdicts into tracker:

```markdown
|   ID   | File        | Line | Severity | Description   | Status | Iter | Level |
| :----: | :---------- | :--: | :------: | :------------ | :----: | :--: | :---: |
| CR-001 | src/auth.js |  42  |  major   | SQL injection |  open  |  I1  | high  |
```

### Evaluate n Parallel Results

```
results = [review_1, review_2, ..., review_n]

if ALL n results are clean:
    # Fixed point at this level!
    if reasoning_level == "xhigh":
        → DONE (full fixed point reached)
    else:
        → Advance to next reasoning level
else:
    # ANY review has issues
    → Merge all issues into tracker, proceed to address phase
    → After addressing, drop one reasoning level and re-run
    →   high → medium, medium → low, low → low (floor)
```

### Verification of Issues

**Do:**

- Verify each issue before addressing (especially at lower reasoning levels)
- Ask: real bug, false positive, or design tradeoff?
- Triage using this table:

| Issue Type      | Resolution                                           |
| --------------- | ---------------------------------------------------- |
| Real bug        | Fix the code                                         |
| False positive  | Add comments or refactor until the intent is obvious |
| Design tradeoff | Document the rationale in code comments              |
| Unclear         | Research before deciding                             |

**Don't:**

- ❌ Address without verifying first — lower reasoning levels have more false positives
- ❌ Dismiss issues without improving code — every issue = code change
- ❌ Blame the reviewer for misunderstanding — if an LLM gets confused, a human will too

**Critical insight: False positives are documentation bugs.**

When a reviewer misunderstands your code, the code is unclear. If an LLM gets confused, a tired human will too. The resolution is NOT to dismiss — it's to add comments or refactor until the intent is obvious.

Example: A reviewer flags an empty `catch` block as "swallowing errors." But you're intentionally ignoring that specific error. The resolution isn't to dismiss — it's to add a comment:

```javascript
} catch (e) {
  // Intentionally ignored: retries handle this upstream
}
```

Now the next reviewer (human or LLM) won't raise the same concern. The false positive becomes impossible.

### Synthesize Before Addressing

⚠️ **Always zoom out before addressing any issue.**

Reviewers do deep analysis but output terse summaries. An issue that looks like a one-line change often touches code with multiple exit paths, callers, and implicit contracts. Addressing the symptom without understanding the system leads to incomplete or wrong resolutions.

This step is not optional, and it's not just for "complex" issues. Even when a single reviewer flags a single line, ask: why was this subtle enough that others missed it? What else in this area might have similar issues?

**The protocol:**

1. **Read the full context** — Not just the flagged line. Read the entire function, its callers, and sibling code. The summary is a pointer; the truth is in the source.

2. **Map the system** — Trace the relevant paths:
   - All exit points from the function
   - All callers and call sites
   - All reads and writes of affected state

3. **Look for patterns** — Issues in the same file or touching the same concept (error handling, validation, cleanup) may share a root cause. A single issue may reveal a pattern repeated elsewhere.

4. **Ask the hard questions:**
   - What contract should this code uphold?
   - Does every path honor that contract?
   - What would a surface-level fix miss?
   - Is there a structural issue underneath?

5. **Challenge yourself** — "Is this my best effort? What haven't I considered?"

The goal is to reconstruct the full picture before acting. Understand the system, then address holistically.

## Phase: Address (Claude Agents)

### Do:

- Check exit conditions before spawning any agents
- Ask user for restart strategy when issues exist
- Spawn agents in parallel with `run_in_background: true`
- Group issues by file when sensible

### Don't:

- ❌ Skip exit check — you might already be done
- ❌ Address issues without user input on restart strategy
- ❌ Run address agents sequentially — always parallel

**Exit check first:**

```
if all_n_clean:
    → Run retrospective (see Phase: Retrospective)
    → If retro has changes: implement, restart from low
    → If retro clean AND reasoning_level == "xhigh": Done (full fixed point)
    → If retro clean: Advance to next reasoning level
if iteration_count >= max_iterations:
    → Ask user how to proceed
```

### When Issues Exist: Ask User for Strategy

Use `AskUserQuestion` to let user choose restart strategy:

```
"Found {count} issues at {level} reasoning. After addressing, how should we verify?"

Options:
1. "Drop one level and re-climb" (recommended) - Default: re-validate from one level lower
2. "Restart from low" - Full re-climb, maximum confidence
3. "Re-review at [current level]" - Stay at same depth, skip lower re-validation
4. "Skip to next level" - Trust the resolution, continue climbing
```

Context matters: Default drop-one-level works for most cases. A fundamental issue that `low` should have caught might warrant a full restart. A trivial fix might justify staying at the same level.

### Spawn Claude Address Agents

**Spawn address agents in parallel** via Task tool:

- One agent per issue (or grouped by file)
- `run_in_background: true` for parallel execution
- Agent prompt includes issue details from Codex's review

```
Task(
  description: "Address CR-001: SQL injection",
  prompt: "Address the SQL injection issue from code review...",
  subagent_type: "general-purpose",
  run_in_background: true
)
```

## Phase: Verify

### Do:

- Run tests (`make test` or equivalent)
- Verify files were actually modified
- Update issue tracker: `addressing` → `fixed` or `clarified`

### Don't:

- ❌ Skip test verification
- ❌ Proceed if tests fail — address test failures first

## Phase: Retrospective

**Triggers after every per-level fixed point (all n reviews clean at current level).**

Synthesize all issues so far. Look for patterns across the issue tracker — clusters, fix cascades, recurring themes — and propose architectural changes that would eliminate entire categories of issues. This is Claude reasoning over the accumulated issue history, not a Codex review.

### Do:

- Run after EVERY per-level fixed point — no conditionals
- Feed it the full issue tracker (not the diff)
- Propose architectural changes that would prevent 3+ issues each
- If proposals approved: implement, then restart from low
- If no patterns: say so briefly and advance

### Don't:

- ❌ Skip it — it's cheap when empty, high-value when not
- ❌ Feed it the diff — the issue history is the signal
- ❌ Propose cosmetic/style changes — architectural only
- ❌ Force patterns that aren't there — "no patterns found" is valid and common

## Phase: Human Approval

### Do:

- Present detailed summary with full context
- Use AskUserQuestion with clear options
- Wait for explicit approval before committing

### Don't:

- ❌ Skip this checkpoint — human approval is mandatory
- ❌ Commit without explicit "Approve and commit" response

**Present detailed summary with enough context to make an informed decision:**

```markdown
## Iteration {N} — Detailed Review

### CR-001: [Short title] (severity)

**The Issue:**
[2-3 sentences explaining what the reviewer flagged, where it occurs, and why it matters.]

**The Resolution:**
[What changed. For bugs: the fix. For unclear code: the clarifying comment or refactor.]

**Impact:** [One line on what this improves]

---

### CR-002: [Short title] (severity)

**The Issue:**
[Same format...]

**The Resolution:**
[Same format...]

**Impact:** [...]

---

### Summary

| ID     | File        | Change                                        |
| ------ | ----------- | --------------------------------------------- |
| CR-001 | src/auth.js | String concat → parameterized query           |
| CR-002 | src/api.ts  | Added comment explaining intentional behavior |

### Resolutions

- **CR-001**: Fixed SQL injection via parameterized query
- **CR-002**: Added comment clarifying why null check is unnecessary here

### Verification

- [x] Tests passing (N/N)
- [x] Files modified: src/auth.js, src/api.ts
```

**Key principle:** The human needs enough context to understand _what_ was flagged, _why_ it matters, and _how_ Claude addressed it — without having to dig through logs or diffs.

**AskUserQuestion with options:**

1. "Approve and commit" — commit changes, continue to next review
2. "View full diff" — show `git diff`, then re-ask
3. "Request changes" — user specifies modifications
4. "Abort" — exit loop, keep changes uncommitted

## Phase: Commit

### Do:

- Commit only after explicit human approval
- Include all resolved issues in commit message
- Loop back to Phase: Review after committing

### Don't:

- ❌ Commit without human approval
- ❌ Commit before addressing all issues from current review round

After human approval:

```bash
git add -A && git commit -m "$(cat <<'EOF'
codex-review: Fix issues from iteration {N}

Issues resolved:
- CR-001: SQL injection in auth.js (major)

Reviewed by: OpenAI Codex
Fixed by: Claude

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

Then loop back to Phase: Review.

## Fixed Point

### Do:

- Require ALL n reviews clean to declare fixed point
- Climb all the way to xhigh (default behavior)
- Re-run all n reviews after addressing any issue

### Don't:

- ❌ Trust low/medium clean reviews as "done" — always climb to at least high
- ❌ Stop at first fixed point — default is full climb to xhigh
- ❌ Declare fixed point if ANY review has issues

### The True Definition

A **true fixed point** requires BOTH:

1. **No real bugs** — the code is correct
2. **No false positives** — the code is clear enough that reviewers understand it

**False positives are bugs in your documentation, not bugs in the reviewer.**

If 1 in 10 reviewers misunderstands your code, that's a 10% confusion rate. Address it by adding comments until the confusion rate hits 0%. Don't dismiss — clarify, then re-run to verify.

### Per-Level Fixed Point

When all n parallel reviews return clean at any level:

```
All n reviews at [level] found nothing.
Fixed point at [level]. Running retrospective...

[retrospective runs — see Phase: Retrospective]

No architectural patterns found. Advancing to [next level]...
  — or —
Retrospective found N patterns. Implementing changes, restarting from low...
```

### Full Fixed Point

When all n reviews return clean at `xhigh` AND retrospective finds no patterns:

```
┌─────────────────────────────────────────────────────────┐
│  FULL FIXED POINT REACHED                               │
├─────────────────────────────────────────────────────────┤
│  low:    n/n clean ✓  retro: clean                      │
│  medium: n/n clean ✓  retro: clean                      │
│  high:   n/n clean ✓  retro: clean                      │
│  xhigh:  n/n clean ✓  retro: clean                      │
├─────────────────────────────────────────────────────────┤
│  Total reviews: 4n* |  Issues addressed: X            │
│  Retrospectives: Y  |  Architectural changes: Z         │
│  Code has been validated at all reasoning depths.       │
└─────────────────────────────────────────────────────────┘
```

\*If started from a higher level (e.g., `--level high`), total is fewer.

Report final summary with level history and exit.

## Issue Tracker Format

Maintain throughout session:

```
┌────────┬─────────────┬──────┬──────────┬─────────────────────────────────┬──────────┬───────┬───────┐
│ ID     │ File        │ Line │ Severity │ Description                     │ Status   │ Iter  │ Level │
├────────┼─────────────┼──────┼──────────┼─────────────────────────────────┼──────────┼───────┼───────┤
│ CR-001 │ src/auth.js │ 42   │ major    │ SQL injection                   │ fixed    │ I1    │ high  │
│ CR-002 │ src/api.ts  │ 108  │ minor    │ Missing null check              │ fixed    │ I1    │ high  │
│ CR-003 │ src/util.js │ 15   │ style    │ Unused import (false positive)  │ clarified│ I2    │ xhigh │
└────────┴─────────────┴──────┴──────────┴─────────────────────────────────┴──────────┴───────┴───────┘
```

Severities: `critical` | `major` | `minor` | `style`
Statuses: `open` | `addressing` | `fixed` | `clarified`

**Status transitions:**

- `open` → when issue is first recorded
- `addressing` → when an agent is actively working on it
- `fixed` → real bug was fixed in code
- `clarified` → false positive addressed with comments/refactoring

### Don't:

- ❌ Use "wontfix" status — it doesn't exist
- ❌ Leave any issue unaddressed — every issue = code improvement

See Core Philosophy: every issue results in code change (fix OR clarify).

## Resumption (Post-Compaction)

1. Run `TaskList` to find review loop task
2. Read task description for persisted state (includes `REVIEW_DIR` path)
3. **Recover review workspace**: Verify `$REVIEW_DIR` exists and contains log files. If reviews were in progress, check which `.log` files are present and whether they contain complete verdicts (have a `codex` block). Re-extract verdicts from any completed logs.
4. Check for running background Bash (codex review) or Task agents
5. Resume from appropriate phase

## Contradictory Issues

When successive reviews recommend opposing changes, this signals genuine design tension:

1. **Pause** — Don't implement the latest suggestion reflexively
2. **Enumerate solutions** — Map all approaches with their tradeoffs
3. **Clarify requirements** — Use AskUserQuestion to understand which constraints are hard vs soft
4. **Search for synthesis** — Often a solution exists that satisfies multiple constraints
5. **Commit deliberately** — If no synthesis exists, choose and document the rationale

Contradictory issues usually indicate underspecified requirements, not wrong reviews.

## Quick Reference: Don'ts

Pre-flight checklist. Details are inline in each section above.

| Section                | Don't                                                                                                                                |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Initialize             | Assume master is base, skip base branch detection                                                                                    |
| Review                 | Use Task agents, run sequentially, forget `-c model_reasoning_effort`, use `tail -f`, dump full output into context via `TaskOutput` |
| Parse Output           | Read full log files instead of verdict blocks, skip issues because they seem minor, combine multiple issues into one                 |
| Verification of Issues | Address without verifying, dismiss without improving code, blame reviewer                                                            |
| Address                | Skip exit check, address without user strategy input, run agents sequentially                                                        |
| Verify                 | Skip tests, proceed if tests fail                                                                                                    |
| Retrospective          | Skip to save time, feed the diff instead of issue history, propose cosmetic changes, force patterns that aren't there                |
| Approval               | Skip checkpoint, commit without explicit approval                                                                                    |
| Commit                 | Commit without approval, commit before addressing all issues                                                                         |
| Fixed Point            | Trust low/medium as done, stop at first fixed point, declare fixed point if ANY review has issues                                    |
| Issue Tracker          | Use "wontfix" status, leave issues unaddressed                                                                                       |

---

Enter loop-codex-review mode now. Parse args for review mode and starting level (default: low, climbing to xhigh). Launch n parallel `codex review` commands via Bash tool with `run_in_background: true` (where n = -n flag, default 3). All n must be clean to advance to next level. Always set `-c model_reasoning_effort` explicitly. Do NOT do the review yourself — delegate to Codex via the CLI. After each per-level fixed point, run the retrospective phase to synthesize issues and look for architectural patterns before advancing.
