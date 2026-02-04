---
name: process-management
description: Linux process management and control
version: 1.0.0
author: terminal-skills
tags: [linux, process, kill, signal, jobs]
---

# Process Management

## Overview
Linux process viewing, signal handling, resource limiting and other management skills.

## Process Viewing

### ps Command
```bash
# Common formats
ps aux                              # All process details
ps -ef                              # Full format
ps -eo pid,ppid,cmd,%mem,%cpu       # Custom columns

# Find specific process
ps aux | grep nginx
ps -C nginx                         # By command name

# Process tree
ps auxf
pstree
pstree -p                           # Show PID
```

### top/htop
```bash
# top interactive commands
top
# P - Sort by CPU
# M - Sort by memory
# k - Kill process
# q - Quit

# htop (more user-friendly)
htop
```

### Other Tools
```bash
# Sort by resource
ps aux --sort=-%cpu | head -10      # Highest CPU
ps aux --sort=-%mem | head -10      # Highest memory

# View process details
cat /proc/PID/status
cat /proc/PID/cmdline
ls -la /proc/PID/fd                 # Open file descriptors
```

## Signal Handling

### Common Signals
```bash
# Signal list
kill -l

# Common signals
# SIGTERM (15) - Graceful termination (default)
# SIGKILL (9)  - Force termination
# SIGHUP (1)   - Reload configuration
# SIGSTOP (19) - Pause process
# SIGCONT (18) - Continue process
```

### kill Command
```bash
# Terminate process
kill PID                            # Send SIGTERM
kill -9 PID                         # Force terminate
kill -HUP PID                       # Reload config

# Terminate by name
pkill nginx
pkill -9 -f "python script.py"

# Terminate all processes of a user
pkill -u username

# killall
killall nginx
killall -9 nginx
```

## Background Tasks

### Job Control
```bash
# Run in background
command &
nohup command &                     # Ignore hangup signal
nohup command > output.log 2>&1 &

# Job management
jobs                                # View jobs
fg %1                               # Foreground
bg %1                               # Background
Ctrl+Z                              # Pause current process
```

### screen/tmux
```bash
# screen
screen -S session_name              # Create session
screen -ls                          # List sessions
screen -r session_name              # Resume session
Ctrl+A D                            # Detach session

# tmux
tmux new -s session_name
tmux ls
tmux attach -t session_name
Ctrl+B D                            # Detach session
```

## Resource Limits

### ulimit
```bash
# View limits
ulimit -a

# Set limits
ulimit -n 65535                     # Max file descriptors
ulimit -u 4096                      # Max processes
ulimit -v unlimited                 # Virtual memory

# Permanent settings /etc/security/limits.conf
# * soft nofile 65535
# * hard nofile 65535
```

### cgroups
```bash
# View cgroup
cat /proc/PID/cgroup

# Limit CPU (systemd)
systemctl set-property service.service CPUQuota=50%

# Limit memory
systemctl set-property service.service MemoryLimit=512M
```

## Common Scenarios

### Scenario 1: Find and Kill Zombie Processes
```bash
# Find zombie processes
ps aux | awk '$8=="Z" {print}'

# Find parent process
ps -o ppid= -p ZOMBIE_PID

# Kill parent process
kill -9 PARENT_PID
```

### Scenario 2: Find Process Using Port
```bash
# Find process using port 80
lsof -i :80
ss -tlnp | grep :80
netstat -tlnp | grep :80

# Kill process
fuser -k 80/tcp
```

### Scenario 3: Monitor Process Resources
```bash
# Real-time monitor single process
top -p PID
watch -n 1 "ps -p PID -o %cpu,%mem,cmd"

# View files opened by process
lsof -p PID
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Process unresponsive | `strace -p PID` to view system calls |
| CPU 100% | `top`, `perf top` to analyze hotspots |
| Memory leak | `pmap -x PID`, `/proc/PID/smaps` |
| Zombie process | Find parent process, restart or kill parent |
| Process OOM killed | `dmesg | grep -i oom` |
