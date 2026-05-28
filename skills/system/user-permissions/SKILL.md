---
name: user-permissions
description: Linux user and permission management
version: 1.0.0
author: terminal-skills
tags: [linux, user, group, sudo, acl, permissions]
---

# User and Permission Management

## Overview
Linux user management, group management, sudo configuration, ACL permissions and other skills.

## User Management

### View Users
```bash
# Current user
whoami
id

# User information
id username
finger username

# All users
cat /etc/passwd
getent passwd

# Logged in users
who
w
last                                # Login history
```

### User Operations
```bash
# Create user
useradd username
useradd -m -s /bin/bash username    # Create home directory, specify shell
useradd -G group1,group2 username   # Specify supplementary groups

# Modify user
usermod -aG groupname username      # Add to group
usermod -s /bin/zsh username        # Change shell
usermod -L username                 # Lock user
usermod -U username                 # Unlock user

# Delete user
userdel username
userdel -r username                 # Also delete home directory

# Change password
passwd username
passwd -l username                  # Lock password
passwd -u username                  # Unlock password
chage -l username                   # View password policy
```

## Group Management

### View Groups
```bash
# User's groups
groups username
id -Gn username

# All groups
cat /etc/group
getent group

# Group members
getent group groupname
```

### Group Operations
```bash
# Create group
groupadd groupname
groupadd -g 1001 groupname          # Specify GID

# Modify group
groupmod -n newname oldname         # Rename

# Delete group
groupdel groupname

# Manage group members
gpasswd -a username groupname       # Add user
gpasswd -d username groupname       # Remove user
gpasswd -M user1,user2 groupname    # Set member list
```

## sudo Configuration

### Basic Usage
```bash
# Execute as root
sudo command
sudo -i                             # Switch to root shell
sudo -u username command            # Execute as another user

# View permissions
sudo -l
```

### sudoers Configuration
```bash
# Edit sudoers (recommended method)
visudo

# Or edit files under /etc/sudoers.d/
visudo -f /etc/sudoers.d/username
```

### Common Configuration Examples
```bash
# /etc/sudoers.d/username

# Full privileges
username ALL=(ALL:ALL) ALL

# No password required
username ALL=(ALL) NOPASSWD: ALL

# Specific commands
username ALL=(ALL) /usr/bin/systemctl restart nginx

# Specific commands without password
username ALL=(ALL) NOPASSWD: /usr/bin/docker

# Group privileges
%groupname ALL=(ALL) ALL
```

## ACL Permissions

### View ACL
```bash
getfacl file
getfacl -R dir                      # Recursive view
```

### Set ACL
```bash
# Set user permissions
setfacl -m u:username:rwx file
setfacl -m u:username:rx dir

# Set group permissions
setfacl -m g:groupname:rx file

# Set default ACL (new files inherit)
setfacl -d -m u:username:rwx dir

# Recursive set
setfacl -R -m u:username:rx dir

# Remove ACL
setfacl -x u:username file          # Remove specific
setfacl -b file                     # Remove all
```

## Special Permissions

### SUID/SGID/Sticky
```bash
# SUID (4) - Execute as file owner
chmod u+s file
chmod 4755 file

# SGID (2) - Execute as file group/directory inherits group
chmod g+s file
chmod 2755 dir

# Sticky (1) - Only owner can delete
chmod +t dir
chmod 1777 dir

# View
ls -la
# -rwsr-xr-x  SUID
# -rwxr-sr-x  SGID
# drwxrwxrwt  Sticky
```

## Common Scenarios

### Scenario 1: Create Developer User
```bash
# Create user and group
groupadd developers
useradd -m -s /bin/bash -G developers devuser

# Set password
passwd devuser

# Configure sudo
echo "devuser ALL=(ALL) NOPASSWD: /usr/bin/docker, /usr/bin/systemctl" > /etc/sudoers.d/devuser
chmod 440 /etc/sudoers.d/devuser
```

### Scenario 2: Shared Directory Permissions
```bash
# Create shared directory
mkdir /shared
groupadd shared
chown root:shared /shared
chmod 2775 /shared                  # SGID ensures new files inherit group

# Add users to group
usermod -aG shared user1
usermod -aG shared user2
```

### Scenario 3: Restrict User to Specific Commands
```bash
# /etc/sudoers.d/limited-user
limited ALL=(ALL) NOPASSWD: /usr/bin/systemctl status *, /usr/bin/journalctl
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| sudo permission denied | Check `/etc/sudoers.d/` configuration |
| User cannot login | Check shell, password lock status |
| Group permissions not working | Re-login or `newgrp groupname` |
| ACL not working | Check if filesystem supports ACL |
