---
name: skill-code-simplifier
description: Automatically refine and simplify skill content while preserving functionality. Based on Anthropic's code-simplifier pattern. Enhances clarity, enforces standards, reduces verbosity, eliminates redundancy, and maintains balance between brevity and understanding. Operates autonomously on recent changes. Use after editing skills or before packaging.
version: 1.0.0
author: Guillaume
created: 2026-01-10
updated: 2026-01-10
tags: [meta-skill, refactoring, clarity, automation, quality]
dependencies: [skill-quality-auditor]
compatibility: [claude.ai, claude-code]
license: MIT
---

# Skill Code Simplifier

Automatically refine and simplify skills while preserving all functionality (inspired by Anthropic's code-simplifier).

## Prerequisites

- Python 3.8+
- Git (for tracking changes)
- Skills library

## Core Principles

**1. Preserve Functionality**: Never change what the skill teaches - only how it teaches it

**2. Apply Standards**: Follow skill-template.md best practices:
- Use numbered steps with time estimates
- Include validation with expected outputs
- Provide executable commands (no pseudo-code)
- Maintain consistent frontmatter
- Use kebab-case naming

**3. Enhance Clarity**:
- Reduce unnecessary verbosity
- Eliminate redundant examples
- Improve command readability
- Consolidate related workflows
- **IMPORTANT**: Avoid nested instructions - prefer flat numbered steps

**4. Maintain Balance**: Avoid over-simplification that removes helpful context

**5. Focus Scope**: Only refine recently modified skills

## Quick Start

### 1. Simplify a Skill (2 min)

```bash
python3 scripts/simplify-skill.py ~/Skills_librairie/skills/postgres-backup

# Output:
# Analyzing postgres-backup...
# 
# Simplifications made:
# - Reduced step 2 from 8 lines to 5 lines (-38%)
# - Removed redundant explanation in Prerequisites
# - Consolidated 3 similar examples into 1
# - Standardized time estimates (5 minutes → 5 min)
# 
# Before: 1,245 words, 8,450 tokens
# After: 892 words, 6,150 tokens (-27%)
# 
# Functionality preserved: ✓
```

### 2. Review Changes (1 min)

```bash
# See what changed
git diff skills/postgres-backup/SKILL.md
```

### 3. Accept or Revert

```bash
# Accept changes
git add skills/postgres-backup/SKILL.md
git commit -m "Simplify postgres-backup skill"

# Or revert
git checkout skills/postgres-backup/SKILL.md
```

## Simplification Patterns

### Pattern 1: Remove Redundant Explanations

**Before:**
```markdown
### Install Docker

You need to install Docker on your system. Docker is a containerization platform. 
To install it, you should first update your package manager, then add the Docker 
repository, and finally install Docker using apt. This process typically takes about 
5 minutes depending on your internet speed.

```bash
sudo apt update
sudo apt install docker.io
```

After installation, you should verify that Docker is installed correctly by checking the version.
```

**After:**
```markdown
### 1. Install Docker (5 min)

```bash
sudo apt update && sudo apt install -y docker.io

# Verify
docker --version
# Expected: Docker version 24.0.x
```
```

**Reductions:**
- 82 words → 22 words (73% shorter)
- Self-documenting commands
- Expected output shown
- Time estimate in heading

### Pattern 2: Consolidate Similar Examples

**Before:**
```markdown
Example 1: Backup to local disk
```bash
pg_dump mydb > backup.sql
```

Example 2: Backup to local disk with date
```bash
pg_dump mydb > backup-$(date +%Y%m%d).sql
```

Example 3: Backup to local disk with compression
```bash
pg_dump mydb | gzip > backup-$(date +%Y%m%d).sql.gz
```
```

**After:**
```markdown
```bash
# Basic backup
pg_dump mydb > backup-$(date +%Y%m%d).sql

# With compression (recommended)
pg_dump mydb | gzip > backup-$(date +%Y%m%d).sql.gz
```
```

### Pattern 3: Simplify Command Explanations

**Before:**
```markdown
The next step is to set the DATABASE_URL environment variable which contains the connection 
string to your PostgreSQL database. This should include the username, password, host, port, 
and database name in the format shown below.
```

**After:**
```markdown
Set database connection:
```

**Context provided by command itself:**
```bash
export DATABASE_URL="postgres://user:pass@localhost:5432/dbname"
```

### Pattern 4: Flatten Nested Instructions

**Before:**
```markdown
1. Install PostgreSQL
   - First, update packages
     - Run apt update
     - Then run apt upgrade
   - Next, install PostgreSQL
     - Use apt install
     - Verify with psql --version
```

**After:**
```markdown
1. Install PostgreSQL (5 min)

```bash
sudo apt update && sudo apt install -y postgresql
psql --version
# Expected: psql (PostgreSQL) 14.x
```
```

## Automatic Triggers

```bash
# Run on save (via file watcher)
python3 scripts/simplify-skill.py --watch ~/Skills_librairie/skills

# Run on commit (pre-commit hook)
# .git/hooks/pre-commit:
for skill in $(git diff --cached --name-only | grep SKILL.md); do
    python3 scripts/simplify-skill.py "$(dirname $skill)"
done

# Run before packaging
python3 scripts/simplify-skill.py skills/* --batch
```

## Metrics

```bash
# Show metrics before/after
python3 scripts/simplify-skill.py skill-path --metrics

# Output:
# Complexity Metrics:
# 
# Before simplification:
# - Total words: 1,845
# - Total tokens: 12,340
# - Avg sentence length: 28 words
# - Nested sections: 5
# - Redundant patterns: 8
# 
# After simplification:
# - Total words: 1,120 (-39%)
# - Total tokens: 7,680 (-38%)
# - Avg sentence length: 19 words
# - Nested sections: 0
# - Redundant patterns: 0
# 
# Improvements:
# ✓ More concise
# ✓ Better readability
# ✓ Preserved all functionality
```

## Safety Checks

Before applying changes, verifies:

1. **Commands still executable**: All bash blocks valid
2. **Links still work**: No broken references
3. **Metadata preserved**: Frontmatter intact
4. **Sections present**: Required sections remain
5. **Examples valid**: Code blocks syntactically correct

```bash
# Dry run (show changes without applying)
python3 scripts/simplify-skill.py skill-path --dry-run

# Apply only safe changes
python3 scripts/simplify-skill.py skill-path --safe-only

# Require manual approval
python3 scripts/simplify-skill.py skill-path --interactive
```

## Configuration

```yaml
# .simplifier-config.yml

rules:
  max_sentence_length: 25
  remove_obvious_comments: true
  consolidate_examples: true
  flatten_nested_sections: true
  standardize_time_format: true
  
preserv e:
  - frontmatter
  - code_blocks
  - troubleshooting_sections
  - validation_steps

aggressive_mode: false  # More conservative by default
```

## Reference Files

- **scripts/simplify-skill.py** - Main simplification engine
- **scripts/analyze-complexity.py** - Complexity metrics
- **references/simplification-patterns.md** - Common patterns
- **references/style-guide.md** - Enforced standards
- **assets/config-template.yml** - Configuration options

## Related Skills

- **skill-quality-auditor** - Check quality after simplification
- **skill-consistency-enforcer** - Enforce style guide
- **skill-code-simplifier** - Based on Anthropic's code-simplifier
