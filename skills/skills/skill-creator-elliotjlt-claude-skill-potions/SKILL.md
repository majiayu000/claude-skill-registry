---
name: skill-creator
description: |
  Meta-skill for creating well-structured skills with proper progressive
  disclosure. When user wants to create a new skill, guide them through
  the process: purpose, triggers, instructions, guardrails, examples.
  Ensures skills follow the repository conventions and are immediately usable.
allowed-tools: |
  bash: ls, cat, mkdir
  file: read, write
---

# Skill Creator

<purpose>
Creating good skills is itself a skill. This meta-skill guides the creation
of new skills with proper structure, clear triggers, actionable instructions,
and the guardrails that make skills reliable. It's the skill that makes skills.
</purpose>

## When To Activate

Trigger when:

- User says "create a skill for X"
- User says "make this into a skill"
- User asks how to write a skill
- User wants to add to the skill library
- skill-forge needs to materialize a skill

## The Skill Template

<template>
```markdown
---
name: [kebab-case-name]
description: |
  [2-4 sentence description. This is what triggers activation.
  Be specific about WHEN this skill should activate. Include
  keywords that would appear in relevant user requests.]
allowed-tools: |
  bash: [list of bash commands needed]
  file: [read, write, etc.]
---

# [Skill Name]

<purpose>
[1-2 paragraphs: Why does this skill exist? What problem does it solve?
What goes wrong without it? This grounds the skill in real need.]
</purpose>

## When To Activate

Trigger when:
- [Specific condition 1]
- [Specific condition 2]
- [Specific condition 3]

Do NOT trigger for:
- [Exception 1]
- [Exception 2]

## Instructions

### Step 1: [Verb-based title]
[Clear, actionable instructions]

### Step 2: [Verb-based title]
[Clear, actionable instructions]

### Step 3: [Verb-based title]
[Clear, actionable instructions]

## NEVER
- [Hard rule 1 - something that would break the skill's purpose]
- [Hard rule 2]
- [Hard rule 3]

## ALWAYS
- [Required behaviour 1]
- [Required behaviour 2]
- [Required behaviour 3]

## Examples

### Example 1: [Descriptive scenario name]

[Show concrete input and output. Real-world scenario.]

### Example 2: [Another scenario]

[Different angle or edge case.]

<failed-attempts>
What DOESN'T work:
- [Approach that seems reasonable but fails, and why]
- [Common mistake to avoid]
</failed-attempts>

## Why This Skill Exists

[Final grounding: the human cost of not having this skill]
```
</template>

## Instructions

### Step 1: Clarify the Need

Before creating, understand:

```
What problem does this skill solve?
What goes wrong without it?
Who/when would use this?
Is there an existing skill that covers this?
```

### Step 2: Define the Trigger

The description field is critical - it determines activation:

```
Good trigger: "When modifying database schemas, force migration planning
              and rollback strategy before executing any ALTER statements"

Bad trigger: "Help with databases"
```

Be specific. Include keywords. Describe the situation.

### Step 3: Write Clear Instructions

Each step should be:
- Actionable (starts with verb)
- Unambiguous (one interpretation)
- Testable (you can verify it was done)

```
Good: "List all callers of the function using grep or IDE find-references"
Bad: "Consider the dependencies"
```

### Step 4: Add Guardrails

NEVER/ALWAYS sections prevent misuse:

- NEVER: Things that would break the skill's intent
- ALWAYS: Non-negotiable behaviours

```
NEVER:
- Skip the migration plan for "simple" changes
- Execute DDL without rollback strategy

ALWAYS:
- Test migrations on copy of production data
- Include rollback script with every migration
```

### Step 5: Provide Real Examples

Examples should be:
- Concrete (real-looking code/scenarios)
- Complete (show full input → output)
- Varied (different situations)

Include `<failed-attempts>` - what doesn't work and why.

### Step 6: Write the File

Create the skill:

```
mkdir -p skills/[skill-name]
# Write SKILL.md with template
```

## Skill Quality Checklist

<checklist>
Before finalizing, verify:

| Aspect | Check |
|--------|-------|
| Name | Kebab-case, descriptive, not generic |
| Description | Specific triggers, includes keywords |
| Purpose | Clear problem statement, real need |
| Triggers | Specific conditions, includes exceptions |
| Instructions | Actionable steps, unambiguous |
| NEVER | Prevents misuse, hard rules |
| ALWAYS | Required behaviours, non-negotiable |
| Examples | Concrete, complete, varied |
| Failed attempts | Documents what doesn't work |
| Distinct | Not duplicate of existing skill |
</checklist>

## Progressive Disclosure

<progressive-disclosure>
Skills should reveal complexity gradually:

**Layer 1: Metadata** (~100 tokens)
- Name + description
- Always loaded, determines activation
- Must be tight and triggerable

**Layer 2: Instructions** (~500-1000 tokens)
- Loaded when skill activates
- Step-by-step process
- The "how to"

**Layer 3: Resources** (variable)
- Scripts, templates, references
- Executed or loaded on demand
- Not in main context

Keep Layer 1 tight. Most tokens should be in Layer 2.
</progressive-disclosure>

## Common Skill Patterns

<patterns>
**The Checklist** (prove-it, loose-ends)
- Run through verification steps
- Binary pass/fail outcomes

**The Process** (rubber-duck, battle-plan)
- Multi-step workflow
- Each step builds on previous

**The Gate** (you-sure, skill-gate)
- Pause before action
- Require confirmation

**The Transform** (geordie, explain-like)
- Change output format/style
- Modify how information is presented

**The Analysis** (pre-mortem, split-decision)
- Structured evaluation
- Multiple perspectives/options
</patterns>

## NEVER

- Create vague, generic skills ("help with code")
- Skip the examples section
- Write instructions that are just "be careful about X"
- Duplicate existing skills
- Create skills without NEVER/ALWAYS guardrails
- Make triggers too broad (will over-activate)

## ALWAYS

- Include `<failed-attempts>` section
- Test trigger description against likely user prompts
- Keep description under 100 tokens
- Make instructions step-by-step and actionable
- Ground in real problem (not theoretical)

## Examples

### Example 1: User Requests New Skill

User: "Create a skill for handling database migrations"

```
Let me create a structured skill for database migrations.

First, some questions:
1. What goes wrong without this skill? (e.g., data loss, failed deployments)
2. What's the trigger? (modifying schemas, adding tables, etc.)
3. What's the process you want enforced?

[After gathering info, creates skill following template]
```

### Example 2: Forging from Discovery

skill-forge identifies a non-obvious learning about API rate limiting.

```
Forging skill: api-rate-limit-handling

[Creates skill with:]
- Trigger: When implementing API calls, external service integration
- Instructions: Check rate limits, implement backoff, handle 429s
- Failed attempts: "Tried simple retry - got banned"
- Examples: Concrete rate limiting code
```

## Integration

This skill is the foundation for:
- **skill-forge**: Uses skill-creator to materialize discoveries
- **learn-from-this**: Feeds insights to skill-creator
- All manual skill creation

## Why This Skill Exists

Bad skills are worse than no skills - they activate at wrong times, give vague
guidance, and erode trust in the system. Good skills are force multipliers.

This meta-skill ensures every new skill meets the quality bar. It's the
quality gate for the skill library itself.
