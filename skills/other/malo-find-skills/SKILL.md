---
name: malo-find-skills
description: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.
---

# Find Skills

This skill helps you discover and install skills from the open agent skills ecosystem (https://skills.sh). Based on the [find-skills](https://github.com/vercel-labs/skills/tree/main/skills/find-skills) skill by Vercel, adapted for this Nix-managed environment.

## When to Use This Skill

Use this skill when the user:

- Asks "how do I do X" where X might be a common task with an existing skill
- Says "find a skill for X" or "is there a skill for X"
- Asks "can you do X" where X is a specialized capability
- Expresses interest in extending agent capabilities
- Wants to search for tools, templates, or workflows

## How Skills Work in This Setup

All paths below (e.g. `home/claude.nix`, `configs/claude/skills/`) are relative to the nix-config directory.

Skills are split into two categories:

- **Custom skills**: Directories in `configs/claude/skills/` committed to the nix-config repo. These are skills we author and maintain.
- **External skills**: Installed from skills.sh via `npx skills add`. These are managed by an activation script in `home/claude.nix` and are gitignored (they appear as symlinks in the skills directory, not regular directories).

The activation script defines a list called `externalSkills`. On every `nh darwin switch --no-nom`, it removes all Claude Code external skills and reinstalls only the declared ones. This keeps external skills declarative and reproducible.

## Finding Skills

### Step 1: Search

Run the find command with a relevant query:

```bash
npx skills find [query]
```

For example:

- "how do I make my React app faster?" -> `npx skills find react performance`
- "can you help me with PR reviews?" -> `npx skills find pr review`
- "I need to create a changelog" -> `npx skills find changelog`

You can also browse skills at https://skills.sh/

### Step 2: Present Options

When you find relevant skills, present them with:

1. The skill name and what it does
2. The install command
3. A link to learn more

### Step 3: Install

To try a skill immediately:

```bash
npx skills add <owner/repo> --skill <name> -g -a claude-code -y
```

Always pass `-a claude-code` to avoid installing for other agents. The `-g` flag installs globally (user-level) and `-y` skips prompts.

### Step 4: Make It Permanent

If the user wants to keep the skill across rebuilds, add it to the `externalSkills` list in `home/claude.nix`:

```nix
externalSkills = [
  "anthropics/skills --skill pdf"
  "owner/repo --skill new-skill"  # <- add here
];
```

Then `nh darwin switch --no-nom` will install it on every activation.

## Creating a Custom Skill

If no existing skill fits, or the user wants to build their own:

1. Create a directory in `configs/claude/skills/<skill-name>/`
2. Add a `SKILL.md` with YAML frontmatter (`name` and `description`) and instructions
3. The gitignore allowlists directories automatically, so it will be tracked in git
4. Optionally add `references/`, `scripts/`, or other supporting files

## When No Skills Are Found

If no relevant skills exist:

1. Acknowledge that no existing skill was found
2. Offer to help with the task directly
3. Suggest creating a custom skill if it's a repeatable workflow
