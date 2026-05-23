---
name: workflow-execute
description: Execute commit N from plan.md and generate summary. Use to implement a specific commit from the implementation plan.
disable-model-invocation: true
---

# Issue Execution Command

## User Input

```text
$ARGUMENTS
```

Expected format:

- `/workflow-execute TASK-NAME N` (task name and commit number)
- `/workflow-execute N` (commit number only - searches for most recent plan.md)

Examples:

- `/workflow-execute REFACTORING 1`
- `/workflow-execute API-REDESIGN 2`
- `/workflow-execute 1` (uses most recent plan.md)

---

## Outline

1. **Parse User Input**:
   - If $ARGUMENTS contains two parts (e.g., "REFACTORING 1"):
     - Extract task name from first part (e.g., "REFACTORING")
     - Extract commit number from second part (e.g., 1)
     - Target: `docs/work/WORK-{task-name}/plan.md`
   - If $ARGUMENTS contains only number (e.g., "1"):
     - Extract commit number
     - Find most recently modified `plan.md` in `docs/work/WORK-*/`
     - If not found, ERROR: "No plan.md found. Use: /workflow-execute TASK-NAME N"

2. **Check Prerequisites**:
   - Verify target `plan.md` exists
   - If not, ERROR: "Run /workflow-plan first for WORK-{task-name}"

3. **Load Context**:
   - **Required**: Read checklist for the commit in plan.md
   - **Optional**: Also reference analysis.md for deep context if complex work
   - Check existing summary-commit-N.md (handle revision cycle)

4. **Execute Tasks**:
   - Execute plan.md checklist items sequentially
   - Create/modify files
   - Write tests

5. **Verify**:
   - Run tests
   - Verify behavior

6. **Generate/Overwrite Summary**:
   - Create `docs/work/WORK-{task-name}/summary-commit-N.md`
   - Overwrite if existing file (keep only final state)

7. **Report Completion**:
   - List of changed files
   - Verification results
   - Remaining commit count

---

## Key Rules

### 📝 Documentation Language

**CRITICAL**: All documents you generate (`summary-commit-N.md`) **MUST be written in Korean**.

### ✅ Must Do

- Faithfully follow plan.md checklist
- **Strictly follow** coding principles
- Write tests
- Auto-generate summary

### ❌ Must Not Do

- Ignore checklist
- Violate coding principles (without justification)
- Skip verification

### 🎯 Implementation Rules

- **Setup first**: Initialize project structure, dependencies, configuration
- **Tests before code**: If you need to write tests
- **Core development**: Implement models, services, CLI commands

### 📊 Progress Tracking

- Report progress after each completed task
- Halt execution if any non-parallel task fails
- Provide clear error messages with context for debugging

### 🧪 Prototype Code Usage (if exists)

**IMPORTANT**: If validation code exists in `__prototype__/` directory:

- ✅ **Reference only**: Understand implementation direction and core logic
- ✅ **Rewrite cleanly**: Implement with code quality, structure, and principles
- ❌ **Never copy**: Prototypes were written for validation only (ignoring cleanliness/structure)

**Prototype purpose**: Proof of technical feasibility and core idea verification

---

## Document Template

File to create: `docs/work/WORK-{task-name}/summary-commit-N.md`

```markdown
# Commit N: [Title]

> **Written At**: [YYYY-MM-DD HH:mm]
> **Related Plan**: `plan.md` > Commit N

---

## 🎯 Achievement Goal

[1 sentence]

---

## 📝 Changed Files

**Added**:

- `src/new/file.ts`: [Description]

**Modified**:

- `src/existing.ts:45`: [Changes]

**Deleted** (if any):

- `src/old/file.ts`: [Deletion reason]

## 💡 Core Changes

- [Change 1]
- [Change 2]

---

## ✅ Verification Results

**Test Method**:

- [Test content]

**Test Results**:

- [Results]

## 🧪 Edge Cases (if verified)

- [Case 1]: [Expected behavior]
- [Case 2]: [Expected behavior]

---

## 🔑 Technical Decisions (if any)

- **[Technology/Pattern]**: [Selection reason in 1 line]

---

## ⚠️ Caveats (if any)

- [Constraints]
- [Environment variable added]: `KEY=value`
- [Dependency install]: `npm install package`

## 📌 Follow-up Tasks (if any)

- TODO: [Specific content]
```

---

## Context Loading

### REQUIRED

- Read `plan.md` for the complete task list and execution plan

### IF EXISTS

- Read `analysis.md` for deep context (optional but recommended for complex work)
- Read existing `summary-commit-N.md` to understand if this is a revision
- Check `__prototype__/` directory (reference code created during validation phase)

---

## Execution

Now start the task according to the guidelines above.
