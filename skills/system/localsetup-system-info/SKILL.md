---
name: localsetup-system-info
description: "Quick system diagnostics: CPU, memory, disk, uptime. Use when capturing server baseline or recording host layout and specs for further operations."
metadata:
  version: "1.1"
compatibility: "Linux: free, df, lscpu, uptime, ip, hostname, lsblk (or /proc); Python 3.10+ stdlib only for script. No sudo or extra packages."
---

# System info

Quick system diagnostics covering CPU, memory, disk, and uptime. Uses standard Linux utilities that are typically available. Use when you need a baseline snapshot of a server (layout, specs, installed software hints) to record for later operations.

## Commands

Run via your platform's command or terminal (e.g. shell tool, exec, or run command):

```bash
# CPU
lscpu
# or: cat /proc/cpuinfo

# Memory
free -h

# Disk
df -h

# Uptime
uptime
```

For a single combined snapshot, run in order: `lscpu`, `free -h`, `df -h`, `uptime`. Capture output to a file or paste into your baseline record.

## Extended snapshot (maximum context, no sudo)

To get maximum context without sudo or extra dependencies, use the bundled script. It uses only Python stdlib and commands/files readable by unprivileged users (no network, no write).

From the repo root (or with the skill directory as cwd):

```bash
python3 _localsetup/skills/localsetup-system-info/scripts/system_snapshot.py
```

Output is GFM markdown to stdout. It includes: identity and time, OS release, uptime and load, CPU, memory, disk and block devices, network (ip addr/route, resolv.conf), sessions (w/who), loaded kernel modules sample, and runtimes in PATH (e.g. python3, node). Redirect to a file to save a baseline, e.g. `... > baseline.md`.

If you prefer not to run the script, you can run these manually (all no sudo):

- `hostname`; `uname -a`; `date -Iseconds`
- `cat /etc/os-release`
- `uptime`; `cat /proc/loadavg`; `cat /proc/uptime`
- `lscpu` (or `cat /proc/cpuinfo`)
- `free -h`; `cat /proc/meminfo`
- `df -h`; `df -i`; `lsblk -o NAME,SIZE,TYPE,MOUNTPOINT`; `cat /proc/partitions`
- `ip -br addr`; `ip route`; `cat /etc/resolv.conf`
- `w` or `who`
- `cat /proc/modules` (sample)
- `which python3 node`; `python3 --version`; `node --version` (if needed)

## Install

No installation needed. The quick commands use `free`, `df`, `uptime`, and `lscpu` (or `/proc`); the extended script uses Python 3.10+ stdlib only. On minimal images, install `util-linux` if `lscpu` or `lsblk` is missing.

<!-- Import note: this skill was imported from openclaw/skills (xejrax/system-info). The source included _meta.json (OpenClaw registry metadata); it was not copied because this framework targets multiple platforms and does not use OpenClaw-specific manifest files. -->
