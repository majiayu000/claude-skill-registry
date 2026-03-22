---
name: shipflow-init
description: Bootstrap a new project for ShipFlow tracking — detect stack, generate CLAUDE.md, create TASKS.md, register in PROJECTS.md
disable-model-invocation: true
argument-hint: [project-path] (omit to init current directory)
---

## Context

- Current directory: !`pwd`
- Package.json: !`cat package.json 2>/dev/null | head -60 || echo "no package.json"`
- Requirements.txt: !`cat requirements.txt 2>/dev/null | head -20 || echo "no requirements.txt"`
- Shell scripts: !`ls -1 *.sh 2>/dev/null | head -10 || echo "no .sh files"`
- Existing CLAUDE.md: !`head -30 CLAUDE.md 2>/dev/null || echo "no CLAUDE.md"`
- Existing TASKS.md: !`head -20 TASKS.md 2>/dev/null || echo "no TASKS.md"`
- Directory listing: !`ls -la 2>/dev/null | head -30`
- Git remote: !`git remote -v 2>/dev/null | head -2 || echo "no git"`
- Project structure: !`find . -maxdepth 2 -type d 2>/dev/null | grep -v node_modules | grep -v .git | grep -v dist | sort | head -30`

## Mode detection

- **`$ARGUMENTS` is a path** → Init the project at that path.
- **`$ARGUMENTS` is empty** → Init the current directory.

---

## Flow

### Step 1: Detect project type

Analyze the project to determine:
- **Stack**: framework (Astro, Next.js, React, React Native, Vue, Python, Bash), runtime (Node, Python, Bun)
- **Package manager**: npm, yarn, pnpm, pip, none (detect from lockfiles)
- **UI framework**: React, Vue, Svelte, none
- **CSS solution**: Tailwind, UnoCSS, CSS Modules, styled-components, none
- **Content type**: blog, docs, app, CLI, API, library
- **i18n**: locale dirs, i18n config, bilingual content
- **Auth**: Clerk, Auth.js, Supabase Auth, none
- **Backend**: Convex, Supabase, Firebase, custom API, none
- **Payments**: Stripe, LemonSqueezy, none

### Step 2: Generate CLAUDE.md template

Create a `CLAUDE.md` with:

```markdown
# CLAUDE.md

This file provides guidance to Claude Code when working in this project.

## Project Overview
[Auto-detected: name, description, stack]

## Commands
[Auto-detected from package.json scripts, Makefile, or shell scripts]

## Architecture
[Auto-detected: directory structure, key patterns]

## Key Conventions
[Framework-specific conventions based on detected stack]
```

Use **AskUserQuestion** to let the user review and confirm:
- Question: "I've detected [stack summary]. Here's the generated CLAUDE.md — should I create it?"
- Options:
  - **Create as-is** — "Save the generated CLAUDE.md" (Recommended)
  - **Edit first** — "Let me review and adjust before saving"
  - **Skip** — "Don't create CLAUDE.md"

### Step 3: Create TASKS.md

**Architecture**: TASKS.md lives in `~/shipflow_data/projects/[name]/TASKS.md` (personal data, not in git) and is symlinked into the project directory as `[project_dir]/TASKS.md`.

**Check first**: skip entirely if `TASKS.md` already exists (file or symlink) in the project directory.

If it does not exist:
1. Create directory `~/shipflow_data/projects/[name]/`
2. Create `~/shipflow_data/projects/[name]/TASKS.md` with the canonical format below
3. Create symlink: `ln -s ~/shipflow_data/projects/[name]/TASKS.md [project_dir]/TASKS.md`

Never create a bare placeholder — populate with real tasks detected in Step 1:

```markdown
# Tasks — [project name]

> **Priority:** 🔴 P0 blocker · 🟠 P1 high · 🟡 P2 normal · 🟢 P3 low · ⚪ deferred
> **Status:** 📋 todo · 🔄 in progress · ✅ done · ⛔ blocked · 💤 deferred

---

## Setup

| Pri | Task | Status |
|-----|------|--------|
| 🔴 | [First critical task based on detected stack — e.g. "Configure env vars", "Set up auth", "Deploy first build"] | 📋 todo |
| 🟠 | [Second high-priority task] | 📋 todo |

---

## [Core Feature Area — detected from project]

| Pri | Task | Status |
|-----|------|--------|
| 🟠 | [Feature task] | 📋 todo |
| 🟡 | [Normal task] | 📋 todo |

---

## Backlog

| Pri | Task | Status |
|-----|------|--------|
| 🟢 | [Future improvement] | 💤 deferred |

---

## Audit Findings
<!-- Populated by /shipflow-audit — dated sections added automatically:

### Audit: [Domain] (YYYY-MM-DD)

**Fixed:**
- [x] Issue resolved

**Remaining:**
- [ ] 🔴 Blocker still open
- [ ] 🟠 High-priority finding
-->
```

Populate the initial tasks intelligently from what was detected in Step 1 (stack, framework, existing files, package.json scripts). Do not leave placeholder text like `[First critical task]` — replace with real tasks for this project.

### Step 4: Register in PROJECTS.md

Read `/home/claude/shipflow_data/PROJECTS.md` and add a row to both tables:

**Project Registry table**:
```
| [name] | [path] | [stack summary] |
```

**Domain Applicability table** — auto-detect defaults:
- Code: ✓ (always)
- Design: ✓ if has UI
- Copy: ✓ if has user-facing content
- SEO: ✓ if web project with public pages
- GTM: ✓ if commercial intent
- Translate: ✓ if i18n detected
- Deps: ✓ if has package manager
- Perf: ✓ (always)

### Step 5: Create CHANGELOG.md + update master TASKS.md

**CHANGELOG.md** lives directly in the project directory (committed to git, visible to other devs).

If `CHANGELOG.md` doesn't exist in the project dir, create it:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased] — [today's date]

### Added
- Initial project setup
```

**Master TASKS.md** — add a section to `/home/claude/shipflow_data/TASKS.md`:

```markdown
## [project name]

**Stack**: [summary] | **Phase**: Setup
```

### Step 6: Configure codebase-mcp

Configure the Shipflow MCP server for this project by writing (or updating) `.claude/settings.json`:

```json
{
  "mcpServers": {
    "codebase": {
      "command": "python3",
      "args": ["/home/claude/ShipFlow/tools/codebase-mcp/server.py", "[ABSOLUTE_PROJECT_PATH]"]
    }
  }
}
```

- Replace `[ABSOLUTE_PROJECT_PATH]` with the actual absolute path of the project.
- If `.claude/settings.json` already exists and has `mcpServers`, merge the `codebase` key without overwriting other entries.
- Create `.claude/` directory if needed.
- Skip silently if `/home/claude/ShipFlow/tools/codebase-mcp/server.py` doesn't exist.

Also append the codebase-mcp usage protocol to the generated `CLAUDE.md` (after the Commands section):

```markdown
## Context MCP — Token-Saving Protocol

This project uses a local codebase MCP server for efficient context management.

### Every turn:
1. **Call `context_continue` FIRST** — returns files already in memory, avoids re-reads.
2. **Call `context_retrieve`** with your query to find relevant files.
3. **Use `context_read`** instead of Read for code exploration (tracks token budget).
4. **After editing**, call `context_register_edit` with a one-sentence summary.

See `/home/claude/ShipFlow/tools/codebase-mcp/README.md` for full tool reference.
```

### Step 7: Confirm domain applicability

Use **AskUserQuestion**:
- Question: "Which audit domains apply to [project name]?"
- `multiSelect: true`
- Options: Code, Design, Copy, SEO, GTM, Translate, Deps, Perf
- Pre-select based on auto-detection from Step 4
- Description for each: what was detected (or "not detected — opt in manually")

Update PROJECTS.md with the user's confirmed selection.

### Step 8: Report

```
PROJECT INITIALIZED: [name]
═══════════════════════════════════
Stack:     [detected stack]
Path:      [project path]
CLAUDE.md: [created / skipped / already existed]
TASKS.md:  [created / skipped / already existed]
MCP:       [configured / skipped]
PROJECTS:  [registered / already registered]
Domains:   [list of applicable domains]
═══════════════════════════════════
Next steps:
  /shipflow-audit        — Run initial audit
  /shipflow-check        — Verify build passes
  /shipflow-tasks        — Start tracking work
```

---

## Important

- Never overwrite an existing CLAUDE.md without asking.
- Never overwrite an existing TASKS.md.
- If the project is already in PROJECTS.md, update the row instead of adding a duplicate.
- Detect the stack from actual files, not just project name.
- The generated CLAUDE.md should match the style of existing project CLAUDE.md files in the workspace.
