---
name: session-qa-eligibility
description: Check investigation session QA skip eligibility per ADR-034. Validates if staged files qualify for investigation-only exemption by checking against allowed paths (.agents/sessions/, .agents/analysis/, .serena/memories/, etc).
version: 1.0.0
license: MIT
model: claude-sonnet-4-5
---

# Session QA Eligibility

Check investigation session QA skip eligibility per ADR-034.

---

## Triggers

- `Check if I can skip QA`
- `Am I eligible for investigation-only?`
- `Verify investigation session eligibility`

---

## When to Use

Use this skill when:

- Completing an investigation-only session and considering QA skip
- Need to verify staged files qualify for investigation-only exemption
- Want to check eligibility before committing with "SKIPPED: investigation-only"

Use the qa agent instead when:

- Session includes any code changes or implementation work
- This skill reports `Eligible: false`

## Process

```text
User Request: Check QA eligibility
    |
    v
+---------------------------------------------+
| Phase 1: GET STAGED FILES                   |
| - Run git diff --cached --name-only        |
| - Collect all staged file paths            |
+---------------------------------------------+
    |
    v
+---------------------------------------------+
| Phase 2: CHECK ALLOWLIST                    |
| - Compare against allowed paths:           |
|   * .agents/sessions/                      |
|   * .agents/analysis/                      |
|   * .agents/retrospective/                 |
|   * .serena/memories/                      |
|   * .agents/security/                      |
| - Identify violations                      |
+---------------------------------------------+
    |
    v
+---------------------------------------------+
| Phase 3: RETURN RESULT                      |
| - Eligible: true if all files in allowlist |
| - Eligible: false if any violations        |
| - Include violations list for debugging    |
+---------------------------------------------+
```

---

## Quick Reference

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| Test-InvestigationEligibility | Check if staged files qualify for investigation-only QA skip | Before committing with `SKIPPED: investigation-only` |

---

## Test Investigation Eligibility

Check if staged files qualify for investigation-only QA skip per ADR-034.

### Usage

```bash
python3 .claude/skills/session-qa-eligibility/scripts/test_investigation_eligibility.py
```

### Output

Returns JSON with:

| Field | Type | Description |
|-------|------|-------------|
| `Eligible` | boolean | `true` if all staged files are in allowlist |
| `StagedFiles` | array | All staged file paths |
| `Violations` | array | Files not in allowlist (empty if eligible) |
| `AllowedPaths` | array | Reference list of allowed path prefixes |
| `Error` | string | Present only on git errors |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (eligibility result in JSON output) |

**Note**: The script always exits 0. Check the `Eligible` field in the JSON output to determine eligibility. The `Error` field is present when git commands fail.

### Error Handling

| Scenario | Behavior | Output |
|----------|----------|--------|
| Not in git repository | Returns JSON with `Eligible: false` | `Error` field explains the issue |
| Git command fails | Returns JSON with `Eligible: false` | `Error` field explains the issue |
| Empty staged files | Returns JSON with `Eligible: true` | `StagedFiles` is empty array |
| Mixed allowed/disallowed files | Returns JSON with `Eligible: false` | `Violations` lists disallowed files |

### Example Outputs

**Eligible (investigation-only files)**:

```json
{
  "Eligible": true,
  "StagedFiles": [".agents/sessions/.agents/sessions/2025-01-01-session-01.json"],
  "Violations": [],
  "AllowedPaths": [
    ".agents/sessions/",
    ".agents/analysis/",
    ".agents/retrospective/",
    ".serena/memories/",
    ".agents/security/"
  ]
}
```

**Not eligible (contains code files)**:

```json
{
  "Eligible": false,
  "StagedFiles": [
    ".agents/sessions/.agents/sessions/2025-01-01-session-01.json",
    "scripts/MyScript.ps1"
  ],
  "Violations": ["scripts/MyScript.ps1"],
  "AllowedPaths": [
    ".agents/sessions/",
    ".agents/analysis/",
    ".agents/retrospective/",
    ".serena/memories/",
    ".agents/security/"
  ]
}
```

**Git error**:

```json
{
  "Eligible": false,
  "StagedFiles": [],
  "Violations": [],
  "AllowedPaths": [
    ".agents/sessions/",
    ".agents/analysis/",
    ".agents/retrospective/",
    ".serena/memories/",
    ".agents/security/"
  ],
  "Error": "Not in a git repository or git command failed"
}
```

---

## Agent Workflow Integration

### SESSION-PROTOCOL.md Relationship

This skill implements the verification step for **Phase 2.5: QA Validation** of the Session End Protocol:

```text
SESSION-PROTOCOL.md (Phase 2.5: QA Validation)
                │
                ├── Feature implementation → MUST invoke qa agent
                │
                └── Investigation session → MAY skip QA
                        │
                        └── test_investigation_eligibility.py
                                │
                                ├── Eligible: true → Use "SKIPPED: investigation-only"
                                │
                                └── Eligible: false → MUST invoke qa agent
```

### Workflow: Before Committing Investigation Work

```text
1. Stage your files
   │
   └── git add .agents/sessions/... .serena/memories/...

2. Run eligibility check
   │
   └── python3 .claude/skills/session-qa-eligibility/scripts/test_investigation_eligibility.py

3. Check output
   │
   ├── Eligible: true
   │   └── Safe to commit with "SKIPPED: investigation-only"
   │
   └── Eligible: false
       │
       ├── Check Violations array
       │   └── Either: Remove violating files from staging
       │   └── Or: Start new session for implementation work
       │
       └── Invoke qa agent for the implementation work
```

### Integration with Session End Checklist

Use this skill to validate the QA skip condition:

```markdown
### Session End (COMPLETE ALL before closing)

| Req | Step | Status | Evidence |
|-----|------|--------|----------|
| MUST | Route to qa agent (feature implementation) | [x] | `SKIPPED: investigation-only` - Verified via test_investigation_eligibility.py |
```

---

## Allowed Paths (Investigation Allowlist)

These paths qualify for investigation-only QA exemption:

| Path | Purpose |
|------|---------|
| `.agents/sessions/` | Session logs documenting work |
| `.agents/analysis/` | Investigation outputs and findings |
| `.agents/retrospective/` | Learnings and retrospective documents |
| `.serena/memories/` | Cross-session context storage |
| `.agents/security/` | Security assessments and reviews |

**Important**: This allowlist MUST match exactly with `scripts/validate_session_json.py $InvestigationAllowlist`. The patterns are validated by Pester tests to ensure consistency.

---

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Skipping eligibility check | May commit ineligible files with investigation-only skip | Always run the skill before using the skip |
| Ignoring violations | QA exemption won't be valid | Address violations or invoke qa agent |
| Using for code changes | Investigation-only is for analysis, not implementation | Start a new session for code work |
| Hardcoding path checks | Patterns may drift from validate_session_json.py | Use this skill which shares the same patterns |

---

## Verification Checklist

After using this skill:

- [ ] Skill output shows `Eligible: true`
- [ ] No `Violations` in output
- [ ] No `Error` field in output
- [ ] Session log evidence updated with skill output

---

## Scripts

### check_qa_eligibility.py

Checks if staged files qualify for investigation-only QA skip per ADR-034.

```bash
python3 .claude/skills/session-qa-eligibility/scripts/check_qa_eligibility.py
```

---

## Related

| Reference | Description |
|-----------|-------------|
| [ADR-034](../../../../.agents/architecture/ADR-034-investigation-session-qa-exemption.md) | Investigation Session QA Exemption architecture decision |
| [SESSION-PROTOCOL.md](../../../../.agents/SESSION-PROTOCOL.md) | Session start/end requirements (Phase 2.5) |
| [Issue #662](https://github.com/rjmurillo/ai-agents/issues/662) | Create QA skip eligibility check skill |
| [validate_session_json.py](../../../../scripts/validate_session_json.py) | Uses same allowlist for CI validation |
| [test_qa_eligibility.py](tests/test_qa_eligibility.py) | Pytest tests ensuring pattern consistency |
