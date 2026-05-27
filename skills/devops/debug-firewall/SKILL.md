---
name: debug-firewall
description: Debug the AWF firewall by inspecting Docker containers (awf-squid, awf-agent), analyzing Squid access logs, checking iptables rules, and troubleshooting blocked domains or network issues.
allowed-tools: Bash(docker:*), Bash(sudo:*), Bash(dmesg:*), Bash(ls:*), Bash(cat:*), Read
---

# AWF Firewall Debugging Skill

Use this skill when you need to debug the awf firewall, inspect container state, analyze traffic, or troubleshoot network issues.

## Container Information

**Container Names:**
- `awf-squid` - Squid proxy container (IP: 172.30.0.10)
- `awf-agent` - Agent execution container (IP: 172.30.0.20)

**Network:** `awf-net` (subnet: 172.30.0.0/24)

## Quick Debugging Commands

### Check Container Status
```bash
docker ps | grep awf
docker inspect awf-squid --format='{{.State.Running}}'
docker inspect awf-agent --format='{{.State.ExitCode}}'
```

### View Logs
```bash
# Real-time logs
docker logs -f awf-squid
docker logs -f awf-agent

# Squid access log (traffic decisions)
docker exec awf-squid cat /var/log/squid/access.log
```

### Analyze Traffic

**Squid Decision Codes:**
- `TCP_TUNNEL:HIER_DIRECT` = ALLOWED (HTTPS)
- `TCP_MISS:HIER_DIRECT` = ALLOWED (HTTP)
- `TCP_DENIED:HIER_NONE` = BLOCKED

```bash
# Find blocked domains
docker exec awf-squid grep "TCP_DENIED" /var/log/squid/access.log | awk '{print $3}' | sort -u

# Count blocked by domain
docker exec awf-squid grep "TCP_DENIED" /var/log/squid/access.log | awk '{print $3}' | sort | uniq -c | sort -rn

# All unique domains accessed
docker exec awf-squid awk '{print $3}' /var/log/squid/access.log | sort -u

# Real-time blocked traffic
docker exec awf-squid tail -f /var/log/squid/access.log | grep --line-buffered TCP_DENIED
```

### Inspect iptables Rules
```bash
# Host-level firewall chain
sudo iptables -t filter -L FW_WRAPPER -n -v

# Agent container NAT rules (redirects to Squid)
docker exec awf-agent iptables -t nat -L OUTPUT -n -v

# Kernel logs for blocked non-HTTP traffic
sudo dmesg | grep "FW_BLOCKED"
```

### Network Inspection
```bash
# Network details
docker network inspect awf-net

# Test Squid connectivity
docker exec awf-agent nc -zv 172.30.0.10 3128

# DNS configuration
docker exec awf-agent cat /etc/resolv.conf
```

### View Configuration
```bash
# Squid config
docker exec awf-squid cat /etc/squid/squid.conf

# Docker compose config
cat /tmp/awf-*/docker-compose.yml

# Agent environment
docker exec awf-agent env | grep -E "PROXY|DNS"
```

## Preserved Logs Locations

**With `--keep-containers`:** Logs remain at work directory
- Squid: `/tmp/awf-<timestamp>/squid-logs/access.log`
- Agent: `/tmp/awf-<timestamp>/agent-logs/` (only if Copilot CLI logs exist)

**Normal execution:** Logs moved after cleanup
- Squid: `/tmp/squid-logs-<timestamp>/access.log`
- Agent: `/tmp/awf-agent-logs-<timestamp>/`

```bash
# Find work directories and preserved logs
ls -ldt /tmp/awf-* /tmp/squid-logs-* 2>/dev/null | head -5

# View Squid logs from work dir (with --keep-containers)
sudo cat /tmp/awf-*/squid-logs/access.log

# View preserved Squid logs (after normal cleanup)
sudo cat $(ls -t /tmp/squid-logs-*/access.log 2>/dev/null | head -1)
```

## Debug Mode Workflow

```bash
# 1. Run with debug logging and keep containers
sudo awf \
  --allow-domains github.com \
  --log-level debug \
  --keep-containers \
  'curl https://api.github.com'

# 2. Inspect containers (they remain running)
docker ps | grep awf
docker logs awf-squid
docker exec awf-squid grep "TCP_DENIED" /var/log/squid/access.log

# 3. Check iptables
sudo iptables -t filter -L FW_WRAPPER -n

# 4. Manual cleanup when done
docker rm -f awf-squid awf-agent
docker network rm awf-net
```

## Common Issues

**Domain blocked unexpectedly:**
```bash
# Check exact domain being requested
docker exec awf-squid tail -20 /var/log/squid/access.log
# Look at the Host header (3rd column) - may need subdomain allowlisted
```

**DNS resolution failing:**
```bash
# Check DNS servers in use
docker exec awf-agent cat /etc/resolv.conf
# Verify DNS allowed in iptables
sudo dmesg | grep "FW_DNS"
```

## Cleanup

```bash
# Manual cleanup
./scripts/ci/cleanup.sh

# Or individually:
docker rm -f awf-squid awf-agent
docker network rm awf-net
sudo iptables -t filter -F FW_WRAPPER 2>/dev/null
sudo iptables -t filter -X FW_WRAPPER 2>/dev/null
rm -rf /tmp/awf-*
```
