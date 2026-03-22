---
name: Database Sync
description: Automate database synchronization, replication, migration, and cross-platform data integration
version: 1.0.0
author: Claude Office Skills
category: data
tags:
  - database
  - sync
  - replication
  - migration
  - integration
department: engineering
models:
  - claude-3-opus
  - claude-3-sonnet
  - gpt-4
mcp:
  server: data-mcp
  tools:
    - postgres_sync
    - mysql_replicate
    - mongodb_sync
    - redis_cache
capabilities:
  - Real-time replication
  - Cross-database sync
  - Schema migration
  - Conflict resolution
input:
  - Source database config
  - Target database config
  - Sync rules
  - Transformation mappings
output:
  - Synced data
  - Replication logs
  - Conflict reports
  - Migration status
languages:
  - en
related_skills:
  - etl-pipeline
  - sheets-automation
  - airtable-automation
---

# Database Sync

Comprehensive skill for database synchronization, replication, and data integration.

## Core Architecture

### Sync Patterns

```
DATABASE SYNC PATTERNS:
┌─────────────────────────────────────────────────────────┐
│                 ONE-WAY REPLICATION                      │
│  ┌──────────┐         ┌──────────┐                      │
│  │  Master  │ ──────▶ │  Replica │                      │
│  └──────────┘         └──────────┘                      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                 BI-DIRECTIONAL SYNC                      │
│  ┌──────────┐         ┌──────────┐                      │
│  │ Database │ ◀─────▶ │ Database │                      │
│  │    A     │         │    B     │                      │
│  └──────────┘         └──────────┘                      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                  HUB-AND-SPOKE                           │
│           ┌──────────┐                                   │
│           │  Spoke 1 │                                   │
│           └────┬─────┘                                   │
│                │                                         │
│  ┌──────────┐──┴──┌──────────┐                          │
│  │  Spoke 2 │◀───▶│   Hub    │◀────┬──────────┐        │
│  └──────────┘     └──────────┘     │  Spoke 3 │        │
│                                     └──────────┘        │
└─────────────────────────────────────────────────────────┘
```

### Sync Methods

```yaml
sync_methods:
  full_sync:
    description: "Complete data refresh"
    use_when:
      - Initial sync
      - Schema changes
      - Disaster recovery
    considerations:
      - Downtime required
      - Resource intensive
      
  incremental_sync:
    description: "Changes only"
    tracking_methods:
      - timestamps (updated_at)
      - change_data_capture (CDC)
      - triggers
      - log_based
    advantages:
      - Minimal data transfer
      - Near real-time
      
  snapshot_sync:
    description: "Point-in-time copy"
    use_when:
      - Analytics
      - Reporting
      - Backup
```

## Configuration

### Source/Target Setup

```yaml
sync_config:
  source:
    type: postgresql
    host: "source-db.example.com"
    port: 5432
    database: "production"
    credentials:
      type: secret_manager
      path: "db/source/credentials"
    ssl: required
    
  target:
    type: mysql
    host: "target-db.example.com"
    port: 3306
    database: "analytics"
    credentials:
      type: secret_manager
      path: "db/target/credentials"
    ssl: required
    
  sync_settings:
    mode: incremental
    batch_size: 10000
    parallel_tables: 4
    retry_attempts: 3
    checkpoint_interval: 5_minutes
```

### Table Mapping

```yaml
table_mappings:
  - source_table: users
    target_table: dim_users
    columns:
      id: user_id
      email: email_address
      created_at: registration_date
      status: user_status
    transformations:
      - column: status
        transform: "UPPER(status)"
      - column: email_address
        transform: "LOWER(email)"
    filters:
      - "status != 'deleted'"
      - "created_at > '2023-01-01'"
    
  - source_table: orders
    target_table: fact_orders
    columns:
      "*": "*"  # All columns
    exclude_columns:
      - internal_notes
      - deleted_at
    incremental_key: updated_at
```

## Change Data Capture

### CDC Configuration

```yaml
cdc_config:
  method: logical_replication  # or: trigger, polling
  
  postgresql:
    publication: "sync_publication"
    slot: "sync_slot"
    tables:
      - users
      - orders
      - products
      
  change_tracking:
    capture_deletes: true
    capture_before_values: true
    
  output_format:
    type: json
    include:
      - operation
      - timestamp
      - table
      - key
      - before
      - after
```

### CDC Event Processing

```yaml
cdc_events:
  example_insert:
    operation: INSERT
    timestamp: "2024-01-15T10:30:00Z"
    table: users
    key: { id: 12345 }
    after:
      id: 12345
      email: "user@example.com"
      status: "active"
      
  example_update:
    operation: UPDATE
    timestamp: "2024-01-15T10:31:00Z"
    table: users
    key: { id: 12345 }
    before:
      status: "active"
    after:
      status: "premium"
      
  example_delete:
    operation: DELETE
    timestamp: "2024-01-15T10:32:00Z"
    table: users
    key: { id: 12345 }
    before:
      id: 12345
      email: "user@example.com"
```

## Conflict Resolution

### Conflict Strategies

```yaml
conflict_resolution:
  strategies:
    - name: last_write_wins
      description: "Most recent update wins"
      resolution: |
        IF source.updated_at > target.updated_at
        THEN use source
        ELSE keep target
        
    - name: source_priority
      description: "Source always wins"
      resolution: "always use source"
      
    - name: merge
      description: "Merge non-conflicting fields"
      resolution: |
        FOR each field:
          IF only_one_changed: use_changed
          IF both_changed: use source.field
          
    - name: custom_rules
      description: "Field-specific rules"
      rules:
        - field: quantity
          strategy: sum
        - field: status
          strategy: priority_order
          order: ["active", "pending", "inactive"]
        - field: last_login
          strategy: max
```

### Conflict Logging

```yaml
conflict_log:
  format:
    timestamp: "{{time}}"
    table: "{{table}}"
    key: "{{primary_key}}"
    field: "{{conflicting_field}}"
    source_value: "{{source.value}}"
    target_value: "{{target.value}}"
    resolution: "{{applied_strategy}}"
    result: "{{final_value}}"
    
  storage:
    type: table
    name: sync_conflicts
    retention_days: 90
    
  alerting:
    threshold: 100  # conflicts per hour
    notify: ["slack:#data-alerts"]
```

## Schema Management

### Schema Sync

```yaml
schema_sync:
  mode: evolve  # or: strict, ignore
  
  operations:
    add_column:
      action: apply
      default_value: null
      
    remove_column:
      action: warn
      keep_data: true
      
    modify_type:
      action: review
      safe_changes:
        - varchar_expand
        - int_to_bigint
        
    rename_column:
      action: manual
      create_mapping: true
```

### Migration Scripts

```sql
-- Example Migration: Add new column
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS 
  loyalty_tier VARCHAR(20) DEFAULT 'bronze';

-- Example Migration: Create sync tracking table
CREATE TABLE IF NOT EXISTS _sync_metadata (
  table_name VARCHAR(100) PRIMARY KEY,
  last_sync_at TIMESTAMP,
  last_sync_key VARCHAR(255),
  records_synced BIGINT,
  status VARCHAR(20)
);

-- Example Migration: Add sync trigger
CREATE OR REPLACE FUNCTION track_changes()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO _change_log (
    table_name, operation, key, changed_at
  ) VALUES (
    TG_TABLE_NAME, TG_OP, NEW.id, NOW()
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

## Monitoring Dashboard

### Sync Status

```
DATABASE SYNC STATUS
═══════════════════════════════════════

OVERALL STATUS: ✓ Healthy

SOURCE: PostgreSQL (production)
TARGET: MySQL (analytics)
MODE:   Incremental CDC

TABLES:
┌──────────────┬──────────┬───────────┬──────────┐
│ Table        │ Status   │ Lag       │ Records  │
├──────────────┼──────────┼───────────┼──────────┤
│ users        │ ✓ Synced │ 2s        │ 1.2M     │
│ orders       │ ✓ Synced │ 5s        │ 8.5M     │
│ products     │ ✓ Synced │ 1s        │ 50K      │
│ events       │ ⚠ Behind │ 2m 30s    │ 45M      │
└──────────────┴──────────┴───────────┴──────────┘

THROUGHPUT:
Current:  5,230 records/sec
Average:  4,850 records/sec
Peak:     12,400 records/sec

LAST 24 HOURS:
Records Synced: 45.2M
Errors:         23
Conflicts:      156
```

### Metrics

```yaml
metrics:
  - name: sync_lag_seconds
    type: gauge
    labels: [table_name, sync_job]
    alert:
      warning: "> 60"
      critical: "> 300"
      
  - name: records_synced_total
    type: counter
    labels: [table_name, operation]
    
  - name: sync_errors_total
    type: counter
    labels: [table_name, error_type]
    
  - name: conflict_count
    type: counter
    labels: [table_name, resolution_strategy]
```

## Integration Examples

### PostgreSQL to BigQuery

```yaml
pg_to_bigquery:
  source:
    type: postgresql
    connection: "${PG_CONNECTION_STRING}"
    tables:
      - name: orders
        incremental_key: updated_at
        
  target:
    type: bigquery
    project: "my-project"
    dataset: "analytics"
    
  schedule: "*/5 * * * *"  # Every 5 minutes
  
  transform:
    - type: add_metadata
      columns:
        _synced_at: "CURRENT_TIMESTAMP()"
        _source: "'production'"
```

### MySQL to Elasticsearch

```yaml
mysql_to_elasticsearch:
  source:
    type: mysql
    tables:
      - products
      
  target:
    type: elasticsearch
    index: products_search
    
  mapping:
    id: _id
    name:
      type: text
      analyzer: standard
    description:
      type: text
      analyzer: english
    category:
      type: keyword
    price:
      type: float
```

## Best Practices

1. **Test Thoroughly**: Validate sync accuracy
2. **Monitor Lag**: Alert on replication delay
3. **Handle Conflicts**: Define clear resolution rules
4. **Backup Before Migration**: Protect data
5. **Use Incremental**: Minimize load
6. **Log Everything**: Maintain audit trail
7. **Plan for Failures**: Implement retry logic
8. **Schema Evolution**: Handle changes gracefully
