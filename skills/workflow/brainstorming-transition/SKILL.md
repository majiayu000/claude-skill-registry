---
name: brainstorming-transition
description: Transition from brainstorming to rough-draft skill
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - mcp__plugin_mermaid-collab_mermaid__*
---

# Transition to Rough-Draft

After the VALIDATING phase passes, transition to the rough-draft skill.

## Pre-Transition Checklist

Before transitioning, verify:

- [ ] Completeness gate passed
- [ ] User confirmed "Yes" to proceed
- [ ] Design doc is saved and up-to-date
- [ ] All diagrams are finalized

## Transition Process

### 1. Update Collab State

```
Tool: mcp__plugin_mermaid-collab_mermaid__update_session_state
Args: { "project": "<cwd>", "session": "<name>", "phase": "rough-draft/interface" }
```

Note: `lastActivity` is automatically updated by the MCP tool.

### 2. Save Snapshot

Before invoking rough-draft, save context via MCP:

```
FUNCTION saveSnapshot(pendingQuestion):
  session = current session name

  # Read current state via MCP
  Tool: mcp__plugin_mermaid-collab_mermaid__get_session_state
  Args: { "project": "<cwd>", "session": session }
  Returns: state = { "phase": "...", "currentItem": ..., ... }

  # Save snapshot via MCP
  Tool: mcp__plugin_mermaid-collab_mermaid__save_snapshot
  Args: {
    "project": "<cwd>",
    "session": session,
    "activeSkill": "brainstorming",
    "currentStep": "VALIDATING",
    "pendingQuestion": null,
    "inProgressItem": state.currentItem,
    "recentContext": []
  }
  # Note: version and timestamp are automatically added

  # Update state to mark snapshot exists
  Tool: mcp__plugin_mermaid-collab_mermaid__update_session_state
  Args: { "project": "<cwd>", "session": session, "hasSnapshot": true }
```

### 3. Pre-Transition Compaction

Before transitioning to rough-draft:

Ask user: "Compact context before starting rough-draft?"

```
1. Yes
2. No
```

- If **1 (Yes)**: Invoke skill: collab-compact, wait for completion, then invoke rough-draft
- If **2 (No)**: Invoke rough-draft directly

### 4. Invoke Rough-Draft Skill

The rough-draft skill will:
1. Read the design doc
2. Create interface definitions
3. Write pseudocode
4. Build code skeleton
5. Hand off to implementation

## Standalone Mode (No Collab)

If brainstorming was used standalone (not within collab workflow):

**Option 1: Stay in collab**
- Design remains in `.collab/<name>/documents/design.md`
- Use `/collab-cleanup` to archive when session ends

**Option 2: Continue to implementation**
- Ask: "Ready to set up for implementation?"
- Use `superpowers:using-git-worktrees` to create isolated workspace
- Use `superpowers:writing-plans` to create detailed implementation plan

## Context Preservation

Design docs survive context compaction. When resuming:

**Re-read design doc to restore context:**

```bash
# Always re-read before continuing work
cat .collab/<name>/documents/design.md

# Also read any diagrams
ls .collab/<name>/diagrams/
```

**After re-reading:**
- Summarize current state briefly
- Identify where brainstorming left off
- Continue from that point

## Snapshot Saving

Save context snapshots to enable recovery after compaction.

### When to Save

Call `saveSnapshot()` after:
- User answers a question
- Phase transition (EXPLORING -> CLARIFYING -> DESIGNING -> VALIDATING)
- Before invoking another skill

### Save Points

**After user answers:**
```
[User provides answer]
-> Update design doc with answer
-> saveSnapshot(next-pending-question-or-null)
-> Continue conversation
```

**At phase transitions:**
```
[Phase complete, transitioning to next]
-> Update collab-state.json phase
-> saveSnapshot(null)
-> Continue to next phase
```

**Before invoking another skill:**
```
[About to invoke rough-draft]
-> saveSnapshot(null)
-> Invoke skill
```

## Integration Points

**Called by:**
- **collab** skill - When starting new collab or resuming at brainstorming phase
- User directly via `/brainstorming` command for standalone design work

**Transitions to:**
- **rough-draft** skill - After completeness gate passes (within collab workflow)
- **writing-plans** skill - For standalone design work leading to implementation

**Collab workflow context:**
When invoked from collab skill, the following are already set up:
- `.collab/<name>/` folder exists
- `collab-state.json` tracks phase as `brainstorming`
- Mermaid-collab server running on assigned port
- Design doc location: `.collab/<name>/documents/design.md`

## State Updates

- On completion: Use `mcp__plugin_mermaid-collab_mermaid__update_session_state({ project, session, phase: "rough-draft/interface" })`
- The MCP tool automatically updates `lastActivity` timestamp
