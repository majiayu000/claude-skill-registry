---
name: doc-scanner
description: "Scans for project documentation files (AGENTS.md, CLAUDE.md, GEMINI.md, COPILOT.md, CURSOR.md, WARP.md, and 15+ other formats) and synthesizes guidance. Auto-activates when user asks to review, understand, or explore a codebase, when starting work in a new project, when asking about conventions or agents, or when documentation context would help. Can consolidate multiple platform docs into unified AGENTS.md."
allowed-tools: "Glob Read Write Bash"
---

# Documentation Scanner

Scan for and synthesize project documentation.

## When to Activate

- User asks to review, understand, or explore a codebase
- Starting work in a new/unfamiliar project
- User asks about project conventions or workflows
- Before making significant architectural decisions

## Instructions

### Step 1: Scan for Documentation

Use Glob to search project root:

```
AGENTS.md, CLAUDE.md, AI.md, ASSISTANT.md,
GEMINI.md, COPILOT.md, CHATGPT.md, CODEIUM.md,
CURSOR.md, WINDSURF.md, VSCODE.md, JETBRAINS.md,
WARP.md, FIG.md, DEVCONTAINER.md, GITPOD.md
```

### Step 2: Read All Found Files

Read complete contents of every documentation file found.

### Step 3: Synthesize

Combine information into unified summary:

```
PROJECT DOCUMENTATION

Sources: [list files found]

RECOMMENDED AGENTS
  Primary: [agents for core work]
  Secondary: [agents for specific tasks]

KEY WORKFLOWS
  [consolidated workflows]

CONVENTIONS
  [code style, patterns]

QUICK COMMANDS
  [common commands]
```

### Step 4: Offer Consolidation

If 2+ documentation files exist, offer to consolidate:

1. Create `.doc-archive/` directory
2. Archive originals with date suffix
3. Generate unified AGENTS.md
4. Report what was consolidated

### Step 5: No Documentation Found

If none found, offer to generate AGENTS.md based on:
- Project structure and tech stack
- Patterns observed in codebase

## Priority Order

1. AGENTS.md (platform-agnostic)
2. CLAUDE.md (Claude-specific)
3. Other AI docs
4. IDE docs
5. Terminal docs

## Additional Resources

For detailed patterns, load:
- `./references/file-patterns.md` - Complete list of files to scan
- `./references/templates.md` - AGENTS.md generation templates
