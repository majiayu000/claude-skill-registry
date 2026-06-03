---
name: dev-cycle
description: Start or resume a development session. Use when beginning feature work, implementing changes, or continuing previous work. Orchestrates discovery, planning, review, and build phases with Bob and Garry.
---

# Dev Cycle - Development Session Manager

Orchestrated development workflow: Discovery → Planning → Review → Build

## Agent Roles

- **Scout**: Codebase Explorer - explores before planning (haiku, fast, cheap)
- **Bob**: Technical Builder - builds code, ensures quality
- **Garry**: Chief of Staff - validates completion, checks alignment
- **Arlo**: Pattern Whisperer - involved when data/analytics/numbers are part of the work

## Session State

Sessions are stored in `~/.claude/dev-cycles/active/` and `~/.claude/dev-cycles/completed/`

## Starting a Session

### 1. Check for Active Session
```bash
ls ~/.claude/dev-cycles/active/ | grep "$(basename $(pwd))"
```

If active session exists for this project:
- Read the session file
- Show current status (phase, completed tasks, blockers)
- Ask: "Continue this session or start new?"

### 2. Start New Session

Ask these questions in order:

1. **Branch**: "Work on existing branch, create new, or no branch?"
   - If existing: `git branch -a` to show options
   - If new: Ask for branch name (follow branch-workflow conventions)
   - If none: Work on current branch

2. **Scope**: "What are we building?"
   - Get clear description
   - For small tasks: Can collapse Discovery+Planning

3. Create session file:
```
~/.claude/dev-cycles/active/{project-name}--{YYYYMMDD-HHMMSS}.md
```

## Session File Format

```markdown
# Dev Cycle: {description}

## Meta
- **Project**: {project-name}
- **Branch**: {branch-name or "none"}
- **Started**: {timestamp}
- **Phase**: discovery | planning | review | building | blocked
- **Involves Data/Analytics**: yes | no

## Discovery
{Requirements, context, decisions made during discovery}

## Plan
{Tasks with checkboxes, phases, acceptance criteria}

## Progress
- [x] Task 1 - completed
- [ ] Task 2 - current
- [ ] Task 3 - pending

## Blockers
{Any blockers encountered - stop and ask Tako}

## Batched Questions
{Easy questions to ask after build is done}

## Decisions
{Key decisions made during this session}
```

## Phase Flow

### Discovery Phase

**1. Scout Exploration (for non-trivial tasks):**
```
Delegate to Scout: "Explore [area relevant to task].
Find: where things live, how they work, existing patterns.
Questions: [specific unknowns from Tako's description]"
```

Scout returns: What exists, how it works, options, unknowns.

**2. Discovery Discussion:**
- Review Scout's findings with Tako
- Clarify edge cases
- Discuss options and tradeoffs
- Make decisions on approach

**3. Update session file with discoveries**

**Exit**: "Ready to plan?"

**Skip Scout when:**
- Small/trivial task
- You already know the codebase well
- Tako says "just do it"

### Planning Phase
- Create task list with phases
- Define acceptance criteria
- Consider technical approach
- For complex work: Use OpenSpec structure
- Update session file with plan
- **Exit**: "Ready for your review?"

### Review Phase
- Present plan summary to Tako
- Tako reviews and adjusts
- Final approval to build
- **Exit**: Tako says "go" or "approved" or similar

### Build Phase
Orchestrated execution:

```
1. For each task/phase:
   └─ Delegate to Bob: "Build [task]. Context: [from session]"

2. After Bob completes:
   └─ Delegate to Garry: "Validate [task] is complete. Check quality."

3. If task involves data/analytics/numbers:
   └─ Delegate to Arlo: "Validate data logic, patterns, calculations in [task]"
   └─ Arlo checks: data flow, edge cases, number handling, analytics accuracy

4. I review output:
   └─ Problems? → Tell agents to fix
   └─ Blocker? → STOP, update session, ask Tako
   └─ Easy question? → Add to "Batched Questions" section

5. Update session file with progress

6. Continue until all tasks done
```

### When to Involve Arlo

Bring Arlo into the loop when the work involves:
- Analytics dashboards or reporting
- Data processing or transformation
- Calculations, aggregations, statistics
- Database queries with numeric results
- Charts, graphs, visualizations
- Pattern detection or anomaly detection
- Financial calculations
- Metrics, KPIs, measurements

Arlo validates:
- Data logic is correct
- Edge cases handled (nulls, zeros, negatives)
- Calculations are accurate
- Patterns make sense
- Numbers tell the right story

### Handling Issues

**Blockers** (STOP immediately):
- Missing requirements
- External dependency needed
- Permission/access issues
- Architecture questions
- Anything that could go wrong

**Batched Questions** (ask after build):
- Naming preferences
- Minor style choices
- Optional enhancements
- "Nice to have" decisions

## Small Task Mode

For small tasks (single feature, few files):
- Collapse Discovery + Planning into one conversation
- Still ask about branch
- Still create session file (for learning capture)
- Can skip formal Review phase if Tako says "just do it"

## Integration

**With branch-workflow**:
- Follow branch naming conventions
- Commit regularly during build
- Push to remote

**With megg**:
- Load context at start: `mcp__megg__context`
- Log significant decisions: `mcp__megg__learn`

**With OpenSpec** (for complex work):
- Create change proposal in openspec/changes/
- Follow openspec-workflow

## Commands in Session

While in an active dev-cycle, Tako can say:
- "continue" - Resume where we left off
- "skip to build" - Jump to build phase
- "pause" - Save state, stop for now
- "blocked on X" - Log blocker
- "/finish-dev" - Complete the cycle

## Example Session Start

```
Me: Checking for active dev-cycle sessions...
    No active session for this project.

    Let's start a new dev cycle.

    1. Branch: Work on existing, create new, or stay on current?

User: new branch feat/add-user-auth

Me: Created branch feat/add-user-auth

    2. What are we building?

User: User authentication with JWT tokens

Me: Got it. Creating session...
    [Session file created]

    Let's start discovery. Tell me more about:
    - What auth methods do you need?
    - Any existing auth code to integrate with?
    - ...
```
