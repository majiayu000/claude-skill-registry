---
name: ssh-essentials
description: Essential SSH commands for secure remote access, key management, port forwarding, tunneling, file transfers, and SSH configuration best practices.
---

# SSH Essentials

## Basic Connection

```bash
ssh user@hostname
ssh user@hostname -p 2222
ssh -i ~/.ssh/id_rsa user@hostname
ssh -v user@hostname        # verbose (debug)
ssh -J jumphost user@target # jump host / bastion
```

## SSH Keys

```bash
# Generate key
ssh-keygen -t ed25519 -C "your@email.com"
ssh-keygen -t rsa -b 4096 -C "your@email.com"

# Copy key to server
ssh-copy-id user@hostname
ssh-copy-id -i ~/.ssh/id_rsa.pub user@hostname

# Check loaded keys
ssh-add -l

# Add key to agent
ssh-add ~/.ssh/id_rsa
ssh-add -K ~/.ssh/id_rsa   # macOS: add to keychain
```

## Port Forwarding & Tunneling

```bash
# Local port forwarding (access remote service locally)
ssh -L 8080:localhost:80 user@remote
ssh -L 3306:db-server:3306 user@bastion    # MySQL through bastion

# Remote port forwarding (expose local service to remote)
ssh -R 8080:localhost:3000 user@remote

# Dynamic SOCKS proxy
ssh -D 1080 user@remote

# Persistent tunnel with autossh
autossh -M 0 -N -L 3306:localhost:3306 user@remote
```

## File Transfers

```bash
# SCP
scp file.txt user@host:/remote/path/
scp user@host:/remote/file.txt /local/path/
scp -r /local/dir user@host:/remote/dir

# rsync (preferred for directories)
rsync -avz /local/dir/ user@host:/remote/dir/
rsync -avz --delete /local/dir/ user@host:/remote/dir/
rsync -avz -e "ssh -p 2222" /local/dir/ user@host:/remote/dir/
```

## SSH Config (~/.ssh/config)

```
Host myserver
    HostName 192.168.1.100
    User deploy
    Port 22
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
    ServerAliveCountMax 3

Host bastion
    HostName bastion.example.com
    User admin

Host prod-db
    HostName 10.0.0.5
    User deploy
    ProxyJump bastion
```

```bash
ssh myserver     # uses config above
```

## Security Best Practices

```bash
# /etc/ssh/sshd_config best practices:
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AllowUsers deploy
MaxAuthTries 3
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 2

# After changes:
sshd -t          # test config
systemctl restart sshd
```

## Troubleshooting

```bash
ssh -vvv user@host          # max verbosity
journalctl -u sshd -f       # server logs
tail -f /var/log/auth.log   # auth attempts
ss -tlnp | grep :22         # check sshd listening
```

## Tips

- Always use ed25519 keys (faster, more secure than RSA 2048)
- Never disable StrictHostKeyChecking in production
- Use SSH agent forwarding (`-A`) sparingly — security risk
- `ProxyJump` is the modern replacement for `ProxyCommand`
- `ServerAliveInterval 60` prevents timeout on idle connections
