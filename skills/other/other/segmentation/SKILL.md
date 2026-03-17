---
name: segmentation
description: Use when designing filters, suppression logic, and personalization cohorts
  for campaigns or automations.
---

# Advanced Segmentation Playbooks

## When to Use
- Planning campaigns requiring persona, lifecycle, or behavioral splits.
- Creating suppression logic to protect deliverability and compliance.
- Building engagement tiers for experimentation and reporting.

## Framework
1. **Lifecycle Grid** – axis of lifecycle stage vs engagement level.
2. **Data Integrity** – confirm consent, field completeness, and recency.
3. **Priority Scoring** – route high-value segments to premium workflows.

## Checklist
- ✅ Primary filter (persona, stage, product usage)
- ✅ Secondary filters (intent, region, business size)
- ✅ Suppress: unsubscribed, bounced, low engagement, legal blocks
- ✅ Personalization fields: {{first_name}}, {{company}}, dynamic modules

## Templates
- **Segmentation Matrix**: See `assets/segmentation_matrix.md` for tier definitions and logic examples.
- **Launch Tiering** – VIP, Prospects, Dormant with separate cadence and pacing table.
- **Signal-Driven** – product milestones trigger micro-segments; includes trigger → audience matrix.
- **Compliance Safe** – CASL/GDPR consent matrix + suppression filters by region.

## Tips
- Keep segment definitions in a shared schema doc for consistency.
- Use dashboards to monitor size changes week over week.
- Pair segmentation with A/B testing to validate hypotheses.

