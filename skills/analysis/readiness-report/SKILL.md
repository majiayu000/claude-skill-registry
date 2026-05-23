---
name: readiness-report
description: Evaluate how well a codebase supports autonomous AI development. Analyzes repositories across eight technical pillars (Style & Validation, Build System, Testing, Documentation, Dev Environment, Debugging & Observability, Security, Task Discovery) and five maturity levels. Use when users request `/readiness-report` or want to assess agent readiness, codebase maturity, or identify gaps preventing effective AI-assisted development.
triggers:
- /readiness-report
---

# Agent Readiness Report

Evaluate how well a repository supports autonomous AI development by analyzing it across eight technical pillars and five maturity levels.

## Overview

Agent Readiness measures how prepared a codebase is for AI-assisted development. Poor feedback loops, missing documentation, or lack of tooling cause agents to waste cycles on preventable errors. This skill identifies those gaps and prioritizes fixes.

## Quick Start

The user will run `/readiness-report` to evaluate the current repository. The agent will then:
1. Clone the repo, scan repository structure, CI configs, and tooling
2. Evaluate 81 criteria across 9 technical pillars
3. Determine maturity level (L1-L5) based on 80% threshold per level
4. Provide prioritized recommendations

## Workflow

### Step 1: Run Repository Analysis

Execute the analysis script to gather signals from the repository:

```bash
python scripts/analyze_repo.py --repo-path .
```

This script checks for:
- Configuration files (.eslintrc, pyproject.toml, etc.)
- CI/CD workflows (.github/workflows/, .gitlab-ci.yml)
- Documentation (README, AGENTS.md, CONTRIBUTING.md)
- Test infrastructure (test directories, coverage configs)
- Security configurations (CODEOWNERS, .gitignore, secrets management)

### Step 2: Generate Report

After analysis, generate the formatted report:

```bash
python scripts/generate_report.py --analysis-file /tmp/readiness_analysis.json
```

### Step 3: Present Results

The report includes:
1. **Overall Score**: Pass rate percentage and maturity level achieved
2. **Level Progress**: Bar showing L1-L5 completion percentages
3. **Strengths**: Top-performing pillars with passing criteria
4. **Opportunities**: Prioritized list of improvements to implement
5. **Detailed Criteria**: Full breakdown by pillar showing each criterion status

## Nine Technical Pillars

Each pillar addresses specific failure modes in AI-assisted development:

| Pillar | Purpose | Key Signals |
|--------|---------|-------------|
| **Style & Validation** | Catch bugs instantly | Linters, formatters, type checkers |
| **Build System** | Fast, reliable builds | Build docs, CI speed, automation |
| **Testing** | Verify correctness | Unit/integration tests, coverage |
| **Documentation** | Guide the agent | AGENTS.md, README, architecture docs |
| **Dev Environment** | Reproducible setup | Devcontainer, env templates |
| **Debugging & Observability** | Diagnose issues | Logging, tracing, metrics |
| **Security** | Protect the codebase | CODEOWNERS, secrets management |
| **Task Discovery** | Find work to do | Issue templates, PR templates |
| **Product & Analytics** | Error-to-insight loop | Error tracking, product analytics |

See `references/criteria.md` for the complete list of 81 criteria per pillar.

## Five Maturity Levels

| Level | Name | Description | Agent Capability |
|-------|------|-------------|------------------|
| L1 | Initial | Basic version control | Manual assistance only |
| L2 | Managed | Basic CI/CD and testing | Simple, well-defined tasks |
| L3 | Standardized | Production-ready for agents | Routine maintenance |
| L4 | Measured | Comprehensive automation | Complex features |
| L5 | Optimized | Full autonomous capability | End-to-end development |

**Level Progression**: To unlock a level, pass ≥80% of criteria at that level AND all previous levels.

See `references/maturity-levels.md` for detailed level requirements.

## Interpreting Results

### Pass vs Fail vs Skip

- ✓ **Pass**: Criterion met (contributes to score)
- ✗ **Fail**: Criterion not met (opportunity for improvement)
- — **Skip**: Not applicable to this repository type (excluded from score)

### Priority Order

Fix gaps in this order:
1. **L1-L2 failures**: Foundation issues blocking basic agent operation
2. **L3 failures**: Production readiness gaps
3. **High-impact L4+ failures**: Optimization opportunities

### Common Quick Wins

1. **Add AGENTS.md**: Document commands, architecture, and workflows for AI agents
2. **Configure pre-commit hooks**: Catch style issues before CI
3. **Add PR/issue templates**: Structure task discovery
4. **Document single-command setup**: Enable fast environment provisioning

## Resources

- `scripts/analyze_repo.py` - Repository analysis script
- `scripts/generate_report.py` - Report generation and formatting
- `references/criteria.md` - Complete criteria definitions by pillar
- `references/maturity-levels.md` - Detailed level requirements

## Automated Remediation

After reviewing the report, common fixes can be automated:
- Generate AGENTS.md from repository structure
- Add missing issue/PR templates
- Configure standard linters and formatters
- Set up pre-commit hooks

Ask to "fix readiness gaps" to begin automated remediation of failing criteria.
