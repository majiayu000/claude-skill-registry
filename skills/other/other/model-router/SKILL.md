---
name: model-router
description: Route work to the cheapest model tier that can reliably complete it.
Use when: (1) choosing a model for a task, (2) deciding model level for sub-agents,
(3) escalating after a failed attempt, (4) avoiding premium-model overuse on routine work.

category: principles
user-invocable: true
---

# Model Router

Choose model tier by task complexity. Keep routine work cheap. Escalate only when required.

## Core Policy

- Classify each task first: `ROUTINE`, `MODERATE`, or `COMPLEX`.
- Start with the lowest tier that can succeed.
- Escalate one tier after a quality failure.
- Keep sub-agents on the cheapest viable tier by default.

## Task Classification

### ROUTINE

Use lowest-cost tier.

Signals:
- File reads/writes
- Status checks and health checks
- Deterministic formatting/transformations
- Bulk fetch/lookup tasks with clear success criteria

### MODERATE

Use mid-tier.

Signals:
- Multi-step synthesis
- Standard code generation/refactoring
- Non-trivial summaries
- Typical implementation tasks with known patterns

### COMPLEX

Use top-tier.

Signals:
- Ambiguous requirements
- Novel debugging/root-cause analysis
- Architecture tradeoffs
- Security-sensitive reasoning
- Repeated failure on lower tiers

## Escalation And De-escalation

- Escalate when output quality is insufficient for the task goal.
- Escalate one tier at a time.
- De-escalate when work returns to deterministic or repetitive operations.
- Document escalation reason in one sentence before switching tiers.

## Sub-Agent Rules

- Default sub-agents to the cheapest tier that matches task class.
- Reserve high-tier sub-agents for clearly complex reasoning only.
- If parent agent is high-tier, do not inherit that tier by default.

## Anti-Patterns

- Premium tier for file I/O or status checks.
- Premium tier for repetitive extraction and formatting.
- Immediate jump from lowest tier to highest tier without justification.
- Leaving routine follow-up tasks on high tier after a complex step is complete.

## Quick Decision Flow

1. Classify task complexity.
2. Pick the lowest viable tier.
3. Run and evaluate output quality.
4. Escalate one tier only if needed.
5. De-escalate for routine follow-up.