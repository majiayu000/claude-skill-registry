---
name: generate-agents-md
description: |
  Cross-tool compatibility workflow. Use when generating AGENTS.md files
  for compatibility with other AI coding tools, or creating tool-specific
  instruction files from CLAUDE.md.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: workflow
---

# Generate AGENTS.md

Extract operational content from CLAUDE.md to create a universal AGENTS.md file for cross-tool compatibility with Cursor, Codex, Copilot, and other AI agents.

## Overview

This workflow extracts the Operations and Boundaries sections from CLAUDE.md to generate a minimal, universal AGENTS.md file that works across 20+ AI coding tools.

**Why generate instead of symlink?**
- Symlinks may not work on all systems (Windows)
- AGENTS.md can be customized without affecting CLAUDE.md
- Some teams prefer explicit files over symlinks
- Allows for tool-specific adjustments

## When to Use

✅ **Use this workflow when:**
- Team uses multiple AI tools (Cursor + Claude Code, Codex + Claude)
- Deploying to systems where symlinks don't work well
- Want a standalone AGENTS.md for open-source projects
- Need to customize AGENTS.md separately from CLAUDE.md

❌ **Use symlink instead when:**
- Only team uses Claude Code and one other tool
- System supports symlinks reliably
- Want single source of truth with no drift

**Symlink command**: `ln -s CLAUDE.md AGENTS.md`

---

## Process

### Step 1: Analyze CLAUDE.md

AI reads CLAUDE.md and identifies:
1. **Operations section** - Setup, Testing, Build, Code Style commands
2. **Boundaries section** - Protected files, never commit, ask before
3. **Project-specific customizations** (if any)

### Step 2: Generate AGENTS.md

Create `AGENTS.md` with AGENTS.md standard structure:

```markdown
# AGENTS.md

> Auto-generated from CLAUDE.md. For full methodology, see CLAUDE.md.
> Last generated: [DATE]

## Project Overview
[Brief description - AI extracts from README or project.md if available]

## Setup Commands
[Extracted from CLAUDE.md Operations section]

## Testing
[Extracted from CLAUDE.md Operations section]

## Build & Deploy
[Extracted from CLAUDE.md Operations section]

## Code Style
[Extracted from CLAUDE.md Operations section]

## Boundaries
[Extracted from CLAUDE.md Boundaries section]

---

*For detailed guardrails, 4D methodology, and workflows, see [CLAUDE.md](./CLAUDE.md)*
```

### Step 3: Verify and Save

1. AI presents generated AGENTS.md for review
2. User approves or requests changes
3. Save to project root: `./AGENTS.md`

---

## AGENTS.md Template

```markdown
# AGENTS.md

> Auto-generated from CLAUDE.md | Last updated: YYYY-MM-DD
> Full documentation: [CLAUDE.md](./CLAUDE.md)

## Project Overview

[PROJECT_NAME] - [BRIEF_DESCRIPTION]

**Tech Stack**: [PRIMARY_TECHNOLOGIES]
**Language**: [PRIMARY_LANGUAGE]

## Setup Commands

```bash
# Install dependencies
[INSTALL_COMMAND]

# Start development server
[DEV_COMMAND]

# Environment setup
cp .env.example .env
```

## Testing

```bash
# Run all tests
[TEST_COMMAND]

# Run with coverage (target: >80% business logic)
[COVERAGE_COMMAND]

# Watch mode
[WATCH_COMMAND]
```

## Build & Deploy

```bash
# Production build
[BUILD_COMMAND]

# Type check
[TYPECHECK_COMMAND]

# Lint
[LINT_COMMAND]
```

## Code Style

```bash
# Format code
[FORMAT_COMMAND]

# Lint and fix
[LINT_FIX_COMMAND]
```

**Conventions**:
- [STYLE_RULE_1]
- [STYLE_RULE_2]
- [STYLE_RULE_3]

## Boundaries

### Do Not Modify
- Lock files (`package-lock.json`, `yarn.lock`, `Cargo.lock`)
- Environment files (`.env`, `.env.local`)
- CI/CD configurations (`.github/workflows/`)
- Applied database migrations

### Never Commit
- Secrets, API keys, credentials
- `.env` files (use `.env.example`)
- Build artifacts, `node_modules/`, `target/`

### Ask Before Changing
- Authentication/authorization logic
- Database schemas
- Public API contracts
- Major dependencies

---

## Additional Context

For detailed development guidelines, see:
- **Full Methodology**: [CLAUDE.md](./CLAUDE.md)
- **Skills**: [.claude/skills/](./agent/skills/)

*This file follows the [AGENTS.md](https://agents.md) standard.*
```

---

## Customization Guide

### Project-Specific Adjustments

When generating AGENTS.md, AI should:

1. **Detect tech stack** from:
   - `package.json` (Node.js)
   - `requirements.txt` / `pyproject.toml` (Python)
   - `go.mod` (Go)
   - `Cargo.toml` (Rust)

2. **Extract actual commands** from:
   - `package.json` scripts
   - `Makefile`
   - `justfile`
   - CI/CD workflows

3. **Include project-specific boundaries** from:
   - `CLAUDE.md` (if exists)
   - Existing `.gitignore` patterns

### Monorepo Support

For monorepos, generate nested AGENTS.md files:

```
project/
├── AGENTS.md              # Root-level (general)
├── CLAUDE.md              # Full methodology
├── packages/
│   ├── api/
│   │   └── AGENTS.md      # API-specific commands
│   └── web/
│       └── AGENTS.md      # Web-specific commands
```

Each nested AGENTS.md should:
- Focus on that package's commands
- Reference root AGENTS.md for general guidelines
- Include package-specific boundaries

---

## Maintenance

### When to Regenerate

Regenerate AGENTS.md when:
- CLAUDE.md Operations section changes
- New build/test commands added
- Project structure changes significantly
- Tech stack updated

### Keeping in Sync

**Option A: Manual regeneration**
```bash
# Load this skill periodically when CLAUDE.md changes
.claude/skills/generate-agents-md/SKILL.md
```

**Option B: Pre-commit hook**
```bash
# .husky/pre-commit or similar
# Check if CLAUDE.md changed, regenerate AGENTS.md
```

**Option C: CI/CD check**
```yaml
# .github/workflows/check-agents-md.yml
- name: Verify AGENTS.md is up to date
  run: |
    # Compare timestamps or checksums
```

---

## Example Usage

### Request
```
Generate AGENTS.md for this project using the generate-agents-md skill
```

### AI Response
```
I'll analyze your project and generate an AGENTS.md file.

**Detected:**
- Tech stack: TypeScript, React, Node.js
- Package manager: npm
- Test framework: Vitest
- Linter: ESLint + Prettier

**Generated AGENTS.md:**
[Shows preview]

**Save to:** ./AGENTS.md

Approve? [Yes/No/Edit]
```

---

## Integration with CLAUDE.md

### How They Work Together

| File | Purpose | Audience |
|------|---------|----------|
| `CLAUDE.md` | Full methodology + guardrails | Claude Code |
| `AGENTS.md` | Operational commands | All AI tools |

### Reading Priority (Claude Code)

1. Claude Code reads `CLAUDE.md` (primary)
2. If `CLAUDE.md` not found, reads `AGENTS.md` (fallback)
3. Both can coexist (different purposes)

### For Other Tools

Most tools (Cursor, Codex, Copilot) read:
1. `AGENTS.md` (primary)
2. May also read `CLAUDE.md` if present

---

## Troubleshooting

### Issue: AGENTS.md and CLAUDE.md out of sync
**Solution**: Regenerate AGENTS.md or set up sync mechanism

### Issue: Other tools not reading AGENTS.md
**Solution**: Ensure file is in project root, named exactly `AGENTS.md`

### Issue: Symlink not working
**Solution**: Use this skill to generate actual file instead

### Issue: Need different commands for different tools
**Solution**: Generate AGENTS.md with common subset, add tool-specific comments

---

**Remember**: AGENTS.md is for operational commands. Keep it minimal and actionable. Full methodology stays in CLAUDE.md.
