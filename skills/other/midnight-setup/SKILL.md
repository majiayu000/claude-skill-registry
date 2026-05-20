---
name: midnight-tooling:midnight-setup
description: Use when setting up Midnight development environment, installing Compact compiler and developer tools, configuring proof server, verifying prerequisites, or getting started with Midnight development.
---

# Midnight Development Environment Setup

Guide developers through setting up a complete Midnight development environment for building zero-knowledge smart contracts and dApps.

## Prerequisites Overview

Before installing Midnight-specific tools, verify these prerequisites:

| Requirement | Minimum | Recommended | Check Command |
|------------|---------|-------------|---------------|
| Node.js | 18.x | 20.x LTS | `node --version` |
| npm | 9.x | Latest | `npm --version` |
| Docker | 20.x | Latest | `docker --version` |
| Git | 2.x | Latest | `git --version` |
| Chrome | Latest | Latest | Required for Lace wallet |

Run the prerequisite check script to verify:
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/midnight-setup/scripts/check-prerequisites.sh
```

For detailed prerequisite verification:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/midnight-setup/scripts/check-prerequisites.py
```

## Installation Steps

### 1. Install Node.js via nvm (Recommended)

Using nvm provides easy version management:

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Restart terminal or source profile
source ~/.zshrc  # or ~/.bashrc

# Install Node.js 18 LTS
nvm install 18 --lts
nvm alias default 18
```

**Important**: After installing or switching Node versions, open a new terminal window. Simply sourcing the profile may leave stale references.

### 2. Install Docker Desktop

Download from [docker.com/products/docker-desktop](https://docker.com/products/docker-desktop/) for your platform. After installation:

1. Launch Docker Desktop
2. Wait for the Docker daemon to start
3. Verify with `docker info`

### 3. Install Compact Developer Tools

The Compact developer tools manage compiler versions and provide the `compact` CLI:

```bash
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/midnightntwrk/compact/releases/latest/download/compact-installer.sh | sh
```

After installation, add the binary to your PATH. The installer will show the exact path, typically:

```bash
# Add to ~/.zshrc or ~/.bashrc
export PATH="$HOME/.compact/bin:$PATH"
```

Then restart your terminal or source the profile.

### 4. Install the Compact Compiler

With the developer tools installed, download the compiler:

```bash
# Download latest compiler
compact update

# Verify installation
compact --version          # Shows developer tools version
compact compile --version  # Shows compiler version
```

### 5. Pull the Proof Server Image

The proof server generates zero-knowledge proofs locally:

```bash
docker pull midnightnetwork/proof-server:latest
```

To start the proof server (when needed for development):

```bash
docker run -p 6300:6300 midnightnetwork/proof-server -- midnight-proof-server --network testnet
```

### 6. Install VS Code Extension (Optional)

The Midnight Compact VS Code extension provides syntax highlighting and IntelliSense:

1. Download the `.vsix` file from the [Compact releases](https://github.com/midnightntwrk/compact/releases)
2. In VS Code: Extensions → "..." menu → "Install from VSIX..."
3. Select the downloaded file

### 7. Install Lace Midnight Preview Wallet (Optional)

For testing dApps with a wallet:

1. Install from Chrome Web Store: search "Lace Midnight"
2. Create a new wallet and save seed phrase securely
3. Get test tokens from [midnight.network/test-faucet/](https://midnight.network/test-faucet/)

## Verification

After completing setup, verify everything works:

```bash
# Check all tools
node --version      # Should be 18+
docker info         # Should show Docker running
compact --version   # Should show developer tools version
compact compile --version  # Should show compiler version

# Check proof server image
docker images | grep proof-server
```

Or run the environment check command: `/midnight:check`

## Compact Developer Tools Reference

| Command | Purpose |
|---------|---------|
| `compact update` | Download/update to latest compiler |
| `compact update <version>` | Switch to specific version |
| `compact list` | Show all available versions |
| `compact list --installed` | Show locally installed versions |
| `compact check` | Check for updates without downloading |
| `compact compile <file> <outdir>` | Compile a contract |
| `compact compile +0.25.0 <file> <outdir>` | Compile with specific version |
| `compact self update` | Update the developer tools themselves |
| `compact help` | Show help |

## Common Setup Issues

| Issue | Solution |
|-------|----------|
| `compact: command not found` | Add `~/.compact/bin` to PATH, restart terminal |
| Node version wrong after install | Open a **new** terminal window |
| Docker daemon not running | Start Docker Desktop application |
| Proof server won't start | Check Docker is running, port 6300 is free |

## Additional Resources

- **`references/installation-steps.md`** - Detailed platform-specific instructions
- **`references/bun-setup.md`** - Alternative setup using Bun runtime

For troubleshooting, use the `/midnight:doctor` command or consult the `midnight-debugging` skill.
