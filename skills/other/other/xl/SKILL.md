---
name: xl
description: Explore and modify Excel workbooks interactively. Use for spreadsheet analysis, formula understanding, refactoring, and data manipulation.
allowed-tools: Bash("${CLAUDE_PLUGIN_ROOT}/bin/xl.exe":*)
---

# Excel Exploration Skill

You can interact with open Microsoft Excel workbooks using the `xl.exe` CLI tool. This enables spreadsheet exploration, formula analysis, and data modification through natural conversation.

## Session Workflow

### 1. Start by Listing Workbooks

Always begin by showing the user what workbooks are available:

```bash
"${CLAUDE_PLUGIN_ROOT}/bin/xl.exe" list
```

This returns JSON with all open Excel instances and workbooks. Each workbook has a `target_id` you'll use for subsequent commands.

### 2. Help User Select a Workbook

Present the workbooks in a readable format. Include:
- Workbook name and path
- Whether it has unsaved changes
- Which one is active (if multiple)

Even if only one workbook is open, show it and confirm with the user before proceeding.

### 3. Explore the Workbook

Once a target is selected, gather context:
- List sheets: `xl.exe sheet list --target <id>`
- List named ranges: `xl.exe name list --target <id>`
- Read specific ranges as needed

### 4. Respond to User Requests

Use the appropriate commands based on what the user wants to do. For modifications, always use `--mode rw`.

## Command Reference

### Listing and Discovery

**List all open workbooks:**
```bash
xl.exe list
```

**List sheets in a workbook:**
```bash
xl.exe sheet list --target <target_id>
```

**List named ranges:**
```bash
xl.exe name list --target <target_id>
```

**Get named range details:**
```bash
xl.exe name get --target <target_id> --name <name>
```

### Reading Data

**Read a range:**
```bash
xl.exe range read --target <target_id> --sheet <sheet_name> --a1 <range>
```

Example:
```bash
xl.exe range read --target "excel:1234:0x000A1234:wb:0" --sheet Sheet1 --a1 A1:D10
```

The output includes:
- `values`: 2D array of cell values
- `formulas`: 2D array of formulas (null for non-formula cells)
- `types`: Cell types (number, string, boolean, date_serial, error, null)

### Modifying Data (requires --mode rw)

**Write values to a range:**
```bash
echo '{"values": [[1, 2], [3, 4]]}' | xl.exe range write --mode rw --target <target_id> --sheet <sheet_name> --a1 <range>
```

**Write formulas:**
```bash
echo '{"formulas": [["=SUM(A1:A10)"], ["=AVERAGE(B1:B10)"]]}' | xl.exe range write --mode rw --target <target_id> --sheet <sheet_name> --a1 <range>
```

**Add a sheet:**
```bash
xl.exe sheet add --mode rw --target <target_id> --sheet <new_sheet_name>
```

**Rename a sheet:**
```bash
xl.exe sheet rename --mode rw --target <target_id> --sheet <old_name> --new-name <new_name>
```

**Delete a sheet:**
```bash
xl.exe sheet delete --mode rw --target <target_id> --sheet <sheet_name>
```

**Add a named range:**
```bash
xl.exe name add --mode rw --target <target_id> --name <name> --refers-to "=Sheet1!\$A\$1:\$C\$10"
```

**Delete a named range:**
```bash
xl.exe name delete --mode rw --target <target_id> --name <name>
```

**Save the workbook:**
```bash
xl.exe workbook save --mode rw --target <target_id>
```

### Calculation Control

**Check calculation mode:**
```bash
xl.exe calc status --target <target_id>
```

**Trigger calculation:**
```bash
xl.exe calc run --mode rw --target <target_id>
```

**Set calculation mode:**
```bash
xl.exe calc set --mode rw --target <target_id> --calc-mode manual
# Options: manual, automatic, automatic_except_tables
```

## Safety Guidelines

### Read-Only Mode (Default)

By default, all commands run in `--mode ro` (read-only). This guarantees:
- No writes to values, formulas, formats, or structure
- No calculation triggers
- No refresh of external data connections
- No opening or closing workbooks

### Read-Write Mode

Use `--mode rw` only when the user explicitly requests a modification. Always:
1. Confirm the intended change with the user
2. Report what was modified after the operation
3. Remind user to save if they want to keep changes

### Error Handling

Commands return JSON with `"ok": true` on success or `"ok": false` with error details:
- `NO_EXCEL_INSTANCE`: No Excel processes running
- `WORKBOOK_NOT_OPEN`: Target workbook no longer open
- `SHEET_NOT_FOUND`: Sheet name doesn't exist
- `RANGE_INVALID`: Invalid A1 reference
- `MODE_VIOLATION`: Attempted write in read-only mode

## Output Interpretation

### Cell Values
- Numbers are returned as JSON numbers
- Strings are returned as JSON strings
- Booleans are `true`/`false`
- Empty cells are `null`
- Dates are Excel serial numbers (days since 1899-12-30)

### Formulas
- Formulas include the leading `=`
- Cells without formulas show `null` in the formulas array
- Named range references in `refers_to` use the format `=Sheet!$A$1:$B$10`

## Example User Prompts

Users might ask things like:

**Exploration:**
- "Show me what workbooks are open"
- "What sheets are in this workbook?"
- "Read the data in A1:D10"
- "What's in the Summary sheet?"
- "What named ranges are defined?"
- "Show me the formulas in column B"

**Analysis:**
- "Find cells that reference Sheet2"
- "What formula is in cell C5?"
- "Show me all cells with SUM formulas"
- "Are there any circular references?"

**Modification:**
- "Add a new sheet called Results"
- "Rename Sheet1 to RawData"
- "Create a named range called SalesTotal for B2:B100"
- "Write these values to A1:C3"
- "Update the formula in D5 to use the new named range"

**Refactoring:**
- "Replace hardcoded references with named ranges"
- "Consolidate duplicate formulas"
- "Standardize the sheet naming"

When handling these requests, break down complex tasks into steps, show the user what you find, and confirm before making changes.

<!--
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Copyright (c) 2026 James Thompson
-->
