---
name: enterprise-code-analyzer
description: >
  Three-tier enterprise code analysis system. Tier 1 analyzes individual
  repositories (structure, patterns, dependencies, memory). Tier 2 maps
  cross-repository relationships (API contracts, shared libraries, service
  coupling). Tier 3 provides enterprise governance (technology portfolio,
  technical debt, security audit, strategic recommendations). Generates
  local .memory folders, .cursorrules files, and governance reports.
license: MIT
compatibility: "Requires git and gh (GitHub CLI). Optional: jq for JSON parsing, curl for OpenMemory sync."
metadata:
  author: anivar
  version: 1.0.0
  tags:
    - enterprise
    - code-analysis
    - repository
    - architecture
    - governance
    - technical-debt
    - security-audit
---

# Enterprise Code Analyzer

Three-tier system for enterprise-wide code understanding. Analyzes individual repositories, maps cross-repository relationships, and provides governance-level insights.

## Architecture

```
Tier 1: Repository Analysis    (individual repo structure, patterns, memory)
    |
    v
Tier 2: Cross-Repo Analysis    (relationships, API contracts, dependencies)
    |
    v
Tier 3: Enterprise Governance   (portfolio, debt, security, strategy)
```

Each tier builds on the previous. Run sequentially for full analysis, or use individual tiers independently.

## When to Apply

Reference these guidelines when:
- Setting up code memory for a new repository
- Understanding repository architecture and patterns
- Finding dependencies between services
- Identifying API contract mismatches
- Running enterprise-wide technology assessments
- Evaluating technical debt across repositories
- Conducting security and compliance audits
- Making strategic technology decisions

## Priority-Ordered References

| Priority | Reference | Tier | Description |
|----------|-----------|------|-------------|
| 1 | `repo-analysis.md` | 1 | Individual repo structure, patterns, dependencies, memory creation |
| 2 | `cross-repo-analysis.md` | 2 | Frontend-backend pairs, service dependencies, API contracts |
| 3 | `enterprise-governance.md` | 3 | Portfolio, debt, security, compliance, strategic recommendations |

## Quick Reference

### Tier 1: Repository Analysis

Creates local `.memory` folder with:
- `structure.json` — repo type, framework, architecture
- `dependencies.json` — dependency catalog
- `relationships.json` — (added by Tier 2)

Also generates `.cursorrules` for IDE integration.

### Tier 2: Cross-Repository Relationships

Maps:
- Frontend-backend pairs with API coverage
- Service dependency graphs
- Shared library versions and mismatches
- Import relationships between repos

### Tier 3: Enterprise Governance

Produces:
- Technology portfolio assessment
- Architecture pattern discovery
- Technical debt registry
- Security and compliance audit
- Strategic recommendations (immediate, short-term, long-term)

## Problem to Reference Mapping

| Problem | Start With |
|---------|------------|
| Analyze a single repository | `repo-analysis.md` |
| Generate .cursorrules for a repo | `repo-analysis.md` |
| Find service dependencies | `cross-repo-analysis.md` |
| Check API contract alignment | `cross-repo-analysis.md` |
| Version consistency across repos | `cross-repo-analysis.md` |
| Technology portfolio overview | `enterprise-governance.md` |
| Technical debt assessment | `enterprise-governance.md` |
| Security audit | `enterprise-governance.md` |
| Strategic planning | `enterprise-governance.md` |

## Full Compiled Document

For the complete guide with all tiers expanded: `AGENTS.md`

## Usage Examples

```
# Tier 1: Analyze single repository
Analyze this repository and create .memory folder.

# Tier 1: Update existing memory
Update the .memory folder for this repository.

# Tier 2: Cross-repo relationships
Analyze relationships between all repositories in ~/projects/.

# Tier 2: API contract check
Are there any API mismatches between frontend and backend?

# Tier 3: Enterprise governance
Run enterprise governance analysis across all repositories.

# Tier 3: Technical debt
Generate technical debt registry for the organization.

# Tier 3: Security audit
Run security and compliance audit across all repositories.
```
