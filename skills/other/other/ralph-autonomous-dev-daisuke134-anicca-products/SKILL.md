---
name: ralph-autonomous-dev
description: Enables autonomous development loops that run until all tasks pass. Use when the user says "until done", "keep going", "finish this", "終わるまでやれ", or requests long-running autonomous iteration with fix_plan.md tracking.
---

# Ralph-Style Autonomous Development Skill

## When to Use This Skill

Invoke this skill when:
- User says "until done", "keep going until complete", "finish this"
- Task requires multiple iterations (tests passing, all features complete)
- Long-running autonomous development is requested
- User explicitly mentions "Ralph" or "autonomous loop"

## Core Concept

Ralph is a bash wrapper for Claude Code that **keeps you running until the job is done**. This skill teaches you to work in a Ralph-compatible way, even without the external wrapper.

## The Ralph Pattern

```
1. Read fix_plan.md → Pick next incomplete task
2. Implement → Run tests
3. Update fix_plan.md → Mark complete or note blockers
4. Repeat until ALL tasks complete
5. Output EXIT_SIGNAL: true when truly done
```

## File Structure

Maintain these files in `.ralph/`:

| File | Purpose |
|------|---------|
| `PROMPT.md` | High-level project goals and rules |
| `fix_plan.md` | Checkbox task list (current work) |
| `AGENT.md` | Build/test commands |

## fix_plan.md Format

```markdown
# Current Sprint Tasks

## Priority 1 (Critical)
- [ ] Task description here
- [x] Completed task

## Priority 2 (Important)
- [ ] Another task

## Blockers
- None currently
```

## Working Loop Behavior

### Before Each Implementation
1. Read `fix_plan.md`
2. Select the first unchecked `- [ ]` item
3. Announce: "Working on: [task name]"

### After Each Implementation
1. Run tests (use commands from `AGENT.md`)
2. If PASS: Mark task `- [x]` in `fix_plan.md`
3. If FAIL: Fix the issue, repeat
4. Move to next task

### Completion Detection

**DO NOT output EXIT_SIGNAL: true unless:**
- ALL checkboxes in `fix_plan.md` are `[x]`
- ALL tests pass
- No remaining work

**Output format when truly complete:**
```
RALPH_STATUS:
  tasks_complete: true
  tests_passing: true
  EXIT_SIGNAL: true
```

## Circuit Breaker Rules

Stop and ask for help if:
- Same error 3+ times in a row
- No progress for 3+ iterations
- Blocked by external dependency (API key, permission, etc.)

## Example Workflow

```
User: "Implement feature X until all tests pass"

Claude Code:
1. Check/create .ralph/fix_plan.md
2. Break feature X into subtasks
3. Loop:
   - Pick first unchecked task
   - Implement
   - Run tests
   - Mark complete if passing
   - Repeat
4. When all done:
   RALPH_STATUS:
     tasks_complete: true
     tests_passing: true
     EXIT_SIGNAL: true
```

## Integration with CLAUDE.md

Add to project's CLAUDE.md:
```markdown
### Autonomous Development
- For "until done" tasks, follow `.claude/skills/ralph-autonomous-dev/SKILL.md`
- Always use fix_plan.md to track progress
- Output EXIT_SIGNAL: true only when truly complete
```

## Commands Reference

```bash
# Build & Test iOS
cd aniccaios && fastlane test

# Build & Test API
cd apps/api && npm test

# Run E2E Tests
maestro test maestro/ --include-tags smokeTest
```

## Key Principles

1. **Never exit prematurely** - Only EXIT_SIGNAL when ALL work is done
2. **Track progress explicitly** - Update fix_plan.md after each task
3. **Test after every change** - Don't mark complete without passing tests
4. **Ask for help when stuck** - Circuit breaker prevents infinite loops
5. **Incremental commits** - Commit after each completed task

## Common Patterns

### Pattern: Feature Implementation
```
1. Create fix_plan.md with subtasks
2. Implement each subtask
3. Test after each
4. Commit when task passes
5. Move to next
```

### Pattern: Bug Fix
```
1. Reproduce the bug (write failing test)
2. Fix the code
3. Verify test passes
4. Commit
5. EXIT_SIGNAL: true
```

### Pattern: Refactoring
```
1. Ensure all tests pass (baseline)
2. Make incremental changes
3. Run tests after each change
4. Commit when stable
5. EXIT_SIGNAL: true when complete
```

## References

- [Ralph GitHub](https://github.com/frankbria/ralph-claude-code)
- [Claude Code Best Practices](https://docs.anthropic.com/en/docs/claude-code/best-practices)
