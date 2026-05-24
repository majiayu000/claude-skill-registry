---
name: master-schedule
description: Silent setup check. Verifies canoa.json exists and the sheet is accessible. If not, copies the template sheet to the user's account and writes canoa.json. Called automatically by other skills before reading or writing product data.
allowed-tools:
  - Read
  - Write
  - Bash
  - mcp__google-sheets__list_sheets
  - mcp__google-sheets__get_sheet_data
  - mcp__google-sheets__create_spreadsheet
  - mcp__google-sheets__update_cells
user-invocable: true
---

# /master-schedule — Sheet Setup Check

**Called automatically by all product skills before reading or writing.** Can also be run manually to reconnect or reset.

Template sheet ID: `1mWnExnSWTKJv0vbu1mDnrQFmv_Iz_fNklIeuBYfMB5k`

---

## Step 1: Check for canoa.json

```bash
cat ./canoa.json 2>/dev/null
```

### Found and valid → Step 2 (verify access)
### Not found → Step 3 (auto-setup)

---

## Step 2: Verify Sheet Access

Call `mcp__google-sheets__list_sheets` with the `master_sheet_id` from `canoa.json`.

- **Success** → sheet is accessible. Return silently — the calling skill continues.
- **404 / error** → sheet was deleted or moved. Proceed to Step 3 to set up a new one.

---

## Step 3: Auto-Setup

No config found or sheet inaccessible. Set up automatically without asking the user.

### 3a: Copy the template

Attempt to copy the template sheet using the Google Drive API (`files.copy`). If a Drive MCP tool is available, use it:

```
drive.files.copy
  fileId: "1mWnExnSWTKJv0vbu1mDnrQFmv_Iz_fNklIeuBYfMB5k"
  title: "Product Library — {today's date}"
```

**If no Drive copy tool is available**, fall back to creating a new spreadsheet and writing the header row:

1. Call `mcp__google-sheets__create_spreadsheet` with title `"Product Library — {today's date}"`
2. Write the 33-column header row to `Sheet1!A1:AG1` using the CSV header from `../../schema/product-schema.md`

Note in `canoa.json` whether this was a template copy or a fresh sheet (`"setup": "copy"` or `"setup": "fresh"`).

### 3b: Identify the Products tab

Look for a tab named `Products`. If not found (e.g. fresh sheet named `Sheet1`), use whatever tab exists and record its name in `canoa.json`.

### 3c: Write canoa.json

```json
{
  "master_sheet_id": "{new sheet ID}",
  "sheet_title": "Product Library — {date}",
  "sheet_url": "https://docs.google.com/spreadsheets/d/{id}",
  "products_tab": "Products",
  "project_name": "",
  "setup": "copy",
  "created_at": "{ISO timestamp}"
}
```

### 3d: Notify the user

```
✓ Product library created and connected.
  docs.google.com/spreadsheets/d/{id}

  You may want to rename this sheet and set a project name.
  Run /master-schedule to update.
```

Then return — the calling skill continues.

---

## Manual Run

When invoked directly (`/master-schedule`), run the same flow but also:

- If `canoa.json` exists and the sheet is accessible, show current status:

```
Product library connected.

  Project:  {project_name or "(unnamed)"}
  Sheet:    {sheet_title}
  URL:      docs.google.com/spreadsheets/d/{id}
  Tab:      {products_tab}

Options:
  1. Update project name
  2. Connect a different sheet (paste URL)
  3. Reset (create a new copy of the template)
```

- If user chooses (2), ask for URL, validate, update `canoa.json`.
- If user chooses (3), run Step 3 again.

---

## MCP Connection Errors

If any MCP call fails with "tool not found" or auth error, stop and report:

```
Google Sheets MCP is not connected or not authenticated.

To connect it, add to ~/.claude/mcp_settings.json:

{
  "mcpServers": {
    "google-sheets": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-sheets"],
      "env": {
        "GOOGLE_SERVICE_ACCOUNT_KEY": "<path-to-service-account-json>"
      }
    }
  }
}

Then restart Claude Code and try again.
Need help creating a service account? Ask for instructions.
```

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| `canoa.json` exists, sheet accessible | Return silently |
| `canoa.json` exists, sheet deleted | Auto-create new copy, update `canoa.json` |
| `canoa.json` missing | Auto-create new copy, write `canoa.json` |
| Drive copy tool not available | Fall back to fresh sheet + header row |
| MCP not connected | Stop, show setup instructions |
