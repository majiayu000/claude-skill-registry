---
name: administering-linux
description: Manage Linux systems covering systemd services, process management, filesystems, networking, performance tuning, and troubleshooting. Use when deploying applications, optimizing server performance, diagnosing production issues, or managing users and security on Linux servers.
---

# Linux Administration

Comprehensive Linux system administration for managing servers, deploying applications, and troubleshooting production issues in modern cloud-native environments.

## Purpose

This skill teaches fundamental and intermediate Linux administration for DevOps engineers, SREs, backend developers, and platform engineers. Focus on systemd-based distributions (Ubuntu, RHEL, Debian, Fedora) covering service management, process monitoring, filesystem operations, user administration, performance tuning, log analysis, and network configuration.

Modern infrastructure requires solid Linux fundamentals even with containerization. Container hosts run Linux, Kubernetes nodes need optimization, and troubleshooting production issues requires understanding systemd, processes, and logs.

**Not Covered:**
- Advanced networking (BGP, OSPF) - see `network-architecture` skill
- Deep security hardening (compliance, pentesting) - see `security-hardening` skill
- Configuration management at scale (Ansible, Puppet) - see `configuration-management` skill
- Container orchestration - see `kubernetes-operations` skill

## When to Use This Skill

Use when deploying custom applications, troubleshooting slow systems, investigating service failures, optimizing workloads, managing users, configuring SSH, monitoring disk space, scheduling tasks, diagnosing network issues, or applying performance tuning.

## Quick Start

### Essential Commands

**Service Management:**
```bash
systemctl start nginx              # Start service
systemctl stop nginx               # Stop service
systemctl restart nginx            # Restart service
systemctl status nginx             # Check status
systemctl enable nginx             # Enable at boot
journalctl -u nginx -f             # Follow service logs
```

**Process Monitoring:**
```bash
top                                # Interactive process monitor
htop                               # Enhanced process monitor
ps aux | grep process_name         # Find specific process
kill -15 PID                       # Graceful shutdown (SIGTERM)
kill -9 PID                        # Force kill (SIGKILL)
```

**Disk Usage:**
```bash
df -h                              # Filesystem usage
du -sh /path/to/dir                # Directory size
ncdu /path                         # Interactive disk analyzer
```

**Log Analysis:**
```bash
journalctl -f                      # Follow all logs
journalctl -u service -f           # Follow service logs
journalctl --since "1 hour ago"    # Filter by time
journalctl -p err                  # Show errors only
```

**User Management:**
```bash
useradd -m -s /bin/bash username   # Create user with home dir
passwd username                    # Set password
usermod -aG sudo username          # Add to sudo group
userdel -r username                # Delete user and home dir
```

## Core Concepts

### Systemd Architecture

Systemd is the standard init system and service manager. Systemd units define services, timers, targets, and other system resources.

**Unit File Locations (priority order):**
- `/etc/systemd/system/` - Custom units (highest priority)
- `/run/systemd/system/` - Runtime units (transient)
- `/lib/systemd/system/` - System-provided units (don't modify)

**Key Unit Types:** `.service` (services), `.timer` (scheduled tasks), `.target` (unit groups), `.socket` (socket-activated)

**Essential systemctl Commands:**
```bash
systemctl daemon-reload            # Reload unit files after changes
systemctl list-units --type=service
systemctl list-timers              # Show all timers
systemctl cat nginx.service        # Show unit file content
systemctl edit nginx.service       # Create override file
```

For detailed systemd reference, see `references/systemd-guide.md`.

### Process Management

Processes are running programs with unique PIDs. Understanding process states, signals, and resource usage is essential for troubleshooting.

**Process States:** R (running), S (sleeping), D (uninterruptible sleep/I/O), Z (zombie), T (stopped)

**Common Signals:** SIGTERM (15) graceful, SIGKILL (9) force, SIGHUP (1) reload config

**Process Priority:**
```bash
nice -n 10 command                 # Start with lower priority
renice -n 5 -p PID                 # Change priority of running process
```

### Filesystem Hierarchy

Essential directories: `/` (root), `/etc/` (config), `/var/` (variable data), `/opt/` (optional software), `/usr/` (user programs), `/home/` (user directories), `/tmp/` (temporary), `/boot/` (boot loader)

**Filesystem Types Quick Reference:**
- **ext4** - General purpose (default)
- **XFS** - Large files, databases (RHEL default)
- **Btrfs** - Snapshots, copy-on-write
- **ZFS** - Enterprise, data integrity, NAS

For filesystem management details including LVM and RAID, see `references/filesystem-management.md`.

### Package Management

**Ubuntu/Debian (apt):**
```bash
apt update && apt upgrade          # Update system
apt install package                # Install package
apt remove package                 # Remove package
apt search keyword                 # Search packages
```

**RHEL/CentOS/Fedora (dnf):**
```bash
dnf update                         # Update all packages
dnf install package                # Install package
dnf remove package                 # Remove package
dnf search keyword                 # Search packages
```

Use native package managers for system services; snap/flatpak for desktop apps and cross-distro compatibility.

## Decision Frameworks

### Troubleshooting Performance Issues

**Investigation Workflow:**

1. **Identify bottleneck:**
   ```bash
   top                             # Quick overview
   uptime                          # Load averages
   ```

2. **CPU Issues (usage >80%):**
   ```bash
   top                             # Press Shift+P to sort by CPU
   ps aux --sort=-%cpu | head
   ```

3. **Memory Issues (swap used):**
   ```bash
   free -h                         # Memory usage
   top                             # Press Shift+M to sort by memory
   ```

4. **Disk I/O Issues (high wa%):**
   ```bash
   iostat -x 1                     # Disk statistics
   iotop                           # I/O by process
   ```

5. **Network Issues:**
   ```bash
   ss -tunap                       # Active connections
   iftop                           # Bandwidth monitor
   ```

For comprehensive troubleshooting, see `references/troubleshooting-guide.md`.

### Filesystem Selection

**Quick Decision:**
- **Default/General** → ext4
- **Database servers** → XFS
- **Large file storage** → XFS or ZFS
- **NAS/File server** → ZFS
- **Need snapshots** → Btrfs or ZFS

## Common Workflows

### Creating a Systemd Service

**Step 1: Create unit file**
```bash
sudo nano /etc/systemd/system/myapp.service
```

**Step 2: Unit file content**
```ini
[Unit]
Description=My Web Application
After=network.target postgresql.service
Requires=postgresql.service

[Service]
Type=simple
User=myapp
Group=myapp
WorkingDirectory=/opt/myapp
Environment="PORT=8080"
ExecStart=/opt/myapp/bin/server
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5s
StandardOutput=journal

# Security hardening
PrivateTmp=true
NoNewPrivileges=true
ProtectSystem=strict
ReadWritePaths=/var/lib/myapp

[Install]
WantedBy=multi-user.target
```

**Step 3: Deploy and start**
```bash
sudo useradd -r -s /bin/false myapp
sudo mkdir -p /var/lib/myapp
sudo chown myapp:myapp /var/lib/myapp
sudo systemctl daemon-reload
sudo systemctl enable myapp.service
sudo systemctl start myapp.service
sudo systemctl status myapp.service
```

For complete examples, see `examples/systemd-units/`.

### Systemd Timer (Cron Replacement)

Create service and timer units for scheduled tasks. Timer unit specifies `OnCalendar=` schedule and `Persistent=true` for missed jobs. Service unit has `Type=oneshot`. See `examples/systemd-units/backup.timer` and `backup.service` for complete examples.

### SSH Hardening

**Generate SSH key:**
```bash
ssh-keygen -t ed25519 -C "admin@example.com"
ssh-copy-id admin@server
```

**Harden sshd_config:**
```bash
sudo nano /etc/ssh/sshd_config
```

Key settings:
```bash
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
AllowUsers admin deploy
X11Forwarding no
Port 2222                          # Optional
```

**Apply changes:**
```bash
sudo sshd -t                       # Test
sudo systemctl restart sshd        # Apply (keep backup session!)
```

For complete SSH configuration, see `examples/configs/sshd_config.hardened` and `references/security-hardening.md`.

### Performance Tuning

Configure sysctl parameters in `/etc/sysctl.d/99-custom.conf` for network tuning (tcp buffers, BBR congestion control), memory management (swappiness, cache pressure), and file descriptors. Set ulimits in `/etc/security/limits.conf` for nofile and nproc. Configure I/O schedulers and CPU governors. For comprehensive tuning, see `references/performance-tuning.md` and `examples/configs/` for templates.

### Log Investigation

Use `systemctl status myapp` and `journalctl -u myapp` to investigate issues. Filter logs by time `--since`, severity `-p err`, or search patterns with `grep`. Correlate with system metrics using `top`, `df -h`, `free -h`. Check for OOM kills with `journalctl -k | grep -i oom`. For detailed workflows, see `references/troubleshooting-guide.md`.

### Essential Commands

**Interface Management:**
```bash
ip addr show                       # Show all interfaces
ip link set eth0 up                # Bring interface up
ip addr add 192.168.1.100/24 dev eth0
```

**Routing:**
```bash
ip route show                      # Show routing table
ip route get 8.8.8.8               # Show route to IP
ip route add 10.0.0.0/24 via 192.168.1.1
```

**Socket Statistics:**
```bash
ss -tunap                          # All TCP/UDP connections
ss -tlnp                           # Listening TCP ports
ss -ulnp                           # Listening UDP ports
ss -tnp state established          # Established connections
```

### Firewall Configuration

**Ubuntu (ufw):**
```bash
sudo ufw status
sudo ufw enable
sudo ufw allow 22/tcp              # Allow SSH
sudo ufw allow 80/tcp              # Allow HTTP
sudo ufw allow from 192.168.1.0/24 # Allow from subnet
sudo ufw default deny incoming
```

**RHEL/CentOS (firewalld):**
```bash
firewall-cmd --state
firewall-cmd --list-all
firewall-cmd --add-service=http --permanent
firewall-cmd --add-port=8080/tcp --permanent
firewall-cmd --reload
```

For complete network configuration including netplan, NetworkManager, and DNS, see `references/network-configuration.md`.

## Scheduled Tasks

### Cron Syntax

```bash
crontab -e                         # Edit user crontab

# Format: minute hour day month weekday command
0 2 * * * /usr/local/bin/backup.sh              # Daily at 2:00 AM
*/5 * * * * /usr/local/bin/check-health.sh      # Every 5 minutes
0 3 * * 0 /usr/local/bin/weekly-cleanup.sh      # Weekly Sunday 3 AM
@reboot /usr/local/bin/startup-script.sh        # Run at boot
```

### Systemd Timer Calendar Syntax

```bash
OnCalendar=daily                   # Every day at midnight
OnCalendar=*-*-* 02:00:00          # Daily at 2:00 AM
OnCalendar=Mon *-*-* 09:00:00      # Every Monday at 9 AM
OnCalendar=*-*-01 00:00:00         # 1st of every month
OnBootSec=5min                     # 5 minutes after boot
```

## Essential Tools

### Process Monitoring
- `top`, `htop` - Real-time process monitor
- `ps` - Report process status
- `pgrep/pkill` - Find/kill by name

### Log Analysis
- `journalctl` - Query systemd journal
- `grep` - Search text patterns
- `tail -f` - Follow log files

### Disk Management
- `df` - Disk space usage
- `du` - Directory space usage
- `lsblk` - List block devices
- `ncdu` - Interactive disk analyzer

### Network Tools
- `ip` - Network configuration
- `ss` - Socket statistics
- `ping` - Test connectivity
- `dig/nslookup` - DNS queries
- `tcpdump` - Packet capture

### System Monitoring
- **Netdata** - Real-time web dashboard
- **Prometheus + Grafana** - Metrics collection
- **ELK Stack** - Centralized logging

## Integration with Other Skills

### Kubernetes Operations
Linux administration is the foundation for Kubernetes node management. Node optimization (sysctl tuning), kubelet as systemd service, container logs via journald, cgroups for resource limits.

Example:
```bash
# /etc/sysctl.d/99-kubernetes.conf
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
```

For Kubernetes-specific operations, see `kubernetes-operations` skill.

### Configuration Management
Linux administration provides knowledge; configuration management automates it. Ansible playbooks automate systemd service creation and system tuning.

For automation at scale, see `configuration-management` skill.

### Security Hardening
This skill covers SSH and firewall basics. For advanced security (MFA, certificates, CIS benchmarks, compliance), see `security-hardening` skill.

### CI/CD Pipelines
CI/CD pipelines deploy to Linux servers using these skills. Uses systemctl for deployment and journalctl for monitoring.

For deployment automation, see `building-ci-pipelines` skill.

## Reference Materials

### Detailed Guides
- **`references/systemd-guide.md`** - Comprehensive systemd reference (unit files, dependencies, targets)
- **`references/performance-tuning.md`** - Complete sysctl, ulimits, cgroups, I/O scheduler guide
- **`references/filesystem-management.md`** - LVM, RAID, filesystem types, permissions
- **`references/network-configuration.md`** - ip/ss commands, netplan, NetworkManager, DNS, firewall
- **`references/security-hardening.md`** - SSH hardening, firewall, SELinux/AppArmor basics
- **`references/troubleshooting-guide.md`** - Common issues, diagnostic workflows, solutions

### Examples
- **`examples/systemd-units/`** - Service, timer, and target unit files
- **`examples/scripts/`** - Backup, health check, and maintenance scripts
- **`examples/configs/`** - sshd_config, sysctl.conf, logrotate examples

## Distribution-Specific Notes

### Ubuntu/Debian
Package Manager: `apt`, Network: `netplan`, Firewall: `ufw`, Repositories: `/etc/apt/sources.list`

### RHEL/CentOS/Fedora
Package Manager: `dnf`, Network: `NetworkManager`, Firewall: `firewalld`, Repositories: `/etc/yum.repos.d/`, SELinux enabled by default

### Arch Linux
Package Manager: `pacman`, Network: `NetworkManager`, Rolling release, AUR for community packages

## Additional Resources

**Official Documentation:**
- systemd: https://systemd.io/
- Linux kernel: https://kernel.org/doc/

**Related Skills:**
- `kubernetes-operations` - Container orchestration on Linux
- `configuration-management` - Automate Linux admin at scale
- `security-hardening` - Advanced security and compliance
- `building-ci-pipelines` - Deploy via CI/CD
- `performance-engineering` - Deep performance analysis
