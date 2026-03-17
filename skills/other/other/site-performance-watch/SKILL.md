---
name: site-performance-watch
description: Monitoring and alerting framework for ecommerce site speed, errors, and
  uptime.
---

# Site Performance Watch Skill

## When to Use
- Setting up proactive monitoring during campaigns or launches.
- Investigating conversion drops tied to latency or availability issues.
- Communicating performance incidents to merchandising and engineering teams.

## Framework
1. **KPI Stack** – FCP, LCP, CLS, TTFB, checkout API latency, error rates, uptime.
2. **Segmentation** – device, geography, browser, promotion, traffic source.
3. **Alerting Rules** – thresholds, aggregation windows, escalation paths, war-room triggers.
4. **Diagnostics** – logging, tracing, screenshot/session replay hooks.
5. **Comms Kit** – stakeholder updates, status pages, rollback plans.

## Templates
- Performance scorecard with spark lines + thresholds.
- Incident log template with root cause, mitigation, and follow-up tasks.
- Escalation matrix covering engineering, DevOps, merchandising, and CX leads.

## Tips
- Pair synthetic monitoring with RUM data to catch both systemic and localized issues.
- Freeze experiment/merch changes when performance breaches critical thresholds.
- Use alongside `diagnose-conversion-drop` to correlate experience and performance data.

---
