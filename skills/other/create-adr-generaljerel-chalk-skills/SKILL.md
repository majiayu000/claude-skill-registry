---
name: create-adr
description: Create an Architecture Decision Record when the user asks to document a technical decision, record an architecture choice, create an ADR, or explain why a particular approach was chosen
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Write, Grep
argument-hint: "[decision title or question being decided]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: docs, architecture, decisions
---

# Create Architecture Decision Record

## Overview

Create a structured Architecture Decision Record (ADR) following Michael Nygard's format. ADRs capture the context, decision, alternatives considered, and consequences of significant technical choices so future engineers understand *why* something was decided, not just *what* was decided.

## Workflow

1. **Read project context** -- Read `.chalk/docs/engineering/` for existing architecture docs and conventions. Read any existing ADRs to understand prior decisions and link related records.

2. **Determine the next ADR number** -- List files in `.chalk/docs/engineering/` matching the pattern `*_adr_*.md`. Find the highest number and increment by 1. If no ADRs exist, start at `1`.

3. **Clarify the decision** -- From `$ARGUMENTS` and conversation context, identify:
   - The specific technical decision being made (or proposed)
   - The forces and constraints driving the decision
   - The alternatives that were (or should be) considered
   - Ask the user for clarification if the decision scope is ambiguous

4. **Research alternatives** -- If the user hasn't specified alternatives, propose 2-4 reasonable options based on the project context. Every ADR must have at least 2 alternatives considered, including the chosen approach.

5. **Draft the ADR** -- Write the full ADR using the format below. Be concrete and specific. Avoid vague statements like "it depends" or "we'll figure it out later."

6. **Write the file** -- Save to `.chalk/docs/engineering/<n>_adr_<decision_slug>.md`.

7. **Confirm** -- Tell the user the ADR was created with its path, the decision summary, and any related ADRs it links to.

## Filename Convention

```
<number>_adr_<snake_case_decision>.md
```

Examples:
- `3_adr_use_postgres_over_mongodb.md`
- `7_adr_adopt_event_sourcing_for_orders.md`
- `12_adr_migrate_to_monorepo.md`

## ADR Format

```markdown
# ADR-<number>: <Decision Title>

## Status

<Proposed | Accepted | Deprecated | Superseded by [ADR-X](link)>

## Date

<YYYY-MM-DD>

## Context

<Describe the forces at play: technical constraints, business requirements, team capabilities,
timeline pressure, existing system state. Be specific about what problem triggered this decision.
Reference related ADRs if they exist.>

## Decision

<State the decision clearly and concisely. Use active voice: "We will use X" not "X was chosen."
Include enough detail that someone could implement this without further clarification.>

## Alternatives Considered

| Option | Pros | Cons | Why Rejected |
|--------|------|------|--------------|
| <Chosen option> | <pros> | <cons> | **Selected** |
| <Alternative 1> | <pros> | <cons> | <specific reason> |
| <Alternative 2> | <pros> | <cons> | <specific reason> |

## Consequences

### Positive

- <Concrete benefit 1>
- <Concrete benefit 2>

### Negative

- <Concrete tradeoff 1 and how we will mitigate it>
- <Concrete tradeoff 2 and how we will mitigate it>

### Neutral

- <Side effects that are neither good nor bad but worth noting>

## Revisit When

- <Specific trigger condition 1, e.g., "Monthly active users exceed 100k">
- <Specific trigger condition 2, e.g., "The team grows beyond 5 engineers">
- <Specific trigger condition 3, e.g., "Write volume exceeds 10k ops/sec">
```

## Content Guidelines

### Status Values

| Status | When to Use |
|--------|-------------|
| **Proposed** | Decision is open for discussion, not yet committed |
| **Accepted** | Decision has been agreed upon and is in effect |
| **Deprecated** | Decision is no longer relevant (explain why) |
| **Superseded** | Replaced by a newer ADR (link to it) |

### Writing Good Context

The Context section is the most important part of an ADR. It should answer:
- What problem are we solving?
- What constraints exist (technical, business, timeline)?
- What is the current state of the system?
- Who are the stakeholders affected?

A reader 6 months from now should understand the full picture from Context alone.

### Writing Good Alternatives

For each alternative, the "Why Rejected" column must be specific and honest:
- Good: "Query performance degrades below acceptable thresholds at our projected data volume (>50M rows)"
- Bad: "Doesn't meet our needs"
- Good: "Requires team expertise in Rust which we don't have and can't hire for in Q1"
- Bad: "Too complex"

### Writing Revisit Triggers

Revisit triggers should be concrete, measurable conditions -- not vague timeframes:
- Good: "If P95 response time exceeds 500ms under normal load"
- Bad: "If performance becomes a problem"
- Good: "When we add a second product line that needs independent deployment"
- Bad: "When things change"

### Retroactive ADRs

If documenting a decision that was already made, acknowledge this in the Context section: "This ADR documents a decision made on <date> during <context>. It is being recorded retroactively to preserve the reasoning." This is legitimate and valuable -- most teams under-document decisions.

## Linking Related ADRs

When writing a new ADR, check for related existing ADRs:
- Decisions in the same domain (e.g., multiple database-related ADRs)
- Decisions this one depends on or is constrained by
- Decisions this one supersedes

Reference them in the Context section: "This decision builds on [ADR-3: Use PostgreSQL](3_adr_use_postgres.md) which established our primary data store."

## Anti-patterns

- **ADR without alternatives**: Every decision has alternatives, even if one is "do nothing." If you can't think of alternatives, you haven't understood the decision space. Always include at least 2 options in the Alternatives table.
- **Missing consequences**: An ADR that only lists positive consequences is marketing, not engineering. Every decision has tradeoffs. Name the negative consequences explicitly and describe mitigation strategies.
- **Vague rejection reasons**: "Doesn't fit our needs" is not a rejection reason. Be specific about which needs, what measurement, what threshold.
- **Not recording what was rejected**: The rejected alternatives are often more valuable than the chosen one. They prevent future engineers from re-evaluating options that were already considered.
- **Writing ADRs after the fact without acknowledging it**: Retroactive ADRs are fine, but pretending a decision was carefully evaluated when it was actually made under pressure is dishonest. Acknowledge the circumstances.
- **Overloading a single ADR**: One ADR per decision. If you're covering multiple decisions, split them into separate ADRs that reference each other.
- **Status that never updates**: If a decision is superseded, update the old ADR's status to point to the new one. Stale statuses erode trust in the ADR system.
