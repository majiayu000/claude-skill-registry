---
name: session-init
description: Create protocol-compliant JSON session logs with verification-based enforcement. Autonomous operation with auto-incremented session numbers and objective derivation from git state. Use when starting any new session.
version: 1.0.0
license: MIT
model: claude-sonnet-4-5
metadata:
  domains:
    - session-protocol
    - compliance
    - automation
  type: initialization
---

# Session Init

Create protocol-compliant session logs with verification-based enforcement.

---

## Quick Start

### Automated (Recommended)

```bash
python3 .claude/skills/session-init/scripts/new_session_log.py
```

The script will:

1. Prompt for session number and objective
2. Auto-detect git state (branch, commit, date)
3. Read canonical template from SESSION-PROTOCOL.md
4. Write session log with EXACT template format
5. Validate immediately with validate_session_json.py
6. Exit nonzero on validation failure

### Manual (If Needed)

```text
/session-init
```

Follow the manual workflow below if the automated script doesn't meet your needs.

---

## Triggers

| Phrase | Action |
|--------|--------|
| `/session-init` | Create new session log |
| `create session log` | Natural language activation |
| `start new session` | Alternative trigger |
| `initialize session` | Alternative trigger |

| Input | Output | Quality Gate |
|-------|--------|--------------|
| Session number, objective | Validated session log file | Exit code 0 from validation |

---

## When to Use

Use this skill when:

- Starting any new work session
- Need a protocol-compliant session log
- Previous session log failed CI validation and need a fresh start

Use [session-log-fixer](../session-log-fixer/SKILL.md) instead when:

- An existing session log has validation errors that need repair
- CI failed with "Session protocol validation failed"

Use [session-migration](../session-migration/SKILL.md) instead when:

- Converting old markdown session logs to JSON format

## Why This Skill Exists

**Problem**: Every PR starts with malformed session logs that fail CI validation.

**Root Cause**: Agents generate session logs from LLM memory instead of copying the canonical template from SESSION-PROTOCOL.md. This causes variations like:

- Missing `(COMPLETE ALL before closing)` text in Session End header
- Wrong heading levels (`##` vs `###`)
- Missing sections

**Solution**: Verification-based enforcement following the proven Serena initialization pattern.

---

## Session Naming Protocol

**Format**: `YYYY-MM-DD-session-NN.json`

The script automatically generates human-readable filenames by extracting up to 5 keywords from the session objective using NLP heuristics:

- **Remove stop words**: Common words like "the", "a", "to", "for" are filtered out
- **Keep domain terms**: Technical verbs like "implement", "debug", "fix", "refactor" are preserved
- **Convert to kebab-case**: Words are joined with hyphens for readability
- **Limit to 5 keywords**: Most relevant terms from the start of the objective

### Examples

| Session Objective | Generated Filename |
|-------------------|--------------------|
| "Debug recurring session validation failures" | `2026-01-06-session-374-debug-recurring-session-validation-failures.md` |
| "Implement OAuth 2.0 authentication flow" | `2026-01-06-session-375-implement-oauth-authentication-flow.md` |
| "Fix test coverage gaps in UserService" | `2026-01-06-session-376-fix-test-coverage-gaps-userservice.md` |
| "Refactor PaymentProcessor for better error handling" | `2026-01-06-session-377-refactor-paymentprocessor-better-error-handling.md` |

### Benefits

- **Human-readable discovery**: Browse session history with `ls .agents/sessions/` and instantly understand content
- **Grep-friendly search**: Find sessions by topic with `grep -l "oauth" .agents/sessions/*.json`
- **Self-documenting**: No need to open files to understand what each session covers
- **Chronological order**: YYYY-MM-DD prefix preserves time-based sorting
- **Pattern identification**: Keyword clustering reveals recurring themes across sessions

---

## Process Overview

```text
User Request: /session-init
    |
    v
+---------------------------------------------+
| Phase 1: GATHER INPUTS                      |
| - Prompt for session number                 |
| - Prompt for objective                      |
| - Auto-detect: date (YYYY-MM-DD)           |
| - Auto-detect: branch (git branch)         |
| - Auto-detect: commit (git log)            |
| - Auto-detect: git status                  |
+---------------------------------------------+
    |
    v
+---------------------------------------------+
| Phase 2: READ CANONICAL TEMPLATE            |
| - Read .agents/SESSION-PROTOCOL.md         |
| - Extract template (lines 494-612)         |
| - Preserve EXACT formatting                |
| - Critical: Keep "(COMPLETE ALL before     |
|   closing)" text in Session End header     |
+---------------------------------------------+
    |
    v
+---------------------------------------------+
| Phase 3: POPULATE TEMPLATE                  |
| - Replace NN with session number           |
| - Replace YYYY-MM-DD with date             |
| - Replace [branch name] with actual branch |
| - Replace [SHA] with commit hash           |
| - Replace [objective] with user input      |
| - Replace [clean/dirty] with git status    |
+---------------------------------------------+
    |
    v
+---------------------------------------------+
| Phase 4: WRITE SESSION LOG                  |
| - Generate descriptive filename with        |
|   keywords from objective                   |
| - Write to .agents/sessions/YYYY-MM-DD-    |
|   session-NN-keyword1-keyword2-...md       |
| - Preserve all template sections           |
+---------------------------------------------+
    |
    v
+---------------------------------------------+
| Phase 5: IMMEDIATE VALIDATION               |
| - Run validate_session_json.py         |
| - Report validation result                 |
| - If FAIL: show errors, allow retry       |
| - If PASS: confirm success                 |
+---------------------------------------------+
    |
    v
Protocol-Compliant Session Log
```

---

## Workflow

### Step 1: Gather Session Information

Prompt user for required inputs:

```text
What is the session number? (e.g., 375)
What is the session objective? (e.g., "Implement session-init skill")
```

Auto-detect from environment:

```bash
# Current date
date +%Y-%m-%d
# or PowerShell: Get-Date -Format "yyyy-MM-dd"

# Current branch
git branch --show-current

# Starting commit
git log --oneline -1

# Git status
git status --short
```

### Step 2: Read Canonical Template

**CRITICAL**: Use the new_session_log.py script to read the template from SESSION-PROTOCOL.md.

```bash
python3 .claude/skills/session-init/scripts/new_session_log.py
```

**DO NOT** generate the template from memory or read specific line numbers. The script extracts the canonical template dynamically:

- Header levels (`##` vs `###`)
- Table structure with pipe separators
- Checkbox format `[ ]`
- Comment blocks `<!-- -->`
- **CRITICAL**: `### Session End (COMPLETE ALL before closing)` header text

### Step 3: Populate Template Variables

Replace placeholders with actual values:

| Placeholder | Replace With |
|-------------|--------------|
| `NN` | Session number (e.g., 375) |
| `YYYY-MM-DD` | Current date |
| `[branch name]` | Git branch name |
| `[SHA]` | Starting commit hash |
| `[What this session aims to accomplish]` | User-provided objective |
| `[clean/dirty]` | Git status result |

Leave these unchanged:

- All checklist items `[ ]` (unchecked)
- Evidence columns with placeholder text
- Comment blocks

### Step 4: Write Session Log File

Write the populated session log to a file with descriptive naming:

**Filename Format**: `YYYY-MM-DD-session-NN.json`

The script automatically:

1. Extracts up to 5 keywords from the objective
2. Filters out common stop words (the, a, to, for, etc.)
3. Converts to kebab-case
4. Generates human-readable filename

**Example**:

For objective "Debug recurring session validation failures", the filename becomes:
`2026-01-06-session-374-debug-recurring-session-validation-failures.md`

Construct filename: `.agents/sessions/YYYY-MM-DD-session-NN.json`

Example: `.agents/sessions/.agents/sessions/2026-01-05-session-375.json`

Write the populated template to this file.

### Step 5: Validate Immediately

Run validation script:

```bash
python3 scripts/validate_session_json.py ".agents/sessions/YYYY-MM-DD-session-NN.json"
```

Check exit code:

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | PASS | Confirm success, agent proceeds |
| 1 | FAIL | Show errors, offer to retry |

---

## Verification Checklist

Before reporting success:

- [ ] Session number provided by user
- [ ] Objective provided by user
- [ ] Template read from SESSION-PROTOCOL.md (NOT generated from memory)
- [ ] All template sections present
- [ ] Session End header includes `(COMPLETE ALL before closing)`
- [ ] File written to correct path `.agents/sessions/YYYY-MM-DD-session-NN.json`
- [ ] Validation script executed
- [ ] Validation result is PASS (exit code 0)

---

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Generating template from memory | Will miss exact formatting | Read from SESSION-PROTOCOL.md |
| Skipping validation | Won't catch errors until CI | Validate immediately |
| Hardcoding template in skill | Template may change | Always read from canonical source |
| Pre-checking boxes | Defeats verification purpose | Leave all unchecked |
| Using `## Session End` | Missing required text | Use `### Session End (COMPLETE ALL before closing)` |

---

## Example Output

**Success**:

```text
Session log created and validated

  File: .agents/sessions/.agents/sessions/2026-01-05-session-375.json
  Validation: PASS
  Branch: feat/session-init
  Commit: abc1234

Next: Complete Session Start checklist in the session log
```

**Failure**:

```text
Session log created but validation FAILED

  File: .agents/sessions/.agents/sessions/2026-01-05-session-375.json
  Validation: FAIL
  Errors:
    - Missing Session End checklist header

Run: python3 scripts/validate_session_json.py ".agents/sessions/.agents/sessions/2026-01-05-session-375.json" 

Fix the issues and re-validate.
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [log-fixer](../log-fixer/) | Reactive fix after failure (this skill prevents need) |
| [qa-eligibility](../qa-eligibility/) | QA eligibility checking (different purpose) |

---

## Scripts

| Script | Purpose | Exit Codes |
|--------|---------|------------|
| [new_session_log.py](scripts/new_session_log.py) | Automated session log creation with validation | 0=success, 1=error |
| [new_session_log_json.py](scripts/new_session_log_json.py) | Simplified JSON session log creation | 0=success, 1=error |

### Example Usage

**Automated (Recommended)**:

```bash
# Create session log with parameters
python3 .claude/skills/session-init/scripts/new_session_log.py --session-number 375 --objective "Implement feature X"

# Skip validation
python3 .claude/skills/session-init/scripts/new_session_log.py --session-number 375 --objective "Implement feature X" --skip-validation

# Simplified JSON-only version
python3 .claude/skills/session-init/scripts/new_session_log_json.py --session-number 375 --objective "Implement feature X"
```

---

## References

- [SESSION-PROTOCOL.md](.agents/SESSION-PROTOCOL.md) - Canonical template source
- [validate_session_json.py](scripts/validate_session_json.py) - Validation script
- [Template Extraction](references/template-extraction.md) - How to extract template
- [Validation Patterns](references/validation-patterns.md) - Common validation issues

---

## Pattern: Verification-Based Enforcement

This skill follows the same pattern as Serena initialization:

| Aspect | Serena Init | Session Init |
|--------|-------------|--------------|
| **Verification** | Tool output in transcript | Validation script exit code |
| **Feedback** | Immediate (tool response) | Immediate (validation output) |
| **Enforcement** | Cannot proceed without output | Cannot claim success without pass |
| **Compliance Rate** | 100% (never violated) | Target: 100% |

**Why it works**:

- Reads canonical template from file (single source of truth)
- Auto-populates git state (reduces manual errors)
- Validates immediately with same script as CI (instant feedback)
- Cannot skip validation (built into skill workflow)
- Provides actionable error messages if validation fails
