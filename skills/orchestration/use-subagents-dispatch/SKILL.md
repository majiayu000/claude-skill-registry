---
name: use-subagents-dispatch
description: Use when executing implementation plans with independent tasks in the current session
---

Execute plan by dispatching fresh subagent per task, with two-stage review after each: spec compliance first, then code quality.

**Core principle:** Fresh subagent per task + two-stage review = high quality, fast iteration

**vs. Executing Plans (parallel session):**
- Same session (no context switch)
- Fresh subagent per task (no context pollution)
- Two-stage review: spec compliance → code quality
- Faster iteration (no human-in-loop between tasks)

# The Process

**Per Task:**

1. **Dispatch implementer subagent** (./implementer-prompt.md)
   - If questions: Answer, provide context
   - Implementer implements, tests, commits, self-reviews

2. **Dispatch spec reviewer subagent** (./spec-reviewer-prompt.md)
   - If gaps found: Implementer fixes, spec reviewer re-reviews
   - Continue until spec compliant

3. **Dispatch code quality reviewer subagent** (./code-quality-reviewer-prompt.md)
   - If issues found: Implementer fixes, code reviewer re-reviews
   - Continue until approved

4. **Mark task complete** in TodoWrite

**After all tasks:**

5. **Dispatch final code-reviewer** for entire implementation
6. **Use autonome:use-branch-complete**

# Advantages

**vs. Manual execution:**
- Subagents follow TDD naturally
- Fresh context per task (no confusion)
- Parallel-safe (subagents don't interfere)
- Subagent can ask questions before AND during work

**Efficiency gains:**
- No file reading overhead (controller provides full text)
- Controller curates exactly what context is needed
- Questions surfaced before work begins

**Quality gates:**
- Self-review catches issues before handoff
- Spec compliance prevents over/under-building
- Code quality ensures implementation is well-built
- Review loops ensure fixes actually work

# Red Flags

**Never:**
- Skip reviews (spec compliance OR code quality)
- Proceed with unfixed issues
- Dispatch multiple implementation subagents in parallel (conflicts)
- Make subagent read plan file (provide full text instead)
- Skip scene-setting context
- Ignore subagent questions
- Accept "close enough" on spec compliance
- Skip review loops (reviewer found issues = implementer fixes = review again)
- **Start code quality review before spec compliance is ✅** (wrong order)
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

# Integration

**Required workflow skills:**
- **autonome:use-plan-create** - Creates the plan this skill executes
- **autonome:use-review-request** - Code review template for reviewer subagents
- **autonome:use-branch-complete** - Complete development after all tasks

**Subagents should use:**
- **autonome:use-tdd** - Subagents follow TDD for each task

**Alternative workflow:**
- **autonome:plan-execute** - Use for parallel session instead of same-session execution
