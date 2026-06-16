---
name: system-performance-remediation
user-invocable: false
skill_api_version: 1
hexagonal_role: supporting
metadata:
  tier: execution
description: "Use when restoring machine responsiveness from high CPU, memory, IO, cache, or runaway process pressure."
practices:
- pragmatic-programmer
---
<!-- TOC: Quick Reference | VM Tuning & Cache Bloat | systemd-oomd Protection | Kill Hierarchy | Diagnosis | Swap & zram | Disk Cleanup | Zellij/Tmux Cleanup | Orphans | Agent Swarm Fix | Fleet Triage | Emergency | References -->

# System Performance Remediation

> **Core Principle:** First, do no harm. Kill OBVIOUSLY useless processes before touching anything potentially useful.

> **The Whack-a-Mole Anti-Pattern:**
> Killing child processes (cargo builds, tests) is POINTLESS if confused parent agents respawn them.
> **Kill the confused agents, not their children.**

---

## Quick Reference — Copy-Paste Commands

```bash
# === INSTANT DIAGNOSIS ===
uptime && nproc && cat /proc/pressure/cpu | head -1

# === ONE-LINER STATUS (includes swap + memory pressure) ===
echo "Load: $(uptime | awk -F'load average:' '{print $2}') / $(nproc) cores | Mem: $(free -h | awk '/Mem:/{print $3"/"$2}') | Swap: $(free -h | awk '/Swap:/{print $3"/"$2}') | Zombies: $(ps -eo stat | grep -c '^Z' || echo 0) | MemP: $(awk -F= '/some/{print $2}' /proc/pressure/memory | cut -d' ' -f1)%"

# === VM TUNING CHECK (catches cache bloat before it kills sessions) ===
sysctl vm.vfs_cache_pressure vm.min_free_kbytes && cat /proc/pressure/memory

# === FIND STUCK PROCESSES ===
ps -eo pid,etimes,pcpu,args --sort=-etimes | grep -E 'bun test|cargo test|vercel|git add' | awk '$2 > 3600'

# === FIND STALE GEMINI AGENTS (24+ hours) ===
ps -eo pid,etimes,pcpu,rss,args | grep 'bun.*gemini' | grep -v grep | awk '$2 > 86400 {print $1, int($2/3600)"h", $3"%", int($4/1024)"MB"}'

# === COUNT MCP SERVER BLOAT ===
ps aux | grep -E 'playwright|morphmcp' | grep -v grep | wc -l

# === FIND COMPETING BUILDS ===
ps aux | grep cc1plus | grep -oP 'target[^/]*/' | sort | uniq -c

# === FIND OLD AGENTS (16+ hours) ===
ps -eo pid,etimes,pcpu,args | grep -E 'claude --dangerously|codex --dangerously' | awk '$2 > 57600 {print $1, int($2/3600)"h", $3"%"}'

# === KILL OLD AGENTS (16+ hours) ===
ps -eo pid,etimes,args | grep -E 'claude|codex' | awk '$2 > 57600 {print $1}' | xargs -r kill

# === RENICE ALL COMPILATION ===
for pid in $(pgrep -f '/bin/cargo') $(pgrep cc1plus); do renice 19 -p $pid; ionice -c 3 -p $pid; done 2>/dev/null

# === ZELLIJ DEAD SESSION COUNT ===
zellij list-sessions 2>&1 | grep -c EXITED
```

---

## Kill Hierarchy (Safest First)

| Priority | Category | Examples | Risk |
|----------|----------|----------|------|
| 1 | **Zombies** | Defunct processes (Z state) | Zero — already dead |
| 2 | **Exited zellij/tmux sessions** | `zellij delete-all-sessions` | Zero — already exited |
| 3 | **Stuck tests** | `bun test`, `cargo test` 12+ hours | Low — idempotent |
| 4 | **Orphaned poll loops** | zsh shells waiting on files that never appear | Low — wasted CPU |
| 5 | **Stuck CLI** | `vercel inspect`, `git add .` 5+ min | Low — restart-safe |
| 6 | **Duplicate builds** | Multiple `cargo check` same project | Low — keep newest |
| 7 | **Old dev servers** | `next dev`, `bun --hot` idle 24+ hours | Low — restart-safe |
| 8 | **Stale gemini agents** | `bun gemini` running 24+ hours | Medium — likely stuck |
| 9 | **Old tmux sessions** | `ntm-*` no activity | Medium — check first |
| 10 | **Old agents** | `claude`, `codex` 16+ hours | Medium — likely stuck |
| 11 | **Active agents** | `claude`, `codex` <16 hours | High — doing work |
| 12 | **System processes** | NEVER TOUCH | Forbidden |

### Protected Patterns (NEVER KILL)

```
systemd, sshd, dbus, cron, docker, containerd
postgres, mysql, redis, elasticsearch, nginx, caddy
wezterm-mux-server  ← ABSOLUTELY NEVER TOUCH — holds ALL agent sessions
```

### SIGTERM vs SIGKILL

Some processes ignore SIGTERM. Always try SIGTERM first, wait 3s, escalate:

```bash
kill $PID; sleep 3; kill -0 $PID 2>/dev/null && kill -9 $PID
```

**Known SIGTERM-ignorers:** `bun test` — always needs SIGKILL after SIGTERM fails.

---

## VM Tuning & Filesystem Cache Bloat (The Silent Killer)

> **Real-world incident (2026-02-23):** On trj (499GB RAM, btrfs), `vfs_cache_pressure=50` let btrfs
> inode/dentry caches balloon to 388GB page cache + 40GB slab. Memory pressure hit 18%.
> `systemd-oomd` killed `user@1000.service`, destroying the mux server and **all 382 agent sessions**
> instantly. The fix: `vfs_cache_pressure=200` + `min_free_kbytes=2GB` + drop caches.
> Pressure dropped from 18% to 2.4% in minutes.

### The Cache Bloat Pattern

High-RAM machines with many agents accumulate massive filesystem caches. The kernel hoards dentries, inodes, and page cache (especially on btrfs). This creates **memory pressure even with "free" RAM** because the kernel's reclaim paths stall under pressure.

**Symptoms:**
- System feels sluggish despite `free -h` showing lots of "available" RAM
- `/proc/pressure/memory` shows sustained avg10 > 5% (the key metric!)
- `kcompactd0` running at 2-5% CPU continuously
- Slab cache (`cat /proc/meminfo | grep Slab`) is 20-40+ GB
- `vmstat 1 3` shows high `si`/`so` or `bi`/`bo` in first sample

### Diagnose Cache Bloat

```bash
# 1. Check memory pressure (THE critical metric)
cat /proc/pressure/memory
# some avg10=18.78 → 18.78% of time tasks stalled on memory = BAD

# 2. Check VM tuning
sysctl vm.vfs_cache_pressure vm.min_free_kbytes

# 3. Check slab breakdown
sudo slabtop -o -s c | head -15
# Look for: btrfs_inode (GB), radix_tree_node (GB), dentry (GB), ext4_inode_cache (GB)

# 4. Check page cache vs actual usage
grep -E "Cached|Slab|SReclaimable|SUnreclaim|Dirty|MemAvail" /proc/meminfo

# 5. Check kcompactd (memory compaction daemon — should be ~0% CPU)
ps -o pid,pcpu,etime,cmd -p $(pgrep kcompactd) 2>/dev/null
```

### Fix: Tune VM Parameters

**Settings by filesystem and RAM size:**

| Machine Type | FS | vfs_cache_pressure | min_free_kbytes | Notes |
|-------------|-----|-------------------|-----------------|-------|
| 499GB btrfs | btrfs | **200** | **2GB** (2097152) | btrfs caches are aggressive |
| 251GB ext4 | ext4 | **150** | **1-2GB** (1048576-2097152) | ext4 is less cache-heavy |
| 58GB ext4 | ext4 | **150** | **512MB** (524288) | VPS tier |
| 29GB ext4 | ext4 | **150** | **512MB** (524288) | VPS tier |
| 15GB ext4 | ext4 | **150** | **256MB** (262144) | Small VPS |

```bash
# Apply immediately
sudo sysctl -w vm.vfs_cache_pressure=200 vm.min_free_kbytes=2097152

# Drop caches for immediate relief (only if pressure avg10 > 5%)
sudo sh -c "sync; echo 3 > /proc/sys/vm/drop_caches"

# Persist to sysctl conf
sudo tee /etc/sysctl.d/99-system-resource-protection.conf << 'EOF'
# Tuned for heavy agent workloads
vm.swappiness = 10
vm.vfs_cache_pressure = 200
vm.dirty_background_ratio = 5
vm.dirty_ratio = 10
vm.min_free_kbytes = 2097152
fs.inotify.max_user_watches = 524288
fs.inotify.max_user_instances = 1024
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr
vm.max_map_count = 2147483642
EOF
```

**WARNING:** The default `vfs_cache_pressure=100` is dangerous on high-RAM btrfs machines.
A value of `50` (often set by "desktop optimization" scripts) is even worse — it actively
tells the kernel to hoard caches. Always check this on any machine that feels sluggish.

### Fleet-Wide VM Audit

```bash
# Quick audit of VM tuning across fleet
for host in trj css csd vmi1152480 vmi1153651 vmi1156319 vmi1167313 vmi1227854 vmi1264463 vmi1293453; do
  echo -n "$host: " && ssh -o ConnectTimeout=5 $host \
    'printf "vfs=%s min_free=%sKB mem_pressure=%s\n" \
      $(sysctl -n vm.vfs_cache_pressure) \
      $(sysctl -n vm.min_free_kbytes) \
      $(awk -F= "/some/{print \$2}" /proc/pressure/memory | cut -d" " -f1)' 2>/dev/null || echo "UNREACHABLE"
done
```

---

## systemd-oomd Protection (Preventing Session Massacres)

> **The worst-case scenario:** `systemd-oomd` kills `user@1000.service`, which cascades to
> kill the wezterm-mux-server, destroying ALL agent sessions. This happened on trj when
> a single session peaked at 404GB and the user slice hit 496GB/536GB EffectiveMemoryMax.

### Set Per-Session Memory Limits

Prevent any single session from consuming enough memory to trigger oomd:

```bash
# Cap individual sessions (prevents one runaway session from killing the user slice)
sudo mkdir -p /etc/systemd/system/session-.scope.d
sudo tee /etc/systemd/system/session-.scope.d/memory-limit.conf << 'EOF'
[Scope]
MemoryMax=64G
MemoryHigh=48G
EOF

# Cap the entire user slice (leave headroom for system)
# NOTE: Check for existing override.conf that might set MemoryMax=infinity
sudo mkdir -p /etc/systemd/system/user-1000.slice.d
# Edit existing override.conf if present, or create new:
sudo tee /etc/systemd/system/user-1000.slice.d/memory-limit.conf << 'EOF'
[Slice]
MemoryMax=460G
MemoryHigh=400G
EOF

sudo systemctl daemon-reload
```

**CRITICAL:** Check for pre-existing override files that set `MemoryMax=infinity` — these
sort alphabetically after `memory-limit.conf` and will negate your limits. Consolidate
all settings into a single file or name yours `zz-memory-limit.conf`.

### Verify Session Limits

```bash
# Check per-session limits
for scope in $(systemctl --user list-units --type=scope --state=running --no-legend | awk '{print $1}' | grep session); do
  echo -n "$scope: " && systemctl show "$scope" -p MemoryMax 2>/dev/null
done

# Check user slice limit
systemctl show user-1000.slice -p MemoryMax -p MemoryHigh
```

### Retain oomd Logs

By default, journald rotation can lose oomd kill logs. Ensure they survive:

```bash
sudo mkdir -p /etc/systemd/journald.conf.d
sudo tee /etc/systemd/journald.conf.d/retain-oomd.conf << 'EOF'
[Journal]
SystemMaxUse=2G
SystemKeepFree=1G
MaxRetentionSec=7day
EOF
sudo systemctl restart systemd-journald
```

### Fix resource-watchdog Service

If `resource-watchdog.service` is crash-looping with `IOPRIO` errors:

```bash
# Check status
systemctl --user status resource-watchdog.service

# The fix: IOSchedulingClass=realtime requires root — change to best-effort
# In ~/.config/systemd/user/resource-watchdog.service:
# IOSchedulingClass=realtime  →  IOSchedulingClass=best-effort

systemctl --user daemon-reload
systemctl --user restart resource-watchdog.service
```

---

## Diagnosis

### CPU Pressure (Critical for Sluggishness)

Load average can look "OK" while system feels sluggish. **CPU pressure reveals the truth.**

```bash
cat /proc/pressure/cpu
# some avg10=57.18 → 57% of time tasks waiting for CPU = BAD
```

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| CPU pressure avg10 | <10% | 10-30% | >30% |
| IO pressure avg10 | <5% | 5-15% | >15% |
| Memory pressure avg10 | <5% | 5-20% | >20% |

### Full Status Check (Linux)

```bash
uptime && nproc              # Load vs cores (danger: ratio > 1.5)
free -h                       # Memory (danger: available < 10%)
swapon --show                 # Swap config (danger: 0B total or near-full)
ps -eo stat | grep -c '^Z'   # Zombie count
cat /proc/sys/fs/file-nr     # File handles (allocated, free, max)
ps aux --sort=-%cpu | head -20 # Top CPU consumers
ps aux --sort=-%mem | head -10 # Top memory consumers
vmstat 1 3                    # IO wait, context switches, swap in/out
cat /proc/pressure/cpu        # CPU pressure
cat /proc/pressure/memory     # Memory pressure (THE key sluggishness metric)
cat /proc/pressure/io         # IO pressure
df -h / /data /tmp /data/tmp  # Disk space
sysctl vm.vfs_cache_pressure vm.min_free_kbytes  # VM tuning (cache bloat check)
grep -E "Slab|SReclaimable" /proc/meminfo         # Slab cache size
```

### macOS Quick Status

```bash
top -l 1 -n 10 -stats pid,command,cpu,mem,state | head -20
memory_pressure               # < 20% = warning, < 10% = critical
```

---

## Swap & zram Management

### The Swap Paradox

A machine can have 189GB free RAM yet feel sluggish because **30GB of process pages are stuck in swap** from a past memory spike. The kernel doesn't proactively move pages back to RAM — they only fault back on access, causing latency spikes.

**Symptom:** Machine feels laggy, `free -h` shows plenty of available RAM but significant swap used.

### Diagnose Swap Issues

```bash
swapon --show
free -h | grep Swap
```

**Red flags:**
- **Swap total = 0B** — no safety net, OOM killer strikes without warning
- **Swap used >> 0 with lots of free RAM** — past spike left pages in swap, causing latency
- **Swap near-full** — next spike = OOM kill

### Fix: Flush Swap Back to RAM

When swap is used but RAM is plentiful, flush to restore responsiveness:

```bash
# ONLY do this when free RAM >> swap used
sudo swapoff -a && sudo swapon -a
# Can take minutes for large swap usage (30GB ≈ 2-5 min)
```

### Set Up zram Swap

zram creates compressed swap in RAM. Cold pages get compressed (2-3x ratio with lz4) instead of being evicted or hitting disk. Size at ~13% of total RAM.

| RAM | Cores | zram Size | Algorithm |
|-----|-------|-----------|-----------|
| 499GB | 128 | 64GB | lzo-rle or lz4 |
| 251GB | 64-128 | 32GB | lz4 |
| 62GB | 16 | 8GB | lz4 |
| 31GB | 8 | 4GB | lz4 |

```bash
# Activate immediately
sudo modprobe zram num_devices=1
echo lz4 | sudo tee /sys/block/zram0/comp_algorithm 2>/dev/null
echo 32G | sudo tee /sys/block/zram0/disksize   # Adjust per table above
sudo mkswap /dev/zram0
sudo swapon -p 100 /dev/zram0  # Priority 100 = prefer over disk swap

# Verify
swapon --show && zramctl
```

### Persist zram Across Reboots

Machines silently lose zram after reboot without a systemd service:

```bash
sudo tee /etc/systemd/system/zram-swap.service > /dev/null << 'EOF'
[Unit]
Description=Configure zram swap
After=local-fs.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/bin/bash -c 'modprobe zram num_devices=1 && echo lz4 > /sys/block/zram0/comp_algorithm 2>/dev/null; echo 32G > /sys/block/zram0/disksize && mkswap /dev/zram0 && swapon -p 100 /dev/zram0'
ExecStop=/bin/bash -c 'swapoff /dev/zram0 2>/dev/null; echo 1 > /sys/block/zram0/reset 2>/dev/null'

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload && sudo systemctl enable zram-swap.service
```

**Adjust the `echo 32G` line** to match the sizing table above for your machine.

---

## Disk Space Cleanup

### Common Disk Hogs on Agent Machines

```bash
df -h / /data /tmp /data/tmp
du -sh /tmp/* 2>/dev/null | sort -rh | head -20
du -sh /data/tmp/* 2>/dev/null | sort -rh | head -20

# Find stale Rust target dirs (>7 days old)
find /data -maxdepth 2 -name 'cargo-target*' -o -name 'target-*' -o -name 'tmp-target-*' 2>/dev/null

# Large old files (>100MB, >3 days)
find /tmp /data/tmp -type f -size +100M -mtime +3 -exec ls -lh {} \; 2>/dev/null | head -30
```

### Known Disk Hogs

| Pattern | Location | Typical Size | Safe to Remove? |
|---------|----------|-------------|-----------------|
| `rch_*` / `rch-target-*` | /tmp, /data/tmp | 10-200GB each | Yes if not actively compiling |
| `rch_bolddesert` etc | /data/tmp | Up to **400GB** | Yes — agent build caches |
| `codex_*_target` | /tmp | 5-30GB each | Yes if idle |
| `tmp.XXXXXXXXXX` (mktemp) | /data/tmp | 30-200GB | Check with `fuser` first |
| `cargo-target*` / `target-*-build` | /data root | 15-40GB each | Yes if >7 days old |
| `go-build*` | /data/tmp | 1-5GB each | Yes — Go rebuilds automatically |
| `fsfs_index_snapshot*` | /tmp | 1-2GB each | Yes |

### Before Removing: Check if In Use

```bash
fuser /data/tmp/suspect_dir 2>&1 | head -3
stat -c '%y' /data/tmp/suspect_dir   # Last modification time
```

---

## Zellij Session Cleanup

Agent swarms create hundreds of zellij sessions that pile up as EXITED. 268 exited sessions is common after a few weeks.

```bash
# Count exited sessions
zellij list-sessions 2>&1 | grep -c EXITED

# List active (non-exited) sessions
zellij list-sessions 2>&1 | grep -v EXITED | grep -v '^$'

# Delete ALL exited sessions (safe — they're already dead)
zellij delete-all-sessions --yes

# Delete a specific session
zellij delete-session SESSION_NAME
```

Exited sessions consume disk and memory for stored scrollback. Clean regularly.

---

## NTM/Tmux Cleanup

```bash
# List sessions with ages
/usr/bin/tmux list-sessions -F '#{session_name} #{session_created}' | while read name created; do
  echo "$name: $(( ($(date +%s) - created) / 3600 ))h old"
done

# Kill test artifact sessions (safe)
/usr/bin/tmux list-sessions -F '#{session_name}' | grep -E '^ntm-(test|lifecycle|rapid)-' | \
  xargs -I{} /usr/bin/tmux kill-session -t {}
```

---

## Orphaned Process Cleanup

### Orphaned Poll Loops

Agent shells sometimes spawn zsh processes that poll forever for files that will never appear:

```bash
# Find orphaned zsh shells waiting on nonexistent files
ps aux | grep 'while.*sleep.*done' | grep -v grep
ps aux | grep 'zsh.*exit_code' | grep -v grep

# Find detached agent processes (no TTY = likely orphaned)
ps aux | grep -E 'claude|codex|cass' | grep -v grep | awk '$7 == "?" {print}'
```

### MCP Server Bloat

Each claude/codex agent spawns ~4 MCP server processes (playwright npx, morphmcp npx, sh wrapper, playwright-mcp node). Stale agents leave these orphaned:

```bash
# Count MCP servers
ps aux | grep -E 'playwright|morphmcp' | grep -v grep | wc -l

# They die when their parent agent dies — kill the agent, not the MCP servers
```

### Runaway `cass` / `am` Processes

These can burn 20%+ CPU each when stuck:

```bash
# Find long-running cass processes
ps -eo pid,etimes,pcpu,rss,comm | grep cass | awk '$2 > 86400 {print}'
```

---

## Agent Swarm Meltdown Fix

**The #1 cause of meltdowns:** Multiple agents building the same project with different `CARGO_TARGET_DIR`.

### Step 1: Detect Competing Builds

```bash
ps aux | grep cc1plus | grep -oP 'target[^/]*/' | sort | uniq -c
```

### Step 2: Kill Confused OLD Agents (NOT the builds!)

```bash
ps -eo pid,etimes,pcpu,args | grep -E 'claude --dangerously|codex --dangerously' | \
  awk '$2 > 57600 {print $1, int($2/3600)"h"}' | \
  while read pid age; do echo "Killing old agent $pid ($age)"; kill $pid; done
```

### Step 3: Renice Remaining Builds

```bash
for pid in $(pgrep -f '/bin/cargo') $(pgrep cc1plus); do
  renice 19 -p $pid; ionice -c 3 -p $pid
done 2>/dev/null
```

### Step 4: Monitor Improvement

```bash
for i in 1 2 3; do
  sleep 10
  echo "$(date +%H:%M:%S) Load: $(cat /proc/loadavg | awk '{print $1}') | CPU pressure: $(cat /proc/pressure/cpu | awk -F= '{print $2}' | cut -d' ' -f1)%"
done
```

---

## Fleet-Wide Triage

When managing multiple machines, triage sequentially via SSH (parallel SSH can cascade failures):

```bash
# Quick status across fleet (sequential to avoid SSH cascading failures)
for host in trj css csd vmi1149989 vmi1152480 vmi1153651 vmi1156319 vmi1167313 vmi1227854 vmi1264463 vmi1293453; do
  echo "=== $host ===" && ssh -o ConnectTimeout=10 $host \
    'df -h / /data 2>/dev/null | tail -n+2 && uptime && echo -n "zombies: " && ps -eo stat | grep -c Z' 2>&1
  echo "---"
done

# Fleet VM tuning audit (catches cache bloat before it kills sessions)
for host in trj css csd vmi1149989 vmi1152480 vmi1153651 vmi1156319 vmi1167313 vmi1227854 vmi1264463 vmi1293453; do
  echo -n "$host: " && ssh -o ConnectTimeout=10 $host \
    'printf "vfs=%s min_free=%sKB mem_pressure=%s slab=%s\n" \
      $(sysctl -n vm.vfs_cache_pressure) \
      $(sysctl -n vm.min_free_kbytes) \
      $(awk -F= "/some/{print \$2}" /proc/pressure/memory | cut -d" " -f1) \
      $(grep SReclaimable /proc/meminfo | awk "{print \$2}")' 2>/dev/null || echo "UNREACHABLE"
done

# Fleet swap audit (machines silently lose swap after reboots)
for host in trj css csd vmi1149989 vmi1152480 vmi1153651 vmi1156319 vmi1167313 vmi1227854 vmi1264463 vmi1293453; do
  echo -n "$host: " && ssh -o ConnectTimeout=10 $host \
    "swapon --show --noheadings | wc -l; systemctl is-enabled zram-swap.service 2>/dev/null || echo 'NO_ZRAM_SERVICE'" 2>/dev/null || echo "UNREACHABLE"
done

# Find stuck bun tests across fleet
for host in trj css csd; do
  echo "=== $host ===" && ssh $host "ps -eo pid,etimes,args | grep 'bun test' | awk '\$2 > 43200 {print \$1, int(\$2/3600)\"h\"}'"
done
```

---

## Kill Stuck Processes

### Stuck Tests (12+ hours)

**Note:** `bun test` ignores SIGTERM — always escalate to SIGKILL.

```bash
for pid in $(ps -eo pid,etimes,args | grep 'bun test' | awk '$2 > 43200 {print $1}'); do
  kill $pid; sleep 3; kill -0 $pid 2>/dev/null && kill -9 $pid
done
```

### Stuck Vercel/Git Commands

```bash
ps -eo pid,etimes,args | grep 'vercel' | awk '$2 > 600 {print $1}' | xargs -r kill
ps -eo pid,etimes,args | grep 'git add' | awk '$2 > 120 {print $1}' | xargs -r kill -9
```

### Stale Gemini Agents (24+ hours)

```bash
ps -eo pid,etimes,args | grep 'bun.*gemini' | grep -v grep | awk '$2 > 86400 {print $1}' | xargs -r kill -9
```

### Abandoned Dev Servers (24+ hours)

```bash
ps -eo pid,etimes,pcpu,args | grep -E 'next dev|bun --hot|vite' | \
  awk '$2 > 86400 && $3 < 1 {print $1}' | xargs -r kill
```

---

## Emergency Response

When load > 2x CPU count:

```bash
# 1. Quick status
echo "LOAD: $(cat /proc/loadavg | awk '{print $1}')/$(nproc) cores"

# 2. Kill stuck tests (always safe — bun needs SIGKILL)
pgrep -f 'bun test' | while read pid; do
  age=$(ps -o etimes= -p $pid 2>/dev/null | tr -d ' ')
  [[ "$age" -gt 43200 ]] && kill -9 $pid && echo "Killed bun test $pid"
done

# 3. Kill stale gemini agents (24+ hours)
ps -eo pid,etimes,args | grep 'bun.*gemini' | grep -v grep | awk '$2 > 86400 {print $1}' | xargs -r kill -9

# 4. Delete exited zellij sessions
zellij delete-all-sessions --yes 2>/dev/null

# 5. Kill old Claude/Codex agents (16+ hours)
ps -eo pid,etimes,args | grep -E 'claude|codex' | awk '$2 > 57600 {print $1}' | xargs -r kill

# 6. Flush swap if used with free RAM available
used_swap=$(free -b | awk '/Swap:/{print $3}')
avail_ram=$(free -b | awk '/Mem:/{print $7}')
[[ $used_swap -gt 0 && $avail_ram -gt $((used_swap * 2)) ]] && sudo swapoff -a && sudo swapon -a && echo "Swap flushed"

# 7. Verify
sleep 5 && uptime && free -h | grep Swap
```

---

## RCH Health Check

```bash
rch daemon status --json 2>/dev/null | head -5  # Running?
rch workers probe --all                          # Workers reachable?
pkill -9 rchd; sleep 1; rch daemon start        # Quick fix
```

---

## File Handle Exhaustion

```bash
cat /proc/sys/fs/file-nr                        # allocated, free, max
sudo sysctl -w fs.file-max=2097152              # Temporary increase
ulimit -n 65536                                  # Session increase
```

---

## Memory Relief

### Quick Cache Drop (Safe)

```bash
free -h
sudo sh -c "sync; echo 3 > /proc/sys/vm/drop_caches"  # Drops clean page cache, dentries, inodes
free -h
```

### Full Memory Pressure Remediation

When memory pressure is sustained (avg10 > 5%), the issue is usually VM tuning, not a single process:

```bash
# 1. Check pressure
cat /proc/pressure/memory
# some avg10=18.78 → 18.78% stalled = BAD

# 2. Fix VM tuning (the root cause on most agent machines)
sudo sysctl -w vm.vfs_cache_pressure=200 vm.min_free_kbytes=2097152

# 3. Drop caches for immediate relief
sudo sh -c "sync; echo 3 > /proc/sys/vm/drop_caches"

# 4. Verify improvement (wait 30s, check again)
sleep 30 && cat /proc/pressure/memory
# avg10 should be dropping rapidly

# 5. Persist the fix
# Edit /etc/sysctl.d/99-system-resource-protection.conf
```

### Slab Cache Investigation

When `free -h` shows huge buff/cache but no single process is responsible:

```bash
# What's in the slab cache?
sudo slabtop -o -s c | head -15

# Common offenders on btrfs:
# - btrfs_inode (7+ GB)      → vfs_cache_pressure too low
# - radix_tree_node (11+ GB) → page cache metadata
# - kmalloc-rnd-08-128       → kernel allocations

# Common offenders on ext4:
# - buffer_head (2+ GB)      → ext4 block metadata
# - ext4_inode_cache (1+ GB) → ext4 inode caching
```

---

## Validation Checklist

```bash
uptime                                          # Load < nproc
free -h                                         # Available increased
cat /proc/pressure/memory                       # avg10 < 5% (THE key metric)
sysctl vm.vfs_cache_pressure vm.min_free_kbytes # vfs >= 150, min_free >= 256MB
swapon --show                                   # Swap present and not full
zramctl                                         # zram active with compression
ps -eo stat | grep -c '^Z'                      # No zombies
zellij list-sessions 2>&1 | grep -c EXITED      # No exited sessions
df -h / /data                                   # Disk not critically full
cat /proc/sys/fs/file-nr                        # FDs normalized
systemctl --user status resource-watchdog 2>/dev/null  # Not crash-looping
grep -E "Slab|SReclaimable" /proc/meminfo       # Slab not bloated (< 10% of RAM)
```

---

## References

| Topic | Reference |
|-------|-----------|
| Agent swarm patterns | [AGENT-SWARM-PATTERNS.md](references/AGENT-SWARM-PATTERNS.md) |
| Common scenarios | [COMMON-SCENARIOS.md](references/COMMON-SCENARIOS.md) |
| Detailed triage steps | [DETAILED-TRIAGE.md](references/DETAILED-TRIAGE.md) |
| Detailed diagnostics | [DIAGNOSIS.md](references/DIAGNOSIS.md) |
| Escalation ladder | [ESCALATION.md](references/ESCALATION.md) |
| Prevention guide | [PREVENTION.md](references/PREVENTION.md) |
| PT integration | [PT-INTEGRATION.md](references/PT-INTEGRATION.md) |
| RCH integration | [RCH-INTEGRATION.md](references/RCH-INTEGRATION.md) |
| Wezterm recovery | [WEZTERM-RECOVERY.md](references/WEZTERM-RECOVERY.md) |
| Diagnostic script | [scripts/diagnose-system.sh](scripts/diagnose-system.sh) |
| Related skills | `ntm`, `vibing-with-ntm`, `rch` |
