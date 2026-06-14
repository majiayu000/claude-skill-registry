---
name: ssh
user-invocable: false
skill_api_version: 1
hexagonal_role: supporting
metadata:
  tier: execution
description: "Use when configuring SSH access, keys, tunnels, host diagnostics, or safe remote command workflows."
practices:
- pragmatic-programmer
---
<!-- TOC: Quick Start | THE EXACT PROMPT | Essential Commands | Config | AGENTS.md Blurb | References -->

# SSH — Secure Remote Access

> **Core Capability:** Secure shell connections, key management, tunneling, and file transfers.

---

## Quick Start

```bash
# Connect to server
ssh user@hostname

# Connect with specific key
ssh -i ~/.ssh/my_key user@hostname

# Run remote command
ssh user@host "cd /app && git status"

# Copy file to remote
scp local.txt user@host:/remote/path/

# Sync directory (preferred over scp)
rsync -avzP ./local/ user@host:/remote/
```

---

## THE EXACT PROMPT — Common Workflows

### Connect Through Jump Host

```bash
# Single jump (bastion)
ssh -J jumphost user@internal-server

# Multiple jumps
ssh -J jump1,jump2 user@internal-server
```

### Local Port Forward (access remote service locally)

```bash
# Access remote:80 via localhost:8080
ssh -L 8080:localhost:80 user@host

# Access db-server:5432 via localhost:5432 through jumphost
ssh -L 5432:db-server:5432 user@jumphost
```

### Generate and Deploy Key

```bash
# Generate Ed25519 key (recommended)
ssh-keygen -t ed25519 -C "you@example.com"

# Copy public key to server
ssh-copy-id user@host
```

---

## Essential Commands

| Task | Command |
|------|---------|
| Connect | `ssh user@host` |
| Connect on port | `ssh -p 2222 user@host` |
| Connect with key | `ssh -i ~/.ssh/key user@host` |
| Run remote command | `ssh user@host "command"` |
| Interactive remote | `ssh -t user@host "htop"` |
| Copy to remote | `scp file.txt user@host:/path/` |
| Copy from remote | `scp user@host:/path/file.txt ./` |
| Sync to remote | `rsync -avzP ./local/ user@host:/remote/` |
| Local forward | `ssh -L local:remote:port user@host` |
| Remote forward | `ssh -R remote:local:port user@host` |
| SOCKS proxy | `ssh -D 1080 user@host` |
| Jump host | `ssh -J bastion user@internal` |
| Generate key | `ssh-keygen -t ed25519` |
| Copy key to server | `ssh-copy-id user@host` |
| Debug connection | `ssh -vvv user@host` |

---

## SSH Config

Location: `~/.ssh/config`

```
Host myserver
    HostName 192.168.1.100
    User deploy
    Port 22
    IdentityFile ~/.ssh/myserver_key
    ForwardAgent yes

Host internal
    HostName 10.0.0.50
    User deploy
    ProxyJump bastion
```

Then connect with just: `ssh myserver`

### Connection Multiplexing (faster reconnects)

```
Host *
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600
```

```bash
mkdir -p ~/.ssh/sockets
```

---

## SSH Agent

```bash
# Start agent
eval "$(ssh-agent -s)"

# Add key
ssh-add ~/.ssh/id_ed25519

# Add with macOS keychain
ssh-add --apple-use-keychain ~/.ssh/id_ed25519

# List loaded keys
ssh-add -l
```

---

## Security Tips

- Use Ed25519 keys (faster, more secure than RSA)
- Set `PasswordAuthentication no` on servers
- Keep keys encrypted with passphrases
- Use `ssh-agent` to avoid typing passphrase repeatedly
- Restrict key usage with `command=` in authorized_keys

---

## AGENTS.md Blurb

Copy this to your project's AGENTS.md:

```markdown
### SSH Access

SSH is configured for these servers:

- **Production:** `ssh prod` (via ~/.ssh/config)
- **Staging:** `ssh staging`

Common operations:

\`\`\`bash
ssh prod "cd /app && git status"      # Check deploy status
rsync -avzP ./dist/ prod:/app/dist/   # Sync files
ssh -L 5432:localhost:5432 prod       # DB tunnel
\`\`\`

Keys: `~/.ssh/id_ed25519` (add with `ssh-add`)
```

---

## References

| Topic | Reference |
|-------|-----------|
| Full command reference | [COMMANDS.md](references/COMMANDS.md) |
| Port forwarding details | [TUNNELS.md](references/TUNNELS.md) |
| Key management | [KEYS.md](references/KEYS.md) |
