---
name: fabric-rti-mcp
description: Expert guidance for Microsoft Fabric Real-Time Intelligence (RTI) using the Fabric RTI MCP Server. Execute KQL queries on Eventhouse, manage Eventstreams for real-time data processing, create Activator triggers for alerting, and manage Map items. Use when working with Fabric RTI, KQL, real-time analytics, streaming data, or event-driven applications.
---

# Microsoft Fabric RTI Expert

Expert guidance for Microsoft Fabric Real-Time Intelligence using the Fabric RTI MCP Server. Work with Eventhouse databases, Eventstreams, Activators, and Maps through natural language.

## Core Capabilities

1. **Eventhouse/KQL** (12 tools) - Query data, manage schemas, sample data
2. **Eventstreams** (17 tools) - Build real-time streaming pipelines
3. **Activator** (2 tools) - Create triggers and alerts
4. **Map** (7 tools) - Manage data visualizations

## Quick Reference

### Eventhouse Tools
- `kusto_query` - Execute KQL queries
- `kusto_list_tables` - List tables in database
- `kusto_get_table_schema` - Get table schema
- `kusto_sample_table_data` - Sample table records
- `kusto_ingest_inline_into_table` - Ingest CSV data

### Eventstream Tools
- `eventstream_list` - List Eventstreams
- `eventstream_create` - Create new Eventstream
- `eventstream_add_sample_data_source` - Add sample data source
- `eventstream_add_eventhouse_destination` - Add Eventhouse destination
- `eventstream_validate_definition` - Validate configuration

### Activator Tools
- `activator_list_artifacts` - List triggers
- `activator_create_trigger` - Create alert trigger

### Map Tools
- `map_list` - List Maps
- `map_create` - Create new Map
- `map_get_definition` - Get Map configuration

---

## Instructions

### Querying Data with KQL

**kusto_query**
Execute KQL queries against Eventhouse databases.

Parameters:
- database (string) - Target database name
- query (string) - KQL query text

Example:
```kql
StormEvents
| where State == "ILLINOIS" and EventType == "Flood"
| summarize Count=count() by StartTime
| order by StartTime desc
```

**kusto_sample_table_data**
Get sample records from a table.

Parameters:
- table_name (string)
- sample_count (number, default: 10)

---

### Managing Eventstreams

**eventstream_create**
Create a new Eventstream for real-time data processing.

Parameters:
- workspace_id (string)
- display_name (string)
- description (string, optional)

**eventstream_add_sample_data_source**
Add sample data source to Eventstream.

**eventstream_add_eventhouse_destination**
Route data to Eventhouse for analytics.

Parameters:
- eventhouse_id (string)
- kql_database_id (string)
- table_name (string)
- input_serialization_type (string) - "Json", "Csv", etc.

**Workflow:**
```
1. eventstream_start_definition
2. eventstream_add_sample_data_source
3. eventstream_add_eventhouse_destination
4. eventstream_validate_definition
5. eventstream_create_from_definition
```

---

### Creating Activator Triggers

**activator_create_trigger**
Create triggers for real-time alerting.

Parameters:
- workspace_id (string)
- display_name (string)
- description (string)
- eventhouse_id (string)
- kql_database_id (string)
- query (string) - KQL query for monitoring
- notification_type (string) - "Email", "Teams"
- recipients (array) - Email addresses or Teams webhooks

Example: Monitor for floods and send email alert
```
Query: StormEvents | where EventType == "Flood" and State == "ILLINOIS"
Notification: Email to admin@company.com
```

---

## Common Scenarios

### Query Analysis
```
1. kusto_list_databases - Find databases
2. kusto_list_tables - Find tables
3. kusto_get_table_schema - Understand structure
4. kusto_query - Run analysis query
```

### Real-Time Pipeline
```
1. eventstream_create - Create pipeline
2. eventstream_add_custom_endpoint_source - Add data source
3. eventstream_add_derived_stream - Transform data
4. eventstream_add_eventhouse_destination - Save to database
5. eventstream_validate_definition - Check config
```

### Alerting Setup
```
1. kusto_query - Test alert condition
2. activator_create_trigger - Create alert
3. Monitor for notifications
```

---

## When to Use This Skill

- Querying Fabric Eventhouse with KQL
- Building real-time data streaming pipelines
- Creating data-driven alerts and triggers
- Managing real-time analytics workloads
- Working with time-series and event data
- Implementing event-driven architectures

## Keywords

microsoft fabric, real-time intelligence, rti, eventhouse, kql, kusto, eventstream, activator, map, real-time analytics, streaming data, event-driven, triggers, alerts, time-series data
