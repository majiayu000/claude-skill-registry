---
name: postgresql-backup
description: PostgreSQL backup and recovery - pg_dump, pg_basebackup, PITR
version: "3.0.0"
sasmp_version: "1.3.0"
bonded_agent: 08-postgresql-devops
bond_type: PRIMARY_BOND
category: database
difficulty: intermediate
estimated_time: 3h
---

# PostgreSQL Backup Skill

> Atomic skill for backup and recovery

## Overview

Production-ready patterns for logical backups, physical backups, and point-in-time recovery.

## Prerequisites

- PostgreSQL 16+
- Sufficient disk space
- Backup storage access

## Parameters

```yaml
parameters:
  backup_type:
    type: string
    required: true
    enum: [logical, physical, pitr]
  format:
    type: string
    enum: [custom, directory, plain]
    default: custom
```

## Quick Reference

### pg_dump (Logical)
```bash
# Custom format (recommended)
pg_dump -Fc -f backup.dump dbname

# Parallel backup
pg_dump -Fd -j 4 -f backup_dir dbname

# Compressed
pg_dump -Fc dbname | gzip > backup.dump.gz
```

### pg_basebackup (Physical)
```bash
pg_basebackup -D /backup -Fp -Xs -P -R
```

### pg_restore
```bash
pg_restore -d newdb -j 4 backup.dump
pg_restore --list backup.dump  # Preview
```

### WAL Archiving
```sql
archive_mode = on
archive_command = 'cp %p /archive/%f'
```

## Backup Strategy

| Type | Use Case | Recovery Speed |
|------|----------|----------------|
| pg_dump | Logical, portable | Slow |
| pg_basebackup | Full cluster | Fast |
| WAL + base | Point-in-time | Fast + precise |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Backup failed | Disk full | Free space |
| Restore slow | Large DB | Use parallel |
| WAL missing | Archive failed | Check archive_command |

## Usage

```
Skill("postgresql-backup")
```
