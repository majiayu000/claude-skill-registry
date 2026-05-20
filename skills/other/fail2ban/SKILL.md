---
name: fail2ban
description: >-
  Protect servers from brute force attacks with Fail2Ban. Use when a user asks
  to block repeated failed login attempts, protect SSH, secure web servers from
  brute force, or ban malicious IPs automatically.
license: Apache-2.0
compatibility: 'Linux'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: devops
  tags:
    - fail2ban
    - brute-force
    - ssh
    - security
    - firewall
---

# Fail2Ban

## Overview

Fail2Ban monitors log files for failed authentication attempts and bans offending IPs using iptables/nftables. Protects SSH, Nginx, Apache, Postfix, and any service with log-based authentication.

## Instructions

### Step 1: Install

```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
```

### Step 2: Configure

```ini
# /etc/fail2ban/jail.local — Custom configuration (never edit jail.conf)
[DEFAULT]
bantime = 1h
findtime = 10m
maxretry = 5
banaction = iptables-multiport

[sshd]
enabled = true
port = ssh
maxretry = 3
bantime = 24h

[nginx-http-auth]
enabled = true
port = http,https
maxretry = 5

[nginx-botsearch]
enabled = true
port = http,https
maxretry = 2
bantime = 7d
```

### Step 3: Monitor

```bash
sudo fail2ban-client status               # list active jails
sudo fail2ban-client status sshd           # show banned IPs
sudo fail2ban-client set sshd unbanip 1.2.3.4   # unban
sudo fail2ban-client set sshd banip 5.6.7.8     # manual ban
```

## Guidelines

- Always create jail.local — jail.conf gets overwritten on updates.
- Start conservative: 5 retries, 1h ban. Adjust based on logs.
- For modern alternative with community threat sharing, consider CrowdSec.
- Use `fail2ban-regex` to test custom filters before deploying.
