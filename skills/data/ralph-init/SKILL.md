---
name: ralph-init
description: Initialize a project with Ralph workflow structure (specs, prompts, loop script). Use when starting a new project or adding Ralph workflow to an existing project.
---

# Ralph Init

Initialize a project with the Ralph workflow structure for autonomous AI-driven development.

## Ralph Philosophy

Ralph is a loop-based autonomous development workflow. Key principles:

**Three Phases:**
1. **Define** - Write specs for each topic of concern (one spec = one topic)
2. **Plan** - Gap analysis: compare specs vs code, generate prioritized task list
3. **Build** - Implement one task per loop iteration, commit, repeat

**Context is Everything:**
- Each loop iteration starts with fresh context
- Use subagents for exploration (preserves main context)
- IMPLEMENTATION_PLAN.md persists state between iterations
- AGENTS.md captures operational learnings

**Backpressure Steers Quality:**
- Tests, typechecks, lints reject invalid work
- Loop continues until backpressure passes
- "Run tests" in prompt, specific commands in AGENTS.md

**Let Ralph Ralph:**
- Trust the loop to self-correct through iteration
- Plan is disposable - regenerate when wrong
- Observe failures, add guardrails to prompts/AGENTS.md

Reference: [Ralph Playbook](https://github.com/ClaytonFarr/ralph-playbook)

## What Gets Created

```
project/
├── specs/
│   ├── README.md               # Spec writing guide
│   └── (example-spec.md)       # Optional example spec
├── AGENTS.md                   # Project guide (commands, architecture, patterns)
├── IMPLEMENTATION_PLAN.md      # Task list (generated during planning)
├── PROMPT_plan.md              # Planning mode prompt
├── PROMPT_build.md             # Building mode prompt
└── loop.sh                     # Ralph loop script (executable)
```

**Note:** AGENTS.md serves as the project's CLAUDE.md - they are the same concept. Some projects symlink `CLAUDE.md → AGENTS.md`.

## Step 1: Gather Project Info

Ask the user:
1. **Project name** - Name for the header
2. **Project description** - One-line description
3. **Project goal** - What this project achieves (for PROMPT_plan.md)
4. **Source location** - Where is source code? (default: `src`)
5. **Shared utilities** - Where are shared components? (default: `src/lib`)
6. **Package manager** - bun (default), pnpm, or npm

## Step 2: Check Existing Files

Check if target files exist. If so, ask whether to skip or overwrite each.

## Step 3: Copy Templates

Templates location: `~/.claude/skills/ralph-init/templates/`

| Template | Destination | Action |
|----------|-------------|--------|
| `AGENTS.md` | `./AGENTS.md` | Replace placeholders |
| `specs-README.md` | `./specs/README.md` | Copy as-is |
| `example-spec.md` | `./specs/example-auth.md` | Optional - ask user |
| `IMPLEMENTATION_PLAN.md` | `./IMPLEMENTATION_PLAN.md` | Copy as-is |
| `PROMPT_plan.md` | `./PROMPT_plan.md` | Replace placeholders |
| `PROMPT_build.md` | `./PROMPT_build.md` | Replace placeholders |
| `loop.sh` | `./loop.sh` | Copy + chmod +x |

## Step 4: Replace Placeholders

In AGENTS.md:
- `{{PROJECT_NAME}}` → project name
- `{{PROJECT_DESCRIPTION}}` → project description
- `{{SOURCE_DIR}}` → source location

In PROMPT_plan.md and PROMPT_build.md:
- `{{SOURCE_DIR}}` → source location (e.g., `src`)
- `{{SHARED_UTILS}}` → shared utilities (e.g., `src/lib`)
- `{{PROJECT_GOAL}}` → project goal

## Step 5: Customize AGENTS.md

After copying, help the user customize:

1. **Commands** - Update for their package manager choice
2. **Architecture** - Explore their project structure and fill in the ASCII tree
3. **Reference Implementations** - Identify good examples in their codebase
4. **Database commands** - Adjust for their ORM/database

## Step 6: Make loop.sh Executable

```bash
chmod +x loop.sh
```

## Step 7: Optional CLAUDE.md Symlink

Ask if they want to symlink CLAUDE.md to AGENTS.md:
```bash
ln -s AGENTS.md CLAUDE.md
```

This makes the file discoverable as both names.

## Step 8: Summary

```
Ralph workflow initialized!

Created:
  specs/README.md           - Spec writing guide
  specs/example-auth.md     - Example spec (if requested)
  AGENTS.md                 - Project guide
  IMPLEMENTATION_PLAN.md    - Task list
  PROMPT_plan.md            - Planning prompt
  PROMPT_build.md           - Building prompt
  loop.sh                   - Loop script

Next steps:
  1. Review and customize AGENTS.md for your project
  2. Write specs in specs/ for your features
  3. Run ./loop.sh plan to generate implementation plan
  4. Review the plan
  5. Run ./loop.sh to start building

For interactive development:
  - superpowers:test-driven-development for TDD
  - ultra-frontend for UI components
```

## Templates Overview

### AGENTS.md (Comprehensive)
Based on Geoff Huntley's loom AGENTS.md structure:
- Tech stack
- Development philosophy
- Specifications guidance
- Reference implementations
- Commands (dev, validation, database)
- Deployment
- Architecture
- Svelte 5 patterns
- Code quality guidelines
- Testing philosophy
- Common pitfalls
- Troubleshooting
- Operational notes
- Development workflow

### example-spec.md
A complete example spec (User Authentication) showing:
- Purpose
- Requirements
- Acceptance criteria
- Edge cases
- API endpoints
- Dependencies

Use this as a reference for writing specs.
