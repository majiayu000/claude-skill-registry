---
name: backup-recovery
description: Define RPO/RTO, implement PITR/Snapshots, and test restores.
role: ops-sre, eng-database
triggers:
  - backup
  - restore
  - disaster recovery
  - rpo
  - rto
  - pitr
  - snapshot
---

# backup-recovery Skill

"A backup is not a backup until you have successfully restored from it."

## 1. Define Objectives
- **RPO (Recovery Point Objective)**: Max data loss. (e.g., "1 hour", "5 minutes", "0 seconds").
- **RTO (Recovery Time Objective)**: Max downtime. (e.g., "4 hours", "30 minutes").

## 2. Strategies
- **Point-In-Time Recovery (PITR)**: Archive WAL/Binlogs to replay transactions up to a specific second. (Critical for RPO ~0).
- **Snapshot**: Daily/Hourly full disk copy. Low impact, slower restore.
- **Logical Dump**: `pg_dump` / `mysqldump`. Portable, slow for large data.

## 3. Storage & Retention
- **Immutability**: Backups must be Read-Only (WORM) to prevent Ransomware encryption.
- **Off-site**: Replicate to a different region/cloud provider (3-2-1 Rule).
- **Retention**: Keep Dailies for 7 days, Weeklies for 1 month, Monthlies for 1 year.

## 4. Testing (The Golden Rule)
- **Automated Restore Drill**: Weekly CI job that:
  1. Spins up a fresh DB.
  2. Pulls the latest backup.
  3. Restores it.
  4. Runs integrity check (`SELECT count(*) ...`).
  5. Reports success/failure to Slack.
