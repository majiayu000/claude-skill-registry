---
title: QEMU Test VMs
description: Alpine and Debian QEMU VMs for protocol testing, fuzzing, and network experiments
tags: [qemu, vm, testing, networking, fuzzing]
---

# QEMU Test VMs for Protocol Testing

## Overview

This skill describes the QEMU virtual machines available for protocol testing, fuzzing, and network experiments. These VMs provide isolated, disposable environments for testing network protocols without risking the host system.

## Available VMs

### Location
All VMs are in: `/home/matt/Git/VoE/qemu-vms/`

### VM Images

1. **Alpine Linux VMs** (lightweight, fast boot)
   - `alpine-base.qcow2` - Base Alpine image
   - `aoe-server.qcow2` - Alpine configured as server
   - `aoe-client.qcow2` - Alpine configured as client

2. **Debian Linux VMs** (full-featured, standard tools)
   - `debian-12-generic-amd64.qcow2` - Base Debian 12 image
   - `debian-aoe-client.qcow2` - Debian configured as client

## Quick Start

### Starting a Single VM

**Alpine VM:**
```bash
cd /home/matt/Git/VoE/qemu-vms
qemu-system-x86_64 -name test-alpine -m 512 \
  -hda alpine-base.qcow2 \
  -netdev user,id=net0,hostfwd=tcp::2222-:22 -device e1000,netdev=net0 \
  -nographic
```

**Debian VM:**
```bash
cd /home/matt/Git/VoE/qemu-vms
qemu-system-x86_64 -name test-debian -m 1024 \
  -hda debian-12-generic-amd64.qcow2 \
  -netdev user,id=net0,hostfwd=tcp::2224-:22 -device e1000,netdev=net0 \
  -enable-kvm -cpu host \
  -nographic
```

**Important:** Always include `-enable-kvm -cpu host` for hardware acceleration. This provides significant performance improvements by using KVM virtualization support.

### Starting Server + Client Pair

Use the provided script:
```bash
cd /home/matt/Git/VoE/qemu-vms
./start-vms.sh
```

This starts:
- Server VM on SSH port 2222
- Client VM on SSH port 2223
- Shared network on socket :8010

## VM Access

### Alpine VMs

**Console Login:**
- Username: `root`
- Password: (blank - just press Enter)

**SSH Login:**
- Username: `claude`
- Password: `alpine`
- Port: 2222 (server) or 2223 (client)

```bash
ssh -p 2222 claude@localhost
```

### Debian VMs

**Console Login:**
- Username: `debian`
- Password: `debian`

**SSH Login:**
- Username: `debian`
- Password: `debian`
- Port: 2224 (default)

```bash
ssh -p 2224 debian@localhost
```

### Manually Injecting SSH Keys

If a VM is configured for key-only SSH authentication (or you want to add your key without password login), you can manually inject the SSH key by mounting the disk image on the host:

```bash
# Load the nbd kernel module if not already loaded
sudo modprobe nbd max_part=8

# Connect the qcow2 image to a network block device
sudo qemu-nbd --connect=/dev/nbd0 /home/matt/Git/VoE/qemu-vms/debian-12-generic-amd64.qcow2

# Wait for the device to be ready
sudo partprobe /dev/nbd0
lsblk | grep nbd0

# Mount the root partition (usually /dev/nbd0p1)
sudo mkdir -p /mnt/debian
sudo mount /dev/nbd0p1 /mnt/debian

# Create .ssh directory if it doesn't exist
sudo mkdir -p /mnt/debian/home/debian/.ssh

# Add your public key
cat ~/.ssh/id_rsa.pub | sudo tee -a /mnt/debian/home/debian/.ssh/authorized_keys

# Set correct permissions (CRITICAL - SSH will reject wrong permissions)
sudo chmod 700 /mnt/debian/home/debian/.ssh
sudo chmod 600 /mnt/debian/home/debian/.ssh/authorized_keys
sudo chown -R 1000:1000 /mnt/debian/home/debian/.ssh  # UID 1000 is typically the first user

# Unmount and disconnect
sudo umount /mnt/debian
sudo qemu-nbd --disconnect /dev/nbd0
```

**Note:** This technique is useful when:
- cloud-init ISO wasn't attached on first boot
- VM is configured for key-only authentication
- Password authentication is disabled in sshd_config
- You need to recover access to a locked VM

## Network Configuration

### Network Modes

**1. User Mode (NAT) - Internet Access**
```bash
-netdev user,id=net0,hostfwd=tcp::2222-:22 -device e1000,netdev=net0
```
- VM gets DHCP address (usually 10.0.2.15)
- Can access internet through host NAT
- Host can access VM via port forwarding
- VM cannot be accessed from other VMs

**2. Socket Mode - VM-to-VM Communication**
```bash
# Server VM (listener)
-netdev socket,id=net1,listen=:8010 -device e1000,netdev=net1,mac=52:54:00:aa:bb:01

# Client VM (connector)
-netdev socket,id=net1,connect=localhost:8010 -device e1000,netdev=net1,mac=52:54:00:aa:bb:02
```
- Direct VM-to-VM networking
- No internet on this interface
- Use for protocol testing between VMs

**3. Combined - Both Networks**
```bash
-netdev user,id=net0,hostfwd=tcp::2222-:22 -device e1000,netdev=net0 \
-netdev socket,id=net1,listen=:8010 -device e1000,netdev=net1
```
- eth0: Internet access + host SSH
- eth1: VM-to-VM communication

### Port Forwarding

Forward additional ports to VM:
```bash
-netdev user,id=net0,hostfwd=tcp::2222-:22,hostfwd=tcp::3260-:3260,hostfwd=tcp::3000-:3000
```

This example forwards:
- Host 2222 → VM 22 (SSH)
- Host 3260 → VM 3260 (iSCSI)
- Host 3000 → VM 3000 (HTTP/CAS)

## Common Use Cases

### 1. Testing Network Protocol Server

**Scenario:** Test iSCSI/NBD/AoE server in VM

```bash
# Start VM with protocol port forwarded
qemu-system-x86_64 -m 1024 -hda debian-12-generic-amd64.qcow2 \
  -netdev user,id=net0,hostfwd=tcp::2224-:22,hostfwd=tcp::3260-:3260 \
  -device e1000,netdev=net0 -nographic

# SSH into VM
ssh -p 2224 debian@localhost

# Run your server in VM
./my-protocol-server --port 3260

# Test from host
./my-protocol-client --host localhost --port 3260
```

### 2. Protocol Fuzzing (Client in VM, Server on Host)

**Scenario:** Fuzz iSCSI server running on host

```bash
# On host - start your server
./iscsi-target --port 3260

# Start VM
qemu-system-x86_64 -m 1024 -hda alpine-base.qcow2 \
  -netdev user,id=net0,hostfwd=tcp::2222-:22 -device e1000,netdev=net0 \
  -nographic

# SSH into VM
ssh -p 2222 claude@localhost

# Run fuzzer in VM targeting host
# Host is reachable at 10.0.2.2 from VM
python3 fuzzer.py --target 10.0.2.2:3260
```

**Key:** From VM, host is always at `10.0.2.2` in user mode networking.

### 3. VM-to-VM Protocol Testing

**Scenario:** Test client/server both in VMs

```bash
# Terminal 1 - Server VM
qemu-system-x86_64 -name server -m 512 -hda aoe-server.qcow2 \
  -netdev user,id=net0,hostfwd=tcp::2222-:22 -device e1000,netdev=net0 \
  -netdev socket,id=net1,listen=:8010 -device e1000,netdev=net1,mac=52:54:00:aa:bb:01 \
  -nographic

# Terminal 2 - Client VM
qemu-system-x86_64 -name client -m 512 -hda aoe-client.qcow2 \
  -netdev user,id=net0,hostfwd=tcp::2223-:22 -device e1000,netdev=net0 \
  -netdev socket,id=net1,connect=localhost:8010 -device e1000,netdev=net1,mac=52:54:00:aa:bb:02 \
  -nographic

# Configure static IPs on eth1 (socket network)
# In server VM:
ip addr add 192.168.100.1/24 dev eth1
ip link set eth1 up

# In client VM:
ip addr add 192.168.100.2/24 dev eth1
ip link set eth1 up

# Test connectivity
ping 192.168.100.1  # from client to server
```

### 4. Packet Capture for Protocol Analysis

**On Host:**
```bash
# Capture traffic to/from VM
sudo tcpdump -i any -w protocol-test.pcap port 3260
wireshark protocol-test.pcap
```

**In VM:**
```bash
# Capture traffic inside VM
tcpdump -i eth0 -w /tmp/capture.pcap
# Copy out via SSH
scp -P 2222 claude@localhost:/tmp/capture.pcap ./
```

### 5. Fuzzing with Boofuzz

**Example Setup:**
```bash
# Start server in VM
qemu-system-x86_64 -m 1024 -hda debian-12-generic-amd64.qcow2 \
  -netdev user,id=net0,hostfwd=tcp::2224-:22,hostfwd=tcp::3260-:3260 \
  -device e1000,netdev=net0 -nographic

# SSH and start target server
ssh -p 2224 debian@localhost
./vulnerable-iscsi-server --port 3260

# From host, run fuzzer
python3 boofuzz-iscsi.py --target localhost:3260
```

If server crashes, VM is isolated - just restart it.

## VM Management

### Exiting QEMU

**From Console:**
- Press `Ctrl-A` then `X` to quit QEMU
- Or: `Ctrl-A` then `C` for QEMU monitor, then type `quit`

**From SSH:**
- Just logout: `exit`
- Stop VM from monitor: `Ctrl-A C` then `quit`

### Resetting VM to Clean State

```bash
# Copy base image over modified one
cd /home/matt/Git/VoE/qemu-vms
cp alpine-base.qcow2 test-vm.qcow2
```

Or use snapshot overlays:
```bash
# Create overlay (changes don't affect base)
qemu-img create -f qcow2 -b alpine-base.qcow2 -F qcow2 test-overlay.qcow2

# Use overlay
qemu-system-x86_64 -hda test-overlay.qcow2 ...

# Discard changes: just delete test-overlay.qcow2
```

### Taking Snapshots

```bash
# Create snapshot
qemu-img snapshot -c before-fuzzing test-vm.qcow2

# List snapshots
qemu-img snapshot -l test-vm.qcow2

# Restore snapshot
qemu-img snapshot -a before-fuzzing test-vm.qcow2
```

## Installing Tools in VMs

### Alpine Linux

```bash
# Update package index
apk update

# Install common tools
apk add python3 py3-pip tcpdump wireshark-common curl wget netcat-openbsd

# Install development tools
apk add gcc musl-dev linux-headers

# Install boofuzz
apk add py3-pip
pip3 install boofuzz
```

### Debian Linux

```bash
# Update package index
sudo apt update

# Install common tools
sudo apt install -y python3 python3-pip tcpdump wireshark tshark curl wget netcat-openbsd

# Install development tools
sudo apt install -y build-essential

# Install boofuzz
pip3 install boofuzz
```

## Building with AddressSanitizer (ASAN)

AddressSanitizer is a powerful memory error detector useful for fuzzing and security testing. **Important:** ASAN requires glibc and will NOT work on Alpine Linux (which uses musl libc).

### ASAN Compatibility

| Distribution | libc | ASAN Support |
|--------------|------|--------------|
| **Debian** | glibc | ✅ Full support |
| **Alpine** | musl | ❌ Not supported |

**Use Debian VMs for any ASAN-instrumented builds.**

### Building with ASAN (Example: NanoMQ)

```bash
# SSH to Debian VM
ssh -p 2224 debian@localhost

# Install build dependencies
sudo apt update
sudo apt install -y git cmake ninja-build build-essential

# Clone without recursive submodules to save space
git clone https://github.com/nanomq/nanomq.git
cd nanomq

# Only initialize essential submodules
git submodule update --init --depth=1 nng

# Create build directory
mkdir build && cd build

# Configure with ASAN flags
cmake .. -G Ninja \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_C_FLAGS="-fsanitize=address -fno-omit-frame-pointer -g -O1" \
  -DCMAKE_EXE_LINKER_FLAGS="-fsanitize=address" \
  -DNNG_ENABLE_TLS=OFF \
  -DENABLE_JWT=OFF \
  -DENABLE_QUIC=OFF

# Build
ninja

# Run with ASAN
ASAN_OPTIONS="detect_leaks=1:abort_on_error=0:halt_on_error=0:print_stats=1" \
  ./nanomq/nanomq start
```

### ASAN Options Explained

```bash
# Recommended ASAN environment variables
export ASAN_OPTIONS="detect_leaks=1:abort_on_error=0:halt_on_error=0:print_stats=1"
```

- `detect_leaks=1` - Enable memory leak detection
- `abort_on_error=0` - Don't abort on first error (useful for fuzzing)
- `halt_on_error=0` - Continue execution after detecting errors
- `print_stats=1` - Print memory allocation statistics

### Disk Space Management

VM disk images can fill up quickly when building large projects. Tips:

**1. Clone without recursive submodules:**
```bash
# Don't do this on small VMs:
git clone --recursive https://github.com/large-project/repo.git

# Instead:
git clone https://github.com/large-project/repo.git
cd repo
git submodule update --init --depth=1 essential-submodule
```

**2. Check disk usage:**
```bash
df -h
du -sh ~/project/*
```

**3. Clean build artifacts:**
```bash
# CMake projects
rm -rf build/
# Or just clean object files
find build/ -name "*.o" -delete
```

**4. Expand VM disk if needed:**
```bash
# On host - resize the qcow2 image
qemu-img resize vm.qcow2 +2G

# In VM - expand the filesystem
sudo growpart /dev/sda 1
sudo resize2fs /dev/sda1
```

## Tips and Tricks

### Copying Files to/from VMs

**Via SSH/SCP:**
```bash
# Copy to VM
scp -P 2222 fuzzer.py claude@localhost:/home/claude/

# Copy from VM
scp -P 2222 claude@localhost:/tmp/results.txt ./
```

**Via HTTP Server:**
```bash
# On host
cd /home/matt/Git/VoE
python3 -m http.server 8000

# In VM (host is 10.0.2.2)
wget http://10.0.2.2:8000/fuzzer.py
```

### Sharing Files Between VMs

Use host as intermediary:
```bash
# VM1 → Host
scp -P 2222 claude@localhost:/tmp/file.txt ./

# Host → VM2
scp -P 2223 file.txt claude@localhost:/tmp/
```

### Running Commands Without Login

```bash
# Execute command via SSH
ssh -p 2222 claude@localhost 'ping -c 3 10.0.2.2'

# Run script
ssh -p 2222 claude@localhost 'bash -s' < local-script.sh
```

### Multiple VMs on Different Ports

```bash
# VM1 on 2222
qemu-system-x86_64 -m 512 -hda vm1.qcow2 \
  -netdev user,id=net0,hostfwd=tcp::2222-:22 -device e1000,netdev=net0 \
  -nographic &

# VM2 on 2223
qemu-system-x86_64 -m 512 -hda vm2.qcow2 \
  -netdev user,id=net0,hostfwd=tcp::2223-:22 -device e1000,netdev=net0 \
  -nographic &

# VM3 on 2224
qemu-system-x86_64 -m 512 -hda vm3.qcow2 \
  -netdev user,id=net0,hostfwd=tcp::2224-:22 -device e1000,netdev=net0 \
  -nographic &
```

## Troubleshooting

### VM Won't Start

**Check if port is in use:**
```bash
ss -tlnp | grep 2222
# Kill conflicting process if needed
```

**Check if previous QEMU is running:**
```bash
ps aux | grep qemu
pkill qemu-system-x86_64
```

### Can't SSH to VM

**Wait for boot:**
```bash
# Keep trying until SSH is up
while ! ssh -p 2222 -o ConnectTimeout=1 claude@localhost 'echo ready'; do
  sleep 1
done
```

**Check SSH service in VM:**
```bash
# From console
rc-status  # Alpine
systemctl status ssh  # Debian
```

### VM-to-VM Network Not Working

**Check interface is up:**
```bash
ip link show eth1
ip link set eth1 up
```

**Check IP addresses:**
```bash
ip addr show
```

**Test connectivity:**
```bash
ping -I eth1 192.168.100.1
```

## Safety Notes

- VMs are isolated from host by default
- Crashes in VM don't affect host system
- Use VMs for testing potentially dangerous code
- Network mode `user` prevents VM from directly accessing host network
- For production testing, use proper network isolation (bridges, VLANs)

## Common Patterns

### Pattern: Fuzzing Server Protocol

1. Start VM with port forwarding
2. Run target server in VM
3. Run fuzzer from host against forwarded port
4. Monitor with tcpdump/wireshark
5. If VM crashes, restart clean image

### Pattern: Testing Client/Server

1. Start two VMs with socket network
2. Configure static IPs on socket interface
3. Run server on VM1, client on VM2
4. Use host SSH to control both
5. Capture traffic with tcpdump

### Pattern: Protocol Development

1. Develop on host (fast compile, full IDE)
2. Copy binary to VM via SCP
3. Test in VM (isolated environment)
4. Iterate quickly

## Reference

### QEMU Network Options
- [QEMU Networking Documentation](https://wiki.qemu.org/Documentation/Networking)
- User mode: `-netdev user,...`
- Socket mode: `-netdev socket,...`
- Port forwarding: `hostfwd=tcp::HOST_PORT-:VM_PORT`

### VM Images
- Alpine: Minimal, fast, 200MB disk
- Debian: Full-featured, 500MB+ disk
- Choose Alpine for speed, Debian for tools

### Typical Resource Allocation
- Alpine: 512MB RAM sufficient
- Debian: 1024MB RAM recommended
- Disk: Images grow dynamically (qcow2)

---

## Changelog

**2025-12-05 (v2):**
- Added hardware acceleration section (KVM/CPU host passthrough)
- Added SSH key manual injection procedure using qemu-nbd
- Added comprehensive ASAN build guide with Alpine/Debian compatibility notes
- Added disk space management tips for constrained VMs
- Documented git submodule best practices for space-limited builds
- Added NanoMQ MQTT broker build example with ASAN instrumentation

**2025-12-05 (v1):**
- Initial documentation

---

**Last Updated:** 2025-12-05
**Location:** `/home/matt/Git/VoE/qemu-vms/`
**Script:** `./start-vms.sh` for quick two-VM setup
