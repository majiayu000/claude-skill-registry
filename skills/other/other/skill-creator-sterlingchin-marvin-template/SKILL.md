---
name: skill-creator
description: |
  Create new MARVIN skills on request. Use when user says "give yourself the ability to X" or "create a skill for Y". Generates proper skill structure with SKILL.md.
license: MIT
compatibility: marvin
metadata:
  marvin-category: meta
  user-invocable: false
  slash-command: null
  model: default
  proactive: false
---

# Skill Creator Skill

Create new MARVIN skills based on user requests.

## When to Use

Trigger phrases:
- "Give yourself the ability to..."
- "Create a skill for..."
- "Add a workflow for..."
- "I want MARVIN to be able to..."

## Process

### Step 1: Understand the Request
Clarify:
- What should the skill do?
- When should it trigger?
- What inputs does it need?
- What output should it produce?

### Step 2: Design the Skill
Determine:
- **name**: Short, kebab-case identifier (e.g., `weekly-review`)
- **description**: Clear explanation of purpose and triggers
- **category**: session, work, content, research, events, communication, meta
- **user-invocable**: Does it have a slash command?
- **slash-command**: If yes, what command? (e.g., `/review`)
- **proactive**: Should MARVIN detect and trigger automatically?

### Step 3: Create Skill Directory
```bash
mkdir -p skills/{skill-name}
```

### Step 4: Write SKILL.md
Create `skills/{skill-name}/SKILL.md` with:

```markdown
---
name: {skill-name}
description: |
  {What this skill does and when to use it.}
license: MIT
compatibility: marvin
metadata:
  marvin-category: {category}
  user-invocable: {true|false}
  slash-command: {/command or null}
  model: default
  proactive: {true|false}
---

# {Skill Title}

{Brief description}

## When to Use

- {Trigger condition 1}
- {Trigger condition 2}

## Process

### Step 1: {First Step}
{Description}

### Step 2: {Second Step}
{Description}

## Output Format

{Expected output}

---

*Skill created: {TODAY}*
```

### Step 5: Add Scripts (if needed)
If the skill requires code:
```bash
mkdir -p skills/{skill-name}/scripts
```

Create necessary scripts in that directory.

### Step 6: Update Skill Index
Add the new skill to the Skill Index in `CLAUDE.md`:

```markdown
| `{skill-name}` | {triggers} | {description} |
```

### Step 7: Confirm Creation
Tell the user:
- Skill created at `skills/{skill-name}/SKILL.md`
- How to trigger it
- Ready to use immediately

## Output Format

```
Created skill: **{skill-name}**
- Location: `skills/{skill-name}/SKILL.md`
- Trigger: {how to use it}
- Category: {category}

The skill is ready to use.
```

## Notes
- Use the template at `skills/_template/SKILL.md` as a starting point
- Keep skills focused on one task
- Include clear trigger conditions so MARVIN knows when to use it

---

*Skill created: 2026-01-22*
