---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks in the current session
---

# Subagent-Driven Development

Execute plan by dispatching fresh subagent per task, with two-stage review after each: spec compliance review first, then code quality review.

**Core principle:** Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration

## When to Use

**Use when:**
- Have implementation plan
- Tasks mostly independent
- Want to stay in this session

**vs. Executing Plans (parallel session):**
- Same session (no context switch)
- Fresh subagent per task (no context pollution)
- Two-stage review after each task: spec compliance first, then code quality
- Faster iteration (no human-in-loop between tasks)

## The Process

1. Read plan, extract all tasks with full text, note context, create TodoWrite
2. For each task:
   - Dispatch implementer subagent (./implementer-prompt.md)
   - Answer questions if subagent asks
   - Subagent implements, tests, commits, self-reviews
   - Dispatch spec reviewer subagent (./spec-reviewer-prompt.md)
   - If spec issues: implementer fixes, re-review
   - Dispatch code quality reviewer subagent (./code-quality-reviewer-prompt.md)
   - If quality issues: implementer fixes, re-review
   - Mark task complete
3. After all tasks: dispatch final code reviewer for entire implementation
4. Use gremlins:finishing-a-development-branch

## Prompt Templates

- `./implementer-prompt.md` - Dispatch implementer subagent
- `./spec-reviewer-prompt.md` - Dispatch spec compliance reviewer subagent
- `./code-quality-reviewer-prompt.md` - Dispatch code quality reviewer subagent

## Example Workflow

```
You: I'm using Subagent-Driven Development to execute this plan.

[Read plan files from plans/active/{plan}/implementation/]
[Extract all 5 tasks with full text and context]
[Create TodoWrite with all tasks]

Task 1: Hook installation script

[Dispatch implementation subagent with full task text + context]

Implementer: "Before I begin - should the hook be installed at user or system level?"

You: "User level (~/.config/gremlins/hooks/)"

Implementer: "Got it. Implementing now..."
[Later] Implementer:
  - Implemented install-hook command
  - Added tests, 5/5 passing
  - Self-review: Found I missed --force flag, added it
  - Committed

[Dispatch spec compliance reviewer]
Spec reviewer: Spec compliant - all requirements met, nothing extra

[Dispatch code quality reviewer]
Code reviewer: Strengths: Good test coverage, clean. Issues: None. Approved.

[Mark Task 1 complete]

Task 2: Recovery modes
...
```

## Red Flags

**Never:**
- Skip reviews (spec compliance OR code quality)
- Proceed with unfixed issues
- Dispatch multiple implementation subagents in parallel (conflicts)
- Make subagent read plan file (provide full text instead)
- Skip scene-setting context (subagent needs to understand where task fits)
- Ignore subagent questions (answer before letting them proceed)
- Accept "close enough" on spec compliance
- Skip review loops (reviewer found issues = implementer fixes = review again)
- Let implementer self-review replace actual review (both are needed)
- **Start code quality review before spec compliance is done**
- Move to next task while either review has open issues

**If subagent asks questions:**
- Answer clearly and completely
- Provide additional context if needed
- Don't rush them into implementation

**If reviewer finds issues:**
- Implementer (same subagent) fixes them
- Reviewer reviews again
- Repeat until approved
- Don't skip the re-review

## Integration

**Required workflow skills:**
- **gremlins:writing-plans** - Creates the plan this skill executes
- **gremlins:requesting-code-review** - Code review template for reviewer subagents
- **gremlins:finishing-a-development-branch** - Complete development after all tasks

**Subagents should use:**
- **gremlins:test-driven-development** - Subagents follow TDD for each task

**Alternative workflow:**
- **gremlins:executing-plans** - Use for parallel session instead of same-session execution
