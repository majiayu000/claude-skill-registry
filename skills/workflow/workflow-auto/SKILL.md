---
name: workflow-auto
description: Execute workflow-analyze → workflow-plan → workflow-execute → commit in sequence without intermediate approval (single commit). Use for small tasks that can be completed in one commit.
disable-model-invocation: true
---

# Auto Workflow Command

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

---

## Overview

This command executes the full workflow (analyze → plan → execute → commit) **in sequence without stopping for approval**.

**Key differences from individual commands**:

- No intermediate approval between phases
- Plan is limited to **single commit** (no commit splitting)
- Automatically generates commit message at the end
- All other processes follow the original commands exactly

**When to use**:

- Tasks that can be completed in one commit
- When you want to skip manual phase transitions

**When NOT to use**:

- Complex features requiring multiple commits → Use individual commands
- Tasks needing validation → Use `/workflow-validate`
- Tasks where you want to review analysis/plan before execution

---

## Execution Flow

### Phase 1: Analyze

Execute **exactly as `/workflow-analyze`** command:

1. Parse user input, generate task name
2. Define problem with concrete scenarios
3. Investigate 2-4 solution approaches
4. Select final approach with rejection reasons
5. Generate clarification questions (max 3)
6. Write documents:
   - `docs/work/WORK-{task-name}/analysis.ko.md`
   - `docs/work/WORK-{task-name}/analysis.md`

**Use the full template from workflow-analyze** (not simplified).

→ **Proceed immediately without approval**

---

### Phase 2: Plan

Execute **exactly as `/workflow-plan`** command, with one constraint:

1. Parse task name from Phase 1
2. Load analysis.md requirements
3. Identify impact scope
4. **Create single commit plan** (no commit splitting)
5. Review principle violations if any
6. Write documents:
   - `docs/work/WORK-{task-name}/plan.ko.md`
   - `docs/work/WORK-{task-name}/plan.md`

**Use the full template from workflow-plan** (not simplified).

**Single commit constraint**: All changes must be planned as one commit with vertical slicing (types + logic + tests together).

→ **Proceed immediately without approval**

---

### Phase 3: Execute

Execute **exactly as `/workflow-execute`** command:

1. Load plan.md checklist
2. Reference analysis.md for context
3. Execute all tasks sequentially
4. Write tests
5. Verify (run tests, check behavior)
6. Generate summary:
   - `docs/work/WORK-{task-name}/summary-commit-1.md`
7. Report completion

**Use the full template from workflow-execute** (not simplified).

→ **Proceed immediately without approval**

---

### Phase 4: Commit Message

Execute **exactly as `/commit`** command:

1. Run git status to check staged/unstaged files
2. Run git diff to analyze changes
3. Check branch name for issue number
4. Generate commit messages in Conventional Commits format
5. Write to `commit_message.md` (Korean and English versions)

**Use the full process from commit command**.

---

## Key Rules

### ✅ Must Do

- Follow each phase's original command exactly
- Use original templates (not simplified versions)
- Execute all three phases without stopping
- Limit plan to single commit
- Follow coding principles strictly

### ❌ Must Not Do

- Simplify or skip any phase steps
- Use custom/shortened templates
- Ask for intermediate approval
- Split into multiple commits

---

## Document Structure

Same as individual commands:

```
docs/work/WORK-{task-name}/
├── analysis.ko.md          (Korean - from workflow-analyze)
├── analysis.md             (English - from workflow-analyze)
├── plan.ko.md              (Korean - from workflow-plan)
├── plan.md                 (English - from workflow-plan)
└── summary-commit-1.md     (Korean - from workflow-execute)

commit_message.md           (from commit - Korean and English versions)
```

---

## Execution

Now execute the full workflow by reading and following each skill:

1. Execute **workflow-analyze** full process
2. Without stopping, execute **workflow-plan** (single commit only)
3. Without stopping, execute **workflow-execute** for commit 1
4. Without stopping, execute **commit** to generate commit_message.md

You MUST follow each skill's exact process and templates.
