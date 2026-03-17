---
name: ralph-prompt-research
description: Generate Ralph-compatible prompts for research, analysis, and planning tasks. Creates prompts with systematic research phases, synthesis requirements, and deliverable specifications. Use when analyzing codebases, creating migration plans, researching technologies, auditing security, or any task requiring investigation before action.
---

# Ralph Prompt Generator: Research & Analysis

## Overview

Generates structured prompts for research, analysis, and planning tasks using the Ralph Wiggum technique. These prompts define clear research methodology, required sources, synthesis requirements, and concrete deliverables rather than code.

**Best For:**
- Codebase analysis and audits
- Security vulnerability assessments
- Technology research and comparison
- Migration planning
- Architecture design documents
- Performance analysis
- Dependency audits
- Documentation generation from code

**Ralph Philosophy**: This generator embraces the principle that failures are deterministic and fixable. Each research iteration builds on previous findings. Don't fear incomplete first passes—they're expected and provide data for deeper analysis in subsequent iterations.

## Quick Start

**Input Required:**
1. Research objective (what you need to understand/analyze)
2. Scope (what to include/exclude)
3. Deliverable format (report, plan, document)
4. Completion promise

**Generate prompt with:**
```
Generate a Ralph research prompt for:
Objective: [What to research/analyze]
Scope: [What's included]
Deliverable: [What to produce]
Promise: [COMPLETION_PHRASE]
```

## Prompt Generation Workflow

### Step 1: Define Research Scope

**Research Definition Template:**
```markdown
OBJECTIVE: [What question to answer or what to analyze]
SCOPE:
  Include: [What's in scope]
  Exclude: [What's explicitly out of scope]
SOURCES: [Where to look for information]
DELIVERABLE: [What artifact to produce]
SUCCESS: [How to know research is complete]
```

### Step 2: Map Research Phases

Standard research phases:

| Phase | Name | Purpose | Deliverable |
|-------|------|---------|-------------|
| 1 | Discovery | Identify what exists | Inventory/map |
| 2 | Analysis | Deep dive into findings | Analysis notes |
| 3 | Synthesis | Draw conclusions | Findings summary |
| 4 | Recommendations | Actionable next steps | Recommendation doc |
| 5 | Documentation | Final deliverable | Complete report |

### Step 3: Define Completion Criteria

**Research completion criteria must be:**
- Based on coverage (examined all relevant items)
- Based on depth (sufficient analysis per item)
- Based on deliverable completeness (all sections written)

**Examples:**
| Research Type | Completion Criteria |
|---------------|---------------------|
| Security audit | All OWASP categories checked, all findings documented |
| Codebase analysis | All modules examined, architecture documented |
| Tech comparison | All options evaluated against all criteria |
| Migration plan | All systems inventoried, migration steps defined |

### Step 4: Structure the Prompt

Use this template:

```markdown
# Research: [Research Title]

## Objective
[Clear statement of what this research aims to answer or analyze]

## Scope

### In Scope
- [Item 1 to analyze]
- [Item 2 to analyze]
- [Item 3 to analyze]

### Out of Scope
- [Explicitly excluded 1]
- [Explicitly excluded 2]

## Sources to Examine
- [Source type 1]: [Where to find]
- [Source type 2]: [Where to find]
- [Source type 3]: [Where to find]

---

## Phase 1: Discovery

### Objective
Create comprehensive inventory of [what to inventory].

### Tasks
1. [Discovery task 1]
2. [Discovery task 2]
3. [Discovery task 3]

### Deliverable: Inventory
Create `[filename].md` with:
```markdown
# [Inventory Title]

## Items Found
| # | Item | Location | Type | Notes |
|---|------|----------|------|-------|
| 1 | | | | |
| 2 | | | | |
```

### Phase 1 Success Criteria
- [ ] All [scope items] examined
- [ ] Inventory file created
- [ ] No areas unexplored

### Phase 1 Checkpoint
Document in inventory file:
```
DISCOVERY COMPLETE:
- Items found: [count]
- Areas examined: [list]
- Coverage: Complete/Partial
```

---

## Phase 2: Analysis

### Objective
Deep analysis of each discovered item.

### Analysis Framework
For each item, analyze:
- [Dimension 1]: [What to examine]
- [Dimension 2]: [What to examine]
- [Dimension 3]: [What to examine]

### Tasks
1. Analyze each item against framework
2. Document findings per item
3. Identify patterns across items
4. Note anomalies or concerns

### Deliverable: Analysis Notes
Create `[analysis-filename].md` with:
```markdown
# Analysis: [Item Name]

## [Dimension 1]
[Findings]

## [Dimension 2]
[Findings]

## [Dimension 3]
[Findings]

## Summary
[Key takeaways for this item]
```

### Phase 2 Success Criteria
- [ ] All inventory items analyzed
- [ ] Analysis notes for each item
- [ ] Patterns identified
- [ ] Anomalies documented

### Phase 2 Checkpoint
```
ANALYSIS COMPLETE:
- Items analyzed: [X/Y]
- Key patterns: [list]
- Concerns identified: [count]
```

---

## Phase 3: Synthesis

### Objective
Synthesize findings into coherent conclusions.

### Tasks
1. Review all analysis notes
2. Identify overarching themes
3. Draw conclusions from patterns
4. Prioritize findings by impact
5. Formulate key insights

### Deliverable: Findings Summary
Create `[findings-filename].md` with:
```markdown
# Research Findings: [Topic]

## Executive Summary
[2-3 paragraphs summarizing key findings]

## Key Findings
1. **[Finding 1]**: [Description and evidence]
2. **[Finding 2]**: [Description and evidence]
3. **[Finding 3]**: [Description and evidence]

## Patterns Observed
- [Pattern 1]
- [Pattern 2]

## Areas of Concern
1. [Concern 1]: [Details]
2. [Concern 2]: [Details]

## Data Summary
- Total items examined: [X]
- Categories: [list]
- Analysis coverage: [X%]
```

### Phase 3 Success Criteria
- [ ] All findings synthesized
- [ ] Conclusions supported by evidence
- [ ] Priorities established
- [ ] Summary document complete

---

## Phase 4: Recommendations

### Objective
Provide actionable recommendations based on findings.

### Tasks
1. Develop recommendations for each finding
2. Prioritize by impact and effort
3. Identify dependencies between recommendations
4. Create action timeline (if applicable)

### Deliverable: Recommendations
Add to findings document or create separate:
```markdown
# Recommendations

## High Priority (Address Immediately)
1. **[Recommendation]**
   - Rationale: [Why]
   - Effort: [Low/Medium/High]
   - Impact: [Low/Medium/High]
   - Dependencies: [Any]

## Medium Priority (Plan for Soon)
[...]

## Low Priority (Future Consideration)
[...]

## Implementation Order
1. First: [Recommendation X]
2. Then: [Recommendation Y]
3. Finally: [Recommendation Z]
```

### Phase 4 Success Criteria
- [ ] All findings have recommendations
- [ ] Priorities assigned
- [ ] Implementation order defined
- [ ] Dependencies identified

---

## Phase 5: Final Documentation

### Objective
Produce final polished deliverable.

### Tasks
1. Compile all sections into final document
2. Add executive summary
3. Review for completeness
4. Ensure actionability
5. Format consistently

### Deliverable: Final Report
Create `[final-report].md` with all sections:
1. Executive Summary
2. Scope and Methodology
3. Findings
4. Analysis
5. Recommendations
6. Appendix (raw data if needed)

### Phase 5 Success Criteria
- [ ] All sections complete
- [ ] Executive summary written
- [ ] Consistent formatting
- [ ] No TODO items
- [ ] Actionable and clear

---

## Final Verification

### Completeness Checklist
- [ ] Phase 1: Discovery complete, inventory exists
- [ ] Phase 2: All items analyzed, notes exist
- [ ] Phase 3: Findings synthesized, summary exists
- [ ] Phase 4: Recommendations provided, prioritized
- [ ] Phase 5: Final document complete

### Quality Checklist
- [ ] All conclusions supported by evidence
- [ ] Recommendations are actionable
- [ ] Document is well-organized
- [ ] No sections are missing content
- [ ] Executive summary captures key points

## Completion
When ALL of the following are true:
- All 5 phases completed
- All deliverables created
- Completeness checklist verified
- Quality checklist verified

Output: <promise>[COMPLETION_PHRASE]</promise>

## Progress Tracking
```
RESEARCH PROGRESS:
Phase 1 (Discovery): [COMPLETE/IN PROGRESS]
Phase 2 (Analysis): [COMPLETE/IN PROGRESS/NOT STARTED]
Phase 3 (Synthesis): [COMPLETE/IN PROGRESS/NOT STARTED]
Phase 4 (Recommendations): [COMPLETE/IN PROGRESS/NOT STARTED]
Phase 5 (Documentation): [COMPLETE/IN PROGRESS/NOT STARTED]

Items examined: [X/Y]
Deliverables created: [list]
```

## If Stuck
- Document what information is missing
- List sources already examined
- Identify the specific gap
- Do NOT skip analysis or output false promise
```

## Example Prompts

### Example 1: Security Audit

**Input:**
- Objective: Identify security vulnerabilities in authentication module
- Scope: src/auth/ directory
- Deliverable: Security audit report with findings and fixes
- Promise: SECURITY_AUDIT_COMPLETE

**Generated Prompt:**

```markdown
# Research: Authentication Security Audit

## Objective
Identify security vulnerabilities in the authentication module following OWASP guidelines and provide remediation recommendations.

## Scope

### In Scope
- All files in src/auth/
- Authentication flows (login, signup, password reset)
- Session management
- Token handling
- Input validation

### Out of Scope
- Authorization (permissions, roles)
- Third-party auth providers
- Frontend security

## Sources to Examine
- Code files: src/auth/**/*.ts
- Tests: tests/auth/**/*.ts
- Configuration: auth-related config files
- Dependencies: auth-related npm packages

---

## Phase 1: Discovery

### Tasks
1. List all files in auth module
2. Identify all entry points (routes)
3. Map authentication flows
4. Identify external dependencies
5. List all sensitive operations

### Deliverable: auth-inventory.md
```markdown
# Auth Module Inventory

## Files
| File | Purpose | Entry Points | Sensitive Ops |
|------|---------|--------------|---------------|

## Dependencies
| Package | Version | Security Notes |

## Authentication Flows
1. Login: [path]
2. Signup: [path]
[...]
```

### Phase 1 Success
- [ ] All auth files listed
- [ ] All entry points identified
- [ ] Flows mapped
- [ ] Dependencies inventoried

---

## Phase 2: Analysis

### Security Analysis Framework
For each component, check:
- **A1 Injection**: SQL, NoSQL, command injection risks
- **A2 Broken Auth**: Weak passwords, session issues
- **A3 Sensitive Data**: Password storage, token exposure
- **A4 XXE**: XML parsing vulnerabilities
- **A5 Access Control**: Proper authorization checks
- **A6 Misconfiguration**: Insecure defaults
- **A7 XSS**: User input handling
- **A8 Deserialization**: Unsafe object handling
- **A9 Components**: Vulnerable dependencies
- **A10 Logging**: Insufficient monitoring

### Tasks
1. Analyze each file against OWASP framework
2. Check password hashing implementation
3. Review JWT token handling
4. Examine session management
5. Check input validation

### Deliverable: security-analysis.md
Per-file analysis with vulnerabilities found.

---

## Phase 3: Synthesis

### Tasks
1. Categorize all vulnerabilities by severity
2. Identify systemic issues
3. Calculate risk scores
4. Prioritize by exploitability

### Deliverable: security-findings.md
```markdown
# Security Findings

## Critical (Requires Immediate Action)
- [Vulnerability]: [Location] - [Impact]

## High
[...]

## Medium
[...]

## Low
[...]

## Summary Statistics
- Critical: X
- High: X
- Medium: X
- Low: X
```

---

## Phase 4: Recommendations

### Tasks
1. Provide fix for each vulnerability
2. Prioritize fixes by risk
3. Estimate effort for each fix
4. Identify quick wins

### Deliverable: remediation-plan.md
```markdown
# Remediation Plan

## Immediate Actions
1. [Fix]: [How] - [Effort]

## Short-term (This Sprint)
[...]

## Medium-term
[...]
```

---

## Phase 5: Final Report

### Deliverable: AUTH-SECURITY-AUDIT.md
Complete report with:
1. Executive Summary
2. Methodology
3. Findings by Severity
4. Detailed Vulnerability Descriptions
5. Remediation Plan
6. Verification Steps

---

## Completion
When audit report complete with all vulnerabilities documented and remediation provided:

Output: <promise>SECURITY_AUDIT_COMPLETE</promise>
```

### Example 2: Technology Comparison

**Input:**
- Objective: Compare React vs Vue vs Svelte for new frontend
- Scope: Team skills, project requirements, ecosystem
- Deliverable: Comparison report with recommendation
- Promise: FRAMEWORK_COMPARISON_COMPLETE

**Generated Prompt:**

```markdown
# Research: Frontend Framework Comparison

## Objective
Compare React, Vue, and Svelte to recommend the best framework for the new frontend project based on team skills, project requirements, and ecosystem.

## Scope

### In Scope
- Learning curve for team
- Performance characteristics
- Ecosystem (libraries, tools)
- Community and support
- Project requirements fit
- Long-term maintainability

### Out of Scope
- Mobile development (React Native, etc.)
- SSR frameworks (Next.js, Nuxt, SvelteKit)
- Backend considerations

---

## Phase 1: Discovery

### Tasks
1. Document team's current skills
2. List project requirements
3. Identify key evaluation criteria
4. Gather framework documentation

### Deliverable: evaluation-criteria.md
```markdown
# Evaluation Framework

## Team Context
- Current experience: [frameworks]
- Available learning time: [duration]
- Team size: [N]

## Project Requirements
- [Requirement 1]
- [Requirement 2]
[...]

## Evaluation Criteria
| Criterion | Weight | Reason |
|-----------|--------|--------|
| Learning curve | 25% | Team has limited React experience |
| Performance | 20% | App will be data-heavy |
[...]
```

---

## Phase 2: Analysis

### Analysis Framework
For each framework:
- **Learning Curve**: Time to productivity
- **Performance**: Bundle size, runtime speed, memory
- **Ecosystem**: Available libraries, tools, IDE support
- **Community**: Documentation, Stack Overflow, GitHub activity
- **Hiring**: Developer availability
- **Architecture**: How it fits project patterns

### Deliverable: framework-analysis.md
```markdown
# React Analysis
## Learning Curve
[Analysis]

## Performance
[Analysis]

[... repeat for Vue and Svelte]
```

---

## Phase 3: Synthesis

### Tasks
1. Score each framework on each criterion
2. Apply weights
3. Calculate overall scores
4. Identify dealbreakers

### Deliverable: comparison-matrix.md
```markdown
# Framework Comparison Matrix

| Criterion | Weight | React | Vue | Svelte |
|-----------|--------|-------|-----|--------|
| Learning Curve | 25% | 3 | 4 | 4 |
| Performance | 20% | 3 | 4 | 5 |
[...]
| **Weighted Total** | | X.X | X.X | X.X |
```

---

## Phase 4: Recommendations

### Deliverable: recommendation.md
```markdown
# Framework Recommendation

## Recommendation: [Framework]

### Rationale
[Why this framework is best for this team and project]

### Advantages
- [Advantage 1]
- [Advantage 2]

### Concerns and Mitigations
- [Concern 1]: [How to address]

### Implementation Approach
1. [Step 1]
2. [Step 2]
[...]
```

---

## Phase 5: Final Report

### Deliverable: FRAMEWORK-COMPARISON-REPORT.md

---

## Completion
When complete comparison with recommendation:

Output: <promise>FRAMEWORK_COMPARISON_COMPLETE</promise>
```

## Best Practices

### Research Methodology
- Define scope explicitly (what's in/out)
- Use consistent analysis framework
- Document evidence for conclusions
- Separate findings from opinions

### Deliverables
- Create artifacts as you go
- Use consistent format
- Include data to support conclusions
- Make recommendations actionable

### DO:
- Define clear scope boundaries
- Create deliverables at each phase
- Support conclusions with evidence
- Provide actionable recommendations
- Track progress systematically

### DON'T:
- Skip the discovery phase
- Make recommendations without evidence
- Leave sections incomplete
- Output promise before documentation

## Integration with Ralph Loop

```bash
/ralph-wiggum:ralph-loop "[paste generated prompt]" --completion-promise "YOUR_PROMISE" --max-iterations 50
```

**Recommended iterations by research complexity:**
- Simple audit (single module): `--max-iterations 30-40`
- Comparison (3-5 options): `--max-iterations 40-60`
- Full codebase analysis: `--max-iterations 70-100`
- Complex planning: `--max-iterations 60-80`

---

For single-task prompts, see `ralph-prompt-single-task`.
For multi-task prompts, see `ralph-prompt-multi-task`.
For project-level prompts, see `ralph-prompt-project`.
