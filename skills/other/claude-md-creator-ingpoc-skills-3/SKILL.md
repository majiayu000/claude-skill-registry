---
name: claude-md-creator
description: "Use when creating CLAUDE.md files, updating existing CLAUDE.md, validating CLAUDE.md structure, or auto-fixing CLAUDE.md issues. Load for setting up project instructions, global guidelines, local overrides, or modular rules. Handles global (~/.claude/CLAUDE.md), project (.claude/CLAUDE.md), local (CLAUDE.local.md), and rules (.claude/rules/*.md) with smart project detection and template generation."
keywords: claude-md, instructions, setup, configuration, guidelines, project-setup
---

# CLAUDE.md Creator

Create, validate, and maintain CLAUDE.md files with intelligent project detection.

## Workflow Decision Tree

```
                    User Request
                        │
            ┌───────────┴───────────┐
            │   What's needed?      │
            └───────────┬───────────┘
         ┌──────────────┼──────────────┐
         │              │              │
    Create new    Update existing   Validate/Fix
         │              │              │
    ┌────┴────┐    ┌────┴────┐    ┌───┴────┐
    │         │    │         │    │        │
  Which      Detect   Merge    Auto-fix   Auto-fix
  type?      context  changes  issues    issues
    │         │        │        │         │
  Detect    Project   Ask      Run       Run
  context    type     user     fix       fix
    │         │      changes   script    script
    └────┬────┘       │        │         │
         │           │        │         │
    Generate    Generate     Validate   Validate
    content     content      output     output
         │           │        │         │
         └───────────┴────────┴─────────┘
                       │
                  Write to
                  file
```

## Quick Start

| Task | Command |
|------|---------|
| Create project CLAUDE.md | `scripts/generate-claude-md.py --type project` |
| Update existing file | `scripts/update-claude-md.py <path>` |
| Validate file | `scripts/validate-claude-md.py <path>` |
| Auto-fix issues | `scripts/auto-fix-claude-md.py <path>` |
| Detect context | `scripts/detect-claude-type.py` |

## Step 1: Determine CLAUDE.md Type

**Script:** `scripts/detect-claude-type.py`

**Detection Logic:**

| Context | Path | Size Target | When to Use |
|---------|------|-------------|-------------|
| Global | `~/.claude/CLAUDE.md` | 50-150 lines | Personal preferences across all projects |
| Project | `.claude/CLAUDE.md` | 100-300 lines | Team instructions for this project |
| Local | `CLAUDE.local.md` | <50 lines | Personal overrides for this project |
| Rules | `.claude/rules/*.md` | 20-100 each | Modular topics by subject |

## Step 2: Detect Project Type

**Script:** `scripts/detect-project.py`

Scans for project markers to generate smart defaults:

| Marker | Language | Framework | Template Used |
|--------|----------|-----------|---------------|
| `package.json` + "next" | TypeScript | Next.js | `nodejs.md` |
| `package.json` + "react" + "vite" | TypeScript | Vite React | `nodejs.md` |
| `requirements.txt` + "fastapi" | Python | FastAPI | `python.md` |
| `requirements.txt` + "django" | Python | Django | `python.md` |
| `Cargo.toml` | Rust | - | `rust.md` |
| `go.mod` | Go | - | `go.md` |
| None detected | - | - | `general.md` |

## Step 3: Generate CLAUDE.md

**Script:** `scripts/generate-claude-md.py`

**Template Selection:**
```
Base template (assets/*.template.md)
    +
Language template (assets/framework-templates/*.md)
    +
Project-specific data (detected)
    =
Final CLAUDE.md
```

## Step 4: Validate Structure

**Script:** `scripts/validate-claude-md.py`

**Checks Performed:**

| Category | Check | Error Level |
|----------|-------|-------------|
| Frontmatter | Valid YAML fence | ❌ Error |
| Frontmatter | Required fields | ❌ Error |
| Structure | Section headers | ⚠️ Warning |
| Best practices | Line count | ⚠️ Warning |
| Best practices | Table format | ⚠️ Warning |
| Content | Command validity | ⚠️ Warning |
| Content | Path references | ⚠️ Warning |

## Step 5: Auto-Fix Issues

**Script:** `scripts/auto-fix-claude-md.py`

**Auto-Fixes:**

| Issue | Fix | Backup |
|-------|-----|--------|
| Missing frontmatter | Add YAML fence | ✅ Yes |
| Empty sections | Remove or placeholder | ✅ Yes |
| Malformed tables | Convert to proper Markdown | ✅ Yes |
| Extra blank lines | Collapse to 1 line | No |
| Inconsistent headings | Normalize to H2/H3 | ✅ Yes |
| Missing commands | Add from project detection | ✅ Yes |

**Run modes:**
```bash
# Dry run
./auto-fix-claude-md.py --dry-run <path>

# Auto-fix all
./auto-fix-claude-md.py <path>

# Fix specific category
./auto-fix-claude-md.py --category structure <path>
```

## Step 6: Update Existing

**Script:** `scripts/update-claude-md.py`

**Merge Strategy:**
1. Read existing CLAUDE.md
2. Detect project changes
3. Ask user what to update
4. Preserve custom sections
5. Write updated file

## Best Practices

| Principle | Target |
|-----------|--------|
| **Tables > Prose** | Use tables for commands, configs |
| **Specific commands** | Extract real commands from package.json |
| **Line targets** | Global: 50-150, Project: 100-300, Local: <50, Rules: 20-100 |
| **Progressive disclosure** | Quick start → detailed → references |

## Resources

### scripts/

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `detect-claude-type.py` | Determine CLAUDE.md type | Auto-detection |
| `detect-project.py` | Scan project markers | Before generation |
| `generate-claude-md.py` | Create from templates | New file creation |
| `validate-claude-md.py` | Check structure | After edits |
| `auto-fix-claude-md.py` | Fix issues | Validation fails |
| `update-claude-md.py` | Update existing | Project changes |

### references/

| File | Load When |
|------|-----------|
| `best-practices.md` | Writing content |
| `validation-rules.md` | Understanding errors |
| `project-detection.md` | Extending detection |
| `examples/` | Real-world patterns |

### assets/

| File | Purpose |
|------|---------|
| `global.template.md` | Personal preferences |
| `project.template.md` | Team instructions |
| `local.template.md` | Personal overrides |
| `rule.template.md` | Modular topics |
| `framework-templates/*.md` | Language/framework additions |
