---
name: SSH Key-Based Authentication
description: This skill should be used when the user asks to "configure SSH key authentication", "set up SSH keys", "generate SSH key pairs", "copy SSH keys to servers", "configure SSH config file", "troubleshoot SSH key access", "manage multiple SSH keys", "restrict SSH key usage", "secure SSH access", or "automate SSH connections". Use this skill to implement secure, passwordless SSH authentication using cryptographic key pairs.
version: 1.0.0
tags: [ssh, authentication, security, cryptography, devops, remote-access, automation]
---

# SSH Key-Based Authentication

## Purpose

Implement secure SSH key-based authentication for remote server access. This skill covers generating cryptographic key pairs, deploying public keys to servers, configuring SSH clients for multiple servers, and applying security best practices. Essential for DevOps automation, secure system administration, and eliminating password-based authentication vulnerabilities.

## Prerequisites

- Access to client and server systems with SSH installed
- User account on remote server with home directory access
- Terminal or command-line interface familiarity
- Understanding of file permissions concepts
- Root or sudo access for server-side configuration (optional)

## Outputs and Deliverables

- Generated RSA/ED25519 SSH key pairs
- Configured remote server authorized_keys file
- SSH client configuration file for multiple servers
- Secure passwordless authentication setup
- Documentation of key management procedures

---

## Core Workflow

### Phase 1: Understand SSH Key Architecture

Master the fundamentals of SSH key-based authentication:

**Key Pair Components**

| Component | Location | Purpose | Security |
|-----------|----------|---------|----------|
| Private Key | Client: ~/.ssh/id_rsa | Proves identity | MUST remain secret |
| Public Key | Server: ~/.ssh/authorized_keys | Verifies identity | Can be shared freely |

**Why Keys Over Passwords**
- Enhanced Security: Private keys are cryptographically strong (2048-4096 bits)
- Brute Force Resistant: Practically impossible to guess key values
- Automation Ready: Enables scripted/CI/CD server access
- Convenience: No password entry required after setup
- Audit Trail: Keys can be individually tracked and revoked

**Key Algorithms**
```bash
# RSA - widely compatible, use 4096 bits
ssh-keygen -t rsa -b 4096

# ED25519 - modern, smaller, faster (recommended)
ssh-keygen -t ed25519

# ECDSA - elliptic curve alternative
ssh-keygen -t ecdsa -b 521
```

### Phase 2: Generate SSH Key Pairs

Create cryptographic key pairs on the client machine:

**Standard Key Generation**
```bash
# Generate RSA 4096-bit key with email identifier
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Interactive prompts:
# 1. File location: Press Enter for default (~/.ssh/id_rsa)
# 2. Passphrase: Enter strong passphrase (recommended)
```

**Advanced Key Generation Options**
```bash
# Generate ED25519 key (modern, recommended)
ssh-keygen -t ed25519 -C "user@hostname" -f ~/.ssh/myserver_ed25519

# Generate key with specific filename
ssh-keygen -t rsa -b 4096 -f ~/.ssh/production_key -C "production-access"

# Generate key without passphrase (automation only)
ssh-keygen -t ed25519 -N "" -f ~/.ssh/automation_key -C "automation"
```

**Parameter Reference**

| Option | Description | Example |
|--------|-------------|---------|
| -t | Key type (rsa, ed25519, ecdsa) | -t ed25519 |
| -b | Key bits (RSA: 2048/4096) | -b 4096 |
| -C | Comment (identifier) | -C "admin@server" |
| -f | Output filename | -f ~/.ssh/mykey |
| -N | New passphrase | -N "passphrase" |
| -p | Change passphrase | ssh-keygen -p -f keyfile |

**Generated Files**
```
~/.ssh/id_rsa        # Private key (PROTECT THIS)
~/.ssh/id_rsa.pub    # Public key (share with servers)
```

### Phase 3: Deploy Public Keys to Servers

Install public key on remote servers for authentication:

**Method 1: ssh-copy-id (Recommended)**
```bash
# Copy public key to remote server
ssh-copy-id username@remote_server

# Specify a particular key
ssh-copy-id -i ~/.ssh/mykey.pub username@remote_server

# Use non-standard port
ssh-copy-id -p 2222 username@remote_server
```

**Method 2: Manual Installation**
```bash
# Display public key on client
cat ~/.ssh/id_rsa.pub

# On remote server, add to authorized_keys
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "ssh-rsa AAAA..." >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

**Method 3: One-liner (pipe method)**
```bash
# Combine into single command
cat ~/.ssh/id_rsa.pub | ssh username@server "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

**Verify Deployment**
```bash
# Test key-based authentication
ssh username@remote_server

# Verify with verbose output
ssh -v username@remote_server
```

### Phase 4: Configure SSH Client

Streamline connections with SSH config file:

**Create Configuration File**
```bash
# Edit or create SSH config
nano ~/.ssh/config

# Set proper permissions
chmod 600 ~/.ssh/config
```

**Basic Configuration Example**
```
# Production Web Server
Host prod-web
    HostName 192.168.1.100
    User admin
    IdentityFile ~/.ssh/production_key
    Port 22

# Development Server
Host dev
    HostName dev.example.com
    User developer
    IdentityFile ~/.ssh/dev_key
    Port 2222

# Jump Host Configuration
Host bastion
    HostName bastion.example.com
    User jumpuser
    IdentityFile ~/.ssh/bastion_key

Host internal-*
    ProxyJump bastion
    User admin
    IdentityFile ~/.ssh/internal_key
```

**Configuration Options Reference**

| Directive | Purpose | Example |
|-----------|---------|---------|
| Host | Alias for connection | Host myserver |
| HostName | Actual hostname/IP | HostName 10.0.0.1 |
| User | Login username | User admin |
| IdentityFile | Private key path | IdentityFile ~/.ssh/key |
| Port | SSH port | Port 2222 |
| ProxyJump | Jump through host | ProxyJump bastion |
| ForwardAgent | Forward SSH agent | ForwardAgent yes |
| IdentitiesOnly | Use specified key only | IdentitiesOnly yes |
| ServerAliveInterval | Keep connection alive | ServerAliveInterval 60 |

**Connect Using Aliases**
```bash
# Instead of: ssh -i ~/.ssh/production_key admin@192.168.1.100
ssh prod-web

# Instead of complex jump commands
ssh internal-db
```

### Phase 5: Manage SSH Agent

Use SSH agent for key passphrase caching:

**Start SSH Agent**
```bash
# Start agent (Bash)
eval "$(ssh-agent -s)"

# Start agent (Fish shell)
eval (ssh-agent -c)
```

**Add Keys to Agent**
```bash
# Add default key
ssh-add

# Add specific key
ssh-add ~/.ssh/production_key

# Add key with time limit (seconds)
ssh-add -t 3600 ~/.ssh/sensitive_key

# List loaded keys
ssh-add -l

# Remove specific key
ssh-add -d ~/.ssh/oldkey

# Remove all keys
ssh-add -D
```

**Persistent Agent Setup**
```bash
# Add to ~/.bashrc or ~/.zshrc
if [ -z "$SSH_AUTH_SOCK" ]; then
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_ed25519
fi
```

**Keychain for Persistence (Linux)**
```bash
# Install keychain
sudo apt install keychain

# Add to shell profile
eval $(keychain --eval --agents ssh id_ed25519 production_key)
```

### Phase 6: Restrict Key Usage

Implement security restrictions on SSH keys:

**Command Restrictions**
```bash
# In authorized_keys, prefix key with command restriction
command="/usr/bin/backup.sh" ssh-ed25519 AAAA... backup@server

# Restrict to specific commands with options
command="/usr/bin/rsync --server",no-port-forwarding,no-X11-forwarding ssh-rsa AAAA...
```

**Available Restrictions**

| Option | Effect |
|--------|--------|
| command="cmd" | Only allow specified command |
| no-port-forwarding | Disable port forwarding |
| no-X11-forwarding | Disable X11 forwarding |
| no-agent-forwarding | Disable agent forwarding |
| no-pty | Disable terminal allocation |
| from="pattern" | Restrict source IP/hostname |
| environment="VAR=value" | Set environment variable |

**IP Restrictions**
```bash
# Allow only from specific IP
from="192.168.1.50" ssh-ed25519 AAAA... user@host

# Allow from IP range
from="192.168.1.0/24" ssh-ed25519 AAAA... user@host

# Allow from multiple sources
from="192.168.1.50,10.0.0.0/8,*.example.com" ssh-ed25519 AAAA... user@host
```

**Combined Restrictions Example**
```
from="10.0.0.0/8",command="/usr/local/bin/deploy.sh",no-port-forwarding,no-X11-forwarding,no-agent-forwarding ssh-ed25519 AAAA... deploy@ci-server
```

### Phase 7: Set Proper Permissions

Ensure correct file permissions for SSH:

**Client-Side Permissions**
```bash
# SSH directory
chmod 700 ~/.ssh

# Private keys (CRITICAL)
chmod 600 ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_ed25519
chmod 600 ~/.ssh/*_key

# Public keys
chmod 644 ~/.ssh/*.pub

# Config file
chmod 600 ~/.ssh/config

# Known hosts
chmod 644 ~/.ssh/known_hosts
```

**Server-Side Permissions**
```bash
# SSH directory
chmod 700 ~/.ssh

# Authorized keys file
chmod 600 ~/.ssh/authorized_keys

# Home directory (should not be group/world writable)
chmod 755 ~
# or
chmod 700 ~
```

**Verify Permissions**
```bash
# Check all SSH file permissions
ls -la ~/.ssh/

# Expected output:
# drwx------  .ssh/
# -rw-------  id_rsa
# -rw-r--r--  id_rsa.pub
# -rw-------  config
# -rw-------  authorized_keys
```

### Phase 8: Multiple Key Management

Organize and manage multiple SSH keys:

**Key Organization Strategy**
```
~/.ssh/
├── id_ed25519              # Default personal key
├── id_ed25519.pub
├── work_rsa                # Work servers
├── work_rsa.pub
├── production_ed25519      # Production systems
├── production_ed25519.pub
├── github_ed25519          # GitHub/GitLab
├── github_ed25519.pub
├── config                  # SSH configuration
└── known_hosts             # Known host keys
```

**Configuration for Multiple Keys**
```
# GitHub
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/github_ed25519
    IdentitiesOnly yes

# GitLab
Host gitlab.com
    HostName gitlab.com
    User git
    IdentityFile ~/.ssh/gitlab_ed25519
    IdentitiesOnly yes

# Work servers (pattern matching)
Host *.work.example.com
    User workuser
    IdentityFile ~/.ssh/work_rsa
    IdentitiesOnly yes

# Default for unknown hosts
Host *
    IdentityFile ~/.ssh/id_ed25519
    AddKeysToAgent yes
```

**Test Specific Key Usage**
```bash
# Test GitHub connection
ssh -T git@github.com

# Verify which key is being used
ssh -v git@github.com 2>&1 | grep "Offering"
```

### Phase 9: Key Rotation and Backup

Implement key lifecycle management:

**Key Rotation Procedure**
```bash
# 1. Generate new key pair
ssh-keygen -t ed25519 -f ~/.ssh/newkey_$(date +%Y%m%d) -C "rotated-$(date +%Y%m%d)"

# 2. Deploy new public key to all servers
ssh-copy-id -i ~/.ssh/newkey_*.pub user@server1
ssh-copy-id -i ~/.ssh/newkey_*.pub user@server2

# 3. Test new key
ssh -i ~/.ssh/newkey_* user@server1

# 4. Update SSH config
# 5. Remove old key from servers' authorized_keys
# 6. Securely delete old private key
shred -u ~/.ssh/oldkey
```

**Backup Private Keys Securely**
```bash
# Encrypt backup with GPG
gpg --symmetric --cipher-algo AES256 -o ssh_keys_backup.gpg ~/.ssh/id_ed25519

# Store encrypted backup in secure location
# NEVER store unencrypted private keys in cloud storage

# Restore from backup
gpg --decrypt ssh_keys_backup.gpg > ~/.ssh/id_ed25519
chmod 600 ~/.ssh/id_ed25519
```

**Key Inventory Documentation**
```markdown
| Key Name | Algorithm | Created | Servers | Purpose | Expires |
|----------|-----------|---------|---------|---------|---------|
| id_ed25519 | ED25519 | 2024-01 | personal | Default | 2025-01 |
| prod_key | RSA-4096 | 2024-01 | prod-* | Production | 2024-07 |
| deploy_key | ED25519 | 2024-02 | ci/cd | Automation | 2024-08 |
```

### Phase 10: Troubleshoot SSH Key Issues

Diagnose and resolve common problems:

**Debug Connection**
```bash
# Verbose output (1-3 v's for increasing detail)
ssh -v username@server
ssh -vv username@server
ssh -vvv username@server

# Check what keys are being offered
ssh -v user@server 2>&1 | grep -E "Offering|Trying"
```

**Common Issues and Solutions**

| Issue | Cause | Solution |
|-------|-------|----------|
| Permission denied (publickey) | Wrong permissions | chmod 600 ~/.ssh/id_rsa |
| Agent has no identities | Key not loaded | ssh-add ~/.ssh/id_rsa |
| Too many authentication failures | Too many keys tried | Use IdentitiesOnly yes |
| Host key verification failed | Known hosts mismatch | Remove old entry from known_hosts |
| Connection refused | SSH not running/port blocked | Check sshd status, firewall |

**Fix Permission Issues**
```bash
# Fix all SSH permissions at once
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_* ~/.ssh/config ~/.ssh/authorized_keys
chmod 644 ~/.ssh/*.pub ~/.ssh/known_hosts
```

**Check Server-Side Logs**
```bash
# View SSH authentication logs
sudo tail -f /var/log/auth.log        # Debian/Ubuntu
sudo tail -f /var/log/secure          # RHEL/CentOS
sudo journalctl -u sshd -f            # Systemd systems
```

**Force Password Authentication (Testing)**
```bash
# Bypass keys temporarily for troubleshooting
ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no user@server
```

---

## Quick Reference

### Key Generation Commands
```bash
ssh-keygen -t ed25519 -C "comment"              # ED25519 (recommended)
ssh-keygen -t rsa -b 4096 -C "comment"          # RSA 4096-bit
ssh-keygen -p -f ~/.ssh/keyfile                 # Change passphrase
ssh-keygen -y -f ~/.ssh/private_key             # Show public key
ssh-keygen -l -f ~/.ssh/key.pub                 # Show key fingerprint
```

### Key Deployment
```bash
ssh-copy-id user@server                          # Copy default key
ssh-copy-id -i ~/.ssh/key.pub user@server       # Copy specific key
cat key.pub | ssh user@server "cat >> ~/.ssh/authorized_keys"
```

### SSH Agent Commands
```bash
eval "$(ssh-agent -s)"                          # Start agent
ssh-add                                          # Add default key
ssh-add ~/.ssh/keyfile                          # Add specific key
ssh-add -l                                       # List loaded keys
ssh-add -D                                       # Remove all keys
```

### Required Permissions
```
~/.ssh/           700 (drwx------)
id_rsa            600 (-rw-------)
id_rsa.pub        644 (-rw-r--r--)
authorized_keys   600 (-rw-------)
config            600 (-rw-------)
```

---

## Constraints and Limitations

- Private keys must never be shared or transmitted insecurely
- Keys without passphrases create security risk if system compromised
- Some legacy systems may not support ED25519 (use RSA)
- Jump hosts require additional configuration for agent forwarding
- Key rotation requires coordination across all systems
- Lost private keys with no backup result in permanent access loss
- SSH agent forwarding carries security risks on untrusted systems

---

## Troubleshooting

### Quick Diagnostics
```bash
# Check key permissions
ls -la ~/.ssh/

# Test key authentication explicitly
ssh -i ~/.ssh/keyfile -o IdentitiesOnly=yes user@server

# Verify agent has key loaded
ssh-add -l

# View offered authentication methods
ssh -o PreferredAuthentications=publickey -v user@server 2>&1 | grep "Authentications"
```

### Error Resolution Table

| Error Message | Resolution |
|---------------|------------|
| "Permission denied (publickey)" | Check key permissions, verify key in authorized_keys |
| "No such identity" | Key file path incorrect, run ssh-add |
| "Agent refused operation" | Restart SSH agent, re-add keys |
| "Host key verification failed" | ssh-keygen -R hostname |
| "Too many authentication failures" | Add IdentitiesOnly yes to config |
| "Could not open a connection" | Check network, firewall, SSH service |

---

## References

- OpenSSH Documentation: https://www.openssh.com/manual.html
- SSH Academy: https://www.ssh.com/academy/ssh
- NIST Guidelines for SSH Key Management
- Author: Zayan Ahmed - SSH Access Through Keys
