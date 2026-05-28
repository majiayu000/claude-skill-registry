---
name: overlay
description: |
  Development: Overlay session management for bazzite-ai development. Enables live
  editing of justfiles via symlinks to /usr on immutable OS (OSTree) or traditional
  Linux systems. Run from repository root with 'just overlay'. Use when developers
  need to test justfile changes without rebuilding the OS image.
---

# Overlay - Development Session Management

## Overview

The `overlay` command manages development sessions that enable live editing of justfiles by creating symlinks from the repository to `/usr/share/bazzite-ai/just/`. This allows testing changes without rebuilding the OS image.

**Key Concept:** On immutable OSTree systems (Bazzite-AI, Silverblue), `/usr` is read-only. Overlay mode temporarily unlocks it. On traditional systems (Fedora, CentOS), symlinks provide the same live-editing capability.

**This is a development command** - run with `just` from the repository root, not `ujust`.

## Quick Reference

| Action | Command | Description |
|--------|---------|-------------|
| Refresh | `just overlay refresh` | Auto-enables if needed, then refreshes |
| Check | `just overlay check` | Show current overlay/symlink status |
| Enable | `just overlay enable` | Manually bootstrap overlay session |
| Info | `just overlay info` | Show detailed system info |
| Help | `just overlay help` | Show usage help |

**Note:** `just overlay refresh` automatically enables the overlay if not active - this is the recommended primary command.

## Parameters

```bash
just overlay ACTION
```

| Parameter | Values | Description |
|-----------|--------|-------------|
| `ACTION` | `refresh`, `check`, `enable`, `info`, `help` | Overlay action |

## Overlay Commands

### Refresh (Recommended)

```bash
just overlay refresh
```

**Auto-enables if needed**, then regenerates imports. Use this as your primary command.

1. Checks if overlay/symlinks are active
2. If NOT active → automatically runs enable first
3. Regenerates `60-custom.just` import file
4. Shows success message

### Check Status

```bash
just overlay check
```

Shows current status:

- **Immutable OS**: Whether overlay mode is active
- **Traditional OS**: Whether symlinks are configured
- Target repository path

### Enable (Manual)

```bash
just overlay enable
```

Manually bootstraps overlay session:

1. Activates overlay mode (OSTree) or creates symlinks (traditional)
2. Detects repository location automatically
3. Sets up symlinks to `/usr/share/bazzite-ai/just/`
4. Generates `60-custom.just` import file
5. Requires sudo (handles internally)

**Note:** You rarely need this directly - `just overlay refresh` auto-enables.

### System Info

```bash
just overlay info
```

Shows detailed information about:

- OS type (immutable vs traditional)
- Current overlay status
- Repository path
- Symlink targets

## OS Type Detection

| OS Type | Detection | Overlay Method |
|---------|-----------|----------------|
| Immutable (OSTree) | `/run/ostree-booted` exists | `rpm-ostree usroverlay` |
| Traditional | No OSTree marker | Symlinks only |

## Common Workflows

### Initial Development Setup

```bash
# 1. Clone repository
git clone <repo-url> && cd bazzite-ai

# 2. Start overlay testing (auto-enables if needed)
just overlay refresh

# 3. Make changes to justfiles
vim just/bazzite-ai/my-feature.just

# 4. Test immediately with ujust
ujust my-feature

# 5. If adding new files, refresh again
just overlay refresh
```

### After Reboot (Immutable OS Only)

```bash
# Overlay resets on reboot - just run refresh
just overlay refresh

# It auto-enables, then refreshes
# Your git commits persist, overlay changes don't
```

### Testing a New Command

```bash
# 1. Create/edit the justfile
vim just/bazzite-ai/new-command.just

# 2. Refresh to pick up new file
just overlay refresh

# 3. Test the command
ujust new-command
```

## Troubleshooting

### Overlay Not Active After Enable

**Symptom:** `just overlay check` shows "Normal immutable mode"

**Cause:** Overlay activation failed

**Fix:**

```bash
# Check if rpm-ostree unlock succeeded
sudo rpm-ostree status | grep -i unlock

# If not, try manual unlock
sudo rpm-ostree usroverlay

# Then refresh
just overlay refresh
```

### Symlinks Not Working

**Symptom:** Changes to justfiles not reflected in `ujust` output

**Cause:** Symlinks not properly created or 60-custom.just not regenerated

**Fix:**

```bash
# Check symlink status
ls -la /usr/share/bazzite-ai/just/

# Refresh (auto-enables if needed)
just overlay refresh
```

### Command Not Found After Adding File

**Symptom:** New recipe not available in `ujust --list`

**Cause:** 60-custom.just needs regeneration

**Fix:**

```bash
just overlay refresh
```

### Permission Denied

**Symptom:** `sudo: a terminal is required`

**Cause:** Running in non-interactive mode without passwordless sudo

**Fix:**

```bash
# Enable passwordless sudo first
ujust config passwordless-sudo enable

# Then retry
just overlay refresh
```

## Cross-References

- **Related Skills:** `test` (runtime verification), `build` (image building)
- **Configuration:** `ujust config passwordless-sudo enable` for sudo access
- **Documentation:** See architecture docs for overlay internals

## When to Use This Skill

Use when the user asks about:

- "enable overlay", "start testing session", "development mode"
- "test my changes", "live reload justfiles"
- "overlay not working", "symlinks not configured"
- "refresh overlay", "pick up new files"
- "just overlay" (any overlay command)
