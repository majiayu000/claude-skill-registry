---
name: modular-skills
description: |
  Architect skills as modular blocks to control token usage and complexity.
  Triggers: skills, architecture, modular, design-patterns, modularity, skill design, skill architecture, modularization, token optimization, skill structure, refactoring skills, new skill creation, skill complexity.
  Use when creating skills >150 lines, breaking down monolithic skills, or planning new architecture.
  Do not use for evaluating existing skills (use skills-eval) or writing human-facing prose (use writing-clearly-and-concisely).
  Check this skill before starting any new skill development.
category: workflow-optimization
tags: [architecture, modularity, tokens, skills, design-patterns, skill-design, token-optimization]
dependencies: []
tools: [skill-analyzer, token-estimator, module-validator]
usage_patterns:
  - skill-design
  - architecture-review
  - token-optimization
  - refactoring-workflows
complexity: intermediate
estimated_tokens: 1200
version: 1.3.5
---
## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Workflow and Tasks](#workflow-and-tasks)
- [Quality Checks](#quality-checks)
- [Resources](#resources)


# Modular Skills Design

## Overview

This framework breaks complex skills into focused modules to keep token usage predictable and avoid monolithic files. We use progressive disclosure: starting with essentials and loading deeper technical details via `@include` or `Load:` statements only when needed. This approach prevents hitting context limits during long-running tasks.

Modular design keeps file sizes within recommended limits, typically under 150 lines. Shallow dependencies and clear boundaries simplify testing and maintenance. The hub-and-spoke model allows the project to grow without bloating primary skill files, making focused modules easier to verify in isolation and faster to parse.

### Core Components

Three tools support modular skill development:
- `skill-analyzer`: Checks complexity and suggests where to split code.
- `token-estimator`: Forecasts usage and suggests optimizations.
- `module-validator`: Verifies that structure complies with project standards.

### Design Principles

We design skills around single responsibility and loose coupling. Each module focuses on one task, minimizing dependencies to keep the architecture cohesive. Clear boundaries and well-defined interfaces prevent changes in one module from breaking others. This follows Anthropic's Agent Skills best practices: provide a high-level overview first, then surface details as needed to maintain context efficiency.

## Quick Start

### Skill Analysis
Analyze modularity using `scripts/analyze.py`. You can set a custom threshold for line counts to identify files that need splitting.
```bash
python scripts/analyze.py --threshold 100
```
From Python, use `analyze_skill` from `abstract.skill_tools`.

### Token Usage Planning
Estimate token consumption to verify your skill stays within budget. Run this from the skill directory:
```bash
python scripts/tokens.py
```

### Module Validation
Check for structure and pattern compliance before deployment.
```bash
python scripts/abstract_validator.py --scan
```

## Workflow and Tasks

Start by assessing complexity with `skill_analyzer.py`. If a skill exceeds 150 lines, break it into focused modules following the patterns in `../../docs/examples/modular-skills/`. Use `token_estimator.py` to check efficiency and `abstract_validator.py` to verify the final structure. This iterative process maintains module maintainability and token efficiency.

## Quality Checks

Identify modules needing attention by checking line counts and missing Table of Contents. Any module over 100 lines requires a TOC after the frontmatter to aid navigation.
```bash
# Find modules exceeding 100 lines
find modules -name "*.md" -exec wc -l {} + | awk '$1 > 100'
```

### Standards Compliance

Our standards prioritize concrete examples and a consistent voice. Always provide actual commands in Quick Start sections instead of abstract descriptions. Use third-person perspective (e.g., "the project", "developers") rather than "you" or "your". Each code example should be followed by a validation command. For discoverability, descriptions must include at least five specific trigger phrases.

### TOC Template
```markdown
## Table of Contents

- [Section Name](#section-name)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
```

## Resources

### Shared Modules: Cross-Skill Patterns
Standard patterns for triggers, enforcement language, and anti-rationalization:
- **Trigger Patterns**: See [trigger-patterns.md](modules/enforcement-patterns.md)
- **Enforcement Language**: See [enforcement-language.md](../shared-patterns/modules/workflow-patterns.md)
- **Anti-Rationalization**: See [anti-rationalization.md](../skill-authoring/modules/anti-rationalization.md)

### Skill-Specific Modules
Detailed guides for implementation and maintenance:
- **Enforcement Patterns**: See `modules/enforcement-patterns.md`
- **Core Workflow**: See `modules/core-workflow.md`
- **Implementation Patterns**: See `modules/implementation-patterns.md`
- **Migration Guide**: See `modules/antipatterns-and-migration.md`
- **Design Philosophy**: See `modules/design-philosophy.md`
- **Troubleshooting**: See `modules/troubleshooting.md`

### Tools and Examples
- **Tools**: `skill_analyzer.py`, `token_estimator.py`, and `abstract_validator.py` in `../../scripts/`.
- **Examples**: See `../../docs/examples/modular-skills/` for reference implementations.
