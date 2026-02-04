---
name: Filesystem Context Manager
description: Maintain context across Claude Code sessions using filesystem persistence. Prevents context loss, enables plan continuity, and supports multi-session workflows.
version: 1.0.0
dependencies: none
---

# Filesystem Context Manager

A skill for maintaining context across Claude Code sessions using filesystem-based persistence. Implements the six patterns from Context Engineering to prevent context loss during long or multi-session tasks.

## When This Skill Activates

This skill automatically activates when you:
- Start a new session and need to resume previous work
- Work on tasks spanning multiple conversations
- Need to preserve decisions, context, or learnings
- Want to maintain continuity across sessions
- Are working on complex multi-step implementations

**Keywords**: save context, resume work, continue session, persist context, remember this, don't forget, maintain context, session continuity, pick up where we left off

## Core Concepts

### The Context Problem

| Issue | Impact | Solution |
|-------|--------|----------|
| Context window fills up | Early context forgotten | Write to files, read selectively |
| Session ends mid-task | Progress lost | Persist plans and state |
| Complex decisions made | Reasoning forgotten | Document decisions in files |
| Patterns discovered | Must re-learn each session | Store in memory files |

### File-Based Context Hierarchy

```
.claude/
├── context/              # Current session state
│   ├── current-task.md   # Active task description
│   ├── decisions.md      # Decisions made this session
│   └── blockers.md       # Current blockers
├── memory/               # Persistent learnings (survives sessions)
│   ├── patterns.md       # Codebase patterns discovered
│   ├── gotchas.md        # Things to remember
│   └── preferences.md    # User preferences
├── scratch/              # Temporary working files
│   └── tool-outputs/     # Large command outputs
├── plans/                # Implementation plans
│   └── *.md              # Individual plan files
└── skills/               # Skill definitions
```

## Pattern 1: Scratch Pad for Large Outputs

When tool outputs exceed ~2000 tokens, write to file instead of keeping in context.

### Implementation

```bash
# Instead of showing full output in chat
npm run build 2>&1 | tee .claude/scratch/build-output.txt

# Then reference specific parts
grep -n "error" .claude/scratch/build-output.txt
```

### When to Use
- Build outputs with many warnings
- Large database query results
- Extensive grep/search results
- API responses with large payloads

### Example Workflow

```markdown
1. Run command, pipe to scratch file
2. Return summary to chat: "Build completed with 3 errors, see .claude/scratch/build-output.txt"
3. When debugging, grep specific errors from file
4. Delete scratch file when done
```

## Pattern 2: Plan Persistence

Store implementation plans in structured files for continuity.

### Plan File Template

```markdown
# Plan: [Feature/Task Name]

## Metadata
- **Status**: PLANNING | IN_PROGRESS | BLOCKED | COMPLETE
- **Created**: YYYY-MM-DD
- **Updated**: YYYY-MM-DD HH:MM
- **Priority**: HIGH | MEDIUM | LOW

## Objective
[Clear statement of what we're trying to achieve]

## Context
[Background information and why this matters]

## Implementation Steps
- [ ] Step 1: Description
  - Files: `path/to/file.ts`
  - Notes: Implementation details
- [ ] Step 2: Description
- [ ] Step 3: Description

## Files to Modify
| File | Purpose | Status |
|------|---------|--------|
| `app/api/route.ts` | Main endpoint | Pending |
| `lib/service.ts` | Business logic | Done |

## Decisions Made
1. **[Decision]**: [Rationale]
2. **[Decision]**: [Rationale]

## Blockers
- [ ] Blocker 1: Description
- [ ] Blocker 2: Description

## Notes
[Any additional context]
```

### Usage

```bash
# Create new plan
echo "# Plan: Feature X" > .claude/plans/feature-x.md

# Resume work - read plan first
cat .claude/plans/feature-x.md

# Update progress
# Edit the plan file as steps complete
```

## Pattern 3: Session Context Persistence

Maintain current session state for continuity.

### Current Task File

```markdown
# Current Task

## What I'm Working On
[Brief description of current focus]

## Recent Actions
- [Action 1] - [Result]
- [Action 2] - [Result]

## Next Steps
1. [Next immediate action]
2. [Following action]

## Files Currently Open/Relevant
- `path/to/file1.ts` - [Why relevant]
- `path/to/file2.ts` - [Why relevant]

## Session Notes
[Any important context for this session]
```

### Decisions File

```markdown
# Session Decisions

## [Date]

### Decision: [Title]
- **Context**: [Why this came up]
- **Options Considered**:
  - Option A: [Description]
  - Option B: [Description]
- **Chosen**: Option A
- **Rationale**: [Why this was chosen]
- **Impact**: [What this affects]
```

## Pattern 4: Memory Persistence

Store learnings that should survive across all sessions.

### Patterns File

```markdown
# Codebase Patterns

## Authentication
- Always use `createClient` from `@/lib/supabase/server` for API routes
- Check BOTH Authorization header AND cookies (see commit ac642e8)

## API Routes
- Next.js 15 requires async params: `context: { params: Promise<{ id: string }> }`
- Always await params before use

## Database
- Use service role client for admin operations
- RLS policies apply to anon key only

## Testing
- Run `npm run type-check:memory` to avoid heap errors
- Use `npm run dev:memory` for development server
```

### Gotchas File

```markdown
# Gotchas & Lessons Learned

## [Category]

### [Issue Title]
- **Symptom**: [What you see]
- **Cause**: [Why it happens]
- **Fix**: [How to resolve]
- **Prevention**: [How to avoid]
- **Reference**: [Commit/PR/Doc]
```

### Preferences File

```markdown
# User Preferences

## Code Style
- Prefer explicit types over inference
- Use early returns for guard clauses
- Keep functions under 50 lines

## Workflow
- Always run type-check before committing
- Use conventional commits (feat:, fix:, etc.)
- Test in staging before production

## Communication
- Be concise, skip unnecessary explanations
- Show code diffs for changes
- Summarize at end of complex tasks
```

## Pattern 5: Sub-Agent Communication

When using multiple agents, use filesystem for state sharing.

### Agent Workspace Structure

```
.claude/
└── agents/
    ├── research/         # Research agent outputs
    │   └── findings.md
    ├── implementation/   # Implementation agent state
    │   └── progress.md
    └── review/           # Review agent feedback
        └── issues.md
```

### Handoff Protocol

```markdown
# Agent Handoff: [From Agent] → [To Agent]

## Completed Work
[What was accomplished]

## Key Findings
1. [Finding 1]
2. [Finding 2]

## Files Created/Modified
- `path/to/file.ts` - [What was done]

## Recommendations for Next Agent
1. [Recommendation]
2. [Recommendation]

## Open Questions
- [Question needing resolution]
```

## Pattern 6: Self-Updating Memory

Capture learnings automatically during sessions.

### Auto-Capture Triggers

When these occur, update memory files:
- Error resolved after debugging → Add to gotchas.md
- Pattern discovered in codebase → Add to patterns.md
- User states preference → Add to preferences.md
- Workaround found → Add to gotchas.md

### Update Protocol

```bash
# Append new learning to appropriate file
echo "
### [New Learning Title]
- **Context**: [When this applies]
- **Details**: [The learning]
- **Added**: $(date +%Y-%m-%d)
" >> .claude/memory/patterns.md
```

## Quick Start Commands

### Start New Session

```bash
# 1. Check for existing context
cat .claude/context/current-task.md 2>/dev/null || echo "No active task"

# 2. Check active plans
ls -la .claude/plans/*.md 2>/dev/null || echo "No active plans"

# 3. Review memory
cat .claude/memory/gotchas.md 2>/dev/null | head -50
```

### Save Session Context

```bash
# Before ending session, update current-task.md with:
# - What was accomplished
# - What's next
# - Any blockers
```

### Resume Previous Work

```bash
# 1. Read the plan
cat .claude/plans/[plan-name].md

# 2. Read current context
cat .claude/context/current-task.md

# 3. Check recent decisions
cat .claude/context/decisions.md | tail -30
```

## Integration with Existing Skills

| Skill | Integration |
|-------|-------------|
| **context-manager** | Use scratch/ for large context analyzer outputs |
| **project-sync** | Store sync status in context/sync-status.md |
| **bug-fixing** | Document debugging journey in context/debug-log.md |
| **session-manager** | Named sessions map to plan files |

## Best Practices

1. **Update incrementally** - Don't wait until session end
2. **Be specific** - Vague notes don't help future sessions
3. **Clean up scratch/** - Delete temporary files when done
4. **Review memory/** - Periodically prune outdated information
5. **Use consistent format** - Templates make parsing easier
6. **Reference file paths** - Future sessions need to find relevant code
7. **Date entries** - Know when context was captured
8. **Keep plans updated** - Stale plans cause confusion

## Cleanup Commands

```bash
# Clean old scratch files (older than 7 days)
find .claude/scratch -type f -mtime +7 -delete

# Archive completed plans
mv .claude/plans/completed-*.md .claude/plans/archive/

# Prune old context
# Keep only last 5 days of context files
```

---

**Version**: 1.0.0
**Last Updated**: 2025-01-08
**Maintained By**: CircleTel Development Team
**Based On**: https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering
