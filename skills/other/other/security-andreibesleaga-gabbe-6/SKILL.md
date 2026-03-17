---
name: log-analysis
description: Parsing structured logs, finding patterns in noise, and ELK/Splunk querying.
role: ops-monitor
triggers:
  - analyze logs
  - parse logs
  - kibana
  - splunk
  - grep logs
  - error rate
---

# log-analysis Skill

This skill helps agents and engineers interpret logging data to find root causes of issues.

## 1. Structured Logging (The Prerequisite)
- **Format**: JSON. Always.
- **Why**: Allows querying `level="ERROR" AND service="user-api"`. Text logs require fragile regex.
- **Context**: Every log must have `trace_id`, `user_id`, and `environment`.

## 2. Analysis Workflow

1.  **Scope the Timeframe**: "Last 15 minutes" or "Since deployment at 14:00".
2.  **Filter by Level**: Start with `ERROR` and `FATAL`. Ignore `INFO` initially.
3.  **Group by Message**:
    - **Bad**: Reading 1000 lines of `Connection timeout`.
    - **Good**: "Count of errors by message type: Timeout (800), Auth Fail (200)".
4.  **Trace Correlation**: take one `trace_id` from an error and filter ALL logs (inc INFO) for that ID to see the sequence of events leading to failure.

## 3. Query Cheatsheet

### Loki (LogQL)
```logql
{app="frontend"} |= "error" | json | latency > 500ms
```

### Elasticsearch / Kibana (Lucene)
```lucene
service:backend AND level:ERROR AND NOT message:"healthcheck"
```

### Splunk
```splunk
index=prod sourcetype=k8s | stats count by message | sort - count
```

### Command Line (jq)
```bash
cat logs.json | jq 'select(.level=="error") | .message' | sort | uniq -c
```

## 4. Red Flags ("Smells")
- **"Swallowed Exception"**: Logs that say "Error occurred" but print no stack trace.
- **"Noise"**: Periodic errors (e.g., every 5 mins) that everyone ignores. These mask real issues.
- **"Sensitive Data"**: Passwords or PII in logs. -> **CRITICAL**: Report immediately.
