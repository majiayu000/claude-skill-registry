---
title: 'Create your first skill'
---

Skills are reusable knowledge packages that AI coding agents can discover and use to perform tasks more accurately. Unlike commands (which you invoke explicitly) or standards (which apply automatically), skills are **agent-discovered**—the AI automatically loads relevant skills based on the task at hand.

<Tip>
  **Looking for inspiration?** Check out the
  [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills/)
  repository for a curated list of community skills you can use as examples or
  starting points.
</Tip>

<Info>
  Learn more about how skills work in the [Skills
  Management](/concepts/skills-management) section.
</Info>

## Prerequisites

- The CLI must be installed: see [CLI Installation](/tools/cli#installation)
- You must be authenticated: run `packmind-cli login`

## Understanding the Skill Format

Skills follow the [Agent Skills specification](https://agentskills.io/home), an open format for giving agents new capabilities and expertise. A skill is a folder containing at minimum a `SKILL.md` file, plus optional supporting files like templates, scripts, and resources.

For details on the SKILL.md format, frontmatter fields, and best practices, refer to the [Agent Skills specification](https://agentskills.io/home).

## Create a Skill Using the AI Agent

The easiest way to create a skill is using the built-in `/packmind-create-skill` command with your AI coding assistant.

### Install Default Skills

First, ensure the skill creation tools are available locally. Run:

```bash
packmind-cli skills init
```

This installs Packmind's default skills, including the `packmind-create-skill` skill that guides you through creating new skills.

<Tip>
  **Automatic installation** — Default skills are also installed automatically
  when you install a package with `packmind-cli install` or when packages are
  distributed to your repository.
</Tip>

### Create Your Skill

Once default skills are installed, invoke the `/packmind-create-skill` command in your AI coding assistant:

```
/packmind-create-skill
```

The assistant will guide you through:

1. **Defining the skill purpose** — Describe what capability you want to provide
2. **Identifying triggers** — Specify when the AI should activate this skill
3. **Planning resources** — Determine if you need scripts, templates, or references
4. **Generating the skill** — Create the `SKILL.md` and supporting files
5. **Validating** — Check the skill follows the specification

After the assistant generates your skill, you can test it locally before uploading.

## How to Upload a Skill to Packmind

Once you have a skill folder ready, upload it to Packmind using the CLI:

```bash
packmind-cli skills add ./my-skill
```

The CLI will upload the skill to your Packmind organization and display a confirmation.

### Uploading Multiple Skills at Once

If you have a collection of skills organized in subdirectories (e.g., `.claude/skills/*/`), you can upload them all with a single command:

```bash
for dir in '.claude/skills/*/'; do packmind-cli skills add "$dir"; done
```

This iterates through all skill folders and uploads each one to Packmind.

## View Your Skill

After uploading, your skill appears in the Packmind web app:

1. Navigate to **Skills** in the main menu
2. Find your skill in the list
3. Click to view details, including files and version history

## Distribute Your Skill

Once created, add your skill to a package to distribute it to repositories:

1. Go to **Packages** in the web app
2. Edit an existing package or create a new one
3. Add your skill to the package
4. Distribute the package to your repositories

After distribution, the skill appears in:

- `.claude/skills/{skill-slug}/SKILL.md` for Claude Code and Cursor
- `.github/skills/{skill-slug}/SKILL.md` for GitHub Copilot

See [Understanding Where Your Artifacts Appear](/concepts/artifact-rendering) for details.

## Tips

- **Keep skills focused** — Each skill should address a specific capability or workflow
- **Write clear triggers** — Describe precisely when the AI should activate the skill
- **Include examples** — Show expected inputs and outputs where applicable
- **Test locally first** — Verify your SKILL.md renders correctly before uploading
- **Browse community skills** — Explore [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills/) for real-world examples and inspiration
- **Read the specification** — Check the [Agent Skills specification](https://agentskills.io/home) for the complete format details
