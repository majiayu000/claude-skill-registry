---
name: crm-sync
description: Sync leads from Zoho CRM into the local SQLite database. Fetches all leads, performs upserts with change detection, and maintains full audit history.
allowed-tools:
  - Bash
  - Read
  - mcp__zoho-crm__ZohoCRM_Get_Records
---

# crm-sync (CRM Lead Sync)

Synchronise leads from Zoho CRM into the local SQLite database.

## Database

- **Path**: `raw/crm/crm.db`
- **Schema**: `scripts/crm/db_schema.sql`

### Tables

**leads** (current state):
- id (TEXT PRIMARY KEY) - Zoho record ID
- first_name, last_name, company, email, phone, lead_source, description
- created_at, updated_at - local timestamps
- zoho_modified_time - Modified_Time from Zoho

**leads_history** (audit trail):
- All lead fields plus captured_at and change_type ('insert', 'update', 'delete')

**sync_log** (sync metadata):
- started_at, completed_at, records_fetched, records_inserted, records_updated, status, error_message

## Procedure

### Step 1: Initialise Database

Ensure the database exists with correct schema:

```bash
mkdir -p raw/crm
sqlite3 raw/crm/crm.db < scripts/crm/db_schema.sql
```

### Step 2: Start Sync Log

```bash
sqlite3 raw/crm/crm.db "INSERT INTO sync_log (started_at, status) VALUES (datetime('now'), 'running'); SELECT last_insert_rowid();"
```

Save the returned ID for later update.

### Step 3: Fetch Leads from Zoho

Use `mcp__zoho-crm__ZohoCRM_Get_Records`:
- module: "Leads"
- fields: "id,First_Name,Last_Name,Company,Email,Phone,Lead_Source,Description,Modified_Time"

Handle pagination if more than one page of results.

### Step 4: Upsert Each Lead

For each lead returned from Zoho:

**4a. Check if exists:**
```bash
sqlite3 raw/crm/crm.db "SELECT id, zoho_modified_time FROM leads WHERE id = '{lead_id}';"
```

**4b. If new lead** (not in database):
```bash
sqlite3 raw/crm/crm.db "
INSERT INTO leads (id, first_name, last_name, company, email, phone, lead_source, description, created_at, updated_at, zoho_modified_time)
VALUES ('{id}', '{first_name}', '{last_name}', '{company}', '{email}', '{phone}', '{lead_source}', '{description}', datetime('now'), datetime('now'), '{modified_time}');

INSERT INTO leads_history (lead_id, first_name, last_name, company, email, phone, lead_source, description, captured_at, change_type)
VALUES ('{id}', '{first_name}', '{last_name}', '{company}', '{email}', '{phone}', '{lead_source}', '{description}', datetime('now'), 'insert');
"
```

**4c. If existing and Zoho version is newer** (compare zoho_modified_time):
```bash
sqlite3 raw/crm/crm.db "
-- Capture old version to history
INSERT INTO leads_history (lead_id, first_name, last_name, company, email, phone, lead_source, description, captured_at, change_type)
SELECT id, first_name, last_name, company, email, phone, lead_source, description, datetime('now'), 'update'
FROM leads WHERE id = '{id}';

-- Update the lead
UPDATE leads SET
  first_name = '{first_name}',
  last_name = '{last_name}',
  company = '{company}',
  email = '{email}',
  phone = '{phone}',
  lead_source = '{lead_source}',
  description = '{description}',
  updated_at = datetime('now'),
  zoho_modified_time = '{modified_time}'
WHERE id = '{id}';
"
```

**4d. If unchanged** (same or older zoho_modified_time): Skip.

### Step 5: Update Sync Log

On success:
```bash
sqlite3 raw/crm/crm.db "
UPDATE sync_log SET
  completed_at = datetime('now'),
  records_fetched = {fetched},
  records_inserted = {inserted},
  records_updated = {updated},
  status = 'completed'
WHERE id = {sync_id};
"
```

On failure:
```bash
sqlite3 raw/crm/crm.db "
UPDATE sync_log SET
  completed_at = datetime('now'),
  status = 'failed',
  error_message = '{error}'
WHERE id = {sync_id};
"
```

### Step 6: Report Results

Output a summary:
- Records fetched
- New leads inserted
- Existing leads updated
- Unchanged (skipped)
- Any errors

## Field Mapping

| Zoho Field     | Database Column      |
|----------------|----------------------|
| id             | id                   |
| First_Name     | first_name           |
| Last_Name      | last_name            |
| Company        | company              |
| Email          | email                |
| Phone          | phone                |
| Lead_Source    | lead_source          |
| Description    | description          |
| Modified_Time  | zoho_modified_time   |

## Error Handling

- If MCP credentials are missing: Report what's needed
- If API rate limits hit: Wait and retry, or report partial progress
- If database errors occur: Log to sync_log with error_message
- Always update sync_log status even on failure

## Privacy

- Do not display full email addresses or phone numbers in output
- Show redacted summaries unless user explicitly requests full details
