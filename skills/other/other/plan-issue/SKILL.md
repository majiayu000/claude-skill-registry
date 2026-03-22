---
name: plan-issue
description: Explore the codebase and produce an implementation plan for a GitHub issue
argument-hint: <issue-number>
allowed-tools: Bash(gh *)
---

## Plan Implementation for GitHub Issue #$ARGUMENTS

Produce a detailed, approvable implementation plan before writing any code.

---

### Step 1: Read the issue and announce work started

```bash
gh issue view $ARGUMENTS
```

Extract:
- Goal / user-facing behaviour
- Explicit requirements and acceptance criteria
- Any referenced files, classes, or issues

Then post a comment to announce work has started:
```bash
gh issue comment $ARGUMENTS --body "🔧 **Work started** — exploring the codebase and drafting an implementation plan."
```

---

### Step 2: Explore the codebase

Use Glob and Grep (or the Explore agent for broad searches) to locate:

1. **Files to create** — identify the right package and naming convention by finding similar classes
2. **Files to modify** — find every call site or injection point that needs updating
3. **Tests to create/update** — find the existing test class for each file being modified
4. **Relevant patterns** — read 1–2 existing similar classes to match structure (imports, annotations, error handling)

Key places to always check:
- `jhelm-core/src/main/java/org/alexmond/jhelm/core/` — action classes, models, interfaces
- `jhelm-kube/src/main/java/` — Kubernetes client implementation
- `jhelm-app/src/main/java/` — CLI commands (Picocli)
- Matching test directories for each module

---

### Step 3: Write the plan

Write the plan to `/tmp/plan-$ARGUMENTS.md` using this structure:

```markdown
# Plan: <Issue Title> (Issue #$ARGUMENTS)

## Context
<2–3 sentences on what currently exists and what is missing>

## Files to Create
### 1. `path/to/NewClass.java`
- Purpose and key methods
- Important implementation notes

## Files to Modify
### N. `path/to/ExistingClass.java`
- What changes and why
- Code sketch if helpful

## Test Files to Create/Update
### N+1. `path/to/NewClassTest.java`
- Test cases to cover (success, error, edge cases)

## Verification
```bash
./mvnw test -pl <module>
./mvnw install
./mvnw spring-javaformat:apply && ./mvnw validate
```
```

Be specific: include exact class names, method signatures, and field types.
Flag any ambiguities or decisions that need the user's input before proceeding.

---

### Step 4: Post the plan as an issue comment

Post the plan contents to the issue so it's tracked on GitHub:
```bash
gh issue comment $ARGUMENTS --body "$(cat /tmp/plan-$ARGUMENTS.md)"
```

---

### Step 5: Present and seek approval

Call `ExitPlanMode` to show the plan to the user for approval.

**Do not write any production or test code until the plan is approved.**

After approval, implement following the plan exactly, running `/precommit` between
meaningful checkpoints.
