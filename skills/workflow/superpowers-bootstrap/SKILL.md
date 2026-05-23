---
name: superpowers-bootstrap
description: Bootstrap skill - Loads Superpowers SDLC workflow into every session
bootstrap_token: e28604705b8e2934
---

# Superpowers Development Workflow

**Every response MUST start with:** `e28604705b8e2934`

This token proves skills are loaded. Missing token = unvalidated response.

---

## The Superpowers SDLC

You have access to a complete software development workflow. **Skills trigger automatically** - you don't need to invoke them manually. The agent checks for relevant skills before any task.

### Phase 1: Brainstorming (Before Writing Code)

**Skill:** `superpowers:brainstorming`

**Triggers automatically when:** Creating features, building components, adding functionality, modifying behavior.

**What happens:**
1. Explore project context (files, docs, commits)
2. Ask questions **one at a time** (prefer multiple choice)
3. Propose 2-3 approaches with trade-offs
4. Present design in 200-300 word sections, validating each
5. Save design to `docs/plans/YYYY-MM-DD-<topic>-design.md`

**Key principle:** YAGNI ruthlessly - remove unnecessary features from all designs.

---

### Phase 2: Workspace Setup

**Skill:** `superpowers:using-git-worktrees`

**Triggers after:** Design approval, before implementation.

**What happens:**
1. Create isolated git worktree (`.worktrees/<branch>`)
2. Verify `.gitignore` is configured
3. Run project setup (`npm install`, `pip install`, etc.)
4. Verify tests pass (clean baseline)

**Key principle:** Never proceed with failing baseline tests.

---

### Phase 3: Planning

**Skill:** `superpowers:writing-plans`

**Triggers when:** You have approved design/spec, before touching code.

**What happens:**
1. Create detailed implementation plan for "an enthusiastic junior engineer with poor taste, no judgement, and no project context"
2. **Bite-sized tasks** (2-5 minutes each):
   - Write failing test
   - Run it to see it fail
   - Write minimal code
   - Run tests to pass
   - Commit
3. Every step has: exact file paths, complete code, exact commands
4. Save to `docs/plans/YYYY-MM-DD-<feature>.md`

**Key principles:** DRY, YAGNI, TDD, frequent commits.

---

### Phase 4: Execution

**Two options offered after planning:**

#### Option A: Subagent-Driven Development (Same Session)
**Skill:** `superpowers:subagent-driven-development`

Per task:
1. Dispatch **implementer subagent** with full task text
2. Subagent asks clarifying questions (if any)
3. Subagent implements, tests, commits, self-reviews
4. Dispatch **spec reviewer** - verifies code matches spec exactly
5. Dispatch **code quality reviewer** - checks implementation quality
6. Loop until both reviews pass
7. Move to next task

**Key:** Fresh subagent per task = no context pollution.

#### Option B: Batch Execution (Parallel Session)
**Skill:** `superpowers:executing-plans`

1. Load plan, review critically
2. Execute in **batches of 3 tasks**
3. Report progress, wait for human feedback
4. Continue until complete

**Key:** Human-in-the-loop between batches.

---

### Phase 5: Test-Driven Development (Throughout)

**Skill:** `superpowers:test-driven-development`

**The Iron Law:**
```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

**Cycle:**
```
RED -> VERIFY RED -> GREEN -> VERIFY GREEN -> REFACTOR -> repeat
```

**Critical rules:**
- Write code before test? **Delete it. Start over.**
- Test passes immediately? You're testing existing behavior. Fix test.
- "I'll write tests after"? Tests passing immediately prove nothing.

---

### Phase 6: Finishing

**Skill:** `superpowers:finishing-a-development-branch`

**Triggers when:** All tasks complete, tests passing.

**What happens:**
1. Verify all tests pass
2. Present 4 options:
   - Merge locally
   - Push and create PR
   - Keep branch as-is
   - Discard work (requires typed confirmation)
3. Execute choice
4. Clean up worktree

---

## Quick Reference Flow

```
User Request
     |
     v
[brainstorming] --> Design Doc
     |
     v
[using-git-worktrees] --> Isolated Workspace
     |
     v
[writing-plans] --> Implementation Plan
     |
     v
[subagent-driven-dev] OR [executing-plans]
     |  (with TDD throughout)
     v
[finishing-a-development-branch] --> Merge/PR/Keep/Discard
```

---

## Supporting Skills

| Skill | When Used |
|-------|-----------|
| `systematic-debugging` | 4-phase root cause process when bugs found |
| `verification-before-completion` | Ensure fix actually works |
| `requesting-code-review` | Pre-review checklist between tasks |
| `receiving-code-review` | Responding to feedback |
| `writing-skills` | Create new skills following best practices |

---

## Philosophy

- **Test-Driven Development** - Write tests first, always
- **Systematic over ad-hoc** - Process over guessing
- **Complexity reduction** - Simplicity as primary goal
- **Evidence over claims** - Verify before declaring success

---

## Slash Commands

- `/superpowers:brainstorm` - Start design refinement
- `/superpowers:write-plan` - Create implementation plan
- `/superpowers:execute-plan` - Execute plan in batches

---

## Red Flags - STOP Immediately

**Never:**
- Skip brainstorming and jump to code
- Write code before failing test
- Proceed with failing baseline tests
- Skip reviews (spec OR quality)
- Guess at fixes without investigation
- Declare "done" without verification

**Always:**
- Check for relevant skills before any task
- Follow the workflow phases in order
- Verify tests pass before AND after changes
- Get explicit approval before major decisions
