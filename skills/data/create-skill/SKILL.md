---
name: create-skill
description: Create a custom skill that's protected from Dex updates. Automatically appends -custom to ensure your skill is never overwritten.
---

# Create Custom Skill

Create your own skill that's protected from Dex updates.

## How It Works

When you create a skill with this command, Dex automatically:
1. Appends `-custom` to the folder name (so it's never overwritten by updates)
2. Creates the proper SKILL.md structure
3. Sets up optional folders for scripts, references, and assets

## Process

### Step 1: Get Skill Details

Ask the user:

```
What should this skill do?

Give me:
1. A short name (e.g., "meeting-notes", "weekly-report")
2. What it should help you with (1-2 sentences)
```

### Step 2: Create the Skill

**Skill folder:** `.claude/skills/{name}-custom/`

The `-custom` suffix is automatic - don't let the user add it themselves.

**Create SKILL.md:**

```markdown
---
name: {name}-custom
description: {user's description}
---

# {Title Case Name}

{User's description expanded into a helpful intro}

## Process

### Step 1: [First Step]

[Instructions for what to do]

### Step 2: [Second Step]

[Instructions for what to do]

## Notes

- This is a custom skill, protected from Dex updates
- Edit `.claude/skills/{name}-custom/SKILL.md` to modify
```

### Step 3: Confirm

```
✅ Created skill: /{{name}}-custom

Your skill is ready to use. Run /{name}-custom to try it.

**Protected from updates:** The -custom suffix means Dex updates
will never overwrite this skill. It's yours to customize.

**To edit:** Modify .claude/skills/{name}-custom/SKILL.md
```

## Examples

**User:** "I want a skill for preparing board updates"

**Result:**
- Folder: `.claude/skills/board-update-custom/`
- Invoke with: `/board-update-custom`
- Protected from all Dex updates

**User:** "Create a skill called weekly-standup-custom"

**Response:** "I'll create that as `weekly-standup-custom` - you don't need to add '-custom' yourself, I do that automatically. Want me to proceed with just 'weekly-standup'?"

## Tips

- Keep skill names short and descriptive
- Use hyphens, not spaces or underscores
- The skill can reference other files in its folder (scripts/, references/, assets/)
