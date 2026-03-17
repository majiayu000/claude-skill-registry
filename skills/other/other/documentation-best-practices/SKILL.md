---
name: documentation-best-practices
description: Claude Code documentation standards for CLAUDE.md, commands, skills, agents. Use when creating or reviewing documentation files.
---

# SKILL: Documentation Best Practices

> **Purpose**: Apply Claude Code documentation standards based on Superpowers reference
> **Target**: Anyone creating CLAUDE.md, commands, skills, guides, or agents

---

## Quick Start

### When to Use This Skill
- Creating new documentation (CLAUDE.md, command, skill, agent)
- Reviewing existing documentation for quality
- Restructuring documentation to follow best practices

### Quick Reference

| File Type | Target | Max | Action When Exceeded |
|-----------|--------|-----|----------------------|
| **SKILL.md** | 150 | **200** (official: 500) | >300 → Create REFERENCE.md |
| **Agent** | 250 | **300** | >450 → Simplify required |
| **Command** | 150 | **200** | >300 → Extract to guide |
| **CONTEXT.md** | 150 | **200** | >300 → Simplify required |
| **REFERENCE.md** | 250 | 300 | Split into multiple files |

**Note**: Claude Code officially recommends ≤500 lines for SKILL.md. This project uses a stricter 200-line internal standard for token optimization and context efficiency.

## What This Skill Covers

### In Scope
- File size targets based on Superpowers standards
- Frontmatter standards for auto-discovery
- SKILL.md/REFERENCE.md separation pattern
- Agent model allocation

### Out of Scope
- Test writing → @.claude/skills/tdd/SKILL.md
- Code quality → @.claude/skills/vibe-coding/SKILL.md
- Git workflow → @.claude/skills/git-master/SKILL.md

## Core Concepts

### Superpowers Standard

> "The context window is a public good. Skills share the context window with everything else Claude needs."

**Baseline**: SKILL.md <600 words (~150-200 lines)

### Frontmatter Standards

**Skills** (required):
```yaml
---
name: {skill-name}
description: {trigger-rich description for semantic matching}
---
```

**Commands** (auto-discovery):
```yaml
---
description: {action-rich description for slash command discovery}
---
```

**Agents** (required):
```yaml
---
name: {agent-name}
description: {clear purpose statement}
model: {haiku|sonnet|opus}
tools: [tool list]
skills: [skill list]
---
```

### SKILL.md/REFERENCE.md Pattern

**SKILL.md** (≤200 lines):
- Quick Start (when to use, quick reference)
- Core Concepts (essential patterns)
- Further Reading (link to REFERENCE.md)

**REFERENCE.md** (≤300 lines):
- Detailed examples
- Good/bad patterns
- Troubleshooting
- External references

### Agent Model Allocation

| Model | Agents | Purpose |
|-------|--------|---------|
| **Haiku** | explorer, researcher, validator, documenter | Fast, cost-efficient |
| **Sonnet** | coder, tester, plan-reviewer | Balanced quality/speed |
| **Opus** | code-reviewer | Deep reasoning |

### 3-Tier Documentation

- **Tier 1**: `CLAUDE.md` - Project standards (400+ lines)
- **Tier 2**: `{folder}/CONTEXT.md` - Component architecture (≤200 lines)
- **Tier 3**: `{feature}/CONTEXT.md` - Feature implementation (≤200 lines)

## Documentation Quality Checklist

### Structure
- [ ] Clear purpose statement
- [ ] Quick reference table
- [ ] Standard sections
- [ ] Cross-references

### Discoverability
- [ ] Frontmatter complete
- [ ] Description is trigger-rich
- [ ] CONTEXT.md for navigation

### Maintainability
- [ ] Within size limits
- [ ] No duplicated content
- [ ] Examples provided

---

## Common Mistakes Checklist

### Metadata Errors
- [ ] **Outdated line counts**: CONTEXT.md line values don't match actual files
- [ ] **Stale skill counts**: README.md lists wrong number of skills (use `ls .claude/skills | wc -l`)
- [ ] **Version number drift**: CLAUDE.md version differs from package.json or other sources
- [ ] **Missing frontmatter**: SKILL.md or Agent files lack required name/description fields

### Cross-Reference Errors
- [ ] **Broken links**: `@.claude/path/to/file.md` points to non-existent file
- [ ] **Relative paths**: Using `../skills/` instead of `@.claude/skills/`
- [ ] **Deleted file references**: Documentation still mentions removed systems (e.g., Sisyphus after removal)
- [ ] **Wrong file extensions**: Linking to `.ts` instead of `.md` for documentation

### Content Errors
- [ ] **Duplicate content**: Same info appears in CLAUDE.md and CONTEXT.md
- [ ] **Wrong tier**: Implementation details in CLAUDE.md instead of docs/ai-context/
- [ ] **Missing examples**: Abstract concepts without concrete usage examples
- [ ] **Over-sized files**: SKILL.md >200 lines without split to REFERENCE.md

### Recovery Actions
- **Before commit**: Invoke docs-verify skill
- **On verification failure**: Check error message, locate file, apply fix, re-verify
- **For line count violations**: Extract content to REFERENCE.md or docs/ai-context/
- **For broken links**: Verify file exists with `test -f {path}`, use absolute paths

## Further Reading

**Internal**: @.claude/skills/documentation-best-practices/REFERENCE.md - Detailed examples, good/bad patterns, external links | @.claude/skills/coding-standards/SKILL.md - Official directory structure | @.claude/skills/three-tier-docs/SKILL.md - Complete 3-Tier system

**External**: [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills) | [Claude Code Memory Documentation](https://code.claude.com/docs/en/memory) | [Claude Code Best Practices - Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices) | [Superpowers - obra/superpowers](https://github.com/obra/superpowers)
