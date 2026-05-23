---
name: setting-up-hetzner
description: Use when setting up a new machine to work with this repo, or when hcloud context is missing, or direnv isn't loading token
---

# Setting Up Hetzner Dev Infrastructure

## Overview

Prerequisites and first-time setup for working with this repo.

## Prerequisites

Install required tools:

```bash
brew install hcloud direnv nix
```

## First-Time Setup

**Step 1: Create hcloud context**

```bash
hcloud context create workstation
# Enter your API token when prompted
```

Get token from: https://console.hetzner.cloud → Project → Access → API Tokens → Generate (Read & Write)

**Step 2: Allow direnv**

```bash
cd ~/Code/workstation
direnv allow
```

This loads `HCLOUD_TOKEN` from your hcloud CLI context.

## Verify Setup

```bash
# Check token is loaded
echo $HCLOUD_TOKEN | head -c 10

# Check hcloud can connect
hcloud server list
```

## Common Issues

### "context not found"

```bash
hcloud context list
# If empty:
hcloud context create workstation
```

### "direnv: error .envrc"

```bash
direnv allow
```

### Python version error

The `.envrc` requires Python 3.11+ for `tomllib`. Check:

```bash
python3 --version
```

## SSH Key Setup

Ensure your SSH key is registered with Hetzner:

```bash
hcloud ssh-key list
# If 'devbox' key is missing:
hcloud ssh-key create --name devbox --public-key-from-file ~/.ssh/id_ed25519.pub
```
