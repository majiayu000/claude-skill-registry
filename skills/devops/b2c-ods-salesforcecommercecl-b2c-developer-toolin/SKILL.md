---
name: b2c-ods
description: Create and manage on-demand sandboxes (ODS). Use when provisioning development instances, starting/stopping sandboxes, checking sandbox status, or managing sandbox lifecycle. Only create or delete sandboxes when explicitly requested.
---

# B2C ODS Skill

Use the `b2c` CLI plugin to manage Salesforce B2C Commerce On-demand sandboxes (ODS). Only create or delete a sandbox if explicitly asked as this may be a billable or destructible action.

## Sandbox ID Formats

Commands that operate on a specific sandbox accept two ID formats:

- **UUID**: The full sandbox UUID (e.g., `abc12345-1234-1234-1234-abc123456789`)
- **Realm-instance**: The realm-instance format (e.g., `zzzv-123` or `zzzv_123`)

The realm-instance format uses the 4-character realm code followed by a dash or underscore and the instance number. When using a realm-instance format, the CLI will automatically look up the corresponding UUID.

## Examples

### List ODS Sandboxes

```bash
b2c ods list

# for realm zzpq with JSON output
b2c ods list --realm zzpq --json

# filter by status and those created by a specific user, only print the columns id,state,hostname
b2c ods list --filter-params 'state=started,creating&createdBy=clavery@salesforce.com' --realm zzpq --columns id,state,hostname
```

### Create ODS Sandbox

Only create a sandbox if explicitly asked as this may be a billable action.

```bash
# create in realm zzpq with 4 hour TTL (0 = infinite); json output and wait for completion (this may take 5-10 minutes; timeout is 10 minutes)
b2c ods create --realm zzpq --ttl 4 --json --wait

# create in realm zzpq with large profile (medium is default)
b2c ods create --realm zzpq --profile large

# get full log trace output to debug
b2c ods create --realm zzpq --log-level trace
```

### Get/Start/Stop/Restart/Delete Sandbox

Commands that operate on a specific sandbox support both UUID and realm-instance formats:

```bash
# Using UUID
b2c ods get abc12345-1234-1234-1234-abc123456789
b2c ods start abc12345-1234-1234-1234-abc123456789
b2c ods stop abc12345-1234-1234-1234-abc123456789

# Using realm-instance format
b2c ods get zzzv-123
b2c ods start zzzv_123
b2c ods stop zzzv-123
b2c ods restart zzzv-123
b2c ods delete zzzv-123 --force
```

### More Commands

See `b2c ods --help` for a full list of available commands and options in the `ods` topic.
