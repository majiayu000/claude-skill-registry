---
name: task-completer
description: "Use when finishing a task - moves task to completed/, updates project_state.md, suggests next task. Trigger: 'finish task', 'done with task', 'move to completed'. MUST run ALL 5 quality gates. BLOCK completion if gates fail. Never skip gates."
version: 2.1.0
---

# Task Completer

Finalize tasks and update project memory.

## Required References

**Load before completing any task:**

| Reference | Enforces |
|-----------|----------|
| `references/quality-gates.md` | Gates 2, 3, 4 (must ALL pass) |
| dev-guides: https://camoa.github.io/dev-guides/drupal/security/ | Gate 4 security review |

## Activation

Activate when you detect:
- `/drupal-dev-framework:complete` command
- "Done with X task" or "Task complete"
- "Finish this task"
- All acceptance criteria appear met

## Gate Enforcement

**Task CANNOT be completed until ALL gates pass:**

| Gate | Check | Blocking? |
|------|-------|-----------|
| Gate 1 | Code standards (invoke `code-pattern-checker`) | YES |
| Gate 2 | Tests pass (user confirms) | YES |
| Gate 3 | Architecture compliance | YES |
| Gate 4 | Security review | YES |

## Workflow

### 1. Verify Completion

Use `Read` on the task file: `{project_path}/implementation_process/in_progress/{task}.md`

Check each acceptance criterion. Ask user:
```
Completion checklist for {task_name}:

Acceptance Criteria:
- [ ] {criterion 1} - Is this done?
- [ ] {criterion 2} - Is this done?
- [ ] {criterion 3} - Is this done?

Confirm all acceptance criteria are met (yes/no):
```

If NO, identify what's remaining and continue working.

### 2. Run Quality Gates (references/quality-gates.md)

**ALL gates must pass before completion:**

#### Gate 1: Code Standards
Invoke `code-pattern-checker` skill on modified files.
- [ ] PHPCS passes
- [ ] PHPStan passes (if configured)
- [ ] No `\Drupal::service()` in new code

#### Gate 2: Tests Pass
Ask user to confirm:
```
Tests verification (user must run):
  ddev phpunit {test_path}

- [ ] All existing tests pass?
- [ ] New code has test coverage?
- [ ] No skipped tests without documented reason?

Confirm tests pass (yes/no):
```

#### Gate 3: Architecture Compliance
Check against architecture/main.md:
- [ ] SOLID principles followed (references/solid-drupal.md)
- [ ] DRY - no code duplication (references/dry-patterns.md)
- [ ] Library-First pattern used (references/library-first.md)

#### Gate 4: Security — WebFetch `https://camoa.github.io/dev-guides/drupal/security/` for detailed security guidance
- [ ] Input validated via Form API
- [ ] Output escaped properly
- [ ] No raw SQL with user input
- [ ] Access checks on all routes

**If ANY blocking gate fails:** Task completion is BLOCKED. Fix issues first.

### 3. Update Task File

Use `Edit` to add completion section to the task file:

```markdown
---

## Completion

**Completed:** {YYYY-MM-DD}
**Final Status:** Complete

### Summary
{Brief description of what was implemented}

### Files Changed
| File | Action |
|------|--------|
| src/... | Created |
| tests/... | Created |
| *.services.yml | Modified |

### Test Results
- Unit tests: {count} passing
- Kernel tests: {count} passing
- Total: All passing

### Notes
{Any implementation notes, deviations, or decisions made}
```

### 4. Move Task File

Use `Bash` to move the task:
```bash
mv "{project_path}/implementation_process/in_progress/{task}.md" "{project_path}/implementation_process/completed/{task}.md"
```

### 5. Update project_state.md

Use `Edit` to update:

```markdown
## Progress

### Completed Tasks
| Task | Completed | Notes |
|------|-----------|-------|
| {task_name} | {date} | {one-line summary} |

## Current Focus
{Update to next task or "Ready for next component"}
```

### 6. Suggest Next Task

Use `Glob` to find remaining tasks:
```
{project_path}/implementation_process/in_progress/*.md
```

Analyze dependencies and priorities. Present:
```
Task complete: {task_name}

Next task options:
1. {next_task} - {reason: dependency unblocked / priority}
2. {alternative} - {reason}
3. No more tasks - component complete

Which task next? (1/2/3 or other):
```

### 7. Invoke Verification

If this was the last task for a component, suggest:
```
Component {name} appears complete.

Run final validation?
- superpowers:verification-before-completion
- Full test suite
- Integration tests

Proceed? (yes/no)
```

## Stop Points

STOP and wait for user:
- After showing completion checklist (confirm all done)
- If code-pattern-checker finds issues
- After suggesting next task (let user choose)
- Before running verification
