---
name: ssh
description: "SSH remote access patterns and utilities. Connect to servers, manage keys, tunnels, and transfers."
---

# SSH Skill

Use SSH for secure remote access, file transfers, and tunneling.

## Basic Connection

Connect to server:
```bash
ssh user@hostname
```

Connect on specific port:
```bash
ssh -p 2222 user@hostname
```

Connect with specific identity:
```bash
ssh -i ~/.ssh/my_key user@hostname
```

## SSH Config

Config file location:
```
~/.ssh/config
```

Example config entry:
```
Host myserver
    HostName 192.168.1.100
    User deploy
    Port 22
    IdentityFile ~/.ssh/myserver_key
    ForwardAgent yes
```

Then connect with just:
```bash
ssh myserver
```

## Running Remote Commands

Execute single command:
```bash
ssh user@host "ls -la /var/log"
```

Execute multiple commands:
```bash
ssh user@host "cd /app && git pull && pm2 restart all"
```

Run with pseudo-terminal (for interactive):
```bash
ssh -t user@host "htop"
```

## File Transfer with SCP

Copy file to remote:
```bash
scp local.txt user@host:/remote/path/
```

Copy file from remote:
```bash
scp user@host:/remote/file.txt ./local/
```

Copy directory recursively:
```bash
scp -r ./local_dir user@host:/remote/path/
```

## File Transfer with rsync (preferred)

Sync directory to remote:
```bash
rsync -avz ./local/ user@host:/remote/path/
```

Sync from remote:
```bash
rsync -avz user@host:/remote/path/ ./local/
```

With progress and compression:
```bash
rsync -avzP ./local/ user@host:/remote/path/
```

Dry run first:
```bash
rsync -avzn ./local/ user@host:/remote/path/
```

## Port Forwarding (Tunnels)

Local forward (access remote service locally):
```bash
ssh -L 8080:localhost:80 user@host
# Now localhost:8080 connects to host's port 80
```

Local forward to another host:
```bash
ssh -L 5432:db-server:5432 user@jumphost
# Access db-server:5432 via localhost:5432
```

Remote forward (expose local service to remote):
```bash
ssh -R 9000:localhost:3000 user@host
# Remote's port 9000 connects to your local 3000
```

Dynamic SOCKS proxy:
```bash
ssh -D 1080 user@host
# Use localhost:1080 as SOCKS5 proxy
```

## Jump Hosts / Bastion

Connect through jump host:
```bash
ssh -J jumphost user@internal-server
```

Multiple jumps:
```bash
ssh -J jump1,jump2 user@internal-server
```

In config file:
```
Host internal
    HostName 10.0.0.50
    User deploy
    ProxyJump bastion
```

## Key Management

Generate new key (Ed25519, recommended):
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Generate RSA key (legacy compatibility):
```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

Copy public key to server:
```bash
ssh-copy-id user@host
```

Copy specific key:
```bash
ssh-copy-id -i ~/.ssh/mykey.pub user@host
```

## SSH Agent

Start agent:
```bash
eval "$(ssh-agent -s)"
```

Add key to agent:
```bash
ssh-add ~/.ssh/id_ed25519
```

Add with macOS keychain:
```bash
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

List loaded keys:
```bash
ssh-add -l
```

## Multiplexing (Connection Sharing)

In ~/.ssh/config:
```
Host *
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600
```

Create socket directory:
```bash
mkdir -p ~/.ssh/sockets
```

## Known Hosts

Remove old host key:
```bash
ssh-keygen -R hostname
```

Scan and add host key:
```bash
ssh-keyscan hostname >> ~/.ssh/known_hosts
```

## Debugging

Verbose output:
```bash
ssh -v user@host
```

Very verbose:
```bash
ssh -vv user@host
```

Maximum verbosity:
```bash
ssh -vvv user@host
```

## Security Tips

- Use Ed25519 keys (faster, more secure than RSA)
- Set `PasswordAuthentication no` on servers
- Use `fail2ban` on servers to block brute force
- Keep keys encrypted with passphrases
- Use `ssh-agent` to avoid typing passphrase repeatedly
- Restrict key usage with `command=` in authorized_keys
