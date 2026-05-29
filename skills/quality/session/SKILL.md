---
name: session
version: 1.0.0
description: Session management and protocol compliance skills. Use Test-InvestigationEligibility to check if staged files qualify for investigation-only QA skip per ADR-034 before committing with 'SKIPPED investigation-only' verdict.
license: MIT
model: claude-sonnet-4-5
metadata:
  domains:
    - session-protocol
    - qa-validation
    - investigation-eligibility
  type: utility
  complexity: low
  related_skills:
    - github
    - qa
---

# Session Skills

Skills for session management and protocol compliance.

## Triggers

| Phrase | Action |
|--------|--------|
| "Check if I can skip QA" | Run Test-InvestigationEligibility.ps1 |
| "Am I eligible for investigation-only?" | Verify staged files against ADR-034 allowlist |
| "Verify investigation session eligibility" | Check QA skip eligibility before commit |
| "Can I use SKIPPED: investigation-only?" | Validate investigation-only exemption |
| "Test eligibility for QA skip" | Execute eligibility check script |

## Process

### Phase 1: Eligibility Check

| Step | Action | Tool | Output |
|------|--------|------|--------|
| 1.1 | Stage files for commit | `git add` | Files added to staging area |
| 1.2 | Run eligibility check | `Test-InvestigationEligibility.ps1` | JSON with Eligible, StagedFiles, Violations |
| 1.3 | Verify Eligible=true | Parse JSON output | Boolean result |

### Phase 2: Commit Decision

| Step | Action | Condition | Next Step |
|------|--------|-----------|-----------|
| 2.1 | Proceed with investigation-only skip | Eligible=true, Violations=[] | Use "SKIPPED: investigation-only" |
| 2.2 | Address violations or invoke qa agent | Eligible=false | Fix violations or start new session |

---

## Quick Reference

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| Test-InvestigationEligibility | Check if staged files qualify for investigation-only QA skip | Before committing with `SKIPPED: investigation-only` |

---

## Test Investigation Eligibility

Check if staged files qualify for investigation-only QA skip per ADR-034.

### Trigger Phrases

- "Check if I can skip QA"
- "Am I eligible for investigation-only?"
- "Verify investigation session eligibility"
- "Can I use SKIPPED: investigation-only?"

### Usage

```powershell
pwsh .claude/skills/session/scripts/Test-InvestigationEligibility.ps1
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
  "StagedFiles": [".agents/sessions/2025-01-01-session-01.md"],
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
    ".agents/sessions/2025-01-01-session-01.md",
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
                        └── Test-InvestigationEligibility.ps1
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
   └── pwsh .claude/skills/session/scripts/Test-InvestigationEligibility.ps1

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
| MUST | Route to qa agent (feature implementation) | [x] | `SKIPPED: investigation-only` - Verified via Test-InvestigationEligibility.ps1 |
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

**Important**: This allowlist is defined by ADR-034 (Investigation Session QA Exemption). The patterns in `Test-InvestigationEligibility.ps1` are validated by Pester tests to ensure they match the ADR specification.

---

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Skipping eligibility check | May commit ineligible files with investigation-only skip | Always run the skill before using the skip |
| Ignoring violations | QA exemption won't be valid | Address violations or invoke qa agent |
| Using for code changes | Investigation-only is for analysis, not implementation | Start a new session for code work |
| Hardcoding path checks | Patterns may drift from ADR-034 specification | Use this skill which implements the ADR patterns |

---

## Verification Checklist

After using this skill:

- [ ] Skill output shows `Eligible: true`
- [ ] No `Violations` in output
- [ ] No `Error` field in output
- [ ] Session log evidence updated with skill output

---

## Related

| Reference | Description |
|-----------|-------------|
| [ADR-034](../../../.agents/architecture/decisions/adr-034-investigation-session-qa-exemption.md) | Investigation Session QA Exemption architecture decision |
| [SESSION-PROTOCOL.md](../../../.agents/SESSION-PROTOCOL.md) | Session start/end requirements (Phase 2.5) |
| [Issue #662](https://github.com/rjmurillo/ai-agents/issues/662) | Create QA skip eligibility check skill |
| [Validate-SessionJson.ps1](../../../scripts/Validate-SessionJson.ps1) | Validates session JSON format (separate from eligibility) |
| [Test-InvestigationEligibility.Tests.ps1](../../../tests/Test-InvestigationEligibility.Tests.ps1) | Pester tests ensuring pattern consistency |
