---
name: faion-growth-marketer
description: "Growth marketing: experiments, analytics, A/B testing, AARRR metrics, retention."
user-invocable: false
allowed-tools: Read, Write, Edit, Task, WebSearch, AskUserQuestion, TodoWrite, Glob
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Growth Marketer Domain Skill

Data-driven growth: experiments, analytics, A/B testing, AARRR metrics, retention strategies, viral loops, referral programs.

## Purpose

Orchestrates growth activities: metrics tracking, experimentation framework, A/B testing, AARRR optimization, retention strategies, viral mechanics, analytics setup.

## Context Discovery

### Auto-Investigation

Check these project signals to understand growth marketing context:

| Signal | Location | What to Look For |
|--------|----------|------------------|
| Analytics setup | `docs/analytics/`, config files | Google Analytics, Plausible, tracking implementation |
| Metrics dashboard | Analytics platform, internal docs | KPIs, North Star metric, AARRR funnel metrics |
| Experiment docs | `.aidocs/`, `docs/experiments/` | A/B tests, MVT tests, experiment results |
| Cohort data | Analytics, retention reports | User cohorts, retention curves, churn rates |
| Growth loops | Product docs, user flows | Viral loops, referral programs, PLG mechanics |
| Conversion funnels | Analytics, funnel reports | Acquisition → Activation → Retention metrics |
| User data | Database schema, analytics | User properties, events, behavioral data |

### Discovery Questions

```yaml
question: "What's your primary growth focus?"
header: "Growth Focus"
multiSelect: false
options:
  - label: "Establish metrics foundation"
    description: "AARRR framework, North Star metric, analytics setup"
  - label: "Improve activation"
    description: "Onboarding optimization, aha moment, time-to-value"
  - label: "Increase retention"
    description: "Retention strategies, churn prevention, engagement loops"
  - label: "Build viral growth"
    description: "Viral loops, referral programs, K-factor optimization"
```

```yaml
question: "What's your experimentation maturity?"
header: "Experimentation"
multiSelect: false
options:
  - label: "No experiments yet"
    description: "A/B testing basics, experiment setup, statistical foundations"
  - label: "Basic A/B testing"
    description: "Advanced testing, MVT, prioritization frameworks"
  - label: "Regular experiments"
    description: "Optimization tactics, velocity, statistical rigor"
  - label: "Advanced program"
    description: "Growth loops, sophisticated attribution, scaling experiments"
```

```yaml
question: "What metrics do you need to improve?"
header: "Metrics to Optimize"
multiSelect: true
options:
  - label: "Acquisition (AARRR)"
    description: "Traffic sources, CAC, conversion rates"
  - label: "Activation (AARRR)"
    description: "Onboarding, aha moment, time-to-value"
  - label: "Retention (AARRR)"
    description: "Engagement, churn, cohort analysis"
  - label: "Revenue (AARRR)"
    description: "Monetization, LTV, upsells"
  - label: "Referral (AARRR)"
    description: "Viral coefficient, K-factor, referral loops"
```

## When to Use

| Scenario | Methodologies |
|----------|---------------|
| Growth framework | aarrr-pirate-metrics → north-star-metric |
| Activation | activation-framework → activation-tactics → activation-metrics |
| Retention | retention-basics → retention-strategies → ops-churn-prevention |
| Viral growth | viral-loops → growth-viral-loops → growth-referral-programs |
| A/B testing | ab-testing-basics → ab-testing-setup → mvt-basics |
| Analytics setup | google-analytics / plausible-analytics → conversion-tracking |
| Cohort analysis | cohort-basics → cohort-implementation |
| Growth loops | growth-loops → viral-loops |
| Operations | ops-metrics-basics → ops-dashboard-setup → ops-automation-workflow |
| Statistics | statistics-basics → statistics-application |

## Methodologies (30)

### Growth Framework (2)
- aarrr-pirate-metrics.md
- north-star-metric.md

### Activation (3)
- activation-framework.md
- activation-tactics.md
- activation-metrics.md

### Retention (5)
- retention-basics.md
- retention-strategies.md
- retention-metrics.md
- ops-churn-basics.md
- ops-churn-prevention.md

### Viral & Referral (5)
- viral-loops.md
- viral-metrics.md
- viral-optimization.md
- growth-viral-loops.md
- growth-referral-programs.md

### Growth Loops (1)
- growth-loops.md

### Experimentation (4)
- ab-testing-basics.md
- ab-testing-setup.md
- methodologies/growth/mvt-basics.md
- methodologies/growth/mvt-implementation.md

### Analytics (4)
- google-analytics.md
- plausible-analytics.md
- conversion-tracking.md
- privacy-compliance.md

### Cohorts (2)
- cohort-basics.md
- cohort-implementation.md

### Operations (3)
- ops-metrics-basics.md
- ops-dashboard-setup.md
- ops-automation-workflow.md

### Statistics (2)
- statistics-basics.md
- statistics-application.md

### AI & Future (1)
- agentic-commerce-future-trends.md

## Related Skills

- faion-marketing-manager (parent orchestrator)
- faion-conversion-optimizer (funnel optimization, CRO)
- faion-gtm-strategist (GTM metrics)
- faion-content-marketer (content experiments)
- faion-ppc-manager (paid ads optimization)

---

*Growth Marketer v1.0 | 30 Methodologies*
