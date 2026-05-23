---
name: gap-analysis-framework
description: Comprehensive gap analysis framework for identifying missing capabilities, coverage, and requirements. Use for requirements vs implementation gaps, test coverage analysis, documentation gaps, security posture assessment, performance benchmarks, feature parity analysis, team capability gaps, infrastructure coverage, compliance gaps, and accessibility analysis. Includes SWOT, maturity models, and automated gap detection.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, WebFetch]
---

# Gap Analysis Framework

## Purpose

"What's missing?" - This Skill identifies deficiencies across all aspects of software systems:

1. **Requirements vs Implementation** - Missing features or incomplete implementations
2. **Test Coverage Gaps** - Untested code paths and scenarios
3. **Documentation Gaps** - Missing or outdated documentation
4. **Security Posture Gaps** - Vulnerabilities and missing security controls
5. **Performance Gaps** - Performance below targets or benchmarks
6. **Feature Parity** - Comparing with competitors or specifications
7. **Team/Skill Gaps** - Missing expertise or resources
8. **Infrastructure Gaps** - Missing monitoring, redundancy, or scaling
9. **Compliance Gaps** - Regulatory and standards non-compliance
10. **Accessibility Gaps** - WCAG, ARIA, and inclusive design deficiencies

## When to Use This Skill

Use gap analysis for:
- Pre-launch readiness assessment
- Migration planning and competitive analysis
- Compliance audits and security assessments
- Test strategy planning and documentation reviews
- Team planning and infrastructure reviews
- Accessibility audits and API versioning
- Dependency audits and coverage analysis

## Quick Start

### 1. Define Your Gap Type

Choose the analysis pattern matching your use case:

| Gap Type | Use Case | Tools |
|----------|----------|-------|
| **Requirements** | Missing features or implementations | Code inspection, requirements tracking |
| **Test Coverage** | Untested code paths | Coverage.py, Jest, Istanbul |
| **Documentation** | Missing or outdated docs | Docstring analysis, README review |
| **SWOT** | Strategic capability assessment | Stakeholder interviews, market analysis |
| **Maturity Model** | Organizational capability level | CMM assessment, process audit |
| **Security Posture** | Security controls and compliance | SAST/DAST, vulnerability scanning |

### 2. Analyze Current vs Target State

```
Target State (What should be)
         ↓
    ┌────────┐
    │  GAP   │  = Missing, incomplete, deficient
    │Analysis│
    └────────┘
         ↑
Current State (What is)
```

### 3. Prioritize Gaps

```
         │ Easy to Fix │ Hard to Fix │
─────────┼─────────────┼─────────────┤
High     │   QUICK     │  STRATEGIC  │
Impact   │    WINS     │   GAPS      │
─────────┼─────────────┼─────────────┤
Low      │  OPTIONAL   │   IGNORE    │
Impact   │IMPROVEMENTS │   FOR NOW   │
─────────┴─────────────┴─────────────┘
```

### 4. Create Action Plan

For each gap:
1. **Assign Owner** - Who fixes this?
2. **Set Timeline** - By when?
3. **Allocate Resources** - What budget/people?
4. **Define Success** - How to measure closure?
5. **Track Progress** - Regular reviews

## Core Concepts

### Gap Analysis Process

1. **Define Target State** - Requirements, standards, best practices
2. **Assess Current State** - Inventory, measure, document capabilities
3. **Identify Gaps** - Compare target vs current, quantify
4. **Prioritize** - Impact/effort matrix, dependencies
5. **Plan Actions** - Assign owners, set timelines, allocate resources
6. **Execute & Monitor** - Regular reviews, adjust as needed
7. **Verify Closure** - Confirm gap resolution

### Maturity Model Levels

Organizational capability evolves across levels:

```
Level 5: OPTIMIZING    │ ████████████ │ Continuous improvement
Level 4: MANAGED       │ █████████░░░ │ Measured and controlled
Level 3: DEFINED       │ ██████░░░░░░ │ Documented processes
Level 2: REPEATABLE    │ ███░░░░░░░░░ │ Basic discipline
Level 1: INITIAL       │ █░░░░░░░░░░░ │ Ad-hoc/chaotic
```

Maturity gaps show the distance between current and target capability levels.

### SWOT Framework

Gap analysis often uses SWOT to identify strategic gaps:

```
┌────────────────────────┬────────────────────────┐
│ STRENGTHS              │ WEAKNESSES (GAP)       │
│ ✓ What we do well      │ ✗ What's missing      │
├────────────────────────┼────────────────────────┤
│ OPPORTUNITIES          │ THREATS (RISK GAP)    │
│ ⚡ Market potential    │ ⚠️  Gaps expose risk   │
└────────────────────────┴────────────────────────┘
```

## Implementation Patterns

See **PATTERNS.md** for detailed analysis patterns:
1. Requirements vs Implementation
2. Test Coverage
3. Documentation
4. SWOT Analysis
5. Capability Maturity Model (CMM)
6. Security Posture

## Common Gap Analysis Mistakes

See **GOTCHAS.md** for:
- Analysis paralysis and scope creep
- Ignoring root causes and constraints
- Missing stakeholder input
- No prioritization or metrics
- One-time snapshots instead of continuous monitoring

## Best Practices

**DO's**:
- Define clear target state before analyzing
- Quantify gaps with metrics, not just qualitative assessment
- Prioritize ruthlessly - focus on critical gaps first
- Involve stakeholders - get customer, user, and operator input
- Automate detection - build scripts for continuous monitoring
- Track over time - gap analysis should be ongoing
- Root cause analysis - understand *why* gaps exist
- Create action plans - assign owners and timelines
- Celebrate progress - acknowledge closed gaps
- Use industry benchmarks - compare against standards

**DON'Ts**:
- Compare to perfection - set realistic, achievable targets
- Analyze without acting - analysis without action is waste
- Ignore constraints - consider resources, time, budget
- Blame individuals - focus on systems and processes
- Scope creep - distinguish gaps from new features
- Forget context - startup needs differ from enterprise
- Skip quick wins - balance long-term and immediate actions
- Ignore stakeholders - technical gaps aren't the only ones
- Set and forget - reassess regularly as targets evolve
- Overwhelm teams - pace remediation to avoid burnout

## Gap Analysis Checklist

### Pre-Analysis
- [ ] Define scope and boundaries
- [ ] Identify stakeholders
- [ ] Set clear success criteria
- [ ] Gather baseline data/metrics
- [ ] Define target state

### Analysis Phase
- [ ] Inventory current state
- [ ] Document capabilities
- [ ] Identify missing elements
- [ ] Quantify gaps with metrics
- [ ] Categorize gaps by type
- [ ] Assess impact and severity
- [ ] Estimate effort to close

### Prioritization
- [ ] Create impact/effort matrix
- [ ] Identify critical path blockers
- [ ] Find quick wins
- [ ] Consider dependencies
- [ ] Align with business goals

### Action Planning
- [ ] Assign gap owners
- [ ] Set realistic timelines
- [ ] Allocate resources
- [ ] Define success metrics
- [ ] Create tracking mechanism

### Execution & Monitoring
- [ ] Regular progress reviews
- [ ] Update gap status
- [ ] Adjust priorities as needed
- [ ] Celebrate closed gaps
- [ ] Re-assess periodically

## Key Resources

### Gap Analysis Frameworks
- [SWOT Analysis](https://www.mindtools.com/pages/article/newTMC_05.htm) - Strategic positioning
- [Capability Maturity Model](https://en.wikipedia.org/wiki/Capability_Maturity_Model) - Process maturity
- [Root Cause Analysis](https://asq.org/quality-resources/root-cause-analysis) - Finding underlying issues
- [SMART Goals](https://www.mindtools.com/pages/article/smart-goals.htm) - Measurable targets

### Analysis Tools
- **Test Coverage**: Coverage.py, Jest, Istanbul, JaCoCo
- **Code Quality**: SonarQube, Code Climate
- **API Docs**: OpenAPI/Swagger specifications
- **Compliance**: OWASP Top 10, CWE database, WCAG 2.1

## Documentation Map

- **SKILL.md** (this file) - Quick start and essential workflow
- **PATTERNS.md** - Six detailed analysis patterns with code examples
- **KNOWLEDGE.md** - Gap analysis theory, methodologies, and frameworks
- **GOTCHAS.md** - Common mistakes, bias issues, scope management
- **EXAMPLES.md** - Complete real-world gap analysis scenarios
- **REFERENCE.md** - Complete framework reference (SWOT, maturity models, scoring)

## Related Skills

- `security-scanning-suite` - For security gap analysis
- `architecture-evaluation-framework` - For architecture and design gaps
- `evaluation-reporting-framework` - For comprehensive assessment reports
- `codebase-onboarding-analyzer` - For documentation and onboarding gaps

## Next Steps

1. **Choose a pattern** from PATTERNS.md matching your use case
2. **Review examples** in EXAMPLES.md for your gap type
3. **Reference frameworks** in REFERENCE.md for assessment templates
4. **Avoid gotchas** listed in GOTCHAS.md
5. **Use knowledge** in KNOWLEDGE.md for deeper context

---

## Example: Quick Requirements Gap Analysis

**Scenario**: E-commerce site launch in 2 weeks, need to verify completeness.

**1. Identify Requirements**:
```
REQ-001: User registration with email
REQ-002: Product catalog with search
REQ-003: Shopping cart with checkout
REQ-004: Order history and receipts
REQ-005: Admin dashboard for inventory
```

**2. Assess Implementation**:
- REQ-001: 100% complete (with tests)
- REQ-002: 80% complete (search not optimized)
- REQ-003: 50% complete (cart works, checkout needs payment integration)
- REQ-004: 0% (missing)
- REQ-005: 20% (basic scaffolding only)

**3. Identify Gaps**:
```
│ Requirement        │ Status      │ Coverage │ Impact   │
├────────────────────┼─────────────┼──────────┼──────────┤
│ REQ-001            │ Complete    │ 100%     │ None     │
│ REQ-002            │ Partial     │ 80%      │ Medium   │
│ REQ-003            │ Partial     │ 50%      │ CRITICAL │
│ REQ-004            │ Missing     │ 0%       │ CRITICAL │
│ REQ-005            │ Partial     │ 20%      │ High     │
```

**4. Prioritize**:
- CRITICAL: Complete checkout (hard, essential) + Order history (medium effort)
- HIGH: Admin dashboard improvements (ongoing)
- MEDIUM: Search optimization (post-launch nice-to-have)

**5. Plan Actions**:
- Assign payment integration to Backend Lead (3 days)
- Assign order history to Full-stack Dev (2 days)
- Assign dashboard to Admin Dev (5 days, starts after launch)

**6. Monitor**:
- Daily standup on critical gaps
- Verify acceptance criteria met
- Launch when critical gaps closed

This 6-step process provides clear visibility on what's missing and what needs immediate attention.
