---
name: feature-plan
description: Generate EXECUTION_PLAN.md and AGENTS_ADDITIONS.md for a feature. Use after /feature-technical-spec to create the task breakdown.
argument-hint: <feature-name>
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion, Glob, Grep
---

Generate the execution plan and agent additions for the feature `$1`.

## Workflow

Copy this checklist and track progress:

```
Feature Plan Progress:
- [ ] Directory guard
- [ ] Handle arguments (feature name)
- [ ] Check prerequisites (FEATURE_SPEC.md + FEATURE_TECHNICAL_SPEC.md)
- [ ] Existing file guard (prevent overwrite)
- [ ] Generate EXECUTION_PLAN.md and AGENTS_ADDITIONS.md
- [ ] Verify execution skills installed
- [ ] Codex CLI detection and skill install
- [ ] Run spec-verification
- [ ] Run criteria audit
- [ ] Cross-model review (if Codex available)
```

## Directory Guard

1. If `START_PROMPTS.md` or `GENERATOR_PROMPT.md` exists in the current working directory → **STOP**:
   "You're in the toolkit repo. Feature skills run from your project directory.
    Run: `cd ~/Projects/your-project && /feature-plan $1`"

2. Check `.claude/toolkit-version.json` exists in the current working directory (confirms `/setup` was run).
   If missing → **STOP**: "Toolkit not installed. Run `/setup` from the toolkit first."

3. Check `AGENTS.md` exists in the current working directory (confirms project root).
   If missing → **STOP**: "Run this from your project root (where AGENTS.md lives)."

## Arguments

- `$1` = feature name (e.g., `analytics`, `dark-mode`)
- If `$1` is empty, ask the user for the feature name
- `PROJECT_ROOT` = current working directory
- `FEATURE_DIR` = `PROJECT_ROOT/features/$1`

## Prerequisites

- Check that `FEATURE_DIR/FEATURE_SPEC.md` exists. If not:
  "FEATURE_SPEC.md not found at features/$1/. Run `/feature-spec $1` first."
- Check that `FEATURE_DIR/FEATURE_TECHNICAL_SPEC.md` exists. If not:
  "FEATURE_TECHNICAL_SPEC.md not found at features/$1/. Run `/feature-technical-spec $1` first."
- Check that `PROJECT_ROOT/AGENTS.md` exists. If not:
  "AGENTS.md not found. Feature development requires an existing AGENTS.md."

## Existing File Guard (Prevent Overwrite)

Before generating anything, check whether either output file already exists:
- `FEATURE_DIR/EXECUTION_PLAN.md`
- `FEATURE_DIR/AGENTS_ADDITIONS.md`

- If neither exists: continue normally.
- If one or both exist: **STOP** and ask the user what to do for the existing file(s):
  1. **Backup then overwrite (recommended)**: for each existing file, read it and write it to `{path}.bak.YYYYMMDD-HHMMSS`, then write the new document(s) to the original path(s)
  2. **Overwrite**: replace the existing file(s) with the new document(s)
  3. **Abort**: do not write anything; suggest they rename/move the existing file(s) first

## Process

Read `.claude/skills/feature-plan/PROMPT.md` and follow its instructions exactly:

1. Read `FEATURE_DIR/FEATURE_SPEC.md` and `FEATURE_DIR/FEATURE_TECHNICAL_SPEC.md` as inputs
2. Read existing `PROJECT_ROOT/AGENTS.md` to understand current conventions
3. Generate EXECUTION_PLAN.md with phases, steps, and tasks for the feature
4. Generate AGENTS_ADDITIONS.md with any additional workflow guidelines

## Output

Write both documents to the feature directory:
- `FEATURE_DIR/EXECUTION_PLAN.md`
- `FEATURE_DIR/AGENTS_ADDITIONS.md`

## Verify Execution Skills

After writing the documents, verify the execution skills are available so `/fresh-start`, `/phase-start`, etc. work from the feature directory.

Check if `.claude/skills/fresh-start/SKILL.md` exists in PROJECT_ROOT:
- If it exists: good — execution skills are installed
- If it does not exist: **STOP** and tell the user:
  "Execution skills are missing. Run `/setup` from the toolkit to install them."

## Codex CLI Detection (Always Runs)

Check if OpenAI Codex CLI is installed:
```bash
command -v codex >/dev/null 2>&1
```

If Codex is NOT detected: skip silently.

If Codex IS detected:

1. **Check for new skills** by comparing toolkit skills to installed skills:
   ```bash
   # Get installed skills
   INSTALLED_SKILLS=$(ls ~/.codex/skills/ 2>/dev/null | grep -v '^\.')
   ```

2. **If no installed skills exist** (first time), use AskUserQuestion:
   ```
   Question: "Codex CLI detected. Install toolkit skills for Codex?"
   Options:
     - "Yes, install" — Install skills via symlink (auto-updates with toolkit)
     - "No, skip" — Don't install Codex skills
   ```

3. **If user selects install**, resolve toolkit location from `.claude/toolkit-version.json`:
   ```bash
   TOOLKIT_PATH=$(jq -r '.toolkit_location' .claude/toolkit-version.json)
   "$TOOLKIT_PATH/scripts/install-codex-skill-pack.sh" --method symlink
   ```

4. Report installation result.

## Verification (Automatic)

After writing EXECUTION_PLAN.md, run the spec-verification workflow:

1. Read `.claude/skills/spec-verification/SKILL.md` for the verification process
2. Verify context preservation: Check that all key items from FEATURE_TECHNICAL_SPEC.md and FEATURE_SPEC.md appear as tasks or acceptance criteria
3. Run quality checks for untestable criteria, missing dependencies, vague language, regression coverage
4. Present any CRITICAL issues to the user with resolution options
5. Apply fixes based on user choices
6. Re-verify until clean or max iterations reached

**IMPORTANT**: Do not proceed to "Next Step" until verification passes or user explicitly chooses to proceed with noted issues.

## Criteria Audit

Run `/criteria-audit FEATURE_DIR` to validate verification metadata in EXECUTION_PLAN.md.
This passes the feature directory so criteria-audit reads `features/$1/EXECUTION_PLAN.md`
instead of looking in the project root.

- If FAIL: stop and ask the user to resolve missing metadata before proceeding.
- If WARN: report and continue.

## Cross-Model Review (Automatic)

After verification passes, run cross-model review if Codex CLI is available:

1. Check if Codex CLI is installed: `codex --version`
2. If available, run `/codex-consult` with upstream context
3. Present any findings to the user before proceeding

**Consultation invocation:**
```
/codex-consult --upstream features/$1/FEATURE_TECHNICAL_SPEC.md --research "execution planning, task breakdown" features/$1/EXECUTION_PLAN.md
```

**If Codex finds issues:**
- Show critical issues and recommendations
- Ask user: "Address findings before proceeding?" (Yes/No)
- If Yes: Apply suggested fixes
- If No: Continue with noted issues

**If Codex unavailable:** Skip silently and proceed to Next Step.

## Next Step

When verification is complete, inform the user:
```
EXECUTION_PLAN.md and AGENTS_ADDITIONS.md created and verified at features/$1/

Verification: PASSED | PASSED WITH NOTES | NEEDS REVIEW
Cross-Model Review: PASSED | PASSED WITH NOTES | SKIPPED

Next steps:
1. /fresh-start  (will offer to merge AGENTS_ADDITIONS.md if needed)
2. /configure-verification
3. /phase-prep 1
4. /phase-start 1
```
