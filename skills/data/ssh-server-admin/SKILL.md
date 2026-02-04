---
name: ssh-server-admin
description: Securely connect to and manage remote Linux/Unix servers via SSH. Execute commands, transfer files (SCP/SFTP), set up port forwarding and tunnels. Use when the user asks to SSH into a server, connect to a remote machine, run remote commands, upload/download files to servers, set up tunnels, or perform server administration tasks. Works on Windows, macOS, and Linux.
---

# SSH Server Administration

Comprehensive skill for secure remote server management via SSH. Cross-platform compatible: Windows, macOS, and Linux.

## Platform Detection

**Detect the operating system first to use the correct SSH approach:**

- **Windows**: Use PowerShell or Windows OpenSSH (built into Windows 10+)
- **macOS/Linux**: Use standard bash SSH commands

## Authentication Methods

### 1. SSH Key Authentication (Recommended)

**Check for existing keys:**

```bash
# Windows (PowerShell)
Get-ChildItem ~/.ssh/id_*.pub

# macOS/Linux
ls -la ~/.ssh/id_*.pub
```

**If keys exist, use them:**

```bash
ssh -o StrictHostKeyChecking=accept-new [username]@[host] "[command]"
```

**If no keys exist, create them:**

```bash
# All platforms
ssh-keygen -t ed25519 -C "user@example.com"

# Copy public key to server
ssh-copy-id -i ~/.ssh/id_ed25519.pub [username]@[host]
```

### 2. Password Authentication

**macOS/Linux with sshpass:**

```bash
sshpass -p '[password]' ssh -o StrictHostKeyChecking=accept-new [username]@[host] "[command]"
```

**Windows (Python helper):**

```powershell
python scripts/ssh_helper.py --host [host] --user [username] --password [password] --command "[command]"
```

## Credential Collection

When user first requests SSH operation, collect credentials ONCE:

```
I need SSH connection details:

1. Host/IP Address: (e.g., 192.168.1.100 or server.example.com)
2. Username: (e.g., root, admin, ubuntu)
3. Authentication Method: SSH Key (recommended) or Password
4. Port (optional): Default is 22
```

Store credentials in working memory for the session. NEVER write to files or logs.

## Common Commands

### Remote Command Execution

```bash
ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=30 [username]@[host] "[command]"
```

### File Transfer (SCP)

```bash
# Upload file
scp -o StrictHostKeyChecking=accept-new [local_file] [username]@[host]:[remote_path]

# Download file
scp -o StrictHostKeyChecking=accept-new [username]@[host]:[remote_file] [local_path]
```

### Port Forwarding

```bash
# Local port forwarding (access remote service locally)
ssh -L [local_port]:localhost:[remote_port] [username]@[host]

# Remote port forwarding (expose local service remotely)
ssh -R [remote_port]:localhost:[local_port] [username]@[host]

# Dynamic SOCKS proxy
ssh -D [local_port] [username]@[host]
```

## Server Administration Tasks

### System Information

```bash
ssh user@host "uname -a && cat /etc/os-release"  # System info
ssh user@host "df -h"                             # Disk space
ssh user@host "free -h"                           # Memory usage
ssh user@host "ps aux --sort=-%mem | head -20"    # Top processes
ssh user@host "uptime && top -bn1 | head -15"     # System load
```

### Service Management (systemd)

```bash
ssh user@host "systemctl status [service_name]"
ssh user@host "sudo systemctl start|stop|restart [service_name]"
ssh user@host "journalctl -u [service_name] -n 50 --no-pager"
```

### Log Analysis

```bash
ssh user@host "sudo tail -100 /var/log/syslog"
ssh user@host "sudo grep -i error /var/log/syslog | tail -50"
ssh user@host "sudo tail -50 /var/log/auth.log"
```

### Network Diagnostics

```bash
ssh user@host "ss -tulpn"                          # Listening ports
ssh user@host "netstat -an | grep ESTABLISHED"     # Active connections
ssh user@host "ping -c 3 [target] && traceroute [target]"
```

## Configuration Options

| Option | SSH Flag | Description |
|--------|----------|-------------|
| Custom port | `-p [port]` | Non-standard SSH port |
| Timeout | `-o ConnectTimeout=[sec]` | Connection timeout |
| Compression | `-C` | Enable compression |
| Verbose | `-v` or `-vv` | Debug output |
| Identity file | `-i [path]` | Specific SSH key |
| Batch mode | `-o BatchMode=yes` | Fail instead of prompting |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `sshpass: command not found` (Windows) | Use Python helper or set up SSH keys |
| `sshpass: command not found` (macOS) | `brew install hudochenkov/sshpass/sshpass` |
| `sshpass: command not found` (Linux) | `apt install sshpass` or `yum install sshpass` |
| Permission denied | Check username/password/key, verify auth method |
| Connection refused | Verify host/port, check if SSH service running |
| Host key changed | Server reinstalled - verify and update known_hosts |
| Connection timeout | Check network, firewall rules |

## When to Use This Skill

- "SSH into my server at 192.168.1.100"
- "Connect to my remote machine"
- "Run a command on the server"
- "Upload/download files to/from the server"
- "Set up port forwarding"
- "Create an SSH tunnel"
- "Check server status"
- "Restart a service on the server"
- "View server logs"

## When NOT to Use This Skill

- Local file operations (no SSH needed)
- Cloud provider API operations (use their CLIs)
- Database client connections (use database tools)

## Security Best Practices

1. **Prefer SSH keys** over passwords
2. **Never echo passwords** in command output
3. **Use StrictHostKeyChecking** appropriately
4. **Limit key permissions** - `chmod 600 ~/.ssh/id_*`
5. **Use agent forwarding** carefully - `-A` flag
