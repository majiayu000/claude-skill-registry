---
name: gcloud-observability
description: Google Cloud observability - logging, monitoring, tracing
allowed-tools: [Bash, Read, WebFetch]
---

# GCloud Observability Skill

## Overview

Google Cloud observability suite. 90%+ context savings.

## Requirements

- gcloud CLI with logging/monitoring APIs enabled
- GOOGLE_PROJECT_ID environment variable

## Tools (Progressive Disclosure)

### Logging

| Tool       | Description            |
| ---------- | ---------------------- |
| logs-read  | Read Cloud Logging     |
| logs-tail  | Tail logs in real-time |
| logs-query | Advanced log queries   |

### Monitoring

| Tool         | Description            |
| ------------ | ---------------------- |
| metrics-list | List available metrics |
| metrics-get  | Get metric data        |
| alerts-list  | List alerting policies |

### Tracing

| Tool           | Description             |
| -------------- | ----------------------- |
| traces-list    | List traces             |
| trace-get      | Get trace details       |
| latency-report | Get latency percentiles |

## Agent Integration

- **devops** (primary): Observability setup
- **incident-responder** (primary): Incident investigation
- **performance-engineer** (secondary): Performance analysis
