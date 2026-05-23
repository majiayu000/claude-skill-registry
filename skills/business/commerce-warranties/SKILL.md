---
name: commerce-warranties
description: Manage warranties and claims. Use when running `stateset-warranties` or handling warranty/RMA flows.
---

# Commerce Warranties

Track warranty coverage and process claims.

## How It Works

1. Create warranties for orders or products.
2. Submit claims with issue details.
3. Approve or deny claims and record resolution.
4. Report warranty status and costs.

## Usage

- CLI: `stateset-warranties ...`
- Writes require `--apply`.
- MCP tools: `list_warranties`, `create_warranty`, `create_warranty_claim`, `approve_warranty_claim`.

## Output

```json
{"status":"approved","claim_id":"claim_123","resolution":"replace"}
```

## Present Results to User

- Warranty or claim identifiers and status.
- Resolution details (repair, replace, refund).
- Any follow-up actions required.

## Troubleshooting

- Warranty expired: confirm coverage dates.
- Claim already exists: show the open claim.

## References
- references/warranties-flow.md
- /home/dom/stateset-icommerce/cli/.claude/agents/warranties.md
