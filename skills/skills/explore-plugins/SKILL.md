---
name: explore-plugins
description: Discover and install useful Claude Code plugins for your project. Recommends based on your tech stack.
disable-model-invocation: true
---

# Explore Plugins

Discover and install Claude Code plugins (also called "skills packages") that enhance your workflow.

## Usage

`/explore-plugins`

## Procedure

### Step 1: Detect Project Tech Stack

Scan the project to understand what technologies are in use:

- **Language**: Check for `package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, etc.
- **Framework**: Check for Next.js, React, Vue, Django, Rails, etc.
- **Tools**: Check for Docker, Terraform, Kubernetes configs
- **Type**: Is this a web app, API, CLI tool, library, mobile app?

### Step 2: Search Available Plugins

Search for relevant skills/plugins:

1. **Official Anthropic skills**: Search `github.com/anthropics/skills`
2. **Community skills**: Search `github.com` for `claude-code skills [tech-stack]`
3. **skills.sh registry**: Search for skills matching the detected tech stack
4. **Vercel skills**: Search `github.com/vercel-labs/skills`

### Step 3: Present Recommendations

Show the user a categorized list:

```
## Recommended Plugins for Your Project

Based on your stack: [detected stack]

### Highly Recommended
1. **[name]** — [description]
   Installs: [N] | Source: [owner/repo]
   Why: [reason this is relevant to their project]

### Nice to Have
2. **[name]** — [description]
   Installs: [N] | Source: [owner/repo]
   Why: [reason]

### Meta / Utility
3. **find-skills** — Discover more skills on demand
   Installs: 179K+ | Source: vercel-labs/skills
4. **skill-creator** — Create your own skills from workflows
   Installs: 28K+ | Source: anthropics/skills

Which would you like to install? (e.g., "1,3,4")
```

### Step 4: Install Selected Plugins

For each selected plugin, install using the skills CLI:

```bash
npx skills add <owner/repo>
```

This installs the skill to `.claude/skills/`.

If `npx skills` is not available, fall back to manual installation:
1. Clone or download the skill's SKILL.md
2. Place it in `.claude/skills/<skill-name>/SKILL.md`

### Step 5: Verify Installation

After installation:
1. Check that the skill files exist in `.claude/skills/`
2. Tell the user to test with `/[skill-name]`
3. Note that some skills may require additional setup (API keys, config files)

### Step 6: Show What's Installed

List all currently installed skills:

```
## Installed Skills
- [name]: [description] (source: [where it came from])
- [name]: [description] (source: custom/local)
```
