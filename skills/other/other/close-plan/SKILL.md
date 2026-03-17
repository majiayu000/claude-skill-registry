---
name: close-plan
description: Plan completion workflow - archive plan, verify todos, create git commit, push with retry. Use for finalizing completed plans.
---

# SKILL: Close Plan (Plan Completion Workflow)

> **Purpose**: Archive completed plans and create git commits with safe push retry logic
> **Target**: Coder Agent after implementing all Success Criteria

---

## Quick Start

### When to Use This Skill
- Finalize completed plans
- Archive plan to done/ folder
- Create git commit with Co-Authored-By attribution
- Push to remote with retry logic

### Quick Reference
```bash
# Full workflow
/03_close [RUN_ID|plan_path] [no-commit] [no-push] [--force]

# Steps: Load+Verify+TODO Gate → Evidence Verify → Docs Sync+Verify → Move+Git → Worktree Merge
```

---

## Execution Directive

**CRITICAL**: NEVER skip any step - agent MUST verify execution of each step before proceeding to the next. All steps MUST execute in order. Do NOT pause between steps.

---

## Agent Teams Delegation Pattern

**Team Lead operates in delegate mode** (coordinates only, never implements):
- Step 1 TODO analysis: Spawn teammate for TODO verification
- Step 2 evidence verification: Spawn teammate for test execution
- Step 3 docs sync: Spawn teammate for documentation updates (conditional)

**MANDATORY teammate delegation**:
- TODO gate resolution (role: validator)
- Evidence verification (role: validator)
- Documentation sync (role: documenter, conditional)

**TRIVIAL EXCEPTIONS** (no delegation needed):
- Argument parsing, file existence check, timestamp/directory creation, git commit formatting

**WHY**: Agent Teams native isolation provides automatic context protection

---

## Execution Steps (Summary)

### Step 0: Mandatory Oracle Consultation (NEW)
- **Purpose**: Pre-close quality verification
- **GPT Role**: QA Expert - Completion quality assessment
- **Pattern**: mandatory_oracle_consultation before proceeding
- **Graceful Fallback**: Continue if Codex CLI unavailable

### Step 1: Load Plan + Verify SCs + TODO Gate
- Find active plan with absolute path detection
- Parse arguments (plan_path, no-commit, no-push, force)
- Check for incomplete Success Criteria
- **TODO Completion Check (BLOCKING)**: Count unchecked `- [ ]` items
  - Delegate to validator agent for TODO analysis and resolution attempt
  - Exit if validator cannot resolve (unless --force flag)
  - Full implementation: @REFERENCE.md - TODO Completion Gate
- **TaskList Verification**: Verify all tasks completed via TaskList tool
- Exit if no plan or SCs incomplete

### Step 2: Evidence Verification
- Launch validator agent
- Extract and run verify commands from Success Criteria
- Distinguish between "no verify commands" and "verify failed"
- Exit if verification fails

### Step 3: Documentation Sync + Verify (Conditional)
- Check for documentation-relevant changes
- **If changes detected**: Launch documenter agent
- **If no changes**: Skip with message "No documentation update needed"
- Exit if verification fails
- See @.claude/agents/documenter/REFERENCE.md for condition check logic

### Step 4: Archive + Git
- Move plan to `.pilot/plan/done/YYYYMMDD/`
- **TaskUpdate**: Mark plan task as completed
- Create git commit with Co-Authored-By
- Push with retry (3 attempts, 2s/4s/8s backoff)
- Skip commit/push if flags set

### Step 5: Worktree Merge (Optional)
- Trigger if worktree context exists
- Squash merge to main branch
- Cleanup worktree and branch

---

## What This Skill Covers

### In Scope
- Plan path detection (absolute paths)
- Success Criteria verification
- Evidence verification (validator agent)
- Documentation sync + verify (documenter agent, single call)
- Plan archival to done/
- Git commit with Co-Authored-By
- Git push with retry (3 attempts, exponential backoff)
- Worktree auto-merge to main branch with cleanup

### Out of Scope
- Advanced git workflows → @.claude/skills/git-master/SKILL.md

---

## Further Reading

**Internal**: @.claude/skills/close-plan/REFERENCE.md - Full implementation details, worktree cleanup, git push system | @.claude/skills/git-operations/SKILL.md - Git push retry system | @.claude/skills/git-master/SKILL.md - Version control workflow | @.claude/skills/three-tier-docs/SKILL.md - Documentation synchronization | @.claude/skills/using-git-worktrees/SKILL.md - Worktree management

**External**: [Conventional Commits](https://www.conventionalcommits.org/) | [GitHub CLI](https://cli.github.com/manual/gh_pr_create)
