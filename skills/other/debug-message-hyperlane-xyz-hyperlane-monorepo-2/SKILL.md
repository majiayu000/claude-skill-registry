---
name: debug-message
description: Debug why a Hyperlane message is not being processed. Use when given a message ID or explorer URL to investigate delivery failures, gas estimation errors, validator issues, or other processing problems.
---

# Debug Hyperlane Message Skill

## When to Use

- User provides a message ID (e.g., `0xa454...`) or explorer URL
- Investigating why a message is stuck or not delivered
- Debugging gas estimation failures
- Understanding message processing status

## Input Parameters

| Parameter      | Required | Example                                        | Description                     |
| -------------- | -------- | ---------------------------------------------- | ------------------------------- |
| `message_id`   | Yes      | `0xa454559c...`                                | The 66-character hex message ID |
| `explorer_url` | Optional | `https://explorer.hyperlane.xyz/message/0x...` | Can extract message_id from URL |

## Debugging Workflow

### Step 1: Get Basic Message Details from Explorer

Fetch the explorer page to get origin/destination chains and basic status:

```
WebFetch: https://explorer.hyperlane.xyz/message/[MESSAGE_ID]
Prompt: Extract message status, origin chain, destination chain, sender, recipient, timestamp, delivery status
```

Key info to extract:

- Origin chain and domain ID
- Destination chain and domain ID
- Is it delivered? (if yes, no debugging needed)
- Timestamp (how old is it?)

### Step 2: Search Relayer Logs for the Message

Use the gcloud CLI to find logs related to this message in the omniscient relayer:

```bash
gcloud logging read 'resource.type="k8s_container" AND resource.labels.project_id="abacus-labs-dev" AND resource.labels.location="us-east1-c" AND resource.labels.cluster_name="hyperlane-mainnet" AND resource.labels.namespace_name="mainnet3" AND labels.k8s-pod/app_kubernetes_io/component="relayer" AND labels.k8s-pod/app_kubernetes_io/instance="omniscient-relayer" AND labels.k8s-pod/app_kubernetes_io/name="hyperlane-agent" AND "[MESSAGE_ID]"' --project=abacus-labs-dev --limit=50 --format=json --freshness=1d
```

### Step 3: Identify the Message Status

Look for the message in `PendingMessage` entries. Common statuses:

| Status                               | Meaning                                  | Priority                 |
| ------------------------------------ | ---------------------------------------- | ------------------------ |
| `Retry(ErrorEstimatingGas)`          | Gas estimation failing - contract revert | HIGH                     |
| `Retry(GasPaymentRequirementNotMet)` | Insufficient gas payment                 | MEDIUM                   |
| `Retry(CouldNotFetchMetadata)`       | Validator signatures unavailable         | LOW (check after 5+ min) |
| `FirstPrepareAttempt`                | Still processing, not stuck yet          | LOW                      |

Extract status with:

```bash
grep -o "message_id: [MESSAGE_ID][^}]*" [log_output] | sort -u
```

### Step 4: Check for Gas Payment Issues

If message is slow/stuck, search for gas payment evaluation logs:

```bash
gcloud logging read '[BASE_RELAYER_QUERY] AND "[MESSAGE_ID]" AND jsonPayload.fields.message:"Evaluating if message meets gas payment requirement"' --project=abacus-labs-dev --limit=5 --format=json --freshness=7d
```

Key fields in `jsonPayload.fields`:

- `current_payment.gas_amount` - gas units paid for by sender
- `tx_cost_estimate.gas_limit` - gas units needed for delivery
- `current_expenditure.gas_used` - gas already spent on retries
- `policy` - subsidy policy (e.g., `fractional_numerator: 1, fractional_denominator: 2` = 50% subsidy)

If `gas_amount < gas_limit`, message fails with `"Repreparing message: Gas payment requirement not met"` and retries every ~3 minutes.

### Step 5: For Gas Estimation Errors - Get the Revert Reason

If status is `ErrorEstimatingGas`, the actual revert reason is in `jsonPayload.fields.error`. Use this query and extraction:

```bash
# Query logs with error field
gcloud logging read 'resource.type="k8s_container" AND resource.labels.project_id="abacus-labs-dev" AND resource.labels.location="us-east1-c" AND resource.labels.cluster_name="hyperlane-mainnet" AND resource.labels.namespace_name="mainnet3" AND labels.k8s-pod/app_kubernetes_io/component="relayer" AND labels.k8s-pod/app_kubernetes_io/instance="omniscient-relayer" AND labels.k8s-pod/app_kubernetes_io/name="hyperlane-agent" AND "[MESSAGE_ID]" AND jsonPayload.fields.error:*' --project=abacus-labs-dev --limit=5 --format=json --freshness=1d 2>/dev/null | grep -o '"error": "[^"]*"' | head -1
```

The error field contains the full revert reason, e.g.:

```
"error": "ContractError(...JsonRpcError { code: 3, message: \"execution reverted: panic: arithmetic underflow or overflow (0x11)\", data: Some(...) }...)"
```

**Quick extraction** - pipe to extract just the revert message:

```bash
... | grep -oP 'execution reverted: [^"\\]+' | head -1
```

Common revert patterns:

- `execution reverted: panic: arithmetic underflow or overflow (0x11)` - Contract math error
- `execution reverted: [CUSTOM_ERROR]` - Custom contract revert (decode with `cast 4byte`)
- `execution reverted` with hex data - Decode selector with `cast 4byte 0x[first4bytes]`

### Step 6: Extract Message Details

From the logs, identify:

- `origin`: Source chain
- `destination`: Destination chain (or domain ID like `4114` for Citrea)
- `sender`: Origin contract address
- `recipient`: Destination contract address (the warp route or recipient)
- `nonce`: Message sequence number

Example log format:

```
HyperlaneMessage { id: 0x..., nonce: 162898, origin: ethereum, sender: 0x..., destination: 4114, recipient: 0x... }
```

### Step 7: Report Findings

Summarize:

1. **Message ID**: Full ID
2. **Route**: Origin -> Destination (e.g., Ethereum -> Citrea)
3. **Status**: Current processing status
4. **Root Cause**: The actual error (e.g., contract revert reason)
5. **Retry Count**: How many times it's been attempted
6. **Recommendation**: What needs to happen (e.g., fix recipient contract, wait for validators)

## Common Root Causes

### Gas Estimation Errors

| Error                                            | Meaning                | Resolution                |
| ------------------------------------------------ | ---------------------- | ------------------------- |
| `panic: arithmetic underflow or overflow (0x11)` | Contract math error    | Bug in recipient contract |
| `IXERC20_NotHighEnoughLimits()`                  | Bridge rate limit hit  | Wait for limit reset      |
| `InsufficientBalance`                            | Not enough tokens      | Fund the contract         |
| `Unauthorized`                                   | Access control failure | Check permissions         |

### Metadata/Validator Issues

If `CouldNotFetchMetadata` persists > 5 minutes:

1. Check validator status using the `debug-validator-checkpoint-inconsistency` skill
2. Identify if validators are behind on the origin chain

### Gas Payment Issues

If `GasPaymentRequirementNotMet`:

- Compare `current_payment.gas_amount` vs `tx_cost_estimate.gas_limit`
- Message will auto-retry every ~3 min until gas prices drop or subsidy kicks in
- Check `policy` field for subsidy ratio (e.g., 1/2 = relayer covers 50%)
- Resolution: wait for gas prices to drop, or manually subsidize via IGP top-up

## Decoding Revert Selectors

When you see hex revert data like `0x4e487b71...`:

```bash
cast 4byte 0x4e487b71
# Returns: Panic(uint256)
```

Common panic codes:

- `0x11` - Arithmetic overflow/underflow
- `0x12` - Division by zero
- `0x21` - Invalid enum value
- `0x31` - Pop on empty array
- `0x32` - Array out of bounds

## Domain ID Reference

Common domain IDs (destination field in logs):

- `1` - Ethereum
- `42161` - Arbitrum
- `10` - Optimism
- `137` - Polygon
- `4114` - Citrea

Check `@hyperlane-xyz/registry` or chain metadata for full mapping.

## Example Investigation

User asks: "Why isn't message 0xa454... being processed?"

1. Fetch explorer: Origin=Ethereum, Dest=Citrea, not delivered
2. Query relayer logs for `0xa454...`
3. Find status: `Retry(ErrorEstimatingGas)`
4. Search error logs: `execution reverted: panic: arithmetic underflow or overflow (0x11)`
5. Report: "Message from Ethereum to Citrea is failing because the recipient contract (0xbd39...) on Citrea is reverting with an arithmetic overflow error. This is a bug in the destination contract that needs to be fixed by the contract owner."
