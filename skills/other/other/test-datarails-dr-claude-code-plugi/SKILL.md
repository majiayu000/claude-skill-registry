---
name: dr-test
description: Test API field compatibility and performance. Discovers which fields work with aggregation, suggests alternatives for failed fields, and updates the client profile automatically.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__list_finance_tables
  - mcp__datarails-finance-os__get_table_schema
  - mcp__datarails-finance-os__aggregate_table_data
  - mcp__datarails-finance-os__get_sample_records
  - Write
  - Read
  - Bash
argument-hint: ""
---

# API Diagnostic & Field Compatibility Test

Test which fields work with the aggregation API for a specific environment. Discovers field compatibility, suggests alternatives for failed fields, and updates the client profile with `aggregation` hints.

## Purpose

The Datarails aggregation API works for most fields (~212/220) but some fields fail per-client (500 errors). This skill:
1. Tests each mapped field from the client profile against aggregation
2. Reports pass/fail with timing
3. Discovers alternative fields for those that fail
4. Updates the client profile's `aggregation` section automatically

## Arguments

No arguments required. Uses the currently authenticated environment.

## Client Profile System

This skill reads AND writes to client profiles at `config/client-profiles/<env>.json`.

### What It Reads
- `tables.financials.id` - Table to test against
- `field_mappings.*` - Fields to test

### What It Writes
- `aggregation.supported` - Whether aggregation works at all
- `aggregation.failed_fields` - List of actual field names that fail
- `aggregation.field_alternatives` - Map of semantic name to working alternative
- `aggregation.tested_at` - When the test was run

## Workflow

### Phase 1: Setup

#### Step 1: Verify Connection

If any Datarails tool call fails with an authentication or connection error, tell the user:

> The Datarails connector isn't connected. Click the **"+"** button next to the prompt, select **Connectors**, find **Datarails**, and click **Connect**.

Then STOP — do not retry until the user has reconnected.

#### Step 2: Load Client Profile
```
Read: config/client-profiles/<env>.json

If profile exists:
  - Load table IDs and field mappings
  - Continue to testing

If profile does NOT exist:
  - Inform user: "No profile found for '<env>'. Run '/dr-learn --env <env>' first."
  - Stop execution
```

### Phase 2: Discovery

#### Step 3: Get Full Schema
```
Use: mcp__datarails-finance-os__get_table_schema
table_id: <financials_table_id>
```

Build a list of all categorical/string fields to test. Include:
- All fields from `field_mappings` in the profile
- Any additional categorical fields from the schema not yet mapped

#### Step 4: Build Test Plan

Create a list of fields to test. Priority order:
1. `scenario` field (from profile)
2. `date` field
3. `account_l0` field
4. `account_l1` field
5. `account_l2` field
6. `department_l1` field
7. `cost_center` field (if mapped)
8. Any other categorical fields from schema (look for fields with "L1.5", "L1_5", similar names that might be alternatives)

### Phase 3: Aggregation Testing

#### Step 5: Test Each Field

**Aggregation rules:**
- Date fields (`Reporting Date`, `Reporting Month`, etc.) must ALWAYS go in `dimensions`, never in `filters`. Date filters silently return empty results.
- To limit to a specific period, include the date as a dimension and filter the results client-side after the response.
- Only text fields (`Scenario`, `Account Group L0`, etc.) go in `filters`.

For each field, run:
```
Use: mcp__datarails-finance-os__aggregate_table_data
Parameters:
  table_id: <financials_table_id>
  dimensions: ["<field_name>"]
  metrics: [{"field": "<amount_field>", "agg": "SUM"}]
  filters: [
    {"name": "<scenario_field>", "values": ["Actuals"], "is_excluded": false}
  ]
```

Record for each field:
- **Status:** PASS or FAIL
- **Groups returned:** Number of distinct values (if PASS)
- **Error:** Error message (if FAIL)

#### Step 6: Identify Alternatives

For each failed field (especially account_l1, account_l2):
- Look for similar fields in the schema (e.g., "DR_ACC_L1.5", "Account L1 Alt")
- Test those alternatives
- If an alternative works, record the mapping

### Phase 4: Profile Update

#### Step 7: Update Client Profile

Read the current profile, add/update the `aggregation` section:

```json
{
  "aggregation": {
    "supported": true,
    "failed_fields": ["<actual_field_1>", "<actual_field_2>"],
    "field_alternatives": {
      "account_l1": "account_l1_5",
      "account_l2": "account_l1_5"
    },
    "tested_at": "<ISO 8601 timestamp>"
  }
}
```

If new alternative fields are discovered, also add them to `field_mappings`:
```json
{
  "field_mappings": {
    "account_l1_5": "DR_ACC_L1.5"
  }
}
```

Write the updated profile:
```
Use: Write
file_path: config/client-profiles/<env>.json
content: <updated_profile_json>
```

#### Step 8: Generate Diagnostic Report

Save a detailed report to `tmp/`:

```
Use: Write
file_path: tmp/API_Diagnostic_<env>_<timestamp>.txt
```

### Phase 5: Present Results

#### Step 9: Show Summary

Display results:

```
API Diagnostic Results
======================
Environment: <env> (<display_name>)
Table: <table_name> (ID: <table_id>)

Aggregation Tests:
  [PASS]  Scenario         -> 4 groups
  [PASS]  Reporting Date   -> 101 groups
  [PASS]  DR_ACC_L0        -> 5 groups
  [FAIL]  DR_ACC_L1        -> 500 error
  [FAIL]  DR_ACC_L2        -> 500 error
  [PASS]  DR_ACC_L1.5      -> 18 groups
  [PASS]  Department L1    -> 3 groups
  [PASS]  Cost Center      -> 24 groups

Result: 6/8 fields work (75%)

Alternatives Discovered:
  account_l1 -> account_l1_5 (DR_ACC_L1.5, 18 groups)
  account_l2 -> account_l1_5 (DR_ACC_L1.5, 18 groups)

Profile updated: config/client-profiles/<env>.json
Report saved: tmp/API_Diagnostic_<env>_<timestamp>.txt

Impact:
  - /dr-intelligence will use DR_ACC_L1.5 instead of DR_ACC_L1 (~5s vs ~10min)
  - /datarails-finance-os:financial-summary will show real aggregated totals
  - All commands will prefer aggregation where fields are supported
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No profile found | Run `/dr-learn` first |
| All fields fail | Aggregation API may not work in this environment; commands will use pagination |
| Auth expires during testing | Tests run sequentially, each ~5s; re-auth if needed |
| New fields not detected | Re-run `/dr-learn` to refresh the schema, then `/dr-test` |

## Related Skills

- `/dr-learn` - Creates the profile that this skill tests
- Connect via Connectors UI before testing
- `/dr-intelligence` - Uses the aggregation hints from the profile
