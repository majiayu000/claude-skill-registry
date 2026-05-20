---
name: ralph-init
description: Initialize a project with Ralph workflow structure (specs, prompts, loop script). Use when starting a new project or adding Ralph workflow to an existing project.
---

# Ralph Init

Initialize a project with the Ralph workflow for autonomous AI-driven development.

## The Ralph Workflow

Ralph is Geoffrey Huntley's loop-based autonomous development methodology.

**Three Phases:**
1. **Define** - Write specs for topics of concern (`specs/*.md`)
2. **Plan** - Gap analysis: compare specs vs code → `IMPLEMENTATION_PLAN.md`
3. **Build** - Implement one task per loop, commit, repeat

**Core Principles:**
- **Context is everything** - Fresh context each iteration, subagents preserve main context
- **Backpressure steers quality** - Tests/typechecks/lints reject invalid work
- **Let Ralph Ralph** - Trust self-correction through iteration, plans are disposable

Reference: [Ralph Playbook](https://github.com/ClaytonFarr/ralph-playbook)

## Project Structure

**IMPORTANT: Workflow files ALWAYS at project root. Specs in `specs/` at root.**

```
project/
├── loop.sh                    # Ralph loop script (runs from here)
├── PROMPT_plan.md             # Planning mode prompt
├── PROMPT_build.md            # Building mode prompt
├── IMPLEMENTATION_PLAN.md     # Task list (generated/updated by Ralph)
├── AGENTS.md                  # Operational guide (~60 lines max, brief!)
├── specs/                     # Specifications directory
│   ├── README.md              # Lookup table: spec → code
│   └── [topic].md             # One spec per topic of concern
└── src/                       # Source code
    └── lib/                   # Shared utilities & components
```

**Why root?** The loop runs from project root. PROMPTs reference `specs/*` and `@IMPLEMENTATION_PLAN.md`. Everything must be accessible from root.

**AGENTS.md must stay brief:** Operational commands only. No status updates, no progress notes. Those go in IMPLEMENTATION_PLAN.md. A bloated AGENTS.md pollutes every loop's context.

## Step 1: Gather Project Info

Ask the user:
1. **Project name** - Name for AGENTS.md header
2. **Specs location** - Where will specs live? (default: `specs/`)
3. **Source location** - Where is source code? (default: `src`)
4. **Project goal** - One sentence describing what success looks like
5. **Key commands** - Build, test, typecheck, lint commands (can leave as placeholders)

## Step 2: Copy Templates

Templates location: `~/.claude/skills/ralph-init/templates/`

| Template | Destination | Notes |
|----------|-------------|-------|
| `loop.sh` | `./loop.sh` | chmod +x |
| `PROMPT_plan.md` | `./PROMPT_plan.md` | Replace `{{SPECS_DIR}}`, `{{SOURCE_DIR}}`, `{{LIB_DIR}}`, `{{PROJECT_GOAL}}` |
| `PROMPT_build.md` | `./PROMPT_build.md` | Replace `{{SPECS_DIR}}`, `{{SOURCE_DIR}}`, `{{LIB_DIR}}` |
| `AGENTS.md` | `./AGENTS.md` | Replace all `{{...}}` placeholders with project commands |
| `IMPLEMENTATION_PLAN.md` | `./IMPLEMENTATION_PLAN.md` | Empty starting point |
| `specs-README.md` | `./specs/README.md` | Clean lookup table template |

**CRITICAL:** Copy templates VERBATIM. Do NOT improvise. The numbered rules (99999, 999999, etc.) are intentional.

## Step 3: Create specs/README.md

The specs README is a **lookup table** linking specs to code. Follow the Loom pattern:

```markdown
# [Project] Specifications

[One-line description]

## [Category Name]

| Spec | Code | Purpose |
|------|------|---------|
| [spec-name.md](./spec-name.md) | [dir/](../src/dir/) | Brief purpose |
```

**Keep it clean:**
- No workflow documentation (that's in PROMPT files)
- No verbose explanations
- Just specs linked to code they affect
- Group by logical category if many specs

## Step 4: Make Executable

```bash
chmod +x loop.sh
```

## Step 5: Summary

```
Ralph initialized!

Created at project root:
  loop.sh                 - Run with ./loop.sh or ./loop.sh plan
  PROMPT_plan.md          - Planning mode (gap analysis)
  PROMPT_build.md         - Building mode (implementation)
  AGENTS.md               - Operational guide (keep brief!)
  IMPLEMENTATION_PLAN.md  - Task list
  specs/README.md         - Spec index

Usage:
  1. Write specs in specs/
  2. ./loop.sh plan       # Generate implementation plan
  3. Review plan
  4. ./loop.sh            # Start building
```

## Template Placeholders

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{PROJECT_NAME}}` | Project name for AGENTS.md | `My App` |
| `{{SPECS_DIR}}` | Path to specs from root | `specs/` |
| `{{SOURCE_DIR}}` | Path to source code | `src` |
| `{{LIB_DIR}}` | Path to shared utilities | `src/lib` |
| `{{PROJECT_GOAL}}` | One-sentence success criteria | "Build a task management app" |
| `{{TEST_CMD}}` | Test command | `npm test` or `[test command]` |
| `{{TYPECHECK_CMD}}` | Typecheck command | `npm run check` or `[typecheck command]` |
| `{{LINT_CMD}}` | Lint command | `npm run lint` or `[lint command]` |
| `{{BUILD_CMD}}` | Build command | `npm run build` or `[build command]` |
| `{{DEV_CMD}}` | Dev server command | `npm run dev` or `[dev command]` |
