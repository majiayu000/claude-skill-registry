---
name: gpg-signing
description: Comprehensive guide to GPG commit signing. Set up, configure, and troubleshoot GPG commit signing. Fix GPG signing errors, configure passphrase caching, verify commit signatures. Use when working with Git commit signing, GPG keys, commit verification, signature verification, GPG configuration, or when encountering GPG signing errors. Covers Windows (Gpg4win), macOS (GPG Suite), Linux (gnupg), and WSL installation and setup.
allowed-tools: Read, Bash, Glob, Grep
---

# Git GPG Signing

Comprehensive guidance for setting up, configuring, and troubleshooting GPG commit signing across all platforms.

## Table of Contents

- [Overview](#overview)
- [When to Use This Skill](#when-to-use-this-skill)
- [Quick Start](#quick-start)
- [Platform-Specific Setup](#platform-specific-setup)
- [Key Generation](#key-generation)
- [Git Configuration](#git-configuration)
- [Passphrase Caching](#passphrase-caching)
- [GitHub Integration](#github-integration)
- [Troubleshooting](#troubleshooting)
- [GPG Signing Methods Comparison](#gpg-signing-methods-comparison)
- [Security Best Practices](#security-best-practices)
- [Resources](#resources)
- [Related Skills](#related-skills)

## Overview

Git commit signing provides cryptographic proof that commits came from you. This skill helps you:

- Install and configure GPG tools on Windows, macOS, and Linux
- Set up commit signing with proper key management
- Configure passphrase caching for better workflow
- Troubleshoot common GPG signing issues
- Understand security trade-offs and best practices

## When to Use This Skill

This skill should be used when:

- Setting up GPG commit signing for the first time
- Configuring GPG tools (Gpg4win, GPG Suite, gnupg)
- Troubleshooting GPG signing errors ("gpg: signing failed", "inappropriate ioctl", etc.)
- Troubleshooting keyboxd daemon startup issues (Windows race condition)
- Determining which GPG installation Git is using
- Understanding Windows daemon startup behavior vs. official design
- Configuring passphrase caching to reduce prompts
- Understanding GPG vs SSH vs S/MIME signing methods
- Adding GPG keys to GitHub/GitLab/Bitbucket
- Resolving "Unverified" commits on GitHub
- Working with `.gnupg/gpg-agent.conf` configuration

## Quick Start

**Basic Setup (Single Personal Key):**

```bash
# 1. Install GPG (see Platform-Specific Setup below)

# 2. Generate key
gpg --full-generate-key
# Select: (9) ECC (sign and encrypt) → Curve 25519
# Expiration: 0 (no expiration)
# Passphrase: Strong 20+ character passphrase

# 3. Get key ID
gpg --list-secret-keys --keyid-format=long
# Look for "sec   ed25519/<KEY_ID>"

# 4. Configure Git
git config --global user.signingkey <KEY_ID>
git config --global commit.gpgsign true

# 5. Export public key and add to GitHub
gpg --armor --export <KEY_ID>
# Paste at: https://github.com/settings/keys
```

## Platform-Specific Setup

### Windows: Gpg4win Installation

**For detailed Windows setup**, see [references/windows-setup.md](references/windows-setup.md).

**Quick install:**

```powershell
# Option 1: Download installer
# https://gpg4win.org/thanks-for-download.html

# Option 2: winget
winget install --id GnuPG.Gpg4win -e --source winget

# Configure Git to use Gpg4win (adjust path if installed elsewhere)
git config --global gpg.program "C:/Program Files (x86)/GnuPG/bin/gpg.exe"
```

### macOS: GPG Suite / Homebrew

```bash
# Option 1: Homebrew (recommended)
brew install gnupg

# Option 2: GPG Suite
# Download from: https://gpgtools.org/

# Configure Git (if needed)
git config --global gpg.program $(which gpg)
```

### Linux: GnuPG

```bash
# Debian/Ubuntu
sudo apt update && sudo apt install gnupg

# Fedora/RHEL
sudo dnf install gnupg2

# Arch
sudo pacman -S gnupg
```

### WSL: Follow Linux Instructions

**WSL users:** Follow the Linux setup instructions above (WSL runs Linux). See troubleshooting section for WSL-specific issues if needed.

## Key Generation

### Personal Development Key (Interactive)

```bash
# Generate key interactively
gpg --full-generate-key

# Follow prompts:
# 1. Key type: (9) ECC (sign and encrypt) *default*
# 2. Curve: (1) Curve 25519 *default*
# 3. Expiration: 0 = no expiration (or 2y for 2 years)
# 4. Real name: Your Name
# 5. Email: your.verified@email.com
# 6. Comment: (optional, can leave blank)
# 7. Passphrase: Strong 20+ character passphrase

# List keys to get KEY_ID
gpg --list-secret-keys --keyid-format=long
# Look for "sec   ed25519/<KEY_ID>"
```

**Recommended algorithm:** EdDSA using Curve25519 (Ed25519) - modern, fast, small keys, excellent security

**Alternative:** RSA 4096-bit (traditional, widely compatible)

### Exporting Keys

```bash
# Export public key (for GitHub)
gpg --armor --export <KEY_ID>

# Export private key (for backup only - KEEP SECURE!)
gpg --armor --export-secret-keys <KEY_ID>
```

## Git Configuration

### Enable Commit Signing

```bash
# Global (all repositories)
git config --global user.signingkey <KEY_ID>
git config --global commit.gpgsign true
git config --global tag.gpgSign true

# Repository-local (specific repo)
cd /path/to/repo
git config user.signingkey <KEY_ID>
git config commit.gpgsign true
```

### Verify Configuration

```bash
# Check configured key
git config --global user.signingkey

# Test signing
git commit --allow-empty -m "Test GPG signing"

# Verify signature
git log --show-signature -1
```

## Passphrase Caching

GPG agent caches passphrases to reduce how often you're prompted.

**Check if config exists:**

```bash
ls ~/.gnupg/gpg-agent.conf
```

**Create or edit** `~/.gnupg/gpg-agent.conf`:

```conf
# Cache passphrase for 8 hours of inactivity
default-cache-ttl 28800

# Maximum cache time of 24 hours regardless of use
max-cache-ttl 86400

# Allow pinentry to cache the passphrase
allow-preset-passphrase
```

**Apply changes:**

```bash
gpgconf --kill gpg-agent
gpgconf --launch gpg-agent
```

**For comprehensive caching configuration**, including security scenarios, testing procedures, and troubleshooting, see [references/passphrase-caching.md](references/passphrase-caching.md).

### Windows-Specific: Dual GPG Installation Issue

**CRITICAL for Windows users:** Windows typically has **two separate GPG installations** (Gpg4win and Git Bash GPG), each with different config file locations:

- **Gpg4win:** `%APPDATA%\gnupg\gpg-agent.conf` (typically `C:\Users\<Username>\AppData\Roaming\gnupg\gpg-agent.conf`)
- **Git Bash GPG:** `~/.gnupg/gpg-agent.conf` (resolves to `C:\Users\<Username>\.gnupg\gpg-agent.conf`)

**Common problem:** Configuring `~/.gnupg/gpg-agent.conf` (Git Bash GPG) when Git is configured to use Gpg4win. Result: **configuration silently ignored, caching doesn't work**.

**Verify which GPG Git is using:**

```bash
# Check Git's GPG configuration
git config --global gpg.program

# If output is "C:/Program Files (x86)/GnuPG/bin/gpg.exe":
# → Use: %APPDATA%\gnupg\gpg-agent.conf

# Verify GPG's config directory
gpgconf --list-dirs homedir
```

**Windows configuration must include pinentry-program:**

```conf
# Example: %APPDATA%\gnupg\gpg-agent.conf
default-cache-ttl 28800
max-cache-ttl 86400
allow-preset-passphrase

# REQUIRED for Windows:
pinentry-program C:/Program Files (x86)/GnuPG/bin/pinentry-basic.exe
```

**See:** [Windows Setup Guide - Dual GPG Installations](references/windows-setup.md) for detailed explanation.

### Recommended Cache Durations

| Scenario | default-cache-ttl | max-cache-ttl | Rationale |
| --- | --- | --- | --- |
| **High Security** | 900 (15 min) | 3600 (1 hour) | Prompt frequently, short window |
| **Balanced** | 3600 (1 hour) | 28800 (8 hours) | Prompt every ~hour, expires by end of day |
| **Convenience** | 28800 (8 hours) | 86400 (24 hours) | Prompt once per workday, expires daily |

## GitHub Integration

### Adding GPG Key to GitHub

1. **Export public key:**

   ```bash
   gpg --armor --export <KEY_ID>
   ```

2. **Add to GitHub:**
   - Go to: [https://github.com/settings/keys](https://github.com/settings/keys)
   - Click "New GPG key"
   - Paste ASCII-armored public key
   - Click "Add GPG key"

3. **Verify email matches:**
   - Git email must match GPG key email
   - Email must be verified in GitHub account

   ```bash
   # Check Git email
   git config --global user.email

   # Check GPG key email
   gpg --list-keys <KEY_ID>
   ```

### Troubleshooting "Unverified" Commits

**Possible causes:**

1. **Public key not added to GitHub** → Add key at Settings → SSH and GPG keys
2. **Email mismatch** → Ensure Git email = GPG key email = GitHub verified email
3. **Key expired** → Extend expiration or generate new key
4. **Key revoked** → Generate new key (cannot un-revoke)

## Troubleshooting

**For comprehensive troubleshooting**, see [references/troubleshooting.md](references/troubleshooting.md).

### "gpg: signing failed: No secret key"

**Cause:** Git configured to use key ID that doesn't exist in keyring.

**Solution:**

```bash
# List available keys
gpg --list-secret-keys --keyid-format=long

# Verify Git config matches available key
git config --global user.signingkey

# If mismatch, update config
git config --global user.signingkey <CORRECT_KEY_ID>
```

### "gpg: signing failed: Inappropriate ioctl for device"

**Cause:** GPG agent cannot prompt for passphrase (terminal issue).

**Solution (Linux/macOS/WSL):**

```bash
# Set GPG_TTY environment variable
export GPG_TTY=$(tty)

# Add to shell profile (e.g., ~/.bashrc, ~/.zshrc)
echo 'export GPG_TTY=$(tty)' >> ~/.bashrc
```

**Solution (Windows with Gpg4win):**

```bash
# Use GUI pinentry (adjust path to match your Gpg4win installation)
echo 'pinentry-program "C:/Program Files (x86)/GnuPG/bin/pinentry-basic.exe"' >> ~/.gnupg/gpg-agent.conf
gpgconf --kill gpg-agent
```

### "error: gpg failed to sign the data"

**Debug steps:**

```bash
# Test GPG signing directly
echo "test" | gpg --clearsign

# Check GPG agent status
gpgconf --list-components

# Check key expiration
gpg --list-keys --keyid-format=long <KEY_ID>

# Restart GPG agent
gpgconf --kill gpg-agent
gpgconf --launch gpg-agent

# Try commit again
git commit -m "test"
```

### Passphrase Prompt Every Commit (Cache Not Working)

**Windows users:** This is commonly caused by dual GPG installation issues. See [Windows Setup - Passphrase Caching Troubleshooting](references/windows-setup.md) and [Troubleshooting - Windows Caching Issue](references/troubleshooting.md) for detailed diagnosis.

**Possible causes:**

1. **Wrong config file location (Windows):**

   ```bash
   # Verify which GPG Git is using
   git config --global gpg.program

   # Check GPG's config directory
   gpgconf --list-dirs homedir

   # Ensure config exists at correct location
   # Windows (Gpg4win): %APPDATA%\gnupg\gpg-agent.conf
   # Windows (Git Bash): ~/.gnupg/gpg-agent.conf
   # Linux/macOS/WSL: ~/.gnupg/gpg-agent.conf
   ```

2. **gpg-agent.conf not loaded:**

   ```bash
   # Restart agent to load config
   gpgconf --kill gpg-agent
   gpgconf --launch gpg-agent

   # Verify config loaded
   gpgconf --list-options gpg-agent | grep cache-ttl
   ```

3. **Cache TTL set too low** → Increase cache time in `~/.gnupg/gpg-agent.conf`

4. **Multiple GPG agents running:**

   ```bash
   # Kill all agents
   pkill gpg-agent

   # Launch single agent
   gpgconf --launch gpg-agent
   ```

## GPG Signing Methods Comparison

| Method | Best For | Setup Complexity | Key Management |
| --- | --- | --- | --- |
| **GPG** | Full-featured, supports expiration/revocation | Medium | Most flexible |
| **SSH** | Simplest, reuses existing SSH keys | Low | Limited features |
| **S/MIME** | Enterprise with X.509 certificates | High | Org-managed |

### SSH Signing (Alternative)

**When to use SSH instead of GPG:**

- Simple personal projects
- Already have SSH key setup
- Don't need expiration/revocation features
- Want minimal configuration

**Setup:**

```bash
# Configure Git to use SSH signing
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true

# Add SSH key to GitHub as "Signing Key"
```

**Limitations:**

- No key expiration support
- No revocation tracking
- Requires Git 2.34+ (2021)

## Security Best Practices

**For comprehensive security guidance**, see [references/security-best-practices.md](references/security-best-practices.md).

**Quick recommendations:**

- ✅ Use passphrase protection on personal keys (minimum 20 characters)
- ✅ Configure caching to balance security and convenience (4-8 hours)
- ✅ Consider key expiration: No expiration for personal projects, 1-year for enterprise work
- ✅ Backup private key to encrypted vault or password manager's Secure Documents
- ⚠️ Never store unencrypted keys in Git repos, cloud storage, or email

## Resources

### Reference Documentation

- [Quick Command Reference](references/quick-reference.md) - Quick lookup for common GPG and Git signing commands
- [Windows Setup Guide](references/windows-setup.md) - Gpg4win installation, Git Bash paths, security considerations
- [Passphrase Caching Configuration](references/passphrase-caching.md) - Cache strategies, security trade-offs
- [Security Best Practices](references/security-best-practices.md) - Passphrase protection, key expiration, backup strategies
- [Troubleshooting Guide](references/troubleshooting.md) - Common issues and solutions
- [GPG Agent Configuration Example](references/gpg-agent-config-example.conf) - Sample configuration file
- [Test Scenarios](references/test-scenarios.md) - Skill activation validation scenarios

### Official Documentation

- [GitHub: Managing commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification)
- [GnuPG Documentation](https://www.gnupg.org/documentation/)
- [Git Documentation: Signing Your Work](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work)

## Related Skills

- **git-commit**: Use for complete git commit workflow with Conventional Commits format, safety protocols, and attribution requirements
- **config**: Advanced Git configuration including aliases, credentials, and performance tuning
- **gpg-multi-key**: Multi-key management for consultants, CI/CD automation, and enterprise teams

## Version History

- v1.1.1 (2025-11-25): Progressive disclosure optimization - extracted Test Scenarios to reference file, removed redundant Quick Command Reference section, reduced SKILL.md to under 500 lines
- v1.1.0 (2025-11-22): Enhanced troubleshooting - added keyboxd daemon race condition troubleshooting (T7777/T7829), dynamic GPG detection workflow, Windows startup best practices with official design vs. reality analysis
- v1.0.5 (2025-11-19): Optimization improvements - added table of contents to SKILL.md, extracted Essential Commands Reference to quick-reference.md, reduced line count from 530 to 522
- v1.0.4 (2025-11-17): Progressive disclosure improvement - extracted Security Best Practices to separate reference file
- v1.0.3 (2025-11-17): Validated against official documentation - fixed tag.gpgSign capitalization, updated Last Verified dates
- v1.0.2 (2025-11-12): Enhanced documentation - added TOCs to long references, documented test scenarios
- v1.0.1 (2025-11-13): Added cross-reference to git-commit skill
- v1.0.0 (2025-01-09): Initial release migrated from repository documentation

## Last Updated

**Date:** 2025-11-28
**Model:** claude-opus-4-5-20251101
