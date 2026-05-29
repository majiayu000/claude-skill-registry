---
name: adguard-home
description: Manage, troubleshoot, configure, analyze, and review AdGuard Home DNS server. Use when working with AdGuard Home, DNS blocking, ad blocking, network-wide filtering, DNS queries, blocklists, client management, DHCP, or DNS rewrites. Supports REST API and SSH access. Triggers on adguard, DNS blocking, ad blocking, network filtering, DNS server, blocklist, pi-hole alternative.
---

# AdGuard Home Management

Comprehensive management capabilities for AdGuard Home DNS server.

## Prerequisites

### Environment Variables

```bash
ADGUARD_URL=https://your-adguard-domain.local
ADGUARD_USER=admin
ADGUARD_PASS=your-password
ADGUARD_SSH_HOST=192.168.x.x
ADGUARD_SSH_USER=your-ssh-user
```

### Python Packages

```bash
pip install requests paramiko
```

## Quick Reference

### API Authentication

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

```bash
curl -u "$ADGUARD_USER:$ADGUARD_PASS" "$ADGUARD_URL/control/status"
```

### 2. Query Log Analysis

```python
python scripts/adguard_api.py querylog --limit 100 --search "blocked"
```

Filter by response status: `all`, `filtered`, `blocked`, `blocked_safebrowsing`, `blocked_parental`, `whitelisted`, `rewritten`, `processed`

### 3. Filter Management

**View current filters:**
```python
python scripts/adguard_api.py filters
```

**Add a blocklist:**
```python
python scripts/adguard_api.py add-filter --name "My List" --url "https://example.com/blocklist.txt"
```

**Custom filtering rules:**
```bash
# Block domain
||ads.example.com^

# Allow domain (whitelist)
@@||allowed.example.com^

# Block with regex
/ads[0-9]+\.example\.com/
```

### 4. Client Management

```python
# List all clients
python scripts/adguard_api.py clients

# Add/configure client
python scripts/adguard_api.py add-client --name "Living Room TV" --ids "192.168.1.50"
```

### 5. DNS Rewrites

```python
# List rewrites
python scripts/adguard_api.py rewrites

# Add rewrite
python scripts/adguard_api.py add-rewrite --domain "myserver.local" --answer "192.168.1.100"
```

### 6. Statistics

```python
python scripts/adguard_api.py stats
python scripts/adguard_api.py reset-stats
```

## SSH Server Management

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

## Troubleshooting

### DNS Resolution Failures

1. Check AdGuard Home service status
2. Verify upstream DNS servers
3. Check network connectivity
4. Review query log for errors

### Clients Not Using AdGuard Home

1. Verify client DHCP settings
2. Check if client has hardcoded DNS
3. Review router DNS configuration
4. Check firewall rules

### High Latency

1. Check upstream DNS performance
2. Review blocklist count
3. Enable DNS caching
4. Consider local upstream resolver

## Best Practices

1. **Use encrypted DNS** - DoH/DoT for upstream
2. **Regular blocklist updates** - Keep filters current
3. **Monitor query patterns** - Watch for anomalies
4. **Backup configuration** - Before major changes
5. **Enable safebrowsing** - Additional protection
6. **Configure rate limiting** - Prevent abuse
7. **Use client groups** - Different policies per device
8. **Regular log review** - Security monitoring

## When to Use This Skill

- Managing AdGuard Home installation
- Troubleshooting DNS issues
- Configuring blocklists and filters
- Setting up client-specific rules
- Analyzing DNS queries
- Managing DNS rewrites
- Performing security audits
