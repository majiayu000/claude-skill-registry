---
name: loki-logql-query-specialist
description: Query and analyze logs using Loki and LogQL. Provides patterns for correlation ID tracing, error investigation, and service debugging using HuleEdu's structured logging. Integrates with Context7 for latest Loki documentation.
---

# Loki LogQL Query Specialist

Compact skill for querying HuleEdu logs using Loki and LogQL, with focus on correlation-based debugging.

## When to Use

Activate when the user:
- Needs to trace correlation IDs across services
- Wants to investigate errors or failures in logs
- Asks about LogQL query syntax or patterns
- Needs to analyze service-specific log patterns
- Wants to understand Promtail label extraction
- Mentions Loki, LogQL, log aggregation, or correlation tracing
- Needs help with Grafana log panels or queries

## Core Capabilities

- **Correlation ID Tracing**: Find all logs across services for a given correlation ID
- **Error Investigation**: Query patterns for error logs with context
- **Service-Specific Queries**: Filter logs by service/container
- **JSON Field Extraction**: Parse and filter structured log fields
- **Label Strategy**: Understand promoted labels vs message content
- **Promtail Configuration**: Label extraction and pipeline stages
- **Query Optimization**: Performance patterns and best practices
- **Context7 Integration**: Fetch latest Loki/LogQL documentation when needed

## Quick Workflow

1. Identify debugging objective (correlation trace, error investigation, service health)
2. Select appropriate query pattern from reference
3. Build LogQL query using HuleEdu label conventions
4. Execute query in Grafana or via Loki API
5. Interpret results and iterate if needed

## Common Query Patterns

**Trace by Correlation ID** (most common):
```logql
{container=~"huleedu_.*"} |= "correlation_id_value"
```

**Service-Specific Errors**:
```logql
{container="huleedu_batch_orchestrator_service"} |= "ERROR"
```

**JSON Field Filtering**:
```logql
{container=~"huleedu_.*"} | json | level="error" | correlation_id!=""
```

## Available Loki Labels

- `container` - Docker container name (e.g., `huleedu_content_service`)
- `correlation_id` - Request correlation ID (promoted label)
- `level` - Log level (INFO, ERROR, DEBUG, WARNING)
- `logger_name` - Logger instance name
- `service` - Service name from docker-compose
- `service_name` - Alternative service identifier

## Reference Documentation

- **Detailed Query Patterns**: See `reference.md` in this directory
- **Real-World Debugging Scenarios**: See `examples.md` in this directory
- **Promtail Configuration**: `/observability/promtail/promtail-config.yml`
- **LogQL Syntax Reference**: `/observability/LOGQL_SYNTAX_FIX.md`
