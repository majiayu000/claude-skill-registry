---
name: planning-disaster-recovery
description: Design and implement disaster recovery strategies with RTO/RPO planning, database backups, Kubernetes DR, cross-region replication, and chaos engineering testing. Use when implementing backup systems, configuring point-in-time recovery, setting up multi-region failover, or validating DR procedures.
---

# Disaster Recovery

## Purpose

Provide comprehensive guidance for designing disaster recovery (DR) strategies, implementing backup systems, and validating recovery procedures across databases, Kubernetes clusters, and cloud infrastructure. Enable teams to define RTO/RPO objectives, select appropriate backup tools, configure automated failover, and test DR capabilities through chaos engineering.

## When to Use This Skill

Invoke this skill when:
- Defining recovery time objectives (RTO) and recovery point objectives (RPO)
- Implementing database backups with point-in-time recovery (PITR)
- Setting up Kubernetes cluster backup and restore workflows
- Configuring cross-region replication for high availability
- Testing disaster recovery procedures through chaos experiments
- Meeting compliance requirements (GDPR, SOC 2, HIPAA)
- Automating backup monitoring and alerting
- Designing multi-cloud disaster recovery architectures

## Core Concepts

### RTO and RPO Fundamentals

**Recovery Time Objective (RTO):** Maximum acceptable downtime after a disaster before business impact becomes unacceptable.

**Recovery Point Objective (RPO):** Maximum acceptable data loss measured in time. Defines how far back in time recovery must reach.

**Criticality Tiers:**
- **Tier 0 (Mission-Critical):** RTO < 1 hour, RPO < 5 minutes
- **Tier 1 (Production):** RTO 1-4 hours, RPO 15-60 minutes
- **Tier 2 (Important):** RTO 4-24 hours, RPO 1-6 hours
- **Tier 3 (Standard):** RTO > 24 hours, RPO > 6 hours

### 3-2-1 Backup Rule

Maintain **3 copies** of data on **2 different media** types with **1 copy offsite**.

Example implementation:
- Primary: Production database
- Secondary: Local backup storage
- Tertiary: Cloud backup (S3/GCS/Azure)

### Backup Types

**Full Backup:** Complete copy of all data. Slowest to create, fastest to restore.

**Incremental Backup:** Only changes since last backup. Fastest to create, requires full + all incrementals to restore.

**Differential Backup:** Changes since last full backup. Balance between storage and restore speed.

**Continuous Backup:** Real-time or near-real-time backup via WAL/binlog archiving. Lowest RPO.

## Quick Decision Framework

### Step 1: Map RTO/RPO to Strategy

```
RTO < 1 hour, RPO < 5 min
→ Active-Active replication, continuous archiving, automated failover
→ Tools: Aurora Global DB, GCS Multi-Region, pgBackRest PITR
→ Cost: Highest

RTO 1-4 hours, RPO 15-60 min
→ Warm standby, incremental backups, automated failover
→ Tools: pgBackRest, WAL-G, RDS Multi-AZ
→ Cost: High

RTO 4-24 hours, RPO 1-6 hours
→ Daily full + incremental, cross-region backup
→ Tools: pgBackRest, Velero, Restic
→ Cost: Medium

RTO > 24 hours, RPO > 6 hours
→ Weekly full + daily incremental, single region
→ Tools: pg_dump, mysqldump, S3 versioning
→ Cost: Low
```

### Step 2: Select Backup Tools by Use Case

| Use Case | Primary Tool | Alternative | Key Feature |
|----------|-------------|-------------|-------------|
| PostgreSQL production | pgBackRest | WAL-G | PITR, compression, multi-repo |
| MySQL production | Percona XtraBackup | WAL-G | Hot backups, incremental |
| MongoDB | Atlas Backup | mongodump | Continuous backup, PITR |
| Kubernetes cluster | Velero | ArgoCD + Git | PV snapshots, scheduling |
| File/object backup | Restic | Duplicity | Encryption, deduplication |
| Cross-region replication | Aurora Global DB | RDS Read Replica | Active-Active capable |

## Database Backup Patterns

### PostgreSQL with pgBackRest

**Use Case:** Production PostgreSQL with < 5 minute RPO

**Quick Start:** See `examples/postgresql/pgbackrest-config/`

Configure continuous WAL archiving with full/differential/incremental backups to S3/GCS/Azure. Schedule weekly full, daily differential backups. Enable PITR with `pgbackrest --stanza=main --delta restore`.

**Detailed Guide:** `references/database-backups.md#postgresql`

### MySQL with Percona XtraBackup

**Use Case:** MySQL production requiring hot backups

**Quick Start:** See `examples/mysql/xtrabackup/`

Perform full (`xtrabackup --backup --parallel=4`) and incremental backups with binary log archiving for PITR. Restore requires decompress, prepare, apply incrementals, and copy-back steps.

**Detailed Guide:** `references/database-backups.md#mysql`

### MongoDB Backup

**Quick Start:** Use `mongodump --gzip --numParallelCollections=4` for logical backups or MongoDB Atlas for continuous backup with PITR.

**Detailed Guide:** `references/database-backups.md#mongodb`

## Kubernetes Disaster Recovery

### Velero for Cluster Backups

**Quick Start:** `velero install --provider aws --bucket my-backups`

Configure scheduled backups (daily full, hourly production namespace) with PV snapshots. Restore with `velero restore create --from-backup <name>`. Support selective restore (namespace mappings, storage class remapping).

**Examples:** `examples/kubernetes/velero/`
**Detailed Guide:** `references/kubernetes-dr.md`

### etcd Backup

**Quick Start:** `ETCDCTL_API=3 etcdctl snapshot save /backups/etcd/snapshot.db`

Create periodic etcd snapshots for control plane recovery. Restore requires cluster recreation with snapshot data.

**Examples:** `examples/kubernetes/etcd/`

## Cloud-Specific DR Patterns

### AWS

**Key Services:**
- RDS: Automated backups (30-day retention), PITR, Multi-AZ
- Aurora Global DB: Cross-region active-passive with automatic failover
- S3 CRR: Cross-region replication with 15-min SLA (Replication Time Control)

**Examples:** `examples/cloud/aws/`
**Detailed Guide:** `references/cloud-dr-patterns.md#aws`

### GCP

**Key Services:**
- Cloud SQL: PITR with 7-day transaction logs, 30-day retention
- GCS Multi-Regional: Automatic replication across 100+ mile separation
- Regional HA: Synchronous replication within region

**Detailed Guide:** `references/cloud-dr-patterns.md#gcp`

### Azure

**Key Services:**
- Azure Backup: VM backups with flexible retention (daily/weekly/monthly/yearly)
- Azure Site Recovery: Cross-region VM replication with 4-hour app-consistent snapshots
- Geo-Redundant Storage: Automatic replication to secondary region

**Detailed Guide:** `references/cloud-dr-patterns.md#azure`

## Cross-Region Replication Patterns

| Pattern | RTO | RPO | Cost | Use Case |
|---------|-----|-----|------|----------|
| **Active-Active** | < 1 min | < 1 min | High | Both regions serve traffic |
| **Active-Passive** | 15-60 min | 5-15 min | Medium | Standby for failover |
| **Pilot Light** | 10-30 min | 5-15 min | Low | Minimal secondary infra |
| **Warm Standby** | 5-15 min | 5-15 min | Med-High | Scaled-down secondary |

**Implementation Examples:**
- PostgreSQL streaming replication (Active-Passive)
- Aurora Global Database (Active-Active)
- ASG scale-up automation (Pilot Light)

**Detailed Guide:** `references/cross-region-replication.md`

## Testing Disaster Recovery

### Chaos Engineering

**Purpose:** Validate DR procedures through controlled failure injection.

**Test Scenarios:**
- Database failover (stop primary, measure promotion time)
- Region failure (block network, trigger DNS failover)
- Kubernetes recovery (delete namespace, restore from Velero)

**Tools:** Chaos Mesh, Gremlin, Litmus, Toxiproxy

**Examples:** `examples/chaos/db-failover-test.sh`, `examples/chaos/region-failure-test.sh`
**Detailed Guide:** `references/chaos-engineering.md`

### Automated DR Drills

**Run Monthly Tests:**
```bash
./scripts/dr-drill.sh --environment staging --test-type full
./scripts/test-restore.sh --backup latest --target staging-db
```

## Compliance and Retention

| Regulation | Retention | Requirements |
|------------|-----------|--------------|
| GDPR | 1-7 years | EU data residency, right to erasure |
| SOC 2 | 1 year+ | Secure deletion, access controls |
| HIPAA | 6 years | Encryption, PHI protection |
| PCI DSS | 3mo-1yr | Secure deletion, quarterly reviews |

**Implement with S3/GCS lifecycle policies:** 30d→Standard-IA, 90d→Glacier, 365d→Deep Archive

**Immutable backups:** Use S3 Object Lock or Azure Immutable Blob Storage for ransomware protection.

**Detailed Guide:** `references/compliance-retention.md`

## Monitoring and Alerting

**Key Metrics:** Backup success rate, duration, time since last backup, RPO breach, storage utilization

**Prometheus Alerts:** VeleroBackupFailed, VeleroBackupTooOld, BackupSizeTrend

**Validation Scripts:**
```bash
./scripts/validate-backup.sh --backup latest --verify-integrity
./scripts/check-retention.sh --report-violations
./scripts/generate-dr-report.sh --format pdf
```

## Automation and Runbooks

**Automate Backup Schedules:** Cron for pgBackRest (weekly full, daily differential), Velero schedules (K8s)

**DR Runbook Steps:** Detect failure → Verify secondary → Promote → Update DNS → Notify → Document

**Detailed Guide:** `references/runbook-automation.md`

## Integration with Other Skills

### Related Skills

**Prerequisites:**
- `infrastructure-as-code`: Provision backup infrastructure, DR regions
- `kubernetes-operations`: K8s cluster setup for Velero
- `secret-management`: Backup encryption keys, credentials

**Parallel Skills:**
- `databases-postgresql`: PostgreSQL configuration and operations
- `databases-mysql`: MySQL configuration and operations
- `observability`: Backup monitoring, alerting
- `security-hardening`: Secure backup storage, access control

**Consumer Skills:**
- `incident-management`: Invoke DR procedures during incidents
- `compliance-frameworks`: Meet regulatory requirements

### Skill Chaining Example

```
infrastructure-as-code → secret-management → disaster-recovery → observability
       ↓                        ↓                   ↓                ↓
  Create S3 buckets      Store encryption     Configure backups   Monitor jobs
  Provision databases    keys in Vault        Set up replication  Alert failures
  Setup VPCs             Manage credentials   Test DR drills      Track metrics
```

## Best Practices

### Do

✓ Test restores regularly (monthly for critical systems)
✓ Automate backup monitoring and alerting
✓ Encrypt backups at rest and in transit
✓ Implement 3-2-1 backup rule
✓ Define and measure RTO/RPO
✓ Run chaos experiments to validate DR
✓ Document recovery procedures
✓ Store backups in different regions
✓ Use immutable backups for ransomware protection
✓ Automate DR testing in CI/CD

### Don't

✗ Assume backups work without testing
✗ Store all backups in single region
✗ Skip retention policy definition
✗ Forget to encrypt sensitive data
✗ Rely solely on cloud provider backups
✗ Ignore backup monitoring
✗ Perform backups only from primary database under high load
✗ Store encryption keys with backups

## Reference Documentation

- **RTO/RPO Planning:** `references/rto-rpo-planning.md`
- **Database Backups:** `references/database-backups.md`
- **Kubernetes DR:** `references/kubernetes-dr.md`
- **Cloud DR Patterns:** `references/cloud-dr-patterns.md`
- **Cross-Region Replication:** `references/cross-region-replication.md`
- **Chaos Engineering:** `references/chaos-engineering.md`
- **Compliance Requirements:** `references/compliance-retention.md`
- **Runbook Automation:** `references/runbook-automation.md`

## Examples

- **Runbooks:** `examples/runbooks/database-failover.md`, `examples/runbooks/region-failover.md`
- **PostgreSQL:** `examples/postgresql/pgbackrest-config/`, `examples/postgresql/walg-config/`
- **MySQL:** `examples/mysql/xtrabackup/`, `examples/mysql/walg/`
- **Kubernetes:** `examples/kubernetes/velero/`, `examples/kubernetes/etcd/`
- **Cloud:** `examples/cloud/aws/`, `examples/cloud/gcp/`, `examples/cloud/azure/`
- **Chaos:** `examples/chaos/db-failover-test.sh`, `examples/chaos/region-failure-test.sh`

## Scripts

- `scripts/validate-backup.sh`: Verify backup integrity
- `scripts/test-restore.sh`: Automated restore testing
- `scripts/dr-drill.sh`: Run full DR drill
- `scripts/check-retention.sh`: Verify retention policies
- `scripts/generate-dr-report.sh`: Compliance reporting
