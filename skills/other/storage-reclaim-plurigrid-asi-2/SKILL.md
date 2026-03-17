---
name: storage-reclaim
description: Rapidly find and reclaim disk storage by identifying build artifacts, git garbage, temp files, and other space hogs. Use when disk is full or running low on space.
---

# Storage Reclaim

Rapid parallel investigation and cleanup of disk storage.

## Quick Start

```bash
# Top-level overview
du -sh /path/*/ 2>/dev/null | sort -hr | head -20

# Drill into specific directory
du -sh /path/subdir/*/ 2>/dev/null | sort -hr | head -15
```

## Common Space Hogs

### 1. Rust Build Artifacts (`target/`)
- Location: Any Rust project root
- Size: 1-10+ GB per project
- Safe to delete: Yes (rebuilds on next `cargo build`)

```bash
# Find all Rust target directories
find ~ -type d -name "target" -exec du -sh {} \; 2>/dev/null | sort -hr | head -20

# Clean specific project
rm -rf /path/to/project/target

# Or use cargo
cd /path/to/project && cargo clean
```

### 2. Git Garbage (tmp_pack files)
- Location: `.git/objects/pack/tmp_pack_*`
- Cause: Interrupted git operations
- Size: Can be gigabytes

```bash
# Check for git garbage
git count-objects -vH
# Look for "size-garbage" line

# Remove stale pack files
rm -f .git/objects/pack/tmp_pack_*

# Verify cleanup
git count-objects -vH
```

### 3. Node Modules
- Location: `node_modules/` in JS projects
- Size: 100MB - 2GB per project

```bash
# Find all node_modules
find ~ -type d -name "node_modules" -prune -exec du -sh {} \; 2>/dev/null | sort -hr

# Remove (can reinstall with npm install)
rm -rf /path/to/project/node_modules
```

### 4. Python Virtual Environments
- Location: `.venv/`, `venv/`, `env/`
- Size: 100MB - 1GB per environment

```bash
find ~ -type d \( -name ".venv" -o -name "venv" -o -name "env" \) -exec du -sh {} \; 2>/dev/null | sort -hr
```

### 5. Hidden Temp Directories
- Location: `.tmp/`, `.cache/`, `__pycache__/`
- Often overlooked by `du` on directories

```bash
# Check hidden dirs specifically
du -sh /path/.* 2>/dev/null | sort -hr | head -10
```

### 6. Julia Artifacts
- Location: `~/.julia/artifacts/`, `~/.julia/compiled/`
- Size: Can grow to many GB

```bash
du -sh ~/.julia/*/ 2>/dev/null | sort -hr
```

### 7. Docker
```bash
docker system df
docker system prune -a  # Remove all unused images/containers
```

### 8. Homebrew
```bash
brew cleanup --dry-run  # Preview
brew cleanup            # Actually clean
```

## Investigation Pattern

1. **Start broad**: `du -sh /path/*/ | sort -hr | head -20`
2. **Drill into largest**: Repeat for subdirectories
3. **Check hidden**: `du -sh /path/.* | sort -hr`
4. **Git check**: `git count-objects -vH` in any repo
5. **Clean safely**: Remove build artifacts first (always regeneratable)

## Safety Rules

- **Always safe to delete**: `target/`, `node_modules/`, `.tmp/`, `__pycache__/`, build/
- **Check first**: `.git/` (might have garbage, might be real history)
- **Never delete blindly**: Actual source code, `.git/objects/pack/*.pack` (real packs)
- **Regeneratable**: Anything that `cargo build`, `npm install`, `pip install` creates

## Parallel Investigation

Run multiple `du` commands simultaneously for faster discovery:
```bash
# In parallel (use separate terminal or background)
du -sh ~/project1/*/ | sort -hr &
du -sh ~/project2/*/ | sort -hr &
wait
```
