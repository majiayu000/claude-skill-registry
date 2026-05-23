---
name: upstash-context7
description: Upstash context management and serverless Redis/Kafka
allowed-tools: [Bash, Read, WebFetch]
---

# Upstash Context7 Skill

## Overview

Upstash serverless data platform. 90%+ context savings.

## Requirements

- UPSTASH_REDIS_URL
- UPSTASH_REDIS_TOKEN

## Tools (Progressive Disclosure)

### Redis Operations

| Tool | Description | Confirmation |
| ---- | ----------- | ------------ |
| get  | Get value   | No           |
| set  | Set value   | Yes          |
| del  | Delete key  | Yes          |
| scan | Scan keys   | No           |

### Vector Store

| Tool          | Description   | Confirmation |
| ------------- | ------------- | ------------ |
| upsert-vector | Insert vector | Yes          |
| query-vector  | Query similar | No           |
| delete-vector | Delete vector | Yes          |

### QStash (Messaging)

| Tool          | Description     | Confirmation |
| ------------- | --------------- | ------------ |
| publish       | Publish message | Yes          |
| list-messages | List queued     | No           |

## Agent Integration

- **developer** (primary): Serverless data
- **llm-architect** (secondary): Vector operations
