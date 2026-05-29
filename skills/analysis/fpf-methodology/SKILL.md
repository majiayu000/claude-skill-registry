---
name: fpf-methodology
description: First Principles Framework (FPF) for structured, auditable reasoning.

summary: |
  - Cycle: Abduction → Deduction → Induction (Hypothesis → Logic → Evidence)
  - Commands: /q0-init → /q1-hypothesize → /q2-verify → /q3-validate → /q5-decide
  - Output: Design Rationale Records (DRRs) for auditable decisions
  - Use for: Architectural decisions, complex problems, team discussions
  - Skip for: Quick fixes, obvious solutions, time-critical issues

context_cost: medium
load_when:
  - 'structured reasoning'
  - 'architectural decision'
  - 'design rationale'
  - 'hypothesis'
  - 'first principles'

enhances:
  - software-architecture
  - api-design-principles
---

# First Principles Framework (FPF)

Structured reasoning for AI coding tools — make better decisions, remember why you made them.

## When to Use This Skill

**Activate FPF for:**

- Architectural decisions with long-term consequences
- Multiple viable approaches requiring systematic evaluation
- Need auditable reasoning trail for team/future reference
- Complex problems requiring hypothesis → verification cycle
- Building up project knowledge base over time

**Skip FPF for:**

- Quick fixes, obvious solutions
- Easily reversible decisions
- Time-critical situations where overhead isn't justified

## Core Concept

The core cycle follows three modes of inference:

1. **Abduction** — Generate competing hypotheses (don't anchor on the first idea)
2. **Deduction** — Verify logic and constraints (does the idea make sense?)
3. **Induction** — Gather evidence through tests or research (does the idea work in reality?)

Then, audit for bias, decide, and document the rationale in a durable record.

## Assurance Levels

Knowledge claims are tracked at different assurance levels:

| Level       | Name        | Description                          |
| ----------- | ----------- | ------------------------------------ |
| **L0**      | Observation | Unverified hypothesis or note        |
| **L1**      | Reasoned    | Passed logical consistency check     |
| **L2**      | Verified    | Empirically tested and confirmed     |
| **Invalid** | Disproved   | Disproved claims (kept for learning) |

## Commands

Use the following slash commands in order:

| #   | Command           | Phase      | What it does                                   |
| --- | ----------------- | ---------- | ---------------------------------------------- |
| 0   | `/q0-init`        | Setup      | Initialize `.quint/` structure                 |
| 1   | `/q1-hypothesize` | Abduction  | Generate hypotheses → `L0/`                    |
| 1b  | `/q1-add`         | Abduction  | Inject user hypothesis → `L0/`                 |
| 2   | `/q2-verify`      | Deduction  | Logical verification → `L1/`                   |
| 3   | `/q3-validate`    | Induction  | Test (internal) or Research (external) → `L2/` |
| 4   | `/q4-audit`       | Bias-Audit | WLNK analysis, congruence check                |
| 5   | `/q5-decide`      | Decision   | Create DRR from winning hypothesis             |
| S   | `/q-status`       | —          | Show current state and next steps              |
| Q   | `/q-query`        | —          | Search knowledge base                          |
| D   | `/q-decay`        | —          | Check evidence freshness                       |

## Key Concepts

### WLNK (Weakest Link)

Assurance = min(evidence), never average. A chain is only as strong as its weakest link.

### Congruence

External evidence must match our context (high/medium/low). Evidence from a different context may not apply.

### Validity

Evidence expires — check with `/q-decay`. Stale evidence creates epistemic debt.

### Scope

Knowledge applies within specified conditions only. Document the boundaries.

## Workflow Example

```
User: How should we implement caching for our API?

/q0-init                           # Initialize knowledge base
/q1-hypothesize "API caching"      # Generate hypotheses

Hypotheses generated:
- H1: Redis with TTL-based invalidation (Conservative)
- H2: CDN edge caching (Novel)
- H3: In-memory cache with pub/sub invalidation (Hybrid)

/q2-verify H1                      # Verify Redis approach logic
/q3-validate H1                    # Test Redis in development

/q4-audit                          # Check for biases, weakest links
/q5-decide H1                      # Create Design Rationale Record
```

## Design Rationale Record (DRR)

The `/q5-decide` command generates a DRR with:

- **Context**: The initial problem
- **Decision**: The chosen hypothesis
- **Rationale**: Why it won (citing evidence and R_eff)
- **Consequences**: Trade-offs and next steps
- **Validity**: When should this be revisited?

## State Location

All FPF state is stored in `.quint/` directory (git-tracked):

```
.quint/
├── context.md           # Project context and constraints
├── knowledge/
│   ├── L0/              # Unverified hypotheses
│   ├── L1/              # Logically verified claims
│   ├── L2/              # Empirically verified claims
│   └── invalid/         # Disproved claims
└── decisions/           # Design Rationale Records
```

## Transformer Mandate

**Critical Principle:** You (Claude) generate options with evidence. Human decides.

A system cannot transform itself — the human partner makes final architectural decisions. Generate high-quality options, present evidence, but don't autonomously choose major architectural directions.

## Integration with Code Review

After FPF-driven implementation:

1. Generate hypotheses for approach
2. Verify and validate the chosen approach
3. Implement with the structured reasoning as documentation
4. Code review references the DRR for context
5. Future developers understand _why_ decisions were made

## Benefits

- **Auditability**: Every decision has a documented trail
- **Reduced Bias**: Multiple hypotheses prevent anchoring
- **Knowledge Retention**: Project learnings persist
- **Team Alignment**: Clear rationale for decisions
- **Technical Debt Prevention**: Bad decisions caught early
