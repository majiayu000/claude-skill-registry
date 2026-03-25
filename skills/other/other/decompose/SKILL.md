---
name: decompose
description: >
  Lightweight project decomposition skill. Analyzes project scope through a brief interview
  and determines whether the project should be treated as a single feature or split into
  multiple sub-features. For multi-split projects, generates a project manifest listing
  sub-features, dependencies, and execution order.
instructions: >
  Follow the workflow below exactly. This skill is typically invoked inside a sub-agent
  by the spec-forge chain orchestrator (Step D.1) or via /spec-forge:decompose.
  Keep the interview lightweight (3-5 rounds). Do NOT perform demand validation (that is
  /idea's job) or deep research (that is /prd's job). Focus only on scope boundaries and
  dependencies.
---

# Decompose — Project Scope Analysis

Analyze project scope and determine whether to treat it as a single feature or split into multiple sub-features before entering the spec chain.

## Core Principles

1. **Lightweight**: 3-5 rounds of questions, not a deep investigation
2. **Boundary-focused**: Only care about scope boundaries and dependencies
3. **No demand validation**: That is /idea's responsibility
4. **No deep research**: That is /prd's responsibility
5. **Single is valid**: Not every project needs splitting — a single-feature verdict is a good outcome

## Workflow

### Step 1: Read Context

Scan the project to understand what exists:

1. Use Glob to scan the project directory tree (top 3 levels)
2. Read the project README.md if it exists
3. Scan `docs/` for existing specification documents and project manifests
4. Check if `ideas/{feature-name}/draft.md` exists — if found, read it for context on scope

Summarize what you learned in 2-3 sentences. Do not present this to the user — it is internal context for the interview.

### Step 2: Scope Interview

Use AskUserQuestion to understand project boundaries. Ask 3-5 rounds of questions, adapting based on answers.

**Round 1 — The Shape:**
- What are the main functional areas or modules of this project? (e.g., "auth, payments, notifications" or "it's a single API endpoint")
- How big is this project in your mind — a single focused feature, or multiple related features?

**Round 2 — Boundaries:**
- Which parts could be developed and tested independently?
- Which parts depend on each other? (e.g., "payments needs auth to exist first")
- Are there shared foundations that multiple parts need? (data models, infrastructure, auth)

**Round 3+ — Clarification (if needed):**
- Follow up on anything unclear from rounds 1-2
- Stop when you can confidently propose a split structure

Do NOT force answers. If the user says "I'm not sure", use your judgment based on what you know.

### Step 3: Split Decision & Rationale

Based on the interview, determine: **single** or **multi-split**.

**Split heuristics:**

| Signal | Verdict |
|--------|---------|
| Multiple distinct systems (backend + frontend + pipeline) | Multi-split |
| Repeated "and also..." in scope description | Multi-split |
| No single clear purpose — hard to name in one phrase | Multi-split |
| Would produce 10+ PRD requirement groups | Multi-split |
| Single cohesive system with tightly coupled components | Single |
| Fully specifiable in a few paragraphs | Single |
| No architectural decisions needed at the boundary level | Single |
| Too unclear even after interview — need PRD to discover structure | Single (suggest running `/spec-forge:prd` first to clarify scope) |

**Good split characteristics:**
- Cohesive purpose — a clear goal or outcome
- Bounded complexity — 1-3 major components
- Clear interfaces — well-defined inputs and outputs
- Each split is substantial enough for its own Tech Design + Feature Specs

**Rationale requirement:** After reaching a verdict, you MUST produce a formal Split Rationale block (see Step 4a / 4b). Do not present the verdict without justification. The rationale must name which heuristics fired with project-specific evidence, and explicitly state why the alternative verdict was rejected.

### Step 4a: Single Feature Verdict

If the project is a single feature:

1. Produce the Split Rationale block (required before informing the user):

```
Split Rationale:
  Verdict: Single feature

  Signals that fired (Single):
    ✓ [Signal text from heuristics table] — [one sentence of project-specific evidence]
    ✓ [Signal text] — [evidence]

  Signals evaluated but not triggered (Multi-split):
    ✗ [Signal text] — [why it does not apply to this project]
    ✗ [Signal text] — [why it does not apply]

  Why not Multi-split: [1-2 sentences explaining why splitting would be premature,
  over-engineered, or harmful for this specific project — reference scope, coupling,
  team size, or other concrete factors from the interview.]
```

2. Inform the user: "This project is well-scoped as a single feature. Proceeding directly to the spec chain."
3. Return the verdict. Do NOT generate a manifest file.

### Step 4b: Multi-Split — Generate Manifest

If the project should be split:

1. Produce the Split Rationale block (required before presenting the breakdown):

```
Split Rationale:
  Verdict: Multi-split ({N} sub-features)

  Signals that fired (Multi-split):
    ✓ [Signal text from heuristics table] — [one sentence of project-specific evidence]
    ✓ [Signal text] — [evidence]

  Signals evaluated but not triggered (Single):
    ✗ [Signal text] — [why it does not apply to this project]
    ✗ [Signal text] — [why it does not apply]

  Why not Single: [1-2 sentences explaining what makes this project structurally
  too broad or heterogeneous to treat as one feature — e.g., "The auth subsystem
  and payment pipeline share no code paths and require independent deployment cycles."]

  Boundary rationale:
    {sub-feature-1} | {sub-feature-2}: [Why this is a clean cut point — what the
    interface between them is and why each side is independently specifiable]
    [Add one line per boundary if N > 2]
```

2. Present the proposed split structure **together with the rationale** to the user for confirmation
3. Use AskUserQuestion: "Here's my proposed breakdown and the reasoning behind it. Does this look right, or would you change anything?"
4. If the user wants changes, adjust rationale accordingly and re-confirm
5. Once confirmed, write the manifest to `docs/project-{name}.md`

**Manifest format:**

The file MUST start with a FEATURE_MANIFEST comment block, followed by human-readable content:

```
<!-- FEATURE_MANIFEST
{sub-feature-1}
{sub-feature-2}
{sub-feature-3}
END_MANIFEST -->

# Project: {name}

## Sub-Features

### 1. {sub-feature-1}
- **Description**: {what this sub-feature covers}
- **Dependencies**: {none, or list of sub-feature names it depends on}
- **Scope**: {brief scope summary}

### 2. {sub-feature-2}
- **Description**: ...
- **Dependencies**: ...
- **Scope**: ...

## Execution Order

{Ordered list with dependency and parallelism notes}

## Cross-Cutting Concerns

{Shared data models, conventions, infrastructure, or other things that span multiple sub-features}
```

**FEATURE_MANIFEST rules:**
- **CRITICAL**: Must be the VERY FIRST thing in the file — no YAML front-matter, no headings, no blank lines before the `<!-- FEATURE_MANIFEST` comment. The spec-forge chain parser reads from the top and will fail to recognize the manifest if anything precedes it.
- One sub-feature per line, kebab-case (e.g., `user-auth`, `payment-processing`)
- Names become directory names under `docs/` — each sub-feature gets `docs/{name}/tech-design.md`
- This block is machine-parseable; the rest of the file is for humans

### Step 5: Summary

Display the result:

**If single:**
```
Scope analysis complete: {name}
  Verdict: Single feature
  Next: Running spec chain (Tech Design + Feature Specs)
```

**If multi-split:**
```
Scope analysis complete: {name}
  Verdict: {N} sub-features
  Manifest: docs/project-{name}.md

  Sub-features:
    1. {sub-feature-1} — {one-line description}
    2. {sub-feature-2} — {one-line description}
    ...

  Next: Run the full chain for all sub-features:
    /spec-forge {name}
```
