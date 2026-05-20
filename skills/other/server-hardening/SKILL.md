---
name: server-hardening
description: Comprehensive server security hardening workflows based on CIS Benchmarks. Use when securing new servers, improving security posture, or implementing security controls on Linux systems.
---

# Server Hardening Skill

This skill provides comprehensive workflows, checklists, and automated scripts for hardening Linux servers according to industry best practices and CIS Benchmarks.

## When to Use This Skill

Use this skill when:
- Setting up new production servers
- Improving security posture of existing servers
- Implementing CIS Benchmark compliance
- Preparing for security audits
- Responding to security incidents
- Establishing security baselines
- Configuring security monitoring

## Core Principles

### 1. Defense in Depth

**Multiple layers of security:**
- Network security (firewall, IDS/IPS)
- Host security (hardening, patching)
- Application security (WAF, input validation)
- Access control (authentication, authorization)
- Monitoring (logging, alerting)

### 2. Principle of Least Privilege

**Always apply:**
- Minimal user permissions
- Minimal service permissions
- Minimal network access
- Minimal file system access

### 3. Zero Trust

**Assume breach:**
- Never trust, always verify
- Verify every request
- Log every action
- Monitor continuously

## Hardening Workflow

### Phase 1: Pre-Hardening Assessment

```
┌─────────────────────────────────────────────────────────────┐
│ Pre-Hardening Checklist                                     │
├─────────────────────────────────────────────────────────────┤
│ □ Document current configuration                            │
│ □ Create full system backup                                 │
│ □ Document running services                                 │
│ □ Document network connections                              │
│ □ Document user accounts                                    │
│ □ Identify compliance requirements                          │
│ □ Schedule maintenance window                               │
│ □ Prepare rollback plan                                     │
└─────────────────────────────────────────────────────────────┘
```

### Phase 2: Security Baseline

**Establish baseline before hardening:**

```bash
#!/bin/bash
# Security baseline assessment

# System information
echo "=== System Information ==="
uname -a
hostnamectl
cat /etc/os-release

# Running services
echo -e "\n=== Running Services ==="
systemctl list-units --type=service --state=running

# Open ports
echo -e "\n=== Open Ports ==="
ss -tulpn

# User accounts
echo -e "\n=== User Accounts ==="
cat /etc/passwd | grep -v nologin

# Sudo users
echo -e "\n=== Sudo Users ==="
getent group sudo

# Installed packages
echo -e "\n=== Security Packages ==="
dpkg -l | grep -E "(fail2ban|ufw|rkhunter|chkrootkit)" || echo "Not installed"

# Last logins
echo -e "\n=== Last Logins ==="
last -10

# Failed logins
echo -e "\n=== Failed Logins ==="
grep "Failed password" /var/log/auth.log | tail -10 || echo "No failed logins"

# Disk usage
echo -e "\n=== Disk Usage ==="
df -h

# Pending updates
echo -e "\n=== Pending Updates ==="
apt list --upgradable 2>/dev/null | head -20 || yum check-update
```

### Phase 3: Hardening Implementation

**Follow the hardening checklist:**

```
┌─────────────────────────────────────────────────────────────┐
│ Server Hardening Checklist                                  │
├─────────────────────────────────────────────────────────────┤
│ SYSTEM UPDATES                                              │
│ □ Update all packages to latest versions                    │
│ □ Configure automatic security updates                      │
│ □ Remove unnecessary packages                               │
├─────────────────────────────────────────────────────────────┤
│ USER MANAGEMENT                                             │
│ □ Remove/disable unused accounts                            │
│ □ Enforce strong password policy                            │
│ □ Configure sudo access                                     │
│ □ Disable root login                                        │
├─────────────────────────────────────────────────────────────┤
│ SSH HARDENING                                               │
│ □ Change default SSH port                                   │
│ □ Disable root login                                        │
│ □ Disable password authentication                           │
│ □ Configure key-based authentication                        │
│ □ Limit users/groups                                        │
│ □ Configure idle timeout                                    │
├─────────────────────────────────────────────────────────────┤
│ FIREWALL CONFIGURATION                                      │
│ □ Enable UFW/firewalld                                      │
│ □ Default deny incoming                                     │
│ □ Allow only required ports                                 │
│ □ Configure rate limiting                                   │
├─────────────────────────────────────────────────────────────┤
│ FILE SYSTEM SECURITY                                        │
│ □ Set proper permissions on sensitive files                 │
│ □ Mount /tmp, /var/tmp with noexec                          │
│ □ Enable audit logging                                      │
│ □ Configure log rotation                                    │
├─────────────────────────────────────────────────────────────┤
│ NETWORK SECURITY                                            │
│ □ Disable IPv6 if not used                                  │
│ □ Disable IP forwarding                                     │
│ □ Configure kernel security parameters                      │
│ □ Enable SYN flood protection                               │
├─────────────────────────────────────────────────────────────┤
│ MONITORING & LOGGING                                        │
│ □ Install and configure Fail2ban                            │
│ □ Configure centralized logging                             │
│ □ Enable audit daemon                                       │
│ □ Configure log aggregation                                 │
├─────────────────────────────────────────────────────────────┤
│ SECURITY TOOLS                                              │
□ Install intrusion detection (rkhunter, chkrootkit)          │
□ Install vulnerability scanner (lynis)                       │
□ Configure malware scanning                                  │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Scripts

### Automated Hardening Script

See `resources/security-checklist.md` for the complete automated hardening script.

### Manual Hardening Steps

**Step 1: System Updates**

```bash
# Update system
apt-get update && apt-get upgrade -y
apt-get dist-upgrade -y

# Remove unused packages
apt-get autoremove -y
apt-get autoclean

# Install security tools
apt-get install -y fail2ban rkhunter chkrootkit lynis unattended-upgrades
```

**Step 2: User Management**

```bash
# Create admin user
adduser admin
usermod -aG sudo admin

# Set password policy
cat >> /etc/pam.d/common-password << EOF
password requisite pam_pwquality.so retry=3 minlen=14 dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1
EOF

# Lock unused accounts
usermod -L games
usermod -L lists
usermod -L news
```

**Step 3: SSH Hardening**

```bash
# Backup SSH config
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

# Configure SSH
cat > /etc/ssh/sshd_config << 'EOF'
Port 2222
Protocol 2
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
X11Forwarding no
ClientAliveInterval 300
ClientAliveCountMax 2
EOF

# Restart SSH
systemctl restart sshd
```

**Step 4: Firewall Configuration**

```bash
# Configure UFW
ufw --force reset
ufw default deny incoming
ufw default allow outgoing

# Allow SSH (custom port)
ufw allow 2222/tcp comment 'SSH'

# Allow HTTP/HTTPS
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'

# Enable UFW
ufw --force enable
```

### Phase 4: Validation

**Verify hardening was successful:**

```bash
#!/bin/bash
# Post-hardening validation

echo "=== SSH Configuration ==="
sshd -T | grep -E "^(port|permitrootlogin|passwordauthentication)"

echo -e "\n=== Firewall Status ==="
ufw status verbose

echo -e "\n=== Running Services ==="
systemctl list-units --type=service --state=running | wc -l
echo "services running"

echo -e "\n=== Open Ports ==="
ss -tulpn | grep LISTEN

echo -e "\n=== Security Tools Status ==="
systemctl status fail2ban --no-pager
systemctl status auditd --no-pager

echo -e "\n=== Lynis Security Audit ==="
lynis audit system 2>&1 | grep -E "(Warnings|Suggestions)" | head -20
```

### Phase 5: Ongoing Maintenance

**Regular security maintenance:**

```yaml
# Daily Tasks
- Review security logs
- Check failed login attempts
- Verify backup completion

# Weekly Tasks
- Review system updates
- Check intrusion detection alerts
- Audit user accounts

# Monthly Tasks
- Run vulnerability scan (lynis)
- Review firewall rules
- Update security baseline
- Test backup restoration

# Quarterly Tasks
- Full security audit
- Review and rotate credentials
- Update hardening scripts
- Compliance review
```

## CIS Benchmark Compliance

### Key CIS Controls

**1. Account Policies:**

```bash
# Password expiration
chage -M 90 -m 7 -W 14 username

# Lock inactive accounts
usermod -L -e 1 username
```

**2. Audit Configuration:**

```bash
# Enable auditd
systemctl enable auditd
systemctl start auditd

# Configure audit rules
cat >> /etc/audit/rules.d/hardening.rules << 'EOF'
# Monitor user/group changes
-w /etc/passwd -p wa -k identity
-w /etc/group -p wa -k identity
-w /etc/shadow -p wa -k identity

# Monitor sudo
-w /etc/sudoers -p wa -k sudoers

# Monitor SSH
-w /etc/ssh/sshd_config -p wa -k sshd

# Monitor authentication
-w /var/log/auth.log -p wa -k auth_log
EOF
```

**3. File Permissions:**

```bash
# Secure sensitive files
chmod 644 /etc/passwd
chmod 640 /etc/shadow
chmod 640 /etc/group
chmod 600 /etc/ssh/sshd_config

# Find world-writable files
find / -type f -perm -002 2>/dev/null

# Find SUID binaries
find / -type f -perm -4000 2>/dev/null
```

## Security Monitoring

### Log Monitoring

```bash
#!/bin/bash
# Security log monitoring script

LOG_FILE="/var/log/auth.log"

echo "=== Failed Login Attempts (Last 24h) ==="
grep "Failed password" $LOG_FILE | since "24 hours ago" | wc -l

echo -e "\n=== Top IPs with Failed Logins ==="
grep "Failed password" $LOG_FILE | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn | head -10

echo -e "\n=== Successful Logins (Last 24h) ==="
grep "Accepted" $LOG_FILE | since "24 hours ago" | wc -l

echo -e "\n=== Sudo Usage (Last 24h) ==="
grep "sudo:" $LOG_FILE | since "24 hours ago" | wc -l

echo -e "\n=== New User Accounts ==="
grep "useradd" $LOG_FILE | tail -10

echo -e "\n=== SSH Key Changes ==="
grep "authorized_keys" $LOG_FILE | tail -10
```

### Intrusion Detection

```bash
#!/bin/bash
# Check for signs of compromise

echo "=== Checking for Rootkits ==="
rkhunter --check --skip-keypress

echo -e "\n=== Checking for Malware ==="
chkrootkit

echo -e "\n=== Checking for Suspicious Processes ==="
ps auxf | grep -v grep | grep -E "(nc|netcat|nmap|masscan)" || echo "No suspicious processes"

echo -e "\n=== Checking for Unusual Network Connections ==="
netstat -antp | grep -E "(ESTABLISHED|LISTEN)" | grep -v "127.0.0.1"

echo -e "\n=== Checking for Modified Binaries ==="
debsums -s 2>/dev/null || rpm -Va 2>/dev/null || echo "Package verification not available"

echo -e "\n=== Checking Cron Jobs ==="
cat /etc/crontab
ls -la /etc/cron.*
```

## Incident Response

### Security Incident Checklist

```
┌─────────────────────────────────────────────────────────────┐
│ Security Incident Response                                  │
├─────────────────────────────────────────────────────────────┤
│ IMMEDIATE ACTIONS                                           │
│ □ Isolate affected system                                   │
│ □ Preserve evidence (logs, memory dump)                     │
│ □ Document timeline                                         │
│ □ Notify security team                                      │
├─────────────────────────────────────────────────────────────┤
│ INVESTIGATION                                               │
│ □ Identify attack vector                                    │
│ □ Determine scope of compromise                             │
│ □ Check for lateral movement                                │
│ □ Identify affected data                                    │
├─────────────────────────────────────────────────────────────┤
│ CONTAINMENT                                                 │
│ □ Block attacker IPs                                        │
│ □ Rotate compromised credentials                            │
│ □ Patch vulnerabilities                                     │
│ □ Remove malware/backdoors                                  │
├─────────────────────────────────────────────────────────────┤
│ RECOVERY                                                    │
│ □ Restore from clean backup                                 │
│ □ Verify system integrity                                   │
│ □ Re-enable services                                        │
│ □ Monitor for re-infection                                  │
├─────────────────────────────────────────────────────────────┤
│ POST-INCIDENT                                               │
│ □ Document lessons learned                                  │
│ □ Update security controls                                  │
│ □ Report to stakeholders                                    │
│ □ Update incident response plan                             │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Resources

Refer to the following resources in this skill for detailed implementations:

- **`resources/cis-benchmarks.md`**: Complete CIS Benchmark implementation guide
- **`resources/security-checklist.md`**: Comprehensive security checklist with scripts
- **`resources/hardening-scripts/`**: Automated hardening scripts for different distributions

## Compliance Frameworks

### Supported Frameworks

| Framework | Coverage | Documentation |
|-----------|----------|---------------|
| CIS Benchmarks | 95% | resources/cis-benchmarks.md |
| NIST 800-53 | 80% | resources/nist-controls.md |
| PCI DSS | 75% | resources/pci-dss.md |
| HIPAA | 70% | resources/hipaa.md |
| SOC 2 | 80% | resources/soc2.md |

## Anti-Patterns

**Avoid these hardening mistakes:**

❌ **Hardening without backup** (always backup first)
❌ **Applying all controls at once** (phase the rollout)
❌ **Not testing after hardening** (verify functionality)
❌ **Ignoring application requirements** (consider app needs)
❌ **One-time hardening** (continuous process)
❌ **No documentation** (document all changes)
❌ **Skipping validation** (verify with scans)
❌ **Ignoring updates** (regular patching required)

## Success Metrics

**Measure hardening effectiveness:**

| Metric | Target | Measurement |
|--------|--------|-------------|
| CIS Score | > 90% | Lynis audit |
| Critical Vulnerabilities | 0 | Vulnerability scan |
| Failed Login Rate | < 10/day | Log analysis |
| Patch Compliance | > 95% | Update audit |
| Security Incidents | 0 | Incident tracking |

## Tool Usage

### Recommended Tools

**Security Scanning:**
- Lynis (system audit)
- OpenVAS (vulnerability scan)
- rkhunter (rootkit detection)
- chkrootkit (rootkit detection)

**Monitoring:**
- OSSEC (HIDS)
- Wazuh (SIEM)
- Fail2ban (intrusion prevention)
- Auditd (audit logging)

**Compliance:**
- CIS-CAT (CIS benchmark)
- OpenSCAP (compliance scanning)
- InSpec (compliance as code)
