---
name: elasticsearch
description: |
  Elasticsearch audit log search and analytics for INVOOPAY platform.
  Use when: implementing audit logging, searching audit events, building analytics dashboards, configuring data streams, or debugging outbox publishing.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Elasticsearch Skill

Configures Elasticsearch for audit logging, full-text search, and analytics queries. This project uses Elasticsearch for audit trails (API key access, admin actions) and could extend to product search beyond PostgreSQL's TSVECTOR.

## Quick Start

### Elasticsearch Client Setup

```typescript
// src/services/elasticsearchService.ts
import { Client } from '@elastic/elasticsearch';

const client = new Client({
  node: process.env.ELASTICSEARCH_URL || 'http://localhost:9200',
  auth: {
    apiKey: process.env.ELASTICSEARCH_API_KEY
  }
});

export async function indexAuditEvent(event: AuditEvent): Promise<void> {
  await client.index({
    index: `audit-logs-${new Date().toISOString().slice(0, 7)}`, // Monthly indices
    document: {
      ...event,
      '@timestamp': new Date().toISOString()
    }
  });
}
```

### Searching Audit Logs

```typescript
export async function searchAuditLogs(params: {
  keyName?: string;
  action?: string;
  adminUserId?: number;
  from?: string;
  to?: string;
  limit?: number;
}): Promise<AuditEvent[]> {
  const must: any[] = [];
  
  if (params.keyName) must.push({ term: { 'key_name.keyword': params.keyName } });
  if (params.action) must.push({ term: { action: params.action } });
  if (params.adminUserId) must.push({ term: { admin_user_id: params.adminUserId } });
  
  if (params.from || params.to) {
    must.push({
      range: {
        '@timestamp': {
          ...(params.from && { gte: params.from }),
          ...(params.to && { lte: params.to })
        }
      }
    });
  }

  const response = await client.search({
    index: 'audit-logs-*',
    query: { bool: { must } },
    size: params.limit || 100,
    sort: [{ '@timestamp': 'desc' }]
  });

  return response.hits.hits.map(hit => hit._source as AuditEvent);
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Index per time period | Prevents unbounded index growth | `audit-logs-2025-01` |
| Keyword vs text | `.keyword` for exact match, text for full-text | `key_name.keyword` |
| Bool queries | Combine must/should/must_not clauses | `{ bool: { must: [...] } }` |
| Date range | Filter by timestamp | `range: { '@timestamp': { gte, lte } }` |
| Aggregations | Analytics and metrics | `aggs: { by_action: { terms: { field: 'action' } } }` |

## Common Patterns

### Index Template for Audit Logs

```typescript
await client.indices.putIndexTemplate({
  name: 'audit-logs-template',
  index_patterns: ['audit-logs-*'],
  template: {
    settings: {
      number_of_shards: 1,
      number_of_replicas: 0, // Dev; use 1+ in production
      'index.lifecycle.name': 'audit-logs-policy'
    },
    mappings: {
      properties: {
        '@timestamp': { type: 'date' },
        key_name: { type: 'keyword' },
        action: { type: 'keyword' },
        admin_user_id: { type: 'integer' },
        admin_user_email: { type: 'keyword' },
        ip_address: { type: 'ip' },
        user_agent: { type: 'text' },
        metadata: { type: 'object', enabled: false }
      }
    }
  }
});
```

### Aggregation for Analytics

```typescript
const response = await client.search({
  index: 'audit-logs-*',
  size: 0,
  aggs: {
    actions_over_time: {
      date_histogram: {
        field: '@timestamp',
        calendar_interval: 'day'
      },
      aggs: {
        by_action: { terms: { field: 'action' } }
      }
    }
  }
});
```

## See Also

- [patterns](references/patterns.md) - Index design, query patterns, bulk operations
- [workflows](references/workflows.md) - Setup, monitoring, troubleshooting

## Related Skills

- See the **postgresql** skill for hybrid search strategies (Elasticsearch + PostgreSQL)
- See the **docker** skill for Elasticsearch container configuration
- See the **node** skill for async client patterns