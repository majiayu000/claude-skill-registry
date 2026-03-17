---
name: disaster-recovery
description: Backup strategies, disaster recovery planning, and business continuity.
---

# Disaster Recovery

## RTO vs RPO

| Metric | Definition | Example |
|--------|------------|---------|
| **RTO** | Recovery Time Objective | 4 hours |
| **RPO** | Recovery Point Objective | 1 hour |

**RTO:** How long until service is restored?
**RPO:** How much data can we lose?

## DR Strategies

| Strategy | RTO | Cost |
|----------|-----|------|
| Backup & Restore | Hours | $ |
| Pilot Light | Minutes | $$ |
| Warm Standby | Minutes | $$$ |
| Multi-Site Active | Seconds | $$$$ |

## Backup Strategy

### Database

```bash
# PostgreSQL
pg_dump -h host -U user dbname | gzip > backup.sql.gz

# MySQL
mysqldump -h host -u user -p dbname | gzip > backup.sql.gz
```

### Automated Backups

```hcl
# AWS RDS
resource "aws_db_instance" "main" {
  backup_retention_period = 7
  backup_window           = "03:00-04:00"

  # Cross-region replica for DR
  replicate_source_db = aws_db_instance.primary.arn
}
```

## DR Runbook

### Failover Steps

1. **Detect** - Monitor alerts for primary failure
2. **Assess** - Confirm failure, estimate recovery
3. **Decide** - Failover if RTO exceeded
4. **Execute** - Run failover procedure
5. **Verify** - Test functionality
6. **Communicate** - Update stakeholders

### Failback Steps

1. Verify primary is healthy
2. Sync data from secondary
3. Switch traffic back
4. Monitor closely

## Testing

| Test Type | Frequency |
|-----------|-----------|
| Backup restore | Monthly |
| Failover drill | Quarterly |
| Full DR test | Annually |

## Multi-Region

```
Primary (us-east-1)          Secondary (us-west-2)
┌─────────────────┐          ┌─────────────────┐
│    App + DB     │ ──sync── │   DB Replica    │
└─────────────────┘          └─────────────────┘
        │                            │
        └──────── Route 53 ──────────┘
                (failover)
```
