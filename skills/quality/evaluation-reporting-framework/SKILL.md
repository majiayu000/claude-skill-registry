---
name: evaluation-reporting-framework
description: Evaluation and reporting for code quality, performance, security, architecture, team processes, AI/LLM outputs, A/B tests, ROI analysis, and compliance. Scoring systems, benchmarking, dashboard creation, and multi-format report generation (PDF, HTML, Markdown, JSON).
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, WebFetch]
---

# Evaluation & Reporting Framework

## Purpose

"Writing evaluations is a skill" - This skill provides comprehensive evaluation and reporting capabilities across all software development aspects:

1. **Code Quality** - Metrics, standards compliance, technical debt
2. **Performance** - Benchmarking, profiling, optimization analysis
3. **Security** - Vulnerability scoring, risk evaluation, compliance
4. **Architecture** - Design quality, scalability, maintainability
5. **Team/Process** - Velocity, efficiency, maturity
6. **AI/LLM Outputs** - Quality metrics, bias detection, accuracy
7. **A/B Testing** - Statistical significance, experiment reporting
8. **ROI & Financial** - Impact analysis, business value
9. **Compliance** - Regulatory compliance, standards adherence
10. **Multi-Format Reporting** - PDF, HTML, Markdown, interactive dashboards

## When to Use This Skill

- Performance review and benchmarking
- Code quality assessment and technical debt analysis
- Security audit reporting
- Architecture review and design evaluation
- Sprint retrospectives and team velocity analysis
- AI model evaluation and comparison
- A/B test result analysis and decision-making
- ROI calculation for technology investments
- Compliance audit reporting (SOC2, HIPAA, GDPR)
- Executive reporting and stakeholder communication
- Quarterly/annual technical reviews
- Migration readiness assessments
- Vendor evaluation and tool comparison
- SLA compliance reporting
- Post-incident analysis reports

## Quick Start: Essential Workflow

### 1. Define What You're Measuring

Before collecting data, establish clear metrics:

```python
# Example: Code Quality Evaluation Dimensions
dimensions = {
    "maintainability": 0.30,     # 30% weight
    "reliability": 0.25,          # 25% weight
    "security": 0.25,             # 25% weight
    "testability": 0.20            # 20% weight
}
```

### 2. Collect Data

Gather data from tools and systems:

```
Automated: SonarQube, pytest, bandit, coverage tools
Manual: Reviews, surveys, audits
Historical: Previous baselines, trends
```

### 3. Score & Analyze

Apply consistent scoring to normalize data:

```
90-100: A (Excellent/Green)
80-89:  B (Good)
70-79:  C (Acceptable/Amber)
60-69:  D (Poor)
0-59:   F (Critical/Red)
```

### 4. Report & Recommend

Create reports with actionable recommendations:

```
Executive Summary (1-2 pages)
├── Key Finding (headline)
├── Metrics Table
├── Trend Analysis
└── Top 3 Recommendations

Detailed Analysis (5-10 pages)
├── Methodology
├── Detailed Metrics
├── Findings by Dimension
└── Prioritized Action Items
```

## Core Concepts

### Evaluation Framework Layers

The framework operates in 5 interconnected layers:

**1. Define** → **2. Collect** → **3. Analyze** → **4. Interpret** → **5. Report**

Each layer feeds into the next, creating a complete evaluation cycle.

### Scoring Systems (Choose Appropriate Format)

- **Numeric (0-100)**: Universal, mathematical
- **Letter Grades (A-F)**: Familiar, easy to understand
- **RAG Status**: Red/Amber/Green for quick status
- **Confidence Levels**: High/Medium/Low
- **Weighted Composite**: Combine multiple metrics with priorities

### Report Types & Audiences

| Report Type | Audience | Length | Depth |
|-----------|----------|--------|-------|
| Executive Summary | C-Level, Leadership | 1-2 pages | High-level |
| Technical Deep-Dive | Engineers, Architects | 5-10 pages | Detailed |
| Compliance Audit | Legal, Auditors | 10-20 pages | Comprehensive |
| Dashboard | All Stakeholders | Interactive | Current + Trend |
| A/B Test Analysis | Product, Leadership | 3-5 pages | Decision-focused |

## Implementation Patterns

### Pattern 1: Code Quality Evaluation

Comprehensive assessment using 6 dimensions:

**Metrics**: Test coverage, complexity, duplication, security, documentation, performance

**Workflow**: Collect metrics → Calculate composite score → Grade by dimension → Generate report

**Output**: Multi-dimensional report with strengths, weaknesses, and prioritized improvements

See: `/PATTERNS.md` (Pattern 1: Code Quality Evaluation)

---

### Pattern 2: Performance Benchmarking

Statistical analysis of performance with baseline comparison:

**Metrics**: Latency (p50, p95, p99), throughput, error rate, resource usage

**Workflow**: Run benchmarks → Collect measurements → Compare to baseline → Analyze trends

**Output**: Performance comparison with regression detection and optimization recommendations

See: `/PATTERNS.md` (Pattern 2: Performance Benchmarking)

---

### Pattern 3: AI/LLM Output Evaluation

Multi-dimensional LLM output assessment:

**Dimensions**: Accuracy, relevance, coherence, completeness, safety

**Workflow**: Evaluate outputs → Calculate composite score → Identify patterns → Recommend actions

**Output**: LLM evaluation report for model selection and fine-tuning guidance

See: `/PATTERNS.md` (Pattern 3: AI/LLM Output Evaluation)

---

### Pattern 4: A/B Test Analysis

Statistical significance testing for experiments:

**Method**: Two-proportion z-test with confidence intervals

**Workflow**: Define variants → Run test → Calculate significance → Make recommendation

**Decisions**: SHIP IT / ROLLBACK / INCONCLUSIVE (run longer)

See: `/PATTERNS.md` (Pattern 4: A/B Test Analysis)

---

### Pattern 5: Multi-Format Report Generation

Professional reports in multiple output formats:

**Formats**: Markdown, HTML, JSON, PDF

**Features**: Dynamic styling, status colors, tables, charts, metadata

**Workflow**: Define sections → Add tables/content → Generate in multiple formats

See: `/PATTERNS.md` (Pattern 5: Multi-Format Report Generation)

---

## Common Gotchas & Pitfalls

### Critical Mistakes to Avoid

**1. Vanity Metrics** - Measuring what looks good, not what drives decisions
- Solution: Focus on actionable metrics tied to business outcomes

**2. Goodhart's Law** - When measurement becomes target, ceases being good measure
- Solution: Use multiple metrics, avoid gaming, measure outcomes not outputs

**3. Survivor Bias** - Only analyzing success cases, ignoring failures
- Solution: Include all data points, especially failures and edge cases

**4. Correlation ≠ Causation** - Assuming relationships mean cause/effect
- Solution: Use controlled experiments, consider confounding factors

**5. False Precision** - Reporting numbers more precise than they are
- Solution: Use confidence intervals, round appropriately, state uncertainty

**6. Context-Free Metrics** - Numbers without context are meaningless
- Solution: Always include baselines, benchmarks, trends, narrative

See: `/GOTCHAS.md` for 15+ additional gotchas with detailed solutions

---

## Best Practices

### DO's

1. **Define Clear Metrics** - Establish what you're measuring before collecting data
2. **Use Multiple Dimensions** - Single metrics can be misleading, use composite scores
3. **Provide Context** - Always include baselines, benchmarks, and trends
4. **Visualize Data** - Charts and graphs enhance understanding
5. **Tailor to Audience** - Executive summary for leadership, technical details for engineers
6. **Automate Collection** - Manual data gathering is error-prone and time-consuming
7. **Include Confidence Intervals** - Acknowledge uncertainty in measurements
8. **Track Over Time** - One-time snapshots miss trends and patterns
9. **Make Actionable** - Every metric should inform a decision
10. **Validate Methodology** - Peer review evaluation frameworks before deployment

### DON'Ts

1. **Don't Cherry-Pick Data** - Include all relevant data points, not just favorable ones
2. **Don't Ignore Statistical Significance** - A difference isn't meaningful without significance
3. **Don't Compare Apples to Oranges** - Ensure fair comparisons
4. **Don't Over-Optimize Single Metrics** - Can lead to gaming and unintended consequences
5. **Don't Skip Executive Summary** - Not everyone will read full report
6. **Don't Use Jargon** - Explain technical terms for non-technical audiences
7. **Don't Forget the "So What"** - Always explain why metrics matter
8. **Don't Report Without Recommendations** - Analysis should lead to action
9. **Don't Ignore Outliers** - Investigate anomalies, they reveal important insights
10. **Don't Create Reports Nobody Reads** - Ensure reports are useful and consumed

## Evaluation Frameworks

### DORA Metrics (DevOps Performance)

Four metrics measuring software delivery capability:

- **Deployment Frequency**: How often you deploy to production
- **Lead Time for Changes**: Time from commit to production
- **Mean Time to Recovery**: Time to restore service after incident
- **Change Failure Rate**: % of deployments causing failures

### SPACE Framework (Developer Productivity)

Five dimensions of developer productivity:

- **Satisfaction & Well-being**: Developer happiness and health
- **Performance**: Outcomes delivered
- **Activity**: Volume of work
- **Communication & Collaboration**: Team interaction quality
- **Efficiency & Flow**: Ability to work without interruption

### Code Quality Metrics

Standard dimensions for code assessment:

- **Cyclomatic Complexity**: Code complexity (lower is better, <5 is excellent)
- **Technical Debt Ratio**: Effort to fix vs build new
- **Code Coverage**: % of code tested (80%+ is good, 90%+ is excellent)
- **Code Duplication**: % of duplicated code (<5% is excellent)
- **Maintainability Index**: Composite 0-100 metric (higher is better)

## Knowledge Resources

### Theory & Frameworks

See `/KNOWLEDGE.md` for:
- Evaluation framework layers and principles
- Scoring systems and normalization
- DORA, SPACE, and code quality frameworks
- Visualization best practices
- Complete external resource links

### Reporting Templates & Examples

See `/EXAMPLES.md` for:
- Code quality report example (full template)
- Performance report example
- A/B test report example
- Executive summary template
- Real-world scenario walk-throughs

### Common Issues & Solutions

See `/GOTCHAS.md` for:
- Metric selection pitfalls (vanity metrics, Goodhart's Law)
- Data collection problems (bias, correlation)
- Analysis mistakes (false precision, confirmation bias)
- Reporting errors (unclear recommendations, jargon)
- Audience communication issues

### Implementation Patterns

See `/PATTERNS.md` for:
- Code quality evaluation (6 dimensions, scoring, reporting)
- Performance benchmarking (statistical analysis, baseline comparison)
- AI/LLM evaluation (5 dimensions, composite scoring)
- A/B test analysis (z-test, significance, decision rules)
- Multi-format report generation (Markdown, HTML, JSON, PDF)

### Templates & Catalogs

See `/REFERENCE.md` for:
- Format references (Markdown, HTML, JSON, PDF)
- Template library (1-page, 5-page, comparative, compliance)
- Metrics catalog (performance, code quality, team, security)
- Report checklists (pre-report, during analysis, pre-distribution)

## Related Skills

- `gap-analysis-framework` - Identify gaps before evaluation
- `security-scanning-suite` - Security-specific evaluation
- `codebase-onboarding-analyzer` - Code quality assessment
- `architecture-evaluation-framework` - Architecture evaluation
- `ai-evaluation-suite` - AI/LLM specific evaluation

## External References

- [DORA Metrics](https://www.devops-research.com/research.html) - DevOps Research and Assessment
- [SPACE Framework](https://queue.acm.org/detail.cfm?id=3454124) - Developer productivity metrics
- [SonarQube Metrics](https://docs.sonarqube.org/latest/user-guide/metric-definitions/) - Code quality definitions
- [Lighthouse Scoring](https://web.dev/performance-scoring/) - Web performance evaluation
- [A/B Testing Guide](https://www.optimizely.com/optimization-glossary/ab-testing/) - Experiment design
- [Statistical Significance](https://en.wikipedia.org/wiki/Statistical_significance) - Understanding p-values
- [CVSS Scoring](https://www.first.org/cvss/) - Security vulnerability scoring
- [Grafana Documentation](https://grafana.com/docs/) - Dashboard creation

## Progressive Disclosure

This skill uses a progressive disclosure pattern for comprehensive coverage:

- **SKILL.md** (this file, <500 lines): Quick start, essential patterns, key best practices
- **PATTERNS.md** (400+ lines): Complete implementation patterns with Python code examples
- **KNOWLEDGE.md** (310+ lines): Scoring systems, frameworks, visualization principles
- **GOTCHAS.md** (350+ lines): 15+ common mistakes with solutions
- **EXAMPLES.md** (425+ lines): Real reports, templates, decision scenarios
- **REFERENCE.md** (390+ lines): Format templates, metrics catalog, checklists

Start with this file, dive into PATTERNS for implementation, reference KNOWLEDGE for theory, and consult GOTCHAS/EXAMPLES/REFERENCE as needed.

---

**SKILL.md Line Count**: 439 lines
**Complete Framework**: 2,314 lines across 6 files
**Coverage**: 10 major evaluation categories, 5 implementation patterns, 30+ code examples
