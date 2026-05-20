---
name: claude-code-telemetry-enable
description: Enable and configure Claude Code OTEL telemetry for local or Railway observability stacks. Use when setting up Claude Code to send metrics, logs, and traces to observability backends.
---

# Claude Code Telemetry Enable

Enable OpenTelemetry telemetry in Claude Code to send metrics, logs, and traces to your observability stack (local LGTM or Railway).

## When to Use

- After deploying observability stack (`observability-stack-setup`)
- Need to enable Claude Code monitoring
- Want to configure telemetry for local or cloud backends
- Need to verify telemetry connectivity

## What This Skill Does

Creates Claude Code environment configuration files that enable:
- **Metrics**: Token usage, costs, session counts, tool performance
- **Logs**: User prompts (full content), tool results, API requests/errors
- **Traces**: Session flows, tool execution spans, API call traces

**Privacy Note**: Configured for **FULL LOGGING** (no redactions) per your requirements.

## Quick Start

### For Local Stack

```bash
# After running observability-stack-setup
# Invoke this skill with:
enable-local

# Claude Code will now send telemetry to localhost:4317
```

### For Railway Stack

```bash
# After deploying to Railway
# Invoke this skill with:
enable-railway --endpoint https://your-alloy.railway.app:443

# Claude Code will send telemetry to Railway
```

## Operations

### `enable-local`

Configure Claude Code for local LGTM stack.

**Creates**: `~/.config/claude-code/.env.telemetry`

**Configuration**:
```bash
CLAUDE_CODE_ENABLE_TELEMETRY=1
OTEL_METRICS_EXPORTER=otlp
OTEL_LOGS_EXPORTER=otlp
OTEL_EXPORTER_OTLP_PROTOCOL=grpc
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Fast export (for development)
OTEL_METRIC_EXPORT_INTERVAL=10000  # 10 seconds
OTEL_LOGS_EXPORT_INTERVAL=5000     # 5 seconds

# FULL LOGGING (no privacy restrictions)
OTEL_LOG_USER_PROMPTS=1
OTEL_METRICS_INCLUDE_SESSION_ID=true
OTEL_METRICS_INCLUDE_VERSION=true
OTEL_METRICS_INCLUDE_ACCOUNT_UUID=true
```

### `enable-railway`

Configure Claude Code for Railway-hosted LGTM stack.

**Parameters**:
- `--endpoint`: Railway Alloy OTLP endpoint URL
- `--token`: (Optional) Railway authentication token

**Example**:
```bash
enable-railway \
  --endpoint https://your-alloy-abc123.railway.app:443 \
  --token your-railway-token
```

**Creates**: `~/.config/claude-code/.env.telemetry` with Railway endpoint

### `enable-custom`

Configure for custom OTLP endpoint (Grafana Cloud, DataDog, etc.).

**Parameters**:
- `--endpoint`: OTLP endpoint URL
- `--protocol`: `grpc` or `http` (default: grpc)
- `--headers`: Authentication headers (e.g., "Authorization=Bearer token")

**Example**:
```bash
enable-custom \
  --endpoint https://otlp.grafana.net:443 \
  --protocol grpc \
  --headers "Authorization=Basic base64encodedcreds"
```

### `verify`

Test telemetry configuration and connectivity.

**Checks**:
1. Configuration file exists
2. Required environment variables set
3. OTLP endpoint reachable
4. Test telemetry successfully sent
5. Data visible in backend (Grafana/Loki/Prometheus/Tempo)

**Output**:
```
Telemetry Configuration Check:
✅ Config file: ~/.config/claude-code/.env.telemetry
✅ CLAUDE_CODE_ENABLE_TELEMETRY=1
✅ OTLP endpoint: localhost:4317
✅ Endpoint reachable
✅ Test span sent successfully
✅ Data visible in Grafana

Status: HEALTHY - Telemetry fully operational
```

### `disable`

Turn off telemetry completely.

**Actions**:
1. Renames `.env.telemetry` to `.env.telemetry.disabled`
2. OR sets `CLAUDE_CODE_ENABLE_TELEMETRY=0`

**Re-enable**: Rename file back or use `enable-local` / `enable-railway` again

### `status`

Show current telemetry configuration.

**Output**:
```
Telemetry Status:
  State: ENABLED
  Endpoint: http://localhost:4317
  Protocol: gRPC
  Privacy: FULL LOGGING (all data captured)
  Export Intervals: Metrics 10s, Logs 5s

  Captured Data:
    - User prompts (full content)
    - Tool executions (all tools)
    - API requests (tokens, cost, latency)
    - Session metadata (IDs, version, account)
```

## Configuration Details

### Environment Variables

**Essential**:
- `CLAUDE_CODE_ENABLE_TELEMETRY`: `1` to enable, `0` to disable
- `OTEL_EXPORTER_OTLP_ENDPOINT`: OTLP endpoint URL
- `OTEL_EXPORTER_OTLP_PROTOCOL`: `grpc` or `http`

**Exporters**:
- `OTEL_METRICS_EXPORTER`: `otlp` (send metrics via OTLP)
- `OTEL_LOGS_EXPORTER`: `otlp` (send logs via OTLP)

**Export Intervals**:
- `OTEL_METRIC_EXPORT_INTERVAL`: Milliseconds between metric exports (default: 60000)
- `OTEL_LOGS_EXPORT_INTERVAL`: Milliseconds between log exports (default: 5000)

**Privacy Controls** (configured for FULL logging):
- `OTEL_LOG_USER_PROMPTS`: `1` = log full prompt content, `0` = log length only
- `OTEL_METRICS_INCLUDE_SESSION_ID`: `true` = include session IDs in metrics
- `OTEL_METRICS_INCLUDE_VERSION`: `true` = include Claude Code version
- `OTEL_METRICS_INCLUDE_ACCOUNT_UUID`: `true` = include account identifier

**Authentication** (for cloud backends):
- `OTEL_EXPORTER_OTLP_HEADERS`: Headers for authentication (e.g., "Authorization=Bearer token")

### What Gets Captured

**Metrics** (counters, gauges, histograms):
- `claude_code.session.count` - Session frequency
- `claude_code.token.usage` - Token consumption (input + output)
- `claude_code.cost.usage` - API costs in USD
- `claude_code.code_edit_tool.decision` - Accept/reject patterns
- `claude_code.active_time.total` - Engagement duration (seconds)
- `claude_code.pull_request.count` - PR creation count
- `claude_code.commit.count` - Git commit count

**Log Events** (structured JSON):
1. `claude_code.user_prompt` - User prompt submissions (full content)
2. `claude_code.tool_result` - Tool execution outcomes (tool name, status, duration)
3. `claude_code.api_request` - Claude API calls (model, tokens, cost, latency)
4. `claude_code.api_error` - Failed API requests (status codes, retry attempts)
5. `claude_code.tool_decision` - Permission decisions (approved/rejected)

**Traces** (distributed tracing):
- Session traces: Complete conversation workflows
- Tool call spans: Read, Write, Edit, Bash, Glob, Grep, Task, etc.
- Agent task spans: Parallel agent execution
- API request spans: Claude API latency breakdown

### Retention

All data stored for **365 days** (configured in observability stack).

## File Locations

**Configuration File**:
- Linux/WSL: `~/.config/claude-code/.env.telemetry`
- macOS: `~/.config/claude-code/.env.telemetry`
- Windows: `%USERPROFILE%\.config\claude-code\.env.telemetry`

**Managed Settings** (organization-enforced, optional):
- Linux: `/etc/claude-code/managed-settings.json`
- macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`
- Windows: `C:\ProgramData\ClaudeCode\managed-settings.json`

## Troubleshooting

### Telemetry Not Appearing in Grafana

**Check 1**: Is telemetry enabled?
```bash
cat ~/.config/claude-code/.env.telemetry
# Should show CLAUDE_CODE_ENABLE_TELEMETRY=1
```

**Check 2**: Is OTLP endpoint reachable?
```bash
curl -v http://localhost:4317
# Should connect (may get empty response, that's ok)
```

**Check 3**: Is observability stack running?
```bash
docker compose -f .observability/docker-compose.yml ps
# All 5 services should be "running"
```

**Check 4**: Use Claude Code and check immediately
```bash
# After using Claude Code, query Loki:
curl -s 'http://localhost:3100/loki/api/v1/query?query={job="claude_code"}' | jq .
# Should show recent logs
```

### Port Already in Use (4317)

If another service is using port 4317:

**Option 1**: Stop the conflicting service
```bash
sudo lsof -i :4317
sudo kill <PID>
```

**Option 2**: Change Alloy port in observability stack
Edit `.observability/docker-compose.yml`:
```yaml
ports:
  - "4318:4317"  # Expose on 4318 instead
```

Then update telemetry config:
```bash
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
```

### Permission Denied

If configuration file creation fails:
```bash
# Create directory manually
mkdir -p ~/.config/claude-code
chmod 755 ~/.config/claude-code

# Try again
```

## Next Steps

After enabling telemetry:

1. **Use Claude Code**: Run tools (Read, Write, Bash, etc.)
2. **Generate telemetry**: Each operation sends data
3. **View in Grafana**: Open http://localhost:3000
4. **Check dashboards**: Navigate to "Claude Code Overview"
5. **Verify metrics**: See token usage, costs, tool calls

## References

- `references/env-telemetry-local.txt` - Local configuration template
- `references/env-telemetry-railway.txt` - Railway configuration template
- `references/env-telemetry-custom.txt` - Custom endpoint template
- `references/telemetry-variables.md` - All environment variables explained
- `references/privacy-settings.md` - Privacy configuration options

## Scripts

- `scripts/enable-local.sh` - Enable for local stack
- `scripts/enable-railway.sh` - Enable for Railway
- `scripts/verify-telemetry.sh` - Test configuration and connectivity
- `scripts/disable-telemetry.sh` - Turn off telemetry
