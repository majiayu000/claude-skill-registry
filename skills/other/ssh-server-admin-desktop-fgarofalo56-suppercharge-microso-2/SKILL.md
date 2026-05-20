---
name: ssh-server-admin-desktop
description: Securely connect to and manage remote Linux/Unix servers via SSH. Execute commands, transfer files (SCP/SFTP), set up port forwarding and tunnels. Use when the user asks to SSH into a server, connect to a remote machine, run remote commands, upload/download files to servers, set up tunnels, or perform server administration tasks. Works on Windows, macOS, and Linux.
---

# SSH Server Administration

A comprehensive skill for secure remote server management via SSH. Supports command execution, file transfers, port forwarding, and tunneling. **Cross-platform compatible: Windows, macOS, and Linux.**

## Platform Detection

**CRITICAL: Detect the operating system first to use the correct SSH approach.**

Before executing SSH commands, check the platform:
- **Windows**: Use PowerShell or Windows OpenSSH (built into Windows 10+)
- **macOS/Linux**: Use standard bash SSH commands

## Authentication Methods (In Order of Preference)

### 1. SSH Key Authentication (RECOMMENDED - Works Everywhere)

SSH keys are the most secure and reliable method. They work identically on all platforms.

**Check for existing keys:**
```bash
# Windows (PowerShell)
Get-ChildItem ~/.ssh/id_*.pub

# macOS/Linux
ls -la ~/.ssh/id_*.pub
```

**If keys exist, use them:**
```bash
# All platforms - key auth is automatic if keys are set up
ssh -o StrictHostKeyChecking=accept-new [username]@[host] "[command]"
```

**If no keys exist, help user create them:**
```bash
# All platforms (works in PowerShell, bash, zsh)
ssh-keygen -t ed25519 -C "user@example.com"

# Copy public key to server (if ssh-copy-id available)
ssh-copy-id -i ~/.ssh/id_ed25519.pub [username]@[host]

# Or manually append to server's authorized_keys
cat ~/.ssh/id_ed25519.pub | ssh [username]@[host] "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### 2. Password Authentication

**IMPORTANT: Password auth handling differs by platform.**

#### Windows Approach

Windows OpenSSH doesn't support `sshpass`. Use one of these methods:

**Option A: Use the included Python SSH helper (RECOMMENDED)**
```powershell
# Uses paramiko library for cross-platform SSH
python scripts/ssh_helper.py --host [host] --user [username] --password [password] --command "[command]"
```

**Option B: Interactive SSH (user types password)**
```powershell
# This will prompt for password interactively
ssh -o StrictHostKeyChecking=accept-new [username]@[host] "[command]"
```

**Option C: Use PuTTY's plink (if installed)**
```powershell
# plink can accept password via echo (less secure)
echo [password] | plink -ssh -pw [password] [username]@[host] "[command]"
```

#### macOS/Linux Approach

**Option A: Use sshpass (if available)**
```bash
# Check if sshpass is installed
which sshpass

# If installed, use it
sshpass -p '[password]' ssh -o StrictHostKeyChecking=accept-new [username]@[host] "[command]"
```

**Option B: Use the Python SSH helper**
```bash
python3 scripts/ssh_helper.py --host [host] --user [username] --password [password] --command "[command]"
```

**Option C: Install sshpass**
```bash
# Ubuntu/Debian
sudo apt-get install sshpass

# macOS (with Homebrew)
brew install hudochenkov/sshpass/sshpass

# Then use sshpass commands
```

---

## Session Credential Management

**CRITICAL: One-Time Credential Collection**

When the user first requests an SSH operation, collect credentials ONCE:

```
I need SSH connection details. Please provide:

1. **Host/IP Address**: (e.g., 192.168.1.100 or server.example.com)
2. **Username**: (e.g., root, admin, ubuntu)
3. **Authentication Method**:
   - SSH Key (recommended) - just provide path if not default
   - Password
4. **Port** (optional): Default is 22

Example response:
- Host: 192.168.1.100
- Username: admin
- Auth: SSH Key (default location) OR Password: mypassword123
- Port: 22
```

After receiving credentials:
- Store them in working memory for the session
- Detect the operating system and choose appropriate SSH method
- Use credentials for ALL subsequent operations without re-prompting
- NEVER write credentials to files or logs

---

## Cross-Platform Command Reference

### Remote Command Execution

**With SSH Keys (All Platforms):**
```bash
ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=30 [username]@[host] "[command]"
```

**With Password (Platform-Specific):**

```bash
# macOS/Linux with sshpass
sshpass -p '[password]' ssh -o StrictHostKeyChecking=accept-new [username]@[host] "[command]"

# All platforms with Python helper
python scripts/ssh_helper.py --host [host] --user [username] --password "[password]" --command "[command]"
```

### File Transfer (SCP)

**Upload file:**
```bash
# With keys (all platforms)
scp -o StrictHostKeyChecking=accept-new [local_file] [username]@[host]:[remote_path]

# With password (macOS/Linux)
sshpass -p '[password]' scp -o StrictHostKeyChecking=accept-new [local_file] [username]@[host]:[remote_path]

# With Python helper (all platforms)
python scripts/ssh_helper.py --host [host] --user [username] --password "[password]" --upload [local_file] --remote-path [remote_path]
```

**Download file:**
```bash
# With keys (all platforms)
scp -o StrictHostKeyChecking=accept-new [username]@[host]:[remote_file] [local_path]

# With password (macOS/Linux)
sshpass -p '[password]' scp -o StrictHostKeyChecking=accept-new [username]@[host]:[remote_file] [local_path]

# With Python helper (all platforms)
python scripts/ssh_helper.py --host [host] --user [username] --password "[password]" --download [remote_file] --local-path [local_path]
```

### Port Forwarding

**Local Port Forwarding (-L):**
```bash
# Access remote service on local port (all platforms with keys)
ssh -L [local_port]:localhost:[remote_port] [username]@[host]

# Example: Access remote MySQL (3306) on local port 3307
ssh -L 3307:localhost:3306 [username]@[host]
```

**Remote Port Forwarding (-R):**
```bash
# Expose local service to remote (all platforms with keys)
ssh -R [remote_port]:localhost:[local_port] [username]@[host]
```

**Dynamic Port Forwarding (SOCKS Proxy):**
```bash
ssh -D [local_port] [username]@[host]
```

---

## Server Administration Tasks

### System Information
```bash
# Check system info
ssh user@host "uname -a && cat /etc/os-release"

# Check disk space
ssh user@host "df -h"

# Check memory usage
ssh user@host "free -h"

# Check running processes
ssh user@host "ps aux --sort=-%mem | head -20"

# Check system load
ssh user@host "uptime && top -bn1 | head -15"
```

### Service Management (systemd)
```bash
# Check service status
ssh user@host "systemctl status [service_name]"

# Start/stop/restart service
ssh user@host "sudo systemctl start|stop|restart [service_name]"

# View service logs
ssh user@host "journalctl -u [service_name] -n 50 --no-pager"
```

### Log Analysis
```bash
# View recent system logs
ssh user@host "sudo tail -100 /var/log/syslog"

# Search logs for errors
ssh user@host "sudo grep -i error /var/log/syslog | tail -50"

# View auth logs
ssh user@host "sudo tail -50 /var/log/auth.log"
```

### Network Diagnostics
```bash
# Check listening ports
ssh user@host "ss -tulpn"

# Check network connections
ssh user@host "netstat -an | grep ESTABLISHED"

# Test connectivity
ssh user@host "ping -c 3 [target] && traceroute [target]"
```

---

## Instructions for Claude

1. **Detect Platform First**: Check if running on Windows, macOS, or Linux to choose the right SSH approach.

2. **Prefer SSH Keys**: Always check for and recommend SSH key authentication first.

3. **First SSH Request**: Prompt for credentials using the format above. Wait for response before proceeding.

4. **Store Credentials**: Remember credentials for the entire session. DO NOT ask again.

5. **Choose Correct Method**:
   - If SSH keys are available → Use standard SSH commands
   - If password auth on Windows → Use Python helper script or prompt user
   - If password auth on macOS/Linux → Try sshpass, fall back to Python helper

6. **Handle Errors**: If authentication fails, inform user and suggest alternatives:
   - Set up SSH keys
   - Install sshpass (macOS/Linux)
   - Use the Python helper script

7. **Security First**:
   - Never echo passwords in command output
   - Use `-o StrictHostKeyChecking=accept-new` for first connections
   - Recommend SSH keys over passwords

8. **Custom Port**: Add `-p [port]` to SSH/SFTP or `-P [port]` to SCP commands.

---

## Configuration Options

| Option | SSH Flag | Description |
|--------|----------|-------------|
| Custom port | `-p [port]` | Non-standard SSH port |
| Timeout | `-o ConnectTimeout=[sec]` | Connection timeout |
| Compression | `-C` | Enable compression |
| Verbose | `-v` or `-vv` | Debug output |
| Identity file | `-i [path]` | Specific SSH key |
| Batch mode | `-o BatchMode=yes` | Fail instead of prompting |

---

## Troubleshooting

| Issue | Platform | Solution |
|-------|----------|----------|
| `sshpass: command not found` | Windows | Use Python helper or set up SSH keys |
| `sshpass: command not found` | macOS | `brew install hudochenkov/sshpass/sshpass` |
| `sshpass: command not found` | Linux | `apt install sshpass` or `yum install sshpass` |
| Permission denied | All | Check username/password/key, verify server allows auth method |
| Connection refused | All | Verify host/port, check if SSH service running |
| Host key changed | All | Server reinstalled - verify and update known_hosts |
| Connection timeout | All | Check network, firewall rules |
| `paramiko` not found | All | `pip install paramiko` for Python helper |

---

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

---

## Examples

### Example 1: First Connection with Keys
**User:** "SSH into my server and check disk space"

**Claude:**
1. Prompts for connection details
2. User provides: Host: 10.0.0.5, Username: admin, Auth: SSH Key
3. Executes: `ssh -o StrictHostKeyChecking=accept-new admin@10.0.0.5 "df -h"`
4. Returns disk space information

### Example 2: Windows with Password
**User:** "Connect to 192.168.1.100 with password and restart nginx"

**Claude:**
1. Detects Windows platform
2. Uses Python helper: `python scripts/ssh_helper.py --host 192.168.1.100 --user admin --password "secret" --command "sudo systemctl restart nginx"`
3. Returns result

### Example 3: macOS/Linux with Password
**User:** "SSH to my server with password"

**Claude:**
1. Detects macOS/Linux
2. Checks for sshpass: `which sshpass`
3. If available: `sshpass -p 'password' ssh admin@host "command"`
4. If not: Uses Python helper or suggests installing sshpass

---

## Python Helper Script

The `scripts/ssh_helper.py` provides cross-platform SSH with password authentication.

**Install dependencies:**
```bash
pip install paramiko
```

**Usage:**
```bash
# Run command
python scripts/ssh_helper.py --host 192.168.1.100 --user admin --password "secret" --command "df -h"

# Upload file
python scripts/ssh_helper.py --host 192.168.1.100 --user admin --password "secret" --upload ./local.txt --remote-path /tmp/remote.txt

# Download file
python scripts/ssh_helper.py --host 192.168.1.100 --user admin --password "secret" --download /var/log/syslog --local-path ./syslog.txt
```

See `scripts/ssh_helper.py` for full implementation.

---

## Version History

- v2.0.0 (2025-12-17): Cross-platform rewrite - Windows, macOS, Linux support
- v1.0.0 (2025-12-17): Initial release
