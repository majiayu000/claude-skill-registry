---
name: system-admin
description: Linux system administration and monitoring
version: 1.0.0
author: terminal-skills
tags: [linux, system, monitoring, admin]
---

# Linux System Administration

## Overview
Core commands and best practices for Linux system administration, including system information viewing, resource monitoring, service management, etc.

## System Information

### Basic Information
```bash
# System version
cat /etc/os-release
uname -a

# Hostname
hostnamectl

# Uptime and load
uptime
```

### Hardware Information
```bash
# CPU information
lscpu
cat /proc/cpuinfo

# Memory information
free -h
cat /proc/meminfo

# Disk information
lsblk
df -h
```

## Resource Monitoring

### Real-time Monitoring
```bash
# Comprehensive monitoring
top
htop

# Memory monitoring
vmstat 1

# IO monitoring
iostat -x 1
iotop

# Network monitoring
iftop
nethogs
```

### Historical Data
```bash
# System activity report
sar -u 1 10    # CPU
sar -r 1 10    # Memory
sar -d 1 10    # Disk
```

## Service Management

### Systemd Services
```bash
# Service status
systemctl status service-name
systemctl is-active service-name

# Start/Stop services
systemctl start/stop/restart service-name

# Boot startup
systemctl enable/disable service-name

# View all services
systemctl list-units --type=service
```

## Common Scenarios

### Scenario 1: System Health Check
```bash
# Quick health check script
echo "=== System Load ===" && uptime
echo "=== Memory Usage ===" && free -h
echo "=== Disk Usage ===" && df -h
echo "=== Failed Services ===" && systemctl --failed
```

### Scenario 2: Troubleshoot High Load
```bash
# 1. Check load
uptime

# 2. Find high CPU processes
ps aux --sort=-%cpu | head -10

# 3. Find high memory processes
ps aux --sort=-%mem | head -10
```

## Troubleshooting

| Problem | Commands |
|---------|----------|
| System lag | `top`, `vmstat 1`, `iostat -x 1` |
| Disk full | `df -h`, `du -sh /*`, `ncdu` |
| Memory shortage | `free -h`, `ps aux --sort=-%mem` |
| Service abnormal | `systemctl status`, `journalctl -u` |
