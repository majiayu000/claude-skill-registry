---
name: railway-logs
description: Railway log access and analysis for debugging and monitoring. Covers build logs, deploy logs, runtime logs, HTTP logs, filtering, search, and external export. Use when viewing logs, debugging Railway deployments, investigating errors, analyzing HTTP requests, filtering log output, or exporting logs to external systems.
---

# Railway Logs

Access and analyze Railway logs for debugging and monitoring applications.

## Overview

Railway provides comprehensive logging across the deployment lifecycle:
- **Build Logs**: Build process output and compilation
- **Deploy Logs**: Deployment lifecycle and health checks
- **Runtime Logs**: Application stdout/stderr output
- **HTTP Logs**: Request metadata (status, path, IP, timing)

All logs support filtering, search, and can be exported to external systems for long-term retention.

**Keywords**: Railway logs, build logs, deploy logs, runtime logs, HTTP logs, log filtering, log search, debugging, monitoring, observability

## When to Use This Skill

- Debugging deployment failures
- Investigating runtime errors
- Monitoring application behavior
- Analyzing HTTP request patterns
- Filtering logs for specific events
- Exporting logs to external systems (Datadog, Axiom, BetterStack)
- Understanding build/deploy process
- Troubleshooting performance issues

---

## Prerequisites: Link Project First

**Important**: CLI logs require a linked project with Account Token:

```bash
# 1. Set Account Token (NOT project token)
export RAILWAY_API_TOKEN=<your-account-token>

# 2. Link project/environment/service
railway link -p <PROJECT_ID> -e <ENVIRONMENT_ID> -s <SERVICE_ID>

# Example:
railway link -p f8fff4f1-1541-4a47-b509-0c30b9459275 \
             -e 3aa108f4-781d-433c-9eee-875c3dbe903d \
             -s 4b879f5f-5e42-4804-a67c-2a1ff2475cb3

# 3. Verify link
railway status
```

See [cli-commands.md](references/cli-commands.md) for complete reference.

---

## Operations

### Operation 1: View Build Logs

Access build process logs to debug compilation and dependency issues.

**CLI Commands**:
```bash
# Stream build logs (live)
railway logs --build

# Last 100 lines of build logs
railway logs --build --lines 100

# Build logs for specific deployment
railway logs --build <DEPLOYMENT_ID>

# Export build logs to file
railway logs --build --lines 500 > build-logs.txt
```

**Dashboard Access**:
1. Navigate to Railway Dashboard → Your Service
2. Click **Deployments** tab
3. Select deployment
4. View **Build Logs** section

**What to Look For**:
- ✅ Dependency installation success
- ✅ Build steps completion
- ⚠️ Warning messages (may indicate future issues)
- ❌ Build failures and error messages
- 📊 Build time (optimization opportunities)

**Common Issues**:
| Issue | Solution |
|-------|----------|
| Dependencies not installing | Check package.json/requirements.txt |
| Build timeout | Optimize build process or increase timeout |
| Missing build command | Set in Railway dashboard or railway.json |
| Cache issues | Force rebuild without cache |

**See Also**: [railway-troubleshooting](../railway-troubleshooting/SKILL.md) for cache busting

---

### Operation 2: View Deploy Logs

Monitor deployment lifecycle and health check status.

**CLI Commands**:
```bash
# Stream deployment logs (live)
railway logs --deployment

# Last N lines of deploy logs
railway logs --deployment --lines 200

# Specific deployment by ID
railway logs --deployment <DEPLOYMENT_ID>

# Export deploy logs
railway logs --deployment --lines 500 > deploy-logs.txt
```

**Dashboard Access**:
1. Railway Dashboard → Service → Deployments
2. Select deployment
3. View **Deploy Logs** section

**Deployment Phases**:
1. **Building** - Compiling code
2. **Publishing** - Creating container image
3. **Deploying** - Rolling out to infrastructure
4. **Health Checking** - Verifying service health
5. **Active** - Deployment live

**Health Check Debugging**:
```bash
# View health check failures
railway logs --deployment | grep "health check"

# Common health check issues:
# - Port not exposed correctly
# - Application not binding to 0.0.0.0
# - Health endpoint not responding
# - Application crashing during startup
```

**Troubleshooting**:
- Health check failing? Verify `PORT` environment variable
- Deployment stuck? Check for blocking startup processes
- Rollback occurring? Check health check configuration

---

### Operation 3: View Runtime Logs

Access application stdout/stderr for debugging runtime behavior.

**CLI Commands**:
```bash
# Stream runtime logs (live, Ctrl+C to stop)
railway logs

# Last N lines (stops streaming)
railway logs --lines 500

# Stream different service/environment
railway logs --service backend --environment production

# Filter with Railway syntax
railway logs --filter "@level:error"
railway logs --lines 100 --filter "timeout"

# Pipe to grep for local filtering
railway logs | grep ERROR

# JSON output for parsing
railway logs --json | jq 'select(.level == "error")'
```

**Dashboard Access**:
1. Railway Dashboard → Service → Observability
2. Click **Logs** tab
3. Real-time log stream with filtering

**Structured Logging Best Practices**:

Railway supports structured JSON logging. Output JSON on a **single line**:

```javascript
// Node.js Example
console.log(JSON.stringify({
  level: 'error',
  message: 'Database connection failed',
  error: err.message,
  timestamp: new Date().toISOString(),
  userId: req.user?.id
}));
```

```python
# Python Example
import json
import logging

logging.basicConfig(format='%(message)s')
logger = logging.getLogger()

logger.error(json.dumps({
    'level': 'error',
    'message': 'Database connection failed',
    'error': str(e),
    'timestamp': datetime.utcnow().isoformat(),
    'user_id': user_id
}))
```

**Supported Log Levels**:
- `debug` - Detailed diagnostic information
- `info` - General informational messages
- `warn` - Warning messages (potential issues)
- `error` - Error messages (failures)

**Benefits**:
- All JSON fields are searchable in Railway dashboard
- Better filtering and analysis
- Integration with log aggregation tools

---

### Operation 4: View HTTP Logs

Analyze HTTP request patterns and debug API issues.

**Dashboard Access**:
1. Railway Dashboard → Service → Observability
2. Click **HTTP** tab
3. View request metadata

**Available Metadata**:
- HTTP method (GET, POST, etc.)
- Request path
- Status code
- Response time (ms)
- Client IP address
- User agent
- Timestamp

**Filtering HTTP Logs**:
```
# Filter by status code
@httpStatus:500

# Filter by path
@path:"/api/users"

# Combine filters
@httpStatus:500 AND @path:"/api"
```

**Use Cases**:
- Identify slow endpoints (high response time)
- Find error patterns (500, 404 status codes)
- Analyze traffic patterns
- Debug API issues
- Monitor rate limits

**Performance Analysis**:
```bash
# Find slow requests (>1000ms)
# Filter in dashboard: responseTime > 1000

# Find all 5xx errors
# Filter: @httpStatus:5xx

# Analyze specific endpoint
# Filter: @path:"/api/checkout"
```

---

### Operation 5: Filter and Search Logs

Use Railway's powerful filtering syntax for targeted log analysis.

**Filter Syntax**:

| Filter | Example | Description |
|--------|---------|-------------|
| Substring | `"error"` | Search for text |
| HTTP Status | `@httpStatus:500` | Filter by status code |
| Service ID | `@service:<id>` | Filter by service |
| Log Level | `@level:error` | Filter by severity |
| Custom Field | `@userId:123` | Filter by JSON field |

**Boolean Operators**:
```
# AND - Both conditions must match
@httpStatus:500 AND @path:"/api"

# OR - Either condition matches
@level:error OR @level:warn

# NOT - Exclude matches
NOT @path:"/health"

# Grouping
(@level:error OR @level:warn) AND @service:api
```

**Common Filter Patterns**:

```bash
# All errors from last hour
@level:error

# Slow HTTP requests (>1000ms)
@httpStatus:200 AND responseTime > 1000

# Failed API calls
@path:"/api" AND @httpStatus:5xx

# Exclude health checks
NOT @path:"/health" NOT @path:"/metrics"

# Specific user errors
@level:error AND @userId:12345

# Database connection issues
"connection refused" OR "timeout"
```

**Dashboard Filtering**:
1. Observability → Logs
2. Enter filter in search box
3. Use dropdowns for common filters
4. Save frequent filters as presets

**CLI Filtering**:
```bash
# Use grep for basic filtering (streaming is default)
railway logs | grep ERROR

# Use jq for JSON logs
railway logs --json | jq 'select(.level == "error")'

# Complex filtering with awk
railway logs | awk '/ERROR/ || /WARN/'
```

---

### Operation 6: Export Logs Externally

Export logs to external systems for long-term retention and analysis.

**Why Export?**
- Railway retention: 7-30 days (plan dependent)
- Long-term log storage
- Advanced analytics
- Compliance requirements
- Centralized multi-service logging

**External Export Options**:

#### Option 1: Locomotive Sidecar (Webhook Export)

Deploy a sidecar container to forward logs via webhooks.

**Repository**: https://github.com/railwayapp/locomotive

**Setup**:
```bash
# Add locomotive service to Railway project
railway service create locomotive

# Configure environment variables
WEBHOOK_URL=https://your-log-endpoint.com/ingest
WEBHOOK_METHOD=POST
WEBHOOK_HEADERS='{"Authorization": "Bearer xxx"}'

# Deploy locomotive
railway up
```

**Supported Destinations**:
- Custom webhooks
- Datadog
- Axiom
- BetterStack
- Logtail
- Any HTTP endpoint

#### Option 2: OpenTelemetry (OTEL) Integration

Send logs using OTEL protocol.

**Environment Variables**:
```bash
# Add to your service
OTEL_EXPORTER_OTLP_ENDPOINT=https://otel-collector.example.com:4318
OTEL_EXPORTER_OTLP_HEADERS=x-api-key=xxx
OTEL_SERVICE_NAME=my-railway-service
```

**Supported OTEL Collectors**:
- Grafana Alloy
- OpenTelemetry Collector
- Datadog Agent
- New Relic
- Honeycomb

**See Also**: [observability-stack-setup](../observability-stack-setup/SKILL.md) for LGTM stack

#### Option 3: Log Streaming Script

Use the provided script to stream logs to external systems.

**Usage**:
```bash
# Stream to file
.claude/skills/railway-logs/scripts/stream-logs.sh --output file --path logs/

# Stream to webhook
.claude/skills/railway-logs/scripts/stream-logs.sh --output webhook \
  --url https://logs.example.com/ingest \
  --token YOUR_API_KEY

# Stream to S3
.claude/skills/railway-logs/scripts/stream-logs.sh --output s3 \
  --bucket my-logs-bucket \
  --prefix railway/
```

**Features**:
- Continuous streaming
- Automatic reconnection
- Buffering and batching
- Multiple output formats

#### Option 4: Manual Export

Export logs for ad-hoc analysis.

```bash
# Export last 1000 lines
railway logs --lines 1000 > logs-$(date +%Y%m%d-%H%M%S).txt

# Export recent logs (specify number of lines)
railway logs --lines 1000 > logs-recent.txt

# Export and compress
railway logs --lines 5000 | gzip > logs.txt.gz
```

**Scheduled Export** (cron):
```bash
# Add to crontab (every 6 hours)
0 */6 * * * railway logs --lines 10000 > /backup/railway-logs-$(date +\%Y\%m\%d-\%H\%M).txt
```

---

## Integration with External Tools

### Datadog

```bash
# Install Datadog agent in Railway
# Add environment variables:
DD_API_KEY=xxx
DD_SITE=datadoghq.com
DD_LOGS_ENABLED=true
DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true
```

### Axiom

```bash
# Use locomotive sidecar
WEBHOOK_URL=https://api.axiom.co/v1/datasets/<dataset>/ingest
WEBHOOK_HEADERS='{"Authorization": "Bearer <token>"}'
```

### BetterStack (Logtail)

```bash
# Add to your application
LOGTAIL_SOURCE_TOKEN=xxx

# Use Logtail SDK
npm install @logtail/node
```

### Grafana Loki

```bash
# Deploy Grafana Agent/Alloy
# Configure to scrape Railway logs
# See observability-stack-setup skill
```

---

## Best Practices

### 1. Structured Logging

**DO**:
```javascript
console.log(JSON.stringify({ level: 'info', message: 'User login', userId: 123 }));
```

**DON'T**:
```javascript
console.log(`User ${userId} logged in`); // Hard to search/filter
```

### 2. Log Levels

Use appropriate severity:
- `debug` - Development/troubleshooting only
- `info` - Normal operations
- `warn` - Potential issues (high memory, slow queries)
- `error` - Failures requiring attention

### 3. Sensitive Data

**NEVER log**:
- Passwords
- API keys
- Credit card numbers
- Personal identifiable information (PII)

**Redact sensitive data**:
```javascript
console.log(JSON.stringify({
  level: 'info',
  message: 'User login',
  email: 'u***@example.com', // Redacted
  ip: req.ip
}));
```

### 4. Performance

**Avoid excessive logging**:
```javascript
// BAD - Logs every request
app.use((req, res, next) => {
  console.log(`Request: ${req.method} ${req.path}`);
  next();
});

// GOOD - Log only errors or important events
app.use((req, res, next) => {
  if (res.statusCode >= 400) {
    console.log(JSON.stringify({ level: 'error', method: req.method, path: req.path, status: res.statusCode }));
  }
  next();
});
```

### 5. External Export

For production:
- Export logs to external system (Railway retention is limited)
- Use structured logging (JSON)
- Implement log rotation
- Set up alerts on error patterns

---

## Troubleshooting Common Issues

| Issue | Solution |
|-------|----------|
| Logs not appearing | Check application is writing to stdout/stderr |
| JSON logs not parsing | Ensure JSON is on single line (no newlines) |
| Logs truncated | Railway may truncate very long log lines (>10KB) |
| Missing logs | Check log retention period for your plan |
| Can't filter by custom field | Verify field is in structured JSON log |
| High log volume | Reduce logging verbosity, sample logs |

---

## Quick Reference

| Task | Command |
|------|---------|
| Stream runtime logs | `railway logs` |
| Last N lines | `railway logs --lines 100` |
| Build logs | `railway logs --build` |
| Deploy logs | `railway logs --deployment` |
| Export to file | `railway logs --lines 500 > output.txt` |
| Filter errors | `railway logs \| grep ERROR` |
| JSON filtering | `railway logs --json \| jq 'select(.level == "error")'` |

---

## Important: CLI vs API

**Use CLI for logs, not API.** The Railway GraphQL API log queries (`deploymentLogs`, `buildLogs`) often return "Problem processing request". The CLI provides reliable log access:

```bash
railway logs                    # Runtime logs
railway logs --deployment       # Build/deploy logs
railway logs --lines 100        # Historical logs
```

See [railway-api/references/api-limitations.md](../railway-api/references/api-limitations.md) for details.

---

## Related Skills

- [railway-troubleshooting](../railway-troubleshooting/SKILL.md) - Debug deployment issues
- [railway-api](../railway-api/SKILL.md) - Programmatic log access
- [observability-stack-setup](../observability-stack-setup/SKILL.md) - LGTM stack with Loki
- [railway-project-management](../railway-project-management/SKILL.md) - Project setup

---

## References

See the `references/` directory for detailed guides:

- [cli-commands.md](references/cli-commands.md) - **Complete CLI reference (verified working)**
- [log-filtering-syntax.md](references/log-filtering-syntax.md) - Complete filter syntax reference
- [structured-logging.md](references/structured-logging.md) - Structured logging best practices
- [external-export.md](references/external-export.md) - External export integration guides

## Scripts

See the `scripts/` directory for automation tools:

- [stream-logs.sh](scripts/stream-logs.sh) - Stream and filter logs
- [export-logs.sh](scripts/export-logs.sh) - Export logs to file/webhook

---

**Last Updated**: 2025-11-26
