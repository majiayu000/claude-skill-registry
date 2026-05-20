---
name: salesforce-crm-ops
description: "Operate Salesforce as the VC associate CRM: authenticate via OAuth, query with SOQL, upsert Leads/Accounts, create Opportunities, and log Activities/Tasks for dealflow and portfolio support. Includes field mapping configuration and dry-run mode."
license: Proprietary
compatibility: Requires internet access and Salesforce REST API credentials; scripts require Python 3 + requests.
metadata:
  author: evalops
  version: "0.2"
---
# Salesforce CRM ops

## When to use
Use this skill when you need to:
- Create or update Leads/Accounts/Opportunities for dealflow
- Log meetings, diligence calls, and next steps as Activities/Tasks
- Query Salesforce for pipeline, duplicates, and coverage
- Automate basic CRM hygiene via scripts
- Validate your field mappings before running in production

## Compatibility / assumptions
This skill assumes:
- You have Salesforce REST API access and a Connected App.
- You can obtain an access token via OAuth (client credentials or another flow).
- You know your instance base URL (e.g., `https://yourdomain.my.salesforce.com`).

## Required environment variables
Set:
- `SF_BASE_URL` (e.g., `https://yourdomain.my.salesforce.com`)
- `SF_CLIENT_ID`
- `SF_CLIENT_SECRET`

Optional:
- `SF_API_VERSION` (default `v59.0` if omitted)
- `SF_ACCESS_TOKEN` (if you already have one)

## Configuration files (REQUIRED for production use)

### config/field_map.yaml
Every org has different field names and custom objects. Before running any create/update operations, create this file:

```yaml
# Field mappings: skill field name -> Salesforce API field name
lead:
  email: Email
  first_name: FirstName
  last_name: LastName
  company: Company
  title: Title
  website: Website
  status: Status
  source: LeadSource
  thesis_tag: Thesis_Tag__c  # Custom field - adjust to your org
  signal_score: Signal_Score__c  # Custom field - adjust to your org
  must_be_true: Must_Be_True__c  # Custom field - adjust to your org
  pass_reason: Pass_Reason__c  # Custom field - adjust to your org

account:
  name: Name
  website: Website
  description: Description
  thesis_tag: Thesis_Tag__c

opportunity:
  name: Name
  stage: StageName
  close_date: CloseDate
  amount: Amount
  next_step: NextStep
  probability: Probability

task:
  subject: Subject
  due_date: ActivityDate
  status: Status
  priority: Priority
  what_id: WhatId
  who_id: WhoId

activity:
  subject: Subject
  description: Description
  what_id: WhatId
  who_id: WhoId
```

### config/stages.yaml
Map your firm's deal stages to Salesforce picklist values:

```yaml
# Stage mappings: logical stage -> Salesforce StageName picklist value
opportunity_stages:
  sourced: "Sourced"
  first_meeting: "First Meeting"
  diligence: "Diligence"
  ic_scheduled: "IC Scheduled"
  term_sheet: "Term Sheet"
  closed_won: "Closed Won"
  passed: "Passed"

lead_statuses:
  new: "Open - Not Contacted"
  contacted: "Working - Contacted"
  qualified: "Qualified"
  meeting_scheduled: "Meeting Scheduled"
  passed: "Closed - Not Converted"

task_statuses:
  not_started: "Not Started"
  in_progress: "In Progress"
  completed: "Completed"
  waiting: "Waiting on someone else"
```

### config/required_fields.yaml
Document required fields for your org to prevent API errors:

```yaml
# Required fields per object (discover these with schema command)
lead:
  - LastName
  - Company
  - Status

opportunity:
  - Name
  - StageName
  - CloseDate

task:
  - Subject
```

## Core workflows

### 0) Schema discovery (RUN THIS FIRST)
Before creating any records, discover your org's schema:

```bash
# Describe Lead object - shows all fields, required fields, picklist values
python3 scripts/sf_describe.py Lead

# Describe Opportunity object
python3 scripts/sf_describe.py Opportunity

# Describe all relevant objects and save to file
python3 scripts/sf_describe.py Lead Account Opportunity Task Event --output config/schema.json
```

This will show:
- All available fields
- Required fields
- Picklist values (for Status, StageName, etc.)
- Field types and constraints

**Use this output to populate your config/*.yaml files.**

### 1) Dry-run mode (ALWAYS USE FIRST)
Every write operation supports `--dry-run` flag:

```bash
# See what would be created without actually creating
python3 scripts/sf_upsert_lead.py --dry-run \
  --email founder@company.com \
  --first "Ada" --last "Lovelace" \
  --company "ExampleAI"

# Validate opportunity creation
python3 scripts/sf_create_opportunity.py --dry-run \
  --name "ExampleAI Seed" \
  --stage "Qualification" \
  --close-date "2026-03-31"
```

Dry-run will:
- Validate all required fields are present
- Check picklist values against schema
- Show the exact API request that would be made
- NOT create or modify any records

### 2) Get an access token (OAuth client credentials)
Preferred for server-to-server integrations:
- POST to: `https://<mydomain>.my.salesforce.com/services/oauth2/token`
- Use grant type `client_credentials` (or whatever your org allows)

If your org uses a different OAuth flow, adapt accordingly.

### 3) Query Salesforce (SOQL)
Use the Query resource:
- `GET /services/data/vXX.X/query/?q=<SOQL>`

Reminder: encode spaces as `+` or `%20` in URLs.

### 4) Upsert by external ID (PREFERRED)
To avoid duplicates, upsert by a stable external ID rather than creating blind:

```bash
# Upsert by email (if Email is an external ID field)
python3 scripts/sf_upsert_lead.py --external-id Email \
  --email founder@company.com \
  --first "Ada" --last "Lovelace" \
  --company "ExampleAI"

# Upsert by custom external ID field
python3 scripts/sf_upsert_lead.py --external-id External_ID__c \
  --external-id-value "company-123" \
  --first "Ada" --last "Lovelace" \
  --company "ExampleAI"
```

### 5) Create an Opportunity for a deal
Minimum fields depend on your org (check config/required_fields.yaml):

```bash
python3 scripts/sf_create_opportunity.py \
  --name "ExampleAI Seed" \
  --stage "First Meeting" \
  --close-date "2026-03-31" \
  --account-id "001XXXXXXXXXXXX"
```

### 6) Log Activities / Tasks
Create a Task with next step:

```bash
python3 scripts/sf_create_task.py \
  --subject "Follow up: send customer intro" \
  --due-date "2026-02-05" \
  --what-id "006XXXXXXXXXXXX" \
  --status "Not Started"
```

## Scripts

### Core scripts
- `scripts/sf_oauth_client_credentials.py` - Get access token
- `scripts/sf_query.py` - Run SOQL queries
- `scripts/sf_describe.py` - Schema discovery (NEW)
- `scripts/sf_upsert_lead.py` - Create/update Lead
- `scripts/sf_create_opportunity.py` - Create Opportunity
- `scripts/sf_create_task.py` - Create Task

### Script flags (all scripts support these)
- `--dry-run` - Validate without executing
- `--config` - Path to config directory (default: `./config`)
- `--verbose` - Show detailed API requests/responses

## Safety / hygiene rules
- **Always run `--dry-run` first** when testing new operations.
- **Run schema discovery** before configuring a new org.
- Prefer upsert by stable identifiers (email, domain) to avoid duplicates.
- Keep notes factual (assume audits).
- Record next step with a due date; otherwise the CRM is dead.
- Every pass must have a pass reason and "what would change our mind."

## Examples

### First-time setup for a new org
```bash
# 1. Get token
python3 scripts/sf_oauth_client_credentials.py

# 2. Discover schema
python3 scripts/sf_describe.py Lead Account Opportunity Task --output config/schema.json

# 3. Review output and create config files
# Edit config/field_map.yaml, config/stages.yaml, config/required_fields.yaml

# 4. Test with dry-run
python3 scripts/sf_upsert_lead.py --dry-run --email test@example.com --first "Test" --last "User" --company "TestCo"

# 5. Run for real
python3 scripts/sf_upsert_lead.py --email test@example.com --first "Test" --last "User" --company "TestCo"
```

### Query leads by email
```bash
python3 scripts/sf_query.py "SELECT Id, Name, Email, Company FROM Lead WHERE Email='founder@company.com' LIMIT 5"
```

### Upsert a lead with thesis tagging
```bash
python3 scripts/sf_upsert_lead.py \
  --email founder@company.com \
  --first "Ada" --last "Lovelace" \
  --company "ExampleAI" \
  --title "CEO" \
  --website "https://example.ai" \
  --status "Open - Not Contacted" \
  --thesis-tag "AI Security" \
  --signal-score 4 \
  --must-be-true "Enterprise buyers will pay for automated security posture management"
```

### Create an opportunity with full context
```bash
python3 scripts/sf_create_opportunity.py \
  --name "ExampleAI Seed" \
  --stage "First Meeting" \
  --close-date "2026-03-31" \
  --next-step "Schedule diligence calls" \
  --amount 2000000
```

## Troubleshooting

### "Required field missing" error
Run schema discovery to see what's required:
```bash
python3 scripts/sf_describe.py Lead | grep -A5 "required"
```

### "Invalid picklist value" error
Run schema discovery to see valid picklist values:
```bash
python3 scripts/sf_describe.py Opportunity | grep -A20 "StageName"
```

### "Duplicate detected" error
Use upsert with external ID instead of create:
```bash
python3 scripts/sf_upsert_lead.py --external-id Email --email founder@company.com ...
```
