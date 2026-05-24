---
name: execute
description: Execute tasks with velocity and quality. Use when ready to implement after clarity and prioritization are complete. This is the fourth system in the 5-system framework.
---

# Execution System

> **Purpose:** Do the work at high quality with velocity.
> **When to trigger:** After clarity is established and priorities are set.

## Pre-Flight Checklist

Before writing any code, verify:

- [ ] **Clarity exists** - active-context.md is current with clear success criteria
- [ ] **Task is prioritized** - This is the right thing to work on now
- [ ] **Success criteria defined** - I know exactly what "done" looks like
- [ ] **Boundaries set** - I know what NOT to do

If any are missing → Return to appropriate system.

## Execution Protocol

### 1. Track Progress Visibly

Use TodoWrite at the start:
```
1. [ ] Step one of implementation
2. [ ] Step two of implementation
3. [ ] Validation step
```

Update status as you go. The user should always know where you are.

### 2. Make the Smallest Viable Change

- Don't over-engineer
- Don't add features that weren't requested
- Don't refactor unrelated code
- Don't add "nice to haves"
- Solve the exact problem, nothing more

### 3. Validate Continuously

After every significant change:
```bash
npx tsc --noEmit  # Catch type errors immediately
```

Don't let errors accumulate. Fix as you go.

### 4. One Thing at a Time

- Complete one task before starting another
- Don't context-switch mid-implementation
- If blocked, acknowledge it rather than switching
- Mark complete immediately when done

### 5. Parallel When Independent

Use subagents (Task tool) for truly independent work:
- Research while implementing
- Multiple unrelated fixes
- Exploration while writing

But NOT for dependent steps - those must be sequential.

## Quality Gates

Before marking any task complete:

### Code Quality
- [ ] Types pass (`npx tsc --noEmit`)
- [ ] No lint errors
- [ ] Follows existing patterns in codebase
- [ ] No unintended side effects

### Functionality
- [ ] Works for the happy path
- [ ] Edge cases considered
- [ ] Error states handled
- [ ] Loading states present (if UI)

### Integration
- [ ] Doesn't break existing functionality
- [ ] Works with existing data
- [ ] API contracts maintained

### Documentation (if applicable)
- [ ] Complex logic commented
- [ ] API changes noted in SOURCE_OF_TRUTH.md
- [ ] Breaking changes flagged

## Velocity Principles

**Do:**
- Edit existing files over creating new ones
- Use existing patterns and utilities
- Ask early if blocked (don't spin)
- Ship incrementally
- Commit working states frequently

**Don't:**
- Invent new patterns when existing ones work
- Gold-plate solutions
- Wait until everything is perfect
- Make changes outside the task scope

## Output Tracking

During execution, maintain:
1. **Todos** - Current task breakdown with status
2. **Active context** - Updated if scope changes
3. **Issues** - Any new problems discovered → Identity System

## Completion Criteria

A task is ONLY complete when:
1. All acceptance criteria from clarity are met
2. All quality gates pass
3. Type check passes
4. Functionality verified
5. No regressions introduced

## Handling Blocks

If you hit a wall during execution:

1. **STOP** - Don't keep trying the same failing approach
2. **DOCUMENT** - What was attempted, what failed
3. **TRANSITION** - Go to Reset System if blocked, or ask user

Never mark something complete that isn't actually done.

## Transition

After execution:
- Success → Mark complete, update SOURCE_OF_TRUTH.md if significant
- Partial success → Document what remains, continue or handoff
- Failure → Proceed to **Reset System**
- New issues discovered → Log to **Identity System**

**Capture Learning:** If something important was learned (new pattern, gotcha, or insight), add one line to `learnings.md`. Keep it brief - this is memory, not documentation.

---

*This is System 4 of 5: Clarity → Identity → Priority → Execution → Reset*
