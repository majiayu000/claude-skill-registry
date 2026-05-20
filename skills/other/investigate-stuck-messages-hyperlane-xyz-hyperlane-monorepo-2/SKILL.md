---
name: investigate-stuck-messages
description: Investigate stuck messages in relayer queue. Use when alerts mention "queue length > 0", to diagnose why messages are stuck, or to get message IDs for denylisting.
---

# Investigate Stuck Messages

Query the relayer API to investigate stuck messages, their retry counts, and error reasons.

## When to Use

1. **Alert-based triggers:**
   - Alert: "Known app context relayer queue length > 0 for 40m"
   - Any alert mentioning stuck messages in prepare queue
   - High retry counts for specific app contexts

2. **User request triggers:**
   - "Why are messages stuck for [app_context]?"
   - "Investigate stuck messages on [chain]"
   - "What's causing the queue alert?"
   - Pasting a Grafana alert URL

## Input Parameters

**Option 1: Grafana Alert URL (recommended)**

```
/investigate-stuck-messages https://abacusworks.grafana.net/alerting/grafana/cdg1ro5hi4vswb/view?tab=instances
```

**Option 2: Manual specification**

```
/investigate-stuck-messages app_context=EZETH/renzo-prod remote=linea
```

| Parameter     | Required | Default    | Description                                                           |
| ------------- | -------- | ---------- | --------------------------------------------------------------------- |
| `alert_url`   | No       | -          | Grafana alert URL (extracts app_context/remote from firing instances) |
| `app_context` | No\*     | -          | The app context (e.g., `EZETH/renzo-prod`, `oUSDT/production`)        |
| `remote`      | No\*     | -          | Destination chain name (e.g., `linea`, `ethereum`, `arbitrum`)        |
| `environment` | No       | `mainnet3` | Deployment environment                                                |

\*Either `alert_url` OR both `app_context` and `remote` must be provided.

## Workflow

### Step 1: Parse Input and Extract Alert Instances

**If Grafana alert URL provided:**

1. Extract the alert UID from the URL (e.g., `cdg1ro5hi4vswb` from `.../alerting/grafana/cdg1ro5hi4vswb/view`)

2. Query Prometheus directly for firing instances using `mcp__grafana__query_prometheus`:

   ```
   sum by (app_context, remote)(
       max_over_time(
           hyperlane_submitter_queue_length{
               queue_name="prepare_queue",
               app_context!~"Unknown|merkly_eth|merkly_erc20|helloworld|velo_message_module",
               hyperlane_context!~"rc|vanguard0|vanguard1|vanguard2|vanguard3|vanguard4|vanguard5",
               operation_status!~"Retry\\(ApplicationReport\\(.*\\)\\)|FirstPrepareAttempt",
               hyperlane_deployment="mainnet3",
           }[2m]
       )
   ) > 0
   ```

3. Extract `app_context` and `remote` labels from each result.

**If manual app_context/remote provided:**

Use the provided values directly.

### Step 2: Setup Port-Forward to Relayer

Check if port 9090 is already in use:

```bash
lsof -i :9090
```

If not in use, start port-forward in background:

```bash
kubectl port-forward omniscient-relayer-hyperlane-agent-relayer-0 9090 -n mainnet3 &
```

Wait a few seconds for the port-forward to establish.

### Step 3: Get Domain IDs for Chains

Look up domain IDs from the registry:

```bash
cat node_modules/.pnpm/@hyperlane-xyz+registry@*/node_modules/@hyperlane-xyz/registry/dist/chains/<chain>/metadata.json | jq '.domainId'
```

Common domain IDs:

- ethereum: 1
- optimism: 10
- arbitrum: 42161
- polygon: 137
- base: 8453
- unichain: 130
- avalanche: 43114

### Step 4: Query Relayer API

For each destination chain, query the relayer API:

```bash
curl -s 'http://localhost:9090/list_operations?destination_domain=<DOMAIN_ID>' > /tmp/<chain>.json
```

The response contains operations with:

- `id`: Message ID (H256)
- `operation.message.sender`: Sender address
- `operation.message.recipient`: Recipient address
- `operation.num_retries`: Number of retries (higher = more stuck)
- `operation.status`: Error status (e.g., `{"Retry": "ErrorEstimatingGas"}`)
- `operation.message.origin`: Origin domain ID
- `operation.message.destination`: Destination domain ID
- `operation.app_context`: App context name

### Step 5: Filter Messages by App Context

Look up the `app_context` in `rust/main/app-contexts/mainnet_config.json`:

```bash
jq '.metricAppContexts[] | select(.name == "<APP_CONTEXT>")' rust/main/app-contexts/mainnet_config.json
```

Filter API results to only include messages where:

- `operation.message.recipient` matches one of the `recipientAddress` values for that destination domain

**Important**: Addresses are padded to 32 bytes (H256 format).

### Step 6: Query GCP Logs for Actual Errors

**Calculate log freshness based on retry count:**

The relayer uses exponential backoff (see `calculate_msg_backoff` in `rust/main/agents/relayer/src/msg/pending_message.rs`):

| Retries | Backoff/retry | Cumulative Time | Freshness Flag    |
| ------- | ------------- | --------------- | ----------------- |
| 1-4     | 5s-1min       | ~2min           | `--freshness=1h`  |
| 5-24    | 3min          | ~1h             | `--freshness=3h`  |
| 25-39   | 5-26min       | ~5h             | `--freshness=12h` |
| 40-49   | 30min-1h      | ~12h            | `--freshness=24h` |
| 50-60   | 2-22h         | ~35h            | `--freshness=3d`  |
| 60+     | 22h+          | 35h+            | `--freshness=7d`  |

For each message ID, query GCP logs with calculated freshness:

```bash
gcloud logging read 'resource.type=k8s_container AND resource.labels.namespace_name=mainnet3 AND resource.labels.pod_name:omniscient-relayer AND jsonPayload.span.id:<MESSAGE_ID> AND jsonPayload.fields.error:*' --project=abacus-labs-dev --limit=1 --format='value(jsonPayload.fields.error)' --freshness=<CALCULATED_FRESHNESS>
```

Extract the human-readable error from the response using `sed` (macOS compatible):

```bash
echo "$raw_error" | sed -n 's/.*execution reverted: \([^"]*\)".*/\1/p' | head -1
```

Common error patterns:

- `"execution reverted: Nonce already used"` → "Nonce already used"
- `"execution reverted: panic: arithmetic underflow"` → "Arithmetic underflow"

**Note**: Do not use `grep -P` as it's not available on macOS.

### Step 7: Present Investigation Results

Output a detailed summary table with **full message IDs** and **both error sources**:

```
## Investigation Results for [APP_CONTEXT]

### Summary
- Total stuck messages: X
- Destinations affected: [list]
- Reprepare reasons: ErrorEstimatingGas (N), CouldNotFetchMetadata (M)

### Messages

| Message ID | Retries | Reprepare Reason | Error | Origin |
|------------|---------|------------------|-----------|--------|
| `0xaa18ebc1c79345e6d24984a0b9a5ab66c968d128d46b2357b641e56e71b8d30c` | 47 | ErrorEstimatingGas | Nonce already used | optimism |
| `0xd6aeef7c092a88aa23ad53227aeb834ae731d059b3ce749db8451e761f3f15ac` | 47 | ErrorEstimatingGas | Nonce already used | arbitrum |

**Important**: Always show the full 66-character message ID (0x + 64 hex chars). Do not truncate.

### Error Analysis
[Explain based on the actual log errors found]

### Next Steps
To denylist these messages, run:
/denylist-stuck-messages <message_ids> app_context=APP_CONTEXT
```

**Column definitions:**

- **Reprepare Reason**: From `operation.status` in relayer API (e.g., ErrorEstimatingGas, CouldNotFetchMetadata)
- **Error**: Actual revert reason from GCP logs (e.g., "Nonce already used", "Arithmetic underflow")

### Step 8: Output Denylist Command

At the end of the investigation results, output the full denylist command:

```
### Next Steps
To denylist, run:
/denylist-stuck-messages 0xaa18ebc1c79345e6d24984a0b9a5ab66c968d128d46b2357b641e56e71b8d30c 0xd6aeef7c092a88aa23ad53227aeb834ae731d059b3ce749db8451e761f3f15ac app_context=APP_CONTEXT
```

Always use full message IDs, never truncated.

## Error Status Reference

| Status                   | Meaning                                 | Action                                   |
| ------------------------ | --------------------------------------- | ---------------------------------------- |
| `ErrorEstimatingGas`     | Gas estimation failed (contract revert) | Usually denylist - contract won't accept |
| `CouldNotFetchMetadata`  | Can't get ISM metadata                  | Check validators, may resolve itself     |
| `ApplicationReport(...)` | App-specific error                      | Check the specific error message         |
| `GasPaymentNotFound`     | No IGP payment                          | May need manual relay with gas           |

## Error Handling

- **Port-forward fails**: Check kubectl context: `kubectl config current-context`
- **No messages found**: Queue may have cleared; alert may be stale
- **API returns error**: Check relayer pod: `kubectl get pods -n mainnet3 | grep relayer`
- **App context not found**: May be new/custom; ask user for sender/recipient addresses

## Prerequisites

- `kubectl` configured with access to mainnet cluster
- Grafana MCP server connected (for alert URL parsing)
