---
name: project-context-skill
description: |
  Maintains project context and progress tracking across Claude sessions.
  Use at session start to load context, on session end to save progress.
  Triggers: "load project context", "save context", "end session", "what was I working on",
  "switch to [project]", "done for today". Works in both Claude Code and Claude Desktop.
---

# Project Context Loader

## MANDATORY: Project Detection (Run First)

Before ANY other action, identify which project the user is in:

### Claude Code (Terminal)

```bash
pwd  # Get current working directory
```

1. Run `pwd` to get current directory
2. Extract project name from path (last folder name)
3. Load `<pwd>/.claude/PROJECT_CONTEXT.md`
4. **VERIFY**: Does the `# <project-name>` header match the folder name?
   - **YES** → Display context and proceed
   - **NO** → WARN: "Context mismatch! File says [X] but you're in [Y]. Regenerating..."
   - **FILE MISSING** → Auto-generate (see below)

### Claude Desktop (No Terminal)

If `pwd` is unavailable (Claude Desktop environment):

1. Check if user already specified a project in their message
2. If not, ASK: "Which project are you working on today?"
3. Use the projects list at `reference/projects-list.md` if available
4. Load: `/Users/tmkipper/Desktop/tk_projects/{project-name}/.claude/PROJECT_CONTEXT.md`

**To switch projects**: User says "switch to [project-name]" or "working on [project]"

---

## On Session Start

After project detection:

### 1. Load Context File
```
<project-root>/.claude/PROJECT_CONTEXT.md
```

### 2. Verify Against Git State
```bash
git status            # Current branch, modified files
git log --oneline -5  # Recent commits
```

Flag discrepancies:
- TODO marked done in commits? → Move to "Done"
- Branch changed? → Update context header
- Stale info? → Remove it

### 3. Display to User
Show a brief summary:
```
📍 Project: [name]
🌿 Branch: [branch]
📅 Last updated: [date]

Focus items: [count]
```

---

## On Session End

Triggers: "done", "end session", "save context", "done for today"

1. Review conversation for completed work
2. Update PROJECT_CONTEXT.md:
   - Move completed TODOs to "Done (This Session)"
   - Update Status based on commits made
   - Preserve untouched Focus items
   - **Clear previous session's Done list** (prevents accumulation)
   - Update timestamp
3. Show user the updated context

---

## Auto-Generate Context

When no PROJECT_CONTEXT.md exists, create from:

1. `.claude/CLAUDE.md` or `CLAUDE.md` (project docs)
2. `git log --oneline -5` (recent activity)
3. `git status` (current state)
4. `package.json` / `pyproject.toml` / `requirements.txt` (tech stack)

Write to: `<project-root>/.claude/PROJECT_CONTEXT.md`

---

## Context File Format

See `reference/template.md` for full template.

```markdown
# <project-name>

**Branch**: <branch> | **Updated**: <YYYY-MM-DD>

## Status
<2-3 sentences: current state>

## Today's Focus
1. [ ] <task>
2. [ ] <task>

## Done (This Session)
- <populated on session end, cleared on next session start>

## Blockers
<none or list>

## Tech Stack
<single line: Python 3.11 | FastAPI | PostgreSQL>
```

---

## Key Rules

1. **ALWAYS detect project first** - Never assume from previous session
2. **One project = one context file** - No cross-contamination
3. **Verify context matches pwd** - Warn on mismatch
4. **Clear Done list each session** - Prevents infinite accumulation
5. **Never store data in this SKILL.md** - Always use project's own file

---

## Reference Files

- `reference/template.md` - Full context file template with examples
- `reference/projects-list.md` - Tim's projects list for Claude Desktop
