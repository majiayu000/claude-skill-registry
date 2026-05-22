---
name: architecture-evaluation-framework
description: Comprehensive architectural analysis and evaluation framework for system architecture assessment. Use for architecture pattern identification, SOLID principles evaluation, coupling/cohesion analysis, scalability assessment, performance characteristics, security architecture, data architecture, microservices vs monolith, technical debt quantification, and ADRs. Includes C4 model, 4+1 views, QAW, ATAM, architectural fitness functions, and visualization tools.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, WebFetch]
---

# Architecture Evaluation Framework

## Purpose

"How sound is the architecture?" - This Skill provides comprehensive architectural analysis and evaluation capabilities for assessing system architecture quality, identifying architectural issues, and ensuring long-term maintainability and scalability.

## Quick Start Example

Evaluate a Python project's architecture in 3 steps:

```bash
# 1. Run SOLID principles analysis
python solid_analyzer.py src/ -o reports/solid.md

# 2. Analyze coupling and cohesion
python coupling_analyzer.py src/ -o reports/coupling.md

# 3. Generate C4 diagrams
python c4_generator.py --system "MyApp" --output docs/architecture/
```

See complete working examples in [EXAMPLES.md](EXAMPLES.md).

## Core Evaluation Methods

### 1. Architecture Pattern Analysis
- **What**: Identify architectural patterns (MVC, microservices, layered, event-driven)
- **When**: Understanding existing architecture, migration planning
- **How**: Pattern detection algorithms, dependency analysis
- **Details**: [Pattern identification in PATTERNS.md](PATTERNS.md#pattern-identification)

### 2. SOLID Principles Evaluation
- **What**: Check adherence to SOLID design principles
- **When**: Code reviews, refactoring planning, quality audits
- **How**: AST analysis, method counting, dependency checking
- **Details**: [SOLID analyzer implementation](PATTERNS.md#solid-analyzer)

### 3. Coupling and Cohesion Metrics
- **What**: Measure module dependencies and internal cohesion
- **When**: Identifying refactoring candidates, reducing complexity
- **How**: Dependency graphs, LCOM metrics, instability calculations
- **Details**: [Coupling/cohesion patterns](PATTERNS.md#coupling-cohesion)

### 4. Quality Attribute Scenarios (ATAM)
- **What**: Evaluate architecture trade-offs between quality attributes
- **When**: Major architectural decisions, technology selection
- **How**: Scenario-based evaluation, trade-off matrices
- **Details**: [ATAM methodology](KNOWLEDGE.md#atam-methodology)

### 5. C4 Model Documentation
- **What**: Create hierarchical architecture diagrams (Context, Container, Component, Code)
- **When**: Documenting architecture, onboarding, reviews
- **How**: PlantUML generation, structured diagramming
- **Details**: [C4 model guide](KNOWLEDGE.md#c4-model)

### 6. Architecture Decision Records (ADRs)
- **What**: Document and track architectural decisions
- **When**: Making significant architectural choices
- **How**: Structured templates, decision tracking
- **Details**: [ADR templates](PATTERNS.md#adr-management)

## Table of Contents

### Core Files
- **[KNOWLEDGE.md](KNOWLEDGE.md)** - Architecture theory, frameworks, methodologies
- **[PATTERNS.md](PATTERNS.md)** - Implementation patterns and algorithms
- **[EXAMPLES.md](EXAMPLES.md)** - Complete working code examples
- **[GOTCHAS.md](GOTCHAS.md)** - Common pitfalls and troubleshooting
- **[REFERENCE.md](REFERENCE.md)** - API documentation and metrics catalog

### Quick Navigation

#### By Task
- **Evaluating existing architecture** → Start with [Pattern Analysis](PATTERNS.md#pattern-identification)
- **Planning microservices migration** → See [Microservices evaluation](EXAMPLES.md#microservices-evaluation)
- **Measuring technical debt** → Use [Technical debt quantification](PATTERNS.md#technical-debt)
- **Creating architecture docs** → Follow [C4 model guide](EXAMPLES.md#c4-diagrams)
- **Reviewing SOLID compliance** → Run [SOLID analyzer](EXAMPLES.md#solid-analysis)

#### By Technology
- **Python** → [Python architecture analysis](EXAMPLES.md#python-analysis)
- **JavaScript/TypeScript** → [JS/TS patterns](EXAMPLES.md#javascript-analysis)
- **Java** → [Java architecture tools](REFERENCE.md#java-tools)
- **Go** → [Go analysis patterns](EXAMPLES.md#go-analysis)

## Common Gotchas (Top 3)

1. **Analysis Paralysis** - Over-analyzing without implementation
   - **Solution**: Timebox analysis to 2-4 hours, validate with prototypes
   - More details in [GOTCHAS.md](GOTCHAS.md#analysis-paralysis)

2. **Ignoring Conway's Law** - Architecture doesn't match team structure
   - **Solution**: Align team boundaries with architectural boundaries
   - See [organizational patterns](GOTCHAS.md#conways-law)

3. **Premature Optimization** - Over-engineering for imagined scale
   - **Solution**: Design for current +1 order of magnitude only
   - Read [scaling guidelines](GOTCHAS.md#premature-optimization)

Full list of gotchas in [GOTCHAS.md](GOTCHAS.md).

## Architecture Evaluation Process

```
1. Discovery & Documentation
   ├── Map current architecture
   ├── Identify components & boundaries
   └── Document data flows

2. Pattern Analysis
   ├── Identify architectural patterns
   └── Detect anti-patterns

3. Quality Attributes Assessment
   ├── Performance, Scalability, Security
   └── Reliability, Maintainability

4. Technical Analysis
   ├── SOLID compliance
   ├── Coupling & cohesion
   └── Dependency analysis

5. Risk & Debt Assessment
   ├── Identify risks
   └── Quantify technical debt

6. Recommendations & Roadmap
   ├── Prioritize improvements
   └── Create remediation plan
```

## Best Practices

### DO's
1. **Document Architecture Early** - Create diagrams before coding
2. **Use Standard Models** - Adopt C4, 4+1, or other frameworks
3. **Capture Decisions** - Write ADRs for significant choices
4. **Measure Quality Attributes** - Define metrics upfront
5. **Automate Governance** - Use fitness functions

### DON'Ts
1. **Don't Over-Engineer** - Build for current +1 magnitude
2. **Don't Ignore NFRs** - Non-functional requirements matter
3. **Don't Copy Blindly** - Netflix architecture ≠ your startup
4. **Don't Skip Documentation** - Future you will thank you
5. **Don't Work in Isolation** - Involve stakeholders

## Related Skills

- `gap-analysis-framework` - For identifying architectural gaps
- `security-scanning-suite` - For security architecture assessment
- `evaluation-reporting-framework` - For comprehensive reports
- `codebase-onboarding-analyzer` - For architecture understanding
- `git-mastery-suite` - For analyzing architectural evolution

## Quick Reference

### Key Commands
```bash
# Analyze SOLID compliance
python patterns/solid_analyzer.py src/

# Generate coupling report
python patterns/coupling_analyzer.py src/

# Create C4 diagrams
python patterns/c4_generator.py

# Generate ADR
python patterns/adr_manager.py new "Use Redis for caching"

# Run ATAM evaluation
python patterns/atam_evaluator.py
```

### Essential Resources
- [C4 Model](https://c4model.com/) - Architecture documentation
- [ATAM Guide](https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=513908) - Trade-off analysis
- [ADR Repository](https://adr.github.io/) - Decision records
- [12 Factor App](https://12factor.net/) - Modern app principles

See [REFERENCE.md](REFERENCE.md) for complete API documentation and [KNOWLEDGE.md](KNOWLEDGE.md) for theoretical foundations.
