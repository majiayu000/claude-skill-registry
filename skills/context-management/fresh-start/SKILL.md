---
name: fresh-start
description: Orient to project structure and load context. Use at the start of each new session or after context reset to understand the project state.
argument-hint: [project-directory]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

Orient to a project directory and load context for execution.

## Workflow

Copy this checklist and track progress:

```
Fresh Start Progress:
- [ ] Detect context (project root vs feature directory)
- [ ] Directory guard (verify AGENTS.md + EXECUTION_PLAN.md exist)
- [ ] Git initialization (if needed)
- [ ] Feature branch setup (feature mode only)
- [ ] AGENTS_ADDITIONS merge (feature mode only)
- [ ] Read context and summarize
- [ ] Auto-configure verification (first run only)
- [ ] Phase state detection
- [ ] Auto-prep phase (first run only)
- [ ] Branch context detection
```

## Project Directory

Use the current working directory by default.

If `$1` is provided, treat `$1` as the working directory and read files under `$1` instead.

## Context Detection

Determine working context before validation.

**Convention:** For feature work, run all execution commands from the feature directory (`features/<name>/`), not the project root. The skills auto-detect feature mode from the path.

1. Let WORKING_DIR = `$1` if provided, otherwise current working directory

2. If WORKING_DIR matches pattern `*/features/*` (contains `/features/` followed by a feature name):
   - PROJECT_ROOT = parent of parent of WORKING_DIR (e.g., `/project/features/foo` → `/project`)
   - FEATURE_DIR = WORKING_DIR
   - MODE = "feature"

3. Otherwise:
   - PROJECT_ROOT = WORKING_DIR
   - FEATURE_DIR = none
   - MODE = "greenfield"

## Directory Guard (Wrong Directory Check)

Confirm the required files exist:
- `PROJECT_ROOT/AGENTS.md` must exist
- `EXECUTION_PLAN.md` must exist in:
  - FEATURE_DIR (if feature mode)
  - PROJECT_ROOT (if greenfield mode)

- If either is missing:
  - Tell the user this project is not ready for execution yet
  - If they are in the toolkit repo (e.g., `GENERATOR_PROMPT.md` exists), instruct them to:
    1. Run `/generate-plan <project-path>` from the toolkit repo (or `/feature-plan` for features)
    2. `cd` into the project/feature directory
    3. Re-run `/fresh-start`
  - Otherwise, ask the user for the correct project directory path and re-run `/fresh-start <project-path>`

## Git Initialization (First Run)

In PROJECT_ROOT (not the feature directory):

1. Check whether this is already a git repo by running:
   ```bash
   git -C PROJECT_ROOT rev-parse --is-inside-work-tree 2>/dev/null
   ```
   If this returns "true", it's already a git repo.
2. If not a git repo:
   - Ask: "Initialize git in this project now?" (recommended)
   - If yes:
     ```bash
     git init
     git branch -M main
     ```
3. If it is a git repo but has no commits yet:
   - Ask: "Create an initial commit of the current project state now?" (recommended)
   - If yes:
     ```bash
     git add -A
     ```
     Verify with `git status` that files are staged correctly.
     ```bash
     git commit -m "chore: initial commit"
     ```
     Verify with `git log --oneline -1` that the commit was created.

## Feature Branch Setup (Feature Mode Only)

If MODE = "feature", create an isolated branch for this feature work:

1. Derive FEATURE_NAME from the feature directory (basename of FEATURE_DIR, e.g., `analytics-dashboard`)

2. Check current branch:
   ```bash
   git branch --show-current
   ```

3. If already on a `feature/FEATURE_NAME` branch, skip (already set up)

4. Otherwise, create and switch to the feature branch:
   ```bash
   # Commit any uncommitted changes first (preserves user work)
   git add -A && git diff --cached --quiet || git commit -m "wip: uncommitted changes before feature/FEATURE_NAME"
   ```
   Verify with `git status` that files are staged correctly.
   ```bash
   # Create feature branch from current HEAD
   git checkout -b feature/FEATURE_NAME
   ```
   Verify with `git branch` that the new branch is active.

5. Report: "Created branch `feature/FEATURE_NAME` for isolated feature development"

## AGENTS_ADDITIONS Merge (Feature Mode Only)

If MODE = "feature", check for and offer to merge workflow additions:

1. Check if `FEATURE_DIR/AGENTS_ADDITIONS.md` exists
   - If not, skip this section

2. Read AGENTS_ADDITIONS.md and determine if merge is needed:
   - If it contains "No additions required" or similar, report: "No AGENTS.md additions needed for this feature" and skip
   - If it contains actual additions, **validate each section** before presenting:
     - Apply the litmus test: "Would this be useful for a DIFFERENT feature in a DIFFERENT project?"
     - Reject sections that describe specific components, patterns, or architecture of this feature
     - Reject sections that are implementation details or domain knowledge (e.g., "Drawer uses AbortController", "MetricCard drill-down behavior")
     - Only present sections that are genuine workflow/process additions
   - If all sections fail validation, report: "AGENTS_ADDITIONS.md contains feature-specific content, not workflow additions. Skipping." and skip
   - If some sections pass, continue to step 3 with only the valid sections

3. Summarize the additions for the user:
   ```
   AGENTS_ADDITIONS.md proposes workflow additions:

   - {Section Name 1}: {one-line summary of why it's needed}
   - {Section Name 2}: {one-line summary of why it's needed}
   ...
   ```

4. Ask: "Apply these workflow additions to AGENTS.md now? (recommended before starting work)"

5. **Show diff for each section and collect approvals:**

   For each section/block in AGENTS_ADDITIONS.md:
   a. Display the section heading and its content
   b. Show where it would be inserted in AGENTS.md:
      - If a matching heading exists in AGENTS.md → append under that heading
      - If no match → append as a new section at end of AGENTS.md
   c. Ask via AskUserQuestion: "Apply this addition?"
      - Options: "Yes, apply" / "Skip this section" / "Edit first" (let user modify before applying)

   Apply approved sections using Edit tool:
   - Insert under matching heading if one exists, otherwise append as new section
   - Add a comment marker: `<!-- Added for FEATURE_NAME -->`
   - Preserve existing AGENTS.md formatting and structure

   After all sections processed, prepend a header to AGENTS_ADDITIONS.md:
   ```
   <!-- MERGED into PROJECT_ROOT/AGENTS.md on YYYY-MM-DD -->
   <!-- Applied: {list of applied sections} -->
   <!-- Skipped: {list of skipped sections} -->
   ```

   Report: "Applied {N}/{total} workflow additions to AGENTS.md"

6. If user declines all:
   - Report: "Skipped. You can manually apply AGENTS_ADDITIONS.md changes later."
   - Continue with fresh-start (don't block)

## Auto-Configure Verification (First Run Only)

Silently auto-detect verification commands if not already configured.

1. Check if `PROJECT_ROOT/.claude/verification-config.json` exists
2. **Skip this section if ANY of these are true:**
   - File exists and contains real config (has a `commands` key)
   - File exists with only `{"skipped": true}` (user previously opted out)
3. **Run auto-detection if:**
   - File does not exist
   - File is empty

Invoke `/configure-verification` with PROJECT_ROOT. This runs silently with no
prompts and prints a one-line summary. If /configure-verification fails, report the error and continue with manual verification setup.

## Phase State Detection

Check for existing phase state to determine if this is a resume or first run:

1. Check if `.claude/phase-state.json` exists in PROJECT_ROOT (or FEATURE_DIR if feature mode)

2. **If valid phase state exists** (file exists, parses correctly, has `current_phase`):
   - This is a **resume**. Skip auto-configure and auto-prep (already done).
   - Report:
     ```
     RESUMING SESSION
     ================
     Current phase: {current_phase}
     Completed: {count} tasks
     In progress: Task {in_progress_task} (if any)
     Last activity: {relative time, e.g., "2 hours ago"}
     ```
   - If `in_progress_task` exists, offer to continue:
     - "Continue with Task {id}: {task title}?" [Y/n]
     - If yes, jump directly to that task after context load
   - **Do not run auto-prep on resume.** Go straight to Branch Context Detection.

3. **If no phase state exists** (or file is invalid/stale):
   - This is a **first run**. Continue to Auto-Prep Phase section.

## Auto-Prep Phase (First Run Only)

**Skip this section entirely if resuming** (phase-state.json exists and is valid).

After context reading and verification config, automatically prepare the next phase:

1. **Determine next phase number:**
   - If no phase state exists → Phase 1
   - If phase state exists but is stale/invalid → Phase 1

2. **Invoke `/phase-prep {next_phase}`** silently.
   - Phase-prep will verify prerequisites and auto-advance to `/phase-start` if
     all checks pass (via its existing auto-advance logic).
   - If phase-prep blocks (human setup needed), it will report what's needed
     and the user runs `/phase-start` manually after resolving.

## Branch Context Detection

Detect the current git branch and load relevant context:

1. Get current branch:
   ```bash
   git branch --show-current 2>/dev/null
   ```

2. If branch matches `feature/*` pattern:
   - Extract feature name from branch (e.g., `feature/analytics-dashboard` → `analytics-dashboard`)
   - Look for matching feature directory: `PROJECT_ROOT/features/{feature-name}/`
   - If found and MODE is "greenfield", suggest: "Switch to feature mode? Found feature directory for this branch."

3. Summarize recent branch activity:
   ```bash
   git log --oneline -5 2>/dev/null
   ```
   Report: "Recent commits on this branch: {summary}"

4. Check for uncommitted changes:
   ```bash
   git status --porcelain 2>/dev/null
   ```
   If changes exist, report: "Note: {N} uncommitted changes in working tree"

## Required Context

Read these files first:
- **PROJECT_ROOT/AGENTS.md** — Workflow guidelines
- **EXECUTION_PLAN.md** — Tasks and acceptance criteria (from FEATURE_DIR if feature mode, else PROJECT_ROOT)

## Specification Documents

Check which of these exist and read them:

**From PROJECT_ROOT** (always check):
- **PRODUCT_SPEC.md** — What we're building (greenfield)
- **TECHNICAL_SPEC.md** — How it's built (greenfield)
- **LEARNINGS.md** — Discovered patterns and gotchas (if exists)

**From FEATURE_DIR** (if feature mode):
- **FEATURE_SPEC.md** — Feature requirements
- **FEATURE_TECHNICAL_SPEC.md** — Feature technical approach

## Your Task

1. Read all available documents above
2. Summarize your understanding:
   - What is being built
   - Current phase and progress
   - Tech stack and key patterns
   - Key learnings to follow (if LEARNINGS.md exists)
3. Confirm you're ready to begin execution

## Error Handling

| Situation | Action |
|-----------|--------|
| Git init or clone failure | Report the error and stop — cannot proceed without a working repository. |
| AGENTS_ADDITIONS.md merge failure | Report the conflict. Write the unmerged content to a separate file for manual resolution. |
| /phase-prep failure | Report which pre-flight check failed and stop. Do not proceed to execution. |

**Important:** If LEARNINGS.md exists, apply those patterns throughout your work. These are project-specific conventions discovered during development that override general defaults.
