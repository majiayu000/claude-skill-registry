---
name: salesforce-cli
description: >
  Safety-first Salesforce CLI skill wrapping `sf` (v2). This skill should be used when
  performing Salesforce operations — SOQL/SOSL queries, metadata deploy/retrieve, data
  import/export, Apex execution, org management, auth, and platform events. Enforces
  risk classification w/ mandatory confirmation for all write/destructive operations.
  Integrates w/ Salesforce MCP servers and file-converter skill for format conversion.
author: George Khananaev
---

# Salesforce CLI

Safety-first wrapper for Salesforce CLI (`sf` v2). Every command is classified by risk level before execution. **NEVER modify Salesforce data or metadata without explicit user permission.**

## When to Use

- User asks to query Salesforce data (SOQL/SOSL)
- User asks to deploy or retrieve metadata
- User asks to export/import data (CSV, JSON, tree)
- User asks to execute Apex code
- User asks to manage orgs (scratch, sandbox, production)
- User asks to authenticate w/ Salesforce
- User asks to work w/ platform events or CDC
- User asks to manage packages or permissions
- User asks to interact w/ Salesforce APIs (REST, Bulk, Tooling)

## Prerequisites

1. **Install:** `npm install -g @salesforce/cli` or `brew install sf`
2. **Auth:** `sf org login web` (interactive) or `sf org login jwt` (CI/CD)
3. **Verify:** `sf --version` (requires v2.x)
4. **Default org:** `sf config set target-org <alias>`

## Safety Model

Every `sf` command falls into one of four risk tiers. **Default mode is read-only.**

| Tier | Action Required | Examples |
|------|----------------|----------|
| **Safe** | Execute immediately | `sf org list`, `sf data query`, `sf project retrieve preview` |
| **Write** | `AskUserQuestion` BEFORE executing | `sf data create record`, `sf project deploy start --dry-run` |
| **Destructive** | `AskUserQuestion` w/ explicit consequences | `sf project deploy start`, `sf data delete`, `sf org delete` |
| **Forbidden** | Multi-step validation, NEVER auto-confirm | Bulk delete in production, mass data wipe, production org delete |

See [references/safety-rules.md](references/safety-rules.md) for full classification and confirmation templates.

### Production Guardrails

Detect org type before ANY write operation:

```bash
sf org display --target-org <alias> --json
```

Check `instanceUrl` and `isScratch`/`isSandbox` fields:
- `login.salesforce.com` or no sandbox/scratch flag → **PRODUCTION** → extra confirmation required
- `test.salesforce.com` or `isSandbox: true` → **Sandbox**
- `isScratch: true` → **Scratch org**

**For production orgs:** ALL write operations require AskUserQuestion w/ org alias typed confirmation.

### Fail-Safe Principles

1. **If org type detection fails → BLOCK all operations** (never assume non-production)
2. **If unsure about tier → classify HIGHER** (Write → Destructive, Destructive → Forbidden)
3. **Bulk operations always require row count preview** before confirmation
4. **Deploys with `destructiveChanges.xml` are FORBIDDEN** in production via scripts
5. **`--test-level NoTestRun` is BLOCKED** for production deployments
6. **Apex code must be shown** to user BEFORE execution (never run sight-unseen)
7. **Permission set changes** require warning about privilege escalation / lockout risks
8. **Field/object deletions in deploys** require warning about cascade impacts (reports, flows, integrations)
9. **Sandbox refresh** requires explicit acknowledgment that ALL data will be overwritten
10. **PII fields** in queries trigger a warning (Email, Phone, Birthdate, SSN, etc.)

## Decision Flow

```
Command received
  → Detect target org type (prod/sandbox/scratch)
  → Classify risk tier (see Quick Reference)
  → Safe?        Execute immediately
  → Write?       AskUserQuestion → wait for answer → execute or cancel
  → Destructive? AskUserQuestion w/ consequences → wait → execute or cancel
  → Forbidden?   Warn → require typed confirmation → final confirm → execute or cancel
  → PRODUCTION?  Add extra confirmation step regardless of tier
```

## Quick Reference

### Safe (read-only, execute immediately)

| Command | Description |
|---------|-------------|
| `sf org list` | List authorized orgs |
| `sf org list --all` | Include expired scratch orgs |
| `sf org display` | Display org info |
| `sf org open` | Open org in browser |
| `sf config list` | List config values |
| `sf config get target-org` | Get default org |
| `sf alias list` | List aliases |
| `sf data query --query "..."` | SOQL query (w/ mandatory LIMIT) |
| `sf data search --query "..."` | SOSL search |
| `sf data get record` | Get single record |
| `sf project retrieve preview` | Preview what would be retrieved |
| `sf project deploy preview` | Preview what would be deployed |
| `sf apex list log` | List debug logs |
| `sf apex get log` | Get debug log content |
| `sf apex tail log` | Tail logs in real-time |
| `sf api request rest` (GET) | Read-only REST API calls |
| `sf limits api display` | Display API limits |
| `sf schema generate sobject` | Describe object schema |
| `sf package list` | List packages |
| `sf package version list` | List package versions |
| `sf plugins list` | List installed plugins |
| `sf doctor` | Run diagnostics |
| `sf auth list` | List auth connections |

### Write (AskUserQuestion required)

| Command | Description |
|---------|-------------|
| `sf data create record` | Create a single record |
| `sf data update record` | Update a single record |
| `sf data import tree` | Import data from tree files |
| `sf project deploy start --dry-run` | Validate deployment (no changes) |
| `sf project retrieve start` | Retrieve metadata to local |
| `sf org create scratch` | Create scratch org |
| `sf alias set` | Set an alias |
| `sf config set` | Set config value |
| `sf package create` | Create a package |
| `sf package version create` | Create package version |

### Destructive (AskUserQuestion w/ consequences)

| Command | Description |
|---------|-------------|
| `sf project deploy start` (no dry-run) | Deploy metadata (modifies org) |
| `sf data delete record` | Delete a single record |
| `sf data delete bulk` | Bulk delete records |
| `sf data update bulk` | Bulk update records — can corrupt data at scale |
| `sf data import bulk` | Bulk import — can create thousands of duplicate records |
| `sf data upsert bulk` | Bulk upsert — incorrect key can overwrite wrong records |
| `sf apex run` | Execute anonymous Apex |
| `sf org delete scratch` | Delete scratch org |
| `sf org delete sandbox` | Delete sandbox |
| `sf org create sandbox` | Create sandbox (long-running, uses resources) |
| `sf org assign permset` | Assign permission set — can escalate privileges or lock users out |
| `sf package install` | Install package — can modify schema, automation, and data |
| `sf package uninstall` | Uninstall package |
| `sf org logout` | Remove org auth |
| `sf api request rest -X POST/PUT/PATCH/DELETE` | Write/delete REST API calls |

### Forbidden (multi-step validation)

| Command | Description |
|---------|-------------|
| `sf org delete` targeting production | Delete production org connection |
| Bulk delete in production | Mass data deletion in production |
| `sf data delete bulk` w/o WHERE in source query | Full-table data wipe risk |
| `sf project deploy start` w/ `destructiveChanges.xml` in prod | Deploy destructive metadata changes to production |
| `sf project deploy start --test-level NoTestRun` in prod | Skip tests in production (BLOCKED) |
| `sf org refresh sandbox` | Refresh sandbox — overwrites ALL data and customizations |
| `sf org logout --all` | Remove ALL org auth — can break CI/CD pipelines |
| Bulk loops w/o limits | Any loop running delete/update w/o LIMIT |
| `sf apex run` in production w/o review | Execute unreviewed Apex in production |
| Dangerous deploy flags in prod | `--ignore-conflicts`, `--ignore-warnings`, `--purge-on-delete` |

## SOQL/SOSL Query Safety

**Mandatory rules for ALL queries:**

1. **Always add LIMIT** — Default to `LIMIT 200` if user omits
2. **Never use `SELECT *`** — Expand fields via `sf schema generate sobject` or ask user
3. **Production queries** — Require WHERE clause unless object is known to be small
4. **Tooling API queries** — Use `--use-tooling-api` flag for metadata queries

```bash
# Safe SOQL query
sf data query --target-org my-org \
  --query "SELECT Id, Name, Industry FROM Account WHERE Industry = 'Technology' LIMIT 100"

# SOQL w/ relationships
sf data query --target-org my-org \
  --query "SELECT Id, Name, (SELECT Id, FirstName FROM Contacts) FROM Account LIMIT 50"

# SOQL w/ output format
sf data query --target-org my-org \
  --query "SELECT Id, Name FROM Account LIMIT 100" \
  --result-format csv --output-file accounts.csv

# Tooling API query
sf data query --target-org my-org --use-tooling-api \
  --query "SELECT Id, Name FROM ApexClass WHERE Name LIKE '%Test%' LIMIT 50"

# SOSL search
sf data search --target-org my-org \
  --query "FIND {Acme} IN NAME FIELDS RETURNING Account(Id, Name LIMIT 50)"
```

See [references/soql-sosl.md](references/soql-sosl.md) for query patterns, date literals, and aggregate examples.

## Data Export/Import

### Export (Safe tier — read-only)

```bash
# CSV export
sf data query --target-org my-org \
  --query "SELECT Id, Name FROM Account LIMIT 200" \
  --result-format csv --output-file accounts.csv

# JSON export
sf data query --target-org my-org \
  --query "SELECT Id, Name FROM Account LIMIT 200" \
  --json > accounts.json

# Tree export (preserves relationships)
sf data export tree --target-org my-org \
  --query "SELECT Id, Name, (SELECT Id, FirstName FROM Contacts) FROM Account LIMIT 50" \
  --output-dir ./data

# Bulk export (large datasets)
sf data export bulk --target-org my-org \
  --query "SELECT Id, Name FROM Account" \
  --output-file accounts.csv
```

### Import (Write/Destructive tier — confirmation required)

```bash
# Tree import (Write)
sf data import tree --target-org my-org --files Account.json,Contact.json

# Bulk import (Write)
sf data import bulk --sobject Account --file accounts.csv --target-org my-org

# Bulk upsert (Write)
sf data upsert bulk --sobject Account --file data.csv \
  --external-id External_Id__c --target-org my-org
```

### File-Converter Integration

Convert between formats using the `file-converter` skill:

```bash
# Salesforce JSON → CSV (for spreadsheets)
python3 .claude/skills/file-converter/scripts/csv_json_yaml.py accounts.json accounts.csv

# CSV → JSON (for API import)
python3 .claude/skills/file-converter/scripts/csv_json_yaml.py data.csv data.json

# JSON → YAML (for config/review)
python3 .claude/skills/file-converter/scripts/csv_json_yaml.py accounts.json accounts.yaml

# Export → Convert → Report pipeline
sf data query --target-org my-org \
  --query "SELECT Id, Name FROM Account LIMIT 200" --json > data.json
python3 .claude/skills/file-converter/scripts/csv_json_yaml.py data.json report.csv
```

See [references/data-operations.md](references/data-operations.md) for bulk patterns and tree format details.

## Metadata Deploy/Retrieve

### Retrieve (Write tier — modifies local files)

```bash
# Retrieve by source
sf project retrieve start --source-dir force-app --target-org my-org

# Retrieve by metadata type
sf project retrieve start --metadata ApexClass --target-org my-org

# Retrieve by manifest
sf project retrieve start --manifest package.xml --target-org my-org
```

### Deploy (Destructive tier — modifies org)

**Always validate first:**

```bash
# Step 1: Preview (Safe)
sf project deploy preview --source-dir force-app --target-org my-org

# Step 2: Validate / dry-run (Write — confirm first)
sf project deploy start --source-dir force-app --target-org my-org --dry-run

# Step 3: Actual deploy (Destructive — confirm w/ consequences)
sf project deploy start --source-dir force-app --target-org my-org

# Production deploy (always w/ tests)
sf project deploy start --source-dir force-app --target-org prod-org \
  --test-level RunLocalTests
```

## Apex Execution

**Always show code before running. Always confirm.**

```bash
# Step 1: Display the Apex code to the user (MANDATORY)
cat script.apex

# Step 2: AskUserQuestion — "Execute this Apex in <org>?"

# Step 3: Execute (Destructive tier)
sf apex run --target-org my-org --file script.apex

# Run tests (Write tier)
sf apex run test --target-org my-org --class-names MyClassTest --code-coverage

# Get latest log
sf apex get log --target-org my-org --number 1
```

## Org Management

### Scratch Orgs

```bash
# Create (Write)
sf org create scratch --definition-file config/project-scratch-def.json \
  --alias my-scratch --duration-days 7

# List (Safe)
sf org list --all

# Delete (Destructive — confirm first)
sf org delete scratch --target-org my-scratch
```

### Sandboxes

```bash
# Create (Destructive — long-running, consumes resources)
sf org create sandbox --target-org prod-org --name dev-sandbox --alias dev-sb

# Refresh (Destructive)
sf org refresh sandbox --target-org dev-sb

# Delete (Destructive — confirm first)
sf org delete sandbox --target-org dev-sb
```

## Authentication

```bash
# Web login (interactive — recommended for development)
sf org login web --alias my-org --set-default

# Sandbox login
sf org login web --alias my-sandbox --instance-url https://test.salesforce.com

# JWT login (CI/CD — non-interactive)
sf org login jwt --client-id <consumer_key> --jwt-key-file server.key \
  --username user@example.com --alias my-org

# SFDX Auth URL (transfer auth between systems)
sf org login sfdx-url --sfdx-url-file auth.txt --alias my-org

# Device flow (headless environments)
sf org login device

# Verify auth
sf org display --target-org my-org
sf auth list
```

See [references/auth-flows.md](references/auth-flows.md) for detailed setup instructions.

## MCP Server Integration

### Official Salesforce MCP Server (recommended)

```json
{
  "mcpServers": {
    "salesforce-dx": {
      "command": "npx",
      "args": ["-y", "@salesforce/mcp", "--orgs", "DEFAULT_TARGET_ORG"]
    }
  }
}
```

**Available toolsets:** Core, Orgs, Data, Users, Metadata, Testing, Code-Analysis, LWC, Aura, Mobile, Scale Products.

### Tool Detection Flow

```
1. Check: Are Salesforce MCP tools available? (ToolSearch "salesforce")
   → YES: Use MCP tools (structured, validated)
   → NO:  Fall back to sf CLI commands
   → NO CLI: Guide user through installation
```

### Community MCP Servers

| Server | Tools | Best For |
|--------|-------|----------|
| `@salesforce/mcp` (official) | 60+ | Full DX workflow, LWC, testing, metadata |
| `tsmztech/mcp-server-salesforce` | 16 | CRUD, schema, Apex, SOSL |
| `advancedcommunities/salesforce-mcp-server` | 36 | Apex, testing, code analysis, data export |

See [references/mcp-integration.md](references/mcp-integration.md) for setup and toolset details.

## Direct API Access

```bash
# REST API (Safe for GET, Write/Destructive for others)
sf api request rest /services/data/v60.0/sobjects/Account/describe
sf api request rest /services/data/v60.0/query?q=SELECT+Id+FROM+Account+LIMIT+10

# GraphQL
sf api request graphql --body query.graphql --target-org my-org

# Composite (multiple operations in one call)
sf api request rest /services/data/v60.0/composite --body composite.json -X POST
```

## Platform Events & CDC

```bash
# Publish platform event (Destructive — triggers automation)
sf data create record --sobject MyEvent__e --values "Field1__c='value'" --target-org my-org

# Subscribe to events (Safe — read-only)
sf apex run --target-org my-org --file subscribe_events.apex

# Check CDC-enabled objects (Safe)
sf data query --target-org my-org --use-tooling-api \
  --query "SELECT QualifiedApiName FROM EntityDefinition WHERE IsEnabledForChangeDataCapture = true LIMIT 100"
```

## AskUserQuestion Integration

For ALL write, destructive, and forbidden operations, use `AskUserQuestion` w/ tailored options.

### Data Modification Example

```
question: "Create a new Account record in <org-alias> (<org-type>)?"
header: "SF Write"
options:
  - label: "Create record"
    description: "Insert the Account record with the specified field values"
  - label: "Cancel"
    description: "Do not create any records"
```

### Deploy Example

```
question: "Deploy metadata to <org-alias> (<org-type>)? <N> components will be modified."
header: "SF Deploy"
options:
  - label: "Validate only (dry-run)"
    description: "Run validation without making changes"
  - label: "Deploy now"
    description: "Deploy and modify the target org"
  - label: "Cancel"
    description: "Do not deploy"
```

### Apex Execution Example

```
question: "Execute the following Apex in <org-alias> (<org-type>)?\n\n<code preview>"
header: "SF Apex"
options:
  - label: "Execute"
    description: "Run the Apex code in the target org"
  - label: "Cancel"
    description: "Do not execute"
```

See [references/safety-rules.md](references/safety-rules.md) for all confirmation templates.

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `sf: command not found` | Not installed | `npm install -g @salesforce/cli` |
| `No default org set` | No target org | `sf config set target-org <alias>` |
| `INVALID_SESSION_ID` | Auth expired | `sf org login web --alias <org>` |
| `MALFORMED_QUERY` | Bad SOQL syntax | Check query, verify field names |
| `INVALID_FIELD` | Wrong field name | Use `sf schema generate sobject` to check fields |
| `REQUEST_LIMIT_EXCEEDED` | API limit hit | Check `sf limits api display`, wait or optimize |
| `DUPLICATE_VALUE` | Unique constraint | Check external IDs, use upsert instead |
| `REQUIRED_FIELD_MISSING` | Missing field | Check object requirements w/ describe |
| `DEPLOY_FAILED` | Deploy validation error | Check error details, fix code, redeploy |

## Shell Safety

- **No interactive mode:** Always provide explicit flags, never rely on interactive prompts
- **No pagers:** Pipe to `cat` if output may trigger a pager: `sf org list | cat`
- **Always specify org:** Use `--target-org` to prevent accidental operations on wrong org
- **Quote arguments:** Always quote query strings and multi-word values
- **JSON output:** Use `--json` for programmatic parsing
- **Never print tokens:** Auth tokens, keys, and secrets must never appear in output

## Integration

**Pairs with:**
- **file-converter** — Convert Salesforce exports between CSV, JSON, YAML, XML formats
- **github-cli** — Commit and PR Salesforce metadata changes
- **code-quality** — Review Apex code before deployment
- **token-optimizer** — Compress large query results or metadata descriptions
