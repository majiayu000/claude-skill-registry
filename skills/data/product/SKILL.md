---
name: product
description: Product workflows router. Use when validating product ideas, writing specs, analyzing competitors, or tracking metrics. Triggers on "PRD", "competitive analysis", "metrics", "OKRs", "cohort", "requirements", "tech debt", "game-changing features", market positioning, retention analysis, or product strategy tasks.
model: sonnet
allowed-tools: Read
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
- Game-changing feature ideation

## Pre-Work Spec Gate

Before proceeding, score the incoming request (5 dimensions, 0-2 each, max 10):

| Dimension | 0 | 1 | 2 |
|-----------|---|---|---|
| **Problem** | "Make it better" | "Improve onboarding" | "Reduce signup dropout by 20%" |
| **Audience** | None stated | "Our users" | "B2B SaaS teams >50 employees" |
| **Constraints** | None stated | "This quarter" | "No new hires, <$10k budget" |
| **Success** | None stated | "More engagement" | "NPS +10, churn <5%" |
| **Done** | Implied | "When shipped" | "Customer interviews confirm" |

**Decision:**
- **≥8:** Proceed with workflow
- **5-7:** Colleague mode — confirm understanding before analysis
- **<5:** Run `/hope:intent` first — spec too vague

See [fit-decision.md](../../hope/skills/soul/references/fit-decision.md) for full scoring guidance.

## Workflow Selection

Announce which workflow you're using:

| Task Type                                   | Workflow             | Reference                           |
| ------------------------------------------- | -------------------- | ----------------------------------- |
| Competitive analysis, market gaps, win/loss | Competitive Analysis | `references/compete.md`             |
| Feature specs, requirements, MVP scoping    | PRD Generation       | `references/prd.md`                 |
| Goals, OKRs, KPIs, tracking systems         | Metrics & Goals      | `references/metrics.md`             |
| User interviews, qualitative data, insights | Research Synthesis   | `references/research.md`            |
| Retention, LTV, churn, cohort data          | Cohort Analysis      | `references/cohort.md`              |
| PRD review, completeness check, scoring     | PRD Evaluation       | `references/prd-eval.md`            |
| Tech debt triage, remediation planning      | Debt Prioritization  | `references/debt.md`                |
| Breakthrough features, innovation ideation  | Game-Changing Features | `references/game-changing-features.md` |
| TAM/SAM/SOM, market opportunity sizing      | Market Sizing        | `references/market-sizing.md`       |
| A/B tests, controlled experiments           | Experimentation      | `references/experimentation.md`     |

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
4. Execute the workflow with confirmation gates (see below)

## Confirmation Gates

Multi-step workflows pause at checkpoints to prevent wasted work when intent drifts.

**Gate Points:**

| Phase | Gate |
|-------|------|
| After research/discovery | ⚠️ CHECKPOINT: "Does this understanding match your intent?" |
| After approach selection | ⚠️ CHECKPOINT: "Here's my proposed approach. Should I proceed?" |
| Before final artifact | ⚠️ CHECKPOINT: "Ready to generate final output. Confirm?" |

**Skip gates:** Say "proceed without confirmation" to run uninterrupted.

**In workflows:** Each reference file should pause at these points:

```
### Phase 2: Analysis

[... phase content ...]

⚠️ **CHECKPOINT**: Present findings summary. Ask: "Does this capture the key insights? Any adjustments before I continue?"
```

## Rules

- Use Ask tool to gather input before proceeding
- Ground recommendations in evidence
- Use story points, never time estimates
- Challenge assumptions and cut scope by default
- **Quality footer required** after each workflow completes — see [quality-footer.md](../../hope/skills/soul/references/quality-footer.md)

---

## Boundary

**Product intuition is yours. Claude structures, not strategizes.**

- Analysis surfaces patterns in data; user decides meaning
- Recommendations are hypotheses, not directives
- Market insights are inferences, not facts — always confidence-tagged

Product skill organizes thinking. Business judgment remains human.
