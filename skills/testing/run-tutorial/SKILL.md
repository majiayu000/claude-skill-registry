---
name: Run Tutorial Walkthrough
description: Walk through a training tutorial as a user would, progressively building examples exactly as instructed, running all commands, and verifying results against solutions. Use when testing tutorials end-to-end or validating that instructions are correct and complete.
---

# Run Tutorial Walkthrough

Walk through a training tutorial lesson as a learner would, progressively building code, running commands, and verifying the learning journey works end-to-end.

---

## Skill Dependencies (MANDATORY)

This walkthrough MUST invoke other skills. **Do not skip these.**

| Checkpoint | Skill | Condition |
|------------|-------|-----------|
| Before Phase 2 | `/docker-setup` | If Docker environment selected |
| Before Phase 2 | `/validate` | Always - check lesson structure first |
| Phase 3 | `/test-example` | For each solution file |

---

## Initial Setup

Use `AskUserQuestion` to determine:

1. **Which tutorial/lesson** to walk through (specific file, module, or side quest)
2. **Environment**: Docker (recommended) or existing local environment

### Environment Setup

**If Docker selected:**

```
>>> STOP. INVOKE /docker-setup NOW.

Do not proceed until the container is confirmed running.
```

**If existing environment:** Verify Nextflow is installed with `nextflow -version`

### Strict Syntax Parser (v2)

**Always use the strict syntax parser** when running Nextflow commands:

```bash
NXF_SYNTAX_PARSER=v2 nextflow run ...
```

In Docker:

```bash
docker exec -e NXF_SYNTAX_PARSER=v2 nf-training nextflow run ...
```

This validates tutorials against the strict syntax that will become default in future Nextflow versions.

---

## Working Directory Mapping

See [../shared/repo-conventions.md](../shared/repo-conventions.md) for full directory mapping table.

Key pattern: documentation uses underscores (`hello_nextflow`), working directories use hyphens (`hello-nextflow`).

---

## Walkthrough Process

Use `TodoWrite` to track progress through phases and sections.

### Phase 1: Preparation

1. **Read the lesson file** to understand the structure and sections
2. **Identify starting files** - What files should already exist vs. what the user creates
3. **Prepare a clean working state** - Reset or backup existing files to avoid conflicts
4. **Verify prerequisites** - Check that required data files and configs exist

#### CHECKPOINT: Validate Before Proceeding

```
>>> STOP. INVOKE /validate on the lesson file NOW.

Record any issues found. Do not proceed to Phase 2 until validation completes.
```

### Phase 2: Progressive Execution (Core Unique Value)

**CRITICAL**: Complete ALL steps (2.1-2.6) for EACH section before moving to the next section. Do NOT batch multiple sections together. The entire point of this skill is to catch issues that only appear when following the tutorial step-by-step.

For each numbered section in the lesson (0, 1, 2, 3...):

#### 2.1 Read and Understand

- Read the section instructions
- Identify what code changes are expected (Before/After blocks, inline snippets)
- Note what commands should be run

#### 2.2 Verify Current State Matches "Before"

**This is the key unique check**: Before applying any code change:

1. Read the current file content using the `Read` tool
2. Compare with the "Before" block in the documentation
3. If they don't match, **STOP and report the discrepancy**
   - This catches issues where earlier steps didn't work correctly
   - This catches documentation that skipped steps

#### 2.3 Apply Code Changes Progressively

- **Don't copy the final solution** - Apply only the changes shown in this section
- Use the `Edit` tool to make incremental changes, mimicking how a learner would type
- If creating a new file, use the exact content shown at that point (not the final version)

#### 2.4 Run Commands Exactly As Shown

- Execute bash commands in the order they appear using the `Bash` tool
- Use the exact syntax shown (don't "improve" or modify commands)
- Capture output for comparison
- **If a section changes code but doesn't include a "run this" instruction, run the workflow anyway** to verify changes work

#### 2.5 Verify Outputs

- Compare console output with documented "Output" blocks
- See [references/acceptable-differences.md](references/acceptable-differences.md) for what to flag vs. ignore

#### 2.6 Confirm Section Complete Before Proceeding

**MANDATORY**: Before moving to the next section:

1. Verify the workflow/script ran successfully (exit code 0)
2. Confirm output matches documentation (within acceptable differences)
3. Update `TodoWrite` to mark section complete
4. Only then proceed to section N+1

**Why this matters**: Skipping incremental testing defeats the purpose of this skill. A tutorial might work when you jump to the final solution but fail at intermediate steps - exactly the bugs learners encounter.

### Phase 3: Final Verification

After completing all sections:

#### 3.1 Compare Final Code with Solutions

Read the solution file and compare with what was built. Minor differences (whitespace, comments) may be acceptable. Report any significant differences.

#### 3.2 Test Solution Files

```
>>> STOP. INVOKE /test-example on each solution file.

For each solution script, verify:
- Fresh run works
- Resume caches correctly
- Parameter handling (if applicable)
- Output matches documentation

Record results before proceeding.
```

#### 3.3 Cleanup

**Only if walkthrough succeeded with no issues:**

- Reset modified files: `git checkout "${WORKING_DIR}/"`
- Remove work directories and logs

**If issues found:** Leave files in place for Phase 4. Save work directory paths for troubleshooting.

### Phase 4: Propose Fixes and Create PR (if issues found)

If fixable issues were identified, follow [references/pr-workflow.md](references/pr-workflow.md) to create a PR.

Key points:
- Categorize as auto-fixable vs. requires review
- Present fixes to user with **actual section headings** (read from document - do not guess!)
- Get user approval via `AskUserQuestion` before making changes

---

## Output Format

Structure your report with these sections:

```
# Tutorial Walkthrough: <lesson-name>

## Environment
Mode, Nextflow version, working directory

## Section N: <exact title from document>
- State verification: matches "Before" ✓ or mismatch details
- Code changes applied
- Commands run with results

## Validation Results (from /validate)
## Solution Tests (from /test-example)
## Solution Comparison

## Summary
Sections completed, mismatches, failures, discrepancies

## Issues Found
Categorize as Critical / Warning / Minor

## Proposed Fixes (if any)
Table with file, line, current, proposed, reason
```

**IMPORTANT**: Always read actual section headings from the document. Do not guess.

---

## Special Cases

### Exercises

When encountering `??? exercise` blocks:

1. Attempt the exercise based on instructions given
2. Check against `??? solution` block
3. Report if instructions are unclear or incomplete

### Branching/Optional Steps

Some tutorials have optional paths:

- Note which path was taken
- Ask user if they want to test alternative paths
- Document any untested branches
