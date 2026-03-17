---
name: system-hardening-toolkit
version: 1.0.0
description: |
  macOS and Linux security hardening toolkit providing configuration scripts,
  audit checklists, and remediation procedures for system security.
author: QuantQuiver AI R&D
license: MIT

category: tooling
tags:
  - security
  - hardening
  - macos
  - linux
  - system-administration
  - compliance
  - sysadmin

dependencies:
  skills: []
  python: ">=3.9"
  packages: []
  tools:
    - bash
    - code_execution

triggers:
  - "harden system"
  - "security hardening"
  - "secure macOS"
  - "Linux security"
  - "system security audit"
  - "compliance check"
  - "security baseline"
---

# System Hardening Toolkit

## Purpose

A macOS and Linux security hardening toolkit providing configuration scripts, audit checklists, and remediation procedures for system security. Implements CIS benchmarks and security best practices.

**Problem Space:**
- Default OS configurations prioritize usability over security
- Security hardening is complex and error-prone
- Compliance requirements vary by environment
- Manual hardening is time-consuming

**Solution Approach:**
- Automated configuration scripts
- Audit checklists aligned with CIS benchmarks
- Rollback-safe implementations
- Environment-aware recommendations

## When to Use

- New system setup for development
- Production server hardening
- Security audit preparation
- Compliance requirements (SOC2, HIPAA, PCI)
- After security incident for remediation

## When NOT to Use

- Managed corporate devices (use MDM)
- Cloud infrastructure (use cloud-native security)
- Windows systems (different tooling needed)
- When modifications may break critical applications

---

## Core Instructions

### Security Domains

```
┌─────────────────────────────────────────────────────────────────┐
│                    HARDENING DOMAINS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Authentication & Access Control                             │
│     ├── Password policies                                       │
│     ├── SSH configuration                                       │
│     ├── Sudo configuration                                      │
│     └── User account management                                 │
│                                                                 │
│  2. Network Security                                            │
│     ├── Firewall configuration                                  │
│     ├── Network services                                        │
│     ├── TLS/SSL settings                                        │
│     └── DNS security                                            │
│                                                                 │
│  3. File System Security                                        │
│     ├── Permissions                                             │
│     ├── Encryption                                              │
│     ├── Mount options                                           │
│     └── Audit logging                                           │
│                                                                 │
│  4. Service Hardening                                           │
│     ├── Disable unnecessary services                            │
│     ├── Service isolation                                       │
│     ├── Process restrictions                                    │
│     └── Resource limits                                         │
│                                                                 │
│  5. Monitoring & Logging                                        │
│     ├── Audit configuration                                     │
│     ├── Log rotation                                            │
│     ├── Intrusion detection                                     │
│     └── Alerting                                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Standard Procedures

#### 1. Pre-Hardening Assessment

```bash
#!/bin/bash
# System assessment script

echo "=== System Information ==="
uname -a
sw_vers 2>/dev/null || cat /etc/os-release

echo "=== Current Users ==="
dscl . list /Users 2>/dev/null || cat /etc/passwd

echo "=== Running Services ==="
launchctl list 2>/dev/null || systemctl list-units --type=service

echo "=== Open Ports ==="
lsof -i -P -n | grep LISTEN

echo "=== Firewall Status ==="
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null || ufw status

echo "=== SSH Configuration ==="
grep -v "^#" /etc/ssh/sshd_config | grep -v "^$"
```

#### 2. Create Backup

Always backup before hardening:
```bash
# Backup critical configs
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup.$(date +%Y%m%d)
sudo cp /etc/sudoers /etc/sudoers.backup.$(date +%Y%m%d)
```

#### 3. Apply Hardening

Apply changes incrementally with verification.

#### 4. Post-Hardening Verification

Run audit script to confirm changes applied correctly.

### Decision Framework

**Hardening Level Selection:**

| Level | Use Case | Risk Tolerance |
|-------|----------|----------------|
| **Minimal** | Development workstation | High - need flexibility |
| **Standard** | General server | Medium - balance security/usability |
| **Strict** | Production/compliance | Low - security first |
| **Paranoid** | High-security environments | None - maximum restrictions |

---

## Templates

### macOS Hardening Script

```bash
#!/bin/bash
# macOS Security Hardening Script
# Compatible with macOS 12+ (Monterey and later)

set -e

BACKUP_DIR="/var/backups/security-hardening/$(date +%Y%m%d-%H%M%S)"
LOG_FILE="/var/log/security-hardening.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

backup_file() {
    if [ -f "$1" ]; then
        mkdir -p "$BACKUP_DIR/$(dirname "$1")"
        cp "$1" "$BACKUP_DIR/$1"
        log "Backed up: $1"
    fi
}

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root"
    exit 1
fi

mkdir -p "$BACKUP_DIR"
log "Starting macOS hardening..."

# ============================================
# 1. FIREWALL CONFIGURATION
# ============================================
log "Configuring firewall..."

# Enable firewall
/usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on

# Enable stealth mode (don't respond to probes)
/usr/libexec/ApplicationFirewall/socketfilterfw --setstealthmode on

# Enable logging
/usr/libexec/ApplicationFirewall/socketfilterfw --setloggingmode on

# Block all incoming connections (except established)
/usr/libexec/ApplicationFirewall/socketfilterfw --setblockall on

log "Firewall configured."

# ============================================
# 2. SYSTEM INTEGRITY PROTECTION
# ============================================
log "Verifying SIP status..."

if csrutil status | grep -q "enabled"; then
    log "SIP is enabled (good)"
else
    log "WARNING: SIP is disabled. Enable in Recovery Mode."
fi

# ============================================
# 3. FILEVAULT ENCRYPTION
# ============================================
log "Checking FileVault status..."

if fdesetup status | grep -q "FileVault is On"; then
    log "FileVault is enabled (good)"
else
    log "WARNING: FileVault is not enabled. Consider enabling disk encryption."
fi

# ============================================
# 4. GATEKEEPER
# ============================================
log "Configuring Gatekeeper..."

# Enable Gatekeeper
spctl --master-enable

# Verify
spctl --status

log "Gatekeeper enabled."

# ============================================
# 5. AUTOMATIC UPDATES
# ============================================
log "Configuring automatic updates..."

# Enable automatic update checks
defaults write /Library/Preferences/com.apple.SoftwareUpdate AutomaticCheckEnabled -bool true

# Download updates automatically
defaults write /Library/Preferences/com.apple.SoftwareUpdate AutomaticDownload -bool true

# Install system updates automatically
defaults write /Library/Preferences/com.apple.SoftwareUpdate AutomaticallyInstallMacOSUpdates -bool true

# Install security updates automatically
defaults write /Library/Preferences/com.apple.SoftwareUpdate CriticalUpdateInstall -bool true

log "Automatic updates configured."

# ============================================
# 6. SSH HARDENING
# ============================================
log "Hardening SSH configuration..."

backup_file /etc/ssh/sshd_config

cat > /etc/ssh/sshd_config << 'EOF'
# Hardened SSH Configuration

# Protocol and network
Protocol 2
Port 22
AddressFamily inet
ListenAddress 0.0.0.0

# Authentication
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication no
PermitEmptyPasswords no
ChallengeResponseAuthentication no
UsePAM yes

# Security
X11Forwarding no
AllowTcpForwarding no
AllowAgentForwarding no
PermitTunnel no
GatewayPorts no

# Session
ClientAliveInterval 300
ClientAliveCountMax 2
LoginGraceTime 60
MaxAuthTries 3
MaxSessions 2

# Logging
SyslogFacility AUTH
LogLevel VERBOSE

# Ciphers and algorithms
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
KexAlgorithms curve25519-sha256@libssh.org,diffie-hellman-group16-sha512
EOF

log "SSH hardened. Restart SSH service to apply changes."

# ============================================
# 7. PRIVACY SETTINGS
# ============================================
log "Configuring privacy settings..."

# Disable Siri analytics
defaults write com.apple.assistant.support "Assistant Enabled" -bool false

# Disable personalized ads
defaults write com.apple.AdLib allowApplePersonalizedAdvertising -bool false

# Disable crash reporter
defaults write com.apple.CrashReporter DialogType -string "none"

log "Privacy settings configured."

# ============================================
# 8. AUDIT LOGGING
# ============================================
log "Configuring audit logging..."

# Enable audit logging
launchctl load -w /System/Library/LaunchDaemons/com.apple.auditd.plist 2>/dev/null || true

log "Audit logging configured."

# ============================================
# SUMMARY
# ============================================
log ""
log "=== Hardening Complete ==="
log "Backup location: $BACKUP_DIR"
log "Log file: $LOG_FILE"
log ""
log "Manual steps required:"
log "1. Enable FileVault if not already enabled"
log "2. Restart SSH service: sudo launchctl unload/load /System/Library/LaunchDaemons/ssh.plist"
log "3. Review and test all changes"
```

### Linux (Ubuntu/Debian) Hardening Script

```bash
#!/bin/bash
# Linux Security Hardening Script
# Compatible with Ubuntu 20.04+, Debian 11+

set -e

BACKUP_DIR="/var/backups/security-hardening/$(date +%Y%m%d-%H%M%S)"
LOG_FILE="/var/log/security-hardening.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

backup_file() {
    if [ -f "$1" ]; then
        mkdir -p "$BACKUP_DIR/$(dirname "$1")"
        cp "$1" "$BACKUP_DIR/$1"
        log "Backed up: $1"
    fi
}

if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root"
    exit 1
fi

mkdir -p "$BACKUP_DIR"
log "Starting Linux hardening..."

# ============================================
# 1. UPDATE SYSTEM
# ============================================
log "Updating system packages..."

apt-get update
apt-get upgrade -y
apt-get dist-upgrade -y
apt-get autoremove -y

# Enable automatic security updates
apt-get install -y unattended-upgrades
dpkg-reconfigure -plow unattended-upgrades

log "System updated."

# ============================================
# 2. SSH HARDENING
# ============================================
log "Hardening SSH..."

backup_file /etc/ssh/sshd_config

cat > /etc/ssh/sshd_config << 'EOF'
# Hardened SSH Configuration

Port 22
Protocol 2
AddressFamily inet

# Logging
SyslogFacility AUTH
LogLevel VERBOSE

# Authentication
LoginGraceTime 60
PermitRootLogin no
StrictModes yes
MaxAuthTries 3
MaxSessions 2

PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys

PasswordAuthentication no
PermitEmptyPasswords no
ChallengeResponseAuthentication no

# Security
X11Forwarding no
AllowTcpForwarding no
AllowAgentForwarding no
PermitTunnel no
GatewayPorts no
PermitUserEnvironment no

UsePAM yes

# Session
ClientAliveInterval 300
ClientAliveCountMax 2

# Ciphers
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
KexAlgorithms curve25519-sha256@libssh.org,diffie-hellman-group16-sha512

# Banner
Banner /etc/issue.net
EOF

systemctl restart sshd

log "SSH hardened."

# ============================================
# 3. FIREWALL (UFW)
# ============================================
log "Configuring firewall..."

apt-get install -y ufw

# Default policies
ufw default deny incoming
ufw default allow outgoing

# Allow SSH (adjust port if changed)
ufw allow 22/tcp

# Enable firewall
ufw --force enable

log "Firewall configured."

# ============================================
# 4. KERNEL HARDENING
# ============================================
log "Hardening kernel parameters..."

backup_file /etc/sysctl.conf

cat > /etc/sysctl.d/99-security.conf << 'EOF'
# Kernel hardening parameters

# IP Spoofing protection
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1

# Ignore ICMP broadcast requests
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Disable source packet routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv6.conf.default.accept_source_route = 0

# Ignore send redirects
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0

# Block SYN attacks
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 2048
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 5

# Log Martians
net.ipv4.conf.all.log_martians = 1

# Ignore ICMP redirects
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv6.conf.default.accept_redirects = 0

# Disable IPv6 if not needed
# net.ipv6.conf.all.disable_ipv6 = 1

# Protect against SYN flood
net.ipv4.tcp_syncookies = 1

# Restrict core dumps
fs.suid_dumpable = 0

# Randomize virtual address space
kernel.randomize_va_space = 2
EOF

sysctl -p /etc/sysctl.d/99-security.conf

log "Kernel hardened."

# ============================================
# 5. USER AND PASSWORD POLICIES
# ============================================
log "Configuring password policies..."

apt-get install -y libpam-pwquality

backup_file /etc/security/pwquality.conf

cat > /etc/security/pwquality.conf << 'EOF'
# Password quality requirements
minlen = 14
dcredit = -1
ucredit = -1
ocredit = -1
lcredit = -1
minclass = 4
maxrepeat = 3
maxclassrepeat = 3
EOF

# Password aging
sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS 90/' /etc/login.defs
sed -i 's/^PASS_MIN_DAYS.*/PASS_MIN_DAYS 1/' /etc/login.defs
sed -i 's/^PASS_WARN_AGE.*/PASS_WARN_AGE 7/' /etc/login.defs

log "Password policies configured."

# ============================================
# 6. DISABLE UNNECESSARY SERVICES
# ============================================
log "Disabling unnecessary services..."

services_to_disable=(
    "cups"
    "avahi-daemon"
    "bluetooth"
)

for service in "${services_to_disable[@]}"; do
    if systemctl is-active --quiet "$service"; then
        systemctl stop "$service"
        systemctl disable "$service"
        log "Disabled service: $service"
    fi
done

log "Services disabled."

# ============================================
# 7. INSTALL SECURITY TOOLS
# ============================================
log "Installing security tools..."

apt-get install -y \
    fail2ban \
    auditd \
    rkhunter \
    chkrootkit \
    aide

# Configure fail2ban
systemctl enable fail2ban
systemctl start fail2ban

# Configure auditd
systemctl enable auditd
systemctl start auditd

log "Security tools installed."

# ============================================
# SUMMARY
# ============================================
log ""
log "=== Hardening Complete ==="
log "Backup location: $BACKUP_DIR"
log "Log file: $LOG_FILE"
log ""
log "Post-hardening steps:"
log "1. Initialize AIDE: aideinit"
log "2. Configure fail2ban jails as needed"
log "3. Run rkhunter --update && rkhunter --check"
log "4. Review audit logs"
```

### Security Audit Checklist

```yaml
audit_checklist:
  authentication:
    - name: "Root login disabled"
      check: "grep 'PermitRootLogin no' /etc/ssh/sshd_config"
      severity: CRITICAL

    - name: "Password authentication disabled"
      check: "grep 'PasswordAuthentication no' /etc/ssh/sshd_config"
      severity: HIGH

    - name: "Strong password policy"
      check: "grep 'minlen = 14' /etc/security/pwquality.conf"
      severity: MEDIUM

  network:
    - name: "Firewall enabled"
      check: "ufw status | grep 'Status: active'"
      severity: CRITICAL

    - name: "No unnecessary open ports"
      check: "ss -tulpn | grep LISTEN"
      severity: HIGH

  filesystem:
    - name: "Sensitive files permissions"
      check: "stat -c '%a' /etc/shadow | grep '640'"
      severity: HIGH

    - name: "No world-writable files"
      check: "find / -xdev -type f -perm -0002 2>/dev/null"
      severity: MEDIUM

  services:
    - name: "Unnecessary services disabled"
      check: "systemctl list-unit-files --state=enabled"
      severity: MEDIUM

  logging:
    - name: "Auditd running"
      check: "systemctl is-active auditd"
      severity: HIGH
```

---

## Examples

### Example 1: Secure Development Mac

**Input**: "Harden my Mac for secure development"

**Output**: Script applying minimal hardening:
- Firewall enabled
- Gatekeeper enabled
- SSH key-only auth
- FileVault reminder
- Automatic updates enabled

### Example 2: Production Server Hardening

**Input**: "Secure my Ubuntu server for production"

**Output**: Comprehensive hardening:
- Full SSH hardening
- UFW with minimal ports
- Kernel parameter hardening
- Fail2ban installation
- Audit logging enabled

---

## Validation Checklist

Before and after hardening:

- [ ] Backup created and verified
- [ ] SSH access tested before logout
- [ ] Firewall rules verified
- [ ] Services still functional
- [ ] No unauthorized port changes
- [ ] Audit logging working
- [ ] Rollback procedure documented

---

## Related Resources

- Skill: `repository-auditor` - Security scanning for code
- Skill: `cicd-pipeline-generator` - Security in CI/CD
- CIS Benchmarks: https://www.cisecurity.org/cis-benchmarks
- NIST Guidelines: https://csrc.nist.gov/

---

## Changelog

### 1.0.0 (January 2026)
- Initial release
- macOS hardening script
- Linux (Ubuntu/Debian) hardening script
- Audit checklist template
- Rollback procedures
