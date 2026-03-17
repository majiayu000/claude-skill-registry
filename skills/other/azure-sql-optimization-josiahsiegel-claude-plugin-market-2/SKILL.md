---
name: azure-sql-optimization
description: |
  Azure SQL Database optimization and platform-specific features. Use this skill when: (1) User asks about Azure SQL Database optimization, (2) User needs DTU/vCore guidance, (3) User wants to use automatic tuning, (4) User asks about Hyperscale or serverless, (5) User needs Azure SQL performance monitoring.
---

# Azure SQL Database Optimization

Platform-specific optimization for Azure SQL Database.

## Quick Reference

### Service Tier Comparison

| Tier | Best For | Max Size | Key Features |
|------|----------|----------|--------------|
| Basic | Dev/test, light workloads | 2 GB | Low cost |
| Standard | General workloads | 1 TB | S0-S12 DTUs |
| Premium | High I/O, low latency | 4 TB | P1-P15 DTUs |
| General Purpose (vCore) | Most workloads | 16 TB | Serverless option |
| Business Critical | High availability | 4 TB | In-memory, read replicas |
| Hyperscale | Large databases | 100 TB | Auto-scaling storage |

### DTU vs vCore

| Aspect | DTU | vCore |
|--------|-----|-------|
| Pricing | Bundled resources | Separate compute/storage |
| Control | Limited | Fine-grained |
| Reserved capacity | No | Yes (up to 72% savings) |
| Serverless | No | Yes (General Purpose) |
| Best for | Simple workloads | Predictable, migrated workloads |

## Performance Monitoring

### Resource Consumption
```sql
-- Last 15 minutes (avg 15-second intervals)
SELECT
    end_time,
    avg_cpu_percent,
    avg_data_io_percent,
    avg_log_write_percent,
    avg_memory_usage_percent,
    max_worker_percent,
    max_session_percent
FROM sys.dm_db_resource_stats
ORDER BY end_time DESC;

-- Historical (last 14 days, hourly)
SELECT
    start_time,
    end_time,
    avg_cpu_percent,
    avg_data_io_percent,
    avg_log_write_percent
FROM sys.resource_stats
WHERE database_name = DB_NAME()
ORDER BY start_time DESC;
```

### Query Performance Insight
```sql
-- Top CPU consumers last hour
SELECT TOP 20
    qt.query_sql_text,
    rs.avg_cpu_time / 1000 AS avg_cpu_ms,
    rs.count_executions,
    rs.avg_cpu_time * rs.count_executions / 1000 AS total_cpu_ms
FROM sys.query_store_query q
JOIN sys.query_store_query_text qt ON q.query_text_id = qt.query_text_id
JOIN sys.query_store_plan p ON q.query_id = p.query_id
JOIN sys.query_store_runtime_stats rs ON p.plan_id = rs.plan_id
JOIN sys.query_store_runtime_stats_interval rsi ON rs.runtime_stats_interval_id = rsi.runtime_stats_interval_id
WHERE rsi.start_time >= DATEADD(hour, -1, GETUTCDATE())
ORDER BY rs.avg_cpu_time * rs.count_executions DESC;
```

## Automatic Tuning

### Enable Automatic Tuning
```sql
-- Enable all auto-tuning options
ALTER DATABASE current
SET AUTOMATIC_TUNING (
    FORCE_LAST_GOOD_PLAN = ON,
    CREATE_INDEX = ON,
    DROP_INDEX = ON
);

-- Check current settings
SELECT * FROM sys.database_automatic_tuning_options;
```

### View Tuning Recommendations
```sql
-- Current recommendations
SELECT
    name,
    reason,
    score,
    state_desc,
    is_revertable_action,
    is_executable_action,
    details
FROM sys.dm_db_tuning_recommendations;
```

### Apply Recommendations
```sql
-- Force a specific query plan
EXEC sp_query_store_force_plan @query_id = 12345, @plan_id = 67890;

-- Unforce plan
EXEC sp_query_store_unforce_plan @query_id = 12345, @plan_id = 67890;
```

## Hyperscale Features

### Storage Auto-Scaling
- Automatically grows up to 128 TB
- No need to pre-provision storage
- Pay only for storage used

### Read Scale-Out
```sql
-- Connection string option
ApplicationIntent=ReadOnly

-- In application code
"Server=myserver.database.windows.net;Database=mydb;ApplicationIntent=ReadOnly;..."
```

### Named Replicas
```sql
-- Create named replica
ALTER DATABASE MyDatabase
ADD SECONDARY ON SERVER MySecondaryServer
WITH (SERVICE_OBJECTIVE = 'HS_Gen5_2', SECONDARY_TYPE = Named, NAME = N'MyReadReplica');
```

## Serverless Configuration

### Configure Auto-Pause
```sql
-- Via Azure Portal, CLI, or PowerShell
-- Set auto-pause delay (minutes), min/max vCores

-- Check current usage
SELECT
    cpu_percent,
    auto_pause_delay_in_minutes_configured
FROM sys.dm_db_resource_stats_serverless;
```

### Serverless Best Practices
1. **Use for intermittent workloads** - Saves cost during idle periods
2. **Set appropriate min vCores** - Prevents cold starts for time-sensitive apps
3. **Monitor auto-pause** - Auto-resume adds latency
4. **Consider always-on for consistent workloads** - Provisioned may be cheaper

## Connection Optimization

### Connection Pooling
```csharp
// .NET connection string
"Server=tcp:myserver.database.windows.net,1433;Database=mydb;
 Min Pool Size=10;Max Pool Size=100;Connection Timeout=30;"
```

### Retry Logic
```csharp
// Azure SQL requires retry logic for transient faults
var options = new SqlRetryLogicOption()
{
    NumberOfTries = 5,
    DeltaTime = TimeSpan.FromSeconds(1),
    MaxTimeInterval = TimeSpan.FromSeconds(30)
};
```

### Connection Best Practices
1. **Use connection pooling** - Reduce connection overhead
2. **Implement retry logic** - Handle transient faults (error 40613, 40197)
3. **Use redirect connection mode** - Better performance after initial connection
4. **Close connections promptly** - Don't hold connections unnecessarily

## Azure-Specific Limitations

### Not Supported
- SQL Agent (use Azure Functions, Logic Apps)
- BULK INSERT from files (use Blob Storage)
- Linked servers (use Elastic Query)
- FILESTREAM
- Cross-database queries in same server (use Elastic Query)

### Workarounds

#### Bulk Insert from Blob Storage
```sql
-- Create credential
CREATE DATABASE SCOPED CREDENTIAL BlobCredential
WITH IDENTITY = 'SHARED ACCESS SIGNATURE',
SECRET = 'your_sas_token';

-- Create external data source
CREATE EXTERNAL DATA SOURCE BlobStorage
WITH (
    TYPE = BLOB_STORAGE,
    LOCATION = 'https://youraccount.blob.core.windows.net/container',
    CREDENTIAL = BlobCredential
);

-- Bulk insert
BULK INSERT MyTable
FROM 'data.csv'
WITH (DATA_SOURCE = 'BlobStorage', FORMAT = 'CSV', FIRSTROW = 2);
```

#### Elastic Query for Cross-Database
```sql
-- On target database
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'password';

CREATE DATABASE SCOPED CREDENTIAL ElasticCredential
WITH IDENTITY = 'username', SECRET = 'password';

CREATE EXTERNAL DATA SOURCE RemoteDB
WITH (
    TYPE = RDBMS,
    LOCATION = 'remote-server.database.windows.net',
    DATABASE_NAME = 'RemoteDatabase',
    CREDENTIAL = ElasticCredential
);

CREATE EXTERNAL TABLE dbo.RemoteTable (...)
WITH (DATA_SOURCE = RemoteDB);
```

## Cost Optimization

### Reserved Capacity
- Up to 72% savings vs pay-as-you-go
- 1-year or 3-year terms
- Exchange/refund flexibility

### Right-Sizing
```sql
-- Check if over-provisioned
SELECT
    AVG(avg_cpu_percent) AS avg_cpu,
    MAX(avg_cpu_percent) AS max_cpu,
    AVG(avg_data_io_percent) AS avg_io,
    MAX(avg_data_io_percent) AS max_io
FROM sys.dm_db_resource_stats
WHERE end_time >= DATEADD(day, -7, GETUTCDATE());

-- If avg < 40% consistently, consider downsizing
```

### Hyperscale Cost Considerations
- Compute: Per-second billing
- Storage: Per-hour billing for used space
- Read replicas: Additional compute cost
- Memory not automatically released (monitor and scale appropriately)

