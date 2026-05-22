---
name: elasticsearch-logs
description: Elasticsearch log search and analysis
allowed-tools: [Bash, Read, WebFetch]
---

# Elasticsearch Logs Skill

## Overview

Elasticsearch log querying and analysis. 90%+ context savings.

## Requirements

- ELASTICSEARCH_URL environment variable
- ELASTICSEARCH_API_KEY (optional)

## Tools (Progressive Disclosure)

### Search

| Tool         | Description      |
| ------------ | ---------------- |
| search       | Search logs      |
| query-dsl    | DSL query        |
| aggregations | Run aggregations |

### Indices

| Tool         | Description     | Confirmation |
| ------------ | --------------- | ------------ |
| list-indices | List indices    | No           |
| index-stats  | Get index stats | No           |
| delete-index | Delete index    | **REQUIRED** |

### Analysis

| Tool       | Description        |
| ---------- | ------------------ |
| field-caps | Field capabilities |
| analyze    | Analyze text       |

### BLOCKED

| Tool           | Status      |
| -------------- | ----------- |
| cluster delete | **BLOCKED** |

## Agent Integration

- **devops** (primary): Log management
- **incident-responder** (primary): Log investigation
- **developer** (secondary): Debug logging
