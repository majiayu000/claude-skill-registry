---
name: setting-up-public-domain-repos-majo
description: |
  Set up new repositories with dual licensing (Unlicense OR 0BSD) or convert existing repositories
  to public domain. Use when initializing a new project, adding licensing to an unlicensed repo,
  or switching from restrictive licenses to public domain. Fetches authoritative license files,
  configures repository structure, and ensures consistent public domain setup.
license: Unlicense OR 0BSD
metadata:
  author: Mark Joshwel <mark@joshwel.co>
  version: "2026.2.2"
  default_author: Mark Joshwel
  default_email: mark@joshwel.co
---

# Public Domain Repository Setup (Mark)

**Goal**: Set up free-as-in-freedom repositories with dual licensing under The Unlicense OR BSD Zero Clause License (0BSD), ensuring maximum freedom for users while providing legal clarity.

## When to Use This Skill

- **Initializing a new repository** - Setting up licensing from the start
- **Converting an existing repository to public domain** - Changing from restrictive licenses
- **Setting up licensing for a new project** - Ensuring consistent public domain structure
- **Ensuring consistent public domain structure** - Across multiple projects
- **Adding public domain dedication** - To personal or open-source projects

## When NOT to Use This Skill

- **Repository has existing licenses that cannot be changed** (corporate policy)
- **Project requires copyleft licenses** (GPL, AGPL, etc.)
- **Project requires attribution licenses** (MIT, Apache, BSD-2/3-Clause)
- **Contributor cannot waive copyright** (employer restrictions, some jurisdictions)
- **Need to preserve existing license obligations** (fork of licensed project)

## Process

1. **Check repository state** - Determine if new or existing repository
2. **Check for existing license files** (CRITICAL) - Look for LICENSE, COPYING, or similar files
3. **If existing licenses found, STOP and ask user** - Get explicit guidance before proceeding
4. **Fetch authoritative files** - Download from gist repository:
   - CODE_OF_CONDUCT.md
   - CONTRIBUTING
   - LICENCING (British spelling)
   - LICENSE-0BSD
   - UNLICENSE
5. **Update copyright year** - Set to current year in LICENSE-0BSD (CRITICAL)
6. **Place files in repository root** - Copy all fetched files to project root
7. **Initialize git if needed** - Run `git init` if no `.git` directory exists
8. **Verify setup** - Check all 5 files are present with correct content
9. **Commit license files** - Add and commit with message "Add public domain dual-licensing"
10. **Add SPDX identifiers** - Add to source files per `dev-standards-majo` skill
11. **Update AGENTS.md** - Document the licensing choice

## Constraints

- **ALWAYS check for existing LICENSE/COPYING files first** - Do not overwrite without user guidance
- **ALWAYS update copyright year** to current year in LICENSE-0BSD - Never use outdated year
- **ALWAYS use dual-license format** `Unlicense OR 0BSD` in SPDX identifiers
- **NEVER proceed with setup if existing licenses clash** - Stop and ask user for direction
- **Use British spelling "LICENCING"** (with 'c') - But LICENSE-0BSD and UNLICENSE use American spelling (with 's') for standards compatibility
- **Fetch from authoritative gist sources** - Don't create files from scratch
- **Default to Mark Joshwel <mark@joshwel.co>** - Unless user specifies otherwise

Automated setup for public domain repositories with dual licensing (Unlicense OR 0BSD).

## Overview

This skill sets up repositories to be free-as-in-freedom, dual-licensed under The Unlicense or the BSD Zero Clause License (SPDX: `Unlicense OR 0BSD`).

**The Spirit**: Treat the work as public domain via The Unlicense, but provide the BSD Zero Clause License where public domain dedication is not possible due to policies bound to a contributor or their employer.

## Prerequisites

- Git repository (initialized or not)
- Internet access to fetch authoritative files
- Default author: Mark Joshwel <mark@joshwel.co>

## Setup Workflow

### Step 1: Check Repository State

Determine if this is a new repository or existing:

```bash
# Check if git repo exists
if [ -d .git ]; then
    echo "Existing repository"
else
    echo "New repository - will initialize"
fi

# Check for existing license files
ls -la LICENSE* 2>/dev/null || echo "No LICENSE files found"
ls -la UNLICENSE* 2>/dev/null || echo "No UNLICENSE file found"
```

### Step 2: Handle Existing Files (CRITICAL)

**If LICENSE, COPYING, or similar files exist:**

STOP and ask the user:

```
I found existing license files in this repository:
- [List existing files]

How would you like to proceed?
1. Replace with public domain dual-license setup
2. Keep existing licenses and add public domain as additional option
3. Abort setup
4. Something else (describe)
```

**Do not proceed without user guidance when clashes exist.**

### Step 3: Fetch Authoritative Files

Fetch all files from authoritative sources:

```bash
# Create temporary directory for downloads
mkdir -p /tmp/pd-setup

# Fetch all files
curl -sL https://gist.githubusercontent.com/markjoshwel/6a0b4ea7673c279bc5a2fb5fe4ed423e/raw/9cd9bd30475b761823cf6e8920fba268766f3408/CODE_OF_CONDUCT.md -o /tmp/pd-setup/CODE_OF_CONDUCT.md

curl -sL https://gist.githubusercontent.com/markjoshwel/6a0b4ea7673c279bc5a2fb5fe4ed423e/raw/9cd9bd30475b761823cf6e8920fba268766f3408/CONTRIBUTING -o /tmp/pd-setup/CONTRIBUTING

curl -sL https://gist.githubusercontent.com/markjoshwel/6a0b4ea7673c279bc5a2fb5fe4ed423e/raw/9cd9bd30475b761823cf6e8920fba268766f3408/LICENCING -o /tmp/pd-setup/LICENCING

curl -sL https://gist.githubusercontent.com/markjoshwel/6a0b4ea7673c279bc5a2fb5fe4ed423e/raw/9cd9bd30475b761823cf6e8920fba268766f3408/LICENSE-0BSD -o /tmp/pd-setup/LICENSE-0BSD

curl -sL https://gist.githubusercontent.com/markjoshwel/6a0b4ea7673c279bc5a2fb5fe4ed423e/raw/9cd9bd30475b761823cf6e8920fba268766f3408/UNLICENSE -o /tmp/pd-setup/UNLICENSE
```

### Step 4: Update Copyright Year

**CRITICAL**: Update the copyright year in LICENSE-0BSD to the current year:

```bash
# Get current year
CURRENT_YEAR=$(date +%Y)

# Update LICENSE-0BSD with current year
sed -i "s/Copyright (C) [0-9]\{4\}/Copyright (C) $CURRENT_YEAR/" /tmp/pd-setup/LICENSE-0BSD

# Verify the change
grep "Copyright" /tmp/pd-setup/LICENSE-0BSD
```

**Note**: Due to British English conventions, the file is named "LICENCING" (with 'c'), but LICENSE-0BSD and UNLICENSE use American spelling "LICENSE" (with 's') for standards compatibility.

### Step 5: Place Files

Copy files to repository root:

```bash
# Copy all files to repository root
cp /tmp/pd-setup/CODE_OF_CONDUCT.md ./CODE_OF_CONDUCT.md
cp /tmp/pd-setup/CONTRIBUTING ./CONTRIBUTING
cp /tmp/pd-setup/LICENCING ./LICENCING
cp /tmp/pd-setup/LICENSE-0BSD ./LICENSE-0BSD
cp /tmp/pd-setup/UNLICENSE ./UNLICENSE

# Clean up
rm -rf /tmp/pd-setup
```

### Step 6: Initialize Git (if needed)

**IMPORTANT**: Initialize git repository if it doesn't exist:

```bash
# Initialize git if not already initialized
if [ ! -d .git ]; then
    git init
    echo "Git repository initialized"
fi
```

This skill is designed to be called at the opportune time to set up a repository, so initializing git is appropriate.

### Step 7: Verify Setup

Check that all files are in place:

```bash
# List all public domain files
echo "=== Public Domain Repository Files ==="
ls -la CODE_OF_CONDUCT.md CONTRIBUTING LICENCING LICENSE-0BSD UNLICENSE 2>/dev/null

echo ""
echo "=== LICENSE-0BSD Copyright Year ==="
head -1 LICENSE-0BSD

echo ""
echo "=== LICENCING Content Preview ==="
head -10 LICENCING
```

## File Descriptions

| File | Purpose | Source |
|------|---------|--------|
| `CODE_OF_CONDUCT.md` | Community conduct guidelines | Fetched from gist |
| `CONTRIBUTING` | Contribution guidelines with waiver | Fetched from gist |
| `LICENCING` | Dual-licensing explanation (British spelling) | Fetched from gist |
| `LICENSE-0BSD` | BSD Zero Clause License text | Fetched from gist |
| `UNLICENSE` | Public domain dedication | Fetched from gist |

## SPDX License Identifiers

When creating new source files, add the appropriate SPDX identifier at the top:

**For most files** (dual-licensed):
```python
# SPDX-License-Identifier: Unlicense OR 0BSD
```

**For files by contributors who cannot waive copyright**:
```python
# SPDX-License-Identifier: 0BSD
```

**Note**: SPDX identifiers in source files are covered by the `dev-standards-majo` skill. This skill focuses on repository-level setup.

## Complete Setup Script

Here's the complete workflow in one go:

```bash
#!/bin/bash
# Public Domain Repository Setup

set -e

echo "=== Public Domain Repository Setup ==="
echo ""

# Check for existing license files
EXISTING=$(ls LICENSE* COPYING* 2>/dev/null || true)
if [ -n "$EXISTING" ]; then
    echo "WARNING: Existing license files found:"
    echo "$EXISTING"
    echo ""
    echo "Please resolve conflicts before proceeding."
    exit 1
fi

# Create temp directory
TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

# Fetch files
echo "Fetching authoritative files..."
curl -sL https://gist.githubusercontent.com/markjoshwel/6a0b4ea7673c279bc5a2fb5fe4ed423e/raw/9cd9bd30475b761823cf6e8920fba268766f3408/CODE_OF_CONDUCT.md -o "$TMPDIR/CODE_OF_CONDUCT.md"
curl -sL https://gist.githubusercontent.com/markjoshwel/6a0b4ea7673c279bc5a2fb5fe4ed423e/raw/9cd9bd30475b761823cf6e8920fba268766f3408/CONTRIBUTING -o "$TMPDIR/CONTRIBUTING"
curl -sL https://gist.githubusercontent.com/markjoshwel/6a0b4ea7673c279bc5a2fb5fe4ed423e/raw/9cd9bd30475b761823cf6e8920fba268766f3408/LICENCING -o "$TMPDIR/LICENCING"
curl -sL https://gist.githubusercontent.com/markjoshwel/6a0b4ea7673c279bc5a2fb5fe4ed423e/raw/9cd9bd30475b761823cf6e8920fba268766f3408/LICENSE-0BSD -o "$TMPDIR/LICENSE-0BSD"
curl -sL https://gist.githubusercontent.com/markjoshwel/6a0b4ea7673c279bc5a2fb5fe4ed423e/raw/9cd9bd30475b761823cf6e8920fba268766f3408/UNLICENSE -o "$TMPDIR/UNLICENSE"

# Update copyright year
CURRENT_YEAR=$(date +%Y)
sed -i "s/Copyright (C) [0-9]\{4\}/Copyright (C) $CURRENT_YEAR/" "$TMPDIR/LICENSE-0BSD"

# Copy files
echo "Installing files..."
cp "$TMPDIR"/* .

# Initialize git if needed
if [ ! -d .git ]; then
    git init
    echo "Git repository initialized"
fi

echo ""
echo "=== Setup Complete ==="
echo "Files installed:"
ls -la CODE_OF_CONDUCT.md CONTRIBUTING LICENCING LICENSE-0BSD UNLICENSE
echo ""
echo "Copyright year: $CURRENT_YEAR"
```

## Post-Setup Steps

After running this skill:

1. **Review files** - Ensure they meet your project's needs
2. **Add to git**:
   ```bash
   git add CODE_OF_CONDUCT.md CONTRIBUTING LICENCING LICENSE-0BSD UNLICENSE
   git commit -m "Add public domain dual-licensing"
   ```
3. **Update AGENTS.md** - Note the licensing choice
4. **Add SPDX identifiers** to source files (see `dev-standards-majo` skill)

## Testing Skills

- **Existing license check**: Verify no LICENSE/COPYING files exist before proceeding
- **File presence test**: All 5 files present (CODE_OF_CONDUCT.md, CONTRIBUTING, LICENCING, LICENSE-0BSD, UNLICENSE)
- **Copyright year verification**: Check current year is in LICENSE-0BSD line 1
- **Fetch validation**: All files downloaded correctly from gist URLs
- **Git initialization**: `.git` directory exists after setup
- **SPDX format check**: Dual-license format "Unlicense OR 0BSD" in identifiers
- **British spelling**: LICENCING spelled with 'c' (British), LICENSE-0BSD with 's' (American)

## Common Issues

### Issue: curl fails to fetch

**Solution**: Check internet connection and gist URLs. The URLs should be:
- `https://gist.githubusercontent.com/markjoshwel/6a0b4ea7673c279bc5a2fb5fe4ed423e/raw/...`

### Issue: sed not working on macOS

**Solution**: Use `sed -i ''` instead of `sed -i` on macOS:
```bash
sed -i '' "s/Copyright (C) [0-9]\{4\}/Copyright (C) $CURRENT_YEAR/" LICENSE-0BSD
```

### Issue: Existing LICENSE file

**Solution**: This skill will stop and ask for guidance. Do not overwrite without user confirmation.

## Integration

This skill extends `dev-standards-majo`. Always ensure `dev-standards-majo` is loaded for:
- AGENTS.md maintenance
- Universal code principles
- Documentation policies

Works alongside:
- `python-majo` / `js-bun-majo` / `shell-majo` — For language-specific project setup
- `task-planning-majo` — For complex repository setups
- `git-majo` — For committing license files
- `writing-docs-majo` — For writing licence documentation

## References

- [The Unlicense](https://unlicense.org/)
- [BSD Zero Clause License](https://opensource.org/licenses/0BSD)
- [SPDX License List](https://spdx.org/licenses/)

## Notes

- **British vs American spelling**: LICENCING uses British spelling (with 'c'), while LICENSE-0BSD and UNLICENSE use American spelling (with 's') for compatibility with standards
- **Copyright year**: Always updated to current year automatically
- **Author**: Defaults to Mark Joshwel <mark@joshwel.co>
