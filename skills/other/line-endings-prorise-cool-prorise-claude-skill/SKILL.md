---
name: line-endings
description: Comprehensive guide to Git line ending configuration for cross-platform development teams. Use when configuring line endings, setting up .gitattributes, troubleshooting line ending issues, understanding core.autocrlf/core.eol/core.safecrlf, working with Git LFS, normalizing line endings in repositories, or resolving cross-platform line ending conflicts. Covers Windows, macOS, Linux, and WSL. Includes decision trees, workflows, best practices, and real-world scenarios.
allowed-tools: Read, Bash, Glob, Grep
---

# Git Line Endings

Comprehensive guide to Git line ending configuration for cross-platform development teams.

## When to Use This Skill

Use this skill when:

- **Line Endings tasks** - Working on comprehensive guide to git line ending configuration for cross-platform development teams. use when configuring line endings, setting up .gitattributes, troubleshooting line ending issues, understanding core.autocrlf/core.eol/core.safecrlf, working with git lfs, normalizing line endings in repositories, or resolving cross-platform line ending conflicts. covers windows, macos, linux, and wsl. includes decision trees, workflows, best practices, and real-world scenarios
- **Planning or design** - Need guidance on Line Endings approaches
- **Best practices** - Want to follow established patterns and standards

**Last Verified:** 2025-11-25
**Last Audited:** 2025-11-25 (Comprehensive Type A audit - 79/80 score, content validated via MCP servers against official Git documentation)

## Overview

### What Are Line Endings?

Line endings are invisible characters that mark the end of a line in text files:

- **LF (Line Feed)**: `\n` - Used by Unix, Linux, macOS (1 byte)
- **CRLF (Carriage Return + Line Feed)**: `\r\n` - Used by Windows (2 bytes)
- **CR (Carriage Return)**: `\r` - Legacy Mac OS 9 and earlier (rarely seen today)

### Why Line Endings Matter

**The Problem:**

```bash
# Windows developer creates file with CRLF
echo "#!/bin/bash" > script.sh

# Linux developer pulls and tries to run it
./script.sh
# Error: /bin/bash^M: bad interpreter: No such file or directory
```

**Common Issues:**

1. Shell scripts fail to execute (Unix requires LF, CRLF breaks shebang lines)
2. Massive diffs (every line shows as changed when only line endings differ)
3. File corruption (binary files treated as text get line endings mangled)
4. Build failures (Makefiles, configuration files may require specific endings)
5. Git conflicts (line ending differences cause merge conflicts)

### How Git Handles Line Endings

Git provides three mechanisms:

1. **Config settings** (`core.autocrlf`, `core.eol`, `core.safecrlf`) - Automatic conversions
2. **`.gitattributes` file** - Explicit per-file or per-pattern rules (highest priority)
3. **Manual normalization** (`git add --renormalize`) - One-time fixes

**Git's Design Philosophy:**

- Repository (index): Normalized line endings (typically LF)
- Working directory: Platform-appropriate line endings (CRLF on Windows, LF on Unix)
- Conversion happens automatically on checkout and commit

---

## Quick Start

### Two Configuration Approaches

#### Option 1: Traditional (Recommended)

**Platform-specific configs with automatic normalization:**

```bash
# Windows
git config --global core.autocrlf true
git config --global core.safecrlf warn

# Mac/Linux
git config --global core.autocrlf input
git config --global core.safecrlf warn
```

**Pros:**

- ✅ Works WITHOUT .gitattributes (safe for external repos)
- ✅ Git for Windows default (zero config on Windows)
- ✅ Automatic normalization prevents mixed line endings
- ✅ Industry standard

**When to use:** You work in repos you don't control (open source, client, vendor repos)

#### Option 2: Modern Explicit

**Same config everywhere, relies on .gitattributes:**

```bash
# All platforms
git config --global core.autocrlf false
git config --global core.eol native
git config --global core.safecrlf warn
```

**Pros:**

- ✅ Same config everywhere (team consistency)
- ✅ Explicit and predictable
- ✅ Modern best practice

**Cons:**

- ⚠️ **REQUIRES .gitattributes** - Broken without it
- ⚠️ Not safe for external repos

**When to use:** You control ALL repositories and can ensure comprehensive .gitattributes

### Recommendation

**Use Option 1** if you work in mixed environments (internal + external repos). See [Configuration Approaches](references/configuration-approaches.md) for detailed comparison.

---

## Decision Tree

For comprehensive decision tree covering all scenarios (repository control, platform selection, file types, troubleshooting), see [Decision Tree](references/decision-tree.md).

**Quick decision:**

1. **Do you control ALL repositories?** NO → Use Option 1 (Traditional)
2. **What platform?** Windows: `autocrlf=true`, macOS/Linux: `autocrlf=input`
3. **Has .gitattributes?** YES → Both options work, NO → Option 1 only

---

## Understanding .gitattributes

`.gitattributes` is a repository-level file that explicitly declares how Git should handle specific files.

**Minimal .gitattributes:**

```gitattributes
# Auto-detect text files and normalize to LF in repository
* text=auto
```

**Comprehensive .gitattributes:**

```gitattributes
# Default: auto-detect and normalize
* text=auto

# Documentation - LF everywhere
*.md text eol=lf
*.txt text eol=lf

# Shell scripts - MUST be LF (Unix requirement)
*.sh text eol=lf
*.bash text eol=lf

# PowerShell scripts - CRLF (Windows standard)
*.ps1 text eol=crlf
*.cmd text eol=crlf
*.bat text eol=crlf

# Configuration files - LF (cross-platform)
*.json text eol=lf
*.yml text eol=lf
.gitignore text eol=lf
.gitattributes text eol=lf

# Binary files - never convert
*.png binary
*.jpg binary
*.pdf binary
*.zip binary
*.exe binary
```

**Why Use .gitattributes:**

- Explicit rules committed to repository
- All developers get same behavior
- Overrides local configs
- Self-documenting

See [.gitattributes Guide](references/gitattributes-guide.md) for comprehensive patterns and attribute reference.

---

## Platform-Specific Configuration

### Windows

```bash
# Check current config (should be default from Git for Windows)
git config --global --get core.autocrlf
# Expected: true

# If not set, configure explicitly
git config --global core.autocrlf true
git config --global core.safecrlf warn
```

**Behavior:**

- Files in working directory: CRLF (Windows standard)
- Files in repository: LF (cross-platform standard)
- Automatic conversion on checkout and commit

See [Platform-Specific Configuration](references/platform-specific.md) for detailed setup guides for Windows, macOS, Linux, and WSL.

---

## Common Issues & Troubleshooting

### Issue: Shell Scripts Won't Execute (`^M: bad interpreter`)

**Error:**

```bash
$ ./script.sh
bash: ./script.sh: /bin/bash^M: bad interpreter: No such file or directory
```

**Root Cause:** Shell script has CRLF line endings. Unix shells require LF.

**Immediate Fix:**

```bash
# Convert CRLF to LF
dos2unix script.sh

# Or with sed
sed -i 's/\r$//' script.sh

# Make executable
chmod +x script.sh
```

**Permanent Fix (Add to .gitattributes):**

```gitattributes
# Shell scripts MUST have LF
*.sh text eol=lf
*.bash text eol=lf
```

```bash
# Normalize the script
git add --renormalize script.sh
git commit -m "Fix line endings in shell scripts"
```

### Issue: Git Shows Every Line as Changed

**Root Cause:** Line endings changed (CRLF ↔ LF).

**Fix:**

```bash
# Check current line endings
git ls-files --eol file.txt

# Normalize to repository standard
git add --renormalize file.txt
git commit -m "Normalize line endings for file.txt"
```

See [Troubleshooting](references/troubleshooting.md) for comprehensive issue resolution.

---

## Commands Reference

**Quick reference for essential commands:**

```bash
# View configuration
git config --list --show-origin | grep -E "autocrlf|eol|safecrlf"

# Check file attributes
git check-attr -a README.md

# Check line ending status
git ls-files --eol README.md

# Normalize files
git add --renormalize .

# Test line ending behavior
git ls-files --eol | grep "w/crlf" | grep "eol=lf"  # Find mismatches
```

See [Commands Reference](references/commands-reference.md) for complete command listing.

---

## Best Practices Summary

1. **Always use .gitattributes in repos you control**
   - Explicit line ending rules
   - Team-wide consistency
   - Self-documenting

2. **Document platform-specific configs in onboarding**
   - Windows: Verify `autocrlf=true`
   - macOS/Linux: Must set `autocrlf=input`

3. **Set core.safecrlf=warn for safety**
   - Warns about line ending conversions
   - Catches issues early

4. **Test with git ls-files --eol**
   - Regular checks for mismatches
   - Find mixed line endings

5. **Normalize when adding .gitattributes**
   - Run `git add --renormalize .`
   - Review and commit changes

See [Best Practices](references/best-practices.md) for detailed guidance.

---

## Git Large File System (LFS)

Git LFS stores large binary files separately from the main repository to prevent bloat. This is separate from line ending configuration but works alongside it.

See [Git LFS Guide](references/git-lfs.md) for comprehensive installation, configuration, when to use, GitHub limits, and migration strategies.

---

## References

**Configuration and Setup:**

- **[Decision Tree](references/decision-tree.md)** - Comprehensive decision flowchart for all scenarios
- **[Configuration Mechanics](references/configuration-mechanics.md)** - Core.autocrlf, core.eol, core.safecrlf explained
- **[Configuration Approaches](references/configuration-approaches.md)** - Option 1 vs Option 2 comparison
- **[Platform-Specific Configuration](references/platform-specific.md)** - Windows, macOS, Linux, WSL setup guides

**Implementation:**

- **[.gitattributes Guide](references/gitattributes-guide.md)** - Comprehensive patterns and attribute reference
- **[Git LFS Guide](references/git-lfs.md)** - Installation, configuration, migration, GitHub limits
- **[Workflows & Scenarios](references/workflows-scenarios.md)** - New repos, existing repos, external repos, team onboarding
- **[Real-World Examples](references/real-world-examples.md)** - Practical examples and case studies

**Troubleshooting and Support:**

- **[Troubleshooting](references/troubleshooting.md)** - Common issues and detailed solutions
- **[Commands Reference](references/commands-reference.md)** - Complete command listing with examples
- **[Best Practices](references/best-practices.md)** - Detailed best practices and prevention strategies

**Testing:**

- **[Evaluations](references/evaluations.md)** - Test scenarios, multi-model testing, formal evaluations

---

## Testing and Evaluations

For comprehensive test scenarios, multi-model testing notes, and formal evaluations, see [Evaluations](references/evaluations.md).

**Evaluation Summary**: 4/4 evaluations passed (100%) - Tested with Claude Sonnet 4 and Claude Opus 4.5

---

## Version History

- v2.2.0 (2025-11-28): Token optimization - extracted decision tree and evaluations to references/ for progressive disclosure, reduced SKILL.md from 534 to ~400 lines
- v2.1.2 (2025-11-25): Content validation via MCP servers - All technical content verified accurate against official Git documentation
- v2.1.1 (2025-11-25): Audit improvements - Fixed model naming conventions, added Opus 4.5 verification
- v2.1.0 (2025-11-17): Quality improvements - Added formal evaluations, multi-model testing notes
- v2.0.1 (2025-11-17): Content audit - Updated GitHub LFS limits, validated against Git 2.51.2
- v2.0.0 (2024-11-09): Hub/spoke refactoring - extracted detailed content to references/
- v1.0.0 (2024-11-09): Initial release with comprehensive line ending guidance

---

## Official Documentation

- [Git Attributes](https://git-scm.com/docs/gitattributes)
- [Git Config - core.autocrlf](https://git-scm.com/docs/git-config#Documentation/git-config.txt-coreautocrlffalse)
- [Git Config - core.eol](https://git-scm.com/docs/git-config#Documentation/git-config.txt-coreeol)
- [Configuring Git to handle line endings (GitHub)](https://docs.github.com/en/get-started/git-basics/configuring-git-to-handle-line-endings)
- [Git LFS Official Site](https://git-lfs.com/)
- [Git LFS Billing (GitHub)](https://docs.github.com/en/billing/concepts/product-billing/git-lfs)

## Last Updated

**Date:** 2025-11-28
**Model:** claude-opus-4-5-20251101
