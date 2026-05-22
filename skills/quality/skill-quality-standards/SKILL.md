---
name: skill-quality-standards
description: When creating or validating skills. Reference for SKILL-CREATOR and SKILL-VALIDATOR.
version: 1.1.0
tokens: ~420
confidence: high
sources:
  - internal: .claude/skills/REGISTRY.yaml
  - https://www.anthropic.com/news/claude-2-1-prompting (context window optimization)
last_validated: 2025-12-10
next_review: 2025-12-24
tags: [skills, quality, standards, meta]
---

## When to Use
When creating or validating skills. Reference for SKILL-CREATOR and SKILL-VALIDATOR.

## Patterns

### Size Limits
```
Target:  400-1000 tokens (optimal)
Maximum: 1500 tokens (hard limit)
Per task: max 3 skills loaded

Estimation:
  1 word ≈ 1.3 tokens
  1 code line ≈ 10 tokens
  Full skill ≈ 100-150 lines
```

### Confidence Levels
```
HIGH:
  - 2+ authoritative sources (Tier 1-2)
  - Patterns tested in production
  - Official docs cited

MEDIUM:
  - 1 authoritative source
  - Community-validated patterns
  - Reputable tech blog

LOW:
  - Blog posts only
  - Experimental/unverified
  - No official source
```

### Required Sections
```markdown
---
[YAML frontmatter with metadata]
sources:
  - [URL or internal path]
---

## When to Use
[1-2 sentences - clear trigger]

## Patterns
[2-3 patterns with code examples]
[Each with source citation]

## Anti-Patterns
[What NOT to do + why]

## Verification Checklist
[Actionable checks]
```

### Skill Types
```
Generic:    .claude/skills/generic/
            Tech-agnostic, reusable anywhere

Domain:     .claude/skills/domain/
            Industry-specific (fintech, healthcare)

Project:    .claude/skills/project/
            Repo-specific patterns
```

## Anti-Patterns
- Skills over 1500 tokens (split them)
- Patterns without source links in frontmatter
- Vague "When to Use" triggers
- Theory without code examples
- Missing anti-patterns section

## Verification Checklist
- [ ] Under 1500 tokens
- [ ] Every pattern has source in frontmatter
- [ ] "When to Use" is specific
- [ ] 2+ patterns with code
- [ ] Anti-patterns included
- [ ] Checklist is actionable
