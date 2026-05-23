---
name: session-continuity-assistant
description: This skill should be used when the user asks to "continue session", "resume work", "what was I doing last time", "pick up where I left off", "check recent activity", "what happened since last session", or needs context about previous sessions.
version: 1.0.0
---

# Session Continuity Assistant

## Purpose

Help users seamlessly resume work by leveraging the framework's multi-resolution memory system. This skill provides deep context about recent activity, project progress, and suggested next actions.

## When to Use

- User returns after time away
- User forgot what they were working on
- User wants to understand recent progress
- User needs context from previous sessions
- User asks what they were doing
- User wants to know what changed since last session

## Core Workflow

### Step 1: Check Current State

Read `.session-state.md` from the providers directory to understand:
- Last session date and topic
- Active projects
- Current focus
- Pending tasks
- Aggregation status (weekly/monthly logs)

**Location**: `~/.claude-memory/providers/claude/session-state.md`

### Step 2: Load Recent Activity

Read appropriate memory level based on time elapsed:

**Same day**:
- Load daily log: `~/.claude-memory/providers/claude/logs/daily/YYYY.MM.DD.md`
- Contains full session details (~150 lines)

**Same week (1-7 days ago)**:
- Load weekly summary: `~/.claude-memory/providers/claude/logs/weekly/YYYY.MM.weekN.md`
- Contains aggregated week activities (~100 lines)

**Same month (8-30 days ago)**:
- Load monthly summary: `~/.claude-memory/providers/claude/logs/monthly/YYYY.MM.md`
- Contains high-level monthly overview (~30 lines)

**Older than 30 days**:
- Check aggregation status first
- Inform user if logs need aggregation
- Suggest running `/aggregate week` or `/aggregate month`

### Step 3: Project Context

If user was working on specific project:

1. **Read project context**: `.projects/[project-name]/.context.md`
   - Full project memory
   - Recent decisions
   - Technical details

2. **Read project status**: `.projects/[project-name]/.status.md`
   - Current phase/status
   - Roadmap
   - Next actions
   - Blockers

3. **Highlight progress**: Compare with previous state if available

### Step 4: Cross-Provider Check

Check if other providers (LMStudio, Gemini, etc.) have recent activity:

**Read**: `~/.claude-memory/integration/provider-activities.quick.md`
- Shows recent activity from all providers
- Prevents duplicated work
- Enables seamless handoff between providers

### Step 5: Present Summary

Format the continuation summary clearly:

```
**Resuming from**: [Last session date] - [Time elapsed]

**Last Topic**: [What you were doing]

**Progress Made**:
- Key achievement 1
- Key achievement 2
- Key achievement 3

**Decisions/Blockers**:
- Decision 1
- Blocker 1 (if any)

**Current State**:
- Project: [Project name]
- Status: [Status emoji + state]
- Files changed: [Count]

**Suggested Next Steps** (Top 3):
1. [Priority action 1]
2. [Priority action 2]
3. [Priority action 3]

---

Ready to continue? Or would you like to start something new?
```

### Step 6: Offer Choices

After presenting summary, offer clear options:

**Option A**: Continue where you left off
- Load full project context
- Focus on next priority action

**Option B**: Check other projects
- Show active projects dashboard
- Allow context switch with `/switch [project-name]`

**Option C**: Start new activity
- Suggest using `/new` command
- Begin fresh context

## Memory Structure Reference

### Hierarchical Organization

**Working Memory** (Always loaded):
- `.session-state.md` - Current session context (~50 lines)
- Always in providers/claude/ directory

**Quick Memories** (Startup only):
- `global-memory.quick.md` - User profile condensed (~50 lines)
- `project.context.quick.md` - Project essentials (~30 lines)
- `provider-activities.quick.md` - Cross-provider timeline (~10 lines)

**Full Memories** (On-demand):
- `global-memory.safe.md` - Complete profile, PII redacted (~165 lines)
- `project.context.md` - Full project memory
- Daily/weekly/monthly logs

**Cloud Memory** (If configured):
- GitHub repository: claude-memory-cloud
- Synced across devices
- Contains all logs, projects, global memory

### Reading Strategy

**To continue session from**:

| Time Elapsed | Read | Token Cost |
|--------------|------|------------|
| Today | Daily log | ~150 lines |
| This week | Weekly summary | ~100 lines |
| This month | Monthly summary | ~30 lines |
| Older | Check aggregation status | ~10 lines |

## Best Practices

### Efficient Context Loading

1. **Start minimal**: Read session-state first (50 lines)
2. **Load progressively**: Only load detailed logs if needed
3. **Respect token budget**: Use quick versions when available
4. **Aggregate first**: If logs not aggregated, suggest user run `/aggregate`

### Temporal Awareness

**Check current date vs last session**:
- Same day: "Continuing from earlier today"
- Yesterday: "Continuing from yesterday"
- This week: "Continuing from [day] this week"
- Older: "It's been [N] days since last session"

**Suggest aggregation when needed**:
- Friday afternoon: "Would you like to run `/aggregate week` before weekend?"
- End of month: "Month ending soon, consider `/aggregate month`"

### Project Awareness

**Understand project state transitions**:
- PLANNING → IMPLEMENTING → TESTING → COMPLETED
- Different next actions per state
- Highlight blockers if project stuck

**Multi-project scenarios**:
- If user worked on multiple projects, prioritize by "last touched"
- Show top 3 active projects
- Allow quick switching with `/switch`

## Resources

For detailed information, see:
- **`references/memory-structure.md`** - Complete framework memory layout
- **`references/continuation-patterns.md`** - Common resume scenarios and templates

## Integration with Commands

This skill complements framework commands:

**`/continue`**: Uses quick memories (84-88% token savings)
**`/switch [project]`**: Changes project context
**`/projects`**: Lists all active projects
**`/end`**: Creates detailed session log for continuity

Use this skill when user asks conversationally; use commands when explicit control needed.

## Examples

### Example 1: Same-Day Continuation

**User**: "What was I doing?"

**Skill loads**:
1. session-state.md (last session today, 3 hours ago)
2. Daily log for today
3. Current project context

**Response**:
```
**Resuming from**: Today, 3:12 PM (3 hours ago)

**Last Topic**: Implementing cloud memory sync (v2.3)

**Progress Made**:
- Created setup-cloud-memory.sh script
- Documented multi-device workflow
- Added provider-agnostic design

**Next Steps**:
1. Test setup script on second device
2. Merge branch to main
3. Update README with cloud sync docs

Ready to continue testing on second device?
```

### Example 2: Weekly Continuation

**User**: "What did I work on this week?"

**Skill loads**:
1. session-state.md (last session 3 days ago)
2. Weekly summary for current week
3. Provider activities (check other providers)

**Response**:
```
**Resuming from**: Monday (3 days ago)

**This Week's Focus**:
- Golfleet L2 reorganization (Monday)
- Cloud memory infrastructure planning (Tuesday-Wednesday)
- No activity Thursday-Friday

**Key Achievements**:
- Mapped 3 operational cores for Golfleet
- Designed cloud memory architecture (v2.3)
- Created comprehensive planning docs

**Open Items**:
- [ ] Complete Golfleet RACI matrix
- [ ] Test cloud memory on multiple devices

Which would you like to continue: Golfleet or Cloud Memory?
```

### Example 3: Cross-Provider Handoff

**User**: "Continue where I left off"

**Skill loads**:
1. session-state.md (last Claude session 2 days ago)
2. provider-activities.quick.md (shows LMStudio session yesterday!)
3. Load LMStudio logs to see what was done

**Response**:
```
**Note**: Your last session was with **LMStudio** yesterday, not Claude.

**LMStudio Session** (Yesterday, 10:45 AM):
- Worked on data analysis pipeline
- Processed 3 datasets
- Generated visualization scripts

**Claude Session** (2 days ago):
- Framework enhancement planning

Would you like to:
1. Continue LMStudio work (data analysis)
2. Return to Claude work (framework)
3. See full provider timeline
```

## Troubleshooting

**Issue**: Can't find recent logs
**Solution**: Check aggregation status in session-state.md; suggest `/aggregate`

**Issue**: Project context missing
**Solution**: User may not have used `/switch [project]` yet; guide to create project context

**Issue**: Memory files not found
**Solution**: Framework may not be fully set up; suggest running `/start` first

**Issue**: Cloud memory out of sync
**Solution**: Check if cloud sync configured; suggest pulling latest with `git pull` in ~/.claude-memory-cloud/

## Version History

**v1.0.0** (2025-12-28)
- Initial release
- Multi-provider awareness
- Cloud memory support
- Progressive loading strategy
