---
name: faion-gtm-manifest
description: "GTM Manifest from research data. Triggers: gtm, go-to-market, launch strategy."
user-invocable: false
allowed-tools: Read, Write, Glob, Task, AskUserQuestion, TodoWrite
---

# GTM Manifest Orchestrator

**Communication: User's language. Docs: English.**

## Prerequisites

Requires completed research in `product_docs/`:
- market-research.md
- competitive-analysis.md
- user-personas.md
- pricing-research.md

If missing → run `faion-product-research` first.

## Workflow

```
1. Read product research docs
2. AskUserQuestion: sales model, timeline
3. Generate 12 sections sequentially
4. Combine into gtm-manifest-full.md
```

## Output

```
product_docs/gtm-manifest/
├── 01-executive-summary.md
├── 02-market-context.md
├── 03-icp.md
├── 04-value-proposition.md
├── 05-positioning.md
├── 06-messaging-framework.md
├── 07-pricing-packaging.md
├── 08-sales-model.md
├── 09-marketing-channels.md
├── 10-launch-plan.md
├── 11-success-metrics.md
├── 12-risks-mitigations.md
└── gtm-manifest-full.md
```

## Sections

| # | Section | Key Content |
|---|---------|-------------|
| 01 | Executive Summary | Vision, market opportunity, strategy |
| 02 | Market Context | TAM/SAM/SOM, trends from research |
| 03 | ICP | Ideal Customer Profile from personas |
| 04 | Value Proposition | Core benefits, differentiation |
| 05 | Positioning | vs competitors, unique angle |
| 06 | Messaging | Headlines, taglines, key messages |
| 07 | Pricing | Tiers, packaging from research |
| 08 | Sales Model | PLG/Sales-led/Hybrid |
| 09 | Channels | Marketing channels, priorities |
| 10 | Launch Plan | Timeline, milestones |
| 11 | Metrics | KPIs, success criteria |
| 12 | Risks | Risks and mitigations |

## Strategy Questions

```python
AskUserQuestion(
    questions=[
        {
            "question": "Sales model?",
            "options": [
                {"label": "PLG", "description": "Product-Led Growth"},
                {"label": "Sales-Led", "description": "Enterprise sales"},
                {"label": "Hybrid", "description": "PLG + Sales"}
            ]
        },
        {
            "question": "Launch timeline?",
            "options": [
                {"label": "MVP", "description": "3-6 months"},
                {"label": "Full", "description": "6-12 months"}
            ]
        }
    ]
)
```

## Execution

For each section, use Task with general-purpose agent:

```python
for section in SECTIONS:
    Task(
        subagent_type="general-purpose",
        prompt=f"""
PROJECT: {project}
SECTION: {section.name}
RESEARCH: {research_data}
OUTPUT: product_docs/gtm-manifest/{section.file}

Write {section.name} section using research data.
Follow standard GTM format.
"""
    )
```

## Final Merge

```python
# Combine all sections
sections = sorted(glob("product_docs/gtm-manifest/*.md"))
full_content = "\n\n---\n\n".join([read(s) for s in sections])
write("product_docs/gtm-manifest/gtm-manifest-full.md", full_content)
```
