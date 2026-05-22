---
name: datadog-observability
description: Datadog monitoring, APM, logs, and infrastructure observability
allowed-tools: [Bash, Read, WebFetch]
---

# Datadog Observability Skill

## Overview

Provides 90%+ context savings vs raw Datadog API integration. Multi-service support with progressive disclosure by observability category.

## Requirements

- Datadog API configured
- Environment variables:
  - `DD_API_KEY` (required): Datadog API key
  - `DD_APP_KEY` (required): Datadog application key
  - `DD_SITE` (optional): Datadog site (default: datadoghq.com)

## Tools (Progressive Disclosure)

### Metrics Operations

| Tool          | Description             | Confirmation |
| ------------- | ----------------------- | ------------ |
| query-metrics | Query metric timeseries | No           |
| list-metrics  | List available metrics  | No           |
| post-metrics  | Submit custom metrics   | Yes          |

### APM/Traces Operations

| Tool            | Description                     | Confirmation |
| --------------- | ------------------------------- | ------------ |
| list-services   | List APM services               | No           |
| service-summary | Get service performance summary | No           |
| search-traces   | Search distributed traces       | No           |

### Logs Operations

| Tool          | Description                   | Confirmation |
| ------------- | ----------------------------- | ------------ |
| search-logs   | Search log entries            | No           |
| log-indexes   | List log indexes              | No           |
| log-pipelines | View log processing pipelines | No           |

### Monitors/Alerts Operations

| Tool           | Description         | Confirmation |
| -------------- | ------------------- | ------------ |
| list-monitors  | List monitors       | No           |
| monitor-status | Get monitor status  | No           |
| create-monitor | Create new monitor  | Yes          |
| mute-monitor   | Mute monitor alerts | Yes          |

### Infrastructure Operations

| Tool            | Description               | Confirmation |
| --------------- | ------------------------- | ------------ |
| list-hosts      | List infrastructure hosts | No           |
| host-metrics    | Get host-level metrics    | No           |
| list-containers | List containers           | No           |

## Quick Reference

```bash
# Query metrics
curl -X POST "https://api.${DD_SITE}/api/v1/query" \
  -H "DD-API-KEY: ${DD_API_KEY}" \
  -H "DD-APPLICATION-KEY: ${DD_APP_KEY}" \
  -d '{"query":"avg:system.cpu.user{*}"}'

# Search logs
curl -X POST "https://api.${DD_SITE}/api/v2/logs/events/search" \
  -H "DD-API-KEY: ${DD_API_KEY}" \
  -H "DD-APPLICATION-KEY: ${DD_APP_KEY}" \
  -d '{"filter":{"query":"service:web","from":"now-1h","to":"now"}}'

# List monitors
curl -X GET "https://api.${DD_SITE}/api/v1/monitor" \
  -H "DD-API-KEY: ${DD_API_KEY}" \
  -H "DD-APPLICATION-KEY: ${DD_APP_KEY}"

# Get service summary
curl -X GET "https://api.${DD_SITE}/api/v1/apm/service/{service_name}" \
  -H "DD-API-KEY: ${DD_API_KEY}" \
  -H "DD-APPLICATION-KEY: ${DD_APP_KEY}"
```

## Configuration

- **DD_API_KEY**: Datadog API key (required)
- **DD_APP_KEY**: Datadog application key (required)
- **DD_SITE**: Datadog site domain (optional, default: datadoghq.com)
  - US1: datadoghq.com
  - US3: us3.datadoghq.com
  - US5: us5.datadoghq.com
  - EU: datadoghq.eu
  - AP1: ap1.datadoghq.com

## Security

⚠️ **Never hardcode API keys or application keys**
⚠️ **Use environment variables or secret management**
⚠️ **Monitor mutations (create, mute) require confirmation**
⚠️ **Never expose DD_API_KEY or DD_APP_KEY in logs or responses**

## Agent Integration

- **devops** (primary): Infrastructure monitoring and SRE
- **incident-responder** (primary): Crisis management and troubleshooting
- **performance-engineer** (secondary): Performance analysis
- **developer** (secondary): Application monitoring

## Troubleshooting

| Issue                 | Solution                           |
| --------------------- | ---------------------------------- |
| Authentication failed | Verify DD_API_KEY and DD_APP_KEY   |
| Site not found        | Check DD_SITE configuration        |
| Rate limit exceeded   | Implement exponential backoff      |
| Empty metrics         | Verify metric names and time range |
