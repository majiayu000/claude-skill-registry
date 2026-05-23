---
name: discovery.market_scan
phase: discovery
roles:
  - Product Manager
  - Product Marketing
description: Analyze the competitive and adjacent solution landscape to surface differentiation opportunities.
variables:
  required:
    - name: product
      description: Name of the product or initiative you are positioning.
    - name: segment
      description: Target customer or market segment to assess.
    - name: competitors
      description: Comma-separated list of competitor or alternative solutions.
  optional:
    - name: evaluation_criteria
      description: Dimensions to compare, e.g., pricing, integrations, compliance.
    - name: timeframe
      description: Time horizon for the analysis (e.g., FY25).
outputs:
  - Competitive comparison matrix with key differentiators.
  - Opportunity summary and product positioning angles.
  - Risk register noting threats and mitigation ideas.
---

# Purpose
Equip go-to-market and product leads with a structured competitive analysis that highlights how Claude can support subsequent positioning decisions.

# Pre-run Checklist
- ✅ Validate the competitor list with marketing and sales enablement.
- ✅ Gather any pricing sheets, analyst reports, or customer feedback references.
- ✅ Align on evaluation criteria before invoking the skill.

# Invocation Guidance
```bash
codex skills run discovery.market_scan \
  --vars "product={{product}}" \
         "segment={{segment}}" \
         "competitors={{competitors}}" \
         "evaluation_criteria={{evaluation_criteria}}" \
         "timeframe={{timeframe}}"
```

# Recommended Input Attachments
- Links or documents containing competitor feature sets.
- Customer interviews referencing competitor strengths and weaknesses.

# Claude Workflow Outline
1. Summarize the segment context and the role of your product.
2. Build a table comparing each competitor against the evaluation criteria with notes on strengths and gaps.
3. Highlight differentiation opportunities and suggested win themes for positioning.
4. Identify potential risks or threats that require monitoring, including trigger signals.
5. Recommend follow-up analyses or validations.

# Output Template
```
## Competitive Landscape Overview
<Overview paragraph>

## Comparison Matrix
| Criteria | {{competitor_1}} | {{competitor_2}} | {{product}} Advantage |
| --- | --- | --- | --- |

## Differentiation Opportunities
1. ...
2. ...

## Risks & Mitigations
| Risk | Trigger | Impact | Mitigation |
| --- | --- | --- | --- |
```

# Follow-up Actions
- Align with product marketing on messaging updates.
- Feed insights into roadmap prioritization and customer storytelling.
- Schedule quarterly refreshes to keep the landscape current.
