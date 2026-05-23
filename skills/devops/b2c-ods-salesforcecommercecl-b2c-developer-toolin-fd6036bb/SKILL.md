---
name: b2c-ods
description: Using the b2c CLI for on-demand sandbox (ODS) management
---

# B2C ODS Skill

Use the `b2c` CLI plugin to manage Salesforce B2C Commerce On-demand sandboxes (ODS). Only create or delete a sandbox if explicitly asked as this may be a billable or destructible action.

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

### More Commands

See `b2c ods --help` for a full list of available commands and options in the `ods` topic.
