---
name: ssh-config
description: SSH key management, config file setup, tunnels, and jump hosts. Use when user asks to "setup SSH keys", "configure SSH", "create SSH tunnel", "add SSH host", "jump host", "port forwarding", or manage SSH connections.
---

# SSH Config

SSH key management, configuration, and tunneling.

## Key Management

### Generate Keys

```bash
# Ed25519 (recommended)
ssh-keygen -t ed25519 -C "your@email.com"

# RSA (compatibility)
ssh-keygen -t rsa -b 4096 -C "your@email.com"

# Custom filename
ssh-keygen -t ed25519 -f ~/.ssh/github_key -C "github"
```

### Add to Agent

```bash
# Start agent
eval "$(ssh-agent -s)"

# Add key
ssh-add ~/.ssh/id_ed25519

# Add with timeout (12 hours)
ssh-add -t 43200 ~/.ssh/id_ed25519

# List keys
ssh-add -l
```

### Copy to Server

```bash
ssh-copy-id user@host
ssh-copy-id -i ~/.ssh/mykey.pub user@host
```

## SSH Config File

### Location

```
~/.ssh/config
```

### Basic Host Config

```ssh-config
Host myserver
    HostName 192.168.1.100
    User admin
    Port 22
    IdentityFile ~/.ssh/id_ed25519

Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/github_key
```

### Wildcards

```ssh-config
Host *.example.com
    User deploy
    IdentityFile ~/.ssh/deploy_key

Host 192.168.1.*
    User admin
    StrictHostKeyChecking no
```

### Jump Host (ProxyJump)

```ssh-config
Host bastion
    HostName bastion.example.com
    User jump

Host internal
    HostName 10.0.0.5
    User admin
    ProxyJump bastion
```

Then: `ssh internal`

### Keep Alive

```ssh-config
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

## Port Forwarding

### Local Forward

```bash
# Forward local:8080 to remote:80
ssh -L 8080:localhost:80 user@server

# Access remote database
ssh -L 5432:localhost:5432 user@server
# Then: psql -h localhost -p 5432
```

### Remote Forward

```bash
# Expose local:3000 on remote:8080
ssh -R 8080:localhost:3000 user@server
```

### Dynamic (SOCKS Proxy)

```bash
ssh -D 1080 user@server
# Configure browser to use SOCKS5 localhost:1080
```

### In Config

```ssh-config
Host tunnel-db
    HostName server.example.com
    User admin
    LocalForward 5432 localhost:5432
```

## Tunnels

### Persistent Tunnel (autossh)

```bash
# Install autossh
brew install autossh  # or apt install autossh

# Run persistent tunnel
autossh -M 0 -f -N -L 8080:localhost:80 user@server
```

### Background Tunnel

```bash
ssh -f -N -L 8080:localhost:80 user@server
```

## Security

### Permissions

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
chmod 600 ~/.ssh/config
chmod 600 ~/.ssh/authorized_keys
```

### Disable Password Auth (Server)

```
# /etc/ssh/sshd_config
PasswordAuthentication no
PubkeyAuthentication yes
```

## Quick Commands

```bash
# Test connection
ssh -T git@github.com

# Verbose debug
ssh -vvv user@host

# Run remote command
ssh user@host 'ls -la'

# Copy files
scp file.txt user@host:/path/
scp -r folder/ user@host:/path/

# rsync over SSH
rsync -avz -e ssh folder/ user@host:/path/
```
