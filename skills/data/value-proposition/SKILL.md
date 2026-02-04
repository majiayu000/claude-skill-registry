---
name: definition.value_proposition
phase: definition
roles:
  - Product Manager
  - Product Marketing
description: Shape the value proposition narrative tying customer needs, solution benefits, and proof points together.
variables:
  required:
    - name: product
      description: Product or feature being positioned.
    - name: target_customer
      description: Persona or segment the value proposition serves.
    - name: core_outcome
      description: Primary outcome or benefit promised to the customer.
  optional:
    - name: differentiators
      description: Key capabilities or enablers that make the solution unique.
    - name: proof_points
      description: Evidence such as metrics, testimonials, or case studies.
outputs:
  - Value proposition statement using problem-solution-benefit framing.
  - Supporting benefit pillars with customer proof.
  - Objection handling and enablement checklist.
---

# Purpose
Provide a consistent artifact to align product and go-to-market teams on what makes the solution compelling for the target customer.

# Pre-run Checklist
- ✅ Validate latest customer insights and market scan outcomes.
- ✅ Align with leadership on the core outcome and product narrative.
- ✅ Gather available proof points or performance data.

# Invocation Guidance
```bash
codex skills run definition.value_proposition \
  --vars "product={{product}}" \
         "target_customer={{target_customer}}" \
         "core_outcome={{core_outcome}}" \
         "differentiators={{differentiators}}" \
         "proof_points={{proof_points}}"
```

# Recommended Input Attachments
- Customer stories or testimonials.
- Competitive positioning artifacts.

# Claude Workflow Outline
1. Summarize the customer problem, desired outcome, and differentiators.
2. Craft a concise value proposition statement following the "For/Who/Our product" format.
3. Generate 3–5 benefit pillars with supporting messages and proof points.
4. List common objections and responses for enablement teams.
5. Recommend next steps for testing and validation with customers.

# Output Template
```
## Value Proposition Statement
For {{target_customer}} who need {{core_outcome}}, {{product}} provides ...

## Benefit Pillars
| Pillar | Customer Benefit | Proof Point | Call-to-Action |
| --- | --- | --- | --- |

## Objection Handling
- Objection:
  - Response:
  - Asset/Owner:
```

# Follow-up Actions
- Share the statement with marketing for messaging alignment.
- Validate language with a subset of customers or prospects.
- Update enablement materials and roadmap priorities accordingly.
