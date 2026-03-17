---
name: bulk-promo-order
description: Create multiple promo orders from a spreadsheet or list
user-invocable: true
---

You are helping the sales team create multiple promotional orders at once.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+promo-order` to load the promo-order MCP tools. All tools below are prefixed with `mcp__promo-order__` (e.g., `mcp__promo-order__parse_bulk_orders`).

Follow these steps:

### Step 1: Get the Order List

Ask the user for the order data. Accept formats:
- Pasted CSV/TSV data
- Path to a local CSV file (read and paste contents)
- Markdown table
- Natural language list (e.g., "Send GO sampler to John at 123 Main St")

Expected columns (flexible naming):
- Customer name or email (required)
- Address fields (required for new customers)
- Products and quantities (optional if using a preset)
- Notes (optional)

### Step 2: Collect Required Tracking Fields

Call `mcp__promo-order__list_metafield_options` to get valid values for:
- **internal_requestor** — who is requesting this batch
- **promo_order_type** — the purpose (e.g., "Wholesale/DSD Account Sampling", "Trade Shows and Events")

Present the options and ask the user to select one of each. These are required on every batch.

### Step 3: Check Product Presets

Call `mcp__promo-order__list_product_presets` to show available presets (pre-configured product bundles like "GO sampler pack"). If the user's data doesn't specify products, ask if they want to apply a preset.

### Step 4: Parse the Batch

Call `mcp__promo-order__parse_bulk_orders` with:
- `text`: the raw order data from Step 1
- `preset`: the selected preset handle (if using one)

This parses the input, resolves customers, validates addresses, and returns a batch ID with a preview.

### Step 5: Review the Batch

Call `mcp__promo-order__review_bulk_batch` with the batch ID from Step 4.

Present the validation results:
- Total orders: N
- Valid: N (ready to submit)
- Errors: N (with details per row)

If there are errors, show them and ask the user whether to proceed with valid rows only, fix issues, or cancel.

### Step 6: Execute or Cancel

**If user confirms**, call `mcp__promo-order__confirm_bulk_batch` with:
- `batch_id`: from Step 4
- `preset`: if using one
- `internal_requestor`: from Step 2
- `promo_order_type`: from Step 2
- `complete_orders`: ask user — `true` sends directly to 3PL, `false` creates drafts for review

**If user cancels**, call `mcp__promo-order__cancel_bulk_batch` with the batch ID.

### Step 7: Report Results

Present a results summary:
- Customer | Order ID | Status | Notes
- Summary: N created, N failed, N skipped

If orders were created as drafts, remind the user to approve them via `/jf-sales-command:approve-orders`.

### Error Handling

- If MCP tools are unavailable, stop and inform the user
- If more than 50% of rows have errors after parsing, pause and suggest the user review source data
- If `confirm_bulk_batch` fails, show the error and suggest retrying or cancelling
