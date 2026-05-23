---
name: validate
description: Validate a specification file and provide actionable suggestions for issues
allowed-tools: Bash(./scripts/validate-spec.sh:*), Read, Glob
---

# Validate Skill

Validate specification files and provide actionable suggestions for any issues found.

## Usage

```
/validate                                    # Validate most recent active spec
/validate docs/specs/001-feature/spec.md    # Validate specific spec
```

## Purpose

Run comprehensive validation on a spec file and provide:
1. Pass/fail status for each check
2. Actionable suggestions for fixing issues
3. Context-aware recommendations

## Workflow

### 1. Find Spec File

If no file specified, find the most recently modified active spec:

```bash
find docs/specs -name "spec.md" \
  -not -path "*/done/*" \
  -not -path "*/templates/*" \
  -type f -print0 2>/dev/null | \
  xargs -0 ls -t 2>/dev/null | head -1
```

### 2. Run Validation Script

```bash
./scripts/validate-spec.sh "$SPEC_FILE"
```

The script checks:
1. **Required Sections**: Summary, Problem, User Stories, Requirements, Success Criteria, Design, Tasks
2. **Clarification Markers**: No unresolved `[NEEDS CLARIFICATION:]` markers
3. **GitHub Issue Link**: Issue reference present
4. **Constitution Reference**: Links to constitution.md
5. **Placeholder Detection**: No unfilled template placeholders
6. **Review Checklist**: Completion percentage (error if <75%)
7. **Requirements Count**: At least 2 FR-XXX entries
8. **Success Criteria Count**: At least 2 SC-XXX entries
9. **Task Tracking**: Structured tasks (T001:, T002:...)

### 3. Analyze Results

Parse the script output and categorize:
- **Errors** (must fix before implementation)
- **Warnings** (should review)
- **Passed** (all good)

### 4. Provide Suggestions

For each issue, provide actionable fix:

| Issue | Suggestion |
|-------|------------|
| Missing section | Add the section header and fill content |
| Unresolved clarification | Run `/clarify` to resolve |
| Incomplete review checklist | Complete persona reviews before implementing |
| Few requirements | Add more FR-XXX entries to Requirements section |
| Few success criteria | Add measurable SC-XXX outcomes |

## Output Format

```
╔════════════════════════════════════════════════════════════════╗
║  Spec Validation: docs/specs/001-feature/spec.md               ║
╚════════════════════════════════════════════════════════════════╝

✅ Required Sections: All 7 sections present
✅ Clarification Markers: All resolved
✅ GitHub Issue: #1306 linked
⚠️  Review Checklist: 15/20 complete (75%)
   → Complete remaining items in Security & SRE sections
✅ Requirements: 4 functional requirements (FR-001 to FR-004)
✅ Success Criteria: 3 criteria (SC-001 to SC-003)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Result: PASSED with 1 warning

Next steps:
  - Complete Review Checklist (currently 75%)
  - Begin implementation when ready
```

## Error Suggestions

### Missing Sections
```
❌ Missing: ## User Stories

Suggestion: Add user stories with Gherkin acceptance scenarios:

### US-1: [Story Title] (Priority: P1)
As a **[role]**, I want **[capability]**, so that **[benefit]**.

**Acceptance Scenarios**:
1. **Given** [precondition], **When** [action], **Then** [result]
```

### Unresolved Clarifications
```
❌ Found 2 unresolved [NEEDS CLARIFICATION] markers

Suggestion: Run /clarify to resolve these with structured options:
  Line 163: [NEEDS CLARIFICATION: Should cache support cross-namespace?]
  Line 164: [NEEDS CLARIFICATION: Default eviction policy?]
```

### Incomplete Review Checklist
```
⚠️  Review Checklist: 10/20 complete (50%)

Suggestion: Review spec from each persona's perspective:
  - [ ] Project Manager: 5/5 ✅
  - [ ] Platform Engineer: 3/5 (missing: examples, KCL pattern check)
  - [ ] Security: 2/5 (missing: network policy, RBAC, secrets)
  - [ ] SRE: 0/5 (not started)
```

## Integration

This skill fits in the SDD workflow:

```
/spec → /spec-status → /clarify → /validate → implement → /create-pr
```

## Related Skills

- `/spec` - Create new specification
- `/spec-status` - View pipeline overview
- `/clarify` - Resolve clarification markers
- `/create-pr` - Create PR when implementation complete
