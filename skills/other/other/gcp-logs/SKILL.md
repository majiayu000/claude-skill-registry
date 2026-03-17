---
name: gcp-logs
description: Read and query GCP logs for Hyperlane agents using gcloud CLI. Use when investigating relayer, validator, or scraper logs, debugging message processing, or analyzing operational issues. Provides efficient filtering and context management strategies.
---

# GCP Logs Query Skill

## When to Use

- Investigating relayer, validator, or scraper behavior
- Debugging message processing issues
- Analyzing operational incidents
- Looking for specific errors or patterns in agent logs

## Prerequisites

- `gcloud` CLI installed and authenticated
- Access to `abacus-labs-dev` GCP project

## Base Query Templates

### Relayer (Omniscient)

```bash
gcloud logging read 'resource.type="k8s_container" AND resource.labels.project_id="abacus-labs-dev" AND resource.labels.location="us-east1-c" AND resource.labels.cluster_name="hyperlane-mainnet" AND resource.labels.namespace_name="mainnet3" AND labels.k8s-pod/app_kubernetes_io/component="relayer" AND labels.k8s-pod/app_kubernetes_io/instance="omniscient-relayer" AND labels.k8s-pod/app_kubernetes_io/name="hyperlane-agent"' --project=abacus-labs-dev --limit=50 --format=json --freshness=1d
```

### Validator

```bash
gcloud logging read 'resource.type="k8s_container" AND resource.labels.project_id="abacus-labs-dev" AND resource.labels.location="us-east1-c" AND resource.labels.cluster_name="hyperlane-mainnet" AND resource.labels.namespace_name="mainnet3" AND labels.k8s-pod/app_kubernetes_io/component="validator" AND labels.k8s-pod/app_kubernetes_io/name="hyperlane-agent"' --project=abacus-labs-dev --limit=50 --format=json --freshness=1d
```

### Scraper

```bash
gcloud logging read 'resource.type="k8s_container" AND resource.labels.project_id="abacus-labs-dev" AND resource.labels.location="us-east1-c" AND resource.labels.cluster_name="hyperlane-mainnet" AND resource.labels.namespace_name="mainnet3" AND labels.k8s-pod/app_kubernetes_io/component="scraper3" AND labels.k8s-pod/app_kubernetes_io/instance="omniscient-scraper" AND labels.k8s-pod/app_kubernetes_io/name="hyperlane-agent"' --project=abacus-labs-dev --limit=50 --format=json --freshness=1d
```

## Noise Filtering

Add these filters to reduce noisy log lines that consume context without providing value:

```
-jsonPayload.fields.message="Found log(s) in index range"
-jsonPayload.fields.message="Dispatching get_public_key"
NOT "Instantiated AWS signer"
-jsonPayload.fields.message="Ingesting leaf"
-jsonPayload.fields.message="Message already marked as processed in DB"
-jsonPayload.fields.message="Message destined for self, skipping"
-jsonPayload.fields.message="Message has already been delivered, marking as submitted."
-jsonPayload.fields.message="Popped OpQueue operations"
-jsonPayload.fields.message="Validator returned latest index"
-jsonPayload.fields.message="Found signed checkpoint"
-jsonPayload.fields.return="Ok(None)"
-jsonPayload.fields.message="Fast forwarded current sequence"
-jsonPayload.fields.message="Cursor can't make progress, sleeping"
-jsonPayload.fields.message="fallback_request"
-jsonPayload.fields.message="No message found in DB for leaf index"
-jsonPayload.fields.message="Processor working on message"
-jsonPayload.fields.message="Message destined for unknown domain, skipping"
```

## Progressive Query Strategy (Token Efficiency)

### Step 1: Fetch Message Field Only First

To minimize context consumption, first fetch only the `message` field:

```bash
gcloud logging read '[BASE_QUERY] AND "[search_term]"' --project=abacus-labs-dev --limit=30 --format='json(jsonPayload.fields.message,timestamp)' --freshness=1d
```

This gives you a quick overview without the full log payload.

### Step 2: Get Full Context for Specific Entries

Once you identify interesting log entries, fetch full details:

```bash
gcloud logging read '[BASE_QUERY] AND "[specific_identifier]"' --project=abacus-labs-dev --limit=20 --format=json --freshness=1d
```

### Step 3: Extract Specific Fields

When you need specific details, use jq or grep to extract:

```bash
gcloud logging read '[QUERY]' --format=json | jq '.[].jsonPayload.fields.error'
```

## Common Query Patterns

### Search by Message ID

```bash
gcloud logging read '[BASE_QUERY] AND "0x[MESSAGE_ID]"' --project=abacus-labs-dev --limit=50 --format=json --freshness=1d
```

### Search for Errors/Warnings

```bash
gcloud logging read '[BASE_QUERY] AND severity>="WARNING"' --project=abacus-labs-dev --limit=50 --format=json --freshness=1d
```

### Search by Chain/Domain

```bash
gcloud logging read '[BASE_QUERY] AND jsonPayload.spans.domain:"[chain_name]"' --project=abacus-labs-dev --limit=50 --format=json --freshness=1d
```

### Search for Stuck Messages (High Retry Count)

```bash
gcloud logging read '[BASE_QUERY] AND jsonPayload.fields.num_retries>=5' --project=abacus-labs-dev --limit=30 --format=json --freshness=1d
```

### Search for Gas Estimation Errors

```bash
gcloud logging read '[BASE_QUERY] AND "eth_estimateGas"' --project=abacus-labs-dev --limit=30 --format=json --freshness=1d
```

### Search by App Context

```bash
gcloud logging read '[BASE_QUERY] AND jsonPayload.fields.app_context:"[APP_CONTEXT]"' --project=abacus-labs-dev --limit=30 --format=json --freshness=1d
```

## Time Range Options

- `--freshness=1h` - Last hour
- `--freshness=1d` - Last day
- `--freshness=7d` - Last week
- Or use explicit timestamps in filter: `timestamp>="2026-01-27T00:00:00Z"`

## Output Format Options

- `--format=json` - Full JSON (verbose, high context)
- `--format='json(jsonPayload.fields.message,timestamp)'` - Specific fields only (efficient)
- `--format='value(jsonPayload.fields.message)'` - Just values, no structure

## Key Log Fields to Focus On

| Field                            | Description                |
| -------------------------------- | -------------------------- |
| `jsonPayload.fields.message`     | Main log message           |
| `jsonPayload.fields.error`       | Error details              |
| `jsonPayload.spans[].domain`     | Chain involved             |
| `jsonPayload.fields.num_retries` | Retry count                |
| `jsonPayload.fields.operations`  | Pending message details    |
| `jsonPayload.span.id`            | Message ID in span context |

## Environment Variations

| Environment | Namespace  | Cluster             |
| ----------- | ---------- | ------------------- |
| mainnet3    | `mainnet3` | `hyperlane-mainnet` |
| testnet4    | `testnet4` | `hyperlane-mainnet` |

## Tips

1. **Always start specific** - Search for exact message IDs or error patterns first
2. **Use noise filters** - The base logs are very noisy; always filter
3. **Limit results** - Use `--limit` to avoid overwhelming context
4. **Progressive detail** - Start with message field only, expand as needed
5. **Time bound queries** - Use `--freshness` or timestamp filters
6. **Pipe to grep/jq** - Post-process large results locally
