---
name: docker-platform-guide
description: Platform-specific Docker considerations for Windows, Linux, and macOS
---

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems


### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

- **Priority**: Update existing README.md files rather than creating new documentation
- **Repository cleanliness**: Keep repository root clean - only README.md unless user requests otherwise
- **Style**: Documentation should be concise, direct, and professional - avoid AI-generated tone
- **User preference**: Only create additional .md files when user specifically asks for documentation


---

# Docker Platform-Specific Guide

This skill provides detailed guidance on Docker differences, considerations, and optimizations for Windows, Linux, and macOS platforms.

## Linux

### Advantages

- **Native containers:** No virtualization layer overhead
- **Best performance:** Direct kernel features (cgroups, namespaces)
- **Full feature set:** All Docker features available
- **Production standard:** Most production deployments run on Linux
- **Flexibility:** Multiple distributions supported

### Platform Features

**Container Technologies:**
- Namespaces: PID, network, IPC, mount, UTS, user
- cgroups v1 and v2 for resource control
- Overlay2 storage driver (recommended)
- SELinux and AppArmor for mandatory access control

**Storage Drivers:**
```bash
# Check current driver
docker info | grep "Storage Driver"

# Recommended: overlay2
# /etc/docker/daemon.json
{
  "storage-driver": "overlay2"
}
```

### Linux-Specific Configuration

**Daemon Configuration** (`/etc/docker/daemon.json`):
```json
{
  "storage-driver": "overlay2",
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "live-restore": true,
  "userland-proxy": false,
  "userns-remap": "default",
  "icc": false,
  "default-ulimits": {
    "nofile": {
      "Name": "nofile",
      "Hard": 64000,
      "Soft": 64000
    }
  }
}
```

**User Namespace Remapping:**
```bash
# Enable in daemon.json
{
  "userns-remap": "default"
}

# Restart Docker
sudo systemctl restart docker

# Result: root in container = unprivileged user on host
```

### SELinux Integration

```bash
# Check SELinux status
sestatus

# Run container with SELinux enabled
docker run --security-opt label=type:svirt_sandbox_file_t myimage

# Volume labels
docker run -v /host/path:/container/path:z myimage  # Private label
docker run -v /host/path:/container/path:Z myimage  # Shared label
```

### AppArmor Integration

```bash
# Check AppArmor status
sudo aa-status

# Run with default Docker profile
docker run --security-opt apparmor=docker-default myimage

# Create custom profile
sudo aa-genprof docker run myimage
```

### Systemd Integration

```bash
# Check Docker service status
sudo systemctl status docker

# Enable on boot
sudo systemctl enable docker

# Restart Docker
sudo systemctl restart docker

# View logs
sudo journalctl -u docker -f

# Configure service
sudo systemctl edit docker
```

### cgroup v1 vs v2

```bash
# Check cgroup version
stat -fc %T /sys/fs/cgroup/

# If using cgroup v2, ensure Docker version >= 20.10

# /etc/docker/daemon.json
{
  "exec-opts": ["native.cgroupdriver=systemd"]
}
```

### Linux Distribution Specifics

**Ubuntu/Debian:**
```bash
# Install Docker
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

# Non-root user
sudo usermod -aG docker $USER
```

**RHEL/CentOS/Fedora:**
```bash
# Install Docker
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
sudo dnf install docker-ce docker-ce-cli containerd.io

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Non-root user
sudo usermod -aG docker $USER
```

**Alpine:**
```bash
# Install Docker
apk add docker docker-compose

# Start Docker
rc-update add docker boot
service docker start
```

## macOS

### Architecture

- **Docker Desktop:** Required (no native Docker on macOS)
- **Virtualization:** Uses HyperKit (Intel) or Virtualization.framework (Apple Silicon)
- **Linux VM:** Containers run in lightweight Linux VM
- **File sharing:** osxfs or VirtioFS for bind mounts

### macOS-Specific Considerations

**Resource Allocation:**
```
Docker Desktop → Preferences → Resources → Advanced
- CPUs: Allocate based on workload (default: half available)
- Memory: Allocate generously (default: 2GB, recommend 4-8GB)
- Swap: 1GB minimum
- Disk image size: 60GB+ for development
```

**File Sharing Performance:**

Traditional osxfs is slow. Improvements:
1. **VirtioFS:** Enable in Docker Desktop settings (faster)
2. **Delegated/Cached mounts:**

```yaml
volumes:
  # Host writes delayed (best for source code)
  - ./src:/app/src:delegated

  # Container writes cached (best for build outputs)
  - ./build:/app/build:cached

  # Default consistency (slowest but safest)
  - ./data:/app/data:consistent
```

**Network Access:**

```bash
# Access host from container
host.docker.internal

# Example: Connect to host PostgreSQL
docker run -e DATABASE_URL=postgresql://host.docker.internal:5432/db myapp
```

### Apple Silicon (M1/M2/M3) Specifics

**Architecture Considerations:**
```bash
# Check image architecture
docker image inspect node:20-alpine | grep Architecture

# M-series Macs are ARM64
# Some images only available for AMD64

# Build multi-platform
docker buildx build --platform linux/amd64,linux/arm64 -t myapp .

# Run AMD64 image on ARM (via emulation)
docker run --platform linux/amd64 myimage  # Slower
```

**Rosetta 2 Integration:**
```
Docker Desktop → Features in development → Use Rosetta for x86/amd64 emulation
```
Faster AMD64 emulation on Apple Silicon.

### macOS Docker Desktop Settings

**General:**
- ✅ Start Docker Desktop when you log in
- ✅ Use VirtioFS (better performance)
- ✅ Use Virtualization framework (Apple Silicon)

**Resources:**
```
CPUs: 4-6 (for development)
Memory: 6-8 GB (for development)
Swap: 1-2 GB
Disk image size: 100+ GB (grows dynamically)
```

**Docker Engine:**
```json
{
  "builder": {
    "gc": {
      "enabled": true,
      "defaultKeepStorage": "20GB"
    }
  },
  "experimental": false,
  "features": {
    "buildkit": true
  }
}
```

### macOS File Permissions

```bash
# macOS user ID and group ID
id -u  # Usually 501
id -g  # Usually 20

# Match in container
docker run --user 501:20 myimage

# Or in Dockerfile
RUN adduser -u 501 -g 20 appuser
USER appuser
```

### macOS Development Workflow

```yaml
# docker-compose.yml for development
version: '3.8'

services:
  app:
    build: .
    volumes:
      # Source code with delegated (better performance)
      - ./src:/app/src:delegated
      # node_modules in volume (much faster than bind mount)
      - node_modules:/app/node_modules
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development

volumes:
  node_modules:
```

### Common macOS Issues

**Problem:** Slow file sync
**Solution:**
- Use VirtioFS
- Use delegated/cached mounts
- Store dependencies in volumes (not bind mounts)

**Problem:** High CPU usage
**Solution:**
- Reduce file watching
- Exclude large directories from file sharing
- Allocate more resources

**Problem:** Port already in use
**Solution:**
```bash
# Find process using port
lsof -i :PORT
kill -9 PID
```

## Windows

### Windows Container Types

**1. Linux Containers on Windows (LCOW):**
- Most common for development
- Uses WSL2 or Hyper-V backend
- Runs Linux containers
- Good compatibility

**2. Windows Containers:**
- Native Windows containers
- For Windows-specific workloads
- Requires Windows Server base images
- Less common in development

### Windows Backend Options

**WSL2 Backend (Recommended):**
- Faster
- Better resource usage
- Native Linux kernel
- Requires Windows 10/11 (recent versions)

**Hyper-V Backend:**
- Older option
- More resource intensive
- Works on older Windows versions

### WSL2 Configuration

**Enable WSL2:**
```powershell
# Run as Administrator
wsl --install

# Or manually
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Set WSL2 as default
wsl --set-default-version 2

# Install Ubuntu (or other distro)
wsl --install -d Ubuntu
```

**Docker Desktop Integration:**
```
Settings → Resources → WSL Integration
- Enable integration with default distro
- Select additional distros
```

### Windows Path Considerations

**Path Formats:**
```bash
# Forward slashes (recommended, works everywhere)
docker run -v C:/Users/name/project:/app myimage

# Backslashes (need escaping in some contexts)
docker run -v C:\Users\name\project:/app myimage

# In docker-compose.yml (forward slashes)
volumes:
  - C:/Users/name/project:/app

# Or relative paths
volumes:
  - ./src:/app/src
```

### Git Bash / MINGW Path Conversion Issues

**CRITICAL ISSUE:** When using Docker in Git Bash (MINGW) on Windows, automatic path conversion breaks volume mounts.

**The Problem:**
```bash
# What you type in Git Bash:
docker run -v $(pwd):/app myimage

# What Git Bash converts it to (BROKEN):
docker run -v C:\Program Files\Git\d\repos\project:/app myimage
```

**Solutions:**

**1. MSYS_NO_PATHCONV (Recommended):**
```bash
# Per-command fix
MSYS_NO_PATHCONV=1 docker run -v $(pwd):/app myimage

# Session-wide fix (add to ~/.bashrc)
export MSYS_NO_PATHCONV=1

# Function wrapper (automatic for all Docker commands)
docker() {
  (export MSYS_NO_PATHCONV=1; command docker.exe "$@")
}
export -f docker
```

**2. Double Slash Workaround:**
```bash
# Use double leading slash to prevent conversion
docker run -v //c/Users/project:/app myimage

# Works with $(pwd) too
docker run -v //$(pwd):/app myimage
```

**3. Named Volumes (No Path Issues):**
```bash
# Named volumes work without any fixes
docker run -v my-data:/data myimage
```

**What Works Without Modification:**
- Docker Compose YAML files with relative paths
- Named volumes
- Network and image commands
- Container commands without volumes

**What Needs MSYS_NO_PATHCONV:**
- Bind mounts with `$(pwd)`
- Bind mounts with absolute Unix-style paths
- Volume mounts specified on command line

**Shell Detection:**
```bash
# Detect Git Bash/MINGW and auto-configure
if [ -n "$MSYSTEM" ] || [[ "$(uname -s)" == MINGW* ]]; then
  export MSYS_NO_PATHCONV=1
  echo "Git Bash detected - Docker path conversion fix enabled"
fi
```

**Recommended ~/.bashrc Configuration:**
```bash
# Docker on Git Bash fix
if [ -n "$MSYSTEM" ]; then
  export MSYS_NO_PATHCONV=1
fi
```

See the `docker-git-bash-guide` skill for comprehensive path conversion documentation, troubleshooting, and examples.

### Windows File Sharing

**Configure Shared Drives:**
```
Docker Desktop → Settings → Resources → File Sharing
Add: C:\, D:\, etc.
```

**Performance Considerations:**
- File sharing is slower than Linux/Mac
- Use WSL2 backend for better performance
- Store frequently accessed files in WSL2 filesystem

### Windows Line Endings

**Problem:** CRLF vs LF line endings

**Solution:**
```bash
# Git configuration
git config --global core.autocrlf input

# Or per-repo (.gitattributes)
* text=auto
*.sh text eol=lf
*.bat text eol=crlf
```

```dockerfile
# In Dockerfile for scripts
FROM alpine
COPY --chmod=755 script.sh /
# Ensure LF endings
RUN dos2unix /script.sh || sed -i 's/\r$//' /script.sh
```

### Windows Firewall

```powershell
# Allow Docker Desktop
New-NetFirewallRule -DisplayName "Docker Desktop" -Direction Inbound -Program "C:\Program Files\Docker\Docker\Docker Desktop.exe" -Action Allow

# Check blocked ports
netstat -ano | findstr :PORT
```

### Windows-Specific Docker Commands

```powershell
# Run PowerShell in container
docker run -it mcr.microsoft.com/powershell:lts-7.4-windowsservercore-ltsc2022

# Windows container example
docker run -it mcr.microsoft.com/windows/servercore:ltsc2022 cmd

# Check container type
docker info | Select-String "OSType"
```

### WSL2 Disk Management

**Problem:** WSL2 VHDX grows but doesn't shrink

**Solution:**
```powershell
# Stop Docker Desktop and WSL
wsl --shutdown

# Compact disk image (run as Administrator)
# Method 1: Optimize-VHD (requires Hyper-V tools)
Optimize-VHD -Path "$env:LOCALAPPDATA\Docker\wsl\data\ext4.vhdx" -Mode Full

# Method 2: diskpart
diskpart
# In diskpart:
select vdisk file="C:\Users\YourName\AppData\Local\Docker\wsl\data\ext4.vhdx"
attach vdisk readonly
compact vdisk
detach vdisk
exit
```

### Windows Development Workflow

```yaml
# docker-compose.yml for Windows
version: '3.8'

services:
  app:
    build: .
    volumes:
      # Use forward slashes
      - ./src:/app/src
      # Named volumes for better performance
      - node_modules:/app/node_modules
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    # Windows-specific: ensure proper line endings
    command: sh -c "dos2unix /app/scripts/*.sh && npm start"

volumes:
  node_modules:
```

### Common Windows Issues

**Problem:** Permission denied errors
**Solution:**
```powershell
# Run Docker Desktop as Administrator
# Or grant permissions to Docker Desktop
icacls "C:\ProgramData\DockerDesktop" /grant Users:F /T
```

**Problem:** Slow performance
**Solution:**
- Use WSL2 backend
- Store project in WSL2 filesystem (`\\wsl$\Ubuntu\home\user\project`)
- Use named volumes for node_modules, etc.

**Problem:** Path not found
**Solution:**
- Use forward slashes
- Ensure drive is shared in Docker Desktop
- Use absolute paths or `${PWD}`

## Platform Comparison

| Feature | Linux | macOS | Windows |
|---------|-------|-------|---------|
| **Performance** | Excellent (native) | Good (VM overhead) | Good (WSL2) to Fair (Hyper-V) |
| **File sharing** | Native | Slow (improving with VirtioFS) | Slow (better in WSL2) |
| **Resource efficiency** | Best | Good | Good (WSL2) |
| **Feature set** | Complete | Complete | Complete (LCOW) |
| **Production** | Standard | Dev only | Dev only (LCOW) |
| **Ease of use** | Moderate | Easy (Docker Desktop) | Easy (Docker Desktop) |
| **Cost** | Free | Free (Docker Desktop Personal) | Free (Docker Desktop Personal) |

## Cross-Platform Best Practices

### Multi-Platform Images

```bash
# Create buildx builder
docker buildx create --name multiplatform --driver docker-container --use

# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t myimage:latest \
  --push \
  .
```

### Platform-Agnostic Dockerfiles

```dockerfile
# Works on all platforms
FROM node:20-alpine

# Use COPY with --chmod (not RUN chmod, which is slower)
COPY --chmod=755 script.sh /usr/local/bin/

# Use environment variables for paths
ENV APP_HOME=/app
WORKDIR ${APP_HOME}

# Use exec form for CMD/ENTRYPOINT (works on Windows containers too)
CMD ["node", "server.js"]
```

### Cross-Platform Compose Files

```yaml
version: '3.8'

services:
  app:
    build: .
    volumes:
      # Relative paths work everywhere
      - ./src:/app/src
      # Named volumes (platform-agnostic)
      - data:/app/data
    environment:
      # Use environment variables
      - NODE_ENV=${NODE_ENV:-development}

volumes:
  data:
```

### Testing Across Platforms

```bash
# Test on different platforms with buildx
docker buildx build --platform linux/amd64 -t myapp:amd64 --load .
docker run --rm myapp:amd64

docker buildx build --platform linux/arm64 -t myapp:arm64 --load .
docker run --rm myapp:arm64
```

## Platform Selection Guide

**Choose Linux for:**
- Production deployments
- Maximum performance
- Full Docker feature set
- Minimal overhead
- CI/CD pipelines

**Choose macOS for:**
- Development on Mac hardware
- When you need macOS tools
- Docker Desktop ease of use
- M1/M2/M3 development

**Choose Windows for:**
- Development on Windows hardware
- Windows-specific applications
- When team uses Windows
- WSL2 for better Linux container support

This platform guide covers the major differences. Always test on your target deployment platform before going to production.
