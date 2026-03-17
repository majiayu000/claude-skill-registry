---
name: adguard-home
description: Manage, troubleshoot, configure, analyze, and review AdGuard Home DNS server. Use when working with AdGuard Home, DNS blocking, ad blocking, network-wide filtering, DNS queries, blocklists, client management, DHCP, or DNS rewrites. Supports REST API and SSH access.
---

# AdGuard Home Management

This skill provides comprehensive management capabilities for AdGuard Home DNS server running on Ubuntu Server.

## Prerequisites

Before using this skill, ensure you have:

1. **Environment variables configured** (in `.env` or shell):
   ```bash
   ADGUARD_URL=https://your-adguard-domain.local
   ADGUARD_USER=admin
   ADGUARD_PASS=your-password
   ADGUARD_SSH_HOST=192.168.x.x
   ADGUARD_SSH_USER=your-ssh-user
   ```

2. **Python packages installed**:
   ```bash
   pip install requests paramiko
   ```

3. **SSH key authentication** (recommended) or password access to Ubuntu server

## Quick Reference

### API Authentication
All API calls use HTTP Basic Auth:
```bash
curl -u "$ADGUARD_USER:$ADGUARD_PASS" "$ADGUARD_URL/control/status"
```

### Common Tasks

| Task | API Endpoint | Method |
|------|--------------|--------|
| Get status | `/control/status` | GET |
| Get DNS info | `/control/dns_info` | GET |
| Query log | `/control/querylog` | GET |
| Get stats | `/control/stats` | GET |
| List clients | `/control/clients` | GET |
| Filter status | `/control/filtering/status` | GET |
| Clear cache | `/control/cache_clear` | POST |

## Core Management Tasks

### 1. Status & Health Check

Check AdGuard Home status:
```python
python scripts/adguard_api.py status
```

Or via curl:
```bash
curl -u "$ADGUARD_USER:$ADGUARD_PASS" "$ADGUARD_URL/control/status"
```

### 2. Query Log Analysis

Analyze DNS queries to troubleshoot issues:
```python
python scripts/adguard_api.py querylog --limit 100 --search "blocked"
```

Filter by response status: `all`, `filtered`, `blocked`, `blocked_safebrowsing`, `blocked_parental`, `whitelisted`, `rewritten`, `safe_search`, `processed`

### 3. Filter Management

**View current filters:**
```python
python scripts/adguard_api.py filters
```

**Add a blocklist:**
```python
python scripts/adguard_api.py add-filter --name "My List" --url "https://example.com/blocklist.txt"
```

**Add custom filtering rule:**
```bash
# Block domain
||ads.example.com^

# Allow domain (whitelist)
@@||allowed.example.com^

# Block with regex
/ads[0-9]+\.example\.com/
```

### 4. Client Management

**List all clients:**
```python
python scripts/adguard_api.py clients
```

**Add/configure client:**
```python
python scripts/adguard_api.py add-client --name "Living Room TV" --ids "192.168.1.50"
```

### 5. DNS Rewrites

**List rewrites:**
```python
python scripts/adguard_api.py rewrites
```

**Add rewrite:**
```python
python scripts/adguard_api.py add-rewrite --domain "myserver.local" --answer "192.168.1.100"
```

### 6. Statistics & Analytics

**Get statistics:**
```python
python scripts/adguard_api.py stats
```

**Reset statistics:**
```python
python scripts/adguard_api.py reset-stats
```

## SSH Server Management

For tasks requiring direct server access:

### Service Management
```bash
# Check service status
ssh $ADGUARD_SSH_USER@$ADGUARD_SSH_HOST "systemctl status AdGuardHome"

# Restart service
ssh $ADGUARD_SSH_USER@$ADGUARD_SSH_HOST "sudo systemctl restart AdGuardHome"

# View logs
ssh $ADGUARD_SSH_USER@$ADGUARD_SSH_HOST "sudo journalctl -u AdGuardHome -n 100"
```

### Configuration File
Location: `/opt/AdGuardHome/AdGuardHome.yaml`

```bash
# Backup config
ssh $ADGUARD_SSH_USER@$ADGUARD_SSH_HOST "sudo cp /opt/AdGuardHome/AdGuardHome.yaml /opt/AdGuardHome/AdGuardHome.yaml.bak"

# View config
ssh $ADGUARD_SSH_USER@$ADGUARD_SSH_HOST "sudo cat /opt/AdGuardHome/AdGuardHome.yaml"
```

### Update AdGuard Home
```bash
ssh $ADGUARD_SSH_USER@$ADGUARD_SSH_HOST "cd /opt/AdGuardHome && sudo ./AdGuardHome -s stop && sudo ./AdGuardHome --update && sudo ./AdGuardHome -s start"
```

## Troubleshooting Guide

See [troubleshooting.md](troubleshooting.md) for common issues and solutions including:
- DNS resolution failures
- Clients not using AdGuard Home
- High latency issues
- Blocklist update failures
- Service startup problems

## Best Practices

See [best-practices.md](best-practices.md) for configuration recommendations including:
- Recommended upstream DNS servers
- Optimal blocklist selection
- Security hardening
- Performance tuning
- Backup strategies

## API Reference

See [reference.md](reference.md) for complete API endpoint documentation.

## Example Workflows

### Investigate Blocked Request
1. Check query log for the blocked domain
2. Identify which filter blocked it
3. Add whitelist rule if false positive
4. Clear DNS cache
5. Test resolution

### Add New Device with Custom Settings
1. Identify device IP/MAC
2. Create client configuration
3. Set custom upstream DNS if needed
4. Configure blocked services
5. Set parental controls if applicable

### Security Audit
1. Review client list for unknown devices
2. Check query log for suspicious domains
3. Verify safebrowsing is enabled
4. Review TLS configuration
5. Check for software updates
