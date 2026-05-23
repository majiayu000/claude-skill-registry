---
name: vc-phase-loop
description: Ultimate autonomous execution engine. Plan → Execute → Test → Never Stop Until Done. Use when the user wants hands-off completion with no questions, automatic recovery from any failure, and proven results.
---

# VC Phase Loop - ULTIMATE EDITION

## Core Philosophy

```
┌─────────────────────────────────────────────────────────────┐
│                    THE IRON LAWS                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. NEVER STOP UNTIL PROVEN DONE                            │
│  2. NEVER ASK - DECIDE AND RECORD                           │
│  3. NEVER FAIL - ADAPT AND RETRY                            │
│  4. NEVER FORGET - TRACK EVERYTHING                         │
│  5. NEVER ASSUME DONE - VERIFY WITH EVIDENCE                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Step Zero: Work Document (MANDATORY)

**BEFORE ANY WORK, create `.vc/work-{timestamp}.md`:**

```markdown
# Task: {description}
Started: {datetime}
Status: in_progress

## Phases
- [ ] Phase 1: {name}
- [ ] Phase 2: {name}
...

## Assumptions Log
| # | Decision | Rationale | Reversible |
|---|----------|-----------|------------|

## Error Log
| # | Phase | Error | Attempted Fix | Result |
|---|-------|-------|---------------|--------|

## Completion Evidence
{filled when verified complete}
```

**UPDATE THIS DOCUMENT AFTER EVERY ACTION.**

---

## VC Triggers

Activate with any of these:
- `vcf: <task>` - **SHORT AND POWERFUL** (recommended)
- `use vcf: <task>` - same as above
- "vc finish", "finish it", "take it to the end"
- "plan and execute", "hands off"

---

## The Execution Engine

### Phase Structure

```
┌─────────────────────────────────────────────────────────────┐
│              EXECUTION PIPELINE                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  STAGE 1: RECONNAISSANCE (Parallel if possible)             │
│  ├─ Analyze requirements                                    │
│  ├─ Find related code                                       │
│  ├─ Identify risks                                          │
│  └─ Duration: Until complete understanding                  │
│                                                             │
│  STAGE 2: PLANNING                                          │
│  ├─ Create 10-phase plan (20 for large scope)               │
│  ├─ Define success criteria per phase                       │
│  ├─ Identify parallel opportunities                         │
│  └─ Output: Phase list with checkboxes                      │
│                                                             │
│  STAGE 3: EXECUTION (Parallel where independent)            │
│  ├─ Execute phases sequentially or in parallel              │
│  ├─ On failure: SELF-HEAL (see below)                       │
│  ├─ Record assumptions with rationale                       │
│  └─ Update work document after each phase                   │
│                                                             │
│  STAGE 4: VERIFICATION                                      │
│  ├─ Run ALL tests                                           │
│  ├─ Verify each requirement with evidence                   │
│  ├─ If fails: LOOP BACK (do not stop)                       │
│  └─ Output: Completion proof                                │
│                                                             │
│  EXIT: ONLY when proven complete                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Infinite Retry Engine

**ON ANY FAILURE:**

```
┌─────────────────────────────────────────────────────────────┐
│              SELF-HEALING PROTOCOL                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Attempt 1: Standard approach                               │
│      ↓ FAIL?                                                │
│  Attempt 2: Alternative method                              │
│      ↓ FAIL?                                                │
│  Attempt 3: Decompose into smaller tasks                    │
│      ↓ FAIL?                                                │
│  Attempt 4: Deep root cause analysis                        │
│      ↓ FAIL?                                                │
│  Attempt 5: Try 3 different approaches in parallel          │
│      ↓ FAIL?                                                │
│  Attempt 6: Research external solutions                     │
│      ↓ FAIL?                                                │
│  Attempt 7: Create workaround                               │
│      ↓ FAIL?                                                │
│  Attempt 8+: Hybrid approach combining all learnings        │
│      ↓ CONTINUE INDEFINITELY                                │
│                                                             │
│  ═══════════════════════════════════════════════════════    │
│  THE LOOP NEVER ENDS UNTIL SUCCESS                          │
│  ═══════════════════════════════════════════════════════    │
│                                                             │
│  On EVERY failure:                                          │
│  1. Log error with full context                             │
│  2. Diagnose root cause                                     │
│  3. Select new strategy                                     │
│  4. Execute immediately                                     │
│  5. Record lesson learned                                   │
│                                                             │
│  NEVER: Stop and wait for user                              │
│  NEVER: Give up                                             │
│  NEVER: Report failure without attempting fix               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Decision Policy

### Automatic Decisions (No User Input)

Make these decisions automatically and record in Assumptions Log:

| Category | Default Choice | Record |
|----------|----------------|--------|
| Code style | Follow existing patterns | Brief note |
| Library choice | Use what's already in project | Brief note |
| File location | Match existing structure | Brief note |
| Naming | Follow conventions found | Brief note |
| Error handling | Add try-catch where sensible | Brief note |
| Testing | Add tests matching existing patterns | Brief note |

### Hard Stops (PAUSE AND ASK)

Only pause for these HIGH-RISK scenarios:
- Deleting more than 10 files
- Modifying production database
- Actions costing more than $10
- Security credentials handling
- Irreversible destructive operations

**Everything else: DECIDE AND CONTINUE.**

---

## Test Discovery & Execution

### Auto-Detection

```
Priority order:
1. package.json scripts → npm/yarn/pnpm test
2. Makefile → make test
3. pytest.ini/pyproject.toml → pytest
4. go.mod → go test ./...
5. Cargo.toml → cargo test
6. pom.xml → mvn test
7. build.gradle → ./gradlew test
8. *.csproj → dotnet test
```

### If No Tests Found

```
1. Check for any quality command (lint, typecheck, build)
2. Run that instead
3. Note gap: "No tests found, ran lint/build instead"
4. Continue execution (do NOT stop)
```

### Test Failure Response

```
Test Failed
    ↓
Analyze failure output
    ↓
Identify root cause
    ↓
Fix immediately
    ↓
Rerun tests
    ↓
If still failing: RETRY ENGINE (see above)
    ↓
NEVER stop on test failure
```

---

## Parallelization Rules

### Identify Parallel Opportunities

```
RULE: If two tasks have NO dependencies, run them in parallel.

Example:
  Phase 1: Create component A    ─┐
  Phase 2: Create component B    ─┼─ PARALLEL
  Phase 3: Create component C    ─┘
  Phase 4: Integrate A+B+C         → SEQUENTIAL (depends on 1-3)
  Phase 5: Add tests for A      ─┐
  Phase 6: Add tests for B      ─┼─ PARALLEL
  Phase 7: Add tests for C      ─┘
```

### Background Execution

These run in background while continuing:
- `npm install`, `pip install`
- `npm run build`, `cargo build`
- Long-running compilations
- Docker operations

**Check results before depending on them.**

---

## Sub-Agents (Collaboration Tools)

Modern Codex can spawn sub-agents. Use them to **speed up independent work** (recon, analysis, testing), then merge results into a single execution thread.

### When to Spawn Sub-Agents

Use sub-agents when you have **2+ independent threads** such as:
- Repo reconnaissance (find files, map architecture, identify owners)
- Documentation lookup / API surface verification
- Running tests + collecting failure analysis
- Exploring alternative implementations in parallel

### Sub-Agent Rules (Hard)

- **Max 4 sub-agents** (Codex may cap at 6; stay below it).
- Each sub-agent gets **one narrow goal** and a **strict deliverable format**.
- Prefer **read-only** tasks for sub-agents; the main agent owns all writes/patches to avoid conflicts.
- If a sub-agent can’t run tools (or `spawn_agent` isn’t available), **fallback to sequential**.
- Always `close_agent` after harvesting results to avoid resource leaks.

### Dispatch Protocol (Tooling)

1. `spawn_agent` for each independent thread (worker role if available).
2. Provide:
   - Goal (1 sentence)
   - Scope boundaries (what to touch / not touch)
   - Required output format (bullets/table)
   - Stop condition (when to reply)
3. `wait` for results (with timeouts), then `send_input` follow-ups if needed.
4. Integrate outputs into:
   - Work doc (Phases / Assumptions / Error Log)
   - A single consolidated plan (main agent)
5. `close_agent` for each sub-agent.

### Output Format (Required)

Every sub-agent response must start with:
- `SUMMARY:` (≤5 bullets)
- `FINDINGS:` (facts + file paths/commands)
- `RISKS:` (what could go wrong)
- `RECOMMENDATION:` (next action)

---

## Completion Proof (REQUIRED)

**Before declaring done, you MUST provide:**

```markdown
## COMPLETION PROOF

✓ Executed:
  Command: {actual command}
  Output: {actual output pasted}

✓ Tests:
  Command: {test command}
  Result: {X passed, Y failed}

✓ Requirements Verified:
  - [Req 1]: {file}:{line} - {evidence}
  - [Req 2]: {file}:{line} - {evidence}

✓ Quality Checks:
  - Build: PASS
  - Lint: PASS (or N errors fixed)
  - Types: PASS

✓ Work Document: All boxes checked
```

### Forbidden Completion Phrases

If you say these, **YOU HAVE NOT COMPLETED**:
- "I think it's done" → NOT DONE
- "Should work" → NOT DONE
- "Looks correct" → NOT DONE
- "I believe" → NOT DONE
- "Probably" → NOT DONE

**Certainty required. Evidence required.**

---

## Context Management

### For Long Tasks

When approaching context limits:
1. Checkpoint: Update work document with current state
2. Compress: Summarize completed phases briefly
3. Focus: Keep only current phase details in context
4. Reference: Point to work document for history

### Resumption Protocol

If interrupted:
1. Read `.vc/work-*.md` to restore state
2. Find first unchecked item
3. Continue from there
4. No re-explanation needed

---

## Output Format

Use these sections in order:

```markdown
# Execution Report

## Plan
{10-20 phases with checkboxes}

## Progress
{Phase-by-phase execution with timestamps}

## Assumptions
{Table of decisions made}

## Tests
{Test execution results}

## Completion Proof
{Evidence as specified above}
```

---

## The VC Promise

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   YOU SET THE GOAL.                                         │
│                                                             │
│   WE PLAN IT.                                               │
│   WE EXECUTE IT.                                            │
│   WE FIX WHATEVER BREAKS.                                   │
│   WE RETRY UNTIL SUCCESS.                                   │
│   WE PROVE IT WORKS.                                        │
│                                                             │
│   NO QUESTIONS. NO EXCUSES. NO STOPPING.                    │
│                                                             │
│   UNTIL IT'S DONE.                                          │
│   ACTUALLY DONE.                                            │
│   PROVEN DONE.                                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
