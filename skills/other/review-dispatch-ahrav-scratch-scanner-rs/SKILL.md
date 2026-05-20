---
name: review-dispatch
description: Parallel specialist code review — 6 focused agents (correctness, design, performance, safety, docs, complexity) diverge independently, then a single ranker merges findings into an importance-ranked report with confidence scores
---

# Review Dispatch

A two-phase specialist code review. Six independent agents each review the same
code through a different lens, then a single ranker merges and prioritizes all
findings into one actionable report.

## When to Use

- Before merging a feature branch or opening a PR
- After completing a significant implementation
- When you want deeper review than a single pass can provide
- For critical code paths where missed issues are costly

## Invocation

```
review-dispatch [<files-or-diff>]
```

- With no argument: reviews the open PR for the current branch (via `gh pr diff`),
  falling back to local unstaged + staged changes if no PR exists.
- With file paths: reviews those specific files
- With a branch name: reviews `git diff main...<branch>`

## Gathering the Review Target

Before launching agents, determine what code to review. The resolution order
is: explicit argument → open PR → local changes.

1. If the user provided specific files, read them and diff them against the
   base branch.
2. If the user provided a branch name, run `git diff main...<branch>`.
3. If no argument was provided, try the **PR-first** path:
   a. Run `gh pr view --json number,baseRefName,headRefName` on the current
      branch. If an open PR exists, use its diff:
      `gh pr diff <number>` for the diff, and
      `gh pr diff <number> --name-only` (or parse the diff header) for the
      changed file list.
   b. If no PR exists (command fails or returns nothing), fall back to local:
      run `git diff` for unstaged changes plus `git diff --cached` for staged
      changes.
4. Also run the appropriate `--name-only` variant to get the list of changed
   files, then read the FULL content of each changed file — agents need
   surrounding context, not just the diff hunks.

Assemble two artifacts:
- **DIFF**: the raw diff output
- **FULL_FILES**: the complete content of every changed file

If the diff is empty, tell the user there's nothing to review and stop.

When reviewing a PR, include the PR number and title in the review header so
findings can be linked back to the PR.

## Phase 1 — Specialist Reviews (6 Parallel Agents)

Launch **all 6 agents in a single message** using the Codex agent tools (`spawn_agent`, `send_input`, `wait`) with
`agent_type=default`. Each agent gets the same code but a different
review lens.

### Common Preamble (included in every agent's prompt)

```
You are a specialist code reviewer. You have ONE job: review the code below
through the lens of {SPECIALTY}. Ignore issues outside your specialty — other
specialists are covering those.

## Code Under Review

### Changed Files
{DIFF}

### Full File Context
{FULL_FILES}

## Rules

- Only report findings within your specialty. Do NOT stray.
- Be concrete: cite file paths and line numbers for every finding.
- Distinguish between "must fix" and "should fix" and "nit".
- If you find nothing noteworthy, say so explicitly — do not invent issues.
- Explore the broader codebase (`rg --files`, `rg`, and targeted file reads) when you need context to
  judge whether something is a real issue or an intentional pattern.
- For each finding, state the CURRENT behavior and the DESIRED behavior.

## Output Format

Return a markdown document starting with:
`# {SPECIALTY} Review`

Then a findings table:

| Severity | File:Line | Finding | Current → Desired |
|----------|-----------|---------|-------------------|

Followed by detailed write-ups for any HIGH or CRITICAL findings, including
suggested fixes with code snippets.

End with a summary: X critical, Y high, Z medium, W low findings.
```

### Agent Specialties

Each agent's `{SPECIALTY}` section replaces the placeholder above.

---

**Agent 1 — Functional Correctness**

```
Your specialty: FUNCTIONAL CORRECTNESS

Focus exclusively on:
- Logic errors, off-by-one mistakes, incorrect boundary conditions
- Unhandled or silently swallowed error cases
- Violations of stated invariants or contracts
- Race conditions, TOCTOU bugs, atomicity gaps
- Missing or incorrect state transitions
- Incorrect operator precedence or short-circuit logic
- Functions that don't do what their name/docs claim

Severity guide:
- CRITICAL: Produces wrong results or data corruption silently
- HIGH: Can panic/crash, or wrong results under specific inputs
- MEDIUM: Edge case that's unlikely but possible
- LOW: Defensive improvement, not a current bug
```

---

**Agent 2 — Design & Architecture**

```
Your specialty: DESIGN & ARCHITECTURE

Focus exclusively on:
- Does the code fit the existing module structure and ownership patterns?
- Are abstractions at the right level? (too much indirection or too little)
- Coupling: does this change create unwanted dependencies between modules?
- Cohesion: does each struct/function have a single, clear responsibility?
- Are public APIs consistent with adjacent APIs in the codebase?
- Type design: could the type system prevent more misuse? (newtypes, enums
  over bools, typestate, parse-don't-validate)
- Naming: do names match project conventions and convey intent?

Severity guide:
- CRITICAL: Architectural violation that will cause cascading problems
- HIGH: Significant design flaw that makes code hard to change correctly
- MEDIUM: Inconsistency with existing patterns or unnecessary coupling
- LOW: Naming nit, minor structural suggestion
```

---

**Agent 3 — Performance**

```
Your specialty: PERFORMANCE

Focus exclusively on:
- Unnecessary heap allocations in hot paths (Vec, String, Box in loops)
- Missing capacity pre-allocation for known-size collections
- Cloning where borrowing would suffice
- O(n²) or worse algorithms hidden in iteration patterns
- Lock contention or oversized critical sections
- Cache-unfriendly data layouts or access patterns
- Blocking operations in async contexts
- Oversized futures or unnecessary Arc/Mutex usage
- Missing #[inline] on small hot functions
- Redundant work (recomputation, repeated lookups, unnecessary sorting)

This codebase uses: NONE_U32 sentinels, const generics for granularity,
#[inline(always)] on hot paths, debug_assert! for zero-cost invariants.

Severity guide:
- CRITICAL: O(n²+) in a path that processes every scanned byte/file
- HIGH: Allocation per-item in a hot loop, lock held across I/O
- MEDIUM: Avoidable clone, missing with_capacity, suboptimal iterator chain
- LOW: Micro-optimization, style preference
```

---

**Agent 4 — Safety & Security**

```
Your specialty: SAFETY & SECURITY

Focus exclusively on:
- Unsafe blocks: are safety invariants documented and actually upheld?
- Buffer overflows, out-of-bounds access, integer overflow in size math
- Use-after-free potential in buffer pool or scratch operations
- Untrusted input handling: length limits, malformed data, amplification
- Information leaks (secrets in logs, error messages, debug output)
- TOCTOU in filesystem operations
- Denial of service vectors (unbounded allocations, regex backtracking)
- Cryptographic misuse (if applicable)

For each unsafe block, verify:
1. Safety comment exists and is accurate
2. Invariants are enforced by the caller, not just assumed
3. Scope is minimal (only unsafe ops inside the block)

Severity guide:
- CRITICAL: Memory safety violation, exploitable vulnerability
- HIGH: Missing safety invariant, potential UB under specific inputs
- MEDIUM: Unsafe block larger than necessary, missing safety comment
- LOW: Defensive hardening suggestion
```

---

**Agent 5 — Documentation & Clarity**

```
Your specialty: DOCUMENTATION & CLARITY

Focus exclusively on:
- Are public items (pub fn, pub struct, pub trait) documented?
- Do doc comments explain WHY, not just WHAT?
- Are safety invariants for unsafe code documented with /// # Safety?
- Are non-obvious algorithms explained? (link to papers/references if relevant)
- Do error types document when each variant is returned?
- Are doc comments accurate? (do they match the actual behavior?)
- Module-level documentation: does the reader understand the module's role?

Do NOT flag missing docs on private helpers, test functions, or trivially
obvious items. Focus on public API and complex internal logic.

Severity guide:
- CRITICAL: Safety contract for unsafe code is undocumented or wrong
- HIGH: Public API with no docs, or docs that describe wrong behavior
- MEDIUM: Missing explanation for a non-obvious algorithm or invariant
- LOW: Doc style nit, minor wording improvement
```

---

**Agent 6 — Complexity & Simplification**

```
Your specialty: CODE COMPLEXITY & SIMPLIFICATION

Focus exclusively on:
- Functions that are too long (>50 lines of logic) — suggest decomposition
- Deeply nested control flow (>3 levels of if/match/loop)
- Duplicated logic that should be extracted
- Overly clever code that could be rewritten more simply
- Dead code, unreachable branches, redundant conditions
- Boolean parameters that should be enums
- Complex match arms that could be simplified with helper methods
- Over-engineering: abstractions, traits, generics used once
- Under-engineering: copy-paste that should be a shared function

For each finding, show the simpler alternative. Don't just say "simplify" —
show WHAT the simplified version looks like.

Severity guide:
- CRITICAL: Complexity hides a bug (found by simplifying the logic)
- HIGH: Function is genuinely hard to reason about for the next maintainer
- MEDIUM: Could be simpler but is still understandable
- LOW: Style preference, minor refactor opportunity
```

---

## Phase 2 — Rank & Merge (Single Agent)

After all 6 specialists complete, launch **1 ranking agent** using the Codex agent tools (`spawn_agent`, `send_input`, `wait`) with `agent_type=default`.

### Ranker Prompt

```
You are the Code Review Synthesizer. Six specialist reviewers have independently
reviewed the same code change. Your job is to merge their findings into one
prioritized, actionable report.

## Original Diff
{DIFF}

## Specialist Reports
{ALL_SIX_REPORTS}

## Your Task

### 1. Deduplicate

Multiple specialists may have flagged the same underlying issue from different
angles. Group these into single findings and note which specialists flagged it.

### 2. Score Each Finding

For every unique finding, assign:

- **Importance** (1-10): How much does this matter?
  - 9-10: Must fix before merge — correctness bug, safety hole, data loss risk
  - 7-8: Should fix before merge — significant design flaw, perf regression
  - 5-6: Fix soon — meaningful improvement, tech debt
  - 3-4: Nice to have — minor improvement
  - 1-2: Nit — style, preference

- **Confidence** (0-100): How confident are you this is a real issue?
  - 90-100: Clear bug or violation, evidence in the code
  - 70-89: Very likely an issue, would need testing to confirm
  - 50-69: Plausible concern, specialist may be over-flagging
  - Below 50: Speculative, possibly a false positive

### 3. Classify

Assign each finding exactly one category:
- 🔴 MUST FIX (importance ≥ 8, confidence ≥ 70)
- 🟠 SHOULD FIX (importance ≥ 6, confidence ≥ 60)
- 🟡 CONSIDER (importance ≥ 4, confidence ≥ 50)
- ⚪ NIT (everything else)

### 4. Output Format

```markdown
## Code Review Summary

**Files reviewed**: {list}
**Specialists**: Correctness, Design, Performance, Safety, Docs, Complexity
**Total unique findings**: X (Y critical, Z high, ...)

### 🔴 Must Fix

| # | Finding | File:Line | Importance | Confidence | Specialists |
|---|---------|-----------|------------|------------|-------------|
| 1 | ...     | ...       | 9/10       | 95%        | Correctness, Safety |

**Details:**

#### 1. {Finding title}
- **What**: {description}
- **Why it matters**: {impact}
- **Fix**: {concrete suggestion with code}
- **Flagged by**: {which specialists}

### 🟠 Should Fix

{same table + details format}

### 🟡 Consider

{same table format, details only for non-obvious items}

### ⚪ Nits

{table only, no details}

### Review Health

| Specialist | Findings | Signal | Notes |
|------------|----------|--------|-------|
| Correctness | 3       | 🟢 High | Found 1 real bug |
| Design     | 2       | 🟡 Med  | Subjective but reasonable |
| Performance | 0      | 🟢 Clean | No issues found |
| Safety     | 1       | 🔴 High | Unsafe block needs fix |
| Docs       | 4       | 🟡 Med  | Missing pub docs |
| Complexity | 2       | 🟢 Low  | Minor suggestions |

Signal ratings:
- 🟢 High: Findings are concrete and actionable
- 🟡 Medium: Mix of real issues and preferences
- 🔴 Critical: Found blocking issues
- ⚪ Clean: Nothing found (which is fine)
```

### Rules

- If a specialist found zero issues, that is GOOD — do not penalize them or
  invent issues. Note it as a clean bill of health in that area.
- If two specialists found the same root cause, count it once but note both
  perspectives.
- Preserve file:line citations from the specialist reports.
- Do NOT add your own findings — you are a synthesizer, not a reviewer.
- If a specialist's finding seems wrong or based on a misunderstanding of the
  codebase, lower its confidence but still include it (marked as uncertain).
```

## Final Presentation

After the ranker completes, present the synthesized report directly to the
user. The report is the ranker's output — do not add a wrapper or summary
around it.

If there are MUST FIX items, call them out prominently at the top.

## Configuration

Default: 6 specialists + 1 ranker (7 agents total). The user can disable
specific specialists:

```
review-dispatch --skip=docs,complexity   (run 4 specialists + 1 ranker)
```

Minimum: at least 2 specialists must run. The ranker always runs.

## Tips

- Pair with `design-tournament` for new code (design first, review after).
- For performance-critical changes, also run `bench-compare` before and after.
- For unsafe code changes, the Safety specialist is essential — don't skip it.
- If the diff is very large (>1000 lines), consider reviewing in logical chunks
  rather than all at once to keep agent context focused.
