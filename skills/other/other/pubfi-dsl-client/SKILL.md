---
name: pubfi-dsl-client
description: Use when external agents must construct PubFi DSL requests for OpenSearch and Postgres without server-side natural language compilation.
---

# PubFi DSL Client Guide

## Overview

This skill defines how to build safe, structured DSL requests for PubFi data access. The server only accepts structured DSL and executes a fixed OpenSearch query shape. The server does not accept SQL, raw OpenSearch DSL, or natural language compilation.

## Base URL

Set `API_BASE` to choose the environment:

- Staging (publish target): `API_BASE=https://api-stg.pubfi.ai`
- Local debugging (Actix server): `API_BASE=http://127.0.0.1:23340`

Note: `0.0.0.0` is typically a listen address, not a client address. If you still need it for local debugging, you may set `API_BASE=http://0.0.0.0:23340`.

## When To Use

- You need to convert an agent intent into a structured request.
- You must avoid sending SQL or raw OpenSearch DSL to the server.
- You need a deterministic, auditable query shape for billing and rate limits.

## Core Rules

- Only send fields defined in the DSL schema.
- Do not send SQL, OpenSearch DSL, or arbitrary field names.
- Use explicit UTC timestamps and treat `window.end` as exclusive.
- Keep `search.doc_topk`, filter sizes, and aggregation sizes within the published limits from the schema endpoint.
- Use `search.doc_topk = 0` when you only need aggregation results.

## Workflow

1. Fetch the schema from the API, or use `references/dsl-schema.md` as the local contract.
2. Convert the user intent into time window, filters, document fields, and aggregation primitives.
3. Validate the JSON shape and required fields before sending.
4. Record the request and response for audit and billing reconciliation.

## Endpoints

- `GET /v1/dsl/schema`
- `POST /v1/dsl/query`

## Example Commands

Fetch the schema:

```bash
curl -sS "$API_BASE/v1/dsl/schema"
```

Run a query:

```bash
curl -sS "$API_BASE/v1/dsl/query" \
  -H 'content-type: application/json' \
  -d @request.json
```

## Example Request

```json
{
  "window": {"start": "2026-02-05T00:00:00Z", "end": "2026-02-06T00:00:00Z"},
  "search": {"text": "liquidity stress exchange withdrawal", "doc_topk": 50},
  "filters": {"tags": ["withdrawal_pause"], "entities": ["Binance"], "sources": ["coindesk"]},
  "output": {
    "fields": [
      "document_id",
      "title",
      "source",
      "source_published_at",
      "tag_slugs",
      "entity_labels",
      "document_summary"
    ],
    "aggregations": [
      {
        "name": "top_tags",
        "aggregation": {"type": "terms", "field": "tag_slugs", "size": 50, "min_doc_count": 2}
      },
      {
        "name": "volume_1h",
        "aggregation": {"type": "date_histogram", "field": "source_published_at", "fixed_interval": "1h"}
      },
      {
        "name": "tag_edges",
        "aggregation": {"type": "cooccurrence", "field": "tag_slugs", "outer_size": 50, "inner_size": 50, "min_doc_count": 2}
      }
    ]
  }
}
```

## Common Mistakes

- Passing natural language constraints instead of structured filters.
- Omitting `window` or using non-UTC timestamps.
- Requesting too many fields or too many aggregations.
- Using unsupported `fixed_interval` values.
- Requesting large co-occurrence expansions that violate edge limits.
