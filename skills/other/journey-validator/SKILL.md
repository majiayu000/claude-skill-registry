---
name: journey-validator
description: "Validate user journey documents before entering development workflow. Checks document structure, cross-validates against domain model (data-types.md, relationships.md), identifies logic inconsistencies (undefined entities/relations/enums), finds redundant or conflicting content, and verifies data operation closures. Use before Phase 0.5 (domain modeling) or after modifying user-journeys. Triggers: 'validate journeys', 'check user journeys', 'journey validation', 'pre-workflow check', or when docs/user-journeys/ files are modified."
---

# Journey Validator

Structured validation workflow for user journey documents. Ensures user-journeys are complete, consistent, and conflict-free before entering the development workflow (Phase 0.5: Domain Modeling).

> **Position in Workflow:** This skill runs BEFORE domain-modeler. It validates the human-authored requirements document to catch issues early, preventing them from propagating into the domain model and subsequent phases.

## When to Use

- **Before development workflow:** Run this before entering Phase 0.5 (Domain Modeling)
- **After journey modifications:** When user-journeys.md or split files are updated
- **Periodic maintenance:** When you suspect the journeys may have drifted from the domain model
- **PM handoff:** When receiving updated requirements from product/design team

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| User journey docs | **Yes** | `docs/user-journeys.md` or `docs/user-journeys/*.md` (split structure) |
| Domain model docs | Optional | `docs/data-types.md`, `docs/relationships.md` (for cross-validation) |
| CRUD operations | Optional | `docs/crud-operations.md` (for operation closure check) |

## Outputs

| Output | Purpose |
|--------|---------|
| Validation report | Structured list of issues found, categorized by severity |
| TODO markers | Inline markers in journey docs for unresolved issues |
| Clean documents | Fixed structural issues (merge conflicts, numbering, etc.) |

## Validation Dimensions

### 1. Structure Validation

Check document structure for technical issues that prevent processing.

**Checks:**
- [ ] No git merge conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
- [ ] Consistent heading hierarchy (no skipped levels)
- [ ] Consistent chapter/section numbering (sequential, no gaps/duplicates)
- [ ] No broken Mermaid diagrams (unclosed code blocks, invalid syntax)
- [ ] Table formatting is correct (consistent column count per row)
- [ ] Cross-references (links) are valid

**Severity:** HIGH — structural issues block further processing

**Fix pattern:**
```
Issue: Merge conflict markers at lines 27, 61, 76
Action: Resolve conflicts, keeping the intended content
```

### 2. Logic Consistency

Cross-validate journeys against the domain model documentation.

**Checks:**
- [ ] Every entity mentioned in journeys is defined in `data-types.md`
- [ ] Every relationship implied in journeys is defined in `relationships.md`
- [ ] Every enum value used in journeys is defined in the corresponding entity
- [ ] Every role mentioned in journeys is defined in the role list

**Severity:** MEDIUM — inconsistencies lead to gaps in the domain model

**Issue format:**
```
L-001: Entity "notification" used in journey but not defined in data-types.md
       Location: 08-activity-close.md, line 45
       Action: Add notification entity to data-types.md OR remove from journey
```

**Common undefined elements:**
| Element Type | Example | Check Against |
|-------------|---------|---------------|
| Entity | `notification`, `certificate` | data-types.md entities |
| Relation | `event:resource`, `group:post` | relationships.md relations |
| Enum value | `vote`, `bounty` | data-types.md `type` enums |
| Role | `jury`, `mentor` | data-types.md user.role enum |
| Status | `reviewing`, `approved` | Entity status enums |

### 3. Redundancy Detection

Find duplicate or highly similar content that should be merged.

**Checks:**
- [ ] No duplicate journey descriptions (same flow described twice)
- [ ] No split chapters that should be merged
- [ ] No repeated business rules across different sections

**Severity:** LOW — redundancy causes maintenance burden but doesn't break the system

**Issue format:**
```
R-001: Redundant content between sections
       §2 "设立活动" vs §6 "悬赏与企业出题"
       Both describe activity creation flow
       Action: Merge into single section with variants, or cross-reference
```

### 4. Conflict Detection

Find contradictory requirements within journeys.

**Checks:**
- [ ] No conflicting business rules (e.g., "users can" vs "users cannot" for same action)
- [ ] No conflicting status transitions (e.g., different valid transitions for same status)
- [ ] No conflicting permission definitions

**Severity:** HIGH — conflicts lead to ambiguous or broken implementations

**Issue format:**
```
C-001: Conflicting requirements
       §3: "团队成员可以直接邀请好友加入"
       §4: "团队成员加入需要队长审批"
       Action: Clarify which rule applies, or define conditions for each
```

### 5. Data Operation Closure

Verify every entity has complete CRUD coverage in journeys.

**Checks:**
- [ ] Every entity has at least one CREATE journey
- [ ] Every entity has at least one READ journey (list/detail)
- [ ] Every entity has UPDATE and DELETE journeys (or explicit note why not)
- [ ] Every relationship has JOIN and LEAVE journeys

**Severity:** MEDIUM — incomplete coverage leads to missing features

**Issue format:**
```
M-001: Missing operation coverage
       Entity: rule
       Missing: No journey describes rule deletion
       Action: Add journey step for rule deletion, or note as "admin-only via API"
```

## Workflow

### Phase 1: Structural Scan

```
1. Read all journey files:
   - If single file: docs/user-journeys.md
   - If split structure: docs/user-journeys/*.md + docs/user-journeys/README.md

2. Check for structural issues:
   - Regex scan for merge conflict markers
   - Parse heading structure, verify hierarchy
   - Verify chapter numbering sequence
   - Check table formatting consistency

3. Fix or report issues:
   - Auto-fix: Remove conflict markers (if resolution is clear)
   - Auto-fix: Renumber chapters (if sequence is broken)
   - Report: Complex issues requiring human decision
```

### Phase 2: Cross-Validation

```
1. Extract referenced elements from journeys:
   - Entities (nouns representing business objects)
   - Relationships (verbs connecting entities)
   - Enum values (status, type, role values)
   - Roles (user types performing actions)

2. Compare against domain model:
   - Load docs/data-types.md → extract defined entities and enums
   - Load docs/relationships.md → extract defined relationships
   - Compute difference sets

3. Report gaps:
   - Elements in journeys but not in model → L-xxx issues
   - Elements in model but not in journeys → potential orphans
```

### Phase 3: Content Analysis

```
1. Redundancy detection:
   - Extract key phrases from each section
   - Compute similarity scores between sections
   - Flag sections with >70% phrase overlap

2. Conflict detection:
   - Extract permission statements ("can", "cannot", "must", "only")
   - Group by entity and operation
   - Flag contradictory statements for same entity+operation

3. Report findings:
   - R-xxx for redundancy
   - C-xxx for conflicts
```

### Phase 4: Coverage Analysis

```
1. Build operation matrix:
   - For each entity: track which CRUD operations are covered
   - For each relationship: track join/leave coverage

2. Identify gaps:
   - Missing CREATE: entity cannot be instantiated
   - Missing READ: entity cannot be viewed
   - Missing UPDATE: entity is immutable (intended?)
   - Missing DELETE: entity is permanent (intended?)

3. Report as M-xxx issues
```

### Phase 5: Report Generation

```
1. Aggregate all issues by severity:
   - HIGH: Structure, Conflicts
   - MEDIUM: Logic, Coverage
   - LOW: Redundancy

2. Generate validation report:
   - Summary counts by event
   - Detailed issue list with locations and actions
   - Recommended fixes

3. Optionally insert TODO markers in source files:
   - Format: <!-- TODO [L-001]: description -->
   - Position: near the problematic content
```

## Issue Marker Convention

When inserting markers into journey documents:

```markdown
<!-- TODO [L-001]: Entity "notification" is not defined in data-types.md -->
用户收到活动开始通知后...

<!-- TODO [C-002]: Conflicts with §4 team approval requirement -->
团队成员可以直接邀请好友加入...
```

Marker format:
- `L-xxx`: Logic inconsistency (undefined elements)
- `C-xxx`: Conflict (contradictory requirements)
- `R-xxx`: Redundancy (duplicate content)
- `M-xxx`: Missing coverage (incomplete CRUD)
- `S-xxx`: Structure issue (formatting, numbering)

## Integration with Development Workflow

```
┌─────────────────────────────────────────────────────────┐
│ User writes/updates docs/user-journeys.md              │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│ journey-validator (this skill)                          │
│  - Validate structure                                   │
│  - Cross-validate against domain model                  │
│  - Detect redundancy and conflicts                      │
│  - Check operation coverage                             │
│  - Generate report / insert TODO markers                │
└─────────────────────────────────────────────────────────┘
                            ↓
              ┌─────── All issues resolved? ──────┐
              │                                    │
             YES                                  NO
              ↓                                    ↓
┌─────────────────────────────────────────┐   ┌─────────────────────┐
│ Phase 0.5: domain-modeler               │   │ Fix issues          │
│  - Extract entities and relationships   │   │  - Resolve TODOs    │
│  - Generate data-types.md, etc.         │   │  - Update journeys  │
└─────────────────────────────────────────┘   │  - Re-run validator │
                                              └─────────────────────┘
```

## Recommended Running Cadence

| Event | Action |
|-------|--------|
| Before Phase 0.5 | **Required** — validate before domain modeling |
| After PM updates | **Required** — catch new issues early |
| After git merge | Recommended — merges often introduce conflicts |
| Weekly maintenance | Optional — catch drift between journeys and model |

## Example Validation Report

```markdown
# Journey Validation Report

**Date:** 2025-02-08
**Files scanned:** 17 (docs/user-journeys/*.md)
**Domain model version:** data-types.md@7e5684d

## Summary

| Event | HIGH | MEDIUM | LOW |
|----------|------|--------|-----|
| Structure | 0 | 0 | 0 |
| Logic | 5 | 3 | 0 |
| Conflict | 1 | 1 | 0 |
| Redundancy | 0 | 0 | 2 |
| Coverage | 0 | 2 | 0 |
| **Total** | **6** | **6** | **2** |

## HIGH Severity Issues

### L-001: Undefined entity "notification"
- **Location:** 08-activity-close.md:45
- **Context:** "系统向所有参赛者发送活动结束通知"
- **Action:** Add `notification` entity to data-types.md with fields: id, type, title, content, user_id, is_read, created_at

### C-001: Conflicting team join rules
- **Location:** 03-team-management.md:20 vs 04-activity-participation.md:35
- **Context:** Direct invite vs approval-required
- **Action:** Define when each rule applies (e.g., public teams vs private teams)

## MEDIUM Severity Issues

### L-002: Undefined relation "event:resource"
- **Location:** 02-activity-setup.md:60
- **Action:** Add to relationships.md if banner images are attached to events

### M-001: Missing DELETE journey for "rule"
- **Location:** N/A (no journey covers rule deletion)
- **Action:** Add as admin-only operation, or note as immutable after event publish

## LOW Severity Issues

### R-001: Redundant activity creation content
- **Locations:** 02-activity-setup.md, 10-bounty-enterprise.md
- **Action:** Merge or cross-reference
```

## Adapting for Other Projects

This skill is designed for Synnovator but can be adapted:

1. **Replace file paths** — Change `docs/user-journeys/` to your journey doc location
2. **Adjust domain model references** — Point to your schema documentation
3. **Customize issue events** — Add project-specific validation checks
4. **Adjust severity thresholds** — Some projects may tolerate more redundancy

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | What to Do Instead |
|-------------|----------------|-------------------|
| Skipping validation before domain modeling | Issues propagate into code | Always validate first |
| Only validating structure | Logic issues are more impactful | Run all 5 dimension checks |
| Ignoring LOW severity issues | They accumulate over time | Address during regular maintenance |
| Auto-fixing conflicts | Human judgment required | Report and let PM decide |
| Running only on single files | Cross-file conflicts missed | Validate entire journey set |
