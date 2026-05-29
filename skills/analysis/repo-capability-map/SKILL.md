---
name: repo-capability-map
description: Analyzes repository modules for current capabilities, groups them by domain, and identifies strategic gaps against mission objectives
version: 1.0.0
category: workspace-hub
type: skill
trigger: manual
auto_execute: false
capabilities:
  - capability_discovery
  - domain_classification
  - maturity_assessment
  - gap_analysis
  - cross_repo_comparison
  - capability_reporting
tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
related_skills: [repository-health-analyzer, work-queue, claude-reflect, compliance-check]
---

# Repo Capability Map

> Discover what each repository can do, classify capabilities by domain, assess maturity, and identify strategic gaps.

## Purpose

While `repository-health-analyzer` asks "is the repo well-maintained?", this skill asks **"what can this repo do, and what's missing?"**

It produces a structured capability inventory across the entire workspace, enabling:
- Strategic planning against mission objectives
- Identification of capability gaps before they become blockers
- Cross-repo dependency awareness
- Maturity tracking over time

## Capability Taxonomy

Two-level hierarchy: **Domain** > **Capability Area**

| Domain ID | Domain Name | Description |
|-----------|-------------|-------------|
| `ENG` | Engineering Analysis | Simulation, modeling, structural/fatigue analysis |
| `DATA` | Data & Analytics | Data pipelines, visualization, statistical analysis |
| `WEB` | Web & Frontend | Websites, UI components, client-side applications |
| `BIZ` | Business Operations | Admin tools, invoicing, client management |
| `INFRA` | Infrastructure & DevOps | CI/CD, packaging, deployment, shared utilities |
| `KNOW` | Knowledge & Documentation | Media, resumes, knowledge bases, training materials |
| `FIN` | Financial & Investments | Portfolio tracking, financial modeling, reporting |

The taxonomy is **discovered dynamically** -- the agent maps findings to known domains but can create new ones if a repo doesn't fit.

## Maturity Model

| Level | Label | Criteria |
|-------|-------|----------|
| 1 | **Nascent** | Mentioned in mission/roadmap but no implementation exists |
| 2 | **Emerging** | Partial implementation, <50% test coverage, active WIP |
| 3 | **Established** | Working implementation with tests, docs, CLI/API available |
| 4 | **Mature** | Production-grade, 80%+ coverage, skills defined, decision history |

Assessment is based on **observable artifacts** (files exist, tests present, skills defined) -- not subjective judgments.

## Analysis Methodology

For each repo, read files in priority order:

### Tier 1 -- Declared Identity (highest confidence)
- `README.md` -- mission, capabilities snapshot, features
- `CLAUDE.md` -- tech stack, project rules, domain keywords
- `.agent-os/product/mission.md` -- strategic phases, success metrics
- `.agent-os/product/roadmap.md` -- planned features, completion status

### Tier 2 -- Structural Evidence
- `src/` directory tree -- module names, sub-packages
- `.claude/skills/` -- domain skills (each skill = capability signal)
- `pyproject.toml` / `package.json` -- dependencies, entry points
- `tests/` and `docs/` structure

### Tier 3 -- Behavioral Evidence
- `git log --oneline -30` -- recent activity, development focus
- `scripts/` directory -- automation capabilities
- `data/` / `config/` contents -- data domains

## Actions

| Action | File | Description |
|--------|------|-------------|
| scan | `actions/scan.md` | Extract capabilities from one or all repos |
| gaps | `actions/gaps.md` | Analyze gaps against mission objectives |
| report | `actions/report.md` | Generate console summary + markdown report |
| compare | `actions/compare.md` | Side-by-side comparison between two repos |

## Templates

| Template | File | Description |
|----------|------|-------------|
| Repo Profile | `templates/repo-profile.md` | Per-repo capability profile |
| Capability Report | `templates/capability-report.md` | Full workspace capability report |

## Integration Points

- **repository-health-analyzer** -- health gates capability scanning (unhealthy repos get flagged)
- **work-queue** -- gap analysis can feed `/work add` items for uncovered objectives
- **claude-reflect** -- periodic reflection includes capability changes over time
- **compliance-check** -- repos missing CLAUDE.md receive lower maturity scores

## Command Reference

See `@.claude/commands/workspace-hub/repo-capability-map.md` for usage.
