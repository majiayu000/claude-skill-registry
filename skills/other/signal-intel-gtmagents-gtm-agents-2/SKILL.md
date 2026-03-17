---
name: signal-intel
description: Use when consolidating intent, product usage, and third-party signals
  to prioritize ABM actions.
---

# Signal Intelligence Systems Skill

## When to Use
- Monitoring account readiness for ABM plays.
- Prioritizing SDR/AE follow-up based on live engagement.
- Coordinating signal-based automations (ads suppression, nurture routing, sales alerts).

## Signal Sources
1. **Intent Platforms** – Bombora, 6sense, ZoomInfo (topics, spike scores, recency).
2. **Product Usage** – PQL metrics, feature adoption, seat utilization, idle license detection.
3. **Engagement** – email/web activity, event attendance, community participation, SDR/AE touchpoints.
4. **Commercial** – opp stages, renewal windows, open tickets, expansion likelihood.
5. **External Events** – hiring, funding, tech stack changes, executive moves, news.

## Framework
1. Normalize identifiers (domain, account ID) across sources.
2. Define scoring rules per signal category with decay functions.
3. Build alerts/automations (Slack, email, CRM tasks, MAP triggers).
4. Feed prioritized lists into plays (target-accounts, plan-plays, monitor-abm).
5. Log outcomes to refine weighting and ROI.

## Templates
- Signal scoring worksheet (source, weight, freshness, trigger threshold).
- Alert matrix (signal → delivery channel → owner → SLA).
- Data dictionary for dashboards/warehouse models.

## Tips
- Combine at least two signal types before triggering high-effort plays.
- Store historical signal snapshots to correlate with pipeline impact.
- Align privacy/compliance flags with marketing automation + CRM suppression rules.

---
