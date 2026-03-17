---
name: awf-skill
description: Use the AWF (Agentic Workflow Firewall) to run commands with network isolation and domain whitelisting. Provides L7 HTTP/HTTPS egress control for AI agents.
allowed-tools: Bash(sudo:*), Bash(awf:*), Bash(docker:*), Read
user-invocable: false
---

# AWF (Agentic Workflow Firewall) Usage Skill

Use this skill when you need to run commands with network isolation, restrict network access to approved domains, or execute AI agents in a sandboxed environment with controlled network access.

## What is AWF?

AWF is a network firewall for agentic workflows that provides:

- **L7 Domain Whitelisting**: Control HTTP/HTTPS traffic at the application layer
- **Host-Level Enforcement**: Uses iptables DOCKER-USER chain to enforce firewall on ALL containers
- **Chroot Mode**: Optional transparent access to host binaries (Python, Node.js, Go) while maintaining network isolation

## When to Use AWF

Use AWF when:
- Running AI agents (Copilot CLI, Claude, etc.) that need network access but should be restricted
- Testing code that makes network requests in a controlled environment
- Enforcing network security policies for automated workflows
- Running untrusted commands with limited network access
- Testing Playwright or other tools against localhost services

## Quick Start

### Basic Command

```bash
# Run a command with only github.com allowed
sudo awf --allow-domains github.com -- curl https://api.github.com
```

The `--` separator divides firewall options from the command to run.

### Test Domain Blocking

```bash
# This should FAIL (example.com not allowed)
sudo awf --allow-domains github.com -- curl -f --max-time 10 https://example.com
```

### Enable Debug Logging

```bash
sudo awf --allow-domains github.com --log-level debug -- curl https://api.github.com
```

## Installation

### Install Script (Recommended)

```bash
curl -sSL https://raw.githubusercontent.com/github/gh-aw-firewall/main/install.sh | sudo bash
sudo awf --version
```

### Build from Source

```bash
git clone https://github.com/github/gh-aw-firewall.git awf
cd awf
npm install
npm run build
npm link
```

## CLI Options Reference

```
sudo awf [options] -- <command>

Domain Options:
  --allow-domains <domains>       Comma-separated allowed domains
  --allow-domains-file <path>     File with allowed domains (one per line)
  --block-domains <domains>       Comma-separated blocked domains (takes precedence)
  --block-domains-file <path>     File with blocked domains

Network Options:
  --dns-servers <servers>         DNS servers (default: 8.8.8.8,8.8.4.4)
  --enable-host-access            Enable access to host via host.docker.internal
  --allow-host-ports <ports>      Ports to allow with host access (e.g., 3000,8080)

Container Options:
  --tty                           Allocate TTY for interactive tools
  --env KEY=VALUE                 Pass environment variable (repeatable)
  --env-all                       Pass all host environment variables
  --mount <host:container[:mode]> Volume mount (repeatable)
  --container-workdir <dir>       Working directory inside container
  --agent-image <value>           Agent image preset (default, act) or custom

Advanced Options:
  --ssl-bump                      Enable HTTPS content inspection
  --allow-urls <urls>             URL patterns for SSL Bump (requires --ssl-bump)

Debugging Options:
  --log-level <level>             Log level: debug, info, warn, error
  --keep-containers               Keep containers after command exits
  --proxy-logs-dir <path>         Directory to save Squid logs to
```

## Domain Whitelisting Patterns

### Subdomain Matching (Automatic)

```bash
# github.com also allows api.github.com, raw.github.com, etc.
sudo awf --allow-domains github.com -- curl https://api.github.com
```

### Wildcard Patterns

```bash
# Match any subdomain
--allow-domains '*.github.com'

# Match prefix patterns
--allow-domains 'api-*.example.com'

# Combine multiple patterns
--allow-domains 'github.com,*.googleapis.com,api-*.example.com'
```

### Protocol-Specific

```bash
# HTTPS only
--allow-domains 'https://secure.example.com'

# HTTP only
--allow-domains 'http://legacy.example.com'
```

### Domain Blocklist

```bash
# Allow domain but block specific subdomain
sudo awf \
  --allow-domains example.com \
  --block-domains internal.example.com \
  -- curl https://api.example.com  # Works
```

## Common Workflows

### 1. Run GitHub Copilot CLI

```bash
sudo awf \
  --allow-domains github.com,api.github.com,githubusercontent.com,anthropic.com \
  -- copilot --prompt "List my repositories"
```

### 2. Run with MCP Servers

```bash
sudo awf \
  --allow-domains github.com,arxiv.org,mcp.tavily.com \
  --log-level debug \
  -- copilot --mcp arxiv,tavily --prompt "Search arxiv for recent AI papers"
```

### 3. Playwright Testing with Localhost

```bash
# The localhost keyword auto-configures host access and dev ports
sudo awf \
  --allow-domains localhost,playwright.dev \
  -- npx playwright test
```

### 4. Pass Environment Variables

```bash
# Pass specific variables
sudo awf --allow-domains github.com \
  -e GITHUB_TOKEN="$GITHUB_TOKEN" \
  -e NODE_ENV=production \
  -- npm test

# Pass all host environment variables
sudo awf --allow-domains github.com --env-all -- npm test
```

### 5. Mount Custom Volumes

```bash
sudo awf --allow-domains github.com \
  -v /path/to/data:/data:ro \
  -- cat /data/config.json
```

### 6. Use Host Binaries (Chroot Mode is Always On)

```bash
# Access host Python, Node, Go, etc. (chroot mode is the default)
sudo awf --allow-domains api.github.com \
  -- python3 -c "import requests; print(requests.get('https://api.github.com').status_code)"
```

### 7. SSL Bump for URL Path Filtering

```bash
sudo awf \
  --allow-domains github.com \
  --ssl-bump \
  --allow-urls "https://github.com/myorg/*" \
  -- curl https://github.com/myorg/some-repo
```

### 8. GitHub Actions Integration

```yaml
- name: Setup awf
  uses: github/gh-aw-firewall@main

- name: Run with firewall
  run: |
    sudo -E awf --allow-domains github.com -- 'cd $GITHUB_WORKSPACE && npm test'
```

## Log Analysis Commands

### View Logs

```bash
# Pretty format (default)
awf logs

# Follow in real-time
awf logs -f

# JSON format for scripting
awf logs --format json

# List available log sources
awf logs --list
```

### Get Statistics

```bash
# Terminal output
awf logs stats

# JSON for scripting
awf logs stats --format json

# Markdown for GitHub Actions
awf logs summary >> $GITHUB_STEP_SUMMARY
```

### Find Blocked Requests

```bash
# Using awf logs
awf logs --format json | jq 'select(.isAllowed == false)'

# Direct Squid log query
sudo grep "TCP_DENIED" /tmp/squid-logs-*/access.log
```

## Debugging Tips

### Keep Containers for Inspection

```bash
sudo awf --allow-domains github.com --keep-containers -- failing-command

# Inspect containers
docker logs awf-squid
docker logs awf-agent

# View Squid config
docker exec awf-squid cat /etc/squid/squid.conf

# Manual cleanup when done
docker rm -f awf-squid awf-agent
```

### Check Which Domains Were Blocked

```bash
# After command completes
sudo cat /tmp/squid-logs-*/access.log | grep TCP_DENIED

# Or use the logs command
awf logs --format json | jq 'select(.isAllowed == false) | .domain'
```

### Debug Container Network

```bash
# Check iptables rules
docker exec awf-agent iptables -t nat -L OUTPUT -n -v

# Check DNS
docker exec awf-agent cat /etc/resolv.conf

# Test connectivity to Squid
docker exec awf-agent nc -zv 172.30.0.10 3128
```

## Squid Decision Codes

When analyzing logs, these codes indicate the traffic decision:

| Code | Meaning |
|------|---------|
| `TCP_TUNNEL:HIER_DIRECT` | ALLOWED (HTTPS tunnel) |
| `TCP_MISS:HIER_DIRECT` | ALLOWED (HTTP request) |
| `TCP_DENIED:HIER_NONE` | BLOCKED (domain not in allowlist) |

## Agent Image Options

### Presets (Pre-built, Fast)

```bash
# Default - minimal ubuntu:22.04 (~200MB)
sudo awf --agent-image default --allow-domains github.com -- command

# Act - GitHub Actions parity (~2GB)
sudo awf --agent-image act --allow-domains github.com -- command
```

### Custom Base Images (Requires --build-local)

```bash
sudo awf \
  --build-local \
  --agent-image ghcr.io/catthehacker/ubuntu:runner-22.04 \
  --allow-domains github.com \
  -- command
```

## Common Issues and Fixes

### "Cannot connect to Docker daemon"

```bash
sudo systemctl start docker
```

### "Port 3128 already in use"

```bash
docker stop $(docker ps -q --filter "expose=3128")
```

### Domain Not Working

1. Check if subdomain is needed: `api.example.com` vs `example.com`
2. Enable debug logging: `--log-level debug`
3. Check Squid logs: `awf logs --format json`

### Command Fails with Exit Code 28 (Timeout)

The domain is being blocked. Check:
1. Is domain in `--allow-domains`?
2. Is subdomain required?
3. View blocked domains: `awf logs --format json | jq 'select(.isAllowed == false)'`

## Limitations

- **No IPv6**: Only IPv4 traffic is supported
- **No HTTP/3**: Container curl doesn't support HTTP/3
- **No internationalized domains**: Use punycode (e.g., `xn--bcher-kva.ch`)
- **HTTP to HTTPS redirects**: May fail; use HTTPS directly
- **IP-based access**: Direct IP access is blocked (no domain)

## Best Practices

1. **Start with minimal domains**: Only add what's needed
2. **Use wildcards carefully**: `*.example.com` is safer than `*`
3. **Enable debug logging**: When troubleshooting add `--log-level debug`
4. **Review logs**: Check what was blocked with `awf logs stats`
5. **Use blocklists**: For fine-grained control when allowing broad domains
6. **Quote shell commands**: Use `'command $VAR'` to preserve container expansion

## Installing This Skill

To install this skill for Claude Code agents in your project:

```bash
# Download the skill
mkdir -p .claude/skills/awf-skill
curl -sSL https://raw.githubusercontent.com/github/gh-aw-firewall/main/skill.md \
  -o .claude/skills/awf-skill/SKILL.md
```

## Related Skills

- `debug-firewall` - Manual Docker debugging commands for AWF
- `awf-debug-tools` - Python scripts for log parsing and diagnostics
