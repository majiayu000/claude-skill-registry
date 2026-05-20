---
name: investigate-merkle-root-mismatch
description: Investigate merkle root mismatch alerts between relayer and validators. Use when alerts mention "merkle root mismatch", "checkpoint root does not match canonical root", or when asked to debug relayer merkle tree issues for a chain. This skill only investigates - use /fix-merkle-root-mismatch to apply fixes.
---

# Investigate Merkle Root Mismatch

## When to Use

1. **Alert-based triggers:**
   - Alert mentions "merkle root mismatch"
   - GCP logs show: "checkpoint root does not match canonical root from merkle proof"
   - The `hyperlane_merkle_root_mismatch` metric is firing

2. **User request triggers:**
   - "Debug merkle tree issues for [chain]"
   - "Investigate the merkle root mismatch on [chain]"
   - "Why is the relayer's merkle tree wrong for [chain]?"

## Input Parameters

| Parameter     | Required | Default    | Description                                                              |
| ------------- | -------- | ---------- | ------------------------------------------------------------------------ |
| `origin`      | Yes      | -          | The origin chain with merkle root mismatch (e.g., `paradex`, `ethereum`) |
| `domain_id`   | No       | -          | Domain ID of the chain (auto-derived from registry if not provided)      |
| `environment` | No       | `mainnet3` | `mainnet3` or `testnet4`                                                 |

## Problem Overview

The relayer maintains a local merkle tree built from message IDs. When a validator signs a checkpoint, the relayer needs to generate a merkle proof. If the relayer's tree has incorrect message IDs, the roots will mismatch and message delivery will fail.

**Most likely cause:** The relayer indexed incorrect message IDs (possibly due to RPC issues or reorgs), while validators have the correct data.

## Prerequisites

- `kubectl` access to the relayer pods
- Grafana MCP server configured

## Investigation Workflow

### Step 1: Confirm the Alert

Query Grafana to confirm the mismatch metric is firing:

```
Use mcp__grafana__query_prometheus with:
- datasourceUid: grafanacloud-prom
- expr: hyperlane_merkle_root_mismatch{origin="[origin]"}
- startTime: now-1h
- queryType: instant
```

If `value` is `1`, the mismatch is confirmed.

### Step 2: Get Latest Tree Insertion Index

Query Grafana for the current tree size:

```
Use mcp__grafana__query_prometheus with:
- datasourceUid: grafanacloud-prom
- expr: hyperlane_latest_tree_insertion_index{origin="[origin]", hyperlane_deployment="[environment]"}
- startTime: now-1h
- queryType: instant
```

This gives you the latest leaf index to work backwards from.

### Step 3: Get Domain ID

If `domain_id` was not provided, fetch from the registry:

```bash
curl -s "https://raw.githubusercontent.com/hyperlane-xyz/hyperlane-registry/main/chains/[origin]/metadata.yaml" | grep domainId
```

### Step 4: Establish Port-Forward to Relayer

Check if port 9090 is already in use:

```bash
lsof -i :9090
```

If not in use, start port-forward in background:

```bash
kubectl port-forward omniscient-relayer-hyperlane-agent-relayer-0 9090:9090 -n [environment] &
```

Wait a few seconds for the port-forward to establish, then verify it's working:

```bash
curl -s "localhost:9090/merkle_tree_insertions?domain_id=[domain_id]&leaf_index_start=0&leaf_index_end=1"
```

### Step 5: Binary Search for First Mismatch

Compare validator checkpoints (from S3) against relayer merkle proofs. Use binary search to find the FIRST mismatched index.

**Validator checkpoint URL pattern:**

```
https://hyperlane-[environment]-[origin]-validator-0.s3.us-east-1.amazonaws.com/checkpoint_[index]_with_id.json
```

**Comparison function:**

```bash
# Check a specific index
index=[INDEX]
domain_id=[DOMAIN_ID]
origin=[ORIGIN]
environment=[ENVIRONMENT]

validator_root=$(curl -s "https://hyperlane-${environment}-${origin}-validator-0.s3.us-east-1.amazonaws.com/checkpoint_${index}_with_id.json" | jq -r '.value.checkpoint.root')
relayer_root=$(curl -s "localhost:9090/merkle_proofs?domain_id=${domain_id}&leaf_index=${index}&root_index=${index}" | jq -r '.root')

echo "Index $index:"
echo "  Validator: $validator_root"
echo "  Relayer:   0x$relayer_root"
if [ "$validator_root" = "0x$relayer_root" ]; then echo "  ✓ Match"; else echo "  ❌ MISMATCH"; fi
```

**Binary search strategy:**

1. Start at the latest index - if mismatch, go to 50% of that index
2. If match at 50%, mismatch is between 50%-100% - try 75%
3. If mismatch at 50%, mismatch is between 0%-50% - try 25%
4. Continue narrowing until you find the exact first mismatch index (where index N-1 matches but index N mismatches)

### Step 6: Identify Mismatched Message IDs

Once you found the first mismatch index, compare message IDs:

**Get validator message IDs:**

```bash
for i in $(seq [first_mismatch] [first_mismatch + 10]); do
  msg=$(curl -s "https://hyperlane-[environment]-[origin]-validator-0.s3.us-east-1.amazonaws.com/checkpoint_${i}_with_id.json" | jq -r '.value.message_id')
  echo "$i: $msg"
done
```

**Get relayer message IDs:**

```bash
curl -s "localhost:9090/merkle_tree_insertions?domain_id=[domain_id]&leaf_index_start=[first_mismatch]&leaf_index_end=[first_mismatch + 10]" | jq -r '.merkle_tree_insertions[] | "\(.leaf_index): \(.message_id)"'
```

### Step 7: Get Block Timestamp for Context

Get the block number and timestamp of the first mismatch to understand when the issue started:

```bash
# Get block number from relayer
curl -s "localhost:9090/merkle_tree_insertions?domain_id=[domain_id]&leaf_index_start=[first_mismatch]&leaf_index_end=[first_mismatch]" | jq '.merkle_tree_insertions[0].insertion_block_number'
```

For EVM chains, get timestamp:

```bash
cast block [block_number] --rpc-url [rpc_url] -j | jq '.timestamp'
```

For Starknet chains:

```bash
curl -s --request POST --url '[rpc_url]' --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0","method":"starknet_getBlockWithTxHashes","params":[{"block_number":[block_number]}],"id":1}' | jq '.result.timestamp'
```

Convert Unix timestamp to human-readable:

```bash
date -r [timestamp] -u '+%Y-%m-%d %H:%M:%S UTC'
```

### Step 8: Report Findings

Present the investigation results with:

1. **Summary table:**

| Parameter            | Value                         |
| -------------------- | ----------------------------- |
| Chain                | [origin]                      |
| Domain ID            | [domain_id]                   |
| Environment          | [environment]                 |
| First Mismatch Index | [index]                       |
| Latest Index         | [latest]                      |
| Total Entries to Fix | [latest - first_mismatch + 1] |
| Mismatch Started At  | [block_number] ([timestamp])  |

2. **Sample of mismatched entries:**

| Leaf Index | Relayer Message ID | Validator Message ID | Block Number |
| ---------- | ------------------ | -------------------- | ------------ |
| [idx]      | 0x...              | 0x...                | [block]      |

3. **Inform the user** that to fix this issue, they should run `/fix-merkle-root-mismatch`.

4. **Note about fixing:** ALL entries from the first mismatch to the latest must be fixed because the merkle tree is cumulative - each root depends on all previous leaves.

## API Reference

### Relayer Endpoints

| Endpoint                  | Method | Parameters                                        | Description                 |
| ------------------------- | ------ | ------------------------------------------------- | --------------------------- |
| `/merkle_tree_insertions` | GET    | `domain_id`, `leaf_index_start`, `leaf_index_end` | List merkle tree insertions |
| `/merkle_proofs`          | GET    | `domain_id`, `leaf_index`, `root_index`           | Get merkle proof for a leaf |

### Validator S3 Checkpoint

```
https://hyperlane-[environment]-[chain]-validator-0.s3.us-east-1.amazonaws.com/checkpoint_[index]_with_id.json
```

Response structure:

```json
{
  "value": {
    "checkpoint": {
      "merkle_tree_hook_address": "0x...",
      "mailbox_domain": 514051890,
      "root": "0x...",
      "index": 37352
    },
    "message_id": "0x..."
  },
  "signature": { ... }
}
```

## Common Issues

1. **Port-forward disconnects:** Re-run the kubectl port-forward command
2. **Validator S3 returns 404:** Checkpoint may not exist yet at that index
3. **Binary search takes too long:** Use larger jumps initially (e.g., 10000 indices)
4. **Shell script errors:** Use manual curl commands instead of the bash scripts in `rust/scripts/`

## Next Steps

After investigation, use `/fix-merkle-root-mismatch` to apply the fixes.

## Runbook Reference

Full runbook: https://www.notion.so/hyperlanexyz/Merkle-Root-Mismatch-26a6d35200d680a2857dcd0b228d4ab7
