---
name: save-session
description: Save session state to Pieces LTM. Use when context is running low, before /compact, when ending a session, or handing off to a fresh Claude instance.
allowed-tools: Bash, mcp__pieces__create_pieces_memory, mcp__serena__write_memory, TodoWrite
---

# Save Session State

Guidance for saving session state before context compression or handoff.

## When Claude Should Use This Skill

- User mentions "save session", "running out of context", "before we lose context"
- User is about to run `/compact`
- User says they're ending the session or switching tasks
- Context usage is high and important work needs to be preserved

## Usage

```
/save-session                           # Save state
/save-session "check auth.ts line 145"  # Save with handoff message
```

## Execution Steps

### 1. Gather State

Run this to get current git and project state:

```bash
echo "PROJECT_PATH=$(pwd)"
echo "---"
git branch --show-current
git status --short
bd list --status=in_progress 2>/dev/null || echo "No in-progress issues"
```

### 2. Create Pieces Memory

Use `mcp__pieces__create_pieces_memory` with:

**summary_description:** Short title with keywords for retrieval
```
[project-name] session: [main topic] - [branch] - [YYYY-MM-DD]
```
Example: `dssk-multichannel-gui session: comment-form extraction - feat/kuendigungsdetails - 2026-01-12`

**summary:** Markdown-formatted narrative with searchable keywords:
```markdown
# Session Summary - {DATE}

## What Was Accomplished
- Completed task 1
- Implemented feature X
- Fixed bug Y

## Current State
- **Branch:** {branch name}
- **Uncommitted changes:** {summary of git status}
- **In-progress issues:** {bd list output}

## Handoff Message
{user's message if provided, otherwise omit}

## Next Steps
1. Continue with X
2. Need to finish Y
3. Review Z

## Key Decisions Made
- Decision 1: rationale
- Decision 2: rationale

## Important Context for Continuation
Any context the next session needs to understand the work.
File paths, architectural decisions, blockers encountered.
```

**project:** Absolute path to project root (from step 1)

**files:** List of key files modified this session (absolute paths)

**connected_client:** `"Claude"`

### 3. Sync Beads

```bash
bd sync
```

### 4. Provide Continuation Instructions

Always end with:

```
**Session saved to Pieces.** To continue in a new session:
1. Start fresh Claude Code session
2. Run `bd ready` to see available work
3. Use `ask_pieces_ltm` to retrieve session context
```

## Serena Memory Updates

If significant code understanding was gained, consider updating:
- `project_overview` - architecture changes
- `coding_standards` - new patterns established
- `types-reference` - new types documented

## Retrieval Best Practices

Pieces indexes content semantically. To improve retrieval:

### In summary_description (acts as title/tag):
- Start with project name: `dssk-multichannel-gui session:`
- Include main topic: `form validation`, `component extraction`
- Add branch name for filtering: `feat/kuendigungsdetails`
- End with date: `2026-01-12`

### In summary content:
- Use consistent section headers (What Was Accomplished, Next Steps, etc.)
- Include technology keywords: `Angular`, `signals`, `reactive forms`
- Mention specific components/files by name
- Add a `## Keywords` section at the end:
  ```markdown
  ## Keywords
  Angular, component extraction, comment-form, kuendigungsdetails, refactoring, Serena, model injection
  ```

### File paths matter:
- Pieces links memories to files - include all modified files
- Use absolute paths for accurate linking
- This enables "what did I do in this file?" queries

### Retrieval queries:
```
ask_pieces_ltm: "What was I working on in dssk-multichannel-gui last week?"
ask_pieces_ltm: "Show me sessions about form validation"
ask_pieces_ltm: "What decisions were made about component extraction?"
```

## Why Pieces Over Basic Memory

- **Cross-tool:** Accessible from Cursor, Windsurf, other AI tools
- **Searchable:** `ask_pieces_ltm` can find context by topic
- **Persistent:** Survives session restarts and tool switches
- **Indexed:** Automatically linked to files and project
