---
name: prp-framework
description: Product Requirement Prompt framework for generating comprehensive PRDs, implementation plans, and feature specifications. Use when creating technical specs, planning features, investigating issues, or documenting requirements for development.
---

# PRP Framework Skill

## Triggers

Use this skill when you see:
- prp, prd, implementation plan, feature spec
- requirements document, technical spec
- issue investigation, root cause analysis
- feature planning, epic breakdown

## Instructions

### PRP Types Overview

| Type | Use Case | Output |
|------|----------|--------|
| Feature PRP | New feature development | Full PRD + implementation plan |
| Bug Investigation PRP | Debug complex issues | Root cause + fix plan |
| Refactor PRP | Code improvement | Impact analysis + migration plan |
| Integration PRP | Third-party integrations | API mapping + implementation |
| Migration PRP | System migrations | Risk analysis + rollback plan |

### Feature PRP Template

```markdown
# Feature PRP: [Feature Name]

## Executive Summary
[2-3 sentence overview of what this feature does and why it matters]

## Problem Statement
### Current State
[Describe the current situation and pain points]

### Desired State
[Describe the ideal end state]

### Success Metrics
- [ ] Metric 1: [Measurable outcome]
- [ ] Metric 2: [Measurable outcome]

## Requirements

### Functional Requirements
| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-1 | [Requirement] | Must Have | |
| FR-2 | [Requirement] | Should Have | |
| FR-3 | [Requirement] | Nice to Have | |

### Non-Functional Requirements
- **Performance**: [Response time, throughput]
- **Scalability**: [Expected load, growth]
- **Security**: [Auth, data protection]
- **Accessibility**: [WCAG level, requirements]

### Out of Scope
- [Explicitly excluded item 1]
- [Explicitly excluded item 2]

## Technical Design

### Architecture Overview
[High-level architecture diagram or description]

### Data Model
```
[Entity/Schema definitions]
```

### API Design
```
[Endpoint definitions]
```

### Dependencies
- [Internal dependency 1]
- [External dependency 1]

## Implementation Plan

### Phase 1: Foundation
**Duration**: [X days/weeks]
**Tasks**:
1. [ ] Task 1
2. [ ] Task 2

### Phase 2: Core Implementation
**Duration**: [X days/weeks]
**Tasks**:
1. [ ] Task 1
2. [ ] Task 2

### Phase 3: Polish & Testing
**Duration**: [X days/weeks]
**Tasks**:
1. [ ] Task 1
2. [ ] Task 2

## Testing Strategy

### Unit Tests
- [Test category 1]
- [Test category 2]

### Integration Tests
- [Test scenario 1]
- [Test scenario 2]

### E2E Tests
- [User flow 1]
- [User flow 2]

## Rollout Plan

### Feature Flags
- `feature_name_enabled`: [Description]

### Rollout Stages
1. **Internal**: [Criteria]
2. **Beta**: [X% of users, criteria]
3. **GA**: [Full rollout]

### Rollback Plan
[How to rollback if issues arise]

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Strategy] |

## Timeline

| Milestone | Date | Owner |
|-----------|------|-------|
| Design Complete | [Date] | [Name] |
| Implementation Complete | [Date] | [Name] |
| Testing Complete | [Date] | [Name] |
| Release | [Date] | [Name] |

## Appendix
- [Link to designs]
- [Link to related docs]
- [Technical references]
```

### Bug Investigation PRP Template

```markdown
# Bug Investigation PRP: [Bug Title]

## Issue Summary
**Reported**: [Date]
**Severity**: [Critical/High/Medium/Low]
**Affected Users**: [Scope]

### Symptoms
[What users are experiencing]

### Expected Behavior
[What should happen]

### Actual Behavior
[What is happening]

## Investigation

### Reproduction Steps
1. [Step 1]
2. [Step 2]
3. [Observe: Error/Unexpected behavior]

### Environment
- **Browser/Client**: [Version]
- **OS**: [Version]
- **Backend Version**: [Version]
- **Database**: [Version]

### Evidence
- [Log snippets]
- [Error messages]
- [Screenshots]

## Root Cause Analysis

### Hypothesis 1: [Theory]
**Evidence For**: [Supporting data]
**Evidence Against**: [Contradicting data]
**Verdict**: [Confirmed/Ruled Out/Needs More Data]

### Hypothesis 2: [Theory]
...

### Confirmed Root Cause
[Detailed explanation of the actual cause]

### Contributing Factors
- [Factor 1]
- [Factor 2]

## Fix Plan

### Immediate Fix
[Quick fix to stop the bleeding]

### Permanent Fix
[Proper solution]

### Code Changes
```
[Files to modify and changes needed]
```

### Testing the Fix
1. [Verification step 1]
2. [Verification step 2]

## Prevention

### Process Improvements
- [Improvement 1]

### Technical Improvements
- [Improvement 1]

### Monitoring
- [Alert/metric to add]
```

### Refactor PRP Template

```markdown
# Refactor PRP: [Component/System Name]

## Current State Assessment

### Code Quality Issues
- [ ] [Issue 1]: [Location, impact]
- [ ] [Issue 2]: [Location, impact]

### Technical Debt
| Item | Severity | Effort | Impact |
|------|----------|--------|--------|
| [Debt item] | High | Large | [Impact] |

### Pain Points
- [Developer pain point 1]
- [Performance pain point 1]

## Proposed Changes

### Architecture Changes
[Before/After comparison]

### Code Changes
| Current | Proposed | Rationale |
|---------|----------|-----------|
| [Pattern A] | [Pattern B] | [Why] |

### API Changes
[Breaking changes, if any]

## Impact Analysis

### Affected Components
- [Component 1]: [How affected]
- [Component 2]: [How affected]

### Breaking Changes
- [Change 1]: [Migration path]

### Performance Impact
- [Expected improvement/degradation]

## Migration Plan

### Phase 1: Preparation
- [ ] Add feature flags
- [ ] Create migration scripts
- [ ] Update documentation

### Phase 2: Incremental Migration
- [ ] Migrate [component 1]
- [ ] Migrate [component 2]

### Phase 3: Cleanup
- [ ] Remove old code
- [ ] Remove feature flags
- [ ] Update tests

### Rollback Strategy
[How to rollback at each phase]

## Success Criteria
- [ ] [Metric 1 improved by X%]
- [ ] [All tests passing]
- [ ] [No performance regression]
```

### Quick PRP (Lightweight)

For smaller features or quick tasks:

```markdown
# Quick PRP: [Title]

## What
[1-2 sentences describing the change]

## Why
[Business/technical justification]

## How
[High-level approach]

## Tasks
1. [ ] [Task 1]
2. [ ] [Task 2]
3. [ ] [Task 3]

## Testing
- [ ] [Test 1]
- [ ] [Test 2]

## Done When
- [ ] [Acceptance criterion 1]
- [ ] [Acceptance criterion 2]
```

### Best Practices

1. **Start with Why**: Always explain the business value
2. **Be Specific**: Vague requirements lead to rework
3. **Include Acceptance Criteria**: Define "done"
4. **Consider Edge Cases**: Document error handling
5. **Plan for Failure**: Include rollback strategies
6. **Get Feedback Early**: Share drafts before implementing
7. **Keep Updated**: PRPs are living documents
8. **Link Everything**: Connect to issues, PRs, docs

### Converting PRP to Tasks

After PRP approval, create Archon tasks:

```python
# For each implementation phase
manage_task("create",
    project_id="...",
    title="[Phase]: [Task name]",
    description="From PRP: [link]\n\nAcceptance criteria:\n- [ ] ...",
    feature="prp-feature-name"
)
```
