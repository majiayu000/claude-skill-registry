---
name: skill-authoring
description: Design and development best practices for Claude Code skills, MCP tools, and AI agent capabilities. Use when creating skills, writing SKILL.md files, designing tool descriptions, or optimizing triggers. Triggers on "create a skill", "skill template", "write skill instructions", SKILL.md, metadata.json, progressive disclosure, trigger optimization, MCP tool design, or skill testing. Does NOT cover specific frameworks or languages (use dedicated skills).
---

# AI Agent Skills Best Practices

Design and development guide for AI agent skills, including Claude Code skills and MCP tools. Contains 46 rules across 8 categories, prioritized by impact to guide skill creation, review, and optimization.

## When to Apply

- Creating new Claude Code skills or MCP tools
- Writing or reviewing SKILL.md metadata and descriptions
- Optimizing skill trigger reliability
- Structuring content for progressive disclosure
- Testing skill activation and behavior
- Designing tool interfaces for agent workflows

## Core Principles

**1. Descriptions drive activation.** Claude selects skills based on description matching against user intent. Include specific capabilities, trigger keywords, and negative cases. A skill with a vague description activates inconsistently or never.

**2. Front-load critical instructions.** Claude may truncate long content. Place non-negotiable rules in the first 100 lines. Bury important constraints at the end and they get ignored.

**3. Progressive disclosure saves tokens.** Load detailed content only when needed. A 2000-line skill wastes context on every activation. Structure as: SKILL.md (overview) → references/ (details) → scripts/ (execution).

**4. Test activation, not just execution.** A skill that works perfectly but never triggers provides zero value. Test with real user phrases, synonyms, and edge cases before deployment.

**5. One skill per domain.** Overlapping skills create activation conflicts. Split by clear boundaries (language, framework, workflow stage) with distinct trigger keywords.

## Rule Categories

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Skill Metadata Design | CRITICAL | `meta-` |
| 2 | Description Engineering | CRITICAL | `desc-` |
| 3 | Content Structure | HIGH | `struct-` |
| 4 | Trigger Optimization | HIGH | `trigger-` |
| 5 | Progressive Disclosure | MEDIUM-HIGH | `prog-` |
| 6 | MCP Tool Design | MEDIUM | `mcp-` |
| 7 | Testing and Validation | MEDIUM | `test-` |
| 8 | Maintenance and Distribution | LOW-MEDIUM | `maint-` |

## Quick Reference

### 1. Skill Metadata Design (CRITICAL)

- `meta-name-format` - Use lowercase hyphenated skill names
- `meta-name-hyphen-boundaries` - Never start or end names with hyphens
- `meta-name-no-consecutive-hyphens` - Avoid consecutive hyphens in names
- `meta-name-uniqueness` - Ensure skill names are globally unique
- `meta-required-frontmatter` - Include all required frontmatter fields
- `meta-allowed-frontmatter-fields` - Use only allowed frontmatter fields
- `meta-frontmatter-yaml-syntax` - Use valid YAML frontmatter syntax
- `meta-name-length` - Keep skill names under 64 characters
- `meta-directory-match` - Match skill name to directory name

### 2. Description Engineering (CRITICAL)

- `desc-specific-capabilities` - Name specific capabilities in description
- `desc-trigger-keywords` - Include user trigger keywords in description
- `desc-third-person-voice` - Write descriptions in third person
- `desc-length-optimization` - Optimize description length for discovery
- `desc-avoid-vague-terms` - Avoid vague terms in descriptions
- `desc-differentiate-similar-skills` - Differentiate similar skills with distinct triggers
- `desc-include-negative-cases` - Include negative cases for precision

### 3. Content Structure (HIGH)

- `struct-header-hierarchy` - Use consistent header hierarchy
- `struct-instructions-first` - Put critical instructions early in content
- `struct-imperative-instructions` - Write instructions in imperative mood
- `struct-code-blocks-with-language` - Specify language in code blocks
- `struct-line-limit` - Keep SKILL.md under 500 lines
- `struct-single-responsibility` - One skill per domain

### 4. Trigger Optimization (HIGH)

- `trigger-slash-command-aliases` - Include slash command aliases in description
- `trigger-file-type-patterns` - Include file type patterns in description
- `trigger-workflow-stages` - Reference workflow stages in description
- `trigger-error-patterns` - Include error patterns in debugging skills
- `trigger-synonym-coverage` - Cover synonyms and alternate phrasings

### 5. Progressive Disclosure (MEDIUM-HIGH)

- `prog-three-level-disclosure` - Implement three-level progressive disclosure
- `prog-one-level-deep-links` - Limit reference links to one level deep
- `prog-scripts-execute-not-read` - Execute scripts instead of reading code
- `prog-lazy-load-examples` - Lazy load examples and reference material
- `prog-mutual-exclusion` - Separate mutually exclusive contexts

### 6. MCP Tool Design (MEDIUM)

- `mcp-tool-naming` - Use clear action-object tool names
- `mcp-parameter-descriptions` - Document all tool parameters
- `mcp-error-messages` - Return actionable error messages
- `mcp-tool-scope` - Design single-purpose tools
- `mcp-allowed-tools` - Use allowed-tools for safety constraints
- `mcp-idempotent-operations` - Design idempotent tool operations

### 7. Testing and Validation (MEDIUM)

- `test-trigger-phrases` - Test skill activation with real user phrases
- `test-edge-cases` - Test skills with edge case inputs
- `test-negative-scenarios` - Test that skills do NOT trigger on unrelated requests
- `test-instruction-clarity` - Test instructions with fresh context

### 8. Maintenance and Distribution (LOW-MEDIUM)

- `maint-semantic-versioning` - Use semantic versioning for skill releases
- `maint-changelog` - Maintain a changelog for skill updates
- `maint-plugin-packaging` - Package skills as plugins for distribution
- `maint-audit-security` - Audit skills before installing from external sources

## Creating Rules

Copy [assets/templates/_template.md](assets/templates/_template.md) and follow the frontmatter schema:

```yaml
---
title: Rule Title Here
impact: CRITICAL|HIGH|MEDIUM-HIGH|MEDIUM|LOW-MEDIUM|LOW
impactDescription: Quantified impact (e.g., "2-10x improvement")
tags: prefix, technique, related-concepts
---
```

Reference files use the pattern: `references/{prefix}-{slug}.md`

## References

- [skills-ref specification](https://github.com/agentskills/agentskills/tree/main/skills-ref)
- [Anthropic Engineering: Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [MCP Best Practices](https://modelcontextprotocol.info/docs/best-practices/)
- [Prompt Engineering Guide: LLM Agents](https://www.promptingguide.ai/research/llm-agents)
- [Claude Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
