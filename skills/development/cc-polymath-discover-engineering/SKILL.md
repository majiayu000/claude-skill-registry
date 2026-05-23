---
name: discover-engineering
description: Automatically discover software engineering practice skills when working with engineering practices. Activates for engineering development tasks.
---

# Engineering Skills Discovery

Provides automatic access to comprehensive engineering skills.

## When This Skill Activates

This skill auto-activates when you're working with:
- engineering practices
- code review
- documentation
- team collaboration
- technical leadership

## Available Skills

### Quick Reference

The Engineering category contains 14 skills:

**Software Development Practices:**
1. **code-review** - PR reviews, feedback, automation
2. **code-quality** - SOLID principles, metrics, code smells
3. **refactoring-patterns** - Safe refactoring techniques
4. **test-driven-development** - TDD, red-green-refactor
5. **domain-driven-design** - DDD patterns, bounded contexts
6. **functional-programming** - FP principles, immutability
7. **design-patterns** - GoF patterns, when to use
8. **technical-debt** - Identifying and managing debt
9. **pair-programming** - Pairing techniques, mob programming
10. **continuous-integration** - CI/CD pipelines, deployment

**RFC & Documentation:**
11. **rfc-consensus-building** - Stakeholder collaboration
12. **rfc-decision-documentation** - ADRs, decision tracking
13. **rfc-structure-format** - RFC templates, formatting
14. **rfc-technical-design** - Architecture proposals

### Load Full Category Details

For complete descriptions and workflows:

```bash
cat ~/.claude/skills/engineering/INDEX.md
```

This loads the full Engineering category index with:
- Detailed skill descriptions
- Usage triggers for each skill
- Common workflow combinations
- Cross-references to related skills

### Load Specific Skills

Load individual skills as needed:

```bash
# Software Development Practices
cat ~/.claude/skills/engineering/code-review.md
cat ~/.claude/skills/engineering/code-quality.md
cat ~/.claude/skills/engineering/refactoring-patterns.md
cat ~/.claude/skills/engineering/test-driven-development.md
cat ~/.claude/skills/engineering/domain-driven-design.md
cat ~/.claude/skills/engineering/functional-programming.md
cat ~/.claude/skills/engineering/design-patterns.md
cat ~/.claude/skills/engineering/technical-debt.md
cat ~/.claude/skills/engineering/pair-programming.md
cat ~/.claude/skills/engineering/continuous-integration.md

# RFC & Documentation
cat ~/.claude/skills/engineering/rfc-consensus-building.md
cat ~/.claude/skills/engineering/rfc-decision-documentation.md
cat ~/.claude/skills/engineering/rfc-structure-format.md
cat ~/.claude/skills/engineering/rfc-technical-design.md
```

### Common Workflow Combinations

**Code Quality Workflow:**
```bash
# Load related skills together
cat ~/.claude/skills/engineering/code-review.md
cat ~/.claude/skills/engineering/code-quality.md
cat ~/.claude/skills/engineering/refactoring-patterns.md
```

**TDD Workflow:**
```bash
cat ~/.claude/skills/engineering/test-driven-development.md
cat ~/.claude/skills/engineering/code-quality.md
cat ~/.claude/skills/engineering/continuous-integration.md
```

**Architecture Design Workflow:**
```bash
cat ~/.claude/skills/engineering/domain-driven-design.md
cat ~/.claude/skills/engineering/design-patterns.md
cat ~/.claude/skills/engineering/rfc-technical-design.md
```

## Progressive Loading

This gateway skill enables progressive loading:
- **Level 1**: Gateway loads automatically (you're here now)
- **Level 2**: Load category INDEX.md for full overview
- **Level 3**: Load specific skills as needed

## Usage Instructions

1. **Auto-activation**: This skill loads automatically when Claude Code detects engineering work
2. **Browse skills**: Run `cat ~/.claude/skills/engineering/INDEX.md` for full category overview
3. **Load specific skills**: Use bash commands above to load individual skills

---

**Next Steps**: Run `cat ~/.claude/skills/engineering/INDEX.md` to see full category details.
