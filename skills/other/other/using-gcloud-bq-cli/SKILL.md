---
name: using-gcloud-bq-cli
description: Gotchas and patterns for gcloud and bq CLI tools. Use when authenticating service accounts, checking IAM permissions, or troubleshooting BigQuery access errors.
---

# Using gcloud and bq CLI

Patterns and gotchas for Google Cloud CLI tools, learned the hard way.

## Critical: bq CLI Ignores GOOGLE_APPLICATION_CREDENTIALS

**Problem:** Setting `export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json` does NOT make the `bq` CLI use those credentials. The `bq` CLI uses the gcloud credential store instead.

**Symptom:** Permission denied errors even when you've set the environment variable and verified the service account has the required permissions.

**Solution:**

```bash
# This does NOT work for bq:
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
bq query "SELECT 1"  # Uses gcloud active account, not the SA!

# This DOES work:
gcloud auth activate-service-account --key-file=/path/to/key.json
bq query "SELECT 1"  # Now uses the service account
```

## Verifying Permissions with testIamPermissions

When debugging permission issues, don't guess - verify what permissions an identity actually has:

```bash
# Get token for currently active gcloud account
ACCESS_TOKEN=$(gcloud auth print-access-token)

# Test specific permissions on a BigQuery table
curl -s -X POST \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  "https://bigquery.googleapis.com/bigquery/v2/projects/PROJECT/datasets/DATASET/tables/TABLE:testIamPermissions" \
  -d '{
    "permissions": [
      "bigquery.tables.get",
      "bigquery.tables.update",
      "bigquery.tables.updateData"
    ]
  }'
```

The response only includes permissions the identity actually has. Missing permissions won't appear.

## BigQuery Permission Differences

Two commonly confused permissions:

| Permission | What it allows |
|------------|----------------|
| `bigquery.tables.update` | Modify table **metadata** (schema, description, labels, partitioning) |
| `bigquery.tables.updateData` | Modify table **data** (inserts, DML statements, streaming writes) |

A service account that can write rows (`updateData`) cannot necessarily modify the schema (`update`). These are separate permissions, often granted by different roles.

## Cleanup After Using Service Account

After using a service account, restore your user account:

```bash
# Revoke SA (token expires naturally, but this removes from gcloud)
gcloud auth revoke SERVICE_ACCOUNT@PROJECT.iam.gserviceaccount.com

# Re-activate your user account
gcloud config set account YOUR_EMAIL@example.com
```

## Schema Updates for Nested RECORD Fields

BigQuery doesn't support `ALTER TABLE ADD COLUMN parent.child` for nested fields. Instead:

```bash
# 1. Export current schema
bq show --schema --format=json PROJECT:DATASET.TABLE > current_schema.json

# 2. Add nested field with jq
cat current_schema.json | jq '
  map(
    if .name == "parent_record" then
      .fields += [{"name": "new_field", "type": "STRING", "mode": "NULLABLE"}]
    else . end
  )
' > updated_schema.json

# 3. Apply updated schema (NOTE: use INTEGER not INT64 for bq CLI)
bq update --schema updated_schema.json PROJECT:DATASET.TABLE
```
