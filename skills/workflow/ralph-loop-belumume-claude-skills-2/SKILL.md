---
name: ralph-loop
description: Activate autonomous Ralph Wiggum loop mode for iterative task completion. Use when you have a well-defined task with clear completion criteria that benefits from persistent, autonomous execution.
trigger: When user invokes /ralph, mentions "ralph mode", "ralph loop", "autonomous loop", or wants to run Claude iteratively until a task is complete
version: 1.0.0
tags:
  - automation
  - workflow
  - claude-code-only
  - hooks
  - autonomous
---

# Ralph Wiggum Loop Mode

Named after the Simpsons character who "never stops despite being confused," this technique runs Claude Code in a loop where the prompt stays the same but the codebase accumulates changes. Each iteration reads previous work and continues until completion.

## When to Use Ralph Mode

**Ideal for:**
- Well-defined implementation tasks with clear completion criteria
- Refactoring or migration work (e.g., React v16 to v19)
- Test-driven development cycles (run until tests pass)
- Batch processing or repetitive tasks
- Overnight autonomous work sessions

**Not ideal for:**
- Tasks requiring design decisions or human judgment
- Exploratory work without clear end states
- Tasks where requirements may change mid-execution
- First-time implementations where you need to learn the code

## Activation Protocol

### Step 1: Validate Task Suitability

Before activating, confirm:
- [ ] Task has clear, measurable completion criteria
- [ ] Success can be verified programmatically (tests, build, specific file state)
- [ ] The work is in a git-tracked directory
- [ ] You understand what success looks like

### Step 2: Create State File

Create `.claude/ralph-loop.local.md` with the following structure:

```markdown
---
active: true
iteration: 0
max_iterations: 20
completion_promise: null
---

# Your Task Prompt Here

## Objective
[Clear statement of what needs to be accomplished]

## Completion Criteria
Complete when TODO.md shows [x] ALL_TASKS_COMPLETE

## Verification Commands
Run these to check progress:
- `[test command]`
- `[build command]`

## Context
- Read [relevant files] for specifications
- Follow [conventions file] for code style
```

### Step 3: Create TODO.md (Recommended Completion Method)

Create `TODO.md` in your project root:

```markdown
# Task Checklist

## Tasks
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Completion
- [ ] ALL_TASKS_COMPLETE
```

### Step 4: Start the Loop

Simply run Claude normally. The Stop hook will detect the state file and keep the loop running until completion is detected.

```bash
claude
```

## Two Completion Methods

### Method 1: TODO.md Markers (Recommended)

The hook checks `TODO.md` for `[x] ALL_TASKS_COMPLETE`. This is more reliable because:
- It's visible in the file system
- It can be tracked in git
- Claude can easily update it
- You can see progress (X/Y tasks complete)

### Method 2: Promise Tags (Legacy)

Set `completion_promise` in the state file and output `<promise>YOUR_TEXT</promise>` when complete.

```markdown
---
active: true
iteration: 0
max_iterations: 20
completion_promise: "feature implemented"
---
```

When Claude outputs `<promise>feature implemented</promise>`, the loop ends.

## Configuration Options

In `.claude/ralph-loop.local.md` frontmatter:

| Option | Default | Description |
|--------|---------|-------------|
| `active` | `true` | Set to `false` to disable loop |
| `iteration` | `0` | Current iteration count (auto-incremented) |
| `max_iterations` | `20` | Safety cap (0 = unlimited) |
| `completion_promise` | `null` | Text to match for promise completion |

## During Execution

### Iteration Status

Every iteration shows:
- Current iteration number
- Task progress (from TODO.md)
- Completion criteria
- Max iterations remaining

### Checkpoint Notifications

Every 5 iterations, you'll see a checkpoint reminder to:
- Review changes: `git log --oneline -10`
- Verify progress is on track
- Consider adjusting the prompt if stuck

### Manual Intervention

**To pause the loop:**
```bash
# Edit the state file
# Change active: true → active: false
```

**To stop immediately:**
```bash
rm .claude/ralph-loop.local.md
```

**To resume:**
```bash
# Re-create or edit the state file
# Set active: true
claude
```

## Safety Features

- **Iteration cap**: Prevents infinite loops (default: 20)
- **Git tracking**: Every change is revertible
- **Checkpoint notifications**: Reminders to review progress
- **Clear completion criteria**: Loop only exits on explicit success
- **Cost awareness**: Track iterations to estimate API costs

## Example: MetricFlow Phase 7-8

```markdown
---
active: true
iteration: 0
max_iterations: 25
completion_promise: null
---

# MetricFlow Phase 7-8: Educator Agent

## Objective
Implement the Educator Agent that uses Claude API to generate educational
explanations for code metrics.

## Completion Criteria
Complete when TODO.md shows [x] ALL_TASKS_COMPLETE

## Verification Commands
- `cd backend && python -m pytest tests/test_educator.py -v`
- `cd backend && python -c "from app.agents.educator import EducatorAgent; print('OK')"`

## Context
- Read docs/plans/MASTER_PLAN.md sections 5.3 (Educator Agent)
- Follow CLAUDE.md for project conventions
- Analyzer and Pattern agents already complete (use their output formats)

## Instructions
1. Check TODO.md for current task list
2. Implement next incomplete task
3. Write tests as you go
4. Run verification after each change
5. Mark [x] ALL_TASKS_COMPLETE when done
```

And corresponding `TODO.md`:

```markdown
# Phase 7-8: Educator Agent

## Tasks
- [ ] Create EducatorAgent class skeleton in backend/app/agents/educator.py
- [ ] Add Claude API client initialization
- [ ] Implement explain_complexity() method
- [ ] Implement explain_maintainability() method
- [ ] Implement explain_code_smells() method
- [ ] Add course concept mapping
- [ ] Write unit tests for all methods
- [ ] Integration test with Analyzer output

## Completion
- [ ] ALL_TASKS_COMPLETE
```

## Troubleshooting

**Loop won't start:**
- Check `.claude/ralph-loop.local.md` exists
- Verify `active: true` is set in frontmatter

**Loop won't stop:**
- Ensure TODO.md contains exactly `[x] ALL_TASKS_COMPLETE` (case-insensitive)
- Or check `completion_promise` matches your output tag
- Check `max_iterations` isn't set to 0 (unlimited)
- Manual stop: `rm .claude/ralph-loop.local.md`

**Stuck on same error:**
- Review the error pattern
- Adjust the prompt with more specific guidance
- Consider breaking task into smaller subtasks

**Costs too high:**
- Reduce `max_iterations`
- Use shorter checkpoint intervals for early review
- Consider if task is too complex for Ralph mode

## Tips for Success

1. **Clear prompts reduce iterations by 40-60%** - be specific
2. **Start with small max_iterations (5-10)** until confident
3. **Git commit after every checkpoint** - easy rollback
4. **Use TODO.md completion** - more reliable than promise tags
5. **Monitor first few iterations** - catch bad patterns early
6. **Supervised autonomy** - review at checkpoints for course projects

## Cost Estimates

| Task Complexity | Iterations | Estimated Cost |
|-----------------|------------|----------------|
| Simple (single feature) | 5-10 | $5-15 |
| Medium (multi-file changes) | 10-20 | $15-30 |
| Complex (full phase) | 20-50 | $30-75 |

## Quick Start Template

```bash
# 1. Create state file
mkdir -p .claude
cat > .claude/ralph-loop.local.md << 'EOF'
---
active: true
iteration: 0
max_iterations: 20
completion_promise: null
---

# Your Task

## Objective
[What you want to accomplish]

## Completion
Check TODO.md for [x] ALL_TASKS_COMPLETE
EOF

# 2. Create TODO.md
cat > TODO.md << 'EOF'
# Tasks
- [ ] First task
- [ ] Second task

## Completion
- [ ] ALL_TASKS_COMPLETE
EOF

# 3. Start Ralph loop
claude
```
