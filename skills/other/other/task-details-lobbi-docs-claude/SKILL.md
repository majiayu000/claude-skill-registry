---
name: task-details
description: Enriches Jira tasks with comprehensive context, requirements analysis, and technical details through intelligent extraction, dependency mapping, and historical analysis
version: 1.0.0
trigger_phrases:
  - "enrich task"
  - "task details"
  - "analyze requirements"
  - "add context to issue"
  - "expand ticket"
  - "detail enhancement"
  - "analyze jira issue"
  - "gather context"
  - "extract requirements"
  - "estimate complexity"
categories: ["jira", "requirements", "analysis", "enrichment"]
---

# Task Details Enrichment Skill

Automatically enrich Jira tasks with comprehensive context, technical requirements, dependencies, and estimates.

## When to Use

- Issue lacks sufficient detail for implementation
- Need to extract hidden requirements from descriptions
- Analyzing issue complexity for estimation
- Identifying dependencies and blockers
- Converting vague requirements into technical details
- Preparing issues for sprint planning

## Core Capabilities

| Capability | Purpose |
|-----------|---------|
| Context Extraction | Parse requirements, acceptance criteria, constraints |
| Dependency Mapping | Identify linked issues, code deps, team deps, blockers |
| Complexity Assessment | Estimate story points, risk factors, historical comparison |
| Requirement Decomposition | Break down epics, extract criteria, identify edge cases |
| Historical Analysis | Find similar resolved issues, extract patterns |

## Decision Tree

```
Analyze Issue
├─ Epic? → Epic Decomposition
├─ Missing Criteria? → Acceptance Criteria Extraction
├─ Unclear Complexity? → Complexity Analysis
├─ Unknown Dependencies? → Dependency Mapping
├─ Unclear Technical Approach? → Technical Design
├─ Missing Tests? → Test Case Generation
└─ Sprint Context Needed? → Sprint Context Analysis
```

## Epic Decomposition

**When:** Epic type, vague requirements, multi-sprint work

**Process:**
1. Extract business objectives and success metrics
2. Identify user journeys and personas
3. Break into stories with acceptance criteria
4. Map story dependencies
5. Create phased roadmap

**Example Output:**
```markdown
# Epic Decomposition: EPIC-001

## Business Objectives
- Primary goal: [What problem solved?]
- Success metrics: [ROI/impact?]

## Stories by Phase
### Phase 1: Foundation (Sprint 1)
- STORY-001: [Title] (5 pts) → Depends on [deps]
- STORY-002: [Title] (3 pts)

### Phase 2: Core (Sprint 2-3)
- STORY-003: [Title] (8 pts) → Depends on STORY-001

## Dependency Graph
STORY-001 → STORY-003 → STORY-005

## Total Effort
- Points: 24 | Sprints: 4 | Team: 2-3 devs
```

## Acceptance Criteria Extraction

**When:** Vague/missing criteria, implicit requirements

**Extraction Patterns:**
- Modal verbs: must, should, shall, will, requires, needs
- Behavior keywords: when, if, then, after, before, given
- Constraints: only, except, within X time, at least, max

**Example Output:**
```markdown
# Acceptance Criteria: ISSUE-001

## Extracted Criteria

### Functional
- [ ] AC1: User can submit form when all required fields filled
- [ ] AC2: System sends confirmation email within 1 minute

### Non-Functional
- [ ] AC3: Form submission < 2 seconds
- [ ] AC4: Mobile support (iOS 14+, Android 10+)

### Security
- [ ] AC5: TLS 1.3 encryption in transit
- [ ] AC6: Rate limit: 5 submissions/hour per user

## Test Scenarios
```gherkin
Given user on contact form
When user enters valid data
Then form submits successfully
And confirmation email sent
```

## Missing Info (Needs Clarification)
- Email service failure behavior?
- Max character limits?
- Duplicate submission handling?
```

## Complexity Analysis

**When:** Estimate missing/unclear, assess technical risk

**Complexity Scoring:**
| Factor | Weight |
|--------|--------|
| Code Changes | 0.25 |
| Integration Points | 0.20 |
| Risk Level | 0.20 |
| Testing Complexity | 0.15 |
| Dependencies | 0.10 |
| Uncertainty | 0.10 |

**Story Point Mapping:**
- 1-10 weighted score → 1 pt (trivial)
- 11-20 → 2 pts (simple)
- 21-30 → 3 pts (moderate)
- 31-40 → 5 pts (complex)
- 41-50 → 8 pts (very complex)
- 51+ → 13 pts or break down

**Example Output:**
```markdown
# Complexity: ISSUE-001

## Summary
- **Points:** 5 | **Confidence:** Medium (70%)
- **Risk:** Medium | **Duration:** 2-3 days

## Code Impact
- Files: 8 | LOC: 300-400 | New Files: 2-3
- Integration Points: Auth0, DB, 3 services
- Risk Factors: Security, DB migration

## Historical Comparison
- Similar issue PROJ-234 (8 pts, 4 days)
- Similar issue PROJ-189 (3 pts, 1 day)
- Team velocity: 25 pts/sprint | 2.5 days per 5-pt story

## Scoring
- Code Changes: 3/5 × 0.25 = 0.75
- Integration: 3/5 × 0.20 = 0.60
- Risk: 4/5 × 0.20 = 0.80
- Testing: 3/5 × 0.15 = 0.45
- Dependencies: 2/5 × 0.10 = 0.20
- Uncertainty: 3/5 × 0.10 = 0.30
- **Total: 3.10 → 5 Points**

## Recommended Actions Before Starting
- [ ] Clarify unclear requirements
- [ ] Define performance SLA
- [ ] Create rollback plan
- [ ] Security review acceptance criteria
```

## Dependency Mapping

**When:** Complex issues, cross-team work, risk assessment

**Dependency Types:**
1. Jira Links: Blocks/blocked by, parent/child, related
2. Code: Shared libs, API contracts, DB schemas, config
3. Team: Other team's work, shared resources, reviews
4. External: Third-party APIs, infrastructure, compliance

**Example Output:**
```markdown
# Dependency Analysis: ISSUE-001

## Summary
- Total: 7 | Blocking: 2 (CRITICAL) | Code: 3 | Team: 2 | External: 1

## Critical Path (5 days)
START → PROJ-100 (Auth API) → PROJ-123 (Current) → PROJ-124 (Frontend) → END

## Blocking Issues
### PROJ-100: Auth0 API Configuration
- Status: In Progress | ETA: 2 days
- Impact: Cannot start until credentials ready
- Action: Daily follow-up

### PROJ-111: Database Migration Framework
- Status: In Review | ETA: 1 day
- Impact: Need migration CLI for schema changes
- Action: Review and test PR locally

## Code Dependencies
- auth.service.ts: Stable, low risk
- user.model.ts: Active dev (PROJ-98), medium risk
- Auth0 API: Well-documented, low risk

## Team Dependencies
- Security Review (2-3 days after PR)
- API Documentation (1 day after merge)

## Risk Matrix
| Dependency | Type | Status | Risk | Mitigation |
|-----------|------|--------|------|-----------|
| PROJ-100 | Blocking | In Progress | High | Daily follow-up |
| PROJ-111 | Blocking | In Review | Medium | Review PR |
| Security | Team | Pending | Medium | Schedule early |

## Execution Order
1. **Pre-work (Days 1-2):** Wait for blockers, test migration, review docs
2. **Implementation (Days 3-4):** Coordinate, implement, write tests
3. **Review (Day 5):** Security, PR, deploy to staging

## Parallel Opportunities
- Write comprehensive tests (no blockers)
- Draft documentation (no blockers)
- Design API spec (no blockers)
```

## Technical Design Enhancement

**When:** Unclear approach, need architecture guidance, identify components

**Key Areas:**
- Architecture impact diagram (mermaid)
- Proposed code changes (1-2 examples)
- Database schema changes
- API endpoints
- Implementation patterns (token rotation, graceful degradation, security)
- Risk mitigation strategies
- Performance considerations and targets
- Testing strategy (unit, integration, security, performance)
- Rollout plan (dev → staging → prod with gradual rollout)
- Monitoring metrics and alerts

## Integration with MCP Tools

```typescript
const issue = await mcp.atlassian.getIssue(issueKey);
const criteria = extractAcceptanceCriteria(issue.fields.description);
const similarIssues = await mcp.atlassian.searchIssues(
  `text ~ "${issue.fields.summary}" AND status = Done`
);
const blockers = issue.fields.issuelinks.filter(l => l.type === 'Blocks');
await mcp.atlassian.updateIssue(issueKey, {
  fields: {
    customfield_10100: criteria,
    customfield_10101: estimatedPoints,
    description: enhancedDescription
  }
});
```

## Enrichment Automation

**Automatic Triggers:**
- Issue Created → Extract criteria, find similar issues, suggest estimate
- Ready for Development → Full dependency analysis, design suggestions, tests
- Assigned to Sprint → Capacity check, complexity re-assessment, resources
- Description Updated → Re-extract criteria, update estimate, flag risks

**Manual Commands:**
```bash
/enrich-task PROJ-123                    # Full enrichment
/enrich-task PROJ-123 --criteria-only   # Criteria only
/enrich-task PROJ-123 --complexity-only # Complexity only
/enrich-sprint "Sprint 24"               # Batch enrich sprint
```

## Best Practices

1. **Progressive Enrichment:** Start lightweight, add detail as issue progresses
2. **Human-in-the-Loop:** Flag uncertain analysis, provide confidence scores
3. **Context Preservation:** Link to sources, document reasoning
4. **Team Adaptation:** Learn from estimation accuracy, adapt to velocity
5. **Continuous Learning:** Track accuracy, refine models, update patterns

## Example: Enriching Vague Bug

**Before:**
```
Title: Login not working
Description: Users can't log in sometimes
```

**After:**
```markdown
## Missing Info (Critical)
- Reproduction steps?
- Affected users (all or subset)?
- Frequency (always, sometimes, rarely)?
- Browser/device specifics?
- Error messages?
- Correlation with deployments?

## Similar Issues
- PROJ-89: "Login timeout issues" (3 pts, 1 day)
  Root cause: Session expiry misconfiguration

## Investigation Steps
1. Check logs for auth errors
2. Review Auth0 dashboard
3. Test in different browsers
4. Check correlation with time periods
5. Review auth.service.ts changes

Cannot Estimate Without Reproduction → Move to "Needs More Info"
```

## Summary

This skill enables comprehensive task enrichment through:
- **Intelligent Extraction:** Auto-parse requirements from descriptions
- **Complexity Assessment:** Technical analysis with accurate estimates
- **Dependency Mapping:** Identify all blockers before work starts
- **Design Guidance:** Suggest architecture and patterns
- **Historical Learning:** Leverage past issues
- **MCP Integration:** Seamless Jira/Confluence automation

Use in EXPLORE phase to ensure comprehensive context before development.
