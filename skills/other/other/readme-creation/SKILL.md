---
name: readme-creation
description: |
  Generate self-contained README files that enable instant developer onboarding.
  Use when creating or updating directory or root repository documentation.
  Triggers: "create readme", "readme", "document directory", "write readme", "root readme".
license: MIT
metadata:
  author: KemingHe
  version: "3.0.0"
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

- Use `tree` or list files at THIS level only (non-recursive)
- Identify: What problem does this directory solve?
- Look for naming patterns in files/subdirectories
- **Detect if this is a root README**: Check if the target directory contains a `.git/` directory or is the repository root
- If root README detected, follow the Root README Mode below before proceeding to Step 2
- If subdirectory README, read root README.md and parent README.md for context

### Root README Mode

Root READMEs are a special case requiring additional context gathering. Auto-detect the following, then **always confirm with the user** before generating:

**Repo visibility**:

- Check for LICENSE, CONTRIBUTING.md, SECURITY.md at project root
- If all three exist, likely a public repo - ask user to confirm
- If missing, likely a private repo - ask user to confirm
- Public repos: Include References to LICENSE, CONTRIBUTING.md, SECURITY.md if they exist; suggest creating them if missing
- Private repos: Skip license/contributing/security sections; ask about internal docs, wikis, or team-specific resources

**Platform detection**:

- Check for `.github/` directory at project root - indicates GitHub
- Check for `.gitlab/` directory at project root - indicates GitLab
- If both or neither, ask user which platform
- GitHub repos: Reference GitHub Issues for questions/support
- GitLab repos: Reference GitLab Issues for questions/support

### Step 2: Write with 30-Second Test in Mind

Structure for scannability:

1. **Title + metadata** - identity
2. **Overview** - what and why (most critical - first thing devs read)
3. **Directory structure or patterns** - what's here (this level only)
4. **Quick links** - where to go next
5. **Prerequisites/Getting Started** - how to use (if operational)
6. **References** - additional context (root READMEs: adjust per visibility and platform)

### Step 3: Validate Self-Containment

Ask: "If a dev lands here with zero context, do they understand in 30 seconds?"

- Purpose clear without reading parent?
- No broken assumptions about prior knowledge?
- Links provide escape hatches to details?
- Root READMEs: Does the References section match the repo's actual visibility and platform?

## Output Format

Present README in markdown following template structure. Target ~50 lines, max 100.

## General Doc Constraints

Apply to all generated output. If a discovered template deviates from any rule (e.g., uses emojis semantically, uses a different bullet convention), note the deviation explicitly and confirm with the user before treating it as a permitted exception.

- **Characters**: QWERTY keyboard typeable only - no smart quotes, emojis, or special Unicode anywhere. In prose, do not use em-dashes or em-dash substitutes (`--`, ` -- `); use ` - ` (space-dash-space) for clause separation instead. Exception: `↑` for ToC navigation.
- **Inline formatting**: Use `_underscore_` for italics, not `*single-star*`. Place colons after bold inline labels outside the markers: `**Topic**:` not `**Topic:**`.
- **Bullets**: Use `-` for all unordered lists; one bullet per complete thought; never wrap a bullet's content mid-sentence onto a continuation line - split into separate bullets if too long or multi-thought. Nested sub-bullets for component grouping are permitted. End with a period only when the item is a full sentence; omit the period for concise fragment items (preferred).
- **Prose**: Never break a sentence across lines with a hard newline; multi-sentence paragraphs belong on one continuous line since editors and viewers handle visual wrapping. Exception: commit message bodies use one sentence per line for `git log` readability.
- **Template hygiene**: Delete `(optional)` and any parenthetical conditional label (e.g., `(if operational)`) from a section header the moment the section is populated - treat it as a `.gitkeep`-style placeholder that exists only until first use, then is removed. Omit the entire section (header and body) when unused. Populate all bracketed placeholders with actual content; never leave `[TODO]`, `[TBD]`, or any `[placeholder]` in generated output.
- **Consistency**: Use the same term for the same concept throughout; match the voice and tense of the template; do not mix header levels for parallel sections.
- **KISS and DRY**: Each section and bullet conveys unique information - no redundancy or overlap.

> General Doc Constraints v1.1.0 - KemingHe/common-devx

## Skill Constraints

- **Self-contained**: README makes sense without parent context
- **30-second rule**: Purpose clear at first scan
- **Non-recursive**: Document THIS level only, link to subdirectory READMEs
- **Pattern over listing**: Consider documenting naming patterns for large directories
- **Link to README.md**: Use `[Dir](../dir/README.md)` not `../dir/`
- **Root README mode**: Always confirm repo visibility (public/private) and platform (GitHub/GitLab) with user before generating a root README
