---
name: skill-creator
description: Create new Claude Code skills following SOTA compact design patterns (v3.2)
version: 1.0.0
---

# Skill Creator - SOTA Pattern

## Workflow

1. **Gather requirements**: Ask user for skill purpose, trigger conditions, and key workflow steps

2. **Design check**: Ensure skill is justified (not a simple task, needs reusability)

3. **Create structure**: 
   - `~/.claude/skills/[skill-name]/SKILL.md` (compact, <200 words)
   - `~/.claude/skills/[skill-name]/EXAMPLES.md` (optional, loaded only on demand)
   - `~/.claude/skills/[skill-name]/GUIDE.md` (optional, loaded only on demand)

4. **Generate SKILL.md** following SOTA pattern:
   - YAML frontmatter: name, description, version
   - Clear workflow (numbered steps)
   - Try-first approach (don't read configs unnecessarily)
   - Lazy loading (load details only when needed)
   - Key principle statement
   - Optional: "See EXAMPLES.md" or "See GUIDE.md" (but don't auto-load)

5. **Create optional docs** only if skill is complex:
   - EXAMPLES.md: Detailed usage examples
   - GUIDE.md: Advanced patterns, troubleshooting, edge cases

6. **Update skill registry**: Add to `~/.claude/skills/README.md` if exists

## SOTA Design Principles

**Target**: <200 words in SKILL.md
**Pattern**: Try operations first, handle errors gracefully
**Loading**: Lazy load everything (even docs)
**Config**: Don't read unless absolutely necessary
**Separation**: Examples/guides in separate files, loaded only when needed

## Key Principle

**Skills are for recurring workflows, not one-off tasks.** Minimize context by keeping SKILL.md ultra-compact and deferring all details to optional, on-demand files.

---

Optional docs: EXAMPLES.md, GUIDE.md (load manually when needed)
