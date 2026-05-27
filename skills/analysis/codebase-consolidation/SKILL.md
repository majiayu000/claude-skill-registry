---
name: codebase-consolidation
description: Analyze, consolidate, and document codebases through multi-perspective analysis. Use when reviewing project structure, planning refactoring, creating documentation, or assessing technical debt.
---

# Codebase Consolidation & Analysis

Systematically analyze codebases to identify consolidation opportunities, document architecture, and generate actionable insights.

## Quick Reference

- **[Analysis Dimensions](analysis-dimensions.md)** - 8 analysis dimensions with detailed criteria
- **[Consolidation Patterns](consolidation-patterns.md)** - Common refactoring patterns with examples
- **[Report Templates](report-templates.md)** - Output format templates

## When to Use

- Starting on a new codebase - Understand structure quickly
- Planning refactoring - Identify consolidation opportunities
- Code review preparation - Comprehensive analysis before changes
- Documentation needs - Generate architecture docs
- Technical debt assessment - Quantify and prioritize improvements
- Onboarding new developers - Create codebase overview
- Pre-release audits - Quality and security review

**Don't use for**: Single file analysis, quick bug fixes, simple feature additions

## Core Purpose

Comprehensive codebase analysis:
- **Code Duplication** - Find duplicate code for consolidation
- **Architectural Analysis** - Document system structure and patterns
- **Refactoring Opportunities** - Identify improvement areas
- **Technical Debt Assessment** - Quantify and prioritize debt
- **Documentation Generation** - Create architecture diagrams and docs
- **Multi-Perspective Analysis** - Review from architect, developer, product views
- **Quality Metrics** - Complexity, coverage, maintainability

## Analysis Dimensions

| Dimension | Focus |
|-----------|-------|
| Code Duplication | Find duplicate/similar code blocks |
| Architectural Structure | System architecture and component relationships |
| Code Organization | Module structure and separation of concerns |
| Refactoring Opportunities | Large files, complex functions |
| Technical Debt | TODOs, missing tests, outdated deps |
| Quality Metrics | LOC, complexity, coverage |
| Design Patterns | Patterns and anti-patterns in use |
| Cross-Cutting Concerns | Error handling, logging, security |

See **[analysis-dimensions.md](analysis-dimensions.md)** for detailed criteria.

## Analysis Workflow

1. **Discovery** - Project structure, file counts, configuration
2. **Dependency Analysis** - cargo tree, outdated, audit
3. **Duplication Detection** - Large files, tech debt markers
4. **Complexity Analysis** - LOC statistics, long functions
5. **Architecture Mapping** - Components, dependencies, data flow
6. **Quality Assessment** - Coverage, linting, formatting
7. **Documentation Review** - Doc generation, API documentation
8. **Synthesis** - Comprehensive report with recommendations

## Output Formats

- **Executive Summary** - Health score, key metrics, priorities
- **Architecture Documentation** - System diagram, patterns, data flows
- **Refactoring Roadmap** - Phased plan with tasks and estimates
- **Technical Debt Report** - Quantified debt, payoff strategy
- **Onboarding Document** - Developer guide to codebase

See **[report-templates.md](report-templates.md)** for complete templates.

## Best Practices

✓ Start with high-level structure, use automated tools, prioritize findings, provide concrete examples with file paths, estimate effort, consider multiple perspectives

✗ Don't analyze without clear goals, only report problems, provide generic advice, ignore context, recommend big rewrites, overwhelm with detail

See **[consolidation-patterns.md](consolidation-patterns.md)** for refactoring patterns and examples.
