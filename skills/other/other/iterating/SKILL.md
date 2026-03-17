---
name: iterating
description: Multi-conversation methodology for iterative stateful work with context accumulation. Use when users request work that spans multiple sessions (research, debugging, refactoring, feature development), need to build on past progress, explicitly mention iterative work, work logs, project knowledge, or cross-conversation learning.
metadata:
  version: 1.1.0
---

# Iterating

Maintain context across multiple sessions by persisting state in Work Logs.

## Environment Detection

Detect environment and load appropriate reference:

```bash
if [ "$CLAUDE_CODE_REMOTE" = "true" ]; then
  # Claude Code on the Web (CCotw) - writes to GitHub
  # Read: references/ccotw-environment.md
elif [ -n "$CLAUDE_CODE_REMOTE" ]; then
  # Claude Code CLI - writes to local filesystem
  # Read: references/codecli-environment.md
elif [ -x "$(command -v osascript)" ] && [ -d "/Applications/Claude.app" ]; then
  # Claude Desktop - may write to disk OR output for download
  # Read: references/desktop-environment.md
else
  # Claude.ai (web/chat/native app) - outputs for download
  # Read: references/chat-environment.md
fi
```

See environment-specific reference for persistence and retrieval details.

## Critical: Checkpoint Pattern

**The iterating skill enforces a checkpoint-and-save pattern to prevent work loss:**

1. **Create/Update WorkLog** → Output for user → **STOP**
2. User saves WorkLog to project knowledge (survives conversation limits)
3. User says "continue" (same or new conversation)
4. **Make incremental progress** on ONE item → Update WorkLog → **STOP**
5. Repeat

**Why this matters:**
- Prevents token exhaustion mid-task
- Survives 5-hour conversation limits
- Allows user to review progress before continuing
- Creates natural save points
- Enables work across multiple conversations

**NEVER skip the STOP step** - going "full waterfall" defeats the entire purpose of iterating.

## WorkLog Format

```markdown
---
version: v1
status: in_progress
---

# [Project Name] Work Log

## v1 | YYYY-MM-DD HH:MM | Title

**Prev:** [previous context OR "Starting new work"]
**Now:** [current goal]

**Progress:** [X% complete OR milestone status]

**Files:**
- `path/to/file.ext` (Why this file matters)
  - L45-67: [What to examine/change here]
  - L123-145: [Another area, specific issue]

**Work:**
+: [additions with file:line]
~: [changes with file:line]
!: [fixes with file:line]

**Decisions:**
- [what]: [why] (vs [alternatives])

**Works:** [effective approaches]
**Fails:** [ineffective approaches, why]

**Blockers:** [None OR specific blocker with owner/ETA]

**Next:**
- [HIGH] [Critical action item]
- [MED] [Important but not urgent]
- [LOW] [Nice to have]

**Open:** [questions needing answers]
```

## Core Workflow

**Starting new work:**
1. Detect environment
2. Create WorkLog v1 with task objective, decisions, file references, next steps
3. Persist using environment-specific method
4. **STOP - Present WorkLog to user**
   - Explain what's planned
   - Tell user to save WorkLog to project knowledge
   - Wait for user to say "continue" before doing ANY work

**Continuing work:**
1. Detect environment
2. Retrieve WorkLog using environment-specific method OR recognize pasted WorkLog
3. Parse latest version and status
4. Acknowledge: "From WorkLog vN, status: [status]. Progress: [X%]. Working on: [specific HIGH item]"
5. **Execute ONE HIGH priority item** (not all of them!)
6. Update WorkLog, increment version
7. Persist using environment-specific method
8. **STOP - Present updated WorkLog to user**
   - Summarize what was completed
   - Tell user to save updated WorkLog
   - Wait for user to say "continue" before next item

**Recognizing pasted WorkLog:**
If user pastes content with WorkLog frontmatter at conversation start:
1. Parse version and status from YAML
2. Acknowledge: "From WorkLog vN, status: [status]. Task: [objective]. Next: [HIGH item]"
3. Continue workflow from step 5 above

## Version Management

- Simple incremental: v1 → v2 → v3
- Frontmatter: `version: vN` (required)
- Filename: `WorkLog vN.md` (optional)
- Multiple files: Use highest version number

## Status States

- **in_progress**: Active work continuing
- **blocked**: Waiting on external dependency/decision
- **needs_review**: Ready for human inspection
- **completed**: Task finished

## Priority System

**Next steps must be prioritized:**
- **[HIGH]**: Critical items blocking other work
- **[MED]**: Important but not urgent
- **[LOW]**: Nice-to-have improvements

**Claude works on ONE HIGH priority item per iteration** unless told otherwise.

**Incremental progress pattern:**
- Pick ONE HIGH item from WorkLog
- Complete that specific item
- Update WorkLog with progress
- STOP for user to save
- User says "continue" → Pick next HIGH item
- Repeat

This prevents token exhaustion and enables natural checkpoints.

## File References

Use relative paths from project root with line ranges:

```markdown
**Files:**
- `src/auth/oauth.ts` (OAuth implementation needs refactoring)
  - L45-67: Current token validation logic
  - L123-145: Refresh token handling (race condition on L134)
```

**Critical:** Use relative paths, NOT absolute `/home/claude/` paths (fresh compute each session).

## Progress Tracking

**Always include progress indicators** (token/quota constraints may prevent completing full plan):

```markdown
**Progress:** 60% complete
```

Or for longer projects:

```markdown
**Progress:** Phase 2/3 | Auth ✅ | Payments 50% 🔄 | UI ⏳
```

## What to Document

**Include:**
- Key decisions with rationale and alternatives
- Effective and ineffective approaches
- Important discoveries
- File references with line ranges
- Next steps with priorities
- Progress indicators
- Blockers with owner/ETA

**Don't include:**
- Minor code changes (use git)
- Obvious information
- Raw data dumps
- Implementation details (use code comments)

## User Communication

**After creating WorkLog:**
- "Created WorkLog v1. Please save this to project knowledge."
- "Ready to start when you say 'continue'."

**After completing an item:**
- "Completed [item]. Updated WorkLog to vN."
- "Please save updated WorkLog to project knowledge."
- "Ready for next item when you say 'continue'."

**When continuing:**
- "From WorkLog vN, status: [status]. Progress: [X%]."
- "Working on: [specific HIGH item]"

**Status changes:**
- "Updated WorkLog status to [new_status]: [reason]"
- "Please save updated WorkLog."

**NEVER say:** "Now I'll continue with the next item..." - Always STOP and wait for user.

## Advanced Patterns

Read [references/advanced-patterns.md](references/advanced-patterns.md) when:
- Working on projects spanning 5+ sessions
- User mentions "debugging strategy", "hypothesis tracking", or "decision evolution"
- Managing multiple concurrent workstreams
- User asks about long-running project patterns
- Blocked on complex issues requiring systematic approach

Otherwise skip - basic workflow above is sufficient for most cases.

## Reference Documentation

- **[references/chat-environment.md](references/chat-environment.md)** - Claude.ai (web/chat/native app)
- **[references/desktop-environment.md](references/desktop-environment.md)** - Claude Desktop
- **[references/codecli-environment.md](references/codecli-environment.md)** - Claude Code CLI
- **[references/ccotw-environment.md](references/ccotw-environment.md)** - Claude Code on the Web
