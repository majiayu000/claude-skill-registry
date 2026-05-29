---
name: output-style-authoring
description: Guide for authoring output-styles that transform Claude's behavior and personality. Use when creating, writing, designing, building, reviewing, or improving output-styles, persona modes, or behavior modifications. Helps with style files, keep-coding-instructions decisions, persona design, and choosing between output-styles, agents, and skills. Expert in style best practices.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
# model: inherit
---

## Reference Files

**Start here:**

- [minimal-template.md](minimal-template.md) - 40-line baseline template (start simple!)
- [persona-strength-spectrum.md](persona-strength-spectrum.md) - Passive/Active/Dominant modes

**Deep dives:**

- [design-principles.md](design-principles.md) - Core authoring principles
- [design-patterns.md](design-patterns.md) - Pattern catalog with templates
- [complete-examples.md](complete-examples.md) - Production-ready examples
- [anti-patterns.md](anti-patterns.md) - Warning signs and smells

---

# Output-Style Authoring

Guide for creating output-styles that transform Claude's behavior and personality.

## Related Skills

This skill is part of the authoring skill family:

- **author-agent** - Guide for creating agents
- **author-skill** - Guide for creating skills
- **author-command** - Guide for creating commands
- **author-output-style** - Guide for creating output styles (this skill)

For validation, use the corresponding audit skills:

- **audit-output-style** - Validate output-style configurations
- **audit-coordinator** - Comprehensive multi-faceted audits

## Quick Start

**New to output-styles?** Start with [minimal-template.md](minimal-template.md)—a 40-line baseline.

## What Are Output-Styles?

System prompts that transform Claude into specialized personas. They modify behavior, personality, and approach for an entire session while keeping all tools available.

**Use when:**

- Transforming into different roles (writer, analyst, teacher)
- Changing response style for entire session
- Non-engineering use cases need different behavior
- Want persistent personality change

**Don't use when:** Need tool restrictions or separate context (use Agent or Skill instead)

## Core Principles

**See [design-principles.md](design-principles.md) for deep dive.**

1. **Transform WHO, not HOW** - Define persona and approach, not rigid processes
2. **Start at 40-60 lines** - Add complexity only when proven necessary
3. **Choose strength wisely** - Most should be Active, not Passive or Dominant (see [persona-strength-spectrum.md](persona-strength-spectrum.md))

## File Structure

**Required:**

- YAML frontmatter with `name` and `description`
- Clear persona definition
- Concrete behavioral directives

**Optional:**

- `keep-coding-instructions: true/false` (default: false)
- Output format specification
- Boundaries (what you don't do)

**Location:**

- User: `~/.claude/output-styles/style-name.md` (just you)
- Project: `.claude/output-styles/style-name.md` (whole team)

**Patterns:** See [design-patterns.md](design-patterns.md) for Role Transformation, Teaching Mode, Specialized Professional, and Quality/Audit templates.

## Creation Process

**Prefer starting with [minimal-template.md](minimal-template.md) and customizing.**

### Step 1: Define Role

- What persona should Claude adopt?
- Is this engineering-related? (determines `keep-coding-instructions`)
- Does similar style exist? (`/output-style` to list)
- Use AskUserQuestion if unclear

### Step 2: Choose Scope

- User (`~/.claude/output-styles/`): Just you, all projects
- Project (`.claude/output-styles/`): Whole team, in git

### Step 3: Decide Coding Instructions

- `keep-coding-instructions: false` - Non-engineering roles (writer, teacher, analyst)
- `keep-coding-instructions: true` - Engineering roles (security, DevOps, QA)
- **Default:** false

### Step 4: Write Persona

**Good:** "You are a technical writer focused on clarity and accessibility."
**Bad:** "You help write documentation." (too vague)

Include WHO Claude is, primary goal, and key differentiators.

### Step 5: Define Behaviors

**Use concrete directives, not adjectives.**

**Good:** "1. Start with why it matters 2. Use examples within 3 paragraphs 3. Define terms on first use"
**Bad:** "Be helpful and explanatory" (doesn't change behavior)

See [anti-patterns.md](anti-patterns.md) #7 for more on this.

### Step 6: Write Description

200-400 chars, explains what + when to use

**Good:** "Clear, beginner-friendly documentation with examples"
**Bad:** "Helps with writing" (too vague)

### Step 7: Create File

- Filename: `style-name.md` (lowercase-with-hyphens)
- Location: `~/.claude/output-styles/` or `.claude/output-styles/`
- Use [minimal-template.md](minimal-template.md) as starting point

### Step 8: Test

Activate with `/output-style style-name` and verify:

1. Appears in menu
2. Behavior changes noticeably
3. Adds value to session
4. Test mid-session deactivation (shouldn't break conversation)

## When to Use What

**See [when-to-use-what.md](../../references/when-to-use-what.md) for complete guide.**

**Quick:**

- **Output-Style:** Transform behavior for entire session (writer, analyst, teacher)
- **Agent:** Separate context with tool restrictions
- **Skill:** Conditional knowledge, auto-triggers

## Critical Warnings

**See [anti-patterns.md](anti-patterns.md) for full diagnostic checklist.**

**Common smells:**

1. **Persona vs process blur** - Specifying HOW to execute, not WHO Claude is
2. **Over 100 lines** - Likely over-built; audit each section
3. **Reads like user checklist** - Instructions for user, not Claude's behavior
4. **Mid-session removal breaks conversation** - Too invasive
5. **Trying to restrict tools** - Can't enforce; use Agent/Skill instead

**Quick tests:**

- Can you describe persona in one sentence?
- Would mid-session deactivation break conversation?
- Is this WHO or HOW? (should be WHO)

## Examples & Resources

- [minimal-template.md](minimal-template.md) - Start here (40-line baseline)
- [complete-examples.md](complete-examples.md) - Production examples
- [persona-strength-spectrum.md](persona-strength-spectrum.md) - Passive/Active/Dominant modes
- [anti-patterns.md](anti-patterns.md) - Warning signs and recovery

## Quick Checklist

- [ ] Clear role/persona
- [ ] User or project scope
- [ ] `keep-coding-instructions` decision
- [ ] Concrete behaviors (not adjectives)
- [ ] 40-80 lines (justify if longer)
- [ ] Test activation and deactivation
- [ ] Refine based on usage
