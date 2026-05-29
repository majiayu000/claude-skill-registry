---
name: ticks
description: Work with Ticks issue tracker and AI agent runner. Use when managing tasks or issues with tk commands, running AI agents on epics, creating ticks from a SPEC.md, or working in a repo with a .tick directory. Triggers on phrases like create ticks, tk, run ticker, epic, close the task, plan this, break this down.
---

# Ticks Workflow

Ticks is an issue tracker designed for AI agents. The `tk` CLI manages tasks, runs agents in continuous loops, and provides a web-based board for monitoring.

## When to Use Ticks vs TodoWrite

**Use Ticks (`tk`) for work that:**
- Spans multiple sessions or conversations
- Has dependencies on other tasks
- Is discovered during other work and should be tracked
- Needs human handoff or approval gates
- Benefits from persistent history and notes

**Use TodoWrite for:**
- Simple single-session tasks
- Work that will be completed in the current conversation
- Tracking progress on immediate work

Don't over-index on creating ticks for every small thing. Use your judgment.

## Skill Workflow

When invoked, follow this workflow:

### Step 0: Check Prerequisites

**1. Git repository:**
```bash
git status 2>/dev/null || git init
```

**2. Ticks initialized:**
```bash
ls .tick/ 2>/dev/null || tk init
```

**3. tk installed:**
```bash
which tk || echo "Install: curl -fsSL https://raw.githubusercontent.com/pengelbrecht/ticks/main/scripts/install.sh | sh"
```

**4. Git tracking (important):**

The `.tick/` directory should be tracked by git, not gitignored. Ticks are designed to be version-controlled so they sync across machines and team members via normal git workflows.

If you see `.tick` or `.tick/` in the project's `.gitignore`, remove it. The only things that should be gitignored are internal/local files, which is handled by `.tick/.gitignore` (ignores `.index.json` and `logs/`).

```bash
# Check if .tick is gitignored (should return nothing)
git check-ignore .tick/

# If it returns ".tick/", remove the entry from .gitignore
```

### Step 1: Check for SPEC.md

Look for a SPEC.md (or similar spec file) in the repo root.

**If no spec exists:** Go to Step 2a (Create Spec)
**If spec exists but incomplete:** Go to Step 2b (Complete Spec)
**If spec is complete:** Skip to Step 3 (Create Ticks)

### Step 2a: Create Spec Through Conversation

Have a natural conversation with the user to understand their idea:

1. **Let them describe it** - Don't interrupt, let them explain the full vision
2. **Ask clarifying questions** - Dig into unclear areas through back-and-forth dialogue
3. **Optionally use AskUserQuestion** - For quick multiple-choice decisions
4. **Write SPEC.md** - Once you have enough detail, generate the spec

**Conversation topics to explore:**
- What problem does this solve? Who's it for?
- Core features vs nice-to-haves
- Technical constraints or preferences
- How will users interact with it?
- What does "done" look like?

### Step 2b: Complete Existing Spec

If SPEC.md exists but has gaps:

1. **Read the spec** - Identify what's missing or unclear
2. **Ask targeted questions** - Focus on the gaps, don't re-ask obvious things
3. **Update SPEC.md** - Fill in the missing details

## Creating Good Tasks

**Every task should be an atomic, committable piece of work with tests.**

The ideal task:
- Has a clear, single deliverable
- Can be verified by running tests
- Results in demoable software that builds on previous work
- Is completable in 1-3 agent iterations

**Good task:**
```bash
tk create "Add email validation to registration" \
  -d "Validate email format on blur, show error below input.

Test cases:
- valid@example.com -> valid
- invalid@ -> invalid
- @nodomain.com -> invalid

Run: go test ./internal/validation/..." \
  -acceptance "All validation tests pass" \
  -parent <epic-id>
```

**Bad task:**
```bash
tk create "Add email validation" -d "Make sure emails are valid"
# No test cases, no verification criteria - agent will guess
```

See `references/tick-patterns.md` for more patterns.

### Step 3: Create Ticks from Spec

Transform the spec into ticks organized by epic.

**For phased specs:** Focus on creating ticks for the current/next phase only. Don't create ticks for future phases - they may change based on learnings.

**Epic organization:**
1. Group related tasks into logical epics (auth, API, UI, etc.)
2. Create tasks with dependencies using `-blocked-by`
3. Mark human-required tasks with `--awaiting work`

**Designing for parallel execution:**
Tasks in the same wave (no blocking relationship) may run concurrently. To avoid file conflicts:
- If two tasks edit the same file, make one block the other
- Use `tk graph <epic>` to visualize waves and verify parallel tasks touch different files
- Example: Task A edits `auth.go`, Task B edits `auth.go` → B should block on A

```bash
# Create epics
tk create "Authentication" -t epic
tk create "API Endpoints" -t epic

# Create tasks with acceptance criteria
tk create "Add JWT token generation" \
  -d "Implement JWT signing and verification" \
  -acceptance "JWT tests pass" \
  -parent <auth-epic>

tk create "Add login endpoint" \
  -d "POST /api/login with email/password" \
  -acceptance "Login endpoint tests pass" \
  -parent <api-epic> \
  -blocked-by <jwt-task>

# Human-only tasks (skipped by tk next)
tk create "Set up production database" --awaiting work \
  -d "Create RDS instance and configure access"

tk create "Create Stripe API keys" --awaiting work \
  -d "Set up Stripe account and get API credentials"
```

### Step 4: Guide User Through Blocking Human Tasks

If human tasks block automated tasks, guide the user through them before running the agent.

```bash
# Check for blocking human tasks
tk list --awaiting work
tk blocked  # See what's waiting
```

Walk the user through each blocking task, then close it:
```bash
tk close <id> "Completed - connection string in .env"
```

### Step 5: Choose Execution Mode

Ticks supports two execution approaches. If the user hasn't specified a preference, ask:

```
Question: "How would you like to execute this epic?"
Header: "Execution"
Options:
  - "tk run" - "Rich monitoring via tickboard, HITL support, cost tracking, git worktree isolation"
  - "Claude Code" - "Native parallel subagents, seamless session execution, direct visibility"
```

#### Option A: tk run

Uses the Ticks agent runner with tickboard monitoring.

```bash
# Run on specific epic
tk run <epic-id>

# Pool mode - N concurrent workers within single epic
tk run <epic-id> --pool 4

# Pool with custom stale timeout
tk run <epic-id> --pool 4 --stale-timeout 2h

# Run in isolated worktree
tk run <epic-id> --worktree

# Parallel epics (each in own worktree)
tk run <epic-id> --parallel 2

# Combined: parallel epics with pool workers each
tk run epic1 epic2 --parallel 2 --pool 4

# With cost limit
tk run <epic-id> --max-cost 5.00
```

**Monitor:** `tk board` opens local web interface.

**Best for:** Production epics, rich HITL workflows, long-running tasks, cost tracking.

#### Option B: Claude Code Native

Uses Claude Code's Task tool to spawn parallel subagents.

**Best for:** Quick parallel execution within a Claude session, direct visibility into agents.

See **`references/claude-runner.md`** for full documentation including:
- Task tool parameters and options
- Agent naming conventions (epic/tick/wave)
- Wave orchestration algorithm
- Polling strategy to avoid hangs
- HITL-aware state transitions
- Example session

#### Quick Comparison

| Aspect | `tk run` | Claude Code |
|--------|----------|-------------|
| Monitoring | Tickboard | Claude Code UI |
| HITL | Rich (approvals, checkpoints) | Basic (conversation) |
| Parallelization | Pool workers (`--pool`) or worktrees (`--parallel`) | Task subagents |
| File isolation | Worktrees (proven) | Shared workspace |
| State persistence | Tick files (survives crashes) | Session-bound |
| Cost tracking | Built-in (`--max-cost`) | Manual |

## Quick Reference

### Creating Ticks

```bash
tk create "Title" -d "Description" -acceptance "Tests pass"  # Task
tk create "Title" -t epic                                    # Epic
tk create "Title" -parent <epic-id>                          # Under epic
tk create "Title" -blocked-by <task-id>                      # Blocked
tk create "Title" --awaiting work                            # Human task
tk create "Title" --requires approval                        # Needs approval gate
```

### Querying

```bash
tk list                      # All open ticks
tk list -t epic              # Epics only
tk list -parent <epic-id>    # Tasks in epic
tk ready                     # Unblocked tasks
tk next <epic-id>            # Next task for agent
tk blocked                   # Blocked tasks
tk list --awaiting           # Tasks awaiting human
tk graph <epic-id>           # Dependency graph with parallelization
tk graph <epic-id> --json    # JSON output for agents
```

### Managing

```bash
tk show <id>                 # Show details
tk close <id> "reason"       # Close tick
tk note <id> "text"          # Add note
tk approve <id>              # Approve awaiting tick
tk reject <id> "feedback"    # Reject with feedback
```

### Running Agent (Two Modes)

**Mode A: Native tk run**
```bash
tk run <epic-id>                      # Run on epic
tk run --auto                         # Auto-select epic
tk run <epic-id> --pool 4             # Pool mode (4 concurrent workers)
tk run <epic-id> --pool 4 --stale-timeout 2h  # Custom stale timeout
tk run <epic-id> --worktree           # Use git worktree
tk run <epic-id> --parallel 3         # 3 epics in parallel worktrees
tk run a b --parallel 2 --pool 4      # 2 epics, 4 workers each
tk run <epic-id> --max-iterations 10  # Limit iterations
tk run <epic-id> --max-cost 5.00      # Cost limit
tk run <epic-id> --watch              # Restart when tasks ready
tk board                              # Web interface
```

**Mode B: Claude Code Native**
```bash
# See references/claude-runner.md for full details

# 1. Get dependency graph
tk graph <epic-id> --json

# 2. Ask user for MAX_AGENTS (1-10)

# 3. For each wave, launch Task agents:
#    Task(subagent_type: "general-purpose",
#         name: "<epic>-w<wave>-<tick>",
#         run_in_background: true,
#         mode: "bypassPermissions")

# 4. Poll for completion, sync to ticks
tk close <tick-id> --reason "Completed via Claude runner"
```

### Planning Parallel Execution

Before running agents, use `tk graph` to understand parallelization opportunities:

```bash
tk graph <epic-id>        # Human-readable wave breakdown
tk graph <epic-id> --json # Machine-readable for planning
```

The graph shows:
- **Waves**: Groups of tasks that can run in parallel
- **Max parallel**: How many workers you could use at once
- **Critical path**: Minimum sequential steps to complete the epic
- **Dependencies**: What each task is blocked by

Use this to decide:
- `--pool N` for N concurrent workers within one epic (recommended)
- `--parallel N` for N epics in separate worktrees
- Combine both: `--parallel 2 --pool 4` for 2 epics with 4 workers each

See `references/tk-commands.md` for full reference.

## Assisting with Awaiting Ticks

When working interactively, help users process awaiting ticks:

```bash
tk list --awaiting    # Find ticks awaiting human
tk next --awaiting    # Next one needing attention
```

Use AskUserQuestion to help users decide, then execute:

```bash
# User approves
tk approve <id>

# User rejects
tk reject <id> "feedback here"

# User provides input
tk note <id> "Use sliding window algorithm" --from human
tk approve <id>
```

Always use `--from human` when adding notes on behalf of the user.
