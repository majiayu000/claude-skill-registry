---
name: using-superpowers
description: MANDATORY skill for all agents. Establishes how to discover, load, and use skills from SKILL-INDEX.md. Also detects when user is teaching new rules.
triggers: skill, skills, use skill, check skills, best practice, pattern
---

# Using Superpowers (Skills System)

> This skill teaches agents HOW to use the skills system. It's meta.

## CRITICAL RULE

<MANDATORY>
If there is even a 1% chance a skill might apply to what you are doing, you MUST check the index and load it.

This is NOT optional. This is NOT negotiable. You cannot rationalize your way out of this.
</MANDATORY>

---

## Part 1: Using Existing Skills

### The Flow

```
User Request → Scan SKILL-INDEX.md → Match Skills → Load Relevant → Announce → Apply
```

### Step-by-Step

1. **Receive user request**
2. **Scan** `skills/SKILL-INDEX.md` (lightweight, categorized)
3. **Identify** skills that might apply (by name, category, triggers)
4. **Load** the specific skill: `skills/{skill-name}/SKILL.md`
5. **Announce**: "Using [skill-name] for [purpose]"
6. **Apply** the skill's rules and patterns
7. **Respond** to user with skill-informed answer

### Red Flags (You're Rationalizing)

| Your Thought | The Reality |
|--------------|-------------|
| "This is just a simple question" | Simple questions have best practices too |
| "I already know this" | Skills evolve. Read the current version. |
| "Let me explore the code first" | Skills tell you HOW to explore |
| "This doesn't need a formal skill" | If a skill exists, use it |
| "The skill is overkill" | Discipline prevents mistakes |
| "I'll just do this one thing first" | Check skills BEFORE doing anything |
| "I know what the user means" | Skills provide the HOW, not just WHAT |

### Skill Priority

When multiple skills could apply:

1. **Process skills first** → debugging, planning, tdd, verification
2. **Domain skills second** → react, python, nextjs, stripe
3. **Integration skills third** → firebase, supabase, clerk

Example:
- "Fix this bug" → `systematic-debugging` first, then domain skills
- "Add Stripe" → `stripe-integration` + framework skill

### Token Economy

- Index scan: ~500 tokens (ALWAYS acceptable)
- Full skill load: 1000-5000 tokens each
- Rule: Load max 2-3 skills per task
- Summarize skill content, don't quote entire files

---

## Part 2: Detecting User Teaching

### The User is Teaching When...

| Signal | Example | Action |
|--------|---------|--------|
| Explicit rule | "siempre usa X", "regla:", "nunca hagas Y" | Confirm & create |
| Correction | "no, hacelo asi..." + shows pattern | Ask if should persist |
| Preference | "prefiero X sobre Y porque..." | Note for skill |
| Repeated pattern | Same correction 3+ times | Propose skill creation |
| Best practice | "buena practica:", "el estandar es..." | Confirm & create |
| Style guide | "en este proyecto usamos..." | Add to project skill |
| Framework rule | "en React siempre...", "en Python nunca..." | Add to language skill |

### Detection Protocol

1. **Recognize** the teaching moment
   - User is explaining HOW, not just WHAT
   - User is correcting your output with a pattern
   - User says "siempre", "nunca", "regla", "preferencia"

2. **Confirm intent**
   - "¿Queres que guarde esto como skill/rule?"
   - "¿Es una preferencia tuya o un estandar del proyecto?"

3. **Clarify scope**
   - "¿Para que lenguaje/framework?" (python, react, general)
   - "¿Skill existente o nuevo?"
   - "¿Solo este proyecto o global?"

4. **Preview** the rule before creating

5. **Create** in `skills/{skill-name}/rules/_custom-{name}.md`

6. **Rebuild** index: `bun run skills/_scripts/generate-index.ts`

### Rule File Format

```markdown
---
title: Rule Title
impact: HIGH | MEDIUM | LOW
tags: tag1, tag2
source: user-taught
date: YYYY-MM-DD
---

## Rule Title

[Why this matters - one sentence]

**Do:**
```code
// correct pattern
```

**Don't:**
```code
// incorrect pattern
```

[Optional: Reference or context]
```

### Scope Resolution

| User Says | Skill Location |
|-----------|----------------|
| "en Python siempre..." | `skills/python/rules/_custom-{name}.md` |
| "en React..." | `skills/react/rules/_custom-{name}.md` |
| "en este proyecto..." | `skills/general/rules/_custom-{name}.md` |
| "siempre que uses X..." | `skills/{x}/rules/_custom-{name}.md` |
| New domain entirely | Create new `skills/{name}/` folder |

---

## Part 3: Maintenance Commands

```bash
# After adding/modifying skills
bun run skills/_scripts/generate-index.ts

# To sync external sources (anthropics, vercel-labs)
bun run skills/_scripts/sync-external.ts

# To rebuild SKILL.md from rules/ folder
bun run skills/_scripts/build.ts
```

---

## Quick Reference

### Skill Categories (from SKILL-INDEX.md)

| Category | Examples | When to Use |
|----------|----------|-------------|
| AI Agents & LLM | langgraph, crewai, rag-engineer | Building AI features |
| Development | react-patterns, nextjs, python | Coding specific stacks |
| Testing & QA | playwright, tdd-workflow | Testing strategies |
| Cybersecurity | pentest-*, ethical-hacking | Security audits |
| Integrations | stripe, firebase, supabase | Third-party APIs |
| Marketing | seo-*, cro-*, copywriting | Growth features |
| Infrastructure | docker, aws-*, git-* | DevOps tasks |
| Workflow | writing-plans, executing-plans | Process management |

### Skill Types

**Rigid** (TDD, debugging, verification): Follow EXACTLY. Don't adapt away discipline.

**Flexible** (patterns, integrations): Adapt principles to context.

The skill itself tells you which type it is.

---

## The Golden Rule

> Instructions say WHAT to do. Skills say HOW to do it well.
> 
> "Add Stripe payments" is WHAT.
> `stripe-integration` skill tells you HOW.
> 
> Never skip the HOW.
