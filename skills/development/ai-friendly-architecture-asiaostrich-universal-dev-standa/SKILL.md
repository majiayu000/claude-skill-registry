---
scope: uds-specific
description: |
  Design AI-friendly architecture with explicit patterns, layered documentation, and semantic boundaries.
  Use when: structuring projects for AI collaboration, optimizing codebase for AI analysis, setting up AI context.
  Keywords: architecture, AI-friendly, context, modules, documentation layers, .ai-context.yaml, 架構, AI 友善, 上下文.
---

# AI-Friendly Architecture Guide

> **Language**: English | [繁體中文](../../locales/zh-TW/skills/ai-friendly-architecture/SKILL.md)

**Version**: 1.0.0
**Last Updated**: 2026-01-25
**Applicability**: Claude Code Skills

---

> **Core Standard**: This skill implements [AI-Friendly Architecture](../../core/ai-friendly-architecture.md). For comprehensive methodology documentation, refer to the core standard.

## Purpose

This skill helps design project architecture that maximizes AI collaboration effectiveness through explicit patterns, layered documentation, and semantic boundaries.

## Quick Reference

### Core Principles

| Principle | Description | Benefit |
|-----------|-------------|---------|
| **Explicit Over Implicit** | Document behavior explicitly | AI understands without guessing |
| **Layered Context** | Multi-level documentation | Appropriate detail per task |
| **Semantic Boundaries** | Clear module boundaries | Independent analysis |
| **Discoverable Structure** | Self-documenting structure | Quick orientation |

### Context Layers

| Layer | Token Budget | Content |
|-------|--------------|---------|
| **L1: Quick Ref** | < 500 | One-liners, API signatures, entry points |
| **L2: Detailed** | < 5,000 | Full API docs, usage examples |
| **L3: Examples** | Unlimited | Complete implementations, edge cases |

### Recommended Structure

```
project/
├── .ai-context.yaml          # AI context configuration
├── docs/
│   ├── QUICK-REF.md          # Level 1 documentation
│   └── ARCHITECTURE.md       # Level 2 documentation
├── src/
│   └── auth/
│       ├── index.ts          # Entry point with module header
│       ├── QUICK-REF.md      # Module quick reference
│       └── README.md         # Module documentation
└── CLAUDE.md                 # AI instruction file
```

## Module Header Template

```javascript
/**
 * ═══════════════════════════════════════════════════════════
 * MODULE: [Module Name]
 * ═══════════════════════════════════════════════════════════
 *
 * PURPOSE: [One-sentence description]
 *
 * DEPENDENCIES:
 *   - [dep1]: [reason]
 *   - [dep2]: [reason]
 *
 * EXPORTS:
 *   - [function1](params): [description]
 *   - [function2](params): [description]
 *
 * CONFIGURATION:
 *   - [CONFIG_VAR]: [description]
 *
 * ═══════════════════════════════════════════════════════════
 */
```

## Detailed Guidelines

For complete standards, see:
- [AI-Friendly Architecture Standards](../../core/ai-friendly-architecture.md)

### AI-Optimized Format (Token-Efficient)

For AI assistants, use the YAML format file for reduced token usage:
- Base standard: `ai/standards/ai-friendly-architecture.ai.yaml`

## .ai-context.yaml Configuration

```yaml
# .ai-context.yaml - AI Context Configuration
version: 1.0.0

project:
  name: my-project
  type: web-app  # web-app | library | cli | api | monorepo
  primary-language: typescript

modules:
  - name: auth
    path: src/auth/
    entry: index.ts
    description: Authentication and authorization
    dependencies: [database, crypto]
    priority: high

  - name: api
    path: src/api/
    entry: routes.ts
    description: REST API endpoints
    dependencies: [auth, database]
    priority: high

analysis-hints:
  entry-points:
    - src/main.ts
    - src/index.ts
  ignore-patterns:
    - node_modules
    - dist
    - "*.test.ts"
  architecture-type: layered

documentation:
  quick-ref: docs/QUICK-REF.md
  detailed: docs/ARCHITECTURE.md
  examples: docs/examples/
```

## Context Priority Guidelines

| Priority | Content Type | Reason |
|----------|--------------|--------|
| 1 | Entry points | Application structure |
| 2 | .ai-context.yaml | Module map and dependencies |
| 3 | QUICK-REF files | Rapid API understanding |
| 4 | Modified files | Direct task relevance |
| 5 | Dependency chain | Context for changes |

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Magic strings** | AI can't trace constants | Typed constants with docs |
| **Implicit routing** | Hidden behavior | Explicit route mappings |
| **Global state** | Unpredictable deps | Dependency injection |
| **Circular deps** | Context confusion | Hierarchical dependencies |
| **Monolithic files** | Context overflow | Focused modules |

## Implementation Checklist

### Quick Start (< 1 hour)

- [ ] Create `.ai-context.yaml` with module list
- [ ] Add `QUICK-REF.md` to project root
- [ ] Document entry points in README
- [ ] Add module headers to main files

### Standard Implementation (< 1 day)

- [ ] Complete `.ai-context.yaml` configuration
- [ ] Add `QUICK-REF.md` to each major module
- [ ] Document all public APIs with type info
- [ ] Add section dividers to large files

---

## Configuration Detection

This skill supports project-specific configuration.

### Detection Order

1. Check for existing `.ai-context.yaml`
2. Check for `QUICK-REF.md` files
3. If not found, **suggest creating AI-friendly structure**

### First-Time Setup

If no configuration found:

1. Suggest: "This project hasn't been configured for AI collaboration. Would you like to set up an AI-friendly structure?"
2. Create `.ai-context.yaml` template
3. Create `QUICK-REF.md` in project root

---

## Related Standards

- [AI-Friendly Architecture](../../core/ai-friendly-architecture.md) - Core architecture standard
- [Project Structure](../../core/project-structure.md) - Directory organization
- [Documentation Structure](../../core/documentation-structure.md) - Documentation layering
- [Anti-Hallucination](../../core/anti-hallucination.md) - AI accuracy standards

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-25 | Initial release |

---

## License

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**Source**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
