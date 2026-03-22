---
name: sf-data
description: |
  Handle Salesforce data operations including data migration, sandbox seeding,
  bulk data loading, data export, and data cleanup. Use when asked about data
  migration, sandbox seeding, bulk data loading, CSV import/export, or moving
  data between orgs. Activate on mentions of "data migration", "sandbox seed",
  "bulk load", "CSV import", "data export", "upsert", or "data plan".
license: Apache-2.0
compatibility: Requires Salesforce CLI (sf) v2+. Authenticated org needed for data operations.
metadata:
  author: clientell
  version: "1.0.0"
  tags: salesforce, data-migration, bulk-api, sandbox, csv
# Claude Code specific
allowed-tools: Read,Write,Edit,Bash(sf *),Glob,Grep
context: fork
---

# Data Migration & Management

You are a Salesforce data specialist. Handle data operations safely and efficiently.

## Data Operations

### Query and Export
```bash
# Query records
sf data query -q "SELECT Id, Name, Industry FROM Account WHERE Industry != null LIMIT 100" --target-org myOrg

# Export to CSV
sf data query -q "SELECT Id, Name, Industry FROM Account" --target-org myOrg --result-format csv > accounts.csv

# Export to JSON
sf data query -q "SELECT Id, Name FROM Account" --target-org myOrg --result-format json > accounts.json

# Bulk query (large datasets)
sf data query -q "SELECT Id, Name FROM Account" --target-org myOrg --bulk
```

### Import and Upsert
```bash
# Insert records from CSV
sf data import tree -f data/accounts.json --target-org myOrg

# Bulk upsert
sf data upsert bulk -s Account -f accounts.csv -i External_Id__c --target-org myOrg

# Insert with plan (preserves relationships)
sf data import tree -p data/plan.json --target-org myOrg
```

### Data Plan for Related Records
```json
[
    {
        "sobject": "Account",
        "saveRefs": true,
        "resolveRefs": false,
        "files": ["Account.json"]
    },
    {
        "sobject": "Contact",
        "saveRefs": false,
        "resolveRefs": true,
        "files": ["Contact.json"]
    }
]
```

### Sandbox Seeding Script
```bash
#!/bin/bash
# seed-sandbox.sh — Create test data in a sandbox

ORG_ALIAS="${1:-sandbox}"

echo "Seeding data in $ORG_ALIAS..."

# Insert accounts
sf data import tree -f data/seed/accounts.json --target-org "$ORG_ALIAS"

# Insert contacts (references accounts)
sf data import tree -f data/seed/contacts.json --target-org "$ORG_ALIAS"

# Insert opportunities
sf data import tree -f data/seed/opportunities.json --target-org "$ORG_ALIAS"

echo "Seeding complete."
```

### Anonymous Apex for Data Setup
```bash
# Run anonymous Apex for complex data setup
sf apex run -f scripts/seed-data.apex --target-org myOrg
```

```apex
// scripts/seed-data.apex
List<Account> accounts = new List<Account>();
for (Integer i = 0; i < 100; i++) {
    accounts.add(new Account(
        Name = 'Test Account ' + i,
        Industry = 'Technology',
        BillingState = 'CA'
    ));
}
insert accounts;
System.debug('Inserted ' + accounts.size() + ' accounts');
```

## Data Cleanup
```bash
# Delete records matching criteria
sf data delete bulk -s Account -f delete-ids.csv --target-org myOrg

# Delete all records of a type (careful!)
sf data query -q "SELECT Id FROM TempObject__c" --target-org myOrg --result-format csv > to-delete.csv
sf data delete bulk -s TempObject__c -f to-delete.csv --target-org myOrg
```

### Bulk API 2.0
Use for datasets >2,000 records. Significantly faster than standard API.
```bash
# Bulk upsert from CSV
sf data upsert bulk -s Account -f accounts.csv -i External_Id__c --target-org myOrg

# Bulk delete from CSV (Id column required)
sf data delete bulk -s Account -f delete-ids.csv --target-org myOrg

# Check job status
sf data bulk results -i <jobId> --target-org myOrg
```
- Job timeout: 10 minutes for ingest, 15 minutes for query
- Max file size: 150 MB per CSV
- Max 150M records per 24-hour rolling window

### External ID Best Practices
- Choose fields that are **unique across source and target orgs**
- Mark as External ID AND Unique for upsert idempotency
- Cannot use masked fields as external IDs (Data Mask limitation)
- For cross-org sync: use a UUID or composite key (OrgId + RecordId)

### Relationship Loading Order
1. Independent objects (no required lookups)
2. Parent objects (Account before Contact)
3. Master-detail parents MUST exist before child insert
4. Junction objects (M2M) load after both parent objects
5. Self-referential records: two-pass load (insert without self-ref, then update)

### Record Type Mapping
- Export record type developer names (not IDs) — IDs differ between orgs
- Validate picklist values exist in target before loading
- Map with: `sf data query -q "SELECT Id, DeveloperName FROM RecordType WHERE SObjectType='Account'"`

### File Migration (ContentVersion)
```apex
ContentVersion cv = new ContentVersion();
cv.Title = 'My File';
cv.PathOnClient = 'myfile.pdf';
cv.VersionData = Blob.valueOf('file content'); // or Base64-decoded
insert cv;
```
- ContentDocumentLink associates files with records
- Max file size: 2 GB (Salesforce Files)
- Attachments (legacy) → migrate to ContentVersion

## Rules
- Always verify target org before data operations
- Use `--dry-run` or `LIMIT` clauses when testing queries
- Preserve referential integrity — load parent records before children
- Use External IDs for upsert operations to avoid duplicates
- Back up data before destructive operations
- Use Bulk API for datasets > 200 records

## Gotchas
- Master-detail parent record MUST exist before child insert — otherwise `ENTITY_IS_DELETED` or `REQUIRED_FIELD_MISSING`
- External ID fields **cannot be masked** in Salesforce Data Mask
- Bulk API jobs timeout after 10-15 minutes — split large datasets
- Polymorphic lookups (e.g., Task.WhatId) need `TYPEOF` in export queries
- ContentVersion requires `PathOnClient` AND `VersionData` — both mandatory
- Self-referential records (e.g., Account.ParentId) require two-pass load
- Bulk API 2.0 returns success for the job even if individual records fail — always check results
- Data Loader truncates field values silently if they exceed field length

## References
- [Data Patterns](references/data-patterns.md) — Bulk API 2.0, Composite API, tree export, external IDs, large data volumes, Big Objects, file upload, multi-currency, ETL, backup/recovery

## Workflow
1. Verify target org connection
2. Analyze data requirements (objects, relationships, volume)
3. Export or generate source data
4. Create import plan with correct object order
5. Execute import with appropriate method (tree, bulk, anonymous Apex)
6. Verify data integrity post-import
