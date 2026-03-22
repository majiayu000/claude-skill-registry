---
name: skill-creator
description: >
  Guide for creating effective skills for Apollo GraphQL and GraphQL development. Use this skill when:
  (1) users want to create a new skill,
  (2) users want to update an existing skill,
  (3) users ask about skill structure or best practices,
  (4) users need help writing SKILL.md files.
license: MIT
compatibility: Works with Claude Code and similar AI coding assistants that support Agent Skills.
metadata:
  author: apollographql
  version: "1.0.0"
allowed-tools: Read Write Edit Glob Grep
---

# Skill Creator Guide

This guide helps you create effective skills for Apollo GraphQL and GraphQL development following the [Agent Skills specification](https://agentskills.io/specification).

## What is a Skill?

A skill is a directory containing instructions that extend an AI agent's capabilities with specialized knowledge, workflows, or tool integrations. Skills activate automatically when agents detect relevant tasks.

## Directory Structure

A skill requires at minimum a `SKILL.md` file:

```
skill-name/
├── SKILL.md              # Required - main instructions
└── references/           # Optional - detailed documentation
    ├── topic-a.md
    └── topic-b.md
```

## SKILL.md Format

### Frontmatter (Required)

```yaml
---
name: skill-name
description: >
  A clear description of what this skill does and when to use it.
  Include trigger conditions: (1) first condition, (2) second condition.
license: MIT
compatibility: Works with Claude Code and similar AI coding assistants.
metadata:
  author: your-org
  version: "1.0.0"
allowed-tools: Read Write Edit Glob Grep
---
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase, hyphens only. Must match directory name. Max 64 chars. |
| `description` | Yes | What the skill does and when to use it. Max 1024 chars. |
| `license` | No | License name (e.g., MIT, Apache-2.0). |
| `compatibility` | No | Environment requirements. Max 500 chars. |
| `metadata` | No | Key-value pairs for author, version, etc. |
| `allowed-tools` | No | Space-delimited list of pre-approved tools. Do not include `Bash(curl:*)`. |

### Name Rules

- Use lowercase letters, numbers, and hyphens only
- Do not start or end with a hyphen
- Do not use consecutive hyphens (`--`)
- Must match the parent directory name

Good: `apollo-client`, `graphql-schema`, `rover`
Bad: `Apollo-Client`, `-apollo`, `apollo--client`

### Description Best Practices

Write descriptions that help agents identify when to activate the skill:

```yaml
# Good - specific triggers and use cases
description: >
  Guide for designing GraphQL schemas following industry best practices. Use this skill when:
  (1) designing a new GraphQL schema or API,
  (2) reviewing existing schema for improvements,
  (3) deciding on type structures or nullability,
  (4) implementing pagination or error patterns.

# Bad - vague and unhelpful
description: Helps with GraphQL stuff.
```

## Body Content

The markdown body contains instructions the agent follows. Structure it for clarity:

### Recommended Sections

1. **Overview** - Brief explanation of the skill's purpose
2. **Process** - Step-by-step workflow (use checkboxes for multi-step processes)
3. **Quick Reference** - Common patterns and syntax
4. **Reference Files** - Links to detailed documentation
5. **Key Rules** - Important guidelines organized by topic
6. **Ground Rules** - Critical do's and don'ts

### Example Structure

```markdown
# Skill Title

Brief overview of what this skill helps with.

## Process

Follow this process when working on [task]:

- [ ] Step 1: Research and understand requirements
- [ ] Step 2: Implement the solution
- [ ] Step 3: Validate the result

## Quick Reference

### Common Pattern

\`\`\`graphql
type Example {
  id: ID!
  name: String
}
\`\`\`

## Reference Files

- [Topic A](references/topic-a.md) - Detailed guide for topic A
- [Topic B](references/topic-b.md) - Detailed guide for topic B

## Key Rules

### Category One

- Rule about this category
- Another rule

### Category Two

- Rule about this category

## Ground Rules

- ALWAYS do this important thing
- NEVER do this problematic thing
- PREFER this approach over that approach
```

## Progressive Disclosure

Structure skills to minimize context usage:

1. **Metadata** (~100 tokens): `name` and `description` load at startup for all skills
2. **Instructions** (< 5000 tokens): Full `SKILL.md` loads when skill activates
3. **References** (as needed): Files in `references/` load only when required

Keep `SKILL.md` under 500 lines. Move detailed documentation to reference files.

## Reference Files

Use `references/` for detailed documentation:

```
references/
├── setup.md          # Installation and configuration
├── patterns.md       # Common patterns and examples
├── troubleshooting.md # Error solutions
└── api.md            # API reference
```

Reference files should be:

- Focused on a single topic
- Self-contained (readable without other files)
- Under 300 lines each

Link to references from `SKILL.md`:

```markdown
## Reference Files

- [Setup](references/setup.md) - Installation and configuration
- [Patterns](references/patterns.md) - Common patterns and examples
```

## Writing Style

Follow the Apollo Voice for all skill content:

### Tone

- Approachable and helpful
- Opinionated and authoritative (prescribe the "happy path")
- Direct and action-oriented

### Language

- Use American English
- Keep language simple; avoid idioms
- Use present tense and active voice
- Use imperative verbs for instructions

### Formatting

- Use sentence casing for headings
- Use code font for symbols, commands, file paths, and URLs
- Use bold for UI elements users click
- Use hyphens (-) for unordered lists

### Avoid

- "Simply", "just", "easy" (can be condescending)
- Vague phrases like "click here"
- Semicolons (use periods instead)
- "We" unless clearly referring to Apollo

## Reference Files

For Apollo GraphQL-specific guidance:

- [Apollo Skills](references/apollo-skills.md) - Patterns and examples for Apollo GraphQL skills

## Versioning

Use semantic versioning (`"X.Y.Z"`) for the `version` field in metadata:

```yaml
metadata:
  author: apollographql
  version: "1.0.0"
```

- **Major (X)**: Breaking changes that alter how the skill behaves or activates (e.g., renamed triggers, removed sections, changed ground rules)
- **Minor (Y)**: New content or capabilities that are backward-compatible (e.g., added reference files, new sections, expanded examples)
- **Patch (Z)**: Small fixes that don't change behavior (e.g., typo corrections, wording tweaks, formatting fixes)

Start new skills at `"1.0.0"`.

## Checklist for New Skills

Before publishing a skill, verify:

- [ ] `name` matches directory name and follows naming rules
- [ ] `description` clearly states what the skill does and when to use it
- [ ] `SKILL.md` is under 500 lines
- [ ] Reference files are focused and under 300 lines each
- [ ] Instructions are clear and actionable
- [ ] Code examples are correct and tested
- [ ] Ground rules use ALWAYS/NEVER/PREFER format
- [ ] Content follows Apollo Voice guidelines

## Ground Rules

- ALWAYS include trigger conditions in the description (use numbered list)
- ALWAYS use checkboxes for multi-step processes
- ALWAYS link to reference files for detailed documentation
- NEVER exceed 500 lines in SKILL.md
- NEVER use vague descriptions that don't help agents identify when to activate
- PREFER specific examples over abstract explanations
- PREFER opinionated guidance over listing multiple options
- USE `allowed-tools` to pre-approve tools the skill needs
- NEVER include `Bash(curl:*)` in `allowed-tools` as it grants unrestricted network access and enables `curl | sh` remote code execution patterns
