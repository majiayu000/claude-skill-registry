---
name: paw-review-impact
description: Analyzes system-wide impact of PR changes including integration effects, breaking changes, performance, and security implications.
---

# Impact Analysis Activity Skill

Analyze system-wide impact of PR changes using understanding artifacts from the Understanding stage.

> **Reference**: Follow Core Review Principles from `paw-review-workflow` skill.

## Responsibilities

- Build integration graph showing what depends on changed code
- Detect breaking changes to public APIs, data models, and interfaces
- Assess performance implications (algorithms, loops, database queries)
- Evaluate security and authorization changes
- Assess design and architecture fit
- Evaluate user impact (end-users and developer-users)
- Document deployment considerations and migration needs
- Produce comprehensive ImpactAnalysis.md artifact

## Non-Responsibilities

- Code quality or gap identification (handled by paw-review-gap)
- Generating review comments (Output stage skills)
- Workflow orchestration (handled by workflow skill)

## Prerequisites

Verify these artifacts exist at `.paw/reviews/<identifier>/`:
- `ReviewContext.md` (PR metadata and parameters)
- `CodeResearch.md` (baseline codebase understanding)
- `DerivedSpec.md` (what the PR is trying to achieve)

If any artifact is missing, report the blocker and do not proceed.

## Step 1: Integration Graph Building

Identify what code depends on the changes:

### Parse Changed Files

- Extract imports, exports, and public API surfaces from changed files
- Use language-appropriate patterns (import/export for JS/TS, import for Python, etc.)
- Record all public symbols (functions, classes, constants) that were modified

### Map Downstream Consumers

- Search for files that import modified modules (one-hop search)
- Identify code that calls modified functions or uses modified classes
- Document integration points with file:line references

### Heuristics

- Parse import statements using regex patterns per language
- Search codebase for symbol references (limit to one level deep to avoid exponential search)
- Record both direct and indirect dependencies

### Output

Integration points table with component, relationship, and impact description

## Cross-Repository Impact

When reviewing PRs across multiple repositories:

### Detection

Cross-repo impact analysis applies when:
- Multiple PRs are being reviewed (separate artifact directories exist)
- ReviewContext.md contains `related_prs` entries
- `paw_get_context` returned `isMultiRootWorkspace: true`

### API Contract Identification

Identify contracts between repositories:

- **Shared Types**: Type definitions used across repos (often in `@types/`, `shared/`, or package exports)
- **API Endpoints**: REST/GraphQL endpoints consumed by other repos
- **Event Schemas**: Message formats for pub/sub or event-driven communication
- **Package Exports**: Public interfaces from shared packages

### Cross-Repo Breaking Change Detection

For each breaking change identified:
1. Check if the change affects contracts used by other PRs in the review set
2. Flag breaking changes that require coordinated updates across repos
3. Document which PR depends on which

**Cross-Repository Breaking Change Types:**
- Type export changes affecting consumers in other repos
- API endpoint changes consumed by other repos
- Shared configuration schema changes
- Package version constraints that conflict

### Dependency Direction

Document which repository depends on which:

| Provider PR | Consumer PR | Contract | Direction |
|-------------|-------------|----------|-----------|
| PR-123-api | PR-456-frontend | `/api/users` endpoint | api → frontend |
| PR-123-api | PR-456-frontend | `UserType` export | api → frontend |

### Update ImpactAnalysis.md Template

Add to each ImpactAnalysis.md when in multi-repo mode:

```markdown
## Cross-Repository Dependencies

| This PR Changes | Affects PR | Type | Migration |
|-----------------|------------|------|-----------|
| `api/types.ts` exports | PR-456-frontend | Breaking | Update types import |
| `/api/users` endpoint | PR-456-frontend | Compatible | No action needed |

**Deployment Order:** PR-123-api MUST deploy before PR-456-frontend
```

### Error Handling

If cross-repo analysis is blocked (e.g., can't access other repository):
- Document the limitation
- Proceed with single-repo analysis
- Note potential cross-repo impacts that couldn't be verified

## Step 2: Breaking Change Detection

Compare before/after to identify incompatible changes:

### Function Signature Changes

- Parameter count changed (added/removed required parameters)
- Parameter types changed (string → number, etc.)
- Return type changed
- Function renamed or removed

### Configuration Schema Changes

- Required config keys removed
- Config value types changed without backward compatibility
- New required config keys added without defaults

### Data Model Changes

- Database schema: required fields added/removed without migration
- API contracts: request/response shapes changed
- File formats: incompatible changes to serialization

### Exported Symbols

- Public exports removed from modules
- API endpoints removed or renamed
- Public classes/functions deleted

### Heuristics

- Diff public function signatures between base and head
- Check for removed exports that other files import
- Identify new required fields in schemas/models
- Flag removals of auth middleware or permission checks

### Output

Breaking changes table with change description, type, and migration needs

## Step 3: Performance Assessment

Evaluate algorithmic and resource usage changes:

### Algorithmic Complexity

- New nested loops (depth ≥2)
- New recursion without memoization
- Array/map operations inside loops
- Sorting or filtering large datasets

### Database and External Calls

- New database queries (especially in loops)
- Queries not batched or cached
- N+1 query patterns introduced
- New external HTTP/API calls

### Hot Path Modifications

- Changes to frequently-called functions (from DerivedSpec.md)
- Modifications to critical user-facing paths
- Changes to startup/initialization code

### Resource Usage

- Large allocations in loops
- Memory-intensive operations
- File I/O in hot paths
- Unbounded collections or buffers

### Heuristics

- Flag nested loops with depth ≥2
- Identify new DB calls not using batch patterns
- Note changes to functions mentioned in DerivedSpec as performance-sensitive
- Look for new large array operations

### Output

Performance implications section with findings and severity

## Step 4: Security & Authorization Review

Assess security-relevant changes:

### Authentication & Authorization

- Auth middleware removed or bypassed
- Permission checks removed or relaxed
- Role checks modified or eliminated
- Session handling changes

### Input Validation

- Validation removed from user inputs
- New endpoints without input sanitization
- SQL injection risks (raw SQL without parameters)
- XSS risks (unescaped user content in responses)

### Data Exposure

- Sensitive fields added to API responses
- Logging of secrets or PII introduced
- Broader data access granted

### Cryptography

- Weak algorithms introduced
- Key management changes
- TLS/encryption removed

### Heuristics

- Flag auth check removals
- Identify new user input not validated
- Search for raw SQL or string concatenation in queries
- Note changes to CORS, CSP, or security headers

### Output

Security implications section with risks and recommendations

## Step 5: Design & Architecture Assessment

Evaluate whether the change fits well within the system:

### Architectural Fit

- Does this change belong in this codebase or should it be in a library/separate service?
- Does it integrate well with existing architectural patterns?
- Is it following the system's design principles?
- Does it add appropriate abstractions or violate existing ones?

### Timing Assessment

- Is now a good time to add this functionality?
- Are there dependencies or prerequisites missing?
- Should this wait for related work to complete?

### System Integration

- How does this fit into the broader system design?
- Does it create new coupling or dependencies that will be hard to maintain?
- Is the integration approach consistent with existing patterns?

### Heuristics

- Check if new code duplicates functionality that exists elsewhere
- Identify if this creates circular dependencies
- Note if this should be extracted to shared library (used by >2 components)
- Flag if architectural patterns diverge from system design docs

### Output

Design assessment section with architectural fit, timing, and integration evaluation

## Step 6: User Impact Evaluation

Assess impact on both end-users and developer-users:

### End-User Impact

- How does this affect user-facing functionality?
- Does it improve user experience or degrade it?
- Are there UI/UX changes that need review?
- Performance impact on user-facing operations?

### Developer-User Impact

For developers who will use this code:
- Is the API clear and intuitive?
- Is it easy to use correctly and hard to use incorrectly?
- Does it have good defaults?
- Is error handling helpful?

### Heuristics

- Identify public API changes and assess usability
- Note user-facing performance changes (page load, response time)
- Check if error messages are clear and actionable
- Assess if new configuration is intuitive

### Output

User impact section covering end-users and developer-users

## Step 7: Code Health Trend Assessment

Evaluate whether changes improve or degrade overall system health:

### Code Health Indicators

- Is this change reducing technical debt or adding to it?
- Is complexity being added appropriately or accumulating unnecessarily?
- Are abstractions making code clearer or more convoluted?
- Long-term maintainability impact?

### Quality Trends

- Does this improve code organization or fragment it further?
- Are patterns becoming more consistent or more varied?
- Is documentation getting better or falling behind?
- Test coverage improving or degrading?

### Heuristics

- Compare new code complexity to baseline from CodeResearch.md
- Note if change reduces duplication or adds it
- Check if change follows or breaks established patterns
- Assess if abstractions reduce or increase cognitive load

### Output

Code health trend assessment included in Risk Assessment section

## Step 8: Deployment Considerations

Document what's needed for safe rollout:

### Database Migrations

- Schema changes requiring migration scripts
- Data backfill or transformation needed
- Rollback strategy for schema changes

### Configuration Changes

- New environment variables required
- Changed config defaults
- Feature flags needed for gradual rollout

### Dependencies & Versioning

- New library dependencies
- Version bumps with breaking changes
- External service integrations

### Rollout Strategy

- Gradual rollout recommendations
- Monitoring and alerting needs
- Rollback plan if issues arise

### Output

Deployment section with migration steps, config changes, and rollout guidance

## Step 9: Generate ImpactAnalysis.md

Create comprehensive impact analysis artifact at `.paw/reviews/<identifier>/ImpactAnalysis.md`:

```markdown
---
date: <timestamp>
git_commit: <head SHA>
branch: <head branch>
repository: <repo>
topic: "Impact Analysis for <PR Title or Branch>"
tags: [review, impact, integration]
status: complete
---

# Impact Analysis for <PR Title or Branch>

## Summary

<1-2 sentence overview of impact scope and risk level>

## Baseline State

<From CodeResearch.md: how the system worked before these changes>

## Integration Points

<Components/modules that depend on changed code>

| Component | Relationship | Impact |
|-----------|--------------|--------|
| `module-a` | imports `changed-module` | Breaking: function signature changed |
| `component-b` | calls `changed-function()` | Safe: backward compatible |

## Breaking Changes

<Public API changes, removed features, incompatibilities>

| Change | Type | Migration Needed |
|--------|------|------------------|
| `processData(data, options)` → `processData(data)` | signature | Yes - update all call sites to remove options param |
| Config key `oldKey` removed | config | Yes - update config files to use `newKey` |

**Migration Impact:** <assessment of effort required>

## Performance Implications

**Algorithmic Changes:**
- <description of complexity changes>

**Database Impact:**
- <new queries, indexing needs>

**Hot Path Changes:**
- <modifications to performance-critical code>

**Overall Assessment:** Low | Medium | High performance risk

## Security & Authorization Changes

**Authentication/Authorization:**
- <auth middleware or permission check changes>

**Input Validation:**
- <new user inputs and their validation>

**Data Exposure:**
- <sensitive data handling changes>

**Overall Assessment:** Low | Medium | High security risk

## Design & Architecture Assessment

**Architectural Fit:**
- <Does this belong in codebase vs library? Integration with architectural patterns?>

**Timing Assessment:**
- <Is now a good time for this functionality? Dependencies or prerequisites?>

**System Integration:**
- <How does this fit into broader system design? Coupling or dependency concerns?>

**Overall Assessment:** Well-integrated | Has concerns | Needs redesign

## User Impact Evaluation

**End-User Impact:**
- <User-facing functionality changes, UX improvements/degradations, performance impact>

**Developer-User Impact:**
- <API clarity, ease of use, good defaults, error handling helpfulness>

**Overall Assessment:** Positive | Neutral | Negative user impact

## Deployment Considerations

**Database Migrations:**
- <migration scripts needed>

**Configuration Changes:**
- <new env vars, config updates>

**Dependencies:**
- <new libraries, version changes>

**Rollout Strategy:**
- <gradual rollout, feature flags, monitoring>

**Rollback Plan:**
- <how to revert if issues arise>

## Dependencies & Versioning

**New Dependencies:**
- <libraries added>

**Version Changes:**
- <dependency version bumps>

**External Services:**
- <new integrations or API changes>

## Risk Assessment

**Overall Risk:** Low | Medium | High

**Rationale:**
<Why this risk level? Consider breaking changes, performance, security, deployment complexity, code health trend>

**Code Health Trend:**
- Is this change improving or degrading overall system code health?
- Does it reduce technical debt or add to it?
- Is complexity being added appropriately or accumulating unnecessarily?
- Long-term maintainability impact?

**Mitigation:**
<Steps to reduce risk: testing, gradual rollout, monitoring, rollback plan>
```

## Guardrails

### Evidence Required

- All findings must have file:line references
- Integration points must cite actual import/usage locations
- Breaking changes must show before/after signatures

### Baseline-Informed

- Use CodeResearch.md to understand what changed
- Compare current integration graph to baseline patterns
- Reference DerivedSpec.md for hot paths and critical functionality

### No Speculation

- Only flag issues with concrete evidence
- Don't invent problems that aren't visible in the diff
- When uncertain, ask clarifying questions

### Scope

- Focus on system-wide impact, not code quality (Gap Analysis handles that)
- Document what changed and what it affects, not whether it's good/bad

## Validation Checklist

Before completing, verify:
- [ ] Integration points identified with file:line references
- [ ] Breaking changes documented with migration needs
- [ ] Performance implications assessed
- [ ] Security changes evaluated
- [ ] Design & architecture assessment completed
- [ ] User impact evaluation completed (end-users and developer-users)
- [ ] Deployment considerations documented
- [ ] Risk assessment includes rationale, code health trend, and mitigation
- [ ] All findings supported by evidence from diff or CodeResearch.md
- [ ] ImpactAnalysis.md artifact generated with all required sections
- [ ] Baseline state from CodeResearch.md included

## Completion Response

```
Activity complete.
Artifact saved: .paw/reviews/<identifier>/ImpactAnalysis.md
Status: Success

Key findings:
- X integration points identified
- Y potential breaking changes
- Security risk: [Low|Medium|High]
- Deployment complexity: [Low|Medium|High]
```
