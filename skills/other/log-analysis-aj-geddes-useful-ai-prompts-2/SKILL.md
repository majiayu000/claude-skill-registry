---
name: log-analysis
description: Analyze application and system logs to identify errors, patterns, and root causes. Use log aggregation tools and structured logging for effective debugging.
---

# Log Analysis

## Overview

Logs are critical for debugging and monitoring. Effective log analysis quickly identifies issues and enables root cause analysis.

## When to Use

- Troubleshooting errors
- Performance investigation
- Security incident analysis
- Auditing user actions
- Monitoring application health

## Instructions

### 1. **Structured Logging**

```javascript
// Good: Structured logs (machine-readable)
logger.info({
  level: 'INFO',
  timestamp: '2024-01-15T10:30:00Z',
  service: 'auth-service',
  user_id: '12345',
  action: 'user_login',
  status: 'success',
  duration_ms: 150,
  ip_address: '192.168.1.1'
});

// Bad: Unstructured logs (hard to parse)
console.log('User 12345 logged in successfully in 150ms from 192.168.1.1');

// JSON Format (Elasticsearch friendly)
{
  "@timestamp": "2024-01-15T10:30:00Z",
  "level": "ERROR",
  "service": "api-gateway",
  "trace_id": "abc123",
  "message": "Database connection failed",
  "error": {
    "type": "ConnectionError",
    "code": "ECONNREFUSED"
  },
  "context": {
    "database": "users",
    "operation": "SELECT"
  }
}
```

### 2. **Log Levels & Patterns**

```yaml
Log Levels:

DEBUG: Detailed diagnostic info
  - Variable values
  - Function entry/exit
  - Intermediate calculations
  - Use: Development only

INFO: General informational messages
  - Startup/shutdown
  - User actions
  - Configuration changes
  - Use: Production (normal operations)

WARN: Warning messages (potential issues)
  - Deprecated API usage
  - Performance degradation
  - Resource limits approaching
  - Use: Production (investigate soon)

ERROR: Error conditions
  - Failed operations
  - Exceptions
  - Failed requests
  - Use: Production (action required)

FATAL/CRITICAL: System unusable
  - Critical failures
  - Out of memory
  - Data corruption
  - Use: Production (immediate action)

---

Log Patterns:

Request Logging:
  - Request ID (trace_id)
  - Method + Path
  - Status code
  - Duration
  - Request size / response size

Error Logging:
  - Error type/code
  - Error message
  - Stack trace
  - Context (user_id, session_id)
  - Timestamp

Business Events:
  - Event type
  - User involved
  - Impact/importance
  - Timestamp
  - Relevant context
```

### 3. **Log Analysis Tools**

```yaml
Log Aggregation:

ELK Stack (Elasticsearch, Logstash, Kibana):
  - Logstash: Parse and process logs
  - Elasticsearch: Search and analyze
  - Kibana: Visualization and dashboards
  - Use: Large scale, complex queries

Splunk:
  - Comprehensive log management
  - Real-time search and analysis
  - Dashboards and alerts
  - Use: Enterprise (expensive)

CloudWatch (AWS):
  - Integrated with AWS services
  - Log Insights for querying
  - Dashboards
  - Use: AWS-based systems

Datadog:
  - Application performance monitoring
  - Log management
  - Real-time alerts
  - Use: SaaS monitoring

---

Log Analysis Techniques:

Grep/Awk:
  grep "ERROR" app.log
  awk '{print $1, $4}' app.log

Filtering:
  Filter by timestamp
  Filter by service
  Filter by error type
  Filter by user

Searching:
  Search for error patterns
  Search for user actions
  Search trace IDs
  Search IP addresses

Aggregation:
  Count occurrences
  Group by error type
  Calculate duration percentiles
  Rate of errors over time
```

### 4. **Common Log Analysis Queries**

```yaml
Find errors in past hour:
  timestamp: last_1h AND level: ERROR

Track user activity:
  user_id: 12345 AND action: *

Find slow requests:
  duration_ms: >1000 AND level: INFO

Analyze error rate by service:
  level: ERROR | stats count by service

Find failed database operations:
  error.type: "DatabaseError" | stats count

Trace request flow:
  trace_id: "abc123" | sort by timestamp

---

Checklist:

[ ] Structured logging implemented
[ ] All errors logged with context
[ ] Request IDs/trace IDs used
[ ] Sensitive data not logged (passwords, tokens)
[ ] Log levels used appropriately
[ ] Log retention policy set
[ ] Log sampling for high-volume events
[ ] Alerts configured for errors
[ ] Dashboards created
[ ] Regular log review scheduled
[ ] Log analysis tools accessible
[ ] Team trained on querying logs
```

## Key Points

- Use structured JSON logging
- Include trace IDs for request tracking
- Log appropriate levels (DEBUG/INFO/ERROR)
- Never log sensitive data (passwords, tokens)
- Aggregate logs centrally
- Create dashboards for key metrics
- Alert on error rates and critical issues
- Retain logs appropriately
- Search logs by trace ID for troubleshooting
- Review logs regularly for patterns
