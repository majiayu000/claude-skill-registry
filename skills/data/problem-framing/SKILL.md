---
name: discovery.problem_framing
phase: discovery
roles:
  - Product Manager
description: Frame the core customer problem, evidence, and success hypothesis before solutioning.
variables:
  required:
    - name: product
      description: Product, program, or initiative under assessment.
    - name: segment
      description: Target customer segment or persona focus.
    - name: evidence_sources
      description: Primary sources backing the problem statement (e.g., interviews, surveys).
  optional:
    - name: timeframe
      description: Planning horizon for the problem framing, such as Q3 or "next release".
outputs:
  - Problem statement and context bullet list.
  - Evidence summary table tying sources to insights.
  - Success hypothesis, leading indicators, and guardrails.
---

# Purpose
Equip product managers with a repeatable prompt that validates the customer problem, supporting evidence, and desired outcomes before discovery work begins.

# Pre-run Checklist
- ✅ Confirm discovery inputs are synthesized from recent research.
- ✅ Align with design and analytics on the persona focus.
- ✅ Clarify any known constraints that must be honored.

# Invocation Guidance
```bash
codex skills run discovery.problem_framing \
  --vars "product={{product}}" \
         "segment={{segment}}" \
         "evidence_sources={{evidence_sources}}" \
         "timeframe={{timeframe}}"
```

# Recommended Input Attachments
- Recent interview transcripts (`research/interviews/*.md`).
- Market or usage dashboards highlighting severity of the problem.

# Claude Workflow Outline
1. Restate the core product charter for the provided segment and timeframe.
2. Build a concise problem statement that references the evidence sources explicitly.
3. Map supporting insights into a table with columns for Source, Key Quote/Signal, Confidence, and Relevance.
4. Draft a success hypothesis including leading metrics, anti-goals, and scope boundaries.
5. Provide alignment questions to take to partner roles (design, engineering, analytics).

# Output Template
```
## Problem Statement
<2-3 sentence articulation>

## Evidence Summary
| Source | Insight | Confidence | Relevance |
| --- | --- | --- | --- |
| {{source}} | {{insight}} | {{confidence}} | {{relevance}} |

## Success Hypothesis
- Leading metric:
- Guardrails:
- Key assumptions to validate:

## Next Alignment Questions
1. ...
2. ...
```

# Follow-up Actions
- Capture open questions in your product backlog with owners and due dates.
- Schedule a triad review with design and engineering to refine the hypothesis.
- Update the discovery tracker once alignment is achieved.
