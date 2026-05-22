---
name: orbstack-best-practices
description: Patterns for OrbStack Linux VMs and Docker on macOS. Covers orbctl/orb commands, machine lifecycle, cloud-init, networking, file sharing, and SSH access. Must use when working with OrbStack, orbctl commands, or Linux VMs on macOS.
---

# OrbStack Best Practices

OrbStack is a fast, lightweight Docker and Linux VM runtime for macOS. Replaces Docker Desktop with better performance and seamless macOS integration.

## Core Commands

```bash
# Start/stop
orb                           # Start + open default machine shell
orb start                     # Start OrbStack
orb stop                      # Stop OrbStack

# Machine management
orb list                      # List machines
orb create ubuntu             # Create with latest version
orb create ubuntu:jammy myvm  # Specific version + name
orb create --arch amd64 ubuntu intel  # x86 on Apple Silicon
orb delete myvm               # Delete machine

# Shell access
orb                           # Default machine shell
orb -m myvm                   # Specific machine
orb -u root                   # As root
orb -m myvm -u root           # Combined

# Run commands
orb uname -a                  # Run in default machine
orb -m myvm ./script.sh       # Run in specific machine

# File transfer
orb push ~/local.txt          # Copy to Linux
orb pull ~/remote.txt         # Copy from Linux
orb push -m vm ~/f.txt /dest/ # Push to specific machine/path

# Docker/K8s
orb restart docker            # Restart Docker engine
orb logs docker               # Docker engine logs
orb start k8s                 # Start Kubernetes
orb delete k8s                # Delete K8s cluster

# Config
orb config set memory_mib 8192  # Set memory limit
orb config docker               # Edit daemon.json
```

## Key Paths

| Path | Description |
|------|-------------|
| `~/OrbStack/<machine>/` | Linux files from macOS |
| `~/OrbStack/docker/volumes/` | Docker volumes from macOS |
| `/mnt/mac/Users/...` | macOS files from Linux |
| `/mnt/machines/<name>/` | Other machines from Linux |
| `~/.orbstack/ssh/id_ed25519` | SSH private key |
| `~/.orbstack/config/docker.json` | Docker daemon config |

## DNS Names

| Pattern | Description |
|---------|-------------|
| `<machine>.orb.local` | Linux machine |
| `<container>.orb.local` | Docker container |
| `<svc>.<project>.orb.local` | Compose service |
| `host.orb.internal` | macOS from Linux machine |
| `host.docker.internal` | macOS from container |
| `docker.orb.internal` | Docker from Linux machine |

## Machine Lifecycle

### Creation

```bash
orb create ubuntu                      # Latest Ubuntu
orb create ubuntu:noble devbox         # Ubuntu 24.04 named "devbox"
orb create --arch amd64 debian x86vm   # x86 emulation via Rosetta
orb create --set-password ubuntu pwvm  # With password set
orb create ubuntu myvm -c cloud.yml    # With cloud-init
```

Supported distros: Alma, Alpine, Arch, CentOS, Debian, Devuan, Fedora, Gentoo, Kali, NixOS, openSUSE, Oracle, Rocky, Ubuntu, Void

### Lifecycle

```bash
orb start myvm      # Start stopped machine
orb stop myvm       # Stop machine
orb restart myvm    # Restart
orb delete myvm     # Delete permanently
orb default myvm    # Set as default machine
orb logs myvm       # View boot logs
```

## Cloud-Init

Create machines with automated provisioning:

```bash
orb create ubuntu myvm -c user-data.yml
```

Example `user-data.yml`:

```yaml
#cloud-config
packages:
  - git
  - vim
  - docker.io

users:
  - name: dev
    groups: sudo, docker
    shell: /bin/bash
    sudo: ALL=(ALL) NOPASSWD:ALL

runcmd:
  - systemctl enable docker
  - systemctl start docker
```

Debug cloud-init:

```bash
orb logs myvm                              # Boot logs from macOS
orb -m myvm cloud-init status --long       # Status inside machine
orb -m myvm cat /var/log/cloud-init-output.log
```

## Networking

### Port Access

Servers in Linux machines are automatically on `localhost`:

```bash
# In Linux: python3 -m http.server 8000
# From macOS: curl localhost:8000 or curl myvm.orb.local:8000
```

### Connecting from Linux to macOS

```bash
# From Linux machine
curl host.orb.internal:3000

# From Docker container
curl host.docker.internal:3000
```

### VPN/Proxy

- Fully VPN-compatible with automatic DNS handling
- Follows macOS proxy settings automatically
- Custom proxy: `orb config set network_proxy http://proxy:8080`
- Disable: `orb config set network_proxy none`

## File Sharing

### macOS Files from Linux

```bash
# Same paths work
cat /Users/allen/file.txt
cat /mnt/mac/Users/allen/file.txt  # Explicit prefix
```

### Linux Files from macOS

```bash
ls ~/OrbStack/myvm/home/user/
ls ~/OrbStack/docker/volumes/myvolume/
```

### Transfer Commands

```bash
orb push ~/local.txt              # To default machine home
orb pull ~/remote.txt             # From default machine
orb push -m vm ~/f.txt /tmp/      # To specific path
```

## SSH Access

Built-in multiplexed SSH server (no per-machine setup):

```bash
ssh orb                    # Default machine
ssh myvm@orb               # Specific machine
ssh user@myvm@orb          # Specific user + machine
```

### IDE Setup

**VS Code**: Install "Remote - SSH" extension, connect to `orb` or `myvm@orb`

**JetBrains**: Host `localhost`, Port `32222`, Key `~/.orbstack/ssh/id_ed25519`

### Ansible

```ini
[servers]
myvm@orb ansible_user=ubuntu
```

SSH agent forwarding is automatic.

## Docker Integration

### Container Domains

```bash
docker run --name web nginx
# Access: http://web.orb.local (no port needed for web servers)

# Compose: <service>.<project>.orb.local
```

### HTTPS

Zero-config HTTPS for all `.orb.local` domains:

```bash
curl https://mycontainer.orb.local
```

### Custom Domains

```bash
docker run -l dev.orbstack.domains=myapp.local nginx
```

### Host Networking

```bash
docker run --net=host nginx
# localhost works both directions
```

### x86 Emulation

```bash
docker run --platform linux/amd64 ubuntu
export DOCKER_DEFAULT_PLATFORM=linux/amd64  # Default to x86
```

### SSH Agent in Containers

```bash
docker run -v /run/host-services/ssh-auth.sock:/agent.sock \
  -e SSH_AUTH_SOCK=/agent.sock alpine
```

### Volumes vs Bind Mounts

Prefer volumes for performance (data stays in Linux):

```bash
docker run -v mydata:/data alpine           # Volume (fast)
docker run -v ~/code:/code alpine           # Bind mount (slower)
```

## Kubernetes

```bash
orb start k8s           # Start cluster
kubectl get nodes       # kubectl included
```

All service types accessible from macOS without port-forward:

```bash
curl myservice.default.svc.cluster.local  # cluster.local works
curl 192.168.194.20                       # Pod IPs work
curl myservice.k8s.orb.local              # LoadBalancer wildcard
```

Local images available immediately (use non-`latest` tag or `imagePullPolicy: IfNotPresent`).

## Troubleshooting

```bash
orb report              # Generate diagnostic report
orb logs myvm           # Machine boot logs
orb logs docker         # Docker engine logs
orb restart docker      # Restart Docker
orb reset               # Factory reset (deletes everything)
```

**Cannot connect to Docker daemon**: Start OrbStack with `orb start`, or fix context with `docker context use orbstack`

**Machine not starting**: Check `orb logs myvm`, try `orb restart myvm`

**Rosetta x86 error**: Install x86 libc:
```bash
sudo dpkg --add-architecture amd64
sudo apt update && sudo apt install libc6:amd64
```

## Configuration

```bash
orb config set rosetta true        # Enable x86 emulation
orb config set memory_mib 8192     # Memory limit (MiB)
orb config set cpu 4               # CPU limit (cores)
orb config set network_proxy auto  # Proxy (auto/none/url)
```

Docker daemon config at `~/.orbstack/config/docker.json`:

```json
{
  "insecure-registries": ["registry.local:5000"],
  "registry-mirrors": ["https://mirror.gcr.io"]
}
```

Apply with `orb restart docker`.

## macOS Commands from Linux

```bash
mac open https://example.com   # Open URL in macOS browser
mac uname -a                   # Run macOS command
mac link brew                  # Link command for reuse
mac notify "Build done"        # Send notification
```

Forward env vars:

```bash
ORBENV=AWS_PROFILE:EDITOR orb ./deploy.sh
```
