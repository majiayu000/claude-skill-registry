---
description: Deep audit producing a handoff document to get another agent fully up to speed
---

Please perform a deep audit of our current task to produce a handoff document that gets another agent fully up to speed.

Deliverable:
Create a file named `AUDIT_HANDOFF.md` at the project root.

Document your current understanding of:
- what we are building
- why we are building it
- the project's telos (ultimate purpose/end-state)
- how we are approaching implementation
- what has been completed so far
- how we define and measure success
- current hypotheses
- what is true (with evidence) vs what is assumed
- what might be wrong
- highest-risk areas
- what we just tried and the outcome
- next hypothesis
- open questions

Required Structure (use these exact section headers)

1. `# Executive Summary`
- 5-10 bullets: current project state, trajectory, and key concerns.

2. `# Product Vision and Telos`
- What we are building.
- Why it matters.
- Desired end-state if the project fully succeeds.

3. `# Implementation Approach`
- Architecture and strategy.
- Key technical decisions and tradeoffs.
- Why this approach was chosen over alternatives.

4. `# Progress So Far`
- Completed work.
- In-progress work.
- Deferred/not started work.
- Include concrete references (files, PRs, commits, tests, docs) where possible.

5. `# Success Metrics`
- Define primary and secondary metrics.
- For each metric include: baseline, current value (if known), target, and measurement method.

6. `# Hypotheses`
- Current main hypothesis.
- Supporting sub-hypotheses.
- What would confirm or falsify each one.

7. `# Evidence vs Assumptions`
Include a table with columns:
`Claim | Type (Evidence/Assumption) | Source | Confidence (Low/Med/High) | Notes`

8. `# Failure Modes and Risk Register`
- What could be wrong.
- Highest-risk areas (ranked by impact x likelihood).
- Detection signals and mitigation options for each risk.

9. `# Most Recent Experiment/Attempt`
- What was just tried.
- Expected result.
- Actual result.
- Interpretation.
- Artifacts (logs, test outputs, benchmark data, screenshots, etc.).

10. `# Next Hypothesis and Immediate Plan`
- Next best hypothesis to test.
- Why this is the highest-leverage next step.
- Step-by-step plan for the next iteration.

11. `# Open Questions`
- Unresolved technical, product, and operational questions.
- For each: why it matters, blocking status, and who/what can resolve it.

## Quality Bar

- Clearly separate **facts**, **inferences**, and **assumptions**.
- Prefer concrete evidence over narrative.
- Cite sources directly (file paths, line refs, commands, outputs, tickets, PR links).
- Be explicit about uncertainty and confidence.
- Keep it concise but complete; optimize for fast onboarding and auditability.
