---
name: dr-drilldown
description: Drill down on a cell in the Datarails Excel Add-in to see underlying detail. Resolves DR.GET formulas (direct or through formula chains), reads hidden "dr control" sheet filters, queries Datarails for breakdown data, and validates totals before presenting results.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__list_finance_tables
  - mcp__datarails-finance-os__get_table_schema
  - mcp__datarails-finance-os__get_field_distinct_values
  - mcp__datarails-finance-os__get_sample_records
  - mcp__datarails-finance-os__get_records_by_filter
  - mcp__datarails-finance-os__aggregate_table_data
  - mcp__datarails-finance-os__execute_query
  - Read
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
argument-hint: "<cell-reference> [--by <field1,field2,...>] [--file <path-to-xlsx>]"
---

# DR.GET Drill-Down

Drill into any cell that contains Datarails data to see the underlying line-item detail. Works with:
- Cells containing a **DR.GET formula** directly
- Cells containing an **Excel formula** (SUM, +, -, etc.) whose precedents are DR.GET cells

**Requirements:** This skill requires Python with openpyxl to read Excel formulas. If openpyxl is not installed, run `pip install openpyxl` first. This skill works in Claude Code only (not Cowork).

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `<cell-reference>` | The cell to drill down on, e.g. `B6` or `Sheet1!B6` | **Required** |
| `--by <fields>` | Comma-separated list of fields to break down by (e.g. `Account Full,Vendor`) | All available fields |
| `--file <path>` | Path to the `.xlsx` workbook file | Ask user |

## Verify Connection

If any Datarails tool call fails with an authentication or connection error, tell the user:

> The Datarails connector isn't connected. Click the **"+"** button next to the prompt, select **Connectors**, find **Datarails**, and click **Connect**.

Then STOP — do not retry until the user has reconnected.

## Workflow

### Phase 0 - Open the Workbook

1. If `--file` was provided, use that path. Otherwise ask the user for the workbook path.
2. Ensure openpyxl is available. If not, install it: `pip install openpyxl`.
3. Read the workbook using Python (openpyxl) via Bash to list sheet names.
4. Confirm the target sheet exists (from the cell reference or default to the active sheet).

### Phase 1 - Resolve the Cell to DR.GET Parameters

**Goal:** Determine which DR.GET dimension filters produce the number in the target cell.

#### Step 1.1 - Read the Target Cell Formula

Use openpyxl with `data_only=False` to read the formula string from the target cell.

#### Step 1.2 - Classify the Formula

| Cell Content | Action |
|-------------|--------|
| Contains `DR.GET` | **Direct DR.GET** - parse dimension pairs. Go to Step 1.3. |
| Other formula starting with `=` | **Derived formula** - find precedent cells, check each for DR.GET. Go to Step 1.4. |
| Static number (no formula) | Tell the user this cell has no formula. Cannot drill down. Stop. |

#### Step 1.3 - Parse a DR.GET Formula

Extract all dimension/value pairs from the formula string. A DR.GET formula has the pattern:

    =DR.GET(Value, "[Dim1]", CellRef1, "[Dim2]", CellRef2, ...)

For each `CellRef`, resolve it to the actual value in that referenced cell. Open the workbook twice: once with `data_only=True` (to get cached values for referenced cells) and once with `data_only=False` (to get formulas).

Use this regex to parse dimension pairs from the formula string:

    pattern = r'"\[([^\]]+)\]"\s*,\s*(\$?[A-Z]+\$?\d+)'

For each match, group(1) is the dimension name and group(2) is the cell reference. Strip `$` from the cell reference and read the cached value from the `data_only=True` workbook.

This produces a dict like:

    {
      "DR_ACC_L1.5": {"ref": "$A6", "value": "Revenues"},
      "Scenario": {"ref": "$B$1", "value": "Actuals"},
      "Reporting Date": {"ref": "B$5", "value": 46053}
    }

Store this as the **resolved DR.GET parameters** for this cell. Go to Phase 2.

#### Step 1.4 - Trace a Derived Formula to its DR.GET Precedents

If the cell contains a non-DR.GET formula (e.g. `=B6+B7-B8`), extract all cell references from the formula and recursively check each one.

Use regex to extract cell references: `r'(?<![A-Z])(\$?[A-Z]+\$?\d+)'`

For each referenced cell:
- If it contains a DR.GET formula, parse it per Step 1.3 and record it as a leaf node with its cached value.
- If it contains another non-DR.GET formula, recurse into it.
- If it is a static value, skip it.

Build a tree structure where:
- Each leaf is a `drget` node with `params` (resolved dimensions) and `cached_value`
- Each non-leaf is a `derived` node with `formula` and `children`
- The root is the target cell

**Important:** When the target is a derived formula, the drill-down will produce **one breakdown table per DR.GET leaf**. Inform the user which DR.GET sources contribute to the number and show the breakdown for each.

**Important:** When extracting cell references from SUM ranges like `=SUM(C6:C9)`, expand the range into individual cell references: C6, C7, C8, C9. Do not treat `C6:C9` as two separate references.

### Phase 2 - Read the "dr control" Hidden Sheet for Global Filters

The Datarails Excel Add-in stores global filters in a hidden worksheet named **"dr control"** (or similar names like "DR_Control", "drcontrol"). These filters restrict what data DR.GET returns - the drill-down MUST account for them.

#### Step 2.1 - Find the Control Sheet

Search all sheet names for any containing "control" (case-insensitive). Common names: `dr control`, `DR_Control`, `drcontrol`.

#### Step 2.2 - Extract Filter JSON

The control sheet stores filter configuration as JSON strings in cells. Scan all cells for JSON content containing `FilterStorageValues`.

Each cell may contain a JSON array or object. Parse it and look for objects that have a `FilterStorageValues` key.

#### Step 2.3 - Parse Filter Definitions

Each filter object has this structure:

    {
      "Key": "global",
      "FilterStorageValues": [
        {
          "Id": 1646893,
          "Name": "Reporting Unit",
          "Type": "Text",
          "Values": ["Core"],
          "AllValues": [null, "###", "Collaborations", "Core", "DNA G", "DNA H", "LAB"],
          "IsExcluded": false,
          "IncludeNullValues": true
        }
      ]
    }

Parse each filter and build a list of **active global filters**:

| Filter Property | Meaning |
|----------------|---------|
| `Name` | The field/dimension being filtered |
| `Values` | Selected values (whitelist) |
| `AllValues` | All possible values for this field |
| `IsExcluded` | If true, `Values` is an exclusion list (blacklist) |
| `IncludeNullValues` | Whether rows with NULL in this field are included |

**If `Values` equals `AllValues`** (or `Values` is empty and `IsExcluded` is false), the filter is not restricting anything - skip it.

**If `Values` is a proper subset of `AllValues`** and `IsExcluded` is false, this is an active filter:

    Active filter: "Reporting Unit" IN ["Core"]

**If `IsExcluded` is true**, the filter means everything EXCEPT these values:

    Active filter: "Reporting Unit" NOT IN ["DNA G", "DNA H"]

Store all active filters - they must be applied to the drill-down query in Phase 3.

### Phase 3 - Query Datarails for the Breakdown

Now build and execute the aggregation query using the resolved DR.GET parameters + global filters from the control sheet.

#### Step 3.1 - Determine the Table ID

Load the client profile from `config/client-profiles/<env>.json` and use `tables.financials.id`. If no profile exists, call `list_finance_tables` to discover the financials table and ask the user to confirm.

#### Step 3.2 - Determine Drill-Down Dimensions

If the user supplied `--by <fields>`:
- Use those fields as the `dimensions` for the aggregation query.

If no `--by` was supplied:
- Use the Datarails table schema to find all categorical fields that are NOT already pinned by the DR.GET parameters.
- Common useful drill-down dimensions: `Account Full`, `Account Name`, `Report_Field`, `DR_ACC_L2`, `Vendor`, `Department L1`, `Department L2`, `Reporting Unit`, `Entity`.
- Ask the user which fields they want to break down by, suggesting the most useful ones.

#### Step 3.3 - Build the Aggregation Query

Combine:
1. **DR.GET dimension filters** (from Phase 1) - these become `filters` on the aggregation
2. **Global filters from dr control** (from Phase 2) - these become additional `filters`
3. **Drill-down dimensions** (from Step 3.2) - these become `dimensions` on the aggregation
4. **Metric:** `SUM` on `Amount` (or the appropriate value field)

Build a filters list:
- For each DR.GET parameter: `{"name": "<dim>", "values": ["<value>"], "is_excluded": false}`
- For each active global filter: `{"name": "<Name>", "values": <Values>, "is_excluded": <IsExcluded>}`

**Aggregation rules:**
- Date fields (`Reporting Date`, `Reporting Month`, etc.) must ALWAYS go in `dimensions`, never in `filters`. Date filters silently return empty results.
- To limit to a specific period, include the date as a dimension and filter the results client-side after the response.
- Only text fields (`Scenario`, `Account Group L0`, etc.) go in `filters`.

Then call `aggregate_table_data`:

    aggregate_table_data(
        table_id="<financials_table_id>",
        dimensions=["<drill-down-field-1>", "<drill-down-field-2>"],
        metrics=[{"field": "Amount", "agg": "SUM"}],
        filters=<combined_filters>
    )

**Important:** Use `aggregate_table_data` (not `get_records_by_filter` or `execute_query`) because it has NO row limit and returns properly computed totals. The other tools cap at 500-1000 rows and would return incomplete data.

#### Step 3.4 - Handle Derived Formulas (Multiple DR.GET Sources)

If the target cell was a derived formula (Phase 1, Step 1.4), run a **separate aggregation** for each DR.GET leaf node. Present each breakdown individually, showing how they combine per the original formula.

Example for `=B6-B7` where B6 = DR.GET(Revenues) and B7 = DR.GET(COGS):
- Query 1: Breakdown of Revenues by the requested fields
- Query 2: Breakdown of COGS by the requested fields
- Show both tables with a note: "Gross Profit = Revenues - COGS"

### Phase 4 - Validate the Total

**This step is CRITICAL. Never skip it.**

After receiving the aggregation results:

1. Sum all the `Amount` values in the drill-down result.
2. Compare this total to the original cell value (cached value from the workbook).
3. Check the match:

| Condition | Action |
|-----------|--------|
| Totals match (within rounding tolerance of $1) | Proceed to present results |
| Totals do NOT match | **DO NOT present the drill-down.** Diagnose the mismatch. |

#### Diagnosing a Mismatch

Common causes and fixes:

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| **Missing global filter** | The dr control sheet has a filter you did not apply | Re-read the control sheet, check for additional filter cells or sheets |
| **Wrong field mapping** | A dimension name in DR.GET does not match the Datarails field name exactly | Use `get_table_schema` to verify field names; try alternatives (e.g. `DR_ACC_L1.5` vs `DR_ACC_L1`) |
| **Date format mismatch** | Reporting Date serial number not matching | Verify the date value and format being sent |
| **IncludeNullValues not applied** | The global filter includes nulls but the query does not | Add a separate query for NULL values in that field and combine |
| **Exclusion filter reversed** | IsExcluded true was not handled correctly | Double-check: if excluded, the values should be in the exclusion list |
| **Multiple control sheet cells** | Filters are spread across multiple cells in the control sheet | Scan ALL cells, not just the first match |

If the mismatch cannot be resolved after 2 attempts:
- Tell the user the exact numbers: "The cell shows X but the drill-down totals to Y (difference of Z)."
- Explain what filters were applied.
- Ask the user if they want to see the partial results anyway, clearly flagged as unvalidated.

### Phase 5 - Present the Results

#### For Direct DR.GET Cells

Show a single table with the drill-down data:

    Drill-down: Cell B6 = $1,234,567 (Revenues, Actuals, Jan-26)
    Active global filters: Reporting Unit = "Core"

    | Account Name           | Amount      |
    |------------------------|-------------|
    | Subscription Revenue   | $1,100,000  |
    | Implementation Revenue | $134,567    |
    | **Total**              | **$1,234,567** |

    Total matches cell value.

#### For Derived Formula Cells

Show each component table plus how they combine:

    Drill-down: Cell B8 = $900,000 (Gross Profit = Revenues - COGS)

    Component 1: Revenues (Cell B6 = $1,234,567)
    | Account Name           | Amount      |
    |------------------------|-------------|
    | ...                    | ...         |

    Component 2: COGS (Cell B7 = $334,567)
    | Account Name              | Amount     |
    |---------------------------|------------|
    | ...                       | ...        |

    Gross Profit = $1,234,567 - $334,567 = $900,000

#### Formatting Rules

- Use markdown tables.
- Format numbers with commas and appropriate decimal places.
- Sort rows by absolute amount descending.
- If there are more than 30 rows, show the top 20 and summarize the rest as "Other (N items)".
- Always show the total row at the bottom.
- Always state whether the total matches the original cell value.

## Error Handling

| Error | Action |
|-------|--------|
| Workbook cannot be opened | Ask user to verify path; check file is not open exclusively in Excel |
| openpyxl not installed | Run `pip install openpyxl` and retry |
| Cell has no formula | Tell user: "This cell contains a static value (no formula). Cannot drill down." |
| No DR.GET found in formula chain | Tell user: "This cell formula does not reference any DR.GET cells. Cannot drill down." |
| No control sheet found | Warn: "No dr control sheet found. Proceeding without global filters - totals may not match if filters are applied in the add-in." |
| Table not found in Datarails | Ask user to run `/dr-learn` to set up the client profile |
| Total mismatch after retries | Report the mismatch clearly and offer partial results flagged as unvalidated |

## Examples

### Example 1: Direct DR.GET cell

    User: /dr-drilldown B6 --file budget.xlsx

Cell B6 contains `=DR.GET(Value, "[DR_ACC_L1.5]", $A6, "[Scenario]", $B$1, "[Reporting Date]", B$5)`
- Resolves: DR_ACC_L1.5=Revenues, Scenario=Actuals, Reporting Date=46053
- Reads dr control: Reporting Unit filter = "Core"
- Queries Datarails with all filters, broken down by all available fields
- Validates total, presents full breakdown

### Example 2: Drill down by specific field

    User: /dr-drilldown B6 --by "Report_Field" --file budget.xlsx

Same resolution, but only breaks down by Report_Field.

### Example 3: Derived formula (Gross Profit)

    User: /dr-drilldown B8 --file budget.xlsx

Cell B8 contains `=B6-B7` where B6 is DR.GET(Revenues) and B7 is DR.GET(COGS).
- Resolves both DR.GET sources
- Runs two separate breakdowns
- Shows both and how they combine to the Gross Profit number

### Example 4: SUM of DR.GET cells

    User: /dr-drilldown C10 --file model.xlsx

Cell C10 contains `=SUM(C6:C9)` where C6-C9 are all DR.GET cells.
- Resolves all four DR.GET sources
- Runs aggregation for each
- Shows combined breakdown with validated total
