---
name: how-to-use-vercel-skills
description: How to create, structure, install, and publish agent skills compatible with the Vercel skills ecosystem and skills.sh. Use when the user wants to build a new skill, structure a SKILL.md file, add install commands to a website or README, or publish skills for distribution across 40+ AI agents.
metadata:
  author: agentpmt
  version: "1.0"
---

# How to Use Vercel Skills

Agent skills are folders of instructions, scripts, and resources that AI agents can discover and use. The format is an open standard supported by 40+ agents including Claude Code, Cursor, GitHub Copilot, Windsurf, Cline, Gemini CLI, OpenAI Codex, Roo Code, and many others.

## When to Use This Skill

- Creating a new agent skill from scratch
- Structuring a SKILL.md file with correct frontmatter and body
- Adding install commands to a website, README, or documentation
- Publishing skills so they appear on skills.sh
- Understanding how the skills CLI works (install, find, list, update, remove)
- Organizing a repository that contains multiple skills

## Skill File Structure

A skill is a directory containing at minimum a `SKILL.md` file. The directory name must exactly match the `name` field in the frontmatter.

### Minimal structure
```
my-skill/
  SKILL.md
```

### Full structure with optional directories
```
my-skill/
  SKILL.md              # Required -- agent instructions
  scripts/              # Optional -- executable helpers (bash, python, js)
  references/           # Optional -- detailed docs loaded on demand
  assets/               # Optional -- templates, schemas, static files
```

## SKILL.md Format

Every SKILL.md must start with YAML frontmatter followed by markdown content.

### Frontmatter

```yaml
---
name: my-skill-name
description: What this skill does and when to use it. Include keywords that help agents match tasks to this skill.
---
```

### Required fields

| Field | Rules |
|-------|-------|
| `name` | 1-64 characters. Lowercase letters, numbers, and hyphens only. Must not start or end with a hyphen. No consecutive hyphens (`--`). Must match the parent directory name. |
| `description` | 1-1024 characters. Describe what the skill does AND when to use it. Include specific keywords that help agents identify relevant tasks. |

### Optional fields

| Field | Purpose |
|-------|---------|
| `license` | License name or reference to a bundled LICENSE file. |
| `compatibility` | Max 500 characters. Environment requirements (e.g., "Requires git, docker, jq"). Most skills do not need this. |
| `metadata` | Arbitrary key-value pairs. Common keys: `author`, `version`. |
| `allowed-tools` | Space-delimited list of pre-approved tools. Experimental, support varies by agent. |

### Full frontmatter example

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.
license: MIT
compatibility: Requires Python 3.10+
metadata:
  author: example-org
  version: "2.1"
allowed-tools: Bash(python:*) Read
---
```

### Name field rules

Valid:
- `pdf-processing`
- `data-analysis`
- `code-review`
- `my-skill-v2`

Invalid:
- `PDF-Processing` (uppercase not allowed)
- `-pdf` (cannot start with hyphen)
- `pdf-` (cannot end with hyphen)
- `pdf--processing` (consecutive hyphens not allowed)
- `my skill` (spaces not allowed)

### Writing a good description

The description is a routing rule, not a title. Agents see only the `name` and `description` at startup to decide whether to load the full skill.

Bad:
```yaml
description: Helps with PDFs.
```

Good:
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.
```

### Body content

The markdown body after frontmatter contains the actual instructions. There are no format restrictions, but recommended sections include:

- What this skill does
- When to use it (and when not to)
- Step-by-step procedure
- Examples of inputs and outputs
- Common edge cases and failure modes
- Validation criteria ("how to know it worked")

Keep the main SKILL.md under 500 lines. Move detailed reference material to files in `references/`.

## Progressive Disclosure

Skills load in stages to minimize context usage:

1. **Metadata** (~100 tokens): `name` and `description` are loaded at startup for all installed skills.
2. **Instructions** (< 5000 tokens recommended): The full SKILL.md body is loaded when the agent activates the skill.
3. **Resources** (as needed): Files in `scripts/`, `references/`, and `assets/` are loaded only when required.

## Install Commands for Websites and READMEs

### Install all skills from a repo
```bash
npx skills add owner/repo
```

### Install a specific skill from a multi-skill repo
```bash
npx skills add owner/repo --skill skill-name
```

### Install all skills from a repo non-interactively
```bash
npx skills add owner/repo --all -y
```

### Install to a specific agent only
```bash
npx skills add owner/repo --agent claude-code
npx skills add owner/repo --agent cursor
```

### Install globally (user-wide, not just current project)
```bash
npx skills add owner/repo --global
```

### Example website/README copy

For a repo at `github.com/myorg/my-agent-skills` with a skill called `my-workflow`:

```markdown
## Install

Install all skills:
```
npx skills add myorg/my-agent-skills
```

Install just the workflow skill:
```
npx skills add myorg/my-agent-skills --skill my-workflow
```
```

## CLI Reference

| Command | Purpose |
|---------|---------|
| `npx skills add <source>` | Install skills from a GitHub repo, URL, or local path |
| `npx skills list` | Show installed skills (alias: `ls`) |
| `npx skills find [query]` | Search for skills interactively or by keyword |
| `npx skills check` | Check for available updates |
| `npx skills update` | Upgrade all installed skills |
| `npx skills init [name]` | Generate a new SKILL.md template |
| `npx skills remove [skills]` | Uninstall skills |

### Source formats the CLI accepts

- GitHub shorthand: `owner/repo`
- Full GitHub URL: `https://github.com/owner/repo`
- Direct skill path: `https://github.com/owner/repo/tree/main/skills/skill-name`
- GitLab and other git hosts
- Local filesystem paths

### Key flags

| Flag | Purpose |
|------|---------|
| `-s, --skill` | Install a specific skill by name, or `'*'` for all |
| `-a, --agent` | Target a specific agent (e.g., `claude-code`, `cursor`) |
| `-g, --global` | Install to user home directory instead of project |
| `--copy` | Copy files instead of creating symlinks |
| `-y, --yes` | Skip confirmation prompts |
| `--all` | Install all skills to all agents non-interactively |
| `-l, --list` | Preview available skills without installing |

## Where Skills Get Installed

The CLI automatically places skills in the correct location for each agent:

| Agent | Project path | Global path |
|-------|-------------|-------------|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `.agents/skills/` | `~/.cursor/skills/` |
| GitHub Copilot | `.agents/skills/` | varies |
| Windsurf | `.agents/skills/` | varies |

40+ agents are supported. The CLI handles path resolution automatically.

## Repository Organization

### Single skill repo
```
my-repo/
  SKILL.md
```

### Multi-skill repo (recommended for collections)
```
my-repo/
  skills/
    skill-one/
      SKILL.md
    skill-two/
      SKILL.md
      scripts/
        helper.sh
      references/
        detailed-guide.md
```

The CLI searches these locations automatically:
- Repository root
- `skills/` directory and its subdirectories
- `skills/.curated/`, `skills/.experimental/`, `skills/.system/`
- Agent-specific directories (`.claude/skills/`, `.agents/skills/`, etc.)
- Recursive fallback if nothing found in standard locations

Skills can be nested in subdirectories (e.g., `skills/category/my-skill/SKILL.md`) and the CLI will still discover them.

## Publishing and Discovery

Skills appear on [skills.sh](https://skills.sh/) automatically when people install them via the CLI. There is no separate publish step. To get your skill listed:

1. Put your skill in a public GitHub repo with a valid SKILL.md
2. Share the install command: `npx skills add owner/repo`
3. As people install it, it appears and climbs the skills.sh leaderboard

## Validation

Use the reference library to validate your skill before publishing:

```bash
npx skills-ref validate ./my-skill
```

This checks that frontmatter is valid and naming conventions are followed.

## Quick Checklist for a New Skill

1. Create a directory with a lowercase, hyphenated name
2. Add a SKILL.md with `name` and `description` in the frontmatter
3. Ensure `name` exactly matches the directory name
4. Write a description that works as a routing rule (what it does + when to use it)
5. Write clear instructions in the markdown body
6. Keep SKILL.md under 500 lines; use `references/` for detailed docs
7. Add `scripts/` for any executable helpers
8. Test by running `npx skills add .` locally
9. Push to a public GitHub repo
10. Share the install command: `npx skills add owner/repo`
