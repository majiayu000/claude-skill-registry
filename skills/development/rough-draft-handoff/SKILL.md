---
name: rough-draft-handoff
description: Phase 4 - Hand off to executing-plans with the dependency graph
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - mcp__plugin_mermaid-collab_mermaid__*
---

# Phase 4: Implementation Handoff

Hand off to executing-plans with the dependency graph.

## Process

**Step 1: Generate implementation plan**

Convert the task dependency graph into an executable plan:

```markdown
# Implementation Plan

## Task Dependency Graph

[Include the YAML from skeleton phase]

## Execution Order

### Parallel Batch 1 (no dependencies)
- auth-types

### Batch 2 (depends on batch 1)
- auth-service

### Batch 3 (depends on batch 2)
- auth-middleware
- auth-tests (can run parallel with middleware)
```

**Step 2: Confirm transition to executing-plans**

Show summary and ask for confirmation:

```
Rough-draft complete. Ready for implementation:
- [N] files created with stubs
- [N] tasks in dependency graph
- [N] parallel-safe tasks identified

Ready to move to executing-plans?
  1. Yes, in current directory
  2. Yes, in a new git worktree (recommended for larger features)
  3. No, I need to revise something
```

**Option 1 - Current directory:**

Update collab state and invoke executing-plans:
```
Tool: mcp__plugin_mermaid-collab_mermaid__update_session_state
Args: { "project": "<cwd>", "session": "<name>", "phase": "implementation" }
```
Note: `lastActivity` is automatically updated by the MCP tool.

Then invoke executing-plans skill.

**Option 2 - Git worktree:**

1. Get session name from collab state
2. Prompt for branch name:
   ```
   Creating worktree with branch: feature/<session-name>
   (Press enter to accept, or type a different branch name)
   ```
3. Announce: "I'm using the using-git-worktrees skill to set up an isolated workspace."
4. Invoke using-git-worktrees skill with the branch name
5. On success:
   - Update collab-state.json to add `worktreePath` field:
     ```json
     {
       "worktreePath": "<absolute-path-to-worktree>"
     }
     ```
   - Update collab state: `phase: "implementation"`
   - Invoke executing-plans skill (now in worktree context)
6. On failure:
   - Report error
   - Ask: "Continue in current directory instead?"
     ```
     1. Yes
     2. No
     ```
   - If **1 (Yes)**: fall back to Option 1 flow
   - If **2 (No)**: stay at rough-draft phase

**Option 3 - Revise:**

Ask what needs revision and return to appropriate phase.

**Step 3: Pre-Implementation Compaction**

Before transitioning to implementation:

Ask user: "Compact context before starting implementation?"

```
1. Yes
2. No
```

- If **1 (Yes)**: Invoke skill: collab-clear, wait for completion, then invoke executing-plans
- If **2 (No)**: Invoke executing-plans directly

**Step 4: Invoke executing-plans**

The executing-plans skill will:
1. Parse the task dependency graph
2. Dispatch parallel-safe tasks via mermaid-collab:subagent-driven-development:implementer-prompt
3. Execute sequential tasks in dependency order
4. Run verify-phase after each task completes

## Final Verification

After all tasks complete:

```bash
./hooks/verify-phase.sh implementation <collab-name>
```

**Checklist:**
- [ ] All tasks from dependency graph completed
- [ ] All TODOs resolved
- [ ] Tests pass
- [ ] Implementation matches design intent

## Completion

### Mark item as documented

Before completing, update the item status in session state:

```
Tool: mcp__plugin_mermaid-collab_mermaid__get_session_state
Args: { "project": "<cwd>", "session": "<session>" }
```

Update the item's status in workItems array:

```
Tool: mcp__plugin_mermaid-collab_mermaid__update_session_state
Args: {
  "project": "<cwd>",
  "session": "<session>",
  "workItems": [<updated array with item status changed to "documented">]
}
```

### Call complete_skill

```
Tool: mcp__plugin_mermaid-collab_mermaid__complete_skill
Args: { "project": "<cwd>", "session": "<session>", "skill": "rough-draft-handoff" }
```

**Handle response:**
- If `action == "clear"`: Invoke skill: collab-clear
- If `next_skill` is not null: Invoke that skill
- If `next_skill` is null: Workflow complete
