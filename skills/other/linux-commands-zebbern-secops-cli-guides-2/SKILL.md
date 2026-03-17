---
name: Linux Commands Reference
description: This skill should be used when the user asks to "run Linux commands", "manage users and permissions", "configure file systems", "work with LVM", "set up networking", "manage services with systemd", "configure firewalls", "implement SELinux or AppArmor", or "automate tasks with cron". It provides comprehensive Linux command reference for security professionals.
version: 1.0.0
tags: [linux, commands, sysadmin, security, networking, permissions, systemd]
---

# Linux Commands Reference

## Purpose

Master essential Linux commands for system administration, security operations, and penetration testing. This skill covers user management, file permissions, disk management, LVM, networking, firewall configuration, security frameworks (SELinux/AppArmor), and task automation.

## Prerequisites

### Required Environment
- Linux system (Debian/Ubuntu or RHEL-based)
- Terminal access with appropriate privileges
- Root or sudo access for administrative tasks

### Required Knowledge
- Basic command-line navigation
- Understanding of Linux file system hierarchy
- Familiarity with text editors (vim/nano)

## Outputs and Deliverables

1. **System Administration Scripts** - Automated user/group management
2. **Security Configurations** - Firewall rules, SELinux policies
3. **Storage Solutions** - LVM configurations, mounted filesystems
4. **Network Configurations** - Interface settings, firewall rules

## Core Workflow

### Phase 1: General Commands and Navigation

Essential system information commands:

```bash
# Shell and system information
ls -al /bin/sh          # See default shell
uname -a                # All system information
uname -r                # Kernel release
uptime                  # System uptime

# Command location and type
which <command>         # Locate executable
whereis <command>       # Binary, source, and man page
type <command>          # Command type

# User information
who                     # Currently logged in users
id                      # Current user UID, GID, groups

# File information
stat <filename>         # Detailed file info
file <filename>         # File type

# Reading files
less <file>             # Scrollable reading
more <file>             # Page-by-page reading
tail -f <file>          # Follow log files
head -n 20 <file>       # First 20 lines

# Finding commands
man -k <keyword>        # Find command by keyword
```

### Phase 2: User and Group Management

Manage users and groups:

```bash
# User information
getent passwd <user>    # User details from /etc/passwd
getent group <group>    # Group details from /etc/group
groups <username>       # User's groups
id <username>           # UID, GID, and groups

# Create users
useradd <username>                    # Create user
useradd -m -s /bin/bash <username>    # With home dir and shell
useradd -D                            # Show defaults

# Modify users
usermod -l new_name old_name          # Change username
usermod -s /bin/zsh <username>        # Change shell
usermod -aG <group> <username>        # Add to group (preserve others)
usermod -L <username>                 # Lock account
usermod -U <username>                 # Unlock account

# Delete users
userdel <username>                    # Delete user
userdel -r <username>                 # Delete with home directory

# Password management
passwd <username>                     # Set password
chage -l <username>                   # Password aging info
chage -E 2024-12-31 <username>        # Set expiration

# Group management
groupadd <groupname>                  # Create group
groupmod -n new_name old_name         # Rename group
groupdel <groupname>                  # Delete group
gpasswd -a <user> <group>             # Add user to group
gpasswd -d <user> <group>             # Remove user from group

# Change shell
chsh -s /bin/zsh <username>           # Change default shell
```

### Phase 3: File Permissions and ACLs

Manage file access:

```bash
# Standard permissions (rwx = 421)
chmod 755 <file>                      # rwxr-xr-x
chmod 644 <file>                      # rw-r--r--
chmod u+x <file>                      # Add execute for owner
chmod g+w <file>                      # Add write for group
chmod o-rwx <file>                    # Remove all for others
chmod u=rw,g=r,o= <file>              # Explicit assignment

# Ownership
chown <user>:<group> <file>           # Change owner and group
chown -R <user>:<group> <dir>         # Recursive ownership
chgrp <group> <file>                  # Change group only

# Access Control Lists (ACL)
getfacl <file>                        # View ACL
setfacl -m u:<user>:rw <file>         # Add user permission
setfacl -m g:<group>:r <file>         # Add group permission
setfacl -x u:<user> <file>            # Remove user ACL
setfacl -b <file>                     # Remove all ACLs
setfacl -d -m u:<user>:rw <dir>       # Default ACL for new files

# Umask (default permission mask)
umask                                 # Show current umask
umask 027                             # Set umask (750 for dirs, 640 for files)
```

Umask values (subtract from 777/666):
- 0: rwx (read, write, execute)
- 7: no permissions

### Phase 4: Disk and Filesystem Management

Manage storage:

```bash
# View devices and partitions
lsblk                                 # List block devices
blkid                                 # Block device attributes
fdisk -l                              # List partition tables
df -h                                 # Disk space usage
du -sh <dir>                          # Directory size

# Create partitions
fdisk /dev/sda                        # MBR partition (interactive)
gdisk /dev/sda                        # GPT partition (interactive)
parted /dev/sda                       # Both MBR and GPT

# Create filesystems
mkfs.ext4 /dev/sda1                   # ext4 filesystem
mkfs.xfs /dev/sda1                    # XFS filesystem
ls /usr/sbin/mkfs*                    # List available filesystems

# Mount filesystems
mount /dev/sda1 /mnt/data             # Mount device
umount /mnt/data                      # Unmount
mount -a                              # Mount all from /etc/fstab

# Swap space
mkswap /dev/sda3                      # Create swap
swapon /dev/sda3                      # Enable swap
swapoff /dev/sda3                     # Disable swap
swapon --show                         # Show swap usage

# Filesystem labels
e2label /dev/sda1 "data"              # Set ext2/3/4 label
xfs_admin -L "data" /dev/sda1         # Set XFS label

# Filesystem check and resize
e2fsck -f /dev/sda1                   # Check ext filesystem
resize2fs /dev/sda1 20G               # Resize ext filesystem
```

### Phase 5: Logical Volume Manager (LVM)

Create and manage logical volumes:

```bash
# Physical Volumes
pvcreate /dev/sdb /dev/sdc            # Create PVs
pvdisplay                             # Detailed PV info
pvs                                   # Summary PV info
pvscan                                # Scan for PVs
pvremove /dev/sdb                     # Remove PV

# Volume Groups
vgcreate my_vg /dev/sdb /dev/sdc      # Create VG
vgdisplay                             # Detailed VG info
vgs                                   # Summary VG info
vgextend my_vg /dev/sdd               # Add PV to VG
vgremove my_vg                        # Remove VG

# Logical Volumes
lvcreate -L 100G my_vg -n my_lv       # Create 100GB LV
lvcreate -l 100%FREE my_vg -n my_lv   # Use all free space
lvdisplay                             # Detailed LV info
lvs                                   # Summary LV info

# Resize Logical Volumes
lvextend -L +10G /dev/my_vg/my_lv     # Extend by 10GB
lvreduce -L 50G /dev/my_vg/my_lv      # Reduce to 50GB
lvresize -L +10G /dev/my_vg/my_lv     # Resize (extend/reduce)
lvremove /dev/my_vg/my_lv             # Remove LV

# After LV resize, resize filesystem
resize2fs /dev/my_vg/my_lv            # For ext2/3/4
xfs_growfs /mnt/mountpoint            # For XFS (extend only)
```

### Phase 6: Process and Service Management

Manage processes and systemd services:

```bash
# Process viewing
ps aux                                # All processes with users
pstree                                # Process tree
top                                   # Interactive process view
htop                                  # Enhanced process view
pgrep <process>                       # Find PID by name

# Process control
kill <PID>                            # Terminate process
kill -9 <PID>                         # Force kill
killall <name>                        # Kill by name
nice -n 10 <command>                  # Start with priority
renice 5 -p <PID>                     # Change running priority

# Background jobs
<command> &                           # Run in background
jobs                                  # List background jobs
fg %1                                 # Bring job 1 to foreground
bg %1                                 # Resume job 1 in background
Ctrl+Z                                # Suspend current process

# Open files
lsof                                  # List open files
lsof -i :80                           # Files on port 80
lsof -u <user>                        # Files opened by user
lsof <file>                           # Processes using file

# Systemd service management
systemctl status <service>            # Service status
systemctl start <service>             # Start service
systemctl stop <service>              # Stop service
systemctl restart <service>           # Restart service
systemctl enable <service>            # Enable at boot
systemctl disable <service>           # Disable at boot
systemctl mask <service>              # Prevent starting
systemctl list-unit-files             # List all units

# Boot analysis
systemd-analyze time                  # Boot time breakdown
systemd-analyze blame                 # Service init times
systemd-analyze security              # Security assessment
```

### Phase 7: Networking

Configure and troubleshoot networking:

```bash
# IP configuration
ip addr                               # Show IP addresses
ip addr add 192.168.1.10/24 dev eth0  # Add IP
ip addr del 192.168.1.10/24 dev eth0  # Remove IP
ip link set eth0 up                   # Bring interface up
ip link set eth0 down                 # Bring interface down

# Routing
ip route                              # Show routing table
ip route add default via 192.168.1.1  # Add default gateway
ip route add 10.0.0.0/8 via 192.168.1.1  # Add static route

# DNS
nslookup <domain>                     # DNS lookup
dig <domain>                          # Detailed DNS query
cat /etc/resolv.conf                  # DNS configuration

# Network testing
ping <host>                           # Test connectivity
traceroute <host>                     # Trace route
tracepath <host>                      # Trace path (no root)

# Socket statistics
ss -tuln                              # TCP/UDP listening ports
ss -an                                # All connections
netstat -tuln                         # Listening ports (legacy)

# NetworkManager CLI
nmcli device status                   # Device status
nmcli connection show                 # List connections
nmcli device wifi list                # List WiFi networks
nmcli device wifi connect <SSID> password <pass>

# Edit connection
nmcli connection edit <conn>
# In editor:
set ipv4.addresses 192.168.1.50/24
set ipv4.gateway 192.168.1.1
set ipv4.dns 8.8.8.8
set ipv4.method manual
save
quit
```

### Phase 8: Firewall Configuration (firewalld)

Manage firewall rules:

```bash
# Status and zones
firewall-cmd --state                  # Check if running
firewall-cmd --get-zones              # List available zones
firewall-cmd --get-default-zone       # Show default zone
firewall-cmd --get-active-zones       # Active zones with interfaces

# Zone management
firewall-cmd --permanent --new-zone=myzone  # Create zone
firewall-cmd --zone=public --change-interface=eth0 --permanent
firewall-cmd --reload                 # Apply changes

# Service rules
firewall-cmd --get-services           # List known services
firewall-cmd --permanent --zone=public --add-service=http
firewall-cmd --permanent --zone=public --add-service=https
firewall-cmd --permanent --zone=public --remove-service=http

# Port rules
firewall-cmd --permanent --zone=public --add-port=8080/tcp
firewall-cmd --permanent --zone=public --add-port=10000-20000/tcp
firewall-cmd --permanent --zone=public --remove-port=8080/tcp

# List rules
firewall-cmd --zone=public --list-services
firewall-cmd --zone=public --list-ports
firewall-cmd --zone=public --list-rich-rules
firewall-cmd --zone=public --list-all

# Rich rules (advanced)
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" service name="ssh" accept'
```

### Phase 9: Security Frameworks

#### SELinux (RHEL-based):

```bash
# Status
sestatus                              # Detailed SELinux status
getenforce                            # Current mode

# Mode changes
setenforce 0                          # Set permissive (temporary)
setenforce 1                          # Set enforcing (temporary)
# Edit /etc/selinux/config for permanent change

# Context management
ls -Z <file>                          # View file context
ps auxZ                               # View process contexts
chcon -t httpd_sys_content_t <file>   # Change context (temporary)
restorecon <file>                     # Restore default context

# Permanent context changes
semanage fcontext -a -t httpd_sys_content_t '/mydata(/.*)?'
restorecon -Rv /mydata

# Port labeling
semanage port -l                      # List port labels
semanage port -a -t http_port_t -p tcp 8080

# Booleans
getsebool -a                          # List all booleans
setsebool httpd_can_network_connect on
setsebool -P httpd_can_network_connect on  # Persistent
```

#### AppArmor (Debian-based):

```bash
# Status
aa-status                             # Profile status
aa-unconfined                         # Unconfined processes

# Profile management
aa-genprof /usr/bin/app               # Generate new profile
aa-logprof                            # Update profiles from logs
aa-autodep /usr/bin/app               # Quick basic profile

# Mode changes
aa-enforce /etc/apparmor.d/profile    # Set enforcing
aa-complain /etc/apparmor.d/profile   # Set complain mode
aa-disable /etc/apparmor.d/profile    # Disable profile
aa-remove-unknown                     # Remove unused profiles
```

### Phase 10: Backup and Task Scheduling

#### Backup tools:

```bash
# Archive with tar
tar -cvf archive.tar files/           # Create archive
tar -xvf archive.tar                  # Extract archive
tar -czvf archive.tar.gz files/       # Create gzipped archive
tar -xzvf archive.tar.gz              # Extract gzipped
tar -cJvf archive.tar.xz files/       # Create xz archive
tar -tvf archive.tar                  # List contents
tar --same-owner -xvf archive.tar     # Preserve ownership

# Disk imaging
dd if=/dev/sda of=/backup/sda.img bs=4M status=progress
dd if=/backup/sda.img of=/dev/sda bs=4M status=progress  # Restore

# Rsync
rsync -avz /source/ /dest/            # Local sync
rsync -avz -e ssh /local/ user@host:/remote/  # Remote sync
rsync -avz --delete /source/ /dest/   # Mirror (delete extras)
rsync -avz --dry-run /source/ /dest/  # Test run
rsync -avz --include="*.pdf" --exclude=".*" /source/ /dest/
```

#### Cron scheduling:

```bash
# Crontab management
crontab -l                            # List crontab
crontab -e                            # Edit crontab
crontab -r                            # Remove crontab

# Cron format: minute hour day month weekday command
# Examples:
0 2 * * * /path/to/backup.sh          # Daily at 2:00 AM
*/5 * * * * /path/to/check.sh         # Every 5 minutes
0 0 * * 0 /path/to/weekly.sh          # Weekly on Sunday
0 0 1 * * /path/to/monthly.sh         # Monthly on 1st

# Special directories (scripts auto-run)
/etc/cron.hourly/
/etc/cron.daily/
/etc/cron.weekly/
/etc/cron.monthly/
```

## Quick Reference

### File Manipulation

| Command | Purpose |
|---------|---------|
| `find / -name "*.txt"` | Find files by name |
| `find / -type f -mtime -7` | Files modified in 7 days |
| `find / -size +100M` | Files larger than 100MB |
| `grep -r "pattern" /path` | Recursive search |
| `awk '{print $1}' file` | Print first column |
| `sed 's/old/new/g' file` | Find and replace |
| `cut -d: -f1 /etc/passwd` | Extract field |
| `sort \| uniq` | Sort and deduplicate |

### Vim Commands

| Mode | Command | Action |
|------|---------|--------|
| Normal | `i/a` | Insert before/after |
| Normal | `o/O` | New line after/before |
| Normal | `dd` | Delete line |
| Normal | `yy` | Copy line |
| Normal | `p` | Paste |
| Normal | `/pattern` | Search forward |
| Execute | `:w` | Save |
| Execute | `:q!` | Quit without saving |
| Execute | `:wq` or `ZZ` | Save and quit |
| Execute | `:%s/old/new/g` | Replace all |

## Constraints and Limitations

### Permission Requirements
- Many commands require root/sudo access
- SELinux/AppArmor may restrict operations
- File ACLs may override standard permissions

### Distribution Differences
- Package managers differ (apt vs dnf/yum)
- Service management may vary
- Security frameworks differ (SELinux vs AppArmor)

### Best Practices
- Always test commands with `--dry-run` when available
- Use absolute paths in scripts and cron jobs
- Back up configurations before modifying
- Check logs after security changes

## Troubleshooting

### Permission Denied

**Solutions:**
1. Check file permissions: `ls -la <file>`
2. Verify SELinux/AppArmor: `sestatus` or `aa-status`
3. Check ACLs: `getfacl <file>`
4. Use sudo if appropriate

### Service Won't Start

**Solutions:**
1. Check status: `systemctl status <service>`
2. View logs: `journalctl -u <service>`
3. Verify configuration files
4. Check port conflicts: `ss -tuln`

### Disk Full

**Solutions:**
1. Find large files: `find / -size +100M`
2. Check by directory: `du -sh /*`
3. Clear package cache: `apt clean` or `dnf clean all`
4. Review log files in `/var/log`
