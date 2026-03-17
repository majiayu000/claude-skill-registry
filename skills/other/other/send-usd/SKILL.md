---
name: send-usd
description: Send USD from one agent to another.
version: 0.1.0
tags:
  - payment
  - transfer
  - usd
  - money
  - finance
  - agent-to-agent
---

# Send USD Skill

This skill initiates a USD transfer between two agents.

## Input

- **from_agent**: string - The sender agent identifier
- **to_agent**: string - The recipient agent identifier
- **amount**: number - Amount in USD to transfer (default: 1.00)
- **memo**: string (optional) - Transaction note

## Output

- **success**: boolean - Whether the transfer succeeded
- **transaction_id**: string - Unique transaction identifier
- **message**: string - Status message

## Example

**Input:**
```json
{
  "from_agent": "agentA",
  "to_agent": "agentB",
  "amount": 1.00,
  "memo": "Payment for services"
}
```

**Output (success):**
```json
{
  "success": true,
  "transaction_id": "txn_abc123",
  "message": "Successfully transferred $1.00 USD from agentA to agentB"
}
```

**Output (failure):**
```json
{
  "success": false,
  "transaction_id": null,
  "message": "Insufficient funds"
}
```

## Error Codes

- `INSUFFICIENT_FUNDS` - Not enough balance to complete transfer
- `INVALID_RECIPIENT` - Recipient agent not found
- `INVALID_AMOUNT` - Amount must be positive and at least $0.01
- `RATE_LIMITED` - Too many requests, try again later

## Security Notes

- All transfers require authentication
- Transactions are logged and auditable
- Daily transfer limits may apply
