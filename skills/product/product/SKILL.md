---
name: product
description: Product workflows router. Use when user mentions "PRD", "competitive analysis", "metrics", "OKRs", "cohort", "requirements", or "technical debt". Triggers on product management and strategy tasks.
---

# Product Skill

Router skill for product management workflows. Detects task type and routes to appropriate workflow.

## When This Skill Activates

You're working on:

- Competitive analysis or market positioning
- Product requirements documentation
- Goal setting and metrics definition
- User research synthesis
- Cohort and retention analysis
- PRD quality evaluation
- Technical debt prioritization

## Workflow Selection

Announce which workflow you're using:

| Task Type                                   | Workflow             | Reference                |
| ------------------------------------------- | -------------------- | ------------------------ |
| Competitive analysis, market gaps, win/loss | Competitive Analysis | `references/compete.md`  |
| Feature specs, requirements, MVP scoping    | PRD Generation       | `references/prd.md`      |
| Goals, OKRs, KPIs, tracking systems         | Metrics & Goals      | `references/metrics.md`  |
| User interviews, qualitative data, insights | Research Synthesis   | `references/research.md` |
| Retention, LTV, churn, cohort data          | Cohort Analysis      | `references/cohort.md`   |
| PRD review, completeness check, scoring     | PRD Evaluation       | `references/prd-eval.md` |
| Tech debt triage, remediation planning      | Debt Prioritization  | `references/debt.md`     |

## Related Thinking Tools

From `hope/skills/soul/references/tools/`:

| Tool                                                                                  | When to Use                               |
| ------------------------------------------------------------------------------------- | ----------------------------------------- |
| [Second-Order Thinking](../../hope/skills/soul/references/tools/second-order.md)      | Predict consequences of product decisions |
| [Pre-Mortem](../../hope/skills/soul/references/tools/pre-mortem.md)                   | Anticipate launch failures                |
| [Impact-Effort](../../hope/skills/soul/references/tools/impact-effort.md)             | Focus on high-impact, low-effort features |

From this skill's `references/`:

| Tool                                              | When to Use                             |
| ------------------------------------------------- | --------------------------------------- |
| [Jobs To Be Done](references/jobs-to-be-done.md)  | Understand what customers hire products for |
| [Systems Archetypes](references/systems-archetypes.md) | Recognize "limits to growth", "shifting burden" patterns |

## Usage

1. Detect which workflow applies based on user's task
2. Announce: "I'm using the product skill for [workflow]"
3. Load the appropriate reference file
4. Execute the workflow exactly as written

## Rules

- Use Ask tool to gather input before proceeding
- Ground recommendations in evidence
- Use story points, never time estimates
- Challenge assumptions and cut scope by default
