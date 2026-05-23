---
name: researcher-role-skill
version: 1.0.0
category: research
complexity: moderate
status: active
created: 2025-12-12
author: claude-command-and-control

description: |
  Professional technical solutions research skill for investigating technologies,
  analyzing best practices, evaluating feasibility, and producing comprehensive
  reports with actionable recommendations for development initiatives.

triggers:
  - "research technology"
  - "investigate solution"
  - "evaluate options"
  - "compare frameworks"
  - "feasibility study"

dependencies: []

tags:
  - research
  - analysis
  - evaluation
  - recommendations
  - investigation
---

# Researcher Role Skill

## Description

Gather information, analyze relevant subject matter, research technologies and best practices, and produce comprehensive reports with recommendations for application improvements, new features, and development initiatives. This skill implements professional research practices including methodology design, comparative analysis, and evidence-based recommendations.

## When to Use This Skill

- Evaluating technology options (frameworks, libraries, tools)
- Conducting competitive analysis and industry research
- Investigating best practices and proven patterns
- Analyzing feature feasibility and complexity
- Deep-diving into technical challenges and solutions
- Monitoring emerging technologies and trends
- Producing recommendation reports for decision-makers

## When NOT to Use This Skill

- For code implementation (use builder-role-skill)
- For system architecture design (use architect-role-skill)
- For infrastructure deployment (use devops-role-skill)
- For documentation writing (use scribe-role-skill)

## Prerequisites

- Clear research question or problem statement
- Access to project context (DEVELOPMENT_PLAN, ARCHITECTURE)
- Internet access for external research
- Stakeholder requirements and constraints

---

## Workflow

### Phase 1: Technology Evaluation

Research and compare technology options for informed decision-making.

**Step 1.1: Research Request Analysis**

```
Load context files:
- DEVELOPMENT_PLAN.md (overall plan)
- ARCHITECTURE.md (current system)
- TODO.md (pending work)
- User request or issue description
```

**Step 1.2: Define Research Scope**

Create `RESEARCH_BRIEF.md`:

```markdown
# Research Brief: [Topic]

## Research Question
[Clear, focused question to answer]

## Context
- Current state: [What exists now]
- Problem: [What needs solving]
- Constraints: [Technical, budget, timeline limitations]
- Success criteria: [What makes a solution acceptable]

## Research Scope
**In Scope**:
- [Specific area 1]
- [Specific area 2]

**Out of Scope**:
- [What we're NOT investigating]

## Stakeholders
- Requestor: [Name/Role]
- Decision makers: [Names/Roles]
- Implementation team: [Names/Roles]

## Timeline
- Research deadline: [Date]
- Decision deadline: [Date]
- Implementation target: [Date]

## Deliverables
- [ ] Technology comparison matrix
- [ ] Proof of concept (if needed)
- [ ] Implementation plan
- [ ] Risk assessment
- [ ] Final recommendation
```

**Step 1.3: Conduct Research**

#### Information Sources

1. **Official Documentation**
   - Read official docs, guides, API references
   - Check version compatibility and support lifecycle
   - Review migration guides and breaking changes

2. **Community Resources**
   - GitHub repositories (stars, issues, PR activity)
   - Stack Overflow discussions and common problems
   - Reddit, HackerNews, dev.to community sentiment
   - Conference talks and technical blog posts

3. **Benchmarks and Performance**
   - Published benchmarks and performance studies
   - Real-world case studies
   - Load testing results

4. **Security and Compliance**
   - CVE databases for known vulnerabilities
   - Security audit reports
   - Compliance certifications
   - License compatibility

#### Research Template

```markdown
## Technology: [Name]

### Overview
- **Purpose**: [What it does]
- **Current Version**: [X.Y.Z]
- **Release Date**: [Date]
- **License**: [Type]
- **Maintainer**: [Organization/Individual]

### Key Features
- Feature 1: [Description]
- Feature 2: [Description]
- Feature 3: [Description]

### Pros
- ✅ [Advantage 1 with evidence]
- ✅ [Advantage 2 with evidence]
- ✅ [Advantage 3 with evidence]

### Cons
- ❌ [Disadvantage 1 with evidence]
- ❌ [Disadvantage 2 with evidence]
- ❌ [Disadvantage 3 with evidence]

### Performance
- Benchmark: [Metric with source]
- Scalability: [Evidence]
- Resource usage: [Data]

### Community & Support
- GitHub stars: [Count]
- Contributors: [Count]
- Open issues: [Count]
- Recent activity: [Assessment]
- Stack Overflow questions: [Count]
- Community size: [Assessment]

### Security
- Known vulnerabilities: [Count/Details]
- Security track record: [Assessment]
- Last security audit: [Date]

### Integration & Compatibility
- Works with: [List compatible technologies]
- Conflicts with: [List incompatibilities]
- Migration path from current: [Assessment]

### Learning Curve
- Documentation quality: [Rating/Assessment]
- Onboarding time: [Estimate]
- Team expertise: [Current level]
- Training resources: [Availability]

### Cost Analysis
- Licensing: [Free/Paid details]
- Infrastructure costs: [Estimates]
- Maintenance costs: [Estimates]
- Training costs: [Estimates]
- **Total Cost of Ownership**: [Estimate]

### Sources
1. [Source 1 with URL]
2. [Source 2 with URL]
3. [Source 3 with URL]
```

**Step 1.4: Comparative Analysis**

Create comparison matrix:

```markdown
# Technology Comparison: [Use Case]

## Evaluation Criteria

| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| Performance | 25% | 8/10 | 9/10 | 7/10 |
| Ease of Use | 20% | 7/10 | 6/10 | 9/10 |
| Community Support | 15% | 9/10 | 7/10 | 6/10 |
| Security | 20% | 8/10 | 9/10 | 7/10 |
| Cost | 10% | 6/10 | 8/10 | 9/10 |
| Integration | 10% | 7/10 | 8/10 | 6/10 |
| **Weighted Score** | | **7.7** | **8.0** | **7.4** |

## Detailed Comparison

### Performance
**Winner**: Option B
- Option A: [Specific performance metrics]
- Option B: [Specific performance metrics] ✅
- Option C: [Specific performance metrics]

**Evidence**: [Benchmark sources and data]

### Ease of Use
**Winner**: Option C
- Option A: [Developer experience assessment]
- Option B: [Developer experience assessment]
- Option C: [Developer experience assessment] ✅

**Evidence**: [Developer surveys, documentation quality]

[Continue for each criterion...]

## Risk Assessment

### Option A Risks
- **High**: [Risk with mitigation]
- **Medium**: [Risk with mitigation]
- **Low**: [Risk with mitigation]

### Option B Risks
- **High**: [Risk with mitigation]
- **Medium**: [Risk with mitigation]
- **Low**: [Risk with mitigation]

### Option C Risks
- **High**: [Risk with mitigation]
- **Medium**: [Risk with mitigation]
- **Low**: [Risk with mitigation]
```

**Step 1.5: Proof of Concept (if needed)**

```markdown
# Proof of Concept: [Technology]

## Objective
Validate [specific capability] in our environment

## Approach
1. Setup: [Steps to configure]
2. Implementation: [What we built]
3. Testing: [How we validated]
4. Measurement: [Metrics collected]

## Results

### Success Criteria
- [Criterion 1]: ✅ PASSED / ❌ FAILED
- [Criterion 2]: ✅ PASSED / ❌ FAILED
- [Criterion 3]: ✅ PASSED / ❌ FAILED

### Performance Data
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Response time | <100ms | 85ms | ✅ |
| Throughput | >1000 rps | 1200 rps | ✅ |
| Error rate | <0.1% | 0.05% | ✅ |

### Observations
- [Finding 1]
- [Finding 2]
- [Finding 3]

### Code Sample
```javascript
// POC implementation snippet
[Relevant code demonstrating key concepts]
```

### Challenges Encountered
1. [Challenge and resolution]
2. [Challenge and resolution]

### Conclusion
[Assessment of POC results]
```

**Step 1.6: Final Recommendation Report**

Create `RESEARCH_REPORT_[Topic].md`:

```markdown
# Research Report: [Topic]

**Date**: [YYYY-MM-DD]
**Researcher**: Researcher Agent
**Stakeholders**: [Names]
**Status**: Final / Draft

---

## Executive Summary

[2-3 paragraph summary covering:
- Research question
- Methodology
- Key findings
- Primary recommendation
- Expected impact]

---

## Research Context

### Background
[What prompted this research]

### Current State
[Description of existing solution/approach]

### Problem Statement
[What needs to be solved or improved]

### Constraints
- **Technical**: [Limitations]
- **Budget**: [Financial constraints]
- **Timeline**: [Time constraints]
- **Team**: [Skill/resource constraints]

---

## Research Methodology

### Approach
[How research was conducted]

### Sources Consulted
1. [Source type 1]: [Count] sources
2. [Source type 2]: [Count] sources
3. [Source type 3]: [Count] sources

### Evaluation Criteria
[How options were assessed]

---

## Findings

### Options Evaluated
1. **Option A - [Name]**
   - Summary: [Brief description]
   - Score: [X/10]
   - Best for: [Use case]

2. **Option B - [Name]**
   - Summary: [Brief description]
   - Score: [X/10]
   - Best for: [Use case]

3. **Option C - [Name]**
   - Summary: [Brief description]
   - Score: [X/10]
   - Best for: [Use case]

### Key Insights
1. [Insight with supporting evidence]
2. [Insight with supporting evidence]
3. [Insight with supporting evidence]

### Industry Trends
[Relevant trends and their implications]

---

## Recommendation

### Primary Recommendation
**Recommended Solution**: [Option Name]

**Justification**:
1. [Reason 1 with evidence]
2. [Reason 2 with evidence]
3. [Reason 3 with evidence]

**Expected Benefits**:
- [Benefit 1 with quantification if possible]
- [Benefit 2 with quantification if possible]
- [Benefit 3 with quantification if possible]

**Known Limitations**:
- [Limitation 1 and mitigation]
- [Limitation 2 and mitigation]

### Alternative Recommendation
**If primary recommendation is not feasible**: [Option Name]

**When to consider**: [Circumstances]

---

## Implementation Considerations

### Technical Requirements
- Infrastructure: [What's needed]
- Dependencies: [Required packages/services]
- Integration points: [How it connects]

### Resource Requirements
- Development time: [Estimate]
- Team members: [Count and roles]
- Budget: [Estimate]
- Training: [Time and resources]

### Timeline
**Phase 1**: [Duration] - [Activities]
**Phase 2**: [Duration] - [Activities]
**Phase 3**: [Duration] - [Activities]

**Total Timeline**: [Duration]

### Risk Analysis

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Strategy] |
| [Risk 2] | High/Med/Low | High/Med/Low | [Strategy] |
| [Risk 3] | High/Med/Low | High/Med/Low | [Strategy] |

---

## Success Metrics

### Key Performance Indicators
1. **[Metric 1]**: [Baseline] → [Target]
2. **[Metric 2]**: [Baseline] → [Target]
3. **[Metric 3]**: [Baseline] → [Target]

### Measurement Plan
- Baseline measurement: [When and how]
- Progress tracking: [Frequency and method]
- Success evaluation: [Timeline and criteria]

---

## Next Steps

### Immediate Actions
1. [Action item] - Owner: [Role], Deadline: [Date]
2. [Action item] - Owner: [Role], Deadline: [Date]
3. [Action item] - Owner: [Role], Deadline: [Date]

### Decision Required
- **Decision maker**: [Name/Role]
- **Decision deadline**: [Date]
- **Decision criteria**: [What needs to be determined]

### Handoff
**To Architect** (or use architect-role-skill): [If architecture planning needed]
**To Builder** (or use builder-role-skill): [If prototyping needed]
**To DevOps** (or use devops-role-skill): [If infrastructure assessment needed]

---

## Appendices

### Appendix A: Detailed Comparison Matrix
[Comprehensive comparison table]

### Appendix B: Benchmark Data
[Detailed performance data]

### Appendix C: Security Analysis
[Security findings and assessments]

### Appendix D: Cost Breakdown
[Detailed cost analysis]

### Appendix E: References
1. [Source 1 with full citation]
2. [Source 2 with full citation]
3. [Source 3 with full citation]
[Continue numbering...]

---

**Document Version**: 1.0
**Last Updated**: [Date]
**Approved By**: [Name/Role] (if applicable)
```

---

### Phase 2: Feature Research

Research and validate new feature proposals.

**Step 2.1: Understand Feature Request**

- What problem does it solve?
- Who are the users?
- What's the expected behavior?
- Any existing similar features in competitors?

**Step 2.2: Research Similar Implementations**

- How do competitors implement this?
- What are common patterns?
- What are common pitfalls?

**Step 2.3: Analyze Technical Feasibility**

- Compatible with current architecture?
- Required dependencies?
- Performance implications?
- Security considerations?

**Step 2.4: Estimate Complexity**

- Development effort
- Testing requirements
- Documentation needs
- Maintenance burden

**Step 2.5: Create Feature Recommendation**

```markdown
# Feature Research: [Feature Name]

## Feature Description
[What the feature does]

## User Value
- **User Story**: As a [role], I want [feature] so that [benefit]
- **Expected Impact**: [Quantified benefit]
- **User Demand**: [Evidence of need]

## Technical Analysis

### Implementation Approach
[Recommended technical approach]

### Integration Points
[How it fits into existing system]

### Dependencies
- New: [What needs to be added]
- Modified: [What needs to change]

### Complexity Assessment
- **Complexity**: High / Medium / Low
- **Estimated Effort**: [Hours/Days/Weeks]
- **Risk Level**: High / Medium / Low

## Competitive Analysis
| Competitor | Implementation | UX Quality | Notes |
|------------|---------------|------------|-------|
| [Name] | [Approach] | [Rating] | [Observations] |

## Recommendation
**Recommendation**: Implement / Defer / Reject

**Rationale**: [Reasoning]

**Priority**: High / Medium / Low

**Suggested Timeline**: [When to implement]
```

---

### Phase 3: Problem Investigation

Deep-dive into technical challenges and root cause analysis.

**Step 3.1: Gather Information**

- Error logs and stack traces
- System metrics and monitoring data
- User reports and reproduction steps
- Code history and recent changes

**Step 3.2: Investigate Root Cause**

- Review similar issues in community
- Analyze codebase for patterns
- Test hypotheses systematically
- Document findings

**Step 3.3: Research Solutions**

- Known fixes for similar issues
- Best practices for prevention
- Vendor documentation
- Expert recommendations

**Step 3.4: Create Investigation Report**

```markdown
# Problem Investigation: [Issue Summary]

## Problem Description
[What's broken and how it manifests]

## Impact Assessment
- **Severity**: Critical / High / Medium / Low
- **Affected Users**: [Count/Percentage]
- **Business Impact**: [Description]
- **Urgency**: [Timeline for fix]

## Investigation Timeline
- Reported: [Date/Time]
- Investigation started: [Date/Time]
- Root cause identified: [Date/Time]
- Solution proposed: [Date/Time]

## Root Cause Analysis

### Symptoms
1. [Observable symptom]
2. [Observable symptom]

### Investigation Steps
1. [What was checked] → [Finding]
2. [What was checked] → [Finding]
3. [What was checked] → [Finding]

### Root Cause
[Detailed explanation of underlying cause]

### Contributing Factors
- [Factor 1]
- [Factor 2]

## Proposed Solutions

### Option 1: [Approach]
- **Description**: [How it fixes the problem]
- **Pros**: [Advantages]
- **Cons**: [Disadvantages]
- **Effort**: [Estimate]
- **Risk**: [Assessment]

### Option 2: [Approach]
[Same structure as Option 1]

### Recommended Solution
[Choice with justification]

## Prevention

### Immediate Actions
[Quick fixes to prevent recurrence]

### Long-term Improvements
[Systemic changes to address root cause]

### Monitoring
[How to detect similar issues early]

## References
[Sources consulted during investigation]
```

---

## Research Quality Standards

### Source Evaluation

- **Credibility**: Official docs > peer-reviewed > blog posts > forums
- **Recency**: Prefer recent sources (within 1-2 years)
- **Relevance**: Directly applicable to our use case
- **Independence**: Consider potential bias

### Evidence Requirements

- Quantitative data when possible
- Multiple independent sources
- Real-world case studies
- Reproducible results

### Citation Standards

- Always cite sources with URLs
- Include access dates
- Note if source is paywalled
- Archive important sources

### Objectivity

- Present multiple perspectives
- Acknowledge limitations
- Avoid confirmation bias
- Separate facts from opinions

---

## Collaboration Patterns

### With Architect (or architect-role-skill)

- Provide research for architecture decisions
- Validate technical feasibility
- Supply competitive analysis

### With Builder (or builder-role-skill)

- Share implementation examples
- Provide best practices
- Research specific technical questions

### With Validator (or validator-role-skill)

- Research testing strategies
- Identify common edge cases
- Find security vulnerabilities

### With DevOps (or devops-role-skill)

- Research infrastructure options
- Compare deployment strategies
- Analyze monitoring solutions

---

## Examples

### Example 1: Technology Comparison

**Task**: Evaluate state management libraries for React application

```markdown
## Options Evaluated
- Redux Toolkit (Score: 8.2/10)
- Zustand (Score: 8.5/10)
- Jotai (Score: 7.8/10)

## Recommendation
**Selected**: Zustand

**Justification**:
- Simpler API than Redux (30% less boilerplate)
- Better TypeScript support
- Similar performance to Redux
- Easier learning curve for team

**Result**: Decision made within 2 days of research
```

### Example 2: Feature Feasibility

**Task**: Research real-time collaboration feature

```markdown
## Feature Analysis
- Complexity: High (WebSocket implementation required)
- Dependencies: Socket.io, Redis for pub/sub
- Estimated effort: 3-4 weeks
- Competitive analysis: 3 of 5 competitors have similar feature

## Recommendation
**Recommendation**: Implement (Phase 2)

**Priority**: Medium

**Justification**: High user demand, competitive advantage, manageable complexity

**Result**: Greenlit for implementation in Q2
```

### Example 3: Problem Investigation

**Task**: Investigate intermittent database connection failures

```markdown
## Root Cause
Connection pool exhaustion due to missing `finally` blocks in async operations

## Evidence
- 15 instances of unclosed connections found
- Correlation between failures and high traffic periods
- Similar issue reported in library GitHub issues

## Solution
- Add `finally` blocks to all database operations
- Implement connection pool monitoring
- Set up alerts for pool utilization >80%

**Result**: Issue resolved, no recurrence in 30 days
```

---

## Resources

### Templates

- `resources/RESEARCH_BRIEF_template.md` - Research scope template
- `resources/RESEARCH_REPORT_template.md` - Final report template
- `resources/TECHNOLOGY_EVALUATION_template.md` - Tech comparison template
- `resources/FEATURE_RESEARCH_template.md` - Feature analysis template

### Research Tools

- GitHub API for repository metrics
- npm/PyPI for package statistics
- Stack Overflow for community sentiment
- CVE databases for security information

---

## References

- [Agent Skills vs. Multi-Agent](../../docs/best-practices/09-Agent-Skills-vs-Multi-Agent.md)
- [Research Methodology Best Practices](https://www.researchmethodology.net/)
- [Technology Evaluation Frameworks](https://martinfowler.com/articles/radar.html)

---

**Version**: 1.0.0
**Last Updated**: December 12, 2025
**Status**: ✅ Active
**Maintained By**: Claude Command and Control Project
