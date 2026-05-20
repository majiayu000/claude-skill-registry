---
name: gpg-multi-key
description: Advanced GPG multi-key management strategies for consultants, CI/CD automation, and enterprise teams. Configure, set up, run, and execute multi-key GPG workflows. Use when managing multiple GPG keys (personal + automation, per-client keys, enterprise keys), configuring CI/CD commit signing, implementing per-client key isolation, using conditional Git includes, setting up automated signing, or scaling GPG key strategies beyond single-key setups.
allowed-tools: Read, Bash, Glob, Grep
---

# GPG Multi-Key

Advanced strategies for managing multiple GPG keys across different contexts: personal development, CI/CD automation, multi-client consultant work, and enterprise environments.

## Overview

Multi-key GPG strategies enable:

- **Separation of concerns:** Personal vs automation vs client keys
- **Risk isolation:** Compromised key in one context doesn't affect others
- **Identity management:** Different email addresses for different clients
- **Security flexibility:** Different passphrase/expiration policies per context

This skill covers scaling from single-key (basic setup) to sophisticated multi-key architectures.

## When to Use This Skill

This skill should be used when:

- Setting up CI/CD automation with GPG signing (GitHub Actions, GitLab CI)
- Managing multiple client identities as a consultant
- Implementing per-client key isolation strategies
- Configuring Git conditional includes for automatic key switching
- Planning GPG key strategies for growing teams
- Balancing security (passphrase protection) with automation (no passphrase)
- Migrating from single-key to multi-key setup
- Understanding security trade-offs for different key types

## Prerequisites

Before using multi-key GPG strategies:

- **GPG installed:** Run `gpg --version` (should show GnuPG 2.2+)
- **Git installed:** Run `git --version` (should show Git 2.23+ for conditional includes)
- **Basic GPG familiarity:** See `git:gpg-signing` skill for single-key setup basics
- **For CI/CD scenarios:** GitHub/GitLab repository access and Secrets management permissions
- **For consultant scenarios:** Organized directory structure (`~/Clients/` recommended)

## Strategy Selection Guide

### Quick Decision Matrix

| Scenario | Keys Needed | Passphrase | Expiration | Reference |
| --- | --- | --- | --- | --- |
| **Personal development only** | 1 key | Yes | No (or 2y) | Basic Setup |
| **Personal + CI/CD** | 2 keys | Personal: Yes, Automation: No | No | [Scenario 2](#scenario-2-personal--cicd-automation) |
| **Multi-client consultant** | 3+ keys | All: Yes | 1 year | [Scenario 3](#scenario-3-multi-client-consultant) |
| **Enterprise team** | 1 key | Yes | 1 year | [Scenario 4](#scenario-4-enterprise-environment) |

### Quick Decision Flowchart

```text
Are you a new GPG user?
├─ YES → Use gpg-signing skill first
└─ NO → Continue below

Do you need multiple keys?
├─ NO → Use gpg-signing skill (Scenario 1)
└─ YES → Continue below

Which applies to you?
├─ Personal projects + CI/CD automation → Scenario 2 (Personal + CI/CD)
├─ Multiple clients (consultant/contractor) → Scenario 3 (Multi-Client)
├─ Corporate/regulated environment → Scenario 4 (Enterprise)
└─ Unsure? → See references/scenarios.md for detailed comparison
```

## Scenario 1: Basic Setup (Single Personal Key)

**For basic single-key setup**, use the `git:gpg-signing` skill instead.

**If you're new to GPG signing**, start with the `git:gpg-signing` skill to:

- Install and configure GPG
- Generate your first signing key
- Set up Git commit signing
- Understand passphrase caching

Then return to this skill when you need multiple keys (CI/CD, clients, enterprise).

## Scenario 2: Personal + CI/CD Automation

**Two-Key Strategy:**

- **Key 1: Personal Development** - Passphrase-protected, used for interactive commits
- **Key 2: CI/CD Automation** - No passphrase (required for unattended operation), stored in GitHub Secrets

**Quick Setup:**

1. Generate automation key (no passphrase)
2. Export private key: `gpg --armor --export-secret-keys <KEY_ID> > automation-private.asc`
3. Store in GitHub Secrets → GPG_PRIVATE_KEY
4. Configure GitHub Actions to import and use key

**Security trade-off:** Automation key has NO passphrase (required for unattended operation), but is isolated from personal key and stored in encrypted GitHub Secrets.

**Full workflow:** See [references/scenarios.md#scenario-2-personal--cicd](references/scenarios.md)

## Scenario 3: Multi-Client Consultant

**Per-Client Key Strategy:**

- Different GPG key for each client
- Automatic key switching by directory (Git conditional includes)
- Identity isolation (Client A commits ≠ Client B commits)

**Directory Structure:**

```text
~/Clients/
├── ClientA/
│   ├── .gitconfig-clienta
│   └── projects/
└── ClientB/
    ├── .gitconfig-clientb
    └── projects/
```

**Automatic Switching:**

Global `~/.gitconfig` uses `includeIf` to load per-client configs based on directory.

**Quick Setup:**

1. Generate key per client (1-year expiration recommended)
2. Configure conditional includes in `~/.gitconfig`
3. Create `.gitconfig-clienta` with client-specific key
4. Test automatic switching: `cd ~/Clients/ClientA && git config user.signingkey`

**Full workflow:** See [references/scenarios.md#scenario-3-multi-client-consultant](references/scenarios.md)

## Scenario 4: Enterprise Environment

**Follow Enterprise Policy:**

Your organization will specify:

- Key algorithm and size (RSA 4096, Ed25519)
- Expiration period (typically 6-12 months)
- Passphrase requirements
- Backup and revocation procedures
- Hardware security key requirements (YubiKey/Nitrokey)

**Typical Requirements:**

- **Algorithm:** RSA 4096-bit (compatibility) or Ed25519 (modern)
- **Expiration:** 1 year (policy-driven rotation)
- **Passphrase:** Required (per complexity rules)
- **Revocation certificate:** Filed with IT
- **Backup:** IT-managed or approved vault

**Full workflow:** See [references/scenarios.md#scenario-4-enterprise-environment](references/scenarios.md)

## How Git Chooses Which Key

**Key Selection Order:**

1. **Repository-local config** (`.git/config` in specific repo)
2. **Conditional includes** (`.gitconfig` with `includeIf`)
3. **Global config** (`~/.gitconfig`)

## Multi-Key Management

### List All Keys

```bash
# List all secret (private) keys
gpg --list-secret-keys --keyid-format=long
```

### Adding Multiple Keys to GitHub

GitHub allows unlimited GPG keys per account.

**Steps:**

1. Export each public key: `gpg --armor --export <KEY_ID>`
2. Add to GitHub: Settings → SSH and GPG keys → New GPG key
3. Paste ASCII-armored public key
4. Repeat for each key

**Email Verification:** Add all work emails to GitHub account and verify each. Commits signed with unverified email show "Unverified".

## Quick Command Reference

Common multi-key operations:

```bash
# List all keys
gpg --list-secret-keys --keyid-format=long

# Check which key Git is using
git config user.signingkey
git config user.email

# Switch key for specific repo
cd /path/to/repo
git config user.signingkey <KEY_ID>

# Test key switching with conditional includes
cd ~/Clients/ClientA/project
git config user.signingkey  # Should show CLIENT_A_KEY_ID

# Verify commit signature
git log --show-signature -1

# Export key for backup
gpg --armor --export-secret-keys <KEY_ID> > backup.asc
```

## Backup and Recovery

**Essential Backups:**

- Private keys (all keys - personal, automation, client)
- Revocation certificates (for each key)
- Passphrases (in password manager, NOT with backup)

**Quick Backup:**

```bash
# Export all private keys (encrypted)
gpg --armor --export-secret-keys > gpg-all-keys-backup.asc
gpg --symmetric --cipher-algo AES256 gpg-all-keys-backup.asc

# Secure storage locations
# ✅ Password manager (1Password, Bitwarden)
# ✅ Encrypted vault (VeraCrypt, Cryptomator)
# ✅ Hardware encrypted USB (in safe)
```

**Recovery:**

```bash
# Decrypt and import
gpg --decrypt gpg-all-keys-backup.asc.gpg > gpg-all-keys-backup.asc
gpg --import gpg-all-keys-backup.asc
```

**Full procedures:** See [references/backup-recovery.md](references/backup-recovery.md)

## Security Best Practices

### Passphrase Protection Strategy

| Key Type | Passphrase | Rationale |
| --- | --- | --- |
| **Personal** | YES (20+ chars) | Defense-in-depth, laptop security |
| **Automation** | NO | Required for unattended CI/CD |
| **Per-Client** | YES (20+ chars) | Client data requires high security |
| **Enterprise** | YES (per policy) | Compliance requirement |

### Expiration Strategy

| Context | Expiration | Rationale |
| --- | --- | --- |
| **Personal projects** | No expiration | GitHub default, manual rotation |
| **Automation** | No expiration | Simplicity, rotate if compromised |
| **Per-client** | 1 year | Enterprise best practice, forces review |
| **Enterprise** | Per policy | Typically 6 months to 1 year |

### Key Separation Benefits

**Why use multiple keys:**

- ✅ Compromised automation key doesn't affect personal key
- ✅ Client key compromise isolated to that client only
- ✅ Different security policies per context (passphrase, expiration)
- ✅ Identity isolation (correct email per client)
- ✅ Can revoke/rotate individual keys without affecting others

## Security Trade-offs Summary

| Decision | Security | Convenience | Recommendation |
| --- | --- | --- | --- |
| **Passphrase on personal key** | ✅ High | ⚠️ Requires entry | ✅ Always use |
| **Passphrase on automation key** | ❌ Single-factor | ✅ Unattended operation | ✅ Required for CI/CD |
| **Key expiration** | ✅ Limits exposure | ⚠️ Rotation overhead | ⚠️ Depends on context |
| **Per-client keys** | ✅ Isolation | ❌ Management overhead | ✅ For consultants |
| **Hardware keys (YubiKey)** | ✅ Maximum security | ❌ Physical dependency | ⚠️ Enterprise only |

**General principle:** Use strongest security that doesn't prevent the task from being accomplished.

## Common Questions & Quick Answers

### When should I use multiple keys instead of one?

Use multiple keys when:

- **Personal + CI/CD:** Need unattended signing (automation key can't have passphrase)
- **Multiple clients:** Different email/identity per client (consultant scenario)
- **Enterprise:** Organizational policy requires key rotation or isolation
- **Never:** Single project → stick with one key (use gpg-signing skill)

### What's the difference between automation and personal keys?

| Aspect | Personal Key | Automation Key |
| --- | --- | --- |
| **Passphrase** | YES (protection) | NO (required for unattended CI/CD) |
| **Storage** | Local GPG keyring | GitHub/GitLab Secrets |
| **Usage** | Interactive development | Automated workflows only |
| **Compromise risk** | Affects personal commits | Affects only automation commits |

### How do I switch between keys?

**Automatic (recommended):** Use Git conditional includes with directory-based switching
**Manual:** `git config user.signingkey <KEY_ID>` for specific repo
**Global:** `git config --global user.signingkey <KEY_ID>` for all repos

### Is it safe to store automation keys in GitHub Secrets?

Yes, with caveats:

- ✅ GitHub Secrets are encrypted at rest and in transit
- ✅ Only visible to authorized team members
- ⚠️ Key has no passphrase (single factor)
- ✅ Mitigated by: using separate key from personal key (isolation)

## Resources

### Internal References

- [Multi-Key Scenarios Comparison](references/scenarios.md)
- [Real-World Implementation Example](references/implementation-example.md)
- [Backup and Recovery Guide](references/backup-recovery.md)

### Official Documentation

- [GitHub: Managing commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification)
- [Git Conditional Includes](https://git-scm.com/docs/git-config#_conditional_includes)
- [GnuPG Documentation](https://www.gnupg.org/documentation/)

## Related Skills

- **gpg-signing** - Prerequisite for basic single-key setup (Scenario 1)
- **setup** - Prerequisite for Git installation and configuration
- **config** - Related for advanced Git configuration topics (conditional includes)

## Version History

- v1.0.0 (2025-01-09): Initial release migrated from repository documentation
- v1.0.1 (2025-11-12): Enhanced documentation - added test scenarios, related skills section
- v1.0.2 (2025-11-12): Audit improvements - enhanced description with execution verbs
- v1.0.3 (2025-11-25): MCP validation audit - all commands and workflows validated

## Last Updated

**Date:** 2025-11-28
**Model:** claude-opus-4-5-20251101

**Tool Versions Tested:**

- GnuPG: 2.2+
- Git: 2.23+
- GitHub CLI: 2.0+ (for automation scenarios)

All configurations validated against official documentation from gnupg.org, git-scm.com, and docs.github.com.
