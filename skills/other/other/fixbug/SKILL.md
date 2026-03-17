---
name: fixbug
description: Debug and fix bugs with interactive upstream trace-back — diagnoses root cause level, confirms upstream document updates, and applies TDD fixes.
---

# Code Forge — Fixbug

Systematically debug and fix bugs with interactive trace-back to upstream documents (task descriptions, plans, requirements).

## When to Use

- Encountered a bug or unexpected behavior in a feature
- Need to diagnose whether the root cause is in code, task description, plan, or requirements
- Want to fix the bug with TDD and keep upstream documents in sync

## Examples

```bash
/code-forge:fixbug login page returns 500 error    # Diagnose and fix from description
/code-forge:fixbug @issues/bug-123.md              # Fix from bug report file
/code-forge:fixbug --review user-auth              # Batch-fix all issues from review report
/code-forge:fixbug --review                        # Auto-detect review report and fix
```

## Workflow

```
Bug Input → Context Scan → Feature Association → Root Cause Diagnosis → Trace-back Confirmation → TDD Fix → Doc Sync → Summary
```

## Detailed Steps

@../shared/configuration.md

---

### Step 1: Receive Bug Description

Accept input in three modes:

- **Prompt text** (e.g., `/code-forge:fixbug login page returns 500 error`) — use the text as bug description
- **File reference** (e.g., `/code-forge:fixbug @issues/bug-123.md`) — read the file for bug details
- **Review mode** (`/code-forge:fixbug --review [feature-name]`) — read the review report and batch-fix all issues. See [Step 1R](#step-1r-review-mode-setup) below.

#### 1.0 Path-Like Input Guard

**Before treating input as prompt text, check if it looks like a file/directory path without `@`.** If the input does NOT start with `@` and is NOT `--review`, but matches ANY of these patterns, it is likely a path the user forgot to prefix with `@`:

- Contains `/` (e.g., `issues/bug-123.md`, `../bugs/report.md`)
- Starts with `.` (e.g., `./bug-report.md`)
- Ends with `.md` (e.g., `bug-123.md`)
- Matches an existing file or directory on disk

**Action:** Use `AskUserQuestion`:

```
Your input looks like a file path: "{input}"
Did you mean to use file mode? (file paths require an @ prefix)
```

- Options:
  - "Yes, use as file path" → prepend `@` and treat as file reference
  - "No, treat as bug description" → continue as prompt text

---

If no input provided, use `AskUserQuestion` to ask: "Describe the bug you encountered."

For prompt text and file reference modes, store the bug description and continue to Step 2.

For `--review` mode, go to Step 1R.

---

### Step 1R: Review Mode Setup

Locate and parse the review report. The review report lives **in the current conversation context** (displayed by a prior `/code-forge:review` run). A saved file on disk is the fallback.

**Source priority:**

1. **Conversation context (primary):** Look for the most recent review report output in the current conversation. The report starts with `# Code Review:` or `# Project Review:` and contains the structured dimension sections. If found, use it directly.

2. **Saved file (fallback):** Only if no review report exists in the current conversation:
   - With feature name (`--review my-feature`): read `{output_dir}/{feature_name}/review.md`
   - Without feature name (`--review`): search `{output_dir}/project-review.md` first, then scan `{output_dir}/*/review.md`
   - If multiple found: use `AskUserQuestion` to let user select

3. **Neither found:** Show error — "No review report found in this session. Run `/code-forge:review` first, or `/code-forge:review --save` to persist to disk."

4. **Parse issues from the report:**
   - Extract all issues with severity `blocker`, `critical`, and `warning`
   - Skip `suggestion`-level issues (these are optional improvements, not bugs)
   - Group issues by file for efficient fixing
   - Sort by severity: blockers first, then criticals, then warnings

5. **Present issue summary and confirm:**

   Display:
   ```
   Review Report: {feature_name or "project"}

   Found {N} issues to fix:
     Blockers:  {count}
     Criticals: {count}
     Warnings:  {count}

   Issues:
     1. [{severity}] {file}:{line} — {title}
     2. [{severity}] {file}:{line} — {title}
     ...
   ```

   Use `AskUserQuestion`: "Fix all {N} issues? Or enter issue numbers to fix selectively (e.g., `1,3,5`)."

   - **"all" / "yes"** → process all issues
   - **Comma-separated numbers** → process only selected issues
   - **"cancel"** → abort

6. **Batch execution:**

   For each selected issue (or group of issues in the same file):
   - Set the issue's `title + description + suggestion` as the bug description
   - The review already provides `file`, `line`, `description`, and `suggestion` — use these directly as the diagnosis. Only spawn a diagnostic sub-agent (Step 4) if the review's suggestion is vague or the fix is non-obvious.
   - Execute Step 6 (TDD Fix) directly:
     - **6.1** Write a regression test targeting the specific issue
     - **6.2** Implement the fix (use the review's `suggestion` as guidance)
     - **6.3** Run full test suite
     - **6.4** Commit with message: `fix: {issue title} ({file}:{line})`
   - **Skip** Steps 2 (Context Scan), 3 (Feature Association), 5 (Upstream Trace-back), and 7 (Doc Sync) — review issues are code-level (Level 1), and file context is already known from the report.
   - After fixing each issue, display a brief progress line:
     ```
     ✅ [{i}/{N}] Fixed: {title} ({file}:{line})
     ```

7. **Update state.json** (if associated with a feature):

   Add a single aggregated fix record to the `fixes` array:
   ```json
   {
     "bug": "review fixes — {N} issues",
     "root_cause_level": 1,
     "root_cause": "Code-level issues identified by review",
     "fixed_files": ["path/to/file1.ext", "path/to/file2.ext"],
     "commits": ["abc1234", "def5678"],
     "doc_updates": [],
     "fixed_at": "ISO timestamp"
   }
   ```

8. **Display batch summary:**

   ```
   Review Fixes Complete: {feature_name or "project"}

   Fixed: {fixed_count}/{total_count} issues
     Blockers:  {fixed_blockers}/{total_blockers}
     Criticals: {fixed_criticals}/{total_criticals}
     Warnings:  {fixed_warnings}/{total_warnings}

   {If any failed:}
   ⚠ Could not fix:
     - {title} ({file}:{line}) — {reason}

   Commits:
     {commit hashes}

   Next steps:
     /code-forge:review {feature_name}    Re-run review to verify fixes
     /code-forge:status {feature_name}    View updated progress
   ```

**Review mode ends here — do NOT continue to Step 2.**

---

### Step 2: Project Context Scan

Scan the project codebase to understand the context:

1. Use `Glob` to get project structure overview
2. Use `Grep` to search for keywords from the bug description in the codebase
3. Identify files and modules likely related to the bug
4. Note the tech stack and testing framework used

Store a concise context summary (~500 words).

---

### Step 3: Associate Feature (If Exists)

Attempt to associate the bug with an existing code-forge feature:

1. Search **both** `{output_dir}/*/state.json` and `.code-forge/tmp/*/state.json` for all features
2. For each feature, check if the bug-related files overlap with the feature's task files (read `tasks/*.md` → "Files Involved" sections)
3. **Match found** → load the feature's `plan.md` and relevant `tasks/*.md` as additional context. Note the feature name.
4. **No match found** → mark as standalone bug. Skip upstream trace-back (Steps 5 and 7). Proceed with code-only fix.

If multiple features match, use `AskUserQuestion` to let user select the most relevant one.

---

### Step 4: Root Cause Diagnosis

**Offload to sub-agent** for deep analysis.

Spawn an `Agent` tool call with:
- `subagent_type`: `"general-purpose"`
- `description`: `"Diagnose bug root cause"`

**Sub-agent prompt must include:**
- Bug description
- Project context summary from Step 2
- Feature context (plan.md, task files) if associated in Step 3
- Instruction to: reproduce the bug, identify the root cause, classify the root cause level

**Root cause levels:**

| Level | Description | Example |
|-------|------------|---------|
| 1 | Code bug | Logic error, boundary miss, typo, wrong variable |
| 2 | Incomplete task description | Task.md steps missing a case, wrong acceptance criteria |
| 3 | Plan design flaw | Architecture doesn't handle a scenario, missing component |
| 4 | Incomplete requirement doc | Original feature doc missing a requirement |

**Sub-agent must return:**

    ROOT_CAUSE_LEVEL: <1-4>
    ROOT_CAUSE_SUMMARY: <1-2 sentence description>
    AFFECTED_FILES:
    - path/to/file.ext: <what's wrong>
    UPSTREAM_DOCS_AFFECTED: (only if Level >= 2)
    - Level 2: tasks/<task>.md — <what's missing/wrong>
    - Level 3: plan.md — <what's missing/wrong>
    - Level 4: {input_dir}/<feature>.md — <what's missing/wrong>
    PROPOSED_FIX: <brief fix description>
    REGRESSION_TEST: <what test to write>

---

### Step 5: Interactive Trace-back Confirmation

**This step only runs if Level >= 2 AND the bug is associated with a feature.**

Present the root cause analysis to the user, then confirm upstream updates level by level.

#### 5.1 Present Analysis

Display:
```
Root Cause Analysis

Level: {level} — {level_description}
Summary: {root_cause_summary}

Affected code:
  {affected_files list}

Upstream documents affected:
  {upstream_docs_affected list}
```

#### 5.2 Per-Level Confirmation

For each affected upstream level (from lowest to highest), use `AskUserQuestion`:

"Root cause traced to **{level_name}**: `{doc_path}` — {what's wrong}. Update this document?"

Options:
- **"Yes, update this document"** → mark for update in Step 7
- **"No, code fix only"** → skip this level, do not modify this document
- **"Show proposed changes"** → display the proposed diff for this document, then re-ask

#### 5.3 Generate Fix Plan

Compile the fix plan:
- Code changes to make (always)
- Upstream documents to update (based on user confirmations)
- Regression test to write

---

### Step 6: TDD Fix

Execute the fix following TDD methodology:

#### 6.1 Write Regression Test

Write a test that reproduces the bug:
- Test must FAIL with the current code (proving the bug exists)
- Test must describe the expected correct behavior

Run the test to verify it fails.

#### 6.2 Implement Fix

Make the minimal code changes to fix the bug.

Run the regression test to verify it passes.

#### 6.3 Run Full Test Suite

Run the project's full test suite to ensure no regressions:
- If tests pass: continue
- If tests fail: investigate and fix before proceeding

#### 6.4 Commit Fix

Commit the code changes with a descriptive message:
```
fix: {brief description of bug fix}
```

---

### Step 7: Upstream Document Sync

**This step only runs if upstream documents were confirmed for update in Step 5.**

For each confirmed document update:

#### 7.1 Show Diff Preview

Before modifying each document, show the proposed changes in diff format:
```
--- a/{doc_path}
+++ b/{doc_path}
@@ ... @@
- old content
+ new content
```

Ask user: "Apply this change?" (Yes / No / Edit manually)

#### 7.2 Apply Changes

- **Level 2** (task.md): Update the task's steps, acceptance criteria, or files involved
- **Level 3** (plan.md): Update architecture, task breakdown, or risk sections
- **Level 4** (feature doc): Update requirements or scope

#### 7.3 Commit Document Updates

Commit upstream document changes separately from code fix:
```
docs: update {doc_path} — traced from bug fix
```

---

### Step 8: Update state.json

If the bug is associated with a feature:

1. Read the feature's `state.json`
2. Add a `fixes` array (if not present) to the feature-level metadata
3. Append a fix record:
   ```json
   {
     "bug": "brief bug description",
     "root_cause_level": 2,
     "root_cause": "brief root cause",
     "fixed_files": ["path/to/file.ext"],
     "commits": ["abc1234"],
     "doc_updates": ["tasks/auth-logic.md"],
     "fixed_at": "ISO timestamp"
   }
   ```
4. Update `state.json` `updated` timestamp

If standalone bug (no associated feature): skip this step.

---

### Step 9: Summary

Display fix summary:

```
Bug Fix Complete

Bug: {description}
Root Cause: Level {level} — {summary}

Code Changes:
  {files changed}

Regression Test:
  {test file and name}

Document Updates:
  {list of updated docs, or "none"}

Commits:
  {commit hashes}

Next steps:
  /code-forge:status {feature}    View updated progress
  /code-forge:review {feature}    Review all changes
```
