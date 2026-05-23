---
scope: universal
description: |
  Prevent AI hallucination and ensure evidence-based responses when analyzing code or making suggestions.
  Use when: analyzing code, making recommendations, providing options, or when user asks about confidence/certainty.
  Keywords: certainty, assumption, inference, evidence, source, 確定性, 推測, 假設, 來源, 證據.
---

# AI Collaboration Standards

> **Language**: English | [繁體中文](../../locales/zh-TW/skills/ai-collaboration-standards/SKILL.md)

**Version**: 1.1.0
**Last Updated**: 2026-01-25
**Applicability**: Claude Code Skills

---

## Purpose

This skill ensures AI assistants provide accurate, evidence-based responses without hallucination.

## Quick Reference

### Unified Tag System

This skill uses two complementary tag categories:

**Category 1: Certainty Tags** (for analyzing existing content)

| Tag | Use When |
|-----|----------|
| `[Confirmed]` | Direct evidence from code/docs |
| `[Inferred]` | Logical deduction from evidence |
| `[Assumption]` | Based on common patterns (needs verification) |
| `[Unknown]` | Information not available |
| `[Need Confirmation]` | Requires user clarification |

**Category 2: Derivation Tags** (for generating new content)

| Tag | Use When |
|-----|----------|
| `[Source]` | Direct content from spec/requirement |
| `[Derived]` | Transformed from source content |
| `[Generated]` | AI-generated structure |
| `[TODO]` | Requires human implementation |

**When to Use Which**:

| Workflow | Primary Tags |
|----------|--------------|
| Code analysis | Certainty Tags |
| Reverse engineering | Certainty Tags |
| Forward derivation | Derivation Tags |
| Spec generation | Derivation Tags |

### Source Types

| Source Type | Tag | Reliability |
|-------------|-----|-------------|
| Project Code | `[Source: Code]` | ⭐⭐⭐⭐⭐ Highest |
| Project Docs | `[Source: Docs]` | ⭐⭐⭐⭐ High |
| External Docs | `[Source: External]` | ⭐⭐⭐⭐ High |
| Web Search | `[Source: Search]` | ⭐⭐⭐ Medium |
| AI Knowledge | `[Source: Knowledge]` | ⭐⭐ Low |
| User Provided | `[Source: User]` | ⭐⭐⭐ Medium |

### Core Rules

1. **Evidence-Based Only**: Only analyze content that has been explicitly read
2. **Cite Sources**: Include file path and line number for code references
3. **Classify Certainty**: Tag all statements with certainty level
4. **Always Recommend**: When presenting options, include a recommended choice with reasoning

## Detailed Guidelines

For complete standards, see:
- [Anti-Hallucination Guidelines](./anti-hallucination.md)
- [Certainty Labels Reference](./certainty-labels.md)

## Examples

### ✅ Correct Response

```
[Confirmed] src/auth/service.ts:45 - JWT validation uses 'jsonwebtoken' library
[Inferred] Based on repository pattern in src/repositories/, likely using dependency injection
[Need Confirmation] Should the new feature support multi-tenancy?
```

### ❌ Incorrect Response

```
The system uses Redis for caching (code not reviewed)
The UserService should have an authenticate() method (API not verified)
```

### ✅ Correct Option Presentation

```
There are three options:
1. Redis caching
2. In-memory caching
3. File-based caching

**Recommended: Option 1 (Redis)**: Given the project already has Redis infrastructure
and needs cross-instance cache sharing, Redis is the most suitable choice.
```

### ❌ Incorrect Option Presentation

```
There are three options:
1. Redis caching
2. In-memory caching
3. File-based caching

Please choose one.
```

## Checklist

Before making any statement:

- [ ] Source Verified - Have I read the actual file/document?
- [ ] Source Type Tagged - Did I specify `[Source: Code]`, `[Source: External]`, etc.?
- [ ] Reference Cited - Did I include file path and line number?
- [ ] Certainty Classified - Did I tag as `[Confirmed]`, `[Inferred]`, etc.?
- [ ] No Fabrication - Did I avoid inventing APIs, configs, or requirements?
- [ ] Recommendation Included - When presenting options, did I include a recommended choice?

---

## Configuration Detection

This skill supports project-specific language configuration for certainty tags.

### Detection Order

1. Check `CONTRIBUTING.md` for "Certainty Tag Language" section
2. If found, use the specified language (English / 中文)
3. If not found, **default to English** tags

### First-Time Setup

If no configuration found and context is unclear:

1. Ask the user: "This project hasn't configured certainty tag language preference. Which would you like to use? (English / 中文)"
2. After user selection, suggest documenting in `CONTRIBUTING.md`:

```markdown
## Certainty Tag Language

This project uses **[English / 中文]** certainty tags.
<!-- Options: English | 中文 -->
```

### Configuration Example

In project's `CONTRIBUTING.md`:

```markdown
## Certainty Tag Language

This project uses **English** certainty tags.

### Tag Reference
- [Confirmed] - Direct evidence from code/docs
- [Inferred] - Logical deduction from evidence
- [Assumption] - Based on common patterns
- [Unknown] - Information not available
- [Need Confirmation] - Requires user clarification
```

---

## Related Standards

- [Anti-Hallucination Standards](../core/anti-hallucination.md)
- [Code Review Checklist](../core/code-review-checklist.md)
- [Testing Standards](../core/testing-standards.md)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-01-25 | Added: Unified Tag System with Certainty and Derivation tag categories |
| 1.0.0 | 2025-12-24 | Added: Standard sections (Purpose, Related Standards, Version History, License) |

---

## License

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**Source**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
