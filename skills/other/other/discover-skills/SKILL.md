---
name: discover-skills
description: Discover available Agent skills. Use when users ask "what skills are available", "list skills", "show me skills", or want to browse installed skill capabilities.
---

# Discover Skills

Help users explore and understand available Claude Code skills.

## Instructions

When invoked, search for and present all available skills in an organized manner.

### Steps

1. **List Loaded Skills**

   Skills from `~/.claude/skills/` and installed plugins are **already loaded** - check the Skill tool's "Available skills" list first.

2. **Search for Additional Skills**

   Use Glob tool to find uninstalled skills in the current project:

   ```
   # Plugin skills in workspace
   Glob: pattern="**/plugins/*/skills/*/SKILL.md"
   ```

3. **Search from Github via preset awesome list and Search using keyword**

   Dicovery skills via networking github colleciton repo, request to view readme for discovery more.

4. **Parse Skill Metadata**

   Extract from each SKILL.md frontmatter:
   - `name`: Skill identifier
   - `description`: What the skill does

5. **Present Results**

   ```markdown
   ## Available Skills

   | Skill | Description |
   |-------|-------------|
   | /skill-name | Brief description |

   ---

   **Tips:**
   - Use `/skill-name` to invoke a skill directly
   - Create custom skills in `.claude/skills/your-skill/SKILL.md`
   - Project skills (`.claude/skills/`) override global ones (`~/.claude/skills/`)
   ```

### Skill Locations

| Location | Scope | Priority |
|----------|-------|----------|
| `.claude/skills/` | Project | Highest |
| Plugin bundles | Plugin | Medium |
| `~/.claude/skills/` | User (global) | Lowest |

### Handling No Skills Found

If no skills are discovered:
1. Inform the user that no custom skills were found
2. Mention built-in skills from Claude Code (commit, code-review, etc.)
3. Provide guidance on creating custom skills
4. Recommend exploring skill collections (see below)

---

## Popular Skill Collections

> ⚠️ **Security Notice:** Always review third-party skills before installing. Skills contain instructions that Claude will follow - treat them like executable code.

### Official

| Repository | Description |
|------------|-------------|
| [anthropics/skills](https://github.com/anthropics/skills) | Official Anthropic skills - document processing, creative design, MCP builders |

### Community Curated (Awesome Lists)

| Repository | Description |
|------------|-------------|
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | Comprehensive catalog with categorized skills |
| [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | Community skills collection |
| [VoltAgent/awesome-claude-skills](https://github.com/VoltAgent/awesome-claude-skills) | Partner and community contributions |
| [BehiSecc/awesome-claude-skills](https://github.com/BehiSecc/awesome-claude-skills) | Curated skills list |

> **Note:** Awesome lists are curated indexes with links to actual skill repos. Always fetch and read the README first:
> ```bash
> gh repo view owner/repo
> ```

### Community Featured Skills

High-quality skills from recognized organizations and developers:

| Repository | Description |
|------------|-------------|
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | Vercel's official agent skills for React and Next.js development and Web Design guideline |
| [huggingface/skills](https://github.com/huggingface/skills) | HuggingFace ML/AI focused skills |
| [trailofbits/skills](https://github.com/trailofbits/skills) | Security-focused skills from Trail of Bits |
| [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | Obsidian knowledge management skills |
| [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) | Scientific research and analysis skills |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | UI/UX design with 50+ styles, palettes, and multi-framework support |

> **Tip:** These repos contain actual SKILL.md files. View and install directly:
> ```bash
> gh repo view vercel-labs/agent-skills
> gh api repos/vercel-labs/agent-skills/git/trees/main?recursive=1 --jq '.tree[] | select(.path | endswith("SKILL.md")) | .path'
> ```

---

## Explore Skills on GitHub

Use `gh` CLI to discover skill repositories dynamically.

### Search for Skill Repositories

```bash
# Search for SKILL.md files (most accurate)
gh search repos "SKILL.md in:path" --limit 30 --json fullName,description,stargazersCount,defaultBranch,createdAt,updatedAt

# Search agent-skills repos
gh search repos "skills" --limit 30 --match readme --json fullName,description,stargazersCount,defaultBranch,createdAt,updatedAt
```

### Get Repository Details

```bash
# Get README content for skill overview
gh repo view owner/repo

# Download specific SKILL.md file
gh repo view owner/repo --raw path/to/SKILL.md > skill.md
```

### Explore Skill Contents

```bash
# List skills directory structure
gh api repos/owner/repo/contents/skills --jq '.[].name'

# Get specific SKILL.md content (use --decode on macOS, -d on Linux)
gh api repos/owner/repo/contents/skills/skill-name/SKILL.md --jq '.content' | base64 --decode

# List all SKILL.md files in repo
gh api repos/owner/repo/git/trees/main?recursive=1 --jq '.tree[] | select(.path | endswith("SKILL.md")) | .path'
```

### Quick Install from GitHub

```bash
# Clone entire skills repo as plugin
gh repo clone owner/repo ~/.claude/plugins/repo-name

# Download single skill
mkdir -p ~/.claude/skills/skill-name
gh repo view owner/repo --raw skills/skill-name/SKILL.md > ~/.claude/skills/skill-name/SKILL.md
```

---

## Creating Custom Skills

Follow the template:

```yaml
---
name: my-skill
description: Clear description of when to trigger this skill
---

# My Skill

## Instructions
[What Claude should do when this skill activates]

## Examples
[Usage examples]
```

**Resources:**
- [What are skills?](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Creating custom skills](https://docs.anthropic.com/en/docs/claude-code/skills#creating-custom-skills)
