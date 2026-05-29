---
name: fix-merkle-root-mismatch
description: Apply fixes for merkle root mismatch issues in the relayer database. Use after running /investigate-merkle-root-mismatch to investigate and identify the mismatched entries. Requires user confirmation before any database modifications.
---

# Fix Merkle Root Mismatch

## When to Use

Use this skill AFTER running `/investigate-merkle-root-mismatch` to investigate the issue.

1. **User request triggers:**
   - "Fix the merkle root mismatch on [chain]"
   - "Apply the merkle tree fixes"
   - "Update the relayer database with correct message IDs"

## Input Parameters

| Parameter                | Required | Default    | Description                                                     |
| ------------------------ | -------- | ---------- | --------------------------------------------------------------- |
| `origin`                 | Yes      | -          | The origin chain to fix (e.g., `polygonzkevm`, `ethereum`)      |
| `domain_id`              | Yes      | -          | Domain ID of the chain                                          |
| `environment`            | No       | `mainnet3` | `mainnet3` or `testnet4`                                        |
| `merkle_tree_insertions` | Yes      | -          | List of corrections: `[{leaf_index, message_id, block_number}]` |

## Prerequisites

1. **Investigation completed** - Run `/investigate-merkle-root-mismatch` first to identify mismatched entries
2. `kubectl` access to the relayer pods
3. Port-forward already established to relayer (port 9090)

## Fix Workflow

### Step 0: Find Monorepo Root

```bash
MONOREPO_ROOT=$(git rev-parse --show-toplevel)
```

### Step 1: Verify Port-Forward is Active

Check if port 9090 is already in use:

```bash
lsof -i :9090
```

If not in use, start port-forward in background:

```bash
kubectl port-forward omniscient-relayer-hyperlane-agent-relayer-0 9090:9090 -n [environment] &
```

Wait a few seconds, then verify it's working:

```bash
curl -s "localhost:9090/merkle_tree_insertions?domain_id=[domain_id]&leaf_index_start=0&leaf_index_end=1"
```

### Step 2: Present Changes for Confirmation

**IMPORTANT: User confirmation required before executing.**

Before making any changes to the relayer database, you MUST:

1. Present a summary of ALL changes to be made in a clear table format:

   | Leaf Index | Correct Message ID                                                 | Block Number |
   | ---------- | ------------------------------------------------------------------ | ------------ |
   | 1477       | 0x4bb3e20db45366a6a360ad2639c5421ea622a69b89b2edb045aa97e2051529b7 | 9891832      |
   | 1478       | 0xa66dbdc1874acfddf14e75e6a20dd1632e9e3206c5f5855884da0d26d8ca12fa | 9891872      |

2. Use `AskUserQuestion` to get explicit confirmation:
   - Question: "Do you want to apply these merkle tree fixes to the relayer database?"
   - Options: "Yes, apply fixes" / "No, cancel"

3. **Only proceed if the user explicitly confirms.**

### Step 3: Apply Merkle Tree Fixes

Once confirmed, insert the correct merkle tree insertions via the relayer API:

```bash
curl -X POST \
    -H 'Content-type: application/json' \
    'localhost:9090/merkle_tree_insertions' \
    -d '{
    "merkle_tree_insertions": [
        {
            "chain": [domain_id],
            "insertion_block_number": [block_number],
            "leaf_index": [index],
            "message_id": "0x..."
        }
    ]
}'
```

**Request schema:**

```json
{
  "merkle_tree_insertions": [
    {
      "chain": "<domain_id as number>",
      "insertion_block_number": "<block number as number>",
      "leaf_index": "<leaf index as number>",
      "message_id": "<0x-prefixed H256 hash>"
    }
  ]
}
```

**Verify response:** The API should return a success response with the count of inserted entries.

### Step 4: Restart Relayer

**IMPORTANT: User confirmation required before executing.**

Use `AskUserQuestion` to confirm:

- Question: "Do you want to restart the relayer to apply the database fixes?"
- Options: "Yes, restart relayer" / "No, I'll restart manually later"

**Only proceed if the user explicitly confirms.**

Once confirmed, restart the relayer to rebuild its in-memory merkle tree:

```bash
pnpm --dir typescript/infra exec tsx ./scripts/agents/restart-agents.ts -e [environment] --context hyperlane --role relayer
```

### Step 5: Validate Fix

After the relayer restarts, verify the fix:

#### 5.1: Get Latest Index

Query Grafana for the current tree size:

```
Use mcp__grafana__query_prometheus with:
- datasourceUid: grafanacloud-prom
- expr: hyperlane_latest_tree_insertion_index{origin="[origin]", hyperlane_deployment="[environment]"}
- startTime: now-1h
- queryType: instant
```

#### 5.2: Spot-Check Roots at Key Indices

Compare validator and relayer roots at three points: first fixed index, middle, and latest.

```bash
index=[INDEX]
validator_root=$(curl -s "https://hyperlane-[environment]-[origin]-validator-0.s3.us-east-1.amazonaws.com/checkpoint_${index}_with_id.json" | jq -r '.value.checkpoint.root')
relayer_root=$(curl -s "localhost:9090/merkle_proofs?domain_id=[domain_id]&leaf_index=${index}&root_index=${index}" | jq -r '.root')
echo "Index $index:"
echo "  Validator: $validator_root"
echo "  Relayer:   0x$relayer_root"
if [ "$validator_root" = "0x$relayer_root" ]; then echo "  ✓ Match"; else echo "  ❌ MISMATCH"; fi
```

Run this for:

1. First fixed index (e.g., 37352)
2. Middle index (e.g., 39000)
3. Latest index (e.g., 41172)

#### 5.3: Verify Mismatch Metric is Clear

```
Use mcp__grafana__query_prometheus with:
- datasourceUid: grafanacloud-prom
- expr: hyperlane_merkle_root_mismatch{origin="[origin]"}
- startTime: now-1h
- queryType: instant
```

**Expected result:** Empty result or value of 0.

#### 5.4: Report Results

Present validation results in a table:

| Index | Location    | Result  |
| ----- | ----------- | ------- |
| 37352 | First fixed | ✓ Match |
| 39000 | Middle      | ✓ Match |
| 41172 | Latest      | ✓ Match |

If still mismatched:

- Inform the user that additional entries may need fixing
- Suggest re-running `/investigate-merkle-root-mismatch` to investigate further

## API Reference

### Relayer Endpoints

| Endpoint                  | Method | Description                         |
| ------------------------- | ------ | ----------------------------------- |
| `/merkle_tree_insertions` | GET    | List merkle tree insertions from DB |
| `/merkle_tree_insertions` | POST   | Insert/update merkle tree entries   |

### Request/Response Examples

**POST /merkle_tree_insertions**

Request:

```json
{
  "merkle_tree_insertions": [
    {
      "chain": 1101,
      "insertion_block_number": 9891832,
      "leaf_index": 1477,
      "message_id": "0x4bb3e20db45366a6a360ad2639c5421ea622a69b89b2edb045aa97e2051529b7"
    }
  ]
}
```

Response (success):

```json
{
  "status": "success",
  "data": {
    "count": 1
  }
}
```

## Common Issues

1. **Port-forward disconnected:** Re-establish before applying fixes
2. **API returns error:** Check the error message, verify domain_id and message_id format
3. **Relayer restart fails:** Check kubectl access and pod status
4. **Fix didn't work:** May have missed some mismatched indices, re-investigate

## Runbook Reference

Full runbook: https://www.notion.so/hyperlanexyz/Merkle-Root-Mismatch-26a6d35200d680a2857dcd0b228d4ab7
