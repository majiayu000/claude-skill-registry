---
name: session-migration
description: Migrate session logs from markdown to JSON format. Use when PRs contain markdown session logs that need conversion to the new JSON schema, or when batch-migrating historical sessions.
license: MIT
version: 1.0.0
model: claude-sonnet-4-5
metadata:
  domains:
    - session-protocol
    - migration
    - data-transformation
  type: utility
  inputs:
    - markdown-session-logs
    - directory-path
  outputs:
    - json-session-logs
---

# Session Migration Skill

Converts markdown session logs to JSON format for deterministic validation.

---

## Quick Start

```bash
# Migrate single file
python3 .claude/skills/session-migration/scripts/convert_session_to_json.py ".agents/sessions/2026-01-09-session-385.md"

# Migrate all sessions in directory
python3 .claude/skills/session-migration/scripts/convert_session_to_json.py ".agents/sessions/"

# Dry run to preview changes
python3 .claude/skills/session-migration/scripts/convert_session_to_json.py ".agents/sessions/" --dry-run

# Force overwrite existing JSON
python3 .claude/skills/session-migration/scripts/convert_session_to_json.py ".agents/sessions/" --force
```

---

## Triggers

Use this skill when:

- `migrate session logs` - Convert markdown to JSON
- `convert sessions to JSON` - Format migration
- `PR has old markdown sessions` - In-flight PR migration
- `session validation failing` - Regex issues with markdown format
- `batch migrate sessions` - Historical log conversion

---

## When to Use

Use this skill when:

- PR contains markdown session logs that need conversion to JSON
- Batch migrating historical sessions from markdown to JSON
- Session validation failing due to regex issues with markdown format

Use [session-init](../session-init/SKILL.md) instead when:

- Creating a new session log (already creates in JSON format)

Use [session-log-fixer](../session-log-fixer/SKILL.md) instead when:

- Fixing validation errors in an existing JSON session log

## Context

### Why JSON?

Markdown session logs required fragile regex patterns to validate:

- `**Branch**:` vs `Branch:` vs `Starting Branch:`
- Table parsing with varied column orders
- Checkbox detection across different formats

JSON provides:

- Deterministic key-based validation
- Schema enforcement
- No regex, no fuzzy matching
- Clear structure for tooling

### Schema Location

JSON sessions follow the schema at:

```text
.agents/schemas/session-log.schema.json
```

### Validator

JSON sessions are validated by:

```text
scripts/validate_session_json.py
```

---

## Process

```text
┌─────────────────────────────────────────────────────────┐
│ 1. INPUT                                                │
│    Markdown session log (.md)                           │
│    OR directory of .md files                            │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│ 2. PARSE                                                │
│    • Extract session number from filename               │
│    • Extract date from filename                         │
│    • Find branch, commit, objective in content          │
│    • Parse checklist tables for completion status       │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│ 3. TRANSFORM                                            │
│    • Build session object (number, date, branch, etc.)  │
│    • Build protocolCompliance object                    │
│    • Map checkbox [x] to complete: true                 │
│    • Extract evidence from table cells                  │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│ 4. OUTPUT                                               │
│    Write .json file alongside .md                       │
│    (same name, different extension)                     │
└─────────────────────────────────────────────────────────┘
```

---

## JSON Structure

```json
{
  "session": {
    "number": 385,
    "date": "2026-01-09",
    "branch": "feat/session-init-skill",
    "startingCommit": "abc1234",
    "objective": "Session protocol validation improvements"
  },
  "protocolCompliance": {
    "sessionStart": {
      "serenaActivated": { "level": "MUST", "complete": true, "evidence": "Tool output" },
      "handoffRead": { "level": "MUST", "complete": true, "evidence": "Content in context" }
    },
    "sessionEnd": {
      "checklistComplete": { "level": "MUST", "complete": true, "evidence": "All [x] checked" },
      "validationPassed": { "level": "MUST", "complete": true, "evidence": "Exit code 0" }
    }
  },
  "workLog": [],
  "endingCommit": "",
  "nextSteps": []
}
```

---

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `-Path` | string | Yes | Path to .md file or directory |
| `-Force` | switch | No | Overwrite existing .json files |
| `-DryRun` | switch | No | Preview without writing files |

---

## Output

The script returns an array of migrated file paths (`string[]`) and prints a summary:

```text
=== Migration Summary ===
Migrated: 356
Skipped (JSON exists): 0
Failed: 0
```

### Exit Codes

| Code | Meaning | Action |
|------|---------|--------|
| `0` | Success | All files migrated or skipped (expected behavior) |
| `1` | Failure | One or more files failed migration (check error output) |

### Return Value

The script prints migration summary and returns exit code 0 on success, 1 on failure.

---

## PR Migration Workflow

For PRs with in-flight markdown sessions:

1. **Check for markdown sessions in PR**:

   ```bash
   git diff origin/main --name-only | grep -E '\.agents/sessions/.*\.md$'
   ```

2. **Run migration**:

   ```bash
   python3 .claude/skills/session-migration/scripts/convert_session_to_json.py ".agents/sessions/"
   ```

3. **Validate migrated sessions**:

   ```bash
   for f in .agents/sessions/*.json; do python3 scripts/validate_session_json.py "$f"; done
   ```

4. **Commit both formats** (for transition period):

   ```bash
   git add .agents/sessions/*.json
   git commit -m "chore(session): migrate session logs to JSON format"
   ```

---

## Checklist Mapping

The migration script maps markdown checklist patterns to JSON keys.

### Session Start Items

| Regex Pattern | JSON Key | Level |
|---------------|----------|-------|
| `activate_project` | `serenaActivated` | MUST |
| `initial_instructions` | `serenaInstructions` | MUST |
| `HANDOFF\.md` | `handoffRead` | MUST |
| `Create.*session.*log\|session.*log.*exist\|this.*file` | `sessionLogCreated` | MUST |
| `skill.*script` | `skillScriptsListed` | MUST |
| `usage-mandatory` | `usageMandatoryRead` | MUST |
| `CONSTRAINTS` | `constraintsRead` | MUST |
| `memor` | `memoriesLoaded` | MUST |
| `verify.*branch\|branch.*verif\|declare.*branch` | `branchVerified` | MUST |
| `not.*main\|Confirm.*main` | `notOnMain` | MUST |
| `git.*status` | `gitStatusVerified` | SHOULD |
| `starting.*commit\|Note.*commit` | `startingCommitNoted` | SHOULD |

### Session End Items

| Regex Pattern | JSON Key | Level |
|---------------|----------|-------|
| `Complete.*session.*log\|session.*log.*complete\|all.*section` | `checklistComplete` | MUST |
| `HANDOFF.*read-only\|Update.*HANDOFF` | `handoffNotUpdated` | MUST NOT |
| `Serena.*memory\|Update.*memory\|memory.*updat` | `serenaMemoryUpdated` | MUST |
| `markdownlint\|markdown.*lint\|Run.*lint` | `markdownLintRun` | MUST |
| `Commit.*change\|change.*commit` | `changesCommitted` | MUST |
| `Validate.*Session\|validation.*pass\|Route.*qa` | `validationPassed` | MUST |
| `PROJECT-PLAN\|task.*checkbox` | `tasksUpdated` | SHOULD |
| `retrospective` | `retrospectiveInvoked` | SHOULD |

---

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Manually converting markdown to JSON | Error-prone, misses edge cases | Use convert_session_to_json.py script |
| Deleting markdown files after migration | May need originals for reference | Keep both during transition period |
| Skipping validation after migration | Migrated JSON may still be incomplete | Always validate with validate_session_json.py |
| Migrating without `-DryRun` first | Cannot preview changes | Use `-DryRun` to preview, then run for real |

## Verification

After migration:

- [ ] JSON files created alongside markdown originals
- [ ] All migrated JSON files pass `validate_session_json.py`
- [ ] Session numbers and dates match between markdown and JSON
- [ ] No migration errors in script output
- [ ] Both formats committed (for transition period)

## Troubleshooting

### JSON already exists

Use `-Force` to overwrite:

```bash
python3 .claude/skills/session-migration/scripts/convert_session_to_json.py ".agents/sessions/" --force
```

### Some sessions fail validation after migration

Expected for genuinely incomplete sessions. The migration preserves the actual state of checkboxes. Review failed sessions manually.

### Pattern not detected

If a checklist item isn't detected, the markdown format may be non-standard. The script uses flexible regex but edge cases exist. Update the `_find_checklist_item` function patterns if needed.

---

## Scripts

### convert_session_to_json.py

Converts markdown session logs to JSON format.

```bash
python3 .claude/skills/session-migration/scripts/convert_session_to_json.py <input-file> [--output <output-file>]
```

---

## Related

### Skills

| Skill | Purpose |
|-------|---------|
| [session-init](../session-init/SKILL.md) | Create new sessions in JSON format |
| [session-log-fixer](../session-log-fixer/SKILL.md) | Fix validation failures |

### Schema and Validation

| Resource | Location | Purpose |
|----------|----------|---------|
| JSON Schema | `.agents/schemas/session-log.schema.json` | Defines required structure |
| JSON Validator | `scripts/validate_session_json.py` | Validates migrated JSON files |
| Legacy Validator | `scripts/validate_session_json.py` | Validates markdown (deprecated) |

### Architecture

- [ADR-014](../.agents/architecture/ADR-014-distributed-handoff-architecture.md): Distributed handoff architecture (context for migration)
