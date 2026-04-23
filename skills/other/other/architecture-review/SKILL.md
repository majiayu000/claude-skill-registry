---
name: architecture-review
description: 'Assess architecture decisions, ADR compliance, coupling analysis, and design principles'
version: 1.9.0
alwaysApply: false
category: architecture
tags:
- architecture
- design
- adr
- coupling
- patterns
- principles
tools:
- adr-auditor
- coupling-analyzer
- principle-checker
usage_patterns:
- architecture-assessment
- adr-audit
- refactor-review
- design-validation
complexity: advanced
model_hint: deep
estimated_tokens: 300
progressive_loading: true
dependencies:
- pensive:shared
- imbue:proof-of-work
- imbue:diff-analysis/modules/risk-assessment-framework
modules:
- modules/adr-audit.md
- modules/coupling-analysis.md
- modules/principle-checks.md
- modules/fpf-methodology.md
---
## Table of Contents

- [Quick Start](#quick-start)
- [When to Use](#when-to-use)
- [Progressive Loading](#progressive-loading)
- [Required TodoWrite Items](#required-todowrite-items)
- [Workflow](#workflow)
- [Step 1: Establish Context (`arch-review:context-established`)](#step-1:-establish-context-(arch-review:context-established))
- [Step 2: ADR Audit (`arch-review:adr-audit`)](#step-2:-adr-audit-(arch-review:adr-audit))
- [Step 3: Interaction Mapping (`arch-review:interaction-mapping`)](#step-3:-interaction-mapping-(arch-review:interaction-mapping))
- [Step 4: Principle Checks (`arch-review:principle-checks`)](#step-4:-principle-checks-(arch-review:principle-checks))
- [Step 5: Risks and Actions (`arch-review:risks-actions`)](#step-5:-risks-and-actions-(arch-review:risks-actions))
- [Testing](#testing)

## Testing

Run `pytest plugins/pensive/tests/skills/test_architecture_review.py` to verify review logic.
- [Architecture Principles Checklist](#architecture-principles-checklist)
- [Coupling](#coupling)
- [Cohesion](#cohesion)
- [Layering](#layering)
- [Evolution](#evolution)


# Architecture Review Workflow

Architecture assessment against ADRs and design principles.

## Quick Start

```bash
/architecture-review
```

## When To Use

- Approving reimplementations.
- Large-scale refactoring reviews.
- System design changes.
- New module/service introduction.
- Dependency restructuring.

## When NOT To Use

- Selecting architecture paradigms - use archetypes
  skills
- API surface review - use api-review
- Selecting architecture paradigms - use archetypes
  skills
- API surface review - use api-review

## Progressive Loading

Load modules based on review scope:

- **`modules/adr-audit.md`** (~400 tokens): ADR verification and documentation.
- **`modules/coupling-analysis.md`** (~450 tokens): Dependency analysis and boundary violations.
- **`modules/principle-checks.md`** (~500 tokens): Code quality, security, and performance.
- **`modules/fpf-methodology.md`** (~800 tokens): FPF (Functional, Practical, Foundation) multi-perspective review methodology.

Load all modules for full reviews. For focused reviews, load only relevant modules.

## Required TodoWrite Items

1. `arch-review:context-established`: Repository, branch, motivation.
2. `arch-review:adr-audit`: ADR verification and new ADR needs.
3. `arch-review:interaction-mapping`: Module coupling analysis.
4. `arch-review:invariant-check`: Invariant conflict detection and 3-option analysis.
5. `arch-review:principle-checks`: LoD, security, performance.
6. `arch-review:risks-actions`: Recommendation and follow-ups.

## Workflow

### Step 1: Establish Context (`arch-review:context-established`)

Confirm repository and branch:
```bash
pwd
git status -sb
```

Document:
- Feature/bug/epic motivating review.
- Affected subsystems.
- Architectural intent from README/docs.
- Design trade-off assumptions.

### Step 2: ADR Audit (`arch-review:adr-audit`)

**Load: `modules/adr-audit.md`**

- Locate ADRs in project.
- Verify required sections.
- Check status flow.
- Confirm immutability compliance.
- Flag need for new ADRs.

### Step 3: Interaction Mapping (`arch-review:interaction-mapping`)

**Load: `modules/coupling-analysis.md`**

- Diagram before/after module interactions.
- Verify composition boundaries.
- Check data ownership clarity.
- Validate dependency flow direction.
- Identify coupling violations.

### Step 3.5: Invariant Conflict Detection (`arch-review:invariant-check`)

Before checking principles, identify whether the changes
conflict with existing design invariants. This is the
highest-judgment step in architecture review — models
get this wrong more often than any other call.

**Identify existing invariants:**

1. Scan ADRs for recorded decisions still in "accepted"
   status
2. Check module boundaries (are imports crossing layers
   that previously didn't?)
3. Check data flow direction (does data now flow in a
   new direction?)
4. Check API contracts (are public interfaces changing
   shape?)
5. Check structural patterns (is a new pattern being
   introduced alongside an existing one?)

```bash
# Detect boundary crossings in changed files
git diff --name-only | while read f; do
  head -20 "$f" 2>/dev/null | rg "^(import|from|use |require)" || true
done
```

**When a conflict is detected:**

Do NOT recommend a resolution. Present the three options
and escalate to human judgment:

| Option | When Right | When Wrong |
|--------|------------|------------|
| **Preserve invariant** (reject feature) | Invariant simplifies many things; feature is marginal | Feature is genuinely needed and invariant is stale |
| **Layer on top** (add inelegantly) | Feature is needed; invariant still valuable; imperfection is OK | Layering creates a maintenance trap that will compound |
| **Revise invariant** (change the design) | Genuine new learning invalidates the original reasoning | You're "cleaning up" a decision you don't fully understand |

**Output format:**

```markdown
### Invariant Conflicts

[I1] **[Invariant name]** — [what decision it represents]
- **Conflict**: [what change clashes]
- **Options**: Preserve / Layer / Revise
- **Recommendation**: ESCALATE TO HUMAN
- **Risk if wrong**: [what compounds]
```

**Why this matters:** Bad invariant decisions compound.
After a few wrong calls the codebase becomes
unsalvageable. This is a judgment problem, not a context
problem — the agent should surface it, not solve it.

### Step 4: Principle Checks (`arch-review:principle-checks`)

**Load: `modules/principle-checks.md`**

- Law of Demeter.
- Anti-slop patterns.
- Security (input validation, least privilege).
- Performance (N+1 queries, caching).

### Step 5: Risks and Actions (`arch-review:risks-actions`)

Summarize using `imbue:diff-analysis/modules/risk-assessment-framework`:
- Current vs proposed architecture.
- Business impact.
- Technical debt implications.

List follow-ups with owners and dates.

Provide recommendation:
- **Approve**: Architecture sound.
- **Approve with actions**: Minor issues to address.
- **Block**: Fundamental problems requiring redesign.

## Architecture Principles Checklist

### Coupling
- [ ] Dependencies follow defined boundaries.
- [ ] No circular dependencies.
- [ ] Extension points used properly.
- [ ] Abstractions don't leak.

### Cohesion
- [ ] Related functionality grouped.
- [ ] Single responsibility per module.
- [ ] Clear module purposes.

### Layering
- [ ] Layers have clear responsibilities.
- [ ] Dependencies flow downward.
- [ ] No layer bypassing.

### Invariants
- [ ] Existing design invariants identified.
- [ ] Conflicts between changes and invariants surfaced.
- [ ] Three-option analysis (preserve/layer/revise) presented.
- [ ] Invariant changes escalated to human judgment.
- [ ] No silent invariant revisions in the diff.

### Evolution
- [ ] Changes are reversible.
- [ ] Migration paths are clear.
- [ ] ADRs document decisions.
