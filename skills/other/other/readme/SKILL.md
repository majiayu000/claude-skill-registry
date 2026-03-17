---
name: readme
description: |
  Generate self-contained README files that enable instant developer onboarding.
  Use when creating or updating directory documentation.
  Triggers: "create readme", "readme", "document directory", "write readme".
license: MIT
metadata:
  author: KemingHe
  version: "2.1.0"
---

# README Generation

Generate self-contained README files that enable developers to instantly understand any directory without reading parent or child documentation.

**Temporary persona**: Senior engineering manager with expertise in developer experience and technical onboarding.

## When to Use This Skill

- Creating README for a new directory
- Updating existing README after structural changes
- Ensuring consistent documentation across repository

## Core Philosophy

**READMEs are entry points, not manuals.**

| Principle | Implication |
| :--- | :--- |
| **Self-contained** | Stands alone - no need to read parent first |
| **30-second test** | Purpose clear within 30 seconds of scanning |
| **Context flows down** | Provides context, links to children for details |
| **Loose coupling** | If directory moves, README still makes sense |

## What Makes a README Effective

**Good README**:

- First 3 lines answer "What is this and why does it exist?"
- Structure visible at a glance (scannable headers)
- Links OUT to details, doesn't duplicate them
- Works as standalone landing page

**Anti-patterns**:

- Requires reading parent README to understand context
- Buries purpose below directory structure
- Duplicates content from other files
- Documents subdirectory internals (violates loose coupling)
- Over 100 lines (too much for quick orientation)

## Documenting Patterns (Large/Flat Directories)

For directories with many similarly-named files, consider documenting the **naming pattern** instead of listing every file. This reduces maintenance when files are added or removed.

**Example pattern table**:

| Pattern | Purpose |
| :--- | :--- |
| `[type]-[tech-and-description].md` | Guides categorized by type |
| `[skill-name]/` | Skill directories with standard structure |

Use your judgment - patterns work well for consistent naming conventions, explicit lists work better for small or varied collections.

## Asset Resolution

1. Check `./assets/readme-template.md` for README template
2. If not found, search `**/readme-template.md` in repository
3. If still not found, use minimal structure from this skill

## Directory Exploration

**Preferred**: Use `tree` command for hierarchical view (may not be installed on all systems):

```shell
tree -L 2 [directory]          # 2-level depth
tree -L 1 --dirsfirst          # Directories first, 1 level
```

**Fallback**: Use `ls` or IDE file listing for flat view.

## Git Operations (Read-Only)

**Setup**: Pipe all git commands to `cat` to avoid interactive mode.

**Safe commands**: `git status | cat`, `git ls-files | cat`, `git log --oneline -5 | cat`

**Forbidden**: git commit, push, pull, merge, rebase, add, reset, clean, stash

## Process

### Step 1: Understand Context

- Read root README.md and parent README.md (if nested)
- Use `tree` or list files at THIS level only (non-recursive)
- Identify: What problem does this directory solve?
- Look for naming patterns in files/subdirectories

### Step 2: Write with 30-Second Test in Mind

Structure for scannability:

1. **Title + metadata** - identity
2. **Overview** - what and why (most critical - first thing devs read)
3. **Directory structure or patterns** - what's here (this level only)
4. **Quick links** - where to go next
5. **Prerequisites/Getting Started** - how to use (if operational)
6. **References** - additional context

### Step 3: Validate Self-Containment

Ask: "If a dev lands here with zero context, do they understand in 30 seconds?"

- Purpose clear without reading parent?
- No broken assumptions about prior knowledge?
- Links provide escape hatches to details?

## Output Format

Present README in markdown following template structure. Target ~50 lines, max 100.

## Constraints

- **Self-contained**: README makes sense without parent context
- **30-second rule**: Purpose clear at first scan
- **Non-recursive**: Document THIS level only, link to subdirectory READMEs
- **Pattern over listing**: Consider documenting naming patterns for large directories
- **Link to README.md**: Use `[Dir](../dir/README.md)` not `../dir/`
- **KISS and DRY**: Say it once, link elsewhere
- **Characters**: QWERTY keyboard typeable only - no em-dashes, smart quotes, emojis, or special Unicode

---

> README Generation Skill v2.1.0 - KemingHe/common-devx
