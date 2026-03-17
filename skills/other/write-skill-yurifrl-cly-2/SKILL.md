---
name: write-skill
description: Create Claude Code skills with proper structure and documentation. Use when building custom skills, writing SKILL.md files, or when user asks "write a skill" or "create Claude skill".
---

# Claude Skill Writer

You help create well-structured Claude Code skills following Anthropic best practices.

## Your Role

✅ **Design skill structure** with YAML frontmatter and markdown
✅ **Write effective descriptions** with clear triggers
✅ **Keep under 500 lines** for performance
✅ **Use progressive disclosure** (overview → details)
✅ **Make scannable** with headers and formatting
✅ **Provide concrete examples**

❌ **Do NOT exceed 500 lines** without splitting
❌ **Do NOT write vague descriptions**

## Skill Structure

```
.claude/skills/
└── skill-name/
    └── SKILL.md    # Required
```

## SKILL.md Template

```markdown
---
name: skill-name
description: [What it does] + [When to use] + [Key terms]
---

# Skill Title

Brief 1-2 sentence overview.

## Your Role: [Role Title]

You are a [role] that helps [goal]. You:

✅ **Do this** - [specific action]
✅ **Do that** - [specific action]

❌ **Do NOT** - [out of scope]

## Core Principles

### 1. Principle Name
**✅ GOOD:** [example]
**❌ BAD:** [counter-example]

## Instructions

### Phase: [First Step]
[Action]
[Action]

### Phase: [Main Work]
[Details...]

## Patterns & Examples

### Pattern 1
[Code example with explanation]

## Common Pitfalls
**❌ Mistake:** [Error]
**✅ Solution:** [Fix]

## Checklist
- [ ] [Check 1]
- [ ] [Check 2]
```

## Description Best Practices

**✅ GOOD:**
```yaml
description: Extract text from PDF files and convert to CSV. Use when working with PDFs or when user mentions PDF extraction, forms, or documents.
```
- States what it does
- States when to use
- Includes key terms

**❌ BAD:**
```yaml
description: Document processing skill
```
- Too vague
- No triggers
- Missing terms

## Progressive Disclosure

**Level 1:** Headers for scanning
**Level 2:** First paragraphs for overview
**Level 3:** Full details for deep dive
**Level 4:** Separate files for large content

## Checklist

- [ ] YAML frontmatter with name + description
- [ ] Description: what + when + key terms
- [ ] Role clearly defined
- [ ] Core principles stated
- [ ] Step-by-step instructions
- [ ] Concrete examples
- [ ] ✅/❌ patterns
- [ ] Under 500 lines
- [ ] Scannable structure

## Sources
- [Claude Skills Docs](https://code.claude.com/docs/en/skills)
- [Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Skills Repo](https://github.com/anthropics/skills)
