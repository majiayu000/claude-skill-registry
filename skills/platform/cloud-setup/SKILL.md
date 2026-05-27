---
name: Cloud Environment Setup
description: Set up Claude Code cloud/mobile environments for AILANG development. Use when starting a new cloud session, when tools are missing (Go, make, gh), or when user says "setup cloud", "setup environment", or mentions mobile Claude Code.
---

# Cloud Environment Setup

Set up a fresh cloud/mobile Claude Code environment with all tools needed for AILANG development.

## Quick Start

Run the setup script to install all required tools:

```bash
.claude/skills/cloud-setup/scripts/setup.sh
```

Or verify an existing environment:

```bash
.claude/skills/cloud-setup/scripts/verify.sh
```

## When to Use This Skill

Use this skill when:
- Starting a new cloud/mobile Claude Code session
- `go`, `make`, or `gh` commands are not found
- User says "setup cloud", "setup environment", "install tools"
- Build commands fail due to missing tools
- User mentions "mobile Claude Code" or "cloud environment"

## Environment Requirements

### Required Tools

| Tool | Purpose | Minimum Version |
|------|---------|-----------------|
| **Go** | Build AILANG | 1.24+ |
| **make** | Build automation | GNU Make 4+ |
| **gh** | GitHub CLI | 2.0+ |
| **git** | Version control | 2.0+ |

### Resource Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| RAM | 4 GB | 8+ GB |
| Disk | 5 GB free | 10+ GB |
| CPUs | 2 | 4+ |
| Network | Required | Required |

## Setup Workflow

### Step 1: Assess Current Environment

```bash
# Check what's available
which go make gh git 2>/dev/null
go version 2>/dev/null
```

### Step 2: Fix DNS (if needed)

Cloud environments sometimes have broken DNS. Fix with:

```bash
echo "nameserver 8.8.8.8" > /etc/resolv.conf
echo "nameserver 8.8.4.4" >> /etc/resolv.conf
```

### Step 3: Install Go

```bash
# Install via apt (may get older version)
apt-get update && apt-get install -y golang-go make

# OR install specific version directly
wget --no-check-certificate https://go.dev/dl/go1.24.4.linux-amd64.tar.gz -O /tmp/go.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf /tmp/go.tar.gz
export PATH=/usr/local/go/bin:$PATH
```

### Step 4: Install GitHub CLI

```bash
# Download and install
curl -L https://github.com/cli/cli/releases/download/v2.63.2/gh_2.63.2_linux_amd64.tar.gz -o /tmp/gh.tar.gz
tar -xzf /tmp/gh.tar.gz -C /tmp
mv /tmp/gh_*/bin/gh /usr/local/bin/
rm -rf /tmp/gh*
```

### Step 5: Configure Go Environment

```bash
export PATH=/usr/local/go/bin:$PATH
export GOTOOLCHAIN=local      # Prevent auto-download of newer Go
export GOPROXY=direct         # Bypass proxy if blocked
```

### Step 6: Build AILANG

```bash
# Download dependencies
go mod download

# Build
make build

# Verify
./bin/ailang run examples/runnable/hello.ail
```

## Available Scripts

### `scripts/setup.sh`

Full automated setup - installs Go, make, gh, and builds AILANG.

**Usage:**
```bash
.claude/skills/cloud-setup/scripts/setup.sh
```

**What it does:**
1. Checks current environment
2. Fixes DNS if needed
3. Installs Go 1.24.4
4. Installs make
5. Installs GitHub CLI
6. Downloads Go modules
7. Builds AILANG
8. Runs verification

### `scripts/verify.sh`

Verify environment is correctly set up.

**Usage:**
```bash
.claude/skills/cloud-setup/scripts/verify.sh
```

**Checks:**
- Go version and PATH
- make availability
- gh CLI availability
- AILANG binary exists
- AILANG can run examples
- Core tests pass

## Resources

### Troubleshooting Guide
See [`resources/troubleshooting.md`](resources/troubleshooting.md) for common issues and solutions.

## Known Issues

### 1. Go Toolchain Auto-Download

**Symptom:** Go tries to download newer toolchain, fails with network error

**Solution:** Set `GOTOOLCHAIN=local`

### 2. DNS Resolution Failures

**Symptom:** `dial tcp: lookup ... on [::1]:53: connection refused`

**Solution:** Add Google DNS to `/etc/resolv.conf`:
```bash
echo "nameserver 8.8.8.8" > /etc/resolv.conf
```

### 3. Go Module Proxy Blocked

**Symptom:** Timeout connecting to `proxy.golang.org` or `storage.googleapis.com`

**Solution:** Use direct downloads:
```bash
export GOPROXY=direct
go mod download
```

### 4. SSL/TLS Handshake Failures

**Symptom:** `curl: (35) ... sslv3 alert handshake failure`

**Solution:** Use `wget --no-check-certificate` instead of `curl`

### 5. Missing Basic Commands

**Symptom:** `head`, `tail`, `grep` not found

**Solution:** Either install coreutils or avoid piping:
```bash
# Instead of: command | head -20
# Just run: command
# And manually inspect output
```

## Post-Setup Checklist

After setup, verify you can:

- [ ] `go version` shows 1.24+
- [ ] `make --version` works
- [ ] `gh --version` works
- [ ] `./bin/ailang run examples/runnable/hello.ail` outputs "Hello, AILANG!"
- [ ] `go test ./internal/lexer/...` passes

## Environment Variables

Set these in your session for reliable builds:

```bash
export PATH=/usr/local/go/bin:$PATH
export GOTOOLCHAIN=local
export GOPROXY=direct
```

## What You Can Do After Setup

With environment configured, you can:

1. **Build AILANG**: `make build`
2. **Run programs**: `./bin/ailang run --caps IO file.ail`
3. **Run tests**: `go test ./internal/...`
4. **Work on design docs**: Full read/write access
5. **Commit and push**: Git operations work
6. **UI development**: Node/npm available for `ui/` work
