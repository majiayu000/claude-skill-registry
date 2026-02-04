---
name: discovery.tech_landscape
phase: discovery
roles:
  - Engineering Lead
  - Solution Architect
description: Assess technical patterns, integrations, and constraints in the domain to inform feasibility and strategy.
variables:
  required:
    - name: domain
      description: Product or problem domain to investigate.
    - name: constraints
      description: Compliance, performance, or architectural constraints that must be respected.
  optional:
    - name: existing_stack
      description: Summary of current systems or technologies in place.
    - name: partnership_targets
      description: Potential vendors or platforms to evaluate for integration.
outputs:
  - Overview of domain-specific architectural trends.
  - Integration and dependency analysis with risk ratings.
  - Recommendation backlog for spikes or proof-of-concepts.
---

# Purpose
Help engineering leadership quickly synthesize domain research into actionable technical exploration tasks during discovery.

# Pre-run Checklist
- ✅ Align with security, platform, and data stakeholders on non-negotiable constraints.
- ✅ Gather existing architecture diagrams and system inventories.
- ✅ Clarify the decision timeline for selecting technologies.

# Invocation Guidance
```bash
codex skills run discovery.tech_landscape \
  --vars "domain={{domain}}" \
         "constraints={{constraints}}" \
         "existing_stack={{existing_stack}}" \
         "partnership_targets={{partnership_targets}}"
```

# Recommended Input Attachments
- Current architecture diagrams.
- Procurement or compliance requirements.
- Vendor documentation links.

# Claude Workflow Outline
1. Outline the domain context and key constraints.
2. Summarize prevailing architecture patterns, tooling, and best practices.
3. Evaluate integration options, highlighting trade-offs and implementation complexity.
4. Flag high-risk areas requiring spikes or proof-of-concepts.
5. Produce a recommended investigation backlog with owners and timelines.

# Output Template
```
## Domain Overview
...

## Architecture & Pattern Insights
- Trend:
- Impact:

## Integration Considerations
| Option | Benefits | Risks | Effort | Recommendation |
| --- | --- | --- | --- | --- |

## Recommended Spikes
1. Spike Title — Owner (Timeline)
   - Goal:
   - Deliverables:
```

# Follow-up Actions
- Create engineering exploration tickets based on recommended spikes.
- Socialize findings with the product trio to refine scope and timeline.
- Update the architectural decision log once selections are made.
