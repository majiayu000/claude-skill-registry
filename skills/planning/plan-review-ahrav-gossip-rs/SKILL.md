---
name: plan-review
description: Use when a markdown plan file exists and needs validation before implementation — catches design flaws, logic holes, footguns, unnecessary complexity, and performance concerns while changes are still cheap
---

# Plan Review

A specialist review for markdown plan files. Selected agents review the same
plan through different lenses, then a synthesizer merges findings into a
focused, actionable report with RETHINK / REVISE / WATCH categories.

## When to Use

- After `/design-tournament` picks an approach but before implementation starts
- After writing or receiving an implementation plan
- Before executing any multi-step plan that touches critical code paths
- When a plan references specific codebase files, types, or modules that should
  be validated against reality

## Invocation

```
/plan-review <path-to-plan-file>
/plan-review --skip=performance path/to/plan.md
/plan-review --focus=distributed path/to/plan.md
/plan-review --mode=fast path/to/plan.md
/plan-review --rerun-unresolved path/to/plan.md
```

- `--skip=<agent>`: Drop a specialist (correctness, footguns, simplification,
  performance). Minimum 2 specialists must run.
- `--focus=<domain>`: Adds domain context to all agent prompts (e.g.,
  `distributed`, `concurrency`, `security`).
- `--mode=fast|standard`: `fast` is optimized for small features and convergence;
  `standard` runs the full specialist set.
- `--rerun-unresolved`: Re-review mode; only previously unresolved findings (and
  regressions directly caused by edits) should be reported.

## Convergence Defaults

Use **Fast mode** by default when all are true:

- Plan is small (typically <= 4 referenced code files and <= 2 core behavior
  changes)
- No new unsafe/concurrency/distributed/security architecture
- No schema/storage identity contract changes
- No broad runtime/backend rollout changes

Fast mode reviewers:

- Required: Correctness, Footguns
- Optional: Simplification (only if plan introduces new flags/config/options,
  new abstractions, or extra plumbing)
- Optional: Performance (only if plan touches hot loops / scanner hot paths or
  claims performance impact)

Goal: for small features, converge in **one** review pass with minimal,
high-signal findings.

## Phase 0 — Orchestrator Prep (no agents)

Before launching agents, the orchestrator:

1. Read the plan file in full.
2. Scan for referenced file paths, modules, types, traits, and design docs.
3. Quick Glob/Grep to confirm referenced codebase paths exist. Note any that
   are missing or have moved.
4. If the plan references design docs in `docs/`, read them.
5. Determine review mode (`fast` or `standard`) from explicit flag or
   convergence defaults above.
6. Build a **Scope Charter**:
   - In-scope changes the plan is allowed to make
   - Explicit out-of-scope items
   - Conditions that justify scope escalation (for example default runtime path
     makes in-scope fix ineffective)
7. If rerun mode is active, collect prior findings and mark them as
   RESOLVED/PARTIAL/UNRESOLVED.
8. Assemble substitution variables:
   - **{PLAN}**: the full plan text
   - **{CONTEXT}**: a summary of referenced paths, whether they exist, any
     design doc excerpts, and any discrepancies found
   - **{SCOPE_CHARTER}**: explicit scope boundaries and escalation conditions
   - **{PRIOR_FINDINGS}**: optional unresolved-finding list for rerun mode

If the plan file is empty or cannot be read, tell the user and stop.

## Phase 1 — Specialist Reviews (2-4 Parallel Agents)

Launch **all selected agents in a single message** using the Task tool with
`subagent_type=general-purpose`. Each agent gets the same plan + context but a
different review lens.

### Common Preamble (included in every agent's prompt)

```
You are a specialist plan reviewer. You have ONE job: review the plan below
through the lens of {SPECIALTY}. Ignore issues outside your specialty — other
specialists are covering those.

## Plan Under Review

{PLAN}

## Codebase Context

{CONTEXT}

## Scope Charter

{SCOPE_CHARTER}

## Prior Findings (optional rerun mode)

{PRIOR_FINDINGS}

## Rules

- Only report findings within your specialty. Do NOT stray.
- Only report findings that REQUIRE action. No nits, no "nice to have", no
  stylistic suggestions. If a finding wouldn't change the plan, don't report it.
- Be concrete: cite the specific plan section, step number, or quoted text for
  every finding.
- Explore the codebase (Glob, Grep, Read) to ground your findings in reality.
  The most valuable findings come from gaps between plan assumptions and
  codebase reality.
- For each finding, state the PROBLEM and the RECOMMENDED CHANGE to the plan.
- Respect the Scope Charter. Do NOT expand scope unless you can prove the
  default execution path makes the current scope invalid.
- In rerun mode, only report unresolved prior findings or regressions directly
  introduced by the revised plan.
- Rate each finding:
  - impact (1-10): How much does this matter if unaddressed?
  - confidence (0-100): How sure are you this is a real issue?

## Output Format

Return a markdown document starting with:
`# {SPECIALTY} Review`

Then a findings list. For each finding:

### Finding N: {title}

- **Plan section**: {which part of the plan}
- **Problem**: {what's wrong or missing}
- **Evidence**: {codebase evidence — file paths, existing code, design doc quotes}
- **Recommended change**: {specific edit to the plan}
- **Impact**: N/10
- **Confidence**: N%

End with: "Total findings: N" (0 is a valid answer — do not invent issues).
```

### Agent Specialties

Each agent's `{SPECIALTY}` section replaces the placeholder above.

---

**Agent 1 — Correctness & Soundness**

```
Your specialty: CORRECTNESS & SOUNDNESS

Focus exclusively on:
- Does the plan actually solve the stated problem?
- Are there logic errors in the described approach?
- Do state transitions, invariants, or contracts hold under all cases?
- Are assumptions about existing code accurate? (check the codebase)
- Does the plan reference types, traits, or APIs that don't exist or have
  different signatures than described?
- Are there ordering dependencies the plan gets wrong?
- Does the plan contradict any design docs it references?

Do NOT review performance, complexity, or failure modes — other specialists
handle those.
```

---

**Agent 2 — Footguns & Failure Modes**

```
Your specialty: FOOTGUNS & FAILURE MODES

Focus exclusively on:
- Race conditions, TOCTOU bugs, atomicity gaps in the planned approach
- Edge cases the plan doesn't address (empty inputs, overflow, boundary values)
- Error propagation paths that could silently swallow failures
- Unsafe interactions between components the plan modifies
- Partial failure scenarios (what if step 3 of 5 fails?)
- Implicit assumptions that could break under different configurations
- "Works on my machine" traps — environment or ordering dependencies

Do NOT review correctness of the happy path, performance, or complexity —
other specialists handle those.
```

---

**Agent 3 — Simplification**

```
Your specialty: SIMPLIFICATION

Focus exclusively on:
- YAGNI: Does the plan build things that aren't needed yet?
- Does the codebase already have utilities, traits, or patterns that the plan
  reinvents? (search with Glob/Grep)
- Are there unnecessary abstraction layers, indirection, or generics?
- Could fewer files, types, or steps achieve the same result?
- Is the plan over-engineering for hypothetical future requirements?
- Are there feature flags, configuration options, or extension points that
  nobody asked for?
- Could an existing codebase pattern be extended instead of building new?

For each finding, describe the simpler alternative concretely. Don't just say
"simplify" — show WHAT the simpler version looks like.

Do NOT review correctness, failure modes, or performance — other specialists
handle those.
```

---

**Agent 4 — Performance & Scalability**

```
Your specialty: PERFORMANCE & SCALABILITY

Focus exclusively on:
- Hot path allocations introduced by the plan (Vec, String, Box in loops)
- Lock contention or oversized critical sections in the planned design
- O(n^2) or worse algorithms hidden in the approach
- Cache-unfriendly data layouts or access patterns
- Blocking operations in async contexts
- Unbounded growth (queues, buffers, caches without size limits)
- Unnecessary serialization/deserialization on critical paths
- Missing batching or amortization opportunities

Only flag issues that matter at the scale this system operates at. Do not flag
micro-optimizations or theoretical concerns that won't manifest in practice.

Do NOT review correctness, failure modes, or complexity — other specialists
handle those.
```

---

## Phase 2 — Synthesize (Single Agent)

After all specialists complete, launch **1 synthesizer agent** using the Task
tool with `subagent_type=general-purpose`.

### Synthesizer Prompt

```
You are the Plan Review Synthesizer. Specialist reviewers have independently
reviewed the same implementation plan. Your job is to merge their findings into
one focused, actionable report.

## Original Plan
{PLAN}

## Specialist Reports
{ALL_SPECIALIST_REPORTS}

## Scope Charter
{SCOPE_CHARTER}

## Prior Findings (optional rerun mode)
{PRIOR_FINDINGS}

## Your Task

### 1. Deduplicate

Multiple specialists may have flagged the same underlying issue from different
angles. Group these into single findings and note which specialists flagged it.

### 2. Overload Check

Count the unique findings after deduplication. If there are MORE THAN 10 unique
findings, or MORE THAN 3 that would be classified as RETHINK (see below), do
NOT list them all individually. Instead, emit ONLY this:

---

**This plan needs significant rework.** The review found {N} issues across
{areas}. Rather than patching {N} individual problems, redesign the approach
and re-run `/plan-review`. The top 3 structural issues to address first are:

1. {highest-impact finding — title, problem, recommended change}
2. {second highest — title, problem, recommended change}
3. {third highest — title, problem, recommended change}

---

Then STOP. Do not produce the full report below.

### 3. Score Each Finding (only if overload check passes)

For every unique finding, assign:

- **Impact** (1-10): How much does this matter if unaddressed?
  - 9-10: Fundamental flaw — approach won't work or will cause serious harm
  - 7-8: Significant gap — plan needs specific edits before implementation
  - 5-6: Real concern — implementation must handle this explicitly
  - 3-4: Minor — below reporting threshold, discard

- **Confidence** (0-100): How confident are you this is a real issue?
  - 90-100: Clear problem, evidence in the codebase
  - 70-89: Very likely an issue, strong reasoning
  - 50-69: Plausible concern, may need investigation
  - Below 50: Speculative — discard

Discard any finding with impact < 4 or confidence < 50. Every finding in the
final report must require action.

### 4. Classify

Assign each surviving finding exactly one category:

- **RETHINK** (impact >= 8, confidence >= 70): Stop. Fundamental approach
  change needed before proceeding. Use this only when:
  - plan contradicts a required correctness contract/invariant, OR
  - default runtime path makes the proposed scope ineffective, OR
  - clear data-loss/security/soundness risk exists.
- **REVISE** (impact >= 6, confidence >= 60): Make specific plan edits before
  implementing.
- **WATCH** (impact >= 4, confidence >= 50): Plan is sound but implementation
  must handle this explicitly.

In rerun mode, do NOT introduce net-new categories/findings unless they are
directly caused by changed plan sections or newly discovered hard evidence.

### 5. Output Format

```markdown
## Plan Review Summary

**Plan**: {plan file path or title}
**Specialists**: {SPECIALIST_LIST}
**Unique findings**: N (after dedup and filtering)

### RETHINK

Items that require fundamental plan changes before proceeding.

| # | Finding | Plan Section | Impact | Confidence | Specialists |
|---|---------|-------------|--------|------------|-------------|

**Details:**

#### 1. {Finding title}
- **Problem**: {description}
- **Evidence**: {codebase evidence}
- **Recommended change**: {specific plan revision}
- **Flagged by**: {which specialists}

### REVISE

Items that require specific plan edits.

{same table + details format}

### WATCH

Items the plan handles correctly but implementation must be careful about.

{same table + details format}

### Specialist Signal

| Specialist | Findings | Assessment |
|------------|----------|------------|
| {Specialist A} | N | {one-line summary} |
| {Specialist B} | N | {one-line summary} |
| ... | ... | ... |
```

### Rules

- Do NOT add your own findings — you are a synthesizer, not a reviewer.
- Do NOT include a MINOR or NIT category. Every finding must require action.
- If a specialist found zero issues, that is GOOD. Note it as clean.
- If a specialist's finding seems wrong or speculative, lower its confidence.
  If it drops below 50%, discard it.
- Preserve plan section references and codebase citations from specialist
  reports.
- Enforce scope-lock: out-of-scope concerns cannot be elevated to RETHINK
  unless Scope Charter escalation conditions are met.
- For performance findings, require concrete hot-path evidence and at least one
  measurable validation step; otherwise demote/discard.
```

## Final Presentation

After the synthesizer completes, present the report directly to the user. The
report is the synthesizer's output — do not add a wrapper or summary around it.

If there are RETHINK items, call them out prominently at the top.

If the synthesizer triggered the overload threshold, present the "significant
rework" verdict as-is and recommend the user redesign before re-running
`/plan-review`.

## Configuration

Default behavior:

- `standard`: 4 specialists + 1 synthesizer (5 agents total)
- `fast`: 2-4 specialists + 1 synthesizer (3-5 agents total), selected by
  convergence defaults and `--skip` flags

```
/plan-review --skip=performance     (3 specialists + 1 synthesizer)
/plan-review --skip=footguns,performance  (2 specialists + 1 synthesizer)
/plan-review --mode=fast            (adaptive 2-4 specialists + synthesizer)
/plan-review --rerun-unresolved     (rerun unresolved-only mode)
```

Minimum: at least 2 specialists must run. The synthesizer always runs.

The `--focus=<domain>` flag appends a paragraph to each agent's prompt:

```
Additional context: This plan operates in the {domain} domain. Pay particular
attention to {domain}-specific concerns in your review.
```

## Tips

- Pair with `/design-tournament` (design first) and `/review-dispatch` (code
  review after implementation). This skill fills the gap between them.
- For plans that reference many codebase files, Phase 0's path validation
  catches stale references before agents waste time on them.
- For small features, prefer `--mode=fast` to drive one-pass convergence.
- On reruns, use `--rerun-unresolved` to prevent finding churn and scope creep.
