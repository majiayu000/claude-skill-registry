---
name: feature-spec
description: Define feature requirements (problem, users, scope, acceptance criteria) through guided Q&A and write FEATURE_SPEC.md. Use when starting a new feature.
argument-hint: <feature-name>
allowed-tools: Bash, Read, Write, AskUserQuestion
---

Generate a feature specification document for the feature `$1`.

## Workflow

Copy this checklist and track progress:

```
Feature Spec Progress:
- [ ] Directory guard
- [ ] Handle arguments (feature name)
- [ ] Create feature directory
- [ ] Existing file guard (prevent overwrite)
- [ ] Run guided Q&A process (from PROMPT.md)
- [ ] Write FEATURE_SPEC.md
- [ ] Capture deferred requirements
- [ ] Cross-model review (if Codex available)
```

## Directory Guard

1. If `START_PROMPTS.md` or `GENERATOR_PROMPT.md` exists in the current working directory → **STOP**:
   "You're in the toolkit repo. Feature skills run from your project directory.
    Run: `cd ~/Projects/your-project && /feature-spec $1`"

2. Check `.claude/toolkit-version.json` exists in the current working directory (confirms `/setup` was run).
   If missing → **STOP**: "Toolkit not installed. Run `/setup` from the toolkit first."

3. Check `AGENTS.md` exists in the current working directory (confirms project root).
   If missing → **STOP**: "Run this from your project root (where AGENTS.md lives)."

## Arguments

- `$1` = feature name (e.g., `analytics`, `dark-mode`)
- If `$1` is empty, ask the user for the feature name
- `PROJECT_ROOT` = current working directory
- `FEATURE_DIR` = `PROJECT_ROOT/features/$1`

Create `features/$1/` if it doesn't exist:
```bash
mkdir -p "features/$1"
```

## Existing File Guard (Prevent Overwrite)

Before asking any questions, check whether `FEATURE_DIR/FEATURE_SPEC.md` already exists.

- If it does not exist: continue normally.
- If it exists: **STOP** and ask the user what to do:
  1. **Backup then overwrite (recommended)**: read the existing file and write it to `FEATURE_DIR/FEATURE_SPEC.md.bak.YYYYMMDD-HHMMSS`, then write the new document to `FEATURE_DIR/FEATURE_SPEC.md`
  2. **Overwrite**: replace `FEATURE_DIR/FEATURE_SPEC.md` with the new document
  3. **Abort**: do not write anything; suggest they rename/move the existing file first

## Process

Read `.claude/skills/feature-spec/PROMPT.md` and follow its instructions exactly:

1. Ask the user to describe the feature they want to add
2. Work through each question category (Problem, Users, Behavior, Integration, Scope)
3. Make recommendations with confidence levels
4. Generate the final FEATURE_SPEC.md document

## Output

Write the completed specification to `FEATURE_DIR/FEATURE_SPEC.md`.

## Deferred Requirements Capture (During Q&A)

**IMPORTANT:** Capture deferred requirements interactively during the Q&A process, not after.

Write deferred items to `PROJECT_ROOT/DEFERRED.md` (not the feature directory).

### When to Trigger

During the Q&A, watch for signals that the user is deferring something:
- "out of scope"
- "not in this feature" / "separate feature"
- "v2" / "future version"
- "later" / "eventually"
- "follow-up" / "future enhancement"
- "nice to have"
- "we'll skip that for now"

### Capture Flow

When you detect a deferral signal, immediately use AskUserQuestion:

```
Question: "Would you like to save this to your deferred requirements?"
Header: "Defer?"
Options:
  - "Yes, capture it" — I'll ask a few quick questions to document it
  - "No, skip" — Don't record this
```

**If user selects "Yes, capture it":**

Ask these clarifying questions:

1. **What's being deferred?**
   "In one sentence, what's the requirement or feature?"
   (Pre-fill with your understanding from context)

2. **Why defer it?**
   Options: "Out of scope for this feature" / "Separate feature" / "V2" / "Needs more research" / "Other"

3. **Notes for later?**
   "Any context that will help when revisiting this?"
   (Optional — user can skip)

### Write to DEFERRED.md Immediately

After collecting answers, append to `PROJECT_ROOT/DEFERRED.md` right away.

**If file doesn't exist, create it:**

```markdown
# Deferred Requirements

> Captured during specification Q&A. Review when planning future versions.

## From FEATURE_SPEC.md: {FEATURE_NAME} ({date})

| Requirement | Reason | Notes |
|-------------|--------|-------|
| {user's answer} | {selected reason} | {notes or "—"} |
```

**If file exists, add new feature section or append to existing:**

```markdown

## From FEATURE_SPEC.md: {FEATURE_NAME} ({date})

| Requirement | Reason | Notes |
|-------------|--------|-------|
| {user's answer} | {selected reason} | {notes or "—"} |
```

### Continue Q&A

After capturing (or skipping), continue the spec Q&A where you left off.

## Verification (Automatic)

After writing FEATURE_SPEC.md, run quality verification:

1. Invoke `/verify-spec feature-spec` on the generated document
2. This runs **quality checks only** (no upstream context preservation since FEATURE_SPEC.md has no upstream):
   - Q-001: Vague/unmeasurable language ("fast", "user-friendly", "simple")
   - Q-002: Subjective terms without targets ("better", "improved")
   - Q-003: Missing rationale for decisions
   - Q-005: Implicit assumptions
   - Q-006: Conflicting requirements
   - Q-PS-001: Missing user flow (feature mentioned without step-by-step interaction)
   - Q-PS-002: Only happy path described (no edge cases)
   - Q-PS-003: Unbounded scope ("all", "any", "every" without limits)
   - Q-PS-004: Missing non-functional requirements (performance, security, accessibility)
3. Present CRITICAL issues with resolution options (max 2 fix iterations)
4. Do not proceed to cross-model review until verification passes or user explicitly chooses to proceed with noted issues

## Cross-Model Review (Automatic)

After verification, run cross-model review if Codex CLI is available:

1. Check if Codex CLI is installed: `codex --version`
2. If available, run `/codex-consult` on the generated document
3. Present any findings to the user before proceeding

**Consultation invocation:**
```
/codex-consult --research "feature requirements, user stories" features/$1/FEATURE_SPEC.md
```

**If Codex finds issues:**
- Show critical issues and recommendations
- Ask user: "Address findings before proceeding?" (Yes/No)
- If Yes: Apply suggested fixes
- If No: Continue with noted issues

**If Codex unavailable:** Skip silently and proceed to Next Step.

## Next Step

When complete, inform the user:
```
FEATURE_SPEC.md created at features/$1/FEATURE_SPEC.md
Deferred Requirements: {count} items captured to DEFERRED.md
Verification: PASSED | PASSED WITH NOTES | NEEDS REVIEW
Cross-Model Review: PASSED | PASSED WITH NOTES | SKIPPED

Next: Run /feature-technical-spec $1
```
