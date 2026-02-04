---
name: Nawin
description: 9P2000 protocol implementation for .NET - connect to 9front/Plan9, serve files, CPU remote shell, authentication servers
---

# Nawin

Nawin is a .NET 9 implementation of the 9P2000 protocol for connecting Windows/Linux systems to 9front (Plan 9) file servers. It provides clients, servers, authentication, and CPU remote shell capabilities.

## Instructions

When helping users with Nawin, follow these guidelines:

1. **Project Location**: The codebase is at `/home/matt/Git/Nawin`
2. **Running Tools**: Use `dotnet run --project Nawin.<Project>` to run tools
3. **Privileged Ports**: Port 564 requires root. Use `sudo $(which dotnet) run` or use a high port like 5640
4. **Authentication**: Support for `none`, `simple:user:pass`, `p9sk1` (Plan 9), and `dp9ik` (9front modern)
5. **9front Testing**: CPU into 9front using the auth server at localhost:17019

## Available Tools

| Project | Purpose | Default Port |
|---------|---------|--------------|
| Nawin.Cli | Interactive 9P client (ls, cat, mount, copy) | connects to 564 |
| Nawin.Serve | Serve local directories over 9P (U9FS replacement) | 564 |
| Nawin.Cpu | CPU client - remote shell with namespace export | 17010 |
| Nawin.CpuServer | Accept inbound CPU connections | 17010 |
| Nawin.Auth | Authentication server (p9sk1/dp9ik) | 567 |
| Nawin.Jerq | Graphics app with /dev/draw export | N/A |

## Examples

### Example 1: Serve a Directory (U9FS Replacement)
```
User: How do I share a directory over 9P?

Claude: Use Nawin.Serve to expose a local directory:

# Serve current directory on high port (no root needed)
dotnet run --project Nawin.Serve -- -p 5640 .

# Serve with simple auth
dotnet run --project Nawin.Serve -- -p 5640 --auth simple:matt:secret /home/matt/share

# On port 564 (requires root)
sudo $(which dotnet) run --project Nawin.Serve -- /home/matt/share
```

### Example 2: Connect to 9front
```
User: How do I list files on a 9front server?

Claude: Use Nawin.Cli with dp9ik auth:

dotnet run --project Nawin.Cli -- -H 9front.local -u glenda -p password -a dp9ik ls /

# Read a file
dotnet run --project Nawin.Cli -- -H 9front.local -u glenda -p password -a dp9ik cat /lib/motd

# Copy file from remote
dotnet run --project Nawin.Cli -- -H 9front.local -u glenda -p password -a dp9ik cp :/etc/profile ./profile
```

### Example 3: CPU into 9front
```
User: How do I get a remote shell on 9front?

Claude: Use Nawin.Cpu for Plan 9 style CPU connection:

# Interactive shell
dotnet run --project Nawin.Cpu -- --host 9front.local --user glenda --password secret --protocol dp9ik

# Run a command
dotnet run --project Nawin.Cpu -- --host 9front.local -u glenda -P secret --protocol dp9ik "cat /dev/sysname"

# With local auth server (p9sk1)
dotnet run --project Nawin.Cpu -- --host localhost --port 17019 --user glenda --password test1234 --protocol p9sk1 "echo hello"
```

### Example 4: Run the Auth Server
```
User: How do I start the authentication server?

Claude: Nawin.Auth runs as a systemd service or manually:

# Check status
systemctl status nawin-auth

# Restart
sudo systemctl restart nawin-auth && sleep 2 && systemctl status nawin-auth 2>&1 | head -15

# Run manually
dotnet run --project Nawin.Auth -- serve --port 567 --authdom mydom --keys ~/.nawin/keys

# Manage users
dotnet run --project Nawin.Auth -- adduser glenda
dotnet run --project Nawin.Auth -- listusers
```

### Example 5: Mount Remote Filesystem
```
User: Can I mount a 9P filesystem locally?

Claude: Yes, Nawin.Cli supports mounting via FUSE (Linux) or ProjFS (Windows):

# Linux (FUSE) - runs in foreground with -f
dotnet run --project Nawin.Cli -- -H 9front.local -u glenda -a dp9ik mount -f /mnt/9front

# Windows (ProjFS)
dotnet run --project Nawin.Cli -- -H 9front.local -u glenda -a dp9ik mount C:\9front
```

---

# Reference Implementation Details

## Project Structure

```
Nawin/
├── Nawin.Protocol/     # Wire format, message serialization, Qid/Stat types
├── Nawin.Transport/    # TCP connection, tag multiplexing
├── Nawin.Client/       # High-level client API, sessions, file handles
├── Nawin.Server/       # Server-side: listener, file tree interface
├── Nawin.Auth/         # p9sk1 and dp9ik authentication
├── Nawin.Cli/          # Command-line client
├── Nawin.Cpu/          # CPU client (rcpu equivalent)
├── Nawin.CpuServer/    # CPU server
├── Nawin.Serve/        # File server (U9FS replacement)
├── Nawin.Jerq/         # Graphics with /dev/draw export
├── Nawin.Mount.Linux/  # FUSE integration
├── Nawin.Mount.Windows/# ProjFS integration
└── Nawin.Tests/        # Unit and integration tests
```

## Authentication Protocols

| Protocol | Description | Use Case |
|----------|-------------|----------|
| `none` | No authentication | Trusted networks |
| `simple` | Username/password (plaintext) | Simple setups |
| `p9sk1` | DES-based Plan 9 auth | Original Plan 9 |
| `dp9ik` | ChaCha20-Poly1305 + PBKDF2 | Modern 9front |

## Nawin.Serve Options

```bash
dotnet run --project Nawin.Serve -- [options] <directory>

Options:
  -p, --port <port>      Port to listen on (default: 564)
  -a, --address <addr>   Address to bind (default: 0.0.0.0)
  --auth <type>          Auth: none, simple:user:pass (default: none)
```

## Nawin.Cli Options

```bash
dotnet run --project Nawin.Cli -- [options] <command> [args]

Options:
  -H, --host <host>      Server hostname (default: localhost)
  -P, --port <port>      Server port (default: 564)
  -u, --user <user>      Username
  -p, --password <pass>  Password
  -a, --auth <type>      Auth: none, simple, p9sk1, dp9ik
  --authserver <h:p>     Auth server for p9sk1/dp9ik
  --aname <name>         Attach name (file tree)

Commands:
  ls [-l] <path>         List directory
  cat <path>             Read file
  write <path> <text>    Write to file
  stat <path>            Show file metadata
  mkdir <path>           Create directory
  rm <path>              Remove file/directory
  cp [-r] <src> <dst>    Copy (: prefix for remote)
  mount [-f] <path>      Mount filesystem
  shell                  Interactive shell
```

## Nawin.Cpu Options

```bash
dotnet run --project Nawin.Cpu -- [options] [command]

Options:
  --host <host>          CPU server hostname
  --port <port>          CPU server port (default: 17010)
  -u, --user <user>      Username
  -P, --password <pass>  Password
  --protocol <proto>     Auth: p9sk1, dp9ik
  -e, --export <dir>     Export local directory to remote
  --jerq                 Enable graphics mode
```

## Testing with 9front

The local 9front VM (barn) can be started with:
```bash
/opt/isos/9front.sh
```

9front source code is available at:
```bash
/mnt/  # When /opt/isos/9front-11321.amd64.iso is mounted
```

CPU into 9front with local auth server:
```bash
dotnet run --project Nawin.Cpu -- --host localhost --port 17019 --user glenda --password test1234 --protocol p9sk1 "command"
```

## Troubleshooting

### "dotnet: command not found" with sudo

```bash
# Use full path
sudo $(which dotnet) run --project Nawin.Serve

# Or preserve PATH
sudo env "PATH=$PATH" dotnet run --project Nawin.Serve
```

### Permission denied on port 564

Use a high port or grant capability:
```bash
# Option 1: Use high port
dotnet run --project Nawin.Serve -- -p 5640 .

# Option 2: Grant capability to published binary
dotnet publish -c Release Nawin.Serve
sudo setcap 'cap_net_bind_service=+ep' ./Nawin.Serve/bin/Release/net9.0/publish/Nawin.Serve
```

### Auth server not running

```bash
sudo systemctl restart nawin-auth && sleep 2 && systemctl status nawin-auth 2>&1 | head -15
```
