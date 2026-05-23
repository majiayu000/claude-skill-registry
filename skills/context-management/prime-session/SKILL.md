---
name: prime-session
description: Orient to current project by reading CLAUDE.md and architecture docs. Auto-invokes when Claude detects a new or unfamiliar repository. Can also be triggered by "orient me", "what is this project", or "prime session".
tools:
  - mcp__serena__*
  - Read
  - Glob
  - Bash:git *
  - Bash:ls *
  - AskUserQuestion
---

# Prime Session Skill

## Purpose

Provide project orientation by reading key documentation files. This skill helps Claude understand the project's architecture, conventions, and current priorities before starting work. It's designed to auto-invoke when entering a new repository.

## Natural Language Triggers

**Automatic Invocation:**
- When Claude detects it's in a new/unfamiliar repository
- When project context seems missing or stale
- At the start of a new conversation in a repo

**Explicit Invocation:**
- "Orient me to this project"
- "What is this project?"
- "Prime session"
- "Get project context"
- "Read the project docs"
- "Familiarize yourself with this codebase"

## Auto-Invoke Conditions

This skill should auto-invoke when:

1. **New Repository Detected:**
   - Claude hasn't seen this repo before in session
   - Git remote URL is unfamiliar

2. **Context Seems Missing:**
   - Claude is unsure about project conventions
   - Module emojis unknown
   - Architecture unclear

3. **User Asks Basic Questions:**
   - "How does this project work?"
   - "What's the structure here?"
   - Questions indicating lack of project context

## Workflow Execution

### Phase 1: Detect Repository

1. **Get Git Context:**
   ```bash
   git remote -v
   git branch --show-current
   pwd
   ```

2. **Identify Project:**
   - Repository name
   - Current branch
   - Working directory

### Phase 2: Read Core Documentation

Read these files in order of priority:

1. **CLAUDE.md** (Primary)
   - Project-specific Claude Code guidance
   - Module definitions and emojis
   - Development priorities
   - Conventions and standards

2. **README.md** (Secondary)
   - Project overview
   - Installation/setup
   - High-level architecture

3. **Architecture Docs** (If exist)
   - `docs/ARCHITECTURE.md`
   - `docs/DESIGN.md`
   - `CONTRIBUTING.md`

4. **Package/Config Files** (Context)
   - `package.json` (Node.js)
   - `pyproject.toml` (Python)
   - `Cargo.toml` (Rust)
   - `go.mod` (Go)

### Phase 3: Build Mental Model

From the documentation, extract:

1. **Project Identity:**
   - What does this project do?
   - Who is it for?
   - Current development phase

2. **Architecture:**
   - Key components/modules
   - Directory structure
   - Tech stack

3. **Conventions:**
   - Module emojis (from CLAUDE.md)
   - Commit message format
   - Branch naming
   - Code style

4. **Priorities:**
   - Current development focus
   - What NOT to change
   - Quality standards

### Phase 4: Present Orientation

Display a concise summary (don't take any action):

```
📍 Project: {project-name}
   Repository: {owner/repo}
   Branch: {current-branch}

📋 Overview:
   {Brief project description}

🏗️ Architecture:
   {Key components/modules}

🎯 Current Focus:
   {Development priorities from CLAUDE.md}

📦 Modules:
   - {module1} {emoji}: {description}
   - {module2} {emoji}: {description}
   ...

📝 Conventions:
   - Commits: {format}
   - Branches: {format}

✅ Ready to assist with this project.
```

## Orientation Depth

After completing quick orientation, offer deeper exploration:

```
AskUserQuestion:
  question: "Quick orientation complete. Would you like more detail?"
  header: "Depth"
  options:
    - label: "This is enough"
      description: "Continue with current context"
    - label: "Deep dive"
      description: "Read all architecture docs, scan structure, review git history"
    - label: "Specific area"
      description: "Focus on a particular module or component"
```

### Quick Orientation (Default)
- Read CLAUDE.md and README.md
- Extract key conventions
- ~30 seconds

### Deep Orientation (On Request)
- Read all architecture docs
- **Use Serena for semantic structure understanding:**
  - `get_symbols_overview()` on key source files
  - `find_symbol()` to locate major components/modules
  - Build symbol-level mental model without reading entire files
- Scan directory structure (for non-code layout)
- Review recent git history
- Understand current work in progress

**Serena Integration Benefits:**
- Understand code architecture without 100+ file reads
- Get symbol-level structure of main components
- Identify key classes, functions, types efficiently
- Build precise mental model for future work

Trigger deep orientation with:
- User selects "Deep dive" in AskUserQuestion
- "Give me a thorough orientation"
- "Deep dive into this project"
- "I want to understand everything"

## Silent Mode

When auto-invoking, the skill can run silently:
- Read documentation without outputting summary
- Store context for later use
- Only show summary if user asks

## Caching Behavior

To avoid re-reading on every interaction:

1. **Session Memory:**
   - Remember orientation within conversation
   - Don't re-read unless files changed

2. **Staleness Detection:**
   - Check if CLAUDE.md was modified since last read
   - Re-orient if project docs updated

## Error Handling

### No CLAUDE.md Found
```
ℹ️ No CLAUDE.md found in this project.

   This project doesn't have Claude Code-specific guidance.
   Reading README.md for basic orientation...

   Consider creating a CLAUDE.md for better assistance.
```

### No README.md Found
```
⚠️ No README.md or CLAUDE.md found.

   Limited project context available.
   Scanning directory structure for orientation...
```

### Empty Repository
```
ℹ️ This appears to be a new/empty repository.

   No documentation found to orient from.
   Ready to help you set up the project!
```

## Integration with Other Skills

**Provides context to:**
- All other skills - Module emojis, conventions
- `commit-changes` - Commit format
- `setup-work` - Branch naming, priorities

**Auto-invokes before:**
- Any skill that needs project context
- First interaction in a repository

## Best Practices

### ✅ DO:
- Read CLAUDE.md first (most relevant)
- Keep orientation summary concise
- Note current development priorities
- Remember module emojis
- Respect project conventions

### ❌ DON'T:
- Take any actions (orientation only)
- Modify any files
- Make assumptions about undocumented conventions
- Output lengthy summaries (be concise)
- Re-read docs unnecessarily

## Example Output

```
📍 Project: escapement
   Repository: fusupo/escapement
   Branch: main

📋 Overview:
   Generic Claude Code workflow system for structured development.
   Provides skills, commands, and agents for multi-project support.

🏗️ Architecture:
   - skills/     Automated workflow modules
   - commands/   Quick CLI helpers (being converted to skills)
   - agents/     Specialized subagents (extensibility ready)
   - docs/       Extended documentation

🎯 Current Focus:
   - Rearchitecting commands as skills
   - Integrating Claude Code affordances
   - Completing documentation

📦 Modules:
   - workflow 🔄: Core workflow definition
   - skills 🎯: Automated workflow skills
   - commands ⚡: Quick CLI helpers
   - docs 📚: Extended documentation
   - install 🔧: Installation and setup

📝 Conventions:
   - Commits: {emoji}{emoji} type(scope): description
   - Branches: {issue-number}-{description}

✅ Ready to assist with this project.
```

---

**Version:** 1.1.0
**Last Updated:** 2025-12-31
**Maintained By:** Escapement
**Changelog:**
- v1.1.0: Added AskUserQuestion for orientation depth selection
- v1.0.0: Initial conversion from commands/prime-session.md
