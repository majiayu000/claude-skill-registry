---
name: modular-skills
description: |

Triggers: skills, architecture, modular, design-patterns, modularity
  Design skills as modular building blocks for predictable token usage.

  Triggers: skill design, skill architecture, modularization, token optimization,
  skill structure, refactoring skills, new skill creation, skill complexity

  Use when: creating new skills that will be >150 lines, breaking down complex
  monolithic skills, planning skill architecture, refactoring overlapping skills,
  reviewing skill maintainability, designing skill module structure

  DO NOT use when: evaluating existing skill quality - use skills-eval instead.
  DO NOT use when: writing prose for humans - use writing-clearly-and-concisely.
  DO NOT use when: need improvement recommendations - use skills-eval.

  Use this skill BEFORE creating any new skill. Check even if unsure.
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
---
## Table of Contents

- [Overview](#overview)
- [Key Benefits](#key-benefits)
- [Core Components](#core-components)
- [Design Principles](#design-principles)
- [What It Is](#what-it-is)
- [Quick Start](#quick-start)
- [Skill Analysis](#skill-analysis)
- [Token Usage Planning](#token-usage-planning)
- [Module Validation](#module-validation)
- [Implementation Workflow](#implementation-workflow)
- [Common Tasks](#common-tasks)
- [Quality Checks](#quality-checks)
- [Module Structure Validation](#module-structure-validation)
- [Essential Quality Standards](#essential-quality-standards)
- [TOC Template for Long Modules](#toc-template-for-long-modules)
- [Table of Contents](#table-of-contents)
- [Detailed Resources](#detailed-resources)
- [Shared Modules (Cross-Skill Patterns)](#shared-modules-(cross-skill-patterns))
- [Skill-Specific Modules](#skill-specific-modules)
- [Tools and Examples](#tools-and-examples)


# Modular Skills Design

## Overview

The modular skills framework provides a methodology for breaking complex skills into focused modules. This approach supports predictable token usage by preventing monolithic files that consume excessive context. By implementing progressive disclosure, skills start with essential information and provide deeper technical details via `@include` or `Load:` statements only when required.

### Outcome Analysis

Modular design results in controlled resource usage by keeping individual files within recommended line limits. This architecture relies on shallow dependencies and clear boundaries between components, which simplifies testing and maintenance. A hub-and-spoke model supports project growth without bloating the primary skill files, and focused modules are easier to verify in isolation.

### Core Components

The framework includes three primary tools for skill development. The `skill-analyzer` provides complexity analysis and suggests optimal points for modularization. For resource management, the `token-estimator` forecasts usage and offers cost optimization guidance based on current skill structures. Finally, the `module-validator` performs structural quality checks to ensure compliance with project standards.

### Design Principles

Effective skill design is based on four key principles. Single responsibility ensures each module serves one clear purpose, while loose coupling minimizes dependencies between different skill components. High cohesion is maintained by grouping related functionality together, and clear boundaries provide well-defined interfaces for interaction.

## What It Is

The framework facilitates designing modular skills. Breaking down large skills into focused modules creates maintainable architecture and controls token usage.

It adheres to Anthropic's Agent Skills best practices, using progressive disclosure: start with a high-level overview, then provide detail as needed.

## Quick Start

### Skill Analysis
```bash
# Analyze skill modularity
python scripts/analyze.py

# Analyze with custom threshold (default: 150 lines)
python scripts/analyze.py --threshold 100

# Python API usage:
from abstract.skill_tools import analyze_skill
analysis = analyze_skill(".", threshold=100)
```
**Verification:** Verify Python environment with `python --version`.

### Token Usage Planning
```bash
# Estimate token consumption for your skill (works from skill directory)
python scripts/tokens.py

# Python API usage:
from abstract.skill_tools import estimate_tokens
tokens = estimate_tokens("SKILL.md")
```
**Verification:** Verify Python environment with `python --version`.

### Module Validation
```bash
# Validate modular structure and patterns
python scripts/abstract_validator.py --scan

# Generate full validation report
python scripts/abstract_validator.py --report

# Auto-fix issues (dry run first)
python scripts/abstract_validator.py --fix --dry-run
```
**Verification:** Verify Python environment with `python --version`.

### Implementation Workflow
1. **Assess**: Use `skill_analyzer.py` to identify complexity and modularization needs
2. **Design**: Break large skills into focused modules based on single responsibility
3. **Estimate**: Use `token_estimator.py` to optimize for context window efficiency
4. **Validate**: Run `abstract_validator.py` to validate proper structure and patterns
5. **Iterate**: Refine based on validation feedback and usage patterns

## Common Tasks

- **Assess skill complexity** with the `skill-analyzer` to determine modularization needs.
- **Design modules** following the workflow in `guide.md`.
- **Implement patterns** using examples in `../../docs/examples/modular-skills/`.
- **Validate module structure** with `module-validator` before deployment.
- **Estimate token usage** with `token-estimator` to optimize context window impact.

## Quality Checks

### Module Structure Validation

Before finalizing modules, verify these quality standards:

```bash
# Check module line counts
find modules -name "*.md" -exec wc -l {} + | sort -n

# Identify modules needing TOCs (>100 lines)
for file in modules/*.md; do
  lines=$(wc -l < "$file")
  if [ $lines -gt 100 ]; then
    echo "$file needs TOC ($lines lines)"
  fi
done
```
**Verification:** Verify availability with `--help`.

### Essential Quality Standards

Based on evaluation feedback (issue #74):

1. **Navigation in Long Modules**: Any module >100 lines MUST include a Table of Contents after frontmatter
2. **Quick Start Concreteness**: Provide actual commands, not abstract descriptions
3. **Voice Consistency**: Use third person - avoid "your"/"you", prefer "project"/"developers"
4. **Verification Steps**: Add validation commands after all code examples
5. **Trigger Phrases**: Include 5+ specific phrases in description for discoverability

### TOC Template for Long Modules

```markdown
## Table of Contents

- [Section Name](#section-name)
- [Another Section](#another-section)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
```
**Verification:** Verify availability with `--help`.

These quality standards emerged from real-world feedback on skill evaluation. Navigation aids such as Tables of Contents are critical for agentic search efficiency, as coding agents use grep to locate content without loading entire files. Providing concrete Quick Start commands ensures developers can immediately apply skills without the overhead of translating abstract descriptions.

## Detailed Resources

For detailed implementation details and advanced techniques:

### Shared Modules: Cross-Skill Patterns
- **Trigger Patterns**: See [trigger-patterns.md](../../shared-modules/trigger-patterns.md) for description field templates
- **Enforcement Language**: See [enforcement-language.md](../../shared-modules/enforcement-language.md) for intensity calibration
- **Anti-Rationalization**: See [anti-rationalization.md](../../shared-modules/anti-rationalization.md) for bypass prevention

### Skill-Specific Modules
- **Enforcement Patterns**: See `modules/enforcement-patterns.md` for frontmatter design patterns
- **Core Workflow**: See `modules/core-workflow.md` for detailed modularization process
- **Implementation Patterns**: See `modules/implementation-patterns.md` for coding and structure patterns
- **Migration Guide**: See `modules/antipatterns-and-migration.md` for converting existing skills
- **Design Philosophy**: See `modules/design-philosophy.md` for underlying principles and thinking
- **Troubleshooting**: See `modules/troubleshooting.md` for common issues and solutions

### Tools and Examples
- **Tools**: Python analysis utilities in `../../scripts/` directory:
  - `skill_analyzer.py` - Complexity analysis and recommendations
  - `token_estimator.py` - Token usage estimation with dependencies
  - `abstract_validator.py` - Pattern validation and auto-fixing
- **Examples**: See `../../docs/examples/modular-skills/` directory for concrete implementations
