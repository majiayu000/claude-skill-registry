---
name: ralph-wiggum
description: Autonomous AI coding loop for unattended development - lets Claude work continuously on tasks while you sleep, with mandatory sandbox enforcement for safety
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - TodoWrite
---

# Ralph Wiggum Mode

"Me fail English? That's unpossible!" - Ralph Wiggum

Ralph Wiggum Mode is an autonomous AI coding loop that enables Claude Code to work continuously on tasks without human intervention. Named after the persistently optimistic Simpsons character, this technique lets Claude work "overnight shifts" while you sleep.

## Key Principle

**Progress persists in files and git, not in the LLM's context window.**

When context fills up, the loop restarts Claude with fresh context. The new instance picks up from the filesystem state (your code, git history, and task tracking files).

## When to Use This Skill

Use Ralph Wiggum mode for:
- Overnight feature development
- Bug bashes (fixing multiple issues)
- Test coverage improvement
- Refactoring large codebases
- Documentation generation
- Any multi-step task you'd like completed while away

## Security Model

**CRITICAL: Ralph requires a sandboxed environment.**

Ralph uses `--dangerously-skip-permissions` which can:
- Delete files without confirmation
- Read credentials (~/.ssh, ~/.aws)
- Make network requests
- Run arbitrary commands

**Ralph will REFUSE to start unless it detects:**
- Container environment (Docker/Kubernetes)
- Network isolation (cannot reach internet)
- Non-root user
- No access to sensitive paths

## Quick Start

### 1. Initialize Ralph in Your Project

```bash
# Run the init script to scaffold Ralph files
./ralph-init.sh
```

This creates:
- `RALPH_PROMPT.md` - The prompt fed to Claude each iteration
- `IMPLEMENTATION_PLAN.md` - Task tracking file
- `ralph.sh` - The main loop script
- `ralph-sandbox.sh` - Docker wrapper
- `Dockerfile.ralph` - Sandbox container definition

### 2. Define Your Work

```bash
# Create specs directory for requirements
mkdir -p specs

# Write your requirements
cat > specs/my-feature.md << 'EOF'
## Feature: User Dashboard

### Requirements
- Show user's recent activity
- Display usage statistics
- Allow date range filtering
EOF

# Update the implementation plan
cat > IMPLEMENTATION_PLAN.md << 'EOF'
## Tasks

- [ ] Create Dashboard component
- [ ] Add activity feed API endpoint
- [ ] Implement date range picker
- [ ] Write tests for dashboard
EOF
```

### 3. Run Ralph (In Sandbox)

```bash
# Recommended: Use the Docker wrapper
./ralph-sandbox.sh

# With iteration limit
./ralph-sandbox.sh . 20

# Check progress from another terminal
tail -f ralph.log
git log --oneline -10
```

### 4. Review Results

```bash
# See what Ralph did
git log --oneline

# Check task completion
cat IMPLEMENTATION_PLAN.md

# Verify tests pass
pytest
```

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL BASH LOOP                            │
│                                                                  │
│   while :; do                                                    │
│       ┌─────────────────────────────────────────────────┐       │
│       │           CLAUDE SESSION                         │       │
│       │                                                  │       │
│       │  1. Read RALPH_PROMPT.md                        │       │
│       │  2. Check IMPLEMENTATION_PLAN.md                │       │
│       │  3. Pick a task, implement it                   │       │
│       │  4. Run tests, commit changes                   │       │
│       │  5. Context fills → Session ends                │       │
│       └─────────────────────────────────────────────────┘       │
│                           ↓                                      │
│       Git commit saves progress                                  │
│       Loop restarts with fresh context                           │
│   done                                                           │
└─────────────────────────────────────────────────────────────────┘
```

## Files Reference

### RALPH_PROMPT.md

The prompt loaded each iteration. Customize this for your use case:

```markdown
# Ralph Mode Instructions

You are operating in autonomous Ralph mode.

## Each Iteration
1. Read IMPLEMENTATION_PLAN.md and git log
2. Pick ONE pending task, mark it in-progress
3. Implement fully with tests
4. Mark complete, commit changes

## Rules
- Never skip tests
- Commit after each meaningful change
- If blocked, document why and continue
```

### IMPLEMENTATION_PLAN.md

Persistent task tracking (survives context resets):

```markdown
## Tasks

- [x] Task 1 (completed in iteration 1)
- [x] Task 2 (completed in iteration 2)
- [ ] Task 3 (in progress)
- [ ] Task 4 (pending)
```

### ralph.sh

The main loop with sandbox enforcement. Key features:
- Refuses to run outside sandbox
- Configurable iteration limits
- Git commits after each iteration
- Graceful shutdown handling

### ralph-sandbox.sh

Docker wrapper that:
- Builds sandbox image if needed
- Mounts only project directory
- Disables network (`--network none`)
- Sets resource limits (memory, CPU, PIDs)
- Drops all capabilities

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `RALPH_MAX_ITERATIONS` | `0` (unlimited) | Stop after N iterations |
| `RALPH_MODEL` | `sonnet` | Claude model to use |
| `RALPH_COST_LIMIT` | `50.00` | Max spend in USD (with cost monitor hook) |
| `ANTHROPIC_API_KEY` | optional | API key (not needed with Claude Code subscription) |

### Sandbox Override (Dangerous)

Only for custom sandbox environments you've verified:

```bash
RALPH_I_KNOW_WHAT_IM_DOING=sandboxed ./ralph.sh
```

## Best Practices

### Prompt Engineering

1. **Be specific** - Tell Claude exactly what to do each iteration
2. **Single task focus** - "Pick ONE task" prevents context bloat
3. **Require tests** - Include testing in the prompt
4. **Track progress** - Use IMPLEMENTATION_PLAN.md as shared state

### Task Decomposition

Break large tasks into small, atomic pieces:

```markdown
## Bad
- [ ] Implement user authentication

## Good
- [ ] Create User model with email, password_hash
- [ ] Add POST /api/register endpoint
- [ ] Add POST /api/login endpoint
- [ ] Add password reset flow
- [ ] Add JWT middleware
- [ ] Write auth tests
```

### Monitoring

```bash
# Watch iterations in real-time
tail -f ralph.log

# Check commits
watch -n 5 'git log --oneline -10'

# Monitor resource usage
docker stats
```

## Safety Hooks (Recommended)

Install these hooks for additional safety:

```bash
# Block dangerous operations
skillz hooks install ralph-safety-check

# Track API costs
skillz hooks install ralph-cost-monitor
```

## Troubleshooting

### Ralph won't start

Check sandbox detection output. You need at least 3 checks passing:
- Container detected
- Network isolated
- Non-root user
- No sensitive path access

### Ralph gets stuck on a task

1. Check `ralph.log` for errors
2. Update `IMPLEMENTATION_PLAN.md` to unblock
3. Add clarifying notes to `RALPH_PROMPT.md`

### Runaway iterations

Set `MAX_ITERATIONS` or use the cost monitor hook:

```bash
./ralph-sandbox.sh . 20  # Stop after 20 iterations
```

## References

- [Original Ralph Wiggum Technique](https://github.com/ghuntley/how-to-ralph-wiggum)
- [Geoffrey Huntley's Blog](https://ghuntley.com/ralph/)
- [VentureBeat Coverage](https://venturebeat.com/technology/how-ralph-wiggum-went-from-the-simpsons-to-the-biggest-name-in-ai-right-now)
