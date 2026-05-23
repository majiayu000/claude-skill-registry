---
name: commerce-customers
description: Manage customer records and profiles in StateSet iCommerce. Use when listing, getting, or creating customers, looking up by email, or running `stateset-direct customers`.
---

# Commerce Customers

Manage customer identity and profile data used across orders, carts, and analytics.

## How It Works

1. Find customers by email or ID.
2. Create or update customer records.
3. Use customer IDs for orders and carts.
4. Report counts or segments as needed.

## Usage

- CLI: `stateset "list customers"` or `stateset-direct customers <action>`
- Writes require `--apply`.
- MCP tools: `list_customers`, `get_customer`, `create_customer`.

## Output

```json
{"status":"ok","customer_id":"cust_123","email":"customer@example.com"}
```

## Present Results to User

- Customer identifiers and key fields updated.
- Any validation or deduping performed.
- Next steps (orders, carts, or segmentation).

## Troubleshooting

- Customer not found: verify email or ID and search again.
- Duplicate email: merge or update the existing record.

## References
- references/customer-commands.md
- /home/dom/stateset-icommerce/examples/cli-reference.md
- /home/dom/stateset-icommerce/cli/src/tools/customers.js
