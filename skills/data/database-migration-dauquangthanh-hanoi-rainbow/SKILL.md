---
name: database-migration
description: Guides database migration projects including engine changes (MySQL to PostgreSQL, Oracle to PostgreSQL, SQL Server to PostgreSQL), version upgrades, cloud migrations (on-premise to RDS/Cloud SQL/Azure Database), schema migrations, zero-downtime migrations, replication setup, and data migration strategies. Covers homogeneous and heterogeneous migrations, ETL processes, cutover procedures, and rollback plans. Use when migrating databases, changing database engines, upgrading database versions, moving databases to cloud, or when users mention "database migration", "DB migration", "PostgreSQL migration", "MySQL to Postgres", "Oracle migration", "database upgrade", or "cloud database migration".
---

# Database Migration

Provides comprehensive guidance for migrating databases between engines, versions, platforms, and architectures. Covers both schema and data migration with strategies for minimizing downtime and ensuring data integrity.

## Migration Decision Tree

**1. Identify Migration Type:**

- Same engine (PostgreSQL → PostgreSQL)? → Homogeneous migration
- Different engine (Oracle → PostgreSQL)? → Heterogeneous migration
- Version upgrade only? → In-place or dump/restore
- Cloud migration? → Consider cloud-native tools

**2. Assess Downtime Requirements:**

- Can tolerate hours of downtime? → Dump and restore
- Need minimal downtime (minutes)? → Replication with cutover
- Require zero downtime? → See [zero-downtime-migration-strategies.md](references/zero-downtime-migration-strategies.md)

**3. Choose Migration Path:**

- Load [migration-types.md](references/migration-types.md) for detailed migration approaches
- For cloud migrations, load [cloud-specific-migrations.md](references/cloud-specific-migrations.md)

## Core Migration Workflow

## Step 1: Assessment and Planning

**Analyze Source Database:**

1. Document current database version, size, and complexity
2. Identify dependencies (applications, services, integrations)
3. Review schema: tables, indexes, constraints, triggers, procedures
4. Assess data volume and growth rate
5. Document current performance baselines

**Define Requirements:**

- Migration type (homogeneous vs heterogeneous)
- Acceptable downtime window
- Data integrity requirements
- Compliance and security requirements
- Rollback criteria

**Output:** Migration plan with approach, timeline, and resources

### Step 2: Environment Setup

**Prepare Target Environment:**

1. Provision target database with appropriate sizing
2. Configure network connectivity and security
3. Set up monitoring and logging
4. Create test and staging environments matching production

**Prepare Migration Tools:**

- Native tools (pg_dump, mysqldump, SQL Server bcp)
- Cloud provider tools (AWS DMS, GCP Database Migration Service)
- Third-party tools (see [tools-reference.md](references/tools-reference.md))

### Step 3: Schema Migration

**For Homogeneous Migration:**

1. Export schema using native tools
2. Review and optimize schema for target version
3. Apply schema to target database
4. Verify all objects created successfully

**For Heterogeneous Migration:**

1. Analyze schema compatibility issues
2. Convert data types, stored procedures, triggers
3. Adapt SQL dialects and syntax
4. Test converted schema thoroughly

Load [migration-types.md](references/migration-types.md) for engine-specific schema conversion guidance.

### Step 4: Data Migration

**Choose Data Migration Strategy:**

**Option A: Dump and Restore (Full Downtime)**

```
1. Stop application writes
2. Create full backup of source database
3. Transfer backup to target environment
4. Restore to target database
5. Verify data integrity (row counts, checksums)
6. Update application connection strings
7. Resume operations
```

Best for: Smaller databases, acceptable downtime windows

**Option B: Replication (Minimal Downtime)**

```
1. Set up replication from source to target
2. Monitor replication lag until synchronized
3. Schedule cutover window
4. Stop writes briefly (minutes)
5. Verify replication is caught up
6. Promote target to primary
7. Update application connections
8. Resume operations
```

Best for: Large databases, minimal downtime requirements

Load [zero-downtime-migration-strategies.md](references/zero-downtime-migration-strategies.md) for advanced zero-downtime patterns.

### Step 5: Validation and Testing

**Validate Data Migration:**

1. Compare row counts between source and target
2. Verify data integrity (checksums, sample queries)
3. Test application functionality against target database
4. Validate performance meets requirements
5. Check all constraints, indexes, and relationships

**Testing Checklist:**

- [ ] All tables migrated with correct row counts
- [ ] Schema objects (indexes, constraints, triggers) present
- [ ] Data types converted correctly
- [ ] Application queries execute successfully
- [ ] Performance meets or exceeds baseline
- [ ] Backup and restore procedures work

Load [common-issues-and-solutions.md](references/common-issues-and-solutions.md) if encountering problems.

### Step 6: Cutover Planning

1. Create detailed cutover runbook with specific timings
2. Define rollback criteria and procedures (load [rollback-procedures.md](references/rollback-procedures.md))
3. Coordinate with stakeholders (apps, operations, business)
4. Schedule maintenance window
5. Prepare communication plan

Load [migration-phases.md](references/migration-phases.md) for detailed phase-by-phase execution guidance.

### Step 7: Post-Migration

**Immediate (Day 1):**

1. Monitor performance metrics and error rates
2. Validate application functionality
3. Keep source database available (read-only) as safety net
4. Document any issues and resolutions

**Short-term (Week 1-2):**

1. Continue monitoring for issues
2. Optimize indexes and queries if needed
3. Tune database configuration for workload
4. Conduct parallel run if applicable

**Long-term:**

1. Validate backup and restore procedures
2. Update disaster recovery plans
3. Document final configuration and lessons learned
4. Decommission source database after retention period

## Key Considerations

**Planning Guidelines:**

- Allow 2-3x estimated time for heterogeneous migrations
- Plan for extended parallel run period (1-4 weeks minimum)
- Database migration often triggers application code changes
- Coordinate with application migration when possible
- Consider phased approach: read replica → read/write split → full cutover

**Critical Success Factors:**

- ✅ Multiple backups before migration
- ✅ Test migration in staging environment first
- ✅ Monitor metrics during migration (lag, throughput, errors)
- ✅ Always have rollback plan ready
- ✅ Document all steps, issues, and decisions
- ✅ Encrypt data in transit and at rest
- ✅ Rotate credentials after migration

Load [best-practices.md](references/best-practices.md) for comprehensive best practices.

## Reference Files

Load these references based on specific needs:

- **[migration-types.md](references/migration-types.md)** - Detailed guidance on homogeneous vs heterogeneous migrations, engine-specific conversion patterns
- **[migration-phases.md](references/migration-phases.md)** - Phase-by-phase execution details with timelines and dependencies
- **[zero-downtime-migration-strategies.md](references/zero-downtime-migration-strategies.md)** - Advanced patterns for zero-downtime migrations (dual writes, event streaming, phased cutover)
- **[cloud-specific-migrations.md](references/cloud-specific-migrations.md)** - AWS DMS, GCP Database Migration Service, Azure Database Migration Service
- **[tools-reference.md](references/tools-reference.md)** - Native tools, cloud provider services, third-party migration tools
- **[rollback-procedures.md](references/rollback-procedures.md)** - Step-by-step rollback procedures for different migration strategies
- **[common-issues-and-solutions.md](references/common-issues-and-solutions.md)** - Troubleshooting guide for common migration problems
- **[best-practices.md](references/best-practices.md)** - Comprehensive best practices checklist
