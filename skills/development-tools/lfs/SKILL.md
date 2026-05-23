---
name: lfs
description: |
  Development: Git LFS file management for large binary files in the repository.
  Handles checkout, status, fetch, and verification of LFS-tracked files.
  Run from repository root with 'just lfs'. Use when developers need to manage
  large files like recordings, images, or binary assets.
---

# LFS - Git LFS Management

## Overview

The `lfs` command manages Git LFS (Large File Storage) files in the repository. It provides utilities for checking out, fetching, and verifying LFS-tracked files.

**Key Concept:** Git LFS stores large binary files (recordings, images, documentation assets) as pointers in the repository, with actual content stored separately. These commands ensure you have the actual file content, not just pointers.

**This is a development command** - run with `just` from the repository root, not `ujust`.

## Quick Reference

| Action | Command | Description |
|--------|---------|-------------|
| Checkout | `just lfs checkout` | Fetch and checkout all LFS files |
| Status | `just lfs status` | Show LFS file status with sizes |
| Fetch | `just lfs fetch -p 'pattern'` | Fetch LFS files matching pattern |
| Verify | `just lfs verify` | Verify all LFS files are checked out |
| Help | `just lfs help` | Show usage help |

## Parameters

```bash
just lfs <action> [parameters]
```

| Parameter | Long Flag | Short | Default | Description |
|-----------|-----------|-------|---------|-------------|
| `action` | (positional) | - | required | Action: checkout, status, fetch, verify, help |
| `pattern` | `--pattern` | `-p` | `""` | Glob pattern for fetch action |

## Actions

### Checkout All LFS Files

```bash
just lfs checkout
```

Fetches and checks out all LFS-tracked files in the repository. This replaces pointer files with actual content.

**Use when:** After cloning the repository or when LFS files show as pointers.

### Show Status

```bash
just lfs status
```

Displays status of all LFS-tracked files including:

- File paths
- File sizes
- Whether content is present or still a pointer

**Use when:** To see which LFS files are in the repository and their sizes.

### Fetch Specific Files

```bash
# Fetch documentation assets
just lfs fetch -p 'docs/**'

# Fetch recordings
just lfs fetch --pattern='docs/recordings/*.cast'

# Fetch images
just lfs fetch -p '*.png'
```

Selectively fetches LFS files matching a glob pattern. Useful for large repositories where you only need specific assets.

**Use when:** You only need certain LFS files and want to save bandwidth/time.

### Verify Files

```bash
just lfs verify
```

Verifies that all LFS-tracked files have been properly checked out (not still pointer files).

**Use when:** Before committing or to diagnose LFS issues.

## Common Workflows

### After Cloning Repository

```bash
# Clone repository
git clone <repo-url>
cd bazzite-ai

# Check LFS status
just lfs status

# Checkout all LFS files
just lfs checkout

# Verify everything is present
just lfs verify
```

### Working with Documentation

```bash
# Fetch only documentation assets
just lfs fetch -p 'docs/**'

# Build documentation
just docs-build
```

### Before Committing

```bash
# Verify LFS files are properly tracked
just lfs verify

# Check status
just lfs status

# Commit changes
git add -A && git commit -m "message"
```

## LFS-Tracked File Types

The repository typically tracks these file types with LFS:

| Pattern | Type | Purpose |
|---------|------|---------|
| `*.cast` | Asciinema recordings | Terminal session recordings |
| `*.png`, `*.jpg` | Images | Documentation images |
| `*.gif` | Animated GIFs | Demo animations |
| `*.qcow2`, `*.raw` | VM images | Virtual machine images |
| `*.iso` | ISO images | Bootable installers |

## Troubleshooting

### LFS Files Show as Pointers

**Symptom:** Opening a file shows text like `version https://git-lfs.github.com/spec/v1...`

**Cause:** LFS content not fetched

**Fix:**

```bash
just lfs checkout
```

### Fetch Fails with Authentication Error

**Symptom:** `error: authentication required`

**Cause:** Not authenticated to LFS server

**Fix:**

```bash
# For GitHub
git credential fill <<EOF
protocol=https
host=github.com
EOF

# Then retry
just lfs checkout
```

### Verify Shows Missing Files

**Symptom:** `just lfs verify` reports pointer files

**Cause:** LFS content not fully downloaded

**Fix:**

```bash
# Force re-fetch all
git lfs fetch --all
just lfs checkout
just lfs verify
```

### Pattern Doesn't Match

**Symptom:** `just lfs fetch -p 'docs/*'` fetches nothing

**Cause:** Pattern needs to match full path or use `**` for recursion

**Fix:**

```bash
# Use ** for recursive matching
just lfs fetch -p 'docs/**'

# Or be more specific
just lfs fetch -p 'docs/recordings/*.cast'
```

## Cross-References

- **Related Skills:** `build` (may need LFS files), `clean` (can clean LFS cache)
- **Git LFS Docs:** <https://git-lfs.github.com/>
- **Configuration:** `.gitattributes` defines LFS-tracked patterns

## When to Use This Skill

Use when the user asks about:

- "lfs", "git lfs", "large file storage"
- "lfs checkout", "fetch lfs files"
- "lfs status", "lfs verify"
- "pointer files", "lfs not working"
- "just lfs" (any lfs command)
