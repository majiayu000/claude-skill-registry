---
name: performance-optimization
description: >-
  Optimize Claude Code plugin performance through progressive loading, token budgeting, and context-aware content delivery.
  performance, optimization, tokens, context, budget, progressive loading, lazy loading.
  Use when designing skills that exceed 800 tokens, auditing token consumption, reducing context footprint.
  Do not use when skills are under 300 tokens, single-purpose with no modules.
category: workflow-optimization
tags:
- performance
- optimization
- tokens
- context-window
- progressive-loading
- budget
- efficiency
dependencies:
- modular-skills
tools:
- Read
- Bash
usage_patterns:
- token-reduction
- progressive-loading
- context-budgeting
- skill-optimization
complexity: intermediate
estimated_tokens: 450
progressive_loading: true
modules:
  - modules/conditional-loading.md
---

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Token Budget Model](#token-budget-model)
- [Progressive Loading Patterns](#progressive-loading-patterns)
- [Optimization Workflow](#optimization-workflow)
- [Quality Checks](#quality-checks)

## Overview

Plugin ecosystems face a fundamental constraint: the skill description budget (2% of context window, ~16k characters at 200k tokens). Every skill loaded into context reduces the space available for actual work. This skill provides patterns to minimize token footprint while preserving full capability.

### Core Principles

1. **Metadata-first discovery** - Claude scans ~100 tokens of frontmatter to decide relevance before loading full content
2. **Progressive disclosure** - Essential content loads immediately; advanced content lives in modules loaded on-demand
3. **Token budgeting** - Track and enforce per-skill token limits aligned with the ecosystem budget
4. **Context-aware delivery** - Load depth matches task complexity

## Quick Start

```bash
# Estimate tokens for a skill
python plugins/abstract/scripts/validate_budget.py

# Check a single skill's token footprint
Skill(abstract:estimate-tokens) --path plugins/my-plugin/skills/my-skill/SKILL.md

# Audit full ecosystem budget
Skill(abstract:skills-eval) --focus token-efficiency
```

## Token Budget Model

### Budget Allocation (Claude Code v2.1.32+)

| Context Window | Budget (2%) | Per-Skill Target | Max Skills |
|---------------|-------------|-------------------|------------|
| 200k tokens | ~16,000 chars | 300-500 chars | ~40 |
| 1M tokens | ~80,000 chars | 300-500 chars | ~200 |

The `SLASH_COMMAND_TOOL_CHAR_BUDGET` env var overrides the default. The ecosystem validator uses 17,000 to provide growth headroom.

### Per-Skill Targets

| Skill Size | Token Range | Strategy |
|-----------|-------------|----------|
| Minimal | <300 tokens | Single SKILL.md, no modules |
| Standard | 300-800 tokens | SKILL.md + 1-2 modules |
| Large | 800-1500 tokens | Progressive loading required |
| Oversize | >1500 tokens | Split into separate skills |

## Progressive Loading Patterns

### Pattern 1: Module Decomposition

Keep SKILL.md lean with frontmatter + overview + quick start. Move implementation details to `modules/`:

```
my-skill/
  SKILL.md              # ~300 tokens: frontmatter, overview, quick start
  modules/
    implementation.md   # Loaded when Claude needs detailed steps
    examples.md         # Loaded when user asks for examples
    advanced.md         # Loaded for complex scenarios
```

### Pattern 2: Tiered Content

Structure SKILL.md with essential content first, deeper content gated behind clear section boundaries:

```markdown
## Quick Start          <!-- Always loaded, ~100 tokens -->
## Core Workflow        <!-- Loaded for standard use, ~200 tokens -->
## Advanced Patterns    <!-- Loaded on-demand via modules -->
```

### Pattern 3: Conditional Module Loading

Use `progressive_loading: true` in frontmatter. Claude loads the base SKILL.md first, then fetches modules only when the task requires deeper guidance. This achieves 40-60% context reduction for complex skills.

## Optimization Workflow

### Step 1: Measure

```bash
# Get current token estimate
Skill(abstract:estimate-tokens) --path path/to/SKILL.md
```

### Step 2: Identify Reduction Targets

- Move examples and edge cases to modules
- Compress repetitive patterns into tables
- Remove content duplicated from dependencies
- Replace verbose explanations with concise rules

### Step 3: Restructure

- Extract sections >200 tokens into `modules/`
- Ensure SKILL.md frontmatter description stays under 500 characters
- Add `progressive_loading: true` to frontmatter
- List modules in frontmatter `modules:` array

### Step 4: Validate

```bash
# Re-measure and verify reduction
python plugins/abstract/scripts/validate_budget.py
# Target: 50%+ reduction from original
```

## Quality Checks

Before finalizing optimization:

- [ ] SKILL.md frontmatter description is under 500 characters
- [ ] Quick Start section provides enough info for basic use
- [ ] All modules are listed in frontmatter `modules:` array
- [ ] `estimated_tokens` in frontmatter reflects actual measured value
- [ ] `progressive_loading: true` is set when modules exist
- [ ] No functionality lost - advanced content accessible via modules
- [ ] Token reduction target met (50%+ for large skills)

## Resources

- [Modular Skills](../modular-skills/SKILL.md) - Architecture patterns for skill decomposition
- **ADR 0004: Skill Description Budget** - The 2% budget rule scales with context window size (200k → ~16k chars, 1M → ~80k chars). Budget is split across all loaded skills. `SLASH_COMMAND_TOOL_CHAR_BUDGET` env var overrides the default.
- **Context Optimization** (`Skill(conserve:context-optimization)`) - MECW principles: measure context before acting, target 50% utilization, use progressive loading for large skills, prefer native tools over bash equivalents
