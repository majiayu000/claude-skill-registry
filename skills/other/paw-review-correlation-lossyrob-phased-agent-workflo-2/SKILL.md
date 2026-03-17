---
name: paw-review-correlation
description: Synthesizes findings across multiple PRs to identify cross-repository dependencies, interface mismatches, and coordination gaps.
---

# Cross-Repository Correlation Analysis Skill

Synthesize findings across multiple PRs to identify cross-repository dependencies, interface mismatches, and coordination gaps that wouldn't be visible when analyzing PRs in isolation.

> **Reference**: Follow Core Review Principles from `paw-review-workflow` skill.

## Applicability

This skill is **only invoked for multi-repository reviews**. Skip this activity when:
- Single PR is being reviewed
- All PRs are from the same repository
- No `related_prs` entries in ReviewContext.md
- Single workspace folder open with single PR

## Prerequisites

Verify these artifacts exist for **each** PR in the review set:

For each `PR-<number>-<repo-slug>/` directory in `.paw/reviews/`:
- `ReviewContext.md` (includes `related_prs` entries)
- `CodeResearch.md` (baseline understanding per repo)
- `DerivedSpec.md` (intent per PR)
- `ImpactAnalysis.md` (includes Cross-Repository Dependencies section)
- `GapAnalysis.md` (includes Cross-Repository Consistency findings)

If any artifact is missing, report blocked status—earlier stages must complete first.

## Core Responsibilities

- Identify shared interfaces between repositories (types, APIs, events, messages)
- Detect interface contract mismatches (producer changed, consumer not updated)
- Flag missing coordinated changes
- Document deployment/migration ordering requirements
- Surface cross-cutting concerns (auth, logging conventions consistency)
- Generate comprehensive `CrossRepoAnalysis.md` artifact

## Non-Responsibilities

- Generating review comments (handled by paw-review-feedback)
- Individual PR analysis (handled by impact/gap skills)
- Workflow orchestration (handled by workflow skill)

## Process Steps

### Step 1: Load All Per-Repo Artifacts

For each PR artifact directory:
1. Read `ImpactAnalysis.md` → extract Cross-Repository Dependencies section
2. Read `GapAnalysis.md` → extract Cross-Repository Consistency findings
3. Read `ReviewContext.md` → extract `related_prs` relationships
4. Read `DerivedSpec.md` → understand each PR's intent

### Step 2: Build Cross-Repo Dependency Graph

Construct a dependency graph showing:

**Repository Roles:**
- **Exporter**: Repository that defines/exports interfaces (APIs, types, events)
- **Consumer**: Repository that imports/uses those interfaces

**Dependency Types:**
- `type-export`: Shared TypeScript/flow types
- `api-endpoint`: REST/GraphQL endpoints
- `event-schema`: Message/event formats
- `package-export`: npm/pip package public interfaces
- `config-schema`: Shared configuration formats

**Output:**
```
Dependency Graph:
  repo-a (API Server)
    → exports: UserProfile type, /api/users endpoint
  repo-b (Frontend)
    → imports: UserProfile type from repo-a
    → calls: /api/users endpoint from repo-a
```

### Step 3: Identify Interface Contracts

For each identified dependency:

**Extract Contract Details:**
- Interface name and type (type, endpoint, event, etc.)
- Defined in: file:line reference in exporter repo
- Consumed in: file:line reference(s) in consumer repo(s)
- Current state: Document what the interface looks like in each repo

**Interface Categories:**
- **Shared Types**: Type definitions, interfaces, schemas
- **API Endpoints**: Request/response shapes, URL paths
- **Event Schemas**: Message formats, event payloads
- **Package Exports**: Public API from shared packages

### Step 4: Detect Interface Mismatches

For each interface contract, check:

**Mismatch Types:**
- **Shape Mismatch**: Fields added/removed/renamed that consumer doesn't handle
- **Type Incompatibility**: Changed types that break consumer usage
- **Missing Update**: Producer changed interface but consumer not updated
- **Version Drift**: Different versions of shared dependency

**Severity Assignment:**
- **Must**: Breaking change that will cause runtime errors
- **Should**: Change that may cause unexpected behavior
- **Could**: Inconsistency that adds technical debt

### Step 5: Analyze Deployment Dependencies

Determine deployment ordering:

**Analysis Questions:**
1. Which repo must deploy first for changes to work?
2. Are there database migrations that must run before code deployment?
3. Are feature flags needed to coordinate the rollout?
4. Can repos deploy independently or must they deploy together?

**Deployment Patterns:**
- **Sequential**: repo-a must deploy before repo-b
- **Coordinated**: Both must deploy within same window
- **Independent**: Can deploy in any order
- **Feature-flagged**: Deploy both, enable via flag

### Step 6: Generate CrossRepoAnalysis.md

Create comprehensive analysis artifact in the **primary** repository's artifact directory.

Primary repository determination:
- Repository with the "upstream" changes (exporter)
- If unclear, use the first PR's repository

## CrossRepoAnalysis.md Template

```markdown
---
date: <ISO-8601 timestamp>
repositories: [owner/repo-a, owner/repo-b]
prs: [PR-123, PR-456]
topic: "Cross-Repository Correlation Analysis"
tags: [cross-repo, correlation, dependencies]
status: complete
---

# Cross-Repository Correlation Analysis

## Repository Relationship

| Repository | Role | PRs | Primary |
|------------|------|-----|---------|
| owner/repo-a | API Server (exports) | PR-123 | ✓ |
| owner/repo-b | Client (imports) | PR-456 | |

## Dependency Graph

```
owner/repo-a
  └─ exports ─→ owner/repo-b
     - UserProfile type
     - /api/users endpoint
```

## Shared Interfaces

### Interface: `UserProfile` Type

- **Type**: type-export
- **Defined in**: [repo-a/src/types/user.ts:15-25](repo-a/src/types/user.ts#L15-L25)
- **Consumed in**: [repo-b/src/api/client.ts:8](repo-b/src/api/client.ts#L8)
- **Status**: ⚠ Mismatch

**Current State:**
- repo-a adds `lastLogin: Date` field at line 22
- repo-b imports UserProfile but doesn't handle `lastLogin`

### Interface: `/api/users` Endpoint

- **Type**: api-endpoint
- **Defined in**: [repo-a/src/routes/users.ts:45-80](repo-a/src/routes/users.ts#L45-L80)
- **Consumed in**: [repo-b/src/services/userService.ts:33](repo-b/src/services/userService.ts#L33)
- **Status**: ✓ Aligned

## Cross-Repository Gaps

### Gap: Missing Consumer Update for `lastLogin` Field

- **Severity**: Must
- **Affects**: repo-b (consumer)
- **Issue**: repo-a adds `lastLogin` field to UserProfile, but repo-b doesn't handle it
- **Evidence**: 
  - Added: [repo-a/src/types/user.ts:22](repo-a/src/types/user.ts#L22) - `lastLogin: Date`
  - Missing: [repo-b/src/api/client.ts](repo-b/src/api/client.ts) - no handling for new field
- **Recommendation**: Update repo-b to consume or explicitly ignore the new field
- **Cross-Reference**: (See PR-456-repo-b for consumer update needed)

### Gap: [Title]

- **Severity**: Should|Could
- **Affects**: [repository]
- **Issue**: [description]
- **Evidence**: 
  - [file:line references]
- **Recommendation**: [specific guidance]

## Deployment Considerations

### Recommended Deployment Order

1. **First**: owner/repo-a (PR-123)
   - Reason: Provides new field that repo-b will consume
   - Prerequisites: None
   
2. **Second**: owner/repo-b (PR-456)
   - Reason: Consumes new field from repo-a
   - Prerequisites: repo-a deployed

### Deployment Strategy

- **Pattern**: Sequential
- **Window**: Deploy repo-a, verify, then deploy repo-b
- **Rollback**: If repo-b deployment fails, repo-a can remain (backward compatible)

### Feature Flag Coordination

- No feature flag coordination required for this change set

*OR*

- **Flag Name**: `enable_last_login_display`
- **repos Affected**: repo-a (API), repo-b (UI)
- **Rollout**: Enable flag after both repos deployed

### Migration Requirements

- [ ] No database migrations required
- [ ] No data backfill required

*OR*

- **Migration**: repo-a requires migration `add_last_login_column`
- **Order**: Run migration before deploying repo-a code
- **Reversibility**: Migration is reversible via `remove_last_login_column`

## Summary

| Metric | Count |
|--------|-------|
| Interface contracts analyzed | X |
| Mismatches found | Y |
| Must-address gaps | Z |
| Should-consider gaps | W |

**Recommended Deployment Order**: repo-a → repo-b

**Key Findings**:
1. [Most critical cross-repo issue]
2. [Second most critical issue]
```

## Validation Checklist

Before marking complete:
- [ ] All per-repo artifacts loaded (ImpactAnalysis.md, GapAnalysis.md for each PR)
- [ ] Dependency graph includes all identified dependencies
- [ ] All shared interfaces documented with file:line references
- [ ] All mismatches have severity assigned (Must/Should/Could)
- [ ] Deployment order is actionable (not just "be careful")
- [ ] CrossRepoAnalysis.md written to primary repo's artifact directory
- [ ] Cross-references use notation: `(See PR-<number>-<repo-slug> for...)`

## Error Handling

### Partial Artifact Availability

If some repositories have artifacts but others don't:
1. Document which repos have complete artifacts
2. Proceed with correlation for available repos
3. Note limitations: "Correlation limited to repos X and Y; repo Z artifacts incomplete"

### Unidentifiable Dependencies

If dependency direction is unclear:
1. Document both possibilities
2. Flag for human review: "Dependency direction unclear—verify during review"

### No Cross-Repo Dependencies Found

If analysis finds no shared interfaces:
1. Document the analysis was performed
2. Note: "No shared interfaces identified between repositories"
3. Include brief explanation of what was checked
4. CrossRepoAnalysis.md still generated (documents that analysis was done)

## Completion

Report:
- Artifact path: `.paw/reviews/<primary-identifier>/CrossRepoAnalysis.md`
- Interface contracts analyzed count
- Mismatches found count
- Recommended deployment order summary
