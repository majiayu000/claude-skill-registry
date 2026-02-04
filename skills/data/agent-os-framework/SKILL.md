---
name: agent-os-framework
description: Generate standardized .agent-os directory structure with product documentation, mission, tech-stack, roadmap, and decision records. Enables AI-native workflows.
version: 1.0.0
category: workspace-hub
type: skill
trigger: manual
auto_execute: false
capabilities:
  - product_documentation
  - mission_definition
  - tech_stack_documentation
  - roadmap_planning
  - decision_records
tools:
  - Write
  - Read
  - Bash
related_skills:
  - repo-readiness
  - python-project-template
---

# Agent OS Framework

> Generate standardized .agent-os structure for AI-native repository workflows.

## Quick Start

```bash
# Generate full .agent-os structure
/agent-os-framework

# Generate for existing project
/agent-os-framework --update

# Generate specific component
/agent-os-framework --component mission
```

## When to Use

**USE when:**
- Setting up new repository
- Adding AI workflow support
- Documenting product vision
- Creating decision records

**DON'T USE when:**
- Project has complete .agent-os
- Non-product repositories (e.g., dotfiles)

## Prerequisites

- Repository initialized with git
- Basic project understanding
- Stakeholder input for mission

## Overview

Creates complete .agent-os structure:

1. **product/** - Core product documentation
2. **specs/** - Feature specifications
3. **standards/** - Code style guidelines
4. **instructions/** - Workflow instructions

## Directory Structure

```
.agent-os/
├── product/
│   ├── mission.md        # Product pitch, users, pain points
│   ├── tech-stack.md     # Technology choices
│   ├── roadmap.md        # Development phases
│   └── decisions.md      # Decision log
├── specs/
│   └── README.md         # Spec index
├── standards/
│   ├── code-style.md     # Coding guidelines
│   └── testing.md        # Testing guidelines
└── instructions/
    ├── create-spec.md    # How to create specs
    └── execute-tasks.md  # How to execute tasks
```

## Core Templates

### 1. mission.md

```markdown
# Mission: [Project Name]

> [One-line pitch describing the project's core purpose]

## Product Pitch

[2-3 paragraph description of what the product does, why it exists, and what problem it solves]

## Target Users

### Primary Users
- **[User Type 1]**: [Description and needs]
- **[User Type 2]**: [Description and needs]

### Secondary Users
- **[User Type 3]**: [Description and needs]

## Pain Points Addressed

### Before This Product
1. **[Pain Point 1]**: [Description of the problem]
2. **[Pain Point 2]**: [Description of the problem]
3. **[Pain Point 3]**: [Description of the problem]

### After This Product
1. **[Solution 1]**: [How this product solves the problem]
2. **[Solution 2]**: [How this product solves the problem]
3. **[Solution 3]**: [How this product solves the problem]

## Success Metrics

| Metric | Current | Target | Timeframe |
|--------|---------|--------|-----------|
| [Metric 1] | [Current value] | [Target value] | [When] |
| [Metric 2] | [Current value] | [Target value] | [When] |
| [Metric 3] | [Current value] | [Target value] | [When] |

## Differentiators

### What Makes This Unique
1. **[Differentiator 1]**: [Description]
2. **[Differentiator 2]**: [Description]
3. **[Differentiator 3]**: [Description]

### Competitive Landscape
- **[Competitor 1]**: [How we differ]
- **[Competitor 2]**: [How we differ]

## Non-Goals

Things explicitly out of scope:
- [Non-goal 1]
- [Non-goal 2]
- [Non-goal 3]

---

*Last Updated: [Date]*
*Version: 1.0.0*
```

### 2. tech-stack.md

```markdown
# Tech Stack: [Project Name]

> Technical architecture and technology choices

## Overview

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| Language | Python | 3.11+ | Primary development |
| Package Manager | UV | Latest | Fast dependency management |
| Testing | pytest | 7.4+ | Test framework |
| Visualization | Plotly | 5.15+ | Interactive charts |
| Data | Pandas | 2.0+ | Data processing |

## Core Technologies

### Python 3.11+
**Why**: Modern async support, performance improvements, type hints
**Usage**: All source code in `src/`

### UV Package Manager
**Why**: 10-100x faster than pip, reliable lockfiles
**Usage**: `uv venv`, `uv pip install`

### pytest
**Why**: Industry standard, excellent fixtures, plugins
**Usage**: All tests in `tests/`

### Plotly
**Why**: Interactive plots, HTML export, professional appearance
**Usage**: All visualizations must be interactive (no static matplotlib)

### Pandas
**Why**: Data manipulation, time series, CSV handling
**Usage**: Data loading and transformation

## Development Tools

| Tool | Purpose | Configuration |
|------|---------|---------------|
| ruff | Linting | pyproject.toml |
| black | Formatting | pyproject.toml |
| mypy | Type checking | pyproject.toml |
| pytest-cov | Coverage | pytest.ini |

## Infrastructure

### Version Control
- **Git**: Source control
- **GitHub**: Remote repository
- **Branch Strategy**: main → feature branches → PR

### CI/CD
- **GitHub Actions**: Automated testing
- **Coverage**: Minimum 80%

## Data Storage

| Type | Location | Format |
|------|----------|--------|
| Raw data | data/raw/ | CSV, JSON |
| Processed | data/processed/ | CSV, Parquet |
| Results | data/results/ | CSV, JSON |
| Reports | reports/ | HTML |

## External Dependencies

### APIs
- [API 1]: [Purpose]
- [API 2]: [Purpose]

### Services
- [Service 1]: [Purpose]
- [Service 2]: [Purpose]

## Decision Rationale

### Why Python?
- Strong ecosystem for data analysis
- Excellent library support (Pandas, NumPy, Plotly)
- Team expertise
- Integration with existing tools

### Why UV over pip?
- Significantly faster installation
- Reliable dependency resolution
- Lockfile support
- workspace-hub standard

### Why Plotly over Matplotlib?
- Interactive by default
- Better HTML export
- Modern API
- workspace-hub HTML reporting standard

---

*Last Updated: [Date]*
*Version: 1.0.0*
```

### 3. roadmap.md

```markdown
# Roadmap: [Project Name]

> Development phases and milestones

## Vision

[Long-term vision for the product - where it will be in 1-2 years]

## Current Phase

**Phase [N]: [Phase Name]**
- Status: [In Progress / Planning / Complete]
- Target: [Date]
- Progress: [X]%

## Phase Overview

```
Phase 1: Foundation      [████████████████████] 100%
Phase 2: Core Features   [████████████░░░░░░░░]  60%
Phase 3: Enhancement     [░░░░░░░░░░░░░░░░░░░░]   0%
Phase 4: Scale           [░░░░░░░░░░░░░░░░░░░░]   0%
Phase 5: Optimization    [░░░░░░░░░░░░░░░░░░░░]   0%
```

## Detailed Phases

### Phase 1: Foundation ✅
**Goal**: Establish project structure and basic functionality
**Duration**: 2 weeks

#### Deliverables
- [x] Project structure setup
- [x] Basic configuration
- [x] Core module implementation
- [x] Initial test coverage (80%+)
- [x] Documentation framework

#### Key Outcomes
- Working development environment
- Basic functionality operational
- CI/CD pipeline configured

---

### Phase 2: Core Features 🚧
**Goal**: Implement primary feature set
**Duration**: 4 weeks

#### Deliverables
- [x] Feature A implementation
- [x] Feature B implementation
- [ ] Feature C implementation
- [ ] Integration testing
- [ ] Documentation complete

#### Key Outcomes
- Primary use cases supported
- User-facing functionality complete
- Quality standards met

---

### Phase 3: Enhancement 📋
**Goal**: Add secondary features and improvements
**Duration**: 3 weeks

#### Deliverables
- [ ] Advanced Feature D
- [ ] Performance optimizations
- [ ] Additional integrations
- [ ] Extended test coverage
- [ ] User documentation

#### Key Outcomes
- Feature-complete product
- Performance targets met
- Full documentation

---

### Phase 4: Scale 📋
**Goal**: Prepare for production scale
**Duration**: 2 weeks

#### Deliverables
- [ ] Performance testing
- [ ] Load testing
- [ ] Security review
- [ ] Deployment automation
- [ ] Monitoring setup

#### Key Outcomes
- Production-ready
- Monitoring operational
- Runbook complete

---

### Phase 5: Optimization 📋
**Goal**: Continuous improvement
**Duration**: Ongoing

#### Deliverables
- [ ] User feedback integration
- [ ] Performance tuning
- [ ] Technical debt reduction
- [ ] Feature iteration

#### Key Outcomes
- Improved user satisfaction
- Better performance
- Reduced maintenance burden

## Milestones

| Milestone | Target Date | Status |
|-----------|------------|--------|
| MVP Complete | [Date] | ✅ |
| Beta Release | [Date] | 🚧 |
| Production Release | [Date] | 📋 |
| Feature Complete | [Date] | 📋 |

## Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | Medium | High | [Mitigation strategy] |
| [Risk 2] | Low | Medium | [Mitigation strategy] |
| [Risk 3] | High | Low | [Mitigation strategy] |

## Dependencies

### External
- [Dependency 1]: Required for [Feature]
- [Dependency 2]: Required for [Feature]

### Internal
- [Team/Resource 1]: [What's needed]
- [Team/Resource 2]: [What's needed]

---

*Last Updated: [Date]*
*Version: 1.0.0*
```

### 4. decisions.md

```markdown
# Decision Log: [Project Name]

> Record of architectural and design decisions

## How to Use This Document

Document significant technical decisions using the format below. Include context, options considered, and rationale.

## Decision Template

```markdown
### DEC-XXX: [Decision Title]
**Date**: YYYY-MM-DD
**Status**: [Proposed | Accepted | Deprecated | Superseded]
**Deciders**: [Names or roles]

#### Context
[What is the issue or opportunity?]

#### Options Considered
1. **Option A**: [Description]
   - Pros: [Benefits]
   - Cons: [Drawbacks]

2. **Option B**: [Description]
   - Pros: [Benefits]
   - Cons: [Drawbacks]

#### Decision
[Which option was chosen and why]

#### Consequences
- Positive: [Good outcomes]
- Negative: [Trade-offs accepted]

#### Related
- [Links to related decisions, issues, docs]
```

---

## Decisions

### DEC-001: Package Manager Selection
**Date**: 2026-01-01
**Status**: Accepted
**Deciders**: Engineering Team

#### Context
Need to select a Python package manager for dependency management across the project.

#### Options Considered
1. **pip + requirements.txt**
   - Pros: Universal, simple
   - Cons: Slow, no lockfile

2. **poetry**
   - Pros: Modern, lockfile support
   - Cons: Slower than UV

3. **UV**
   - Pros: Very fast, lockfiles, drop-in pip replacement
   - Cons: Newer tool

#### Decision
Use UV as the primary package manager.

#### Consequences
- Positive: 10-100x faster installations, reliable builds
- Negative: Team needs to learn UV commands

---

### DEC-002: Visualization Library
**Date**: 2026-01-01
**Status**: Accepted
**Deciders**: Engineering Team

#### Context
Need to select visualization library for data analysis reports.

#### Options Considered
1. **Matplotlib**
   - Pros: Widely used, flexible
   - Cons: Static images, complex API

2. **Plotly**
   - Pros: Interactive, HTML export, modern
   - Cons: Larger bundle size

3. **Altair**
   - Pros: Declarative, clean syntax
   - Cons: Less flexible than Plotly

#### Decision
Use Plotly for all visualizations.

#### Consequences
- Positive: Interactive reports, better user experience
- Negative: No static image export (design decision)
- Note: Aligns with workspace-hub HTML reporting standards

---

### DEC-003: Testing Framework
**Date**: 2026-01-01
**Status**: Accepted
**Deciders**: Engineering Team

#### Context
Need to select testing framework for the project.

#### Options Considered
1. **unittest**
   - Pros: Built-in, no dependencies
   - Cons: Verbose, limited features

2. **pytest**
   - Pros: Fixtures, plugins, markers, excellent output
   - Cons: External dependency

#### Decision
Use pytest with pytest-cov for coverage.

#### Consequences
- Positive: Better developer experience, powerful fixtures
- Negative: Additional dependency (acceptable trade-off)

---

## Pending Decisions

### DEC-004: [Pending Decision Title]
**Date**: Pending
**Status**: Proposed

[Description of pending decision]

---

*Last Updated: [Date]*
*Total Decisions: 3 Accepted, 1 Pending*
```

## Usage Examples

### Example 1: New Project Setup

```bash
# Generate complete .agent-os
/agent-os-framework

# Creates:
# - .agent-os/product/mission.md
# - .agent-os/product/tech-stack.md
# - .agent-os/product/roadmap.md
# - .agent-os/product/decisions.md
# - .agent-os/specs/README.md
# - .agent-os/standards/code-style.md
# - .agent-os/instructions/create-spec.md
```

### Example 2: Update Existing

```bash
# Add missing components
/agent-os-framework --update

# Only creates files that don't exist
```

## Execution Checklist

**Initial Setup:**
- [ ] Create .agent-os directory
- [ ] Generate product/ documents
- [ ] Generate specs/ structure
- [ ] Generate standards/
- [ ] Generate instructions/

**Content Review:**
- [ ] Update mission with actual project details
- [ ] Fill in tech-stack choices
- [ ] Define roadmap phases
- [ ] Document initial decisions

## Best Practices

1. **Keep mission current** - Review quarterly
2. **Document decisions promptly** - When made, not later
3. **Update roadmap status** - Weekly or bi-weekly
4. **Reference in CLAUDE.md** - Link from root config

## Related Skills

- [repo-readiness](../repo-readiness/SKILL.md) - Validates .agent-os
- [python-project-template](../python-project-template/SKILL.md) - Creates initial structure

## References

- [Agent OS Framework](https://buildermethods.com/agent-os)
- [workspace-hub Standards](../../../docs/modules/standards/)

---

## Version History

- **1.0.0** (2026-01-14): Initial release - .agent-os framework with mission, tech-stack, roadmap, and decisions
