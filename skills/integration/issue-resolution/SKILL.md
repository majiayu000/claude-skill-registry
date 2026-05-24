---
name: issue-resolution
description: Systematically diagnose and fix bugs through triage, reproduction, root cause analysis, and verified fixes. Use when resolving bugs, errors, failing tests, or investigating unexpected behavior.
---

# Issue Resolution Pipeline

Systematically resolve issues through iterative diagnosis and verified fixes.

## Pipeline Overview

```
INPUT → Triage → Reproduction → Root Cause Analysis → Impact → Fix → Verify
              ◄──────────────►◄────────────────────►
                    (Iterative loops allowed)
```

| Phase                  | Purpose                            | Output              |
| ---------------------- | ---------------------------------- | ------------------- |
| 0. Triage              | Normalize input, classify severity | Issue Brief         |
| 1. Reproduction        | Prove the bug, trace code path     | Repro Report + Test |
| 2. Root Cause Analysis | Find WHY, not just WHERE           | RCA Report          |
| 3. Impact Assessment   | Blast radius, regression risk      | Impact Report       |
| 4. Fix Decomposition   | Break into beads                   | .beads/\*.md        |
| 5. Verification        | Prove fix works, no regressions    | Passing tests       |

## Phase 0: Triage

Normalize different input types to a structured Issue Brief.

### Input Types

| Type                  | Triage Strategy                       |
| --------------------- | ------------------------------------- |
| **Vague report**      | Clarify → Explore → Reproduce         |
| **Error/Stack trace** | Parse trace → Locate code → Reproduce |
| **Failing test**      | Run test → Extract assertion → Trace  |

### Vague Report Triage

```
User: "Login is broken"
         │
         ▼
Ask clarification questions:
• What error do you see?
• When did it start working / stop working?
• What steps trigger it?
• Specific user/browser/environment?
         │
         ▼ (if user can't clarify)
Explore:
• mcp__gkg__search_codebase_definitions: Find auth/login related code
• git log: Recent changes in area
• Check logs if available
```

### Error/Stack Trace Triage

```
Parse the stack trace:
• Extract file:line locations
• mcp__gkg__get_definition on functions in trace
• Read surrounding context
         │
         ▼
Identify reproduction conditions:
• What input caused this?
• Can we write a test?
```

### Failing Test Triage

```
Run test in isolation:
• bun test <file> --filter "<test name>"
• Read test file for setup/assertions
• Check git log: was it passing before?
         │
         ▼
Trace implementation:
• What code does test exercise?
• mcp__gkg__get_references on tested function
• Recent changes to implementation?
```

### Severity Classification

Determines reproduction requirements:

| Severity                            | Reproduction Required  |
| ----------------------------------- | ---------------------- |
| **CRITICAL** (production, security) | Failing test REQUIRED  |
| **REGRESSION** (was working)        | Failing test REQUIRED  |
| **RACE CONDITION** (timing)         | Failing test REQUIRED  |
| **LOGIC BUG**                       | Failing test PREFERRED |
| **UI/VISUAL**                       | Manual + screenshot OK |
| **PERFORMANCE**                     | Benchmark/profile OK   |
| **QUICK FIX** (obvious cause)       | Manual repro OK        |

### Issue Brief Template

Save to `history/issues/<id>/brief.md`:

```markdown
# Issue Brief: <Short Title>

**Severity**: CRITICAL / HIGH / MEDIUM / LOW
**Type**: Regression / Edge case / Race condition / UI / Performance / Other
**Repro Required**: Failing test / Manual OK

## Symptom

<What is happening>

## Expected Behavior

<What should happen>

## Reproduction

<Steps, test command, or code path>

## Evidence

<Error message, stack trace, test output>

## Affected Area

<Files, modules, features involved>

## Timeline

<When started, recent changes if known>
```

## Phase 1: Reproduction

Prove the bug exists and trace the code path.

### If Failing Test Required

```bash
# Create test file
# packages/<area>/src/__tests__/<feature>.regression.test.ts

# Test should:
# 1. Set up conditions that trigger bug
# 2. Assert expected behavior (currently fails)
# 3. Be deterministic
```

### Reproduction Checklist

- [ ] Bug is reproducible on demand
- [ ] Exact error/behavior captured
- [ ] Minimal reproduction (simplest case that fails)
- [ ] Code path identified (stack trace or tracing)

### Code Path Tracing

```
mcp__gkg__get_definition     → Find where error originates
mcp__gkg__get_references     → Find callers
git blame <file>       → Who changed it, when
git log -p <file>      → What changed recently
```

### Repro Report Template

Save to `history/issues/<id>/repro.md`:

```markdown
# Reproduction Report: <Issue Title>

## Reproduction Method

☐ Failing test: `<test file and name>`
☐ Manual: <steps>

## Error/Behavior Captured

<Exact error message, stack trace>

## Code Path

1. Entry: `<file>:<line>` - <function>
2. Calls: `<file>:<line>` - <function>
3. Fails at: `<file>:<line>` - <reason>

## Recent Changes (if relevant)

- <commit>: <summary>
```

## Phase 2: Root Cause Analysis

Find WHY the bug happens, not just WHERE.

### RCA Framework

```
STEP 1: Generate hypotheses (3-5)
         │
         ▼
STEP 2: Gather evidence for/against each
         │
         ▼
STEP 3: Eliminate hypotheses
         │
         ▼
STEP 4: Confirm root cause
```

### Bug Type → RCA Strategy

| Bug Type            | Strategy                  | Key Tools                       |
| ------------------- | ------------------------- | ------------------------------- |
| **Regression**      | Find breaking change      | `git bisect`, `git blame`       |
| **Edge case**       | Analyze boundary inputs   | Type inspection, boundary tests |
| **Race condition**  | Trace async flow          | Timing logs, async analysis     |
| **Data corruption** | Trace state changes       | Data flow analysis              |
| **External dep**    | Check version/API changes | Changelogs, API docs            |

### Oracle for RCA

**Hypothesis Generation:**

```
oracle(
  task: "Generate root cause hypotheses",
  context: """
    Symptom: <error>
    Code path: <trace>
    Recent changes: <git log>

    Generate 3-5 hypotheses ranked by likelihood.
    For each, what evidence would support/refute it?
  """,
  files: ["<affected files>"]
)
```

**Hypothesis Validation:**

```
oracle(
  task: "Validate root cause hypothesis",
  context: """
    Hypothesis: <proposed cause>
    Evidence: <gathered evidence>

    1. Does evidence support or refute?
    2. Explain causal chain: cause → symptom
    3. What would confirm this?
  """,
  files: ["<relevant files>"]
)
```

### Iteration: RCA → Reproduction Loop

If hypothesis needs more evidence:

```
IN RCA: "Need timing logs to confirm race condition"
    │
    ▼
BACK TO REPRO:
• Add instrumentation
• Run with specific conditions
• Capture new evidence
    │
    ▼
RETURN TO RCA with new evidence
```

### RCA Report Template

Save to `history/issues/<id>/rca.md`:

```markdown
# Root Cause Analysis: <Issue Title>

## Iteration: <N>

## Hypotheses Considered

### Hypothesis A: <Description>

- **Likelihood**: HIGH / MEDIUM / LOW
- **Supporting evidence**: ...
- **Refuting evidence**: ...
- **Verdict**: ✓ CONFIRMED / ✗ ELIMINATED

### Hypothesis B: ...

## Root Cause (Confirmed)

**Cause**: <Clear statement>

**Causal chain**:

1. <Step> leads to
2. <Step> leads to
3. <Symptom>

## Why This Happened

<Underlying reason - missing validation, wrong assumption, etc.>

## Fix Approach

**Immediate**: <What to change>
**Preventive**: <How to prevent similar bugs>
```

## Phase 3: Impact Assessment

Before fixing, understand blast radius.

### Impact Analysis

```
mcp__gkg__get_references <affected function>
    → Who else calls this?

Grep for related patterns
    → Similar code that might have same bug?

Review test coverage
    → What tests cover this area?
```

### Regression Risk

| Factor              | Risk Level |
| ------------------- | ---------- |
| High usage function | HIGH       |
| Shared utility      | HIGH       |
| Public API change   | HIGH       |
| Internal helper     | LOW        |
| Isolated module     | LOW        |

### Spike for Complex Fixes

If fix approach is uncertain:

```bash
bd create "Spike: Validate fix approach for <issue>" -t task -p 0
```

Execute via MULTI_AGENT_WORKFLOW, write to `.spikes/<issue-id>/`.

### Impact Report Template

Save to `history/issues/<id>/impact.md`:

```markdown
# Impact Assessment: <Issue Title>

## Blast Radius

### Direct Impact

- <File/function directly changed>

### Callers Affected

- <List from mcp__gkg__get_references>

### Related Code

- <Similar patterns that may need same fix>

## Regression Risk

**Level**: HIGH / MEDIUM / LOW
**Reason**: <Why this risk level>

## Test Coverage

- Existing tests: <list>
- Tests to add: <list>

## Fix Validation

☐ Spike completed (if needed): `.spikes/<id>/`
☐ Fix approach validated
```

## Phase 4: Fix Decomposition

Break fix into beads.

### Simple Fix (Single Bead)

```bash
bd create "Fix: <issue title>" -t bug -p <priority>
```

Bead includes:

- Root cause reference
- Fix implementation
- Test (failing → passing)
- Docs update (if behavior change)

### Complex Fix (Multiple Beads)

```bash
bd create "Epic: Fix <issue>" -t epic -p <priority>
bd create "Add regression test for <issue>" -t task --blocks <epic>
bd create "Fix <component A>" -t bug --blocks <epic> --deps <test>
bd create "Fix <component B>" -t bug --blocks <epic> --deps <test>
bd create "Update docs for <behavior change>" -t task --blocks <epic> --deps <fix-a>,<fix-b>
```

### Fix Bead Template

```markdown
# Fix: <Issue Title>

**Type**: bug
**Priority**: <0-4>
**Fixes**: <issue reference>

## Root Cause

<From RCA report>

## Fix Implementation

<What to change and why>

## Files to Modify

- `<file>`: <change description>

## Acceptance Criteria

- [ ] Regression test passes
- [ ] Original symptom no longer reproducible
- [ ] No new test failures
- [ ] `bun run check-types` passes
- [ ] `bun run build` passes
```

## Phase 5: Verification

Prove fix works and nothing else broke.

### Verification Checklist

```bash
# 1. Regression test passes
bun test <regression-test-file>

# 2. Original symptom gone
<manual verification or test>

# 3. No new failures
bun run test

# 4. Types and build
bun run check-types
bun run build
```

### Iteration: Verify → RCA Loop

If fix doesn't work:

```
Test still fails after fix
    │
    ▼
Root cause was wrong or incomplete
    │
    ▼
BACK TO RCA:
• Eliminate current hypothesis
• Generate new hypotheses
• Update RCA Report with iteration
```

### Verify → Impact Loop

If fix causes regressions:

```
New test failures after fix
    │
    ▼
Fix has unintended side effects
    │
    ▼
BACK TO IMPACT:
• Reassess blast radius
• Consider alternative fix approach
```

## Loop Limits

Prevent infinite iteration:

| Loop         | Soft Limit | Hard Limit | At Hard Limit               |
| ------------ | ---------- | ---------- | --------------------------- |
| RCA → Repro  | 2          | 4          | Escalate / pair debug       |
| RCA → Triage | 1          | 2          | Re-evaluate original report |
| Verify → RCA | 2          | 3          | Oracle deep review          |

## Quick Reference

### Tool Selection

| Need                  | Tool                            |
| --------------------- | ------------------------------- |
| Parse stack trace     | Read + mcp**gkg**get_definition |
| Find callers          | mcp**gkg**get_references        |
| Recent changes        | git log, git blame              |
| Binary search commits | git bisect                      |
| Reasoning about cause | oracle                          |
| Validate fix approach | Spike via MULTI_AGENT_WORKFLOW  |

### Common Mistakes

- **Fixing symptom, not cause** → Leads to recurrence
- **Skipping reproduction** → Can't verify fix
- **No regression test** → Bug returns later
- **Ignoring impact** → Fix breaks other things
- **Not iterating** → Wrong diagnosis persists
