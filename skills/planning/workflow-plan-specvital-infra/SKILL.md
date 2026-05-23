---
name: workflow-plan
description: Generate implementation plan with commit-level tasks. Use after workflow-analyze to create detailed, vertically-sliced commit plan.
disable-model-invocation: true
---

# Issue Planning Command

## User Input

```text
$ARGUMENTS
```

Expected format: `/workflow-plan TASK-NAME [additional requirements]`

Example:

- `/workflow-plan REFACTORING limit to 3 commits`
- `/workflow-plan API-REDESIGN keep backward compatibility`

You **MUST** consider the user input before proceeding (if not empty).

---

## Outline

1. **Parse User Input**:
   - Extract task name from first word of $ARGUMENTS (e.g., "REFACTORING")
   - Extract additional requirements from remaining text (e.g., "limit to 3 commits")
   - If task name missing, ERROR: "Please provide task name: /workflow-plan TASK-NAME"

2. **Check Prerequisites**:
   - Verify `docs/work/WORK-{task-name}/analysis.md` exists
   - If not exists, use $ARGUMENTS as requirements source and proceed

3. **Load Requirements**:
   - If analysis.md exists: Extract selected approach and completion criteria
   - If not: Interpret user input as requirements (description, URL, file path, etc.)

4. **Identify Impact Scope**:
   - List approximate classes/modules (not specific file names)

5. **Decompose Commits** (Vertical Slicing):
   - Each commit should be independently deployable
   - **Consider additional requirements** from user input (e.g., commit count limits, specific constraints)
   - **Forbid Horizontal Slicing**: Don't separate types/logic/tests/UI into separate commits
   - **Vertical Slicing**: Each commit includes types+logic+tests to provide complete functionality
   - Order: Setup → Core → Integration → Polish
   - Specify verification method and "independently deployable" status for each commit

6. **Review Principle Violations**:
   - Create Complexity Tracking table if coding principle violations are necessary

7. **Write Documents** (Dual Language):
   - Create `docs/work/WORK-{name}/plan.ko.md` (Korean - for user reference)
   - Create `docs/work/WORK-{name}/plan.md` (English - for agent consumption)

---

## Key Rules

### 📝 Documentation Language

**CRITICAL**: You must generate **TWO versions** of all documents:

1. **Korean version** (`plan.ko.md`): For user reference - written in Korean
2. **English version** (`plan.md`): For agent consumption - written in English

**Both versions must contain identical structure and information**, only the language differs.

### ✅ Must Do

- Checklist-focused
- Reference analysis.md only (no repetition)
- **Vertical Slicing**: Each commit independently deployable
- Reflect coding principles
- Impact scope approximate only

### ❌ Must Not Do

- Redefine problem (it's in analysis.md)
- List specific file names
- Verbose explanations

### 🎯 Vertical Slicing Principles (CRITICAL)

**Each commit must satisfy**:

1. **Build Success**: No compilation errors
2. **Preserve Existing Features**: Pass existing tests
3. **Independently Testable**: Can be tested with this commit alone
4. **Meaningful Value**: Provides real value to users/developers

**❌ Horizontal Slicing Forbidden**:

- Separating types only → logic only → tests only → UI only (X)
- This separation makes each commit functionally incomplete

**✅ Vertical Slicing Example**:

- Commit 1: types + logic + tests + schema (usable with manual config)
- Commit 2: UI integration (complete UX)

### 📊 Phase Structure

- **Phase 1**: Setup
- **Phase 2**: Foundational
- **Phase 3+**: User Stories (we call them Core features)
- **Final Phase**: Polish

→ We apply as Commit order

---

## Document Template

Files to create:

- `docs/work/WORK-{task-name}/plan.ko.md` (Korean version)
- `docs/work/WORK-{task-name}/plan.md` (English version)

```markdown
# [Task Name] - Implementation Plan

> **Analysis Result**: See `analysis.md`
> **Selected Approach**: [Approach N]

## 📁 Impact Scope (Approximate)

**Main Areas**: [StatusBarManager, ConfigManager, etc.]

---

## 📝 Commit Plan

### ✅ Commit 1: [Title]

**Goal**: [1 sentence - describe complete value provided by this commit]

**Task Checklist**:

- [ ] [Specific task 1]
- [ ] [Specific task 2]
- [ ] Test: [Test content]
- [ ] Build verification: [Build command]

**Verification Method**:

1. [Specific verification method]
2. [User scenario]

**Independently Deployable**: ✅ / ⚠️ [Reason]

---

### ⬜ Commit 2: [Title]

**Goal**: [1 sentence - describe complete value provided by this commit]

**Task Checklist**:

- [ ] [Specific task 1]
- [ ] [Specific task 2]
- [ ] Test: [Test content]
- [ ] Build verification: [Build command]

**Verification Method**:

1. [Specific verification method]
2. [User scenario]

**Independently Deployable**: ✅ / ⚠️ [Reason]

---

## ⚠️ Principle Violation Justification (Only if needed)

| Violation | Why Necessary                | Why Simple Alternative Rejected |
| --------- | ---------------------------- | ------------------------------- |
| Using any | VS Code API types incomplete | Cost to fix @types > benefit    |

---

## 📊 Progress

- [ ] Commit 1
- [ ] Commit 2
```

---

## Execution

Now start the task according to the guidelines above.
