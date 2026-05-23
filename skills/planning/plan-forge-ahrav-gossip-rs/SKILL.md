---
name: plan-forge
description: Use when a task needs an implementation plan that is iteratively created and stress-tested through review-and-revise cycles before implementation begins — catches blind spots, incorrect codebase assumptions, unnecessary complexity, and performance pitfalls while changes are still cheap
---

# Plan Forge

Iteratively creates AND refines an implementation plan through review-and-revise
cycles. A metallurgy metaphor: the plan is heated (reviewed), hammered (revised),
and quenched (finalized) until it holds up under stress.

Unlike `/plan-review` (one-shot post-hoc review of an existing plan), plan-forge
creates the plan from scratch and runs 1-3 rounds of dual review, consolidation,
and revision before presenting the final artifact.

## When to Use

- Before implementing a multi-step feature that touches critical code paths
- When the task involves non-obvious architectural decisions
- When you want a plan that has been stress-tested before writing any code
- When blind spots in planning are more expensive than the review overhead

## When NOT to Use

- Single-file, few-line changes (just do them)
- The plan already exists and just needs review (use `/plan-review`)
- You need to explore multiple competing designs first (use `/design-tournament`,
  then feed the winner into `/plan-forge`)
- Pure research tasks (use `/deep-research` or `/deeper-research`)

## Invocation

```
/plan-forge <task description>
/plan-forge --rounds=1 <task>
/plan-forge --focus=concurrency <task>
/plan-forge --plan-only <task>
/plan-forge --review-only <path-to-existing-plan>
```

## Architecture

```
Phase 0: Plan Creation (orchestrator explores codebase, writes initial plan)
    |
    v
+---> Phase 1: Dual Review (2 parallel general-purpose agents, fresh context)
|         |
|     Phase 2: Consolidation (1 general-purpose agent merges findings)
|         |
|     Phase 3: Revision (orchestrator revises plan inline)
|         |
|     Decision: continue? ----yes (RETHINK/REVISE items remain, round < max)---+
|         |                                                                      |
|         no (only WATCH items, or max round reached)                            |
|         v                                                                      |
+---- Phase 4: Final Presentation <---------------------------------------------+
```

**Agents per round:** 2 reviewers + 1 consolidator = 3
**Total agents across 1-3 rounds:** 3-9

---

## Phase 0 --- Plan Creation (Orchestrator, Inline)

The orchestrator (you, not a sub-agent) creates the initial plan.

### Steps

1. **Parse task** --- identify core objective, constraints, domain.
2. **Explore codebase** --- use Glob, Grep, Read to find relevant files,
   patterns, existing utilities. Check `src/stdx/` and neighboring modules
   for duplication (per CLAUDE.md rules).
3. **Write initial plan** to `~/.claude/plans/{YYYY-MM-DD}-{feature-slug}-v1.md`.

### Versioned Plan Files

Each revision writes a NEW file with an incremented version suffix. Prior
versions are kept for reference and diffing.

```
~/.claude/plans/2026-02-23-retry-logic-v1.md   <- Phase 0 output (initial)
~/.claude/plans/2026-02-23-retry-logic-v2.md   <- After Round 1 revision
~/.claude/plans/2026-02-23-retry-logic-v3.md   <- After Round 2 revision (final)
```

### Plan File Template

```markdown
# {Plan Title}

| Field            | Value                        |
|------------------|------------------------------|
| Date             | {YYYY-MM-DD}                 |
| Status           | Draft / In Review / Final    |
| Version          | v{N}                         |
| Rounds completed | {N}                          |
| Task             | {one-line summary}           |

## Problem Statement

{What problem does this solve and why does it matter?}

## Codebase Context

{Discovered files, patterns, abstractions relevant to the task.
Include file paths and brief descriptions.}

## Steps

### Step {N}: {Title}

- **What**: {concrete description}
- **Why**: {justification}
- **Files**: {exact paths to create or modify}
- **Tests**: {what to test and how}
- **Acceptance criteria**: {how to verify correctness}

## Testing Strategy

{Overall testing approach --- unit, property-based, integration, etc.}

## Revision Log

{Populated during review rounds. Cumulative across versions.}

| Round | Finding ID | Action Taken |
|-------|-----------|--------------|

## Open Items

{WATCH items and unresolved concerns.}
```

### Flags

- `--review-only <path>`: Skip Phase 0. Load the plan at `<path>` and jump
  directly to Phase 1.
- `--plan-only`: Stop after Phase 0. Write the plan and present it without
  running any review rounds.

---

## Phase 1 --- Dual Review (2 Parallel Agents)

Launch **2 agents in a single message** using the Task tool with
`subagent_type=general-purpose`. Each covers all 4 review lenses but with
different primary emphasis to reduce blind-spot overlap.

| Agent | Label            | Primary Emphasis (40%)         | Secondary (20% each)                     |
|-------|------------------|-------------------------------|------------------------------------------|
| Alpha | Forge Inspector  | Correctness & Soundness       | Footguns, Simplification, Performance    |
| Beta  | Forge Optimizer  | Simplification & Pragmatism   | Performance, Correctness, Footguns       |

### Common Preamble (included in both agents' prompts)

```
You are {AGENT_LABEL}, a plan reviewer in Round {ROUND} of the Plan Forge
process. You review the plan below through ALL four lenses but emphasize
{PRIMARY_EMPHASIS} (allocate ~40% of your attention there, ~20% each to the
other three).

## Plan Under Review

{PLAN}

## Codebase Context

{CONTEXT}

{PRIOR_ROUND_SECTION}

## Four Review Lenses

### Correctness & Soundness
- Does the plan actually solve the stated problem?
- Are assumptions about existing code accurate? (check the codebase)
- Do referenced types, traits, APIs exist with described signatures?
- Are ordering dependencies correct?
- Do state transitions and invariants hold under all cases?

### Footguns & Failure Modes
- Race conditions, TOCTOU bugs, atomicity gaps
- Edge cases not addressed (empty inputs, overflow, boundaries)
- Error propagation paths that silently swallow failures
- Partial failure scenarios (what if step 3 of 5 fails?)
- Implicit assumptions that break under different configurations

### Simplification
- YAGNI: does the plan build things not yet needed?
- Does the codebase already have utilities the plan reinvents? (search with
  Glob/Grep, especially src/stdx/)
- Could fewer files, types, or steps achieve the same result?
- Are there unnecessary abstraction layers or indirection?
- Could an existing pattern be extended instead of building new?

### Performance & Scalability
- Hot path allocations in loops (Vec, String, Box)
- Lock contention or oversized critical sections
- O(n^2) or worse algorithms hidden in the approach
- Blocking operations in async contexts
- Unbounded growth (queues, buffers, caches without limits)

## Rules

- Explore the codebase (Glob, Grep, Read) to ground findings in reality.
  The most valuable findings come from gaps between plan assumptions and
  codebase reality.
- Only report findings that REQUIRE action. No nits, no style suggestions.
- Be concrete: cite the specific plan step, section, or quoted text.
- For each finding, state the PROBLEM and the RECOMMENDED CHANGE.
- Rate each finding:
  - Impact (1-10): How much does this matter if unaddressed?
  - Confidence (0-100%): How sure are you this is a real issue?

## Output Format

Return a markdown document starting with:
`# {AGENT_LABEL} Review --- Round {ROUND}`

For each finding:

### {FINDING_ID}: {title}

- **Plan step**: {which step or section}
- **Lens**: {Correctness | Footguns | Simplification | Performance}
- **Problem**: {what is wrong or missing}
- **Evidence**: {codebase evidence --- file paths, existing code, design docs}
- **Recommended change**: {specific edit to the plan}
- **Impact**: N/10
- **Confidence**: N%

End with: "Total findings: N" (0 is valid --- do not invent issues).
```

### Finding ID Scheme

```
R{round}.A{agent}.F{n}
```

- Agent identifiers: `a` for Alpha, `b` for Beta.
- Example: `R1.Aa.F3` = Round 1, Alpha, Finding 3.

### Agent-Specific Sections

**Alpha (Forge Inspector)** --- replace `{AGENT_LABEL}` with `Forge Inspector`,
`{PRIMARY_EMPHASIS}` with `Correctness & Soundness`:

```
Your primary emphasis is CORRECTNESS & SOUNDNESS (40%). Prioritize verifying
that the plan actually solves the problem, that referenced code exists as
described, and that invariants hold. Give secondary attention (~20% each) to
footguns, simplification, and performance.

Use finding IDs: R{ROUND}.Aa.F1, R{ROUND}.Aa.F2, ...
```

**Beta (Forge Optimizer)** --- replace `{AGENT_LABEL}` with `Forge Optimizer`,
`{PRIMARY_EMPHASIS}` with `Simplification & Pragmatism`:

```
Your primary emphasis is SIMPLIFICATION & PRAGMATISM (40%). Prioritize finding
YAGNI violations, existing utilities the plan reinvents, and opportunities to
achieve the same result with less complexity. Give secondary attention (~20%
each) to performance, correctness, and footguns.

Use finding IDs: R{ROUND}.Ab.F1, R{ROUND}.Ab.F2, ...
```

### Prior Round Section (Rounds 2+)

For rounds 2+, append this section to each agent's prompt:

```
## Prior Round Findings

The following findings were raised in prior rounds. Check whether the revised
plan adequately addresses them. If a prior finding is STILL present, re-raise
it with a note that it was not resolved.

{PRIOR_CONSOLIDATED_FINDINGS}
```

---

## Phase 2 --- Consolidation (1 Agent)

After both reviewers complete, launch **1 consolidator agent** using the Task
tool with `subagent_type=general-purpose`.

### Consolidator Prompt

```
You are the Forge Consolidator for Round {ROUND}. Two independent reviewers
have examined the same implementation plan. Your job is to merge their findings
into one focused, actionable report and issue a verdict.

## Original Plan

{PLAN}

## Reviewer Reports

{ALPHA_REPORT}

---

{BETA_REPORT}

{PRIOR_TRACKING_SECTION}

## Your Task

### 1. Deduplicate

Group findings that flag the same underlying issue from different angles into
single consolidated findings. Note which reviewers flagged each.

### 2. Overload Check

Count unique findings after deduplication. If there are MORE THAN 10 unique
findings, or MORE THAN 3 that would be classified as RETHINK, emit ONLY:

---

**This plan needs fundamental rework.** The review found {N} issues across
{areas}. Rather than patching individually, redesign the approach. The top 3
structural issues to address first:

1. {highest-impact finding}
2. {second highest}
3. {third highest}

---

Then STOP. Do not produce the full report.

### 3. Score Each Finding (if overload check passes)

For every unique finding, assign:

- **Impact** (1-10):
  - 9-10: Fundamental flaw --- approach won't work
  - 7-8: Significant gap --- plan needs edits before implementation
  - 5-6: Real concern --- implementation must handle explicitly
  - 3-4: Minor --- below threshold, discard

- **Confidence** (0-100%):
  - 90-100: Clear problem with codebase evidence
  - 70-89: Very likely, strong reasoning
  - 50-69: Plausible, may need investigation
  - Below 50: Speculative --- discard

Discard findings with impact < 4 or confidence < 50%.

### 4. Classify

Assign each surviving finding exactly one category:

- **RETHINK** (impact >= 8, confidence >= 70): Fundamental approach change
  needed. Non-negotiable.
- **REVISE** (impact >= 6, confidence >= 60): Specific plan edits required.
- **WATCH** (impact >= 4, confidence >= 50): Plan is sound but implementation
  must handle this explicitly.

### 5. Issue Verdict

Based on surviving findings:

- **FORGE AGAIN**: Any RETHINK items exist. Plan MUST be revised and
  re-reviewed.
- **TEMPER**: No RETHINK items, but REVISE items exist. Plan should be revised
  and re-reviewed if round < max.
- **QUENCH**: Only WATCH items (or no findings). Plan is ready.

### 6. Output Format

```markdown
## Forge Consolidation --- Round {ROUND}

**Verdict**: {FORGE AGAIN | TEMPER | QUENCH}
**Unique findings**: {N} (after dedup and filtering)

### RETHINK

| # | Finding ID | Title | Plan Step | Impact | Confidence | Reviewers |
|---|-----------|-------|-----------|--------|------------|-----------|

**Details:**

#### {R{ROUND}.C.F1}: {title}
- **Problem**: {description}
- **Evidence**: {codebase evidence}
- **Recommended change**: {specific plan revision}
- **Original IDs**: {which reviewer finding IDs map here}

### REVISE

{same format}

### WATCH

{same format}

### Prior Finding Tracking

| Prior Finding ID | Status | Notes |
|-----------------|--------|-------|
| R1.C.F2         | RESOLVED | Plan step 3 now addresses this |
| R1.C.F5         | PARTIALLY RESOLVED | Step added but edge case missing |
| R1.C.F7         | UNRESOLVED | Still not addressed |
```

### Consolidated Finding IDs

Use: `R{ROUND}.C.F{n}` (C = consolidated).

### Rules

- Do NOT add your own findings. You are a consolidator, not a reviewer.
- If a reviewer's finding seems speculative, lower its confidence. If it drops
  below 50%, discard it.
- Preserve plan step references and codebase citations from reviewer reports.
```

### Prior Tracking Section (Rounds 2+)

For rounds 2+, append this to the consolidator prompt:

```
## Prior Round Consolidated Findings

Track whether each prior finding has been addressed in the revised plan:

{PRIOR_CONSOLIDATED_FINDINGS_WITH_STATUS}

For each prior finding, assign: RESOLVED / PARTIALLY RESOLVED / UNRESOLVED.
Include this tracking in your output.
```

---

## Phase 3 --- Revision (Orchestrator, Inline)

The orchestrator (you, not a sub-agent) revises the plan based on consolidated
findings and writes a **new versioned file**.

### Revision Rules

1. **RETHINK findings**: Make fundamental changes. These are non-negotiable.
2. **REVISE findings**: Make the specific edits recommended.
3. **WATCH findings**: Add to Open Items section. Do NOT restructure the plan
   for WATCH items.
4. **Update Revision Log**: Map each finding ID to the action taken.
5. **Increment version** in header and filename (`-v1.md` -> `-v2.md`).
6. **Verify internal consistency**: After edits, re-read the plan to ensure
   steps still flow logically and no contradictions were introduced.
7. **Keep prior version file** --- do not delete or overwrite it.

---

## Round Decision

After revision, decide whether to loop back to Phase 1:

| Verdict      | Round < max | Round = max |
|-------------|-------------|-------------|
| FORGE AGAIN | -> Phase 1  | -> Phase 4 (forced stop, flag unresolved RETHINK) |
| TEMPER      | -> Phase 1  | -> Phase 4  |
| QUENCH      | -> Phase 4  | -> Phase 4  |

Default max rounds: 3. Override with `--rounds=N` (1-3).

---

## Phase 4 --- Final Presentation

1. Set plan status to `Final` in the latest version file.
2. Collect all WATCH items into Open Items section.
3. If forced stop with unresolved RETHINK items: add a prominent warning at the
   top of the plan file and call it out when presenting to the user.
4. Present a round summary table to the user.
5. Append all review reports as collapsed `<details>` sections at the end of
   the plan file.
6. Report version history with file paths.

### Final Presentation Format

```markdown
## Plan Forge Complete

**Plan**: {title}
**Rounds**: {N}
**Final verdict**: {QUENCH | forced stop}
**Version history**:
- `{path}-v1.md` (initial)
- `{path}-v2.md` (round 1 revision)
- `{path}-v3.md` (final)

### Round Summary

| Round | Verdict | RETHINK | REVISE | WATCH | Total |
|-------|---------|---------|--------|-------|-------|
| 1     | FORGE AGAIN | 1   | 3      | 2     | 6     |
| 2     | QUENCH      | 0   | 0      | 1     | 1     |

### Open Items (WATCH)

{collected WATCH items from all rounds}

### Review Reports (collapsed)

<details><summary>Round 1 --- Forge Inspector</summary>
{full report}
</details>
<details><summary>Round 1 --- Forge Optimizer</summary>
{full report}
</details>
<details><summary>Round 1 --- Consolidation</summary>
{full report}
</details>
<details><summary>Round 2 --- Forge Inspector</summary>
{full report}
</details>
...
```

---

## Configuration

| Flag | Effect |
|------|--------|
| `--rounds=N` | Override max rounds (1-3). Default: 3. |
| `--focus=<domain>` | Adds domain-specific pitfall context to all agent prompts. |
| `--plan-only` | Create plan (Phase 0), skip all reviews. |
| `--review-only <path>` | Skip plan creation, review existing plan at `<path>`. |

### Focus Domain Pitfalls

When `--focus=<domain>` is specified, append this paragraph to every agent
prompt (Phase 1 and Phase 2):

```
Additional context: This plan operates in the {DOMAIN} domain. Pay particular
attention to {DOMAIN}-specific concerns.
```

Domain-specific pitfall lists to include:

**concurrency**: data races, deadlock/livelock, lock ordering, priority
inversion, false sharing, memory ordering (Acquire/Release vs SeqCst),
`Send`/`Sync` bounds, async cancellation safety.

**distributed**: partial failure, network partitions, clock skew, exactly-once
semantics, idempotency, consensus protocol correctness, split-brain, message
ordering, retry storms.

**security**: input validation, injection (SQL/command/XSS), authentication
bypass, authorization escalation, timing side channels, secret management,
cryptographic misuse, TOCTOU in security checks.

**performance**: allocation hot paths, cache locality, branch prediction,
SIMD opportunities, async runtime blocking, lock contention, false sharing,
memory layout (SoA vs AoS), tail latency.

**unsafe**: soundness holes, aliasing violations, uninitialized memory,
lifetime transmutation, `Send`/`Sync` impl correctness, drop order, panic
safety, provenance.

---

## Anti-Patterns

| Mistake | Why it fails | Do this instead |
|---------|-------------|-----------------|
| Skipping Phase 0 codebase exploration | Plan makes wrong assumptions about existing code | Always Glob/Grep/Read before writing the plan |
| Launching reviewers sequentially | Wastes time and allows anchoring | Always launch both in a single message |
| Orchestrator adding own findings during consolidation | Conflates roles, biases revision | Only the reviewer agents produce findings |
| Revising the plan in-place (overwriting prior version) | Loses diff history | Always write a new `-v{N+1}.md` file |
| Running 3 rounds on a trivial plan | Overhead exceeds value | Use `--rounds=1` for simple plans |
| Treating WATCH items as REVISE | Over-engineering the plan | WATCH goes to Open Items, not plan restructure |
| Ignoring the overload threshold | Patching 15 findings creates a Frankenstein plan | If overload triggers, rethink the approach wholesale |

## Tips

- **Pair with `/design-tournament`**: Run a tournament first to pick the
  approach, then forge the implementation plan for the winning design.
- **Pair with `/plan-review`**: For a final one-shot validation of the forged
  plan with 4 specialist lenses instead of 2 generalist reviewers.
- **For plans with `--focus=unsafe`**: Consider following up with `/unsafe-review`
  after implementation.
- **Diff between versions**: Use `diff ~/.claude/plans/*-v1.md ~/.claude/plans/*-v2.md`
  to see exactly how the plan evolved through review rounds.
