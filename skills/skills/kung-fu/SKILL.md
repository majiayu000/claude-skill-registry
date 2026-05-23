---
name: kung-fu
description: A package manager for AI knowledge. Meta-skill for on-demand skill discovery and installation — search curated local repositories or the global skills.sh registry. Self-teaching capability that finds, evaluates, and installs relevant skills when the agent lacks expertise. Use when encountering unfamiliar frameworks, languages, tools, or domains. Use when you need to "learn a skill", "find skills for X", "search for skills", or when you lack expertise in a specific technology.
context: fork
---

## Learning Skills

### Overview

This skill runs in a forked context and helps you discover and install relevant skills for a given task using a two-tier approach:

1. **Local repositories** (preferred): Search through known, validated repositories in @./SKILL_REPOSITORIES.md
2. **Remote search** (fallback): Query the skills.sh API to discover skills from the broader ecosystem

**Context:** When invoked, use `$ARGUMENTS` to understand what skills are needed. For example, if invoked as `/kung-fu Flask API with authentication`, search for Flask and authentication-related skills.

First, run the `add-skill` CLI with the help flag to get a general understanding of what it does and how it works:

```bash
npx -y add-skill --help
```

### Source Formats

The CLI accepts multiple repository formats:

| Format | Example |
|--------|---------|
| GitHub shorthand | `vercel-labs/agent-skills` |
| Full GitHub URL | `https://github.com/vercel-labs/agent-skills` |
| Direct skill path | `https://github.com/vercel-labs/agent-skills/tree/main/skills/frontend-design` |
| GitLab repository | `https://gitlab.com/org/repo` |
| Generic git URL | `git@github.com:vercel-labs/agent-skills.git` |

### CLI Flags Reference

| Flag | Purpose |
|------|---------|
| `-l, --list` | Display available skills without installing |
| `-s, --skill <skills...>` | Install only specified skills by name |
| `-a, --agent <agents...>` | Target specific agents (see @./AGENTS.md) |
| `-g, --global` | Install to user directory instead of project-level |
| `-y, --yes` | Skip confirmation prompts |
| `-h, --help` | Show help information |

### Reading

Read from the list of repositories in @./SKILL_REPOSITORIES.md and run each one:

```bash
npx -y add-skill <repository> --list
```

This displays a list of skill names and their associated descriptions.

#### Example

```bash
> npx -y add-skill vercel-labs/agent-skills --list

┌   skills
│
◇  Source: https://github.com/vercel-labs/agent-skills.git
│
◇  Repository cloned
│
◇  Found 2 skills
│
◇  Available Skills
│
│    vercel-react-best-practices
│
│      React and Next.js performance optimization guidelines from Vercel Engineering. This skill should be used when writing, reviewing, or refactoring React/Next.js code to ensure optimal performance patterns. Triggers on tasks involving React components, Next.js pages, data fetching, bundle optimization, or performance improvements.
│
│    web-design-guidelines
│
│      Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".
```

Do this for all known skill repositories.

### Remote Search (skills.sh)

If no relevant skills are found in the known repositories, or if the user explicitly requests a remote search, use the skills.sh API to discover skills from the broader ecosystem.

**When to use remote search:**
- User explicitly asks to "search for skills" or "find skills remotely"
- No relevant skills found in @./SKILL_REPOSITORIES.md for the task at hand
- Working with an unfamiliar technology or domain

**Important:** Before searching remotely, ask the user for confirmation unless they explicitly requested it.

#### Search API

```bash
curl -s "https://skills.sh/api/search?q=<query>&limit=<limit>"
```

| Parameter | Description |
|-----------|-------------|
| `q` | Search query (e.g., "flask", "terraform", "react testing") |
| `limit` | Maximum results to return (default: 10, max: 50) |

#### Example Search

```bash
curl -s "https://skills.sh/api/search?q=flask&limit=10"
```

Response:

```json
{
  "query": "flask",
  "searchType": "fuzzy",
  "skills": [
    {
      "id": "flask",
      "name": "flask",
      "installs": 70,
      "topSource": "jezweb/claude-skills"
    },
    {
      "id": "flask-api-development",
      "name": "flask-api-development",
      "installs": 11,
      "topSource": "aj-geddes/useful-ai-prompts"
    }
  ],
  "count": 2,
  "duration_ms": 2
}
```

#### Remote Search Workflow

1. **Search** for skills matching your task:
   ```bash
   curl -s "https://skills.sh/api/search?q=<technology>&limit=20"
   ```

2. **Extract repositories** from the `topSource` field in each result.

3. **List descriptions** from discovered repositories:
   ```bash
   npx -y add-skill <topSource> --list
   ```

4. **Evaluate** the skill descriptions to determine relevance.

5. **Install** relevant skills using the standard installation command.

#### Example: Finding Flask Skills

```bash
# Step 1: Search for flask skills
curl -s "https://skills.sh/api/search?q=flask&limit=10"

# Step 2: List skills from discovered repositories
npx -y add-skill jezweb/claude-skills --list
npx -y add-skill aj-geddes/useful-ai-prompts --list

# Step 3: Install the relevant skill
npx -y add-skill jezweb/claude-skills -y -a claude-code --skill flask
```

### Deciding

Now that you see all available skills, install any skills that are related to the task at hand:

```bash
npx -y add-skill <repository> -y -a <agent-name> --skill <skill-name>
```

The agent name is the name of the agent you are using. See @./AGENTS.md for acceptable values.

#### Example

If your thoughts are along the lines of "I'm creating a website," you should identify *web-design-guidelines* as a good skill to learn:

```bash
npx -y add-skill vercel-labs/agent-skills -y -a claude-code --skill web-design-guidelines
```

You can install multiple skills by repeating the `--skill` flag:

```bash
npx -y add-skill <repository> -y -a <agent-name> --skill <skill-a> --skill <skill-b> --skill <skill-c>
```

You may also install all skills from a repository at once:

```bash
npx -y add-skill <repository> -y -a <agent-name> --all
```

For global installation (user directory instead of project-level), add the `-g` flag:

```bash
npx -y add-skill <repository> -y -g -a <agent-name> --skill <skill-name>
```

### Acknowledgment

After successfully installing skills, announce what you've learned using proper grammar:

**One skill:**
> I know Terraform.

**Two skills:**
> I know Terraform and Flask.

**Three or more skills:**
> I know Terraform, Flask, and React.

This confirms to the user that the knowledge upload is complete.

### Telemetry

To disable anonymous usage data collection:

```bash
DISABLE_TELEMETRY=1 npx -y add-skill <repository> --list
```

Telemetry is automatically disabled in CI environments.