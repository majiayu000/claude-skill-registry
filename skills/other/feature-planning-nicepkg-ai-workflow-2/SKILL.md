---
name: feature-planning
description: Use after research (Z01 files exist) to create implementation plan - follow structured workflow
---

# Feature Workflow: Plan Implementation

## YOU ARE READING THIS SKILL RIGHT NOW

**STOP. Before doing ANYTHING else:**

1. ☐ Create TodoWrite checklist (see below)
2. ☐ Mark Step 1 as `in_progress`
3. ☐ Read CLAUDE.md first (if exists)

**This skill is a WRAPPER that loads Z01 context and invokes superpowers:writing-plans**

## MANDATORY FIRST ACTION: Create TodoWrite

```typescript
TodoWrite({
  todos: [
    {content: "Step 1: Load project context (CLAUDE.md if exists)", status: "in_progress", activeForm: "Reading CLAUDE.md"},
    {content: "Step 2: Verify Z01 files exist", status: "pending", activeForm: "Checking research"},
    {content: "Step 3: Read ALL Z01 files", status: "pending", activeForm: "Loading context"},
    {content: "Step 4: Invoke superpowers:writing-plans", status: "pending", activeForm: "Creating plan"},
    {content: "Step 5: Verify Z02 outputs", status: "pending", activeForm: "Validating output"}
  ]
})
```

**After each step:** Mark completed, move `in_progress` to next step.

## Why Use This Wrapper?

- Automates Z01 → Z02 file management
- Loads CLAUDE.md constraints into planning context
- Enforces feature-workflow naming conventions (Z02_{feature}_plan.md)
- Integrates with clarification workflow (Z02_CLARIFY)
- Maintains consistent file structure

**Without this wrapper:** You'd manually load Z01 files, pass to superpowers:writing-plans, manage Z02 output paths, check for clarifications.

## Workflow Steps

### Step 1: Load Project Context (MANDATORY FIRST)

**Read CLAUDE.md if it exists.**

Extract from CLAUDE.md (if exists):
- Mandatory patterns that MUST be preserved
- Forbidden approaches to AVOID
- Project conventions (naming, structure, etc.)
- Release workflows and constraints

**CRITICAL:** If CLAUDE.md exists and contains constraints, these MUST be passed to superpowers:writing-plans so the plan preserves project standards.

---

### Step 2: Verify Z01 Files Exist

Scan for existing Z01 files in common locations (docs/ai/ongoing, .ai/ongoing, docs/ongoing).

**If Z01 files found:**
- Note the ONGOING_DIR location
- Extract feature name from filename (e.g., Z01_metrics_research.md → "metrics")
- Feature name should already be sanitized snake_case from feature-research

**If NO Z01 files found:**
- Ask user if they want to run feature-workflow:feature-researching first
- Or proceed without research context (suboptimal)

---

### Step 3: Read ALL Z01 Files

Read all Z01 files in ONGOING_DIR:
- Z01_{feature}_research.md (required)
- Z01_CLARIFY_{feature}_research.md (if exists)

**BLOCKING CHECK - If Z01_CLARIFY exists:**
- Read the file
- Check if "User response:" fields are empty
- **If ANY empty → STOP, report:** "Cannot plan with unanswered questions. Please answer all questions in Z01_CLARIFY_{feature}_research.md first."
- If all answered → proceed

Extract:
- Technical research and integration points
- File paths and line ranges
- Answered clarifications
- Security and test requirements

---

### Step 4: Invoke Superpowers Planning

**CRITICAL**: This skill's primary job is to invoke superpowers:writing-plans with Z01 context. If you skip this invocation, the skill provides no value.

**Use Skill tool** to invoke `superpowers:writing-plans`

Provide this instruction:

"Create an implementation plan for the {feature} feature based on the research in Z01_{feature}_research.md and clarifications in Z01_CLARIFY_{feature}_research.md.

**MANDATORY CONSTRAINTS from CLAUDE.md:**
[Include any constraints, patterns, or forbidden approaches from CLAUDE.md here if it exists]

CRITICAL: Save the plan to {ONGOING_DIR}/Z02_{feature}_plan.md (use the detected path, NOT hardcoded docs/plans/).

The plan should be a DIRECTIVE document with:
- Exact file paths from research
- Complete code examples
- Verification steps for each task
- TDD structure (test-fail-implement-pass-commit)
- Assumes engineer has minimal domain knowledge

If you discover NEW blocking questions during planning (not already in Z01_CLARIFY), create {ONGOING_DIR}/Z02_CLARIFY_{feature}_plan.md. Otherwise, do NOT create a Z02_CLARIFY file.

**When incorporating answered questions:** Delete fully-answered CLARIFY files or remove incorporated Q&A pairs if only some were answered."

---

### Step 5: Verify Outputs

When superpowers:writing-plans completes:

**Check structure:**
- Z02_{feature}_plan.md must exist in ONGOING_DIR (main directive plan)
- Z02_CLARIFY_{feature}_plan.md only if NEW questions exist

**Report to user:**
- "Plan created: Z02_{feature}_plan.md"
- If clarifications: "Blocking questions in Z02_CLARIFY_{feature}_plan.md"
- Next step: "Review clarifications, then use feature-workflow:feature-implementing"

---

## Red Flags - You're Failing If:

- **Proceeded with unanswered questions in Z01_CLARIFY** (BLOCKING - must stop)
- **Did NOT read CLAUDE.md first** (if exists)
- **CLAUDE.md exists but constraints not passed to planning**
- **Did NOT check for Z01* files**
- **Directly invoked superpowers:writing-plans without loading Z01 context**
- **Creating plan files with non-standard names** (not Z02_{feature}_plan.md)
- **Saving plans to wrong directory**
- **Used SlashCommand `/superpowers:write-plan`** (use Skill tool)
- **Did NOT explicitly specify output path** in prompt to writing-plans
- **Skipped reading Z01_CLARIFY** (if exists)
- **Using hardcoded paths** (detect pattern instead)

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| **"Skip path detection, I know it's docs/ai/ongoing"** | **NO.** Path assumptions break in non-standard repos. Detect ONGOING_DIR. |
| **"No Z01 files, skip check"** | **NO.** Research context critical for quality plans. Check first. |
| **"Superpowers will figure out output structure"** | **NO.** Generic plans lack our research integration. Provide explicit Z02* instruction. |
| **"Read only Z01_research, skip Z01_CLARIFY"** | **NO.** Missing context = incomplete plan. Read ALL Z01* files. |
| **"Create Z02_CLARIFY even if no questions"** | **NO.** Empty files clutter directory. Only create if NEW questions. |
| **"Just invoke superpowers:writing-plans directly"** | **NO.** This wrapper loads Z01 context. That's its value. |
| "Wrapper skill, no need to track steps" | **NO.** Wrapper has critical steps (context loading, invocation). Track with TodoWrite. |
| "TodoWrite adds overhead, skip it" | **NO.** TodoWrite provides user visibility and prevents skipped steps. MANDATORY. |

## Success Criteria

You followed the workflow if:
- ✓ Read CLAUDE.md if exists
- ✓ Passed CLAUDE.md constraints to superpowers:writing-plans
- ✓ Checked for Z01* files
- ✓ Read ALL Z01* files if they exist
- ✓ Invoked superpowers:writing-plans skill (NOT slash command)
- ✓ Explicitly instructed output path in prompt
- ✓ Verified Z02_{feature}_plan.md was created
- ✓ Reported next steps to user

## When to Use

**Workflow Position:** AFTER feature-research (Z01 files), BEFORE feature-implement

Use when:
- Z01 research files exist
- Need to create implementation plan
- Want automated Z01 → Z02 workflow

**Don't use when:**
- No Z01 files exist → Use feature-research first
- Already have complete plan
- Simple single-step tasks
