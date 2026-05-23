---
name: rough-draft
description: Bridge brainstorming to implementation through 4 phases - interface, pseudocode, skeleton, and implementation handoff
user-invocable: false
model: opus
allowed-tools: mcp__plugin_mermaid-collab_mermaid__*, Read, Glob, Grep
---

## Collab Session Required

Before proceeding, check for active collab session:

1. Check if `.collab/` directory exists
2. Check if any session folders exist within
3. If no session found:
   ```
   No active collab session found.

   Use /collab to start a session first.
   ```
   **STOP** - do not proceed with this skill.

4. If multiple sessions exist, check `COLLAB_SESSION_PATH` env var or ask user which session.

# Rough-Draft: From Design to Implementation

## RESTRICTIONS

**FORBIDDEN during rough-draft phase:**
- Edit tool on source files (only allowed in `.collab/` folder)
- Write tool on source files (only allowed in `.collab/` folder)
- Any file modification outside `.collab/` folder
- Implementing code directly (must go through executing-plans)

**ALLOWED during rough-draft:**
- MCP collab tools - **prefer patch operations** for efficiency:
  - `patch_document` for targeted edits (status changes, adding fields)
  - `patch_diagram` for small diagram updates
  - `update_document`/`update_diagram` only for large rewrites or new sections
  - `create_diagram`, `create_document` for new artifacts
- Read tool (for exploration and context)
- Bash tool (for non-destructive commands like `ls`, `git status`)

**Why this matters:**
- Editing source files during rough-draft bypasses executing-plans
- This skips TDD, spec compliance, and code review gates
- All implementation MUST go through executing-plans with subagent dispatch

**RED FLAG:** If you're about to use Edit or Write on a source file, STOP. You're in the wrong phase. Document changes in the design doc and wait for executing-plans.

---

## Overview

The rough-draft skill bridges the gap between brainstorming (design) and implementation. It progressively refines the design through 4 phases, with verification gates at each transition to catch drift early.

```
+--------------+     +--------------+     +--------------+     +--------------+
|  Interface   |---->|  Pseudocode  |---->|   Skeleton   |---->|  Implement   |
+------+-------+     +------+-------+     +------+-------+     +------+-------+
       |                    |                    |                    |
       v                    v                    v                    v
  +--------+           +--------+           +--------+           +--------+
  | Verify |           | Verify |           | Verify |           | Verify |
  +--------+           +--------+           +--------+           +--------+
```

**Announce at start:** "I'm using the rough-draft skill to refine the design through interface, pseudocode, skeleton, and implementation handoff."

## Auto-Accept Prompt (At Start)

When first invoking rough-draft, ask user for approval workflow preference:

**Render UI Dropdown:**
```
Tool: mcp__plugin_mermaid-collab_mermaid__render_ui
Args: {
  "project": "<absolute-path-to-cwd>",
  "session": "<session-name>",
  "ui": {
    "type": "Card",
    "props": { "title": "Rough-Draft Workflow Preference" },
    "children": [{
      "type": "Markdown",
      "props": { "content": "How should I handle [PROPOSED] artifact reviews during rough-draft phases?" }
    }],
    "children": [{
      "type": "RadioGroup",
      "props": {
        "name": "autoAccept",
        "options": [
          { "value": "yes", "label": "Yes - Skip approval prompts" },
          { "value": "no", "label": "No - Review each phase" }
        ]
      }
    }]
  },
  "blocking": true
}
```

**Store preference in session state:**
```
Tool: mcp__plugin_mermaid-collab_mermaid__update_session_state
Args: {
  "project": "<absolute-path-to-cwd>",
  "session": "<session-name>",
  "metadata": { "autoAcceptRoughDraft": true/false }
}
```

**Use preference in phases:**
- If `autoAcceptRoughDraft: true` - Automatically proceed with [PROPOSED] artifacts without approval prompts
- If `autoAcceptRoughDraft: false` - Always ask for approval before removing [PROPOSED] markers

This preference applies to all Interface, Pseudocode, and Skeleton phase artifacts.

## Prerequisites

Before starting rough-draft, ensure:
- Design doc exists at `.collab/<name>/documents/design.md`
- Design doc passed brainstorming's completeness gate
- `collab-state.json` phase is set to `rough-draft/interface`

## Writing Quality

When writing interfaces and pseudocode, use clear, precise language.

**If `obra/the-elements-of-style` plugin is available**, invoke it for guidance on:
- Omitting needless words
- Using active voice
- Being specific, not vague

Apply these principles to interface documentation and pseudocode comments.

---

## Phase 1: Interface

Define the structural contracts of the system - file paths, class/function signatures, public API contracts, and type definitions.

**Invoke skill: rough-draft-interface** for detailed instructions.

---

### Compaction Checkpoint: Interface → Pseudocode

After Interface phase completes and is approved:

Check your current context usage and ask user: "Context is [X]% full. Ready to compact before Pseudocode phase?"

```
1. Yes - compact now
2. No - continue without compaction
```

- If **1 (Yes)**: Invoke skill: collab-compact, then continue to Pseudocode
- If **2 (No)**: Continue to Pseudocode without compaction

---

## Phase 2: Pseudocode

Define the logic flow for each function - step-by-step descriptions, error handling, edge cases, and dependencies.

**Invoke skill: rough-draft-pseudocode** for detailed instructions.

---

### Compaction Checkpoint: Pseudocode → Skeleton

After Pseudocode phase completes and is approved:

Check your current context usage and ask user: "Context is [X]% full. Ready to compact before Skeleton phase?"

```
1. Yes - compact now
2. No - continue without compaction
```

- If **1 (Yes)**: Invoke skill: collab-compact, then continue to Skeleton
- If **2 (No)**: Continue to Skeleton without compaction

---

## Phase 3: Skeleton

Generate stub file documentation and task dependency graphs. Files are documented but NOT created - they are created during implementation by executing-plans.

**Invoke skill: rough-draft-skeleton** for detailed instructions.

---

### Compaction Checkpoint: Skeleton → Implementation

After Skeleton phase completes and is approved:

Check your current context usage and ask user: "Context is [X]% full. Ready to compact before Implementation?"

```
1. Yes - compact now
2. No - continue without compaction
```

- If **1 (Yes)**: Invoke skill: collab-compact, then continue to Implementation Handoff
- If **2 (No)**: Continue to Implementation Handoff without compaction

---

## Proposed Tag Workflow

For each phase (INTERFACE, PSEUDOCODE, SKELETON), use the proposed tag workflow before verification:

1. Write artifact to design doc with `[PROPOSED]` marker
2. Tell user: "I've added the [interface/pseudocode/skeleton] to the design doc. Please review."
3. Ask: "Does this look right?"
   ```
   1. Yes
   2. No
   ```
4. If **1 (Yes)**: remove `[PROPOSED]` marker, proceed to drift check
5. If **2 (No)**: discuss, revise, repeat

This ensures user reviews each artifact before it becomes part of the design.

---

## Drift Detection

After each phase's `[PROPOSED]` content is accepted, check if it matches the original design.

### When to Check for Drift

Run drift detection after each phase's artifact is accepted:
- After INTERFACE accepted - compare to original design
- After PSEUDOCODE accepted - compare to design + interface
- After SKELETON accepted - compare to design + interface + pseudocode

### Presenting Drift

When drift is detected, present it clearly:

```
**Drift detected:** [What changed]

**Original design:** [What the design doc specified]
**Current artifact:** [What was just produced]

**Pros:**
- [Benefit 1]
- [Benefit 2]

**Cons:**
- [Drawback 1]
- [Drawback 2]

**Recommendation:** [Keep/Discard] - [Reasoning]

Keep this change?

1. Yes
2. No
```

### If User Keeps Change (1)

1. Design doc is already updated (via accepted proposal)
2. Assess significance:
   - **Minor:** Affects one component, no architectural change
   - **Significant:** Affects multiple components or changes architecture
3. Present: "This is [minor/significant] because [reasons]. I recommend [continuing/returning to brainstorming]."
4. Ask: "Go back to brainstorming?"
   ```
   1. Yes
   2. No
   ```
5. If **1 (Yes)** - transition to brainstorming skill
6. If **2 (No)** - continue to next rough-draft phase

### If User Discards Change (2)

1. Revert the design doc to before the proposal
2. Recommend restart point:
   - **Beginning (INTERFACE):** If drift affects foundational decisions
   - **Current phase:** If drift is isolated to this phase
3. Present: "I recommend restarting from [beginning/current phase] because [reasons]."
4. Ask: "Restart from?"
   ```
   1. Beginning (INTERFACE)
   2. Current phase
   ```
5. Execute the restart

---

## Phase 4: Implementation Handoff

Hand off to executing-plans with the dependency graph. Includes options for current directory or git worktree isolation.

**Invoke skill: rough-draft-handoff** for detailed instructions.

---

## Verification Gate Details

### When to Verify

Run verification BEFORE each phase transition:
- Interface -> Pseudocode
- Pseudocode -> Skeleton
- Skeleton -> Implementation
- Implementation -> Complete

### How Verification Works

The `verify-phase.sh` hook:
1. Reads the design document
2. Compares current artifacts to the design
3. Identifies alignment and drift
4. Generates pros/cons for each drift
5. Presents a report to the user

### Handling Verification Results

**If drift detected:**

The hook outputs a report with aligned items, drift detected items with pros/cons, and options to accept all, reject all, or review each.

### User Decisions

**1 - Accept all:**
- Design doc is updated to include the drift
- Decision logged with rationale
- Proceed to next phase

**2 - Reject all:**
- Design doc unchanged
- All drifts added to `pendingVerificationIssues`
- Stay in current phase, fix code

**3 - Review each:**
- Go through each drift one by one
- Accept/reject individually
- Mixed results: some accepted (update design), some rejected (add to pending)

### Decision Log

Accepted drifts are logged in the design doc:

```markdown
## Decision Log

### 2025-01-18: Added refreshToken method
- **Phase:** rough-draft:interface
- **Original:** Not specified
- **Changed to:** Added `refreshToken(token: string): Promise<string>`
- **Reason:** Enables session extension, security best practice
```

---

## State Tracking

### collab-state.json Updates

Track the current phase:

```json
{
  "phase": "rough-draft/interface",
  "template": "feature",
  "lastActivity": "2025-01-18T10:30:00Z",
  "pendingVerificationIssues": [],
  "serverPid": 12345,
  "serverPort": 3737
}
```

**Phase values for rough-draft:**
- `rough-draft/interface`
- `rough-draft/pseudocode`
- `rough-draft/skeleton`
- `implementation`

### Pending Verification Issues

When drifts are rejected:

```json
{
  "pendingVerificationIssues": [
    {
      "type": "drift",
      "phase": "interface",
      "description": "Added refreshToken method not in design",
      "file": "src/auth/service.ts",
      "detectedAt": "2025-01-18T11:00:00Z"
    }
  ]
}
```

Issues must be resolved before phase transition.

---

## Snapshot Saving

Save context snapshots to enable recovery after compaction.

### When to Save

Call `saveSnapshot()` after:
- User accepts proposed interface/pseudocode/skeleton
- Before transitioning to next phase
- Before invoking executing-plans

### Save Function

```
FUNCTION saveSnapshot():
  session = current session name

  # Read current state via MCP
  Tool: mcp__plugin_mermaid-collab_mermaid__get_session_state
  Args: { "project": "<cwd>", "session": session }
  Returns: state = { "phase": "...", ... }

  # Save snapshot via MCP
  Tool: mcp__plugin_mermaid-collab_mermaid__save_snapshot
  Args: {
    "project": "<cwd>",
    "session": session,
    "activeSkill": "rough-draft",
    "currentStep": state.phase (e.g., "rough-draft/interface"),
    "inProgressItem": null,
    "pendingQuestion": null,
    "recentContext": []
  }
  # Note: version and timestamp are automatically added

  # Update state to mark snapshot exists
  Tool: mcp__plugin_mermaid-collab_mermaid__update_session_state
  Args: { "project": "<cwd>", "session": session, "hasSnapshot": true }
```

### Save Points

**After user accepts proposal:**
```
[User accepts interface/pseudocode/skeleton]
-> Remove [PROPOSED] marker
-> saveSnapshot()
-> Run drift check
-> Continue to next phase
```

**At phase transitions:**
```
[Phase complete (interface -> pseudocode -> skeleton)]
-> Update collab-state.json phase via MCP
-> saveSnapshot()
-> Continue to next phase
```

**Before invoking executing-plans:**
```
[Skeleton complete, user confirms implementation]
-> saveSnapshot()
-> Invoke executing-plans skill
```

---

## Task Dependency Graph Format

### YAML Structure

```yaml
tasks:
  - id: <unique-identifier>
    files: [<file-path>, ...]
    description: <what this task implements>
    parallel: true  # Optional: can run with other parallel tasks
    depends-on: [<task-id>, ...]  # Optional: must complete first
```

### Rules

1. **IDs are unique** - No duplicate task IDs
2. **Files are explicit** - Full paths from project root
3. **Dependencies are task IDs** - Not file paths
4. **Parallel means independent** - No shared state, no order requirement
5. **No circular dependencies** - Graph must be acyclic

---

## Context Full Detection

During any rough-draft phase, if context usage approaches capacity, render a non-blocking Alert to notify the user:

**Tool call:**
```
Tool: mcp__plugin_mermaid-collab_mermaid__render_ui
Args: {
  "project": "<absolute-path-to-cwd>",
  "session": "<session-name>",
  "ui": {
    "type": "Alert",
    "props": {
      "type": "warning",
      "title": "Context Full",
      "message": "Run /compact in terminal, then /collab to resume."
    }
  },
  "blocking": false
}
```

This provides early warning before compaction becomes critical.

## Browser-Based Questions

When a collab session is active, prefer `render_ui` for user interactions instead of terminal prompts. Use `mcp__plugin_mermaid-collab_mermaid__render_ui` with Card components containing MultipleChoice or action buttons.

---

## Integration

### Called By

- **brainstorming** skill - After completeness gate passes
- **collab** skill - When resuming at rough-draft phase

### Transitions To

- **executing-plans** skill - With task dependency graph for implementation

### Collab Workflow Context

When invoked from collab workflow:
- `.collab/<name>/` folder exists
- `collab-state.json` tracks phase
- Mermaid-collab server running on assigned port
- Design doc at `.collab/<name>/documents/design.md`

### Context Preservation

If context is lost (compaction), re-read state:

```
# Get current session state
Tool: mcp__plugin_mermaid-collab_mermaid__get_session_state
Args: { "project": "<cwd>", "session": "<name>" }

# Read design doc
Tool: Read
Args: { "file_path": ".collab/<name>/documents/design.md" }

# Determine where to resume based on phase from state
```

---

## Quick Reference

| Phase | Input | Output | Verification Focus |
|-------|-------|--------|-------------------|
| Interface | Design doc | File paths, signatures, types | Completeness, no `any` types |
| Pseudocode | Interface section | Logic flow, error handling | Every function covered |
| Skeleton | Pseudocode section | Stub files, dependency graph | Files created, TODOs match |
| Implementation | Dependency graph | Completed code | Tests pass, design match |

## Common Mistakes

### Skipping verification gates
- **Problem:** Drift accumulates, implementation diverges from design
- **Fix:** Always run `verify-phase.sh` before phase transitions

### Vague pseudocode
- **Problem:** Implementation guesses at details, introduces drift
- **Fix:** Pseudocode should be detailed enough to implement mechanically

### Missing dependencies in graph
- **Problem:** Tasks fail because prerequisites not met
- **Fix:** Trace all imports and analyze what must exist first

### Not updating collab-state.json
- **Problem:** Resume doesn't know current phase
- **Fix:** Use `mcp__plugin_mermaid-collab_mermaid__update_session_state` after each transition (automatically updates lastActivity)

## Red Flags

**Never:**
- Skip a phase (each builds on the previous)
- Proceed with pending verification issues
- Modify design doc without going through verification
- Create files not in the Interface phase
- Add functionality not in the Pseudocode phase

**Always:**
- Run verification before phase transition
- Handle drift explicitly (accept/reject)
- Update collab-state.json with current phase
- Keep design doc synchronized with decisions
- Use mermaid-collab for visualizing dependency graphs
