---
name: data-governance
description: Use when defining data contracts, consent policies, and monitoring for
  automation programs.
---

# Automation Data Governance Skill

## When to Use
- Launching new journeys requiring cross-system data sharing.
- Auditing consent/suppression logic across email/SMS/in-app.
- Investigating data quality incidents impacting automation.

## Framework
1. **Data Contracts** – document required fields/events, owners, freshness SLAs, fallback behavior.
2. **Consent & Compliance** – track opt-in types, regional consent, TTL, audit trails.
3. **Identity Resolution** – ensure consistent IDs across product, CRM, MAP, CDP.
4. **Monitoring** – dashboards/alerts for data latency, schema changes, null spikes.
5. **Change Management** – versioning, rollback, and communication paths.

## Templates
- Data requirements matrix (journey → fields/events → source → owner → SLA).
- Consent policy doc (channel, region, legal basis, suppression rules).
- Incident log + RCA template.

## Tips
- Set automated kill switches when critical fields are stale or missing.
- Collaborate with security/legal on retention + privacy impact assessments.
- Align governance cadences with quarterly automation retros.

---
