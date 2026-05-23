---
name: serverless-slo-definition-monitoring
version: "1.0"
description: >
  Service Level Objective (SLO) definition and monitoring for serverless applications.
  PROACTIVELY activate for: (1) Defining SLOs for serverless functions, (2) Setting up error budgets,
  (3) Configuring SLI metrics, (4) Monitoring latency percentiles, (5) Availability tracking.
  Triggers: "SLO", "SLI", "error budget", "availability", "latency", "percentile", "service level", "reliability"
core-integration:
  techniques:
    primary: ["systematic_analysis"]
    secondary: ["structured_evaluation"]
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Serverless SLO Definition and Monitoring

This skill provides expertise in defining and monitoring Service Level Objectives for serverless applications.

## Overview

SLOs define the reliability targets for your services, enabling data-driven decisions about feature development vs. reliability work.

## Key Concepts

- **SLI (Service Level Indicator)**: Quantitative measure of service behavior (latency, error rate)
- **SLO (Service Level Objective)**: Target value for an SLI (99.9% availability)
- **Error Budget**: Allowable amount of unreliability (100% - SLO target)
- **Burn Rate**: How quickly error budget is being consumed

## Common SLIs for Serverless

1. **Availability**: Percentage of successful requests
2. **Latency**: Response time percentiles (p50, p95, p99)
3. **Throughput**: Requests per second
4. **Error Rate**: Percentage of failed requests

## Example SLO Definitions

```yaml
slos:
  - name: api-availability
    sli: successful_requests / total_requests
    target: 99.9%
    window: 30d

  - name: api-latency
    sli: requests_under_500ms / total_requests
    target: 95%
    window: 30d
```

## Best Practices

1. Start with achievable SLOs and tighten over time
2. Use error budgets to balance velocity and reliability
3. Alert on burn rate, not individual failures
4. Review and adjust SLOs quarterly

[Content to be expanded based on plugin_spec_agentient-observability.md specifications]
