---
name: environment-troubleshooting
description: Use when the DevOp is diagnosing OS issues, network problems, permission errors, disk space, memory constraints, DNS resolution, port conflicts, or service crashes. Activates when debugging infrastructure, environment, or system-level problems.
version: 1.0.0
---

# Environment Troubleshooting Expertise

## When This Applies

Apply this guidance when:
- Diagnosing system or infrastructure issues
- Resolving permission, network, or resource problems
- Debugging service crashes or connectivity failures
- Analyzing logs for infrastructure issues

## Diagnostic Process

### Step 1: Gather Information

```bash
# System overview
uname -a               # OS and kernel
df -h                  # Disk space
free -h                # Memory usage
top -bn1 | head -20    # CPU and process overview

# Network
ip addr                # Network interfaces
ss -tlnp               # Listening ports
curl -v <url>          # Test connectivity
dig <hostname>         # DNS resolution

# Services
systemctl status <service>  # Service status
journalctl -u <service> -n 50  # Recent logs
docker ps -a           # Container status
```

### Step 2: Identify the Category

| Symptom | Category | Common Causes |
|---------|----------|---------------|
| Service won't start | **Process** | Port conflict, missing config, permission |
| Connection refused | **Network** | Firewall, wrong port, service not running |
| Permission denied | **Access** | File permissions, user/group, SELinux |
| Out of memory | **Resource** | Memory leak, insufficient allocation |
| Disk full | **Resource** | Logs, temp files, unrotated data |
| Slow response | **Performance** | CPU saturation, disk I/O, network latency |
| DNS failure | **Network** | DNS config, resolv.conf, network partition |

### Step 3: Resolve

Apply the fix, then verify the original issue is resolved.

## Common Issues and Solutions

### Port Conflicts
```bash
# Find what's using a port
ss -tlnp | grep :3000
# or
lsof -i :3000
```
Solution: Stop the conflicting process or change the port.

### Permission Errors
```bash
# Check file ownership and permissions
ls -la /path/to/file
# Check the running user
whoami
id
```
Solution: `chmod` / `chown` to grant appropriate access. Never use `777`.

### Disk Space
```bash
# Find largest directories
du -sh /* 2>/dev/null | sort -rh | head -10
# Find large files
find / -type f -size +100M 2>/dev/null
```
Solution: Clean logs, remove unused images/containers, rotate old data.

### Container Issues
```bash
# Check container logs
docker logs <container> --tail 100
# Check container resource usage
docker stats --no-stream
# Inspect container
docker inspect <container>
```

### Memory Issues
```bash
# Check per-process memory
ps aux --sort=-%mem | head -10
# Check for OOM kills
dmesg | grep -i "out of memory"
```

## Log Analysis

### Where to Look

| Service Type | Log Location |
|-------------|-------------|
| System | `/var/log/syslog` or `journalctl` |
| Application | Application-specific log dir or stdout |
| Docker | `docker logs <container>` |
| Web server | `/var/log/nginx/` or `/var/log/apache2/` |
| Database | DB-specific log directory |

### What to Look For

1. **Timestamps** — When did the problem start?
2. **Error patterns** — Are errors repeating? Increasing frequency?
3. **Stack traces** — What component is failing?
4. **Resource numbers** — Memory usage, connection counts, disk I/O

## Escalation

When the issue is outside your scope:
- **Code bug causing crashes** → Send to Developer via queue
- **Architecture causing scaling issues** → Send to Architect
- **Needs code commit to fix** → Send to Integrator after implementing fix
- **Production incident** → Send to Production Engineer
