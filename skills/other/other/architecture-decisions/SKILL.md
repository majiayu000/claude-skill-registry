---
name: architecture-decisions
description: >-
  Architecture Decision Records and living architecture documentation.
  Activate when making technology choices, defining system boundaries,
  recording architectural decisions, or creating/updating ARCHITECTURE.md.
  Covers ADR format, decision governance, design facilitation, and
  architectural review.
license: CC0-1.0
metadata:
  author: jwilger
  version: "1.0"
  requires: []
  context: [architecture-decisions, event-model, source-files]
  phase: decide
  standalone: true
---

# Architecture Decisions

**Value:** Communication -- architecture decisions recorded before
implementation ensure every contributor (human or agent) understands why
the system is shaped the way it is. Decisions made in silence are decisions
lost.

## Purpose

Teaches the agent to record architecture decisions before implementing them,
maintain a living architecture document, and facilitate structured decision-making.
Prevents the common failure mode where architecture emerges accidentally and
rationale is lost.

## Practices

### Record Decisions Before Implementation

Never implement a structural change without first recording the decision. An
architecture decision is any choice that affects system structure, technology
stack, domain boundaries, integration patterns, or cross-cutting concerns.

1. Identify the decision: what problem motivates this choice?
2. Document alternatives: at least two realistic options with tradeoffs
3. Record the chosen approach and its consequences
4. Only then proceed to implementation

**Do:**
- Record decisions when they are made, while context is fresh
- One decision per record -- keep them atomic
- State decisions in active voice: "We will use PostgreSQL for event storage"
- Acknowledge negative consequences honestly

**Do not:**
- Document decisions after implementation as retroactive justification
- Bundle multiple decisions into one record
- Omit alternatives -- a decision without alternatives is not a decision

### Maintain the Living Architecture Document

`docs/ARCHITECTURE.md` is the single authoritative source for current system
architecture. It describes WHAT the architecture IS, not WHY it became that way
(the WHY lives in decision records).

Structure:

```markdown
# Architecture

## Overview
High-level system description

## Key Decisions
Current architectural choices (link to decision records)

## Components
Major system components and their responsibilities

## Patterns
Patterns in use (event sourcing, CQRS, etc.)

## Constraints
Current constraints and known tradeoffs
```

Update this document whenever a decision changes the architecture. Keep it
current -- a stale architecture document is worse than none.

### Use ADR-as-PR Format

When the project uses GitHub, architecture decision records live as PR
descriptions, not standalone files. This gives decisions a natural lifecycle:

- **Open PR** = proposed decision, under review
- **Merged PR** = accepted decision
- **Closed PR** = rejected decision
- **New PR with "Supersedes #N"** = revised decision

Each ADR PR:
1. Branches independently from main (`adr/<slug>`)
2. Updates `docs/ARCHITECTURE.md` with the current decision
3. Uses the PR description as the full decision record (see `references/adr-template.md`)
4. Gets labeled `adr` for discoverability

When GitHub PRs are not available, record the architecture decision in
the commit message of the commit that updates `docs/ARCHITECTURE.md`.
Use the same template structure (Context, Decision, Alternatives,
Consequences). The commit message becomes the decision record, and
`git log -- docs/ARCHITECTURE.md` becomes the decision history.

### Facilitate Decisions Systematically

When multiple architectural decisions are needed (new project, major redesign):

1. **Inventory decision points** across categories: technology stack, domain
   boundaries, integration patterns, cross-cutting concerns
2. **Present the agenda** to the human for review before facilitating
3. **For each decision**: present context, present 2-4 options with tradeoffs,
   let the human choose, record immediately
4. **Never batch** -- record each decision individually so they can be reviewed
   and accepted independently

### Review for Architectural Alignment

Before approving implementation work, verify it aligns with documented
architecture:

- Does it follow patterns documented in ARCHITECTURE.md?
- Does it respect domain boundaries?
- Does it introduce new dependencies or patterns not yet decided?
- If it conflicts, record a new decision before proceeding

## Enforcement Note

This skill provides advisory guidance. It instructs the agent to record
decisions before implementation but cannot mechanically prevent implementation
without a decision record. On harnesses with plugin support, enforcement hooks
can block implementation PRs that lack corresponding ADR references. On other
harnesses, the agent follows these practices by convention. For available
enforcement plugins, see the
[Harness Plugin Availability](../../README.md#harness-plugin-availability) table.

## Verification

After completing work guided by this skill, verify:

- [ ] Every structural change has a corresponding decision record
- [ ] `docs/ARCHITECTURE.md` reflects the current architecture
- [ ] Each decision record states context, alternatives, and consequences
- [ ] No decision was recorded retroactively after implementation
- [ ] Decision records are atomic (one decision per record)

If any criterion is not met, record the missing decision before proceeding.

## Dependencies

This skill works standalone. For enhanced workflows, it integrates with:

- **event-modeling:** Completed event models surface the decision points that
  need architectural choices (technology, boundaries, integration patterns)
- **domain-modeling:** Domain model constraints inform bounded context
  boundaries and aggregate design decisions
- **code-review:** Reviewers verify implementation aligns with documented
  architecture decisions

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill event-modeling
```
