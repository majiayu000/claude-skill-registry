---
name: awf-debug-tools
description: Practical Python scripts for debugging awf - parse logs, diagnose issues, inspect containers, test domains
allowed-tools: Bash(python:*), Bash(docker:*), Bash(sudo:*), Read
---

# AWF Debug Tools

A collection of practical Python scripts that help agents efficiently debug and operate the awf firewall. These scripts reduce verbose Docker/log output by 80%+ and provide actionable insights instead of raw data dumps.

## Why These Scripts?

**Problem:** Docker commands and log files are verbose and hard for agents to parse. Diagnosing issues requires 10+ manual commands and produces noisy output that wastes tokens.

**Solution:** One script replaces 5-10 manual commands with clean, filtered output optimized for agent consumption. All scripts support JSON format for easy parsing.

## Available Scripts

All scripts are located in `.claude/skills/awf-debug-tools/scripts/`:

1. **parse-squid-logs.py** - Parse Squid logs and extract blocked domains with counts
2. **diagnose-awf.py** - Run automated diagnostic checks on container health and configuration
3. **inspect-containers.py** - Show concise container status without verbose docker output
4. **test-domain.py** - Test if specific domain is reachable through the firewall

## Quick Start

### Parse Logs to Find Blocked Domains

```bash
# Auto-discover logs and show all domains
python .claude/skills/awf-debug-tools/scripts/parse-squid-logs.py

# Show only blocked domains
python .claude/skills/awf-debug-tools/scripts/parse-squid-logs.py --blocked-only

# Filter by domain
python .claude/skills/awf-debug-tools/scripts/parse-squid-logs.py --domain github.com

# Show top 10, JSON output
python .claude/skills/awf-debug-tools/scripts/parse-squid-logs.py --top 10 --format json
```

### Run Automated Diagnostics

```bash
# Quick health check
python .claude/skills/awf-debug-tools/scripts/diagnose-awf.py

# Detailed output
python .claude/skills/awf-debug-tools/scripts/diagnose-awf.py --verbose

# JSON output for agent parsing
python .claude/skills/awf-debug-tools/scripts/diagnose-awf.py --format json
```

### Inspect Container Status

```bash
# Inspect all containers
python .claude/skills/awf-debug-tools/scripts/inspect-containers.py

# Specific container only
python .claude/skills/awf-debug-tools/scripts/inspect-containers.py --container awf-squid

# Show only logs
python .claude/skills/awf-debug-tools/scripts/inspect-containers.py --logs-only

# JSON output
python .claude/skills/awf-debug-tools/scripts/inspect-containers.py --format json
```

### Test Domain Reachability

```bash
# Test if domain is allowed
python .claude/skills/awf-debug-tools/scripts/test-domain.py github.com

# Test blocked domain with fix suggestion
python .claude/skills/awf-debug-tools/scripts/test-domain.py npmjs.org --suggest-fix

# Check allowlist only (no log lookup)
python .claude/skills/awf-debug-tools/scripts/test-domain.py api.github.com --check-allowlist

# JSON output
python .claude/skills/awf-debug-tools/scripts/test-domain.py github.com --format json
```

## Common Workflows

### Workflow 1: Debugging Blocked Requests

When a command fails due to blocked domain:

```bash
# 1. Run diagnostics to check overall health
python .claude/skills/awf-debug-tools/scripts/diagnose-awf.py

# 2. Parse logs to find which domains were blocked
python .claude/skills/awf-debug-tools/scripts/parse-squid-logs.py --blocked-only

# 3. Test specific domain and get fix suggestion
python .claude/skills/awf-debug-tools/scripts/test-domain.py npmjs.org --suggest-fix

# 4. Apply the suggested fix
sudo awf --allow-domains github.com,npmjs.org 'your-command'
```

### Workflow 2: Container Health Check

When containers aren't starting or behaving unexpectedly:

```bash
# 1. Check container status and recent logs
python .claude/skills/awf-debug-tools/scripts/inspect-containers.py

# 2. Run full diagnostics
python .claude/skills/awf-debug-tools/scripts/diagnose-awf.py --verbose

# 3. If issues found, check Squid logs for errors
python .claude/skills/awf-debug-tools/scripts/parse-squid-logs.py
```

### Workflow 3: Agent Automated Debugging

For agents to diagnose issues without human intervention:

```bash
# Run all checks with JSON output
python .claude/skills/awf-debug-tools/scripts/diagnose-awf.py --format json | jq .

# Parse blocked domains
python .claude/skills/awf-debug-tools/scripts/parse-squid-logs.py --blocked-only --format json | jq .

# Test each blocked domain
python .claude/skills/awf-debug-tools/scripts/test-domain.py npmjs.org --format json | jq .
```

## Output Formats

All scripts support two output formats:

- **table/text** (default): Human-readable format with clear sections and alignment
- **json**: Machine-readable format optimized for agent parsing

Use `--format json` to get structured output that's easy to parse programmatically.

## Exit Codes

All scripts use consistent exit codes:

- **0**: Success (no issues found, domain allowed, etc.)
- **1**: Issues found (blocked domains, failed checks, domain blocked)
- **2**: Error (missing logs, invalid arguments, etc.)

## No Dependencies

All scripts use Python 3.8+ stdlib only. No `pip install` required. They work out of the box on any system with Python 3.8+.

## Script Reference

### parse-squid-logs.py

**Purpose:** Extract blocked domains from Squid logs with counts and statistics.

**Key Options:**
- `--blocked-only` - Show only blocked domains
- `--domain DOMAIN` - Filter by specific domain
- `--top N` - Show top N domains by request count
- `--format {table,json}` - Output format

**Auto-discovers logs** from running containers, preserved logs, or work directories.

### diagnose-awf.py

**Purpose:** Run automated diagnostic checks and report issues with fixes.

**Checks:**
- Container status (running/stopped/missing)
- Container health (Squid healthcheck)
- Network connectivity (Squid reachable from agent)
- DNS configuration
- Squid config validation
- Common issues (port conflicts, orphaned containers)

**Key Options:**
- `--verbose` - Show detailed check output
- `--format {text,json}` - Output format

### inspect-containers.py

**Purpose:** Show concise container status without verbose docker output.

**Shows:**
- Container status and exit codes
- IP addresses and network info
- Health check status
- Top 5 processes
- Recent logs (last 5 lines)

**Key Options:**
- `--container NAME` - Inspect specific container only
- `--logs-only` - Show only recent logs
- `--tail N` - Number of log lines (default: 5)
- `--format {text,json}` - Output format

### test-domain.py

**Purpose:** Test if domain is reachable through the firewall.

**Checks:**
- If domain is in Squid allowlist
- If domain appears in recent Squid logs
- Whether requests were allowed or blocked

**Key Options:**
- `--check-allowlist` - Only check allowlist, don't check logs
- `--suggest-fix` - Show suggested --allow-domains flag
- `--format {text,json}` - Output format

## Integration with Existing Skills

- For manual debugging commands, see the `debug-firewall` skill
- For MCP Gateway integration, see the `awf-mcp-gateway` skill
- For general troubleshooting, see `docs/troubleshooting.md`

## Performance

All scripts are designed for fast execution:

- `parse-squid-logs.py`: <2 seconds for typical log files
- `diagnose-awf.py`: <3 seconds for all checks
- `inspect-containers.py`: <2 seconds for both containers
- `test-domain.py`: <1 second for domain check

## Examples

### Example 1: Find Blocked Domains

```bash
$ python .claude/skills/awf-debug-tools/scripts/parse-squid-logs.py --blocked-only

Blocked Domains (sorted by count):

  Domain                  Blocked  Allowed  Total
  =================================================
  registry.npmjs.org      45       0        45
  example.com             12       0        12

Total requests: 1234
Blocked: 57 (4.6%)
Allowed: 1177 (95.4%)
```

### Example 2: Diagnose Issues

```bash
$ python .claude/skills/awf-debug-tools/scripts/diagnose-awf.py

AWF Diagnostic Report
========================================
[✓] Containers: awf-squid (running), awf-agent (exited:0)
[✓] Health: Squid healthy
[✓] Network: awf-net exists ([{Subnet:172.30.0.0/24 Gateway:172.30.0.1}])
[✓] Connectivity: Squid reachable on 172.30.0.10:3128
[✓] DNS: DNS servers: 127.0.0.11, 8.8.8.8, 8.8.4.4
[✓] Config: 3 domains in allowlist (github.com, .github.com, api.github.com)

Summary: All checks passed ✓
```

### Example 3: Test Domain

```bash
$ python .claude/skills/awf-debug-tools/scripts/test-domain.py npmjs.org --suggest-fix

Testing: npmjs.org

[✗] Allowlist check: Not in allowlist
[✗] Reachability: Blocked (403 TCP_DENIED:HIER_NONE)
[✗] Status: BLOCKED

Suggested fix:
  awf --allow-domains github.com,npmjs.org 'your-command'
```

## Tips for Agents

1. **Use JSON output** for easy parsing: `--format json | jq .`
2. **Chain commands** to get complete picture: diagnose → parse logs → test domain
3. **Check exit codes** to determine if action needed (0 = ok, 1 = issues)
4. **Use --suggest-fix** to get ready-to-use awf commands
5. **Scripts auto-discover logs** - no need to specify paths in most cases

## Troubleshooting

**Script not found:**
```bash
# Use absolute path
python /home/mossaka/developer/gh-aw-repos/gh-aw-firewall/.claude/skills/awf-debug-tools/scripts/parse-squid-logs.py
```

**Permission denied on logs:**
```bash
# Squid logs require sudo to read
sudo python .claude/skills/awf-debug-tools/scripts/parse-squid-logs.py --log-file /tmp/squid-logs-*/access.log
```

**No logs found:**
```bash
# Run awf first to generate logs
sudo awf --allow-domains github.com 'curl https://api.github.com'

# Then parse
python .claude/skills/awf-debug-tools/scripts/parse-squid-logs.py
```

## Future Enhancements

Planned scripts for future versions:
- `analyze-traffic.py` - Analyze traffic patterns over time
- `generate-allowlist.py` - Auto-generate allowlist from logs
- `cleanup-awf.py` - Clean up orphaned resources
- `benchmark-awf.py` - Performance testing utilities
