---
name: beads-execute
description: Execute beads tasks with proper claim/work/close workflow and session management
---

# Beads Execution Skill

## Overview

This skill guides the execution of beads tasks after a dependency graph has been created via `beads-plan`. It covers:
- Finding and claiming ready work
- Executing tasks with proper state management
- Closing tasks and checking newly unblocked work
- Session management and handoff

## Prerequisites

- `bd` CLI installed and initialized in the project
- A beads plan exists (created via `/beads-plan`)
- Working directory is within the beads-initialized project

---

## Project Context and History

When you need to understand what previous agents did or review project history:

### Beads History

```bash
# View all beads in an epic (including closed)
bd list --parent <epic-id> --all

# View a specific bead's full history and notes
bd show <bead-id>

# See what beads were recently closed
bd list --status closed --parent <epic-id>

# Check git commits associated with beads (commits reference bead IDs)
git log --oneline --grep="<bead-id>"
```

### Harness Run Logs

Previous automated runs are logged in `.beads/harness-logs/`:

```bash
# List all run logs (most recent first)
ls -t .beads/harness-logs/*.log

# View the most recent run log
cat "$(ls -t .beads/harness-logs/*.log | head -1)"

# Search logs for errors or specific beads
grep -l "ERROR\|error" .beads/harness-logs/*.log
grep -l "<bead-id>" .beads/harness-logs/*.log
```

Run logs contain:
- Timestamps for each iteration
- Session IDs (for replaying in TUI)
- Epic status at completion
- Structured events (JSON format)

### Git History

Agents commit with bead IDs in the message format `feat(<bead-id>): <title>`:

```bash
# See commits for a specific bead
git log --oneline --grep="<bead-id>"

# See what changed in a bead's implementation
git log -p --grep="<bead-id>"

# See recent bead-related commits
git log --oneline --grep="^feat\|^fix\|^wip" -20
```

### OpenCode Sessions

If you need to review what an agent actually did (tool calls, reasoning):

```bash
# List recent sessions
opencode session list --format json | jq '.[:5]'

# Export a session for review
opencode export <session-id> > session-export.json
```

### Bead Notes

Agents document important context in bead notes:

```bash
# Find beads with notes
bd list --parent <epic-id> --json | jq '.[] | select(.notes != null) | {id, title, notes}'

# Common note prefixes to look for:
# - "Context limit." - Agent hit context exhaustion, notes contain resume point
# - "REVIEW NEEDED:" - Agent flagged uncertainty
# - "Blocked:" - Agent couldn't complete, explains why
```

---

## Session Start Protocol

At the start of an execution session:

```bash
# 1. Sync to get latest state from remote
bd sync

# 2. Show epic status
bd epic status <epic-id>

# 3. Show ready work
bd ready

# 4. Visualize the graph (optional)
bd graph <epic-id>
```

Present this information to the user and help them select which task to work on.

---

## Task Execution Workflow

### 1. Claim a Task

Before starting work, claim the task atomically:

```bash
bd update <task-id> --claim
```

This sets:
- `status` = `in_progress`
- `assignee` = current actor

**Important:** If claim fails, another agent already claimed it. Choose different task.

### 2. View Task Details

```bash
bd show <task-id>
```

Review:
- Description
- Acceptance criteria
- Dependencies (what this blocks)

### 3. Execute the Work

Implement the task according to its acceptance criteria.

**During execution:**
- Create branches per your git workflow
- Run tests where applicable
- Document any discovered work

### 4. File Discovered Work

If you discover additional work needed:

```bash
bd create "Discovered: <title>" -t task -p 2 --parent <epic-id> \
  -d "Found while working on <current-task>: <description>"
```

Add dependencies if the discovered work blocks or is blocked by other tasks:

```bash
bd dep add <new-task> <blocking-task>
```

### 5. Close the Task

When acceptance criteria are met:

```bash
bd close <task-id> -r "Completed: <brief summary>"
```

### 6. Check Newly Unblocked Work

```bash
bd ready
```

This shows tasks that became unblocked by your completion.

---

## Status Transitions

```
open -> in_progress    (via --claim)
in_progress -> closed  (via bd close)
closed -> open         (via bd reopen, if needed)
```

---

## Multi-Task Sessions

For longer sessions working on multiple tasks:

```bash
# After completing one task
bd close <task-1> -r "Completed"
bd ready                           # See what's unblocked
bd update <task-2> --claim         # Claim next task
# ... work on task 2 ...
bd close <task-2> -r "Completed"
bd sync                            # Sync periodically
```

**Rule:** One task `in_progress` at a time. Complete current before claiming next.

---

## Handling Blocked Work

If you need to work on something blocked:

1. Check what's blocking it:
   ```bash
   bd show <blocked-task>  # See "DEPENDS ON" section
   ```

2. Either:
   - Work on the blocker first
   - Re-evaluate if the dependency is correct
   - Remove spurious dependency: `bd dep remove <task> <blocker>`

---

## Key Commands Reference

| Action | Command |
|--------|---------|
| Find ready work | `bd ready` |
| Claim a task | `bd update <id> --claim` |
| View task details | `bd show <id>` |
| Close task | `bd close <id> -r "reason"` |
| See blocked work | `bd blocked` |
| Visualize graph | `bd graph <epic-id>` |
| Sync to git | `bd sync` |
| Epic progress | `bd epic status <id>` |
| Add dependency | `bd dep add <task> <blocker>` |
| Remove dependency | `bd dep remove <task> <blocker>` |
| Create new task | `bd create "Title" -t task -p <N> --parent <epic>` |

---

## Anti-Patterns to Avoid

1. **Working without claiming** - Always claim before starting work
2. **Multiple tasks in-progress** - Complete one before claiming another
3. **Forgetting to close** - Close immediately when acceptance criteria are met
4. **Batching closures** - Close each task as you finish, don't save them up
5. **Ignoring discovered work** - File issues for anything found during execution
6. **Skipping sync** - Sync before session end and periodically during long sessions

---

## Session End Protocol

When the user invokes `/beads-land`, follow the landing protocol:

1. **Check for in-progress tasks** - Close or document status
2. **File remaining work** - Create issues for anything discovered
3. **Sync and push** - MANDATORY before session ends
4. **Provide handoff** - Summary and next session prompt

See `/beads-land` command for the complete protocol.

---

## Loop Mode Protocol

When operating in loop mode (invoked via `/beads-loop`), you execute beads autonomously until completion or error.

### Loop Awareness

You are executing beads automatically. The loop continues until one of:
1. **Epic complete** - 100% of beads closed
2. **Unrecoverable error** - Something requires human intervention
3. **Context exhaustion** - Signal continuation and exit cleanly

**There is no human gate between beads.** The outer harness script handles continuation automatically.

### Selection Heuristics

When multiple beads are ready, prefer:
1. **Higher priority** (P0 > P1 > P2)
2. **Unblocking power** - Beads that unblock the most other beads
3. **Smaller scope** - Faster feedback loops
4. **Context locality** - Related to recently-completed work

In practice, `bd ready` returns beads sorted by priority. Select the first one:

```bash
bd ready --json | jq -r '.[0].id'
```

### Loop Algorithm

```
LOOP:
  1. CHECK COMPLETION
     bd epic status <epic-id> --json
     If 100% complete -> Celebrate, EXIT (no continuation signal)
     
  2. FIND READY WORK
     bd ready --json
     If empty AND blocked exist -> Diagnose deadlock, EXIT
     If empty AND nothing open -> All done, EXIT
     
  3. SELECT AND CLAIM
     task = first ready bead
     bd update <task-id> --claim
     If fails -> Another agent claimed it, GOTO 2
     
  4. EXECUTE
     bd show <task-id> --json
     Implement per acceptance criteria
     File discovered work with bd create
     
  5. VERIFY AND CLOSE
     Verify acceptance criteria met
     bd close <task-id> -r "Completed: <summary>"
     
  6. CHECKPOINT
     bd sync
     git add -A && git commit -m "feat(<task-id>): <title>"
     git push
     
  7. CONTEXT CHECK
     If context approaching limit -> GOTO Context Exhaustion Protocol
     Else -> GOTO 1
```

---

## Context Exhaustion Protocol

When you detect context is approaching limits (conversation getting long, many tool calls, complex state):

### Detection Heuristics

Context exhaustion is approaching when:
- Conversation has been running for extended period with many tool calls
- You're having difficulty tracking state or context
- OpenCode triggers auto-compaction

### Exit Protocol

1. **Complete current atomic operation** - Never stop mid-file-edit
2. **If bead in-progress**, add session notes:
   ```bash
   bd update <task-id> --notes "Context limit. Completed: <what you finished>. Next: <what remains>."
   ```
3. **Sync and push** (non-negotiable):
   ```bash
   bd sync
   git add -A && git commit -m "wip(<task-id>): context checkpoint" || true
   git push
   ```
4. **Write continuation signal**:
   ```bash
   echo "1" > .beads/continue
   ```
5. **Exit cleanly** with a brief status message

**CRITICAL:**
- Do NOT signal the user to re-invoke
- Do NOT wait for confirmation
- Do NOT ask if the user wants to continue
- The outer harness script handles all continuation automatically

---

## Continuation Protocol

When starting a session that may be a continuation (harness re-invoked you):

### On Session Start

1. **Check for in-progress tasks**:
   ```bash
   bd list --status in_progress --json
   ```

2. **If in-progress bead exists**, read its state:
   ```bash
   bd show <task-id> --json
   ```
   Look for notes field - it may contain "Context limit. Completed: X. Next: Y."

3. **Continue from where notes indicate**, or complete the bead if notes are unclear

4. **After completing the resumed bead**, proceed to normal loop (check completion, find ready work, etc.)

### Compaction Recovery

If your context was compacted (you see a summary message at conversation start):
- **Do NOT rely on the summary** for task state
- Immediately query beads: `bd list --status in_progress --json`
- The beads database is the **source of truth**, not conversation history
- Read bead notes for session context

---

## Error Recovery Patterns

### Claim Conflict

```bash
$ bd update bd-XXX --claim
Error: bead already claimed by agent-2
```

**Recovery:** Skip this bead, select next from `bd ready`.

### Test/Verification Failure

If acceptance criteria not met after implementation:

1. **If quickly fixable**: Fix it, verify again
2. **If complex issue**:
   ```bash
   bd update <task-id> --notes "Blocked: <issue description>. Needs: <what's required>"
   bd update <task-id> --status open  # Unclaim
   bd create "Fix: <issue>" -t bug -p 1 --parent <epic>
   bd dep add <task-id> <new-bug-id>  # Original blocked by fix
   bd sync
   ```
   Continue with other ready beads.

### Deadlock (No Ready Beads)

```bash
$ bd ready
(empty)
$ bd list --status open
bd-XXX  ...  (blocked)
bd-YYY  ...  (blocked)
```

**Diagnosis:**
```bash
bd blocked --json    # See what's blocked and why
bd dep cycles        # Check for cycles
```

**Recovery:**
- If cycle exists: Report cycle details, EXIT for human intervention
- If external blocker: Document and EXIT
- If all blocked on one bead: Attempt that bead or escalate

### Git Push Failure

```bash
$ git push
! [rejected] main -> main (fetch first)
```

**Recovery:**
```bash
git pull --rebase
# If conflict in .beads/issues.jsonl:
git checkout --theirs .beads/issues.jsonl
bd import -i .beads/issues.jsonl
bd sync
git push  # Retry
```

---

## Loop Mode Anti-Patterns

In addition to standard anti-patterns, in loop mode also avoid:

1. **Signaling user for continuation** - Harness handles this
2. **Asking for confirmation** - Loop is autonomous
3. **Stopping without sync/push** - Always checkpoint before exit
4. **Ignoring session notes** - Read them on continuation
5. **Trusting compacted context** - Query beads DB for ground truth

---

## Issue Reporting and Documentation

When you encounter problems that cannot be automatically resolved, document them properly for human review.

### Creating Blocking Issues

When a bead cannot be completed due to an issue:

```bash
# Create a blocking bug with full context
bd create "Bug: <concise title>" -t bug -p 1 --parent <epic-id> \
  -d "## Problem
<What went wrong>

## Context  
- Discovered while working on: <bead-id>
- Environment: <relevant details>

## Steps to Reproduce
1. <step>
2. <step>

## Expected vs Actual
- Expected: <what should happen>
- Actual: <what happens>

## Attempted Solutions
- <what you tried>
- <why it didn't work>

## Recommended Fix
<your analysis of what needs to happen>"

# Link the dependency
bd dep add <blocked-bead-id> <new-bug-id>
```

### Documenting Uncertainty

When you're unsure about an implementation decision:

```bash
bd update <bead-id> --notes "REVIEW NEEDED: <question or concern>. Made assumption: <what you assumed>. Alternative: <other option considered>."
```

### Flagging Technical Debt

When you implement a working but non-ideal solution:

```bash
bd create "Tech debt: <what needs improvement>" -t chore -p 3 --parent <epic-id> \
  -d "## Current State
<what exists now>

## Why It's Debt
<why this needs improvement>

## Suggested Improvement
<what should be done>

## Risk If Not Addressed
<consequences of leaving it>"
```

### Run Summary Annotation

At the end of a successful loop iteration, if there are observations worth noting:

```bash
bd update <epic-id> --notes "$(date -Iseconds) Loop completed. Observations: <notable findings, warnings, or recommendations>"
```

### What to Document

Always create beads for:
- Bugs discovered during implementation
- Missing requirements or ambiguities
- Technical debt introduced
- External blockers (APIs down, missing credentials, etc.)
- Security concerns
- Performance issues observed

Do NOT create beads for:
- Minor code style preferences
- Transient issues that self-resolved
- Questions that can be answered by reading docs

### Post-Run Review

After the harness completes, humans can review:

```bash
# View run log
cat .beads/harness-logs/run-*.log | tail -1

# See all bugs filed
bd list -t bug --parent <epic-id>

# Check for tasks with review notes
bd list --parent <epic-id> --json | jq '.[] | select(.notes != null)'

# View epic status
bd epic status <epic-id>
```

---

## Project Documentation Protocol

Documentation is part of the work, not an afterthought. Follow these guidelines for when and how to document.

### When to Create/Update Documentation

**Create documentation when:**

1. **A bead explicitly requires it** - The acceptance criteria mentions docs, README, etc.
2. **You create a new public API** - Functions, endpoints, or interfaces others will use
3. **You add a new command/script** - CLI tools need usage documentation
4. **You set up a new service/component** - How to run, configure, deploy
5. **You implement non-obvious behavior** - Complex algorithms, business logic, edge cases
6. **The project has no README** - Create a minimal one with setup instructions

**Update documentation when:**

1. **You change existing documented behavior** - Keep docs in sync with code
2. **You deprecate or remove features** - Note what changed and migration path
3. **You discover the docs are wrong** - Fix them immediately

**Do NOT create documentation for:**

1. **Self-documenting code** - Well-named functions don't need paragraph explanations
2. **Internal implementation details** - Unless specifically requested
3. **Speculative features** - Only document what exists
4. **Personal notes** - Use bead notes, not project docs

### Documentation Locations

Follow project conventions. Common patterns:

```
README.md              # Project overview, quick start, basic usage
docs/                  # Detailed documentation
  architecture.md      # System design, component relationships
  api.md               # API reference
  deployment.md        # How to deploy
  development.md       # How to contribute/develop
CHANGELOG.md           # Version history (if project uses one)
<component>/README.md  # Component-specific docs
```

### Documentation Standards

**README.md minimum viable content:**

```markdown
# Project Name

Brief description of what this does.

## Quick Start

\`\`\`bash
# How to install/setup
# How to run
\`\`\`

## Usage

Basic usage examples.

## Configuration

Key configuration options (if any).
```

**API/Function documentation:**

```markdown
## function_name

Brief description.

### Parameters

- `param1` (type): Description
- `param2` (type, optional): Description. Default: `value`

### Returns

Description of return value.

### Example

\`\`\`language
example code
\`\`\`

### Errors

- `ErrorType`: When this occurs
```

**When documenting commands/scripts:**

```markdown
## command-name

Description of what it does.

### Usage

\`\`\`bash
command-name [options] <required-arg>
\`\`\`

### Options

- `--flag`: Description
- `--option <value>`: Description (default: X)

### Examples

\`\`\`bash
# Common use case
command-name --flag value

# Another use case  
command-name --other-option
\`\`\`
```

### Documentation as Beads

If a feature requires documentation, it should be part of the bead's acceptance criteria:

```
Acceptance criteria:
- Feature X works as specified
- README updated with usage instructions
- API documented in docs/api.md
```

If you complete a bead and realize docs are needed but weren't specified:

```bash
bd create "Docs: Document <feature>" -t chore -p 3 --parent <epic-id> \
  -d "Add documentation for <feature> implemented in <bead-id>.

Needed:
- Usage examples
- Configuration options
- API reference"
```

### Inline Code Documentation

**Do document:**
- Public API contracts (function signatures, types)
- Complex algorithms (brief explanation of approach)
- Non-obvious side effects
- TODO/FIXME with bead references: `// TODO(bd-XXX): description`

**Don't over-document:**
- Obvious code (`i++ // increment i`)
- Every private function
- Implementation details that may change

### Documentation Commits

Documentation changes follow the same commit pattern:

```bash
git commit -m "docs(<bead-id>): <what was documented>"
```

Examples:
```bash
git commit -m "docs(bd-XXX): add API reference for auth endpoints"
git commit -m "docs(bd-YYY): update README with new CLI options"
```
