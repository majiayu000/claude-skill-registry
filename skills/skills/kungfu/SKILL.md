---
name: kungfu
# prettier-ignore
description: "Use when finding new AI agent skills, discovering capabilities, installing skills from GitHub, searching skill marketplaces, or expanding what Claude can do - like Neo downloading martial arts in The Matrix"
version: 1.2.0
category: meta
triggers:
  - "kungfu"
  - "find skills"
  - "install skill"
  - "skill marketplace"
  - "download skill"
  - "new capabilities"
  - "agent skills"
  - "expand abilities"
  - "i know kungfu"
  - "matrix"
---

<objective>
Discover, evaluate, and install AI agent skills from the ecosystem. Like Neo downloading kung fu in The Matrix - expand capabilities by finding and integrating new skills.
</objective>

<discovery-strategy>
Search GitHub for skill collections using:
- Repos matching "awesome*skills" or "claude*skills"
- Repos containing SKILL.md files (query: `path:SKILL.md claude`)
- Topics: claude-code, ai-skills, agent-skills

Known curated collections (verify availability before citing):
- VoltAgent/awesome-agent-skills
- composioHQ/awesome-claude-code-skills
- sickn33/antigravity-awesome-skills

If curated lists are unavailable, search GitHub directly. Prioritize repos updated within 6 months with meaningful star counts.
</discovery-strategy>

<skill-format>
Valid skills: SKILL.md with frontmatter (name, "Use when..." description, triggers). Optional scripts/tool for executables (require user approval before install).
</skill-format>

<quality-signals>
**Evaluate:** GitHub stars, recent activity, SKILL.md quality, documentation, relevance to user's need.

**Skip:** No SKILL.md, abandoned (no commits in 1+ year AND unresponsive), <10 stars (unless from trusted source), duplicates already-installed skill.
</quality-signals>

<security>
If a skill includes executable scripts in `scripts/`, ALWAYS:
1. Show the user the script contents
2. Explain what the script does
3. Get explicit approval before installing

Never auto-execute downloaded scripts.
</security>

<installation>
Install to the project's `.claude/skills/<skill-name>/` directory. For global installation, use `~/.claude/skills/`.

**Before installing:**
- Check for existing skill with same name
- If conflict: ask user to overwrite, rename, or skip

**After downloading:**
- Validate SKILL.md parses without YAML errors
- Confirm required frontmatter (name, description, triggers) exists
- Test with `/skill <name>` or a natural trigger phrase

**If install fails:** Remove any partially downloaded files and report the specific failure.
</installation>

<workflows>
<search>Query GitHub and curated lists, evaluate candidates against quality signals, present top 3-5 options with name, description, star count, last update, and install instructions.</search>

<install>Fetch skill, run security review if scripts present, validate format, install to skills directory, verify it loads.</install>

<audit>List installed skills from `.claude/skills/`, check source repos for updates, identify unused skills for removal.</audit>
</workflows>
