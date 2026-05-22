---
name: postgresql-admin
description: Administer PostgreSQL - security, roles, permissions, maintenance
version: "3.0.0"
sasmp_version: "1.3.0"
bonded_agent: 04-postgresql-admin
bond_type: PRIMARY_BOND
category: database
difficulty: advanced
estimated_time: 3h
---

# PostgreSQL Administration Skill

> Atomic skill for database security and maintenance

## Overview

Production-ready patterns for role management, security hardening, and routine maintenance.

## Prerequisites

- PostgreSQL 16+
- Superuser or role management privileges

## Parameters

```yaml
parameters:
  operation:
    type: string
    required: true
    enum: [create_role, grant, revoke, audit, maintain]
  role_name:
    type: string
    pattern: "^[a-z][a-z0-9_]*$"
```

## Quick Reference

### Role Creation
```sql
CREATE ROLE app_user WITH LOGIN PASSWORD 'secure' CONNECTION LIMIT 100;
CREATE ROLE readonly_role;
GRANT SELECT ON ALL TABLES IN SCHEMA app TO readonly_role;
```

### Security Hardening
```sql
REVOKE ALL ON SCHEMA public FROM PUBLIC;
ALTER TABLE data ENABLE ROW LEVEL SECURITY;
CREATE POLICY isolation ON data USING (tenant_id = current_setting('app.tenant')::uuid);
```

### Maintenance
```sql
ANALYZE VERBOSE table_name;
VACUUM (VERBOSE, ANALYZE) table_name;
REINDEX INDEX CONCURRENTLY idx_name;
```

## Security Audit

```sql
SELECT rolname FROM pg_roles WHERE rolsuper;  -- Superusers
SELECT * FROM information_schema.table_privileges WHERE grantee = 'PUBLIC';
```

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `42501` | Permission denied | Check GRANTs |
| `28P01` | Auth failed | Reset password |
| `55P03` | Lock unavailable | Kill blocker |

## Usage

```
Skill("postgresql-admin")
```
