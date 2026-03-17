---
name: observability-dashboard-creator
description: Create and manage Grafana dashboards for Claude Code observability. Use when importing pre-built dashboards or creating custom visualizations.
---

# Observability Dashboard Creator

Import pre-built Grafana dashboards and create custom visualizations for Claude Code monitoring.

## When to Use

- After observability stack is running
- Need pre-built Claude Code dashboards
- Want to create custom dashboards
- Need to export/backup existing dashboards

## Operations

### `import-all`

Import all pre-built Claude Code dashboards to Grafana.

**Dashboards Imported**:
1. **Claude Code Overview** - Sessions, tokens, costs, errors at-a-glance
2. **Tool Performance Matrix** - Per-tool metrics (duration, failure rates)
3. **Cost Analysis** - Token usage and API cost tracking
4. **Error Tracking** - Error patterns and recent failures
5. **Session Analysis** - Session duration and conversation patterns

**Usage**:
```bash
# Invoke skill operation
import-all
```

**What Happens**:
1. Connects to Grafana API (localhost:3000)
2. Creates "Claude Code" dashboard folder
3. Imports all 5 dashboards via Grafana API
4. Sets up dashboard links and navigation
5. Verifies import success

### `import-dashboard`

Import a specific dashboard by name.

**Parameters**:
- `name`: Dashboard name (overview, tool-performance, cost-analysis, error-tracking, session-analysis)

**Example**:
```bash
import-dashboard --name overview
```

### `create-custom`

Create custom dashboard from template.

**Parameters**:
- `name`: Dashboard name
- `type`: overview, tool-specific, cost, error, session
- `panels`: Comma-separated panel types

**Example**:
```bash
create-custom \
  --name "Bash Tool Deep Dive" \
  --type tool-specific \
  --panels "duration,errors,frequency,success-rate"
```

### `export-dashboards`

Export all Claude Code dashboards to JSON (backup).

**Output**: `.observability/backups/dashboards-YYYYMMDD_HHMMSS/*.json`

### `list-dashboards`

List all Claude Code dashboards in Grafana.

**Output**:
```
Claude Code Dashboards:
1. Claude Code Overview (ID: 42)
2. Tool Performance Matrix (ID: 43)
3. Cost Analysis (ID: 44)
4. Error Tracking (ID: 45)
5. Session Analysis (ID: 46)
```

## Pre-built Dashboards

### 1. Claude Code Overview

**Panels**:
- Session Count (last 24h)
- Total Token Usage (last 24h)
- Total Cost (last 24h)
- Error Rate (last 1h)
- Token Usage Over Time (timeseries)
- Tool Call Frequency (timeseries by tool)
- Recent Errors (logs table)

**Use Cases**:
- Daily health check
- Quick status overview
- Anomaly detection

### 2. Tool Performance Matrix

**Panels** (per tool: Read, Write, Edit, Bash, etc.):
- Call count
- Average duration
- P95 latency
- P99 latency
- Success rate
- Failure rate
- Top error messages

**Use Cases**:
- Identify slow tools
- Find high-failure tools
- Performance optimization

### 3. Cost Analysis

**Panels**:
- Daily cost trend
- Weekly cost comparison
- Monthly projection
- Token usage breakdown (input vs output)
- Cost per session
- Budget alerts (configurable threshold)
- Top expensive sessions

**Use Cases**:
- Budget tracking
- Cost optimization
- Usage forecasting

### 4. Error Tracking

**Panels**:
- Error timeline (last 24h)
- Error types distribution (pie chart)
- Errors by tool (bar chart)
- Recent errors table (with details)
- Error rate trend
- Top error messages (frequency)

**Use Cases**:
- Debugging
- Error pattern detection
- Quality monitoring

### 5. Session Analysis

**Panels**:
- Session duration distribution (histogram)
- Sessions per day/week (timeseries)
- Active time vs idle time
- Conversation depth (turns per session)
- Session frequency by hour
- Average session length trend

**Use Cases**:
- Usage pattern analysis
- User engagement metrics
- Productivity insights

## Dashboard Features

All dashboards include:
- **Time range selector** (last 15m, 1h, 6h, 24h, 7d, 30d)
- **Auto-refresh** (30s, 1m, 5m, off)
- **Variables** for filtering (tool_name, session_id, etc.)
- **Annotations** for important events
- **Links** between related dashboards

## References

- `references/dashboards/claude-code-overview.json` - Overview dashboard
- `references/dashboards/tool-performance-matrix.json` - Tool metrics
- `references/dashboards/cost-analysis.json` - Cost tracking
- `references/dashboards/error-tracking.json` - Error monitoring
- `references/dashboards/session-analysis.json` - Session analytics
- `references/grafana-api-guide.md` - Grafana API usage

## Scripts

- `scripts/import-all-dashboards.sh` - Import all pre-built dashboards
- `scripts/export-dashboards.sh` - Backup dashboards to JSON
- `scripts/create-folder.sh` - Create "Claude Code" dashboard folder
