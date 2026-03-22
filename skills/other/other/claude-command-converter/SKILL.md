---
name: claude-command-converter
description: Convert Claude Code commands (.claude/commands/*.md) to standard Agent Skills (skills/*/SKILL.md). Use when migrating slash commands to portable skill format, creating skills from existing commands, or standardizing command definitions across AI runtimes.
---

# Claude Command Converter

Convert Claude Code commands to standard Agent Skills format for portability across AI coding assistants.

## When to Use

- Migrating existing `.claude/commands/*.md` files to `skills/*/SKILL.md` format.
- Creating portable skills from Claude Code-specific commands.
- Standardizing command definitions for use with Claude Code, Codex CLI, GitHub Copilot, and other runtimes.

## Inputs

- Source command file path (e.g., `.claude/commands/my-command.md`).
- Optional: target skill name (defaults to command filename without extension).

If input is missing, ask for the source command file path.

## Format Differences

### Claude Code Command Format

Location: `.claude/commands/<command-name>.md`

```yaml
---
description: Short description of the command
handoffs:
  - label: Next Action
    agent: other.command
    prompt: Trigger prompt
    send: true
---
## User Input

\`\`\`text
$ARGUMENTS
\`\`\`

[Command instructions...]
```

### Standard Agent Skill Format

Location: `skills/<skill-name>/SKILL.md`

```yaml
---
name: skill-name
description: Complete description including what the skill does and when to use it.
---

# Skill Title

## When to Use

- Scenario 1
- Scenario 2

## Inputs

- Required input 1
- Optional input 2

## Workflow

1. Step 1
2. Step 2
...

## Outputs

- Output file 1
- Output file 2
```

## Conversion Workflow

1. **Read the source command** from `.claude/commands/`.

2. **Extract metadata**:
   - `description` from YAML frontmatter.
   - `handoffs` for related skills/next steps.
   - `$ARGUMENTS` handling for inputs.

3. **Determine skill name**:
   - Convert `command.name.md` → `command-name` (replace dots with hyphens).
   - Use kebab-case for multi-word names.

4. **Create skill directory**: `skills/<skill-name>/`

5. **Transform content** to SKILL.md format:
   - **Frontmatter**: Keep `name` and `description` only.
   - **Enhance description**: Expand to include when to use the skill.
   - **Convert `$ARGUMENTS`**: Document as Inputs section.
   - **Structure workflow**: Extract steps into numbered Workflow section.
   - **Add "When to Use"**: Derive from command context and description.
   - **Add "Outputs"**: List generated files/artifacts.
   - **Convert handoffs**: Add "Next Steps" section referencing related skills.

6. **Remove runtime-specific content**:
   - Remove `## User Input` section with `$ARGUMENTS` block.
   - Remove `handoffs` from frontmatter (move to prose).
   - Remove `/command.name` references (use skill names instead).

7. **Validate skill structure**:
   - Frontmatter has `name` and `description` only.
   - Body has clear sections (When to Use, Inputs, Workflow, Outputs).
   - No TODO placeholders remain.
   - No runtime-specific variables like `$ARGUMENTS`.

8. **Report conversion result**:
   - Source command path.
   - Generated skill path.
   - Key transformations applied.
   - Manual review recommendations.

## Transformation Rules

| Claude Command                | Agent Skill                                   |
| ----------------------------- | --------------------------------------------- |
| `$ARGUMENTS`                  | Inputs section describing expected user input |
| `handoffs:`                   | Next Steps section with skill references      |
| `/command.name`               | `skill-name` (kebab-case)                     |
| `agent: foo.bar`              | `foo-bar` skill reference                     |
| `description:` in frontmatter | `description:` expanded with triggers         |
| Inline `## User Input`        | Removed; documented in Inputs                 |

## Example Conversion

**Input**: `.claude/commands/speckit.specify.md`

```yaml
---
description: Create feature specification from natural language.
handoffs:
  - label: Build Technical Plan
    agent: speckit.plan
---
## User Input

\`\`\`text
$ARGUMENTS
\`\`\`

The text the user typed after `/speckit.specify`...
```

**Output**: `skills/speckit-specify/SKILL.md`

```yaml
---
name: speckit-specify
description: Create or update a feature specification from a natural language feature description.
---

# Spec Kit Specify Skill

## When to Use

- The user wants a new or updated feature spec from a natural language description.

## Inputs

- Feature description from the user.
- Repo context with `.specify/` scripts and templates.

If the description is missing or unclear, ask a targeted question before continuing.

## Workflow

...

## Outputs

- `specs/<feature>/spec.md`
- `specs/<feature>/checklists/requirements.md`

## Next Steps

After generating spec.md:

- **Plan** technical implementation with speckit-plan.
- **Clarify** specification requirements with speckit-clarify.
```

## Key Rules

- Preserve all workflow logic and instructions.
- Remove runtime-specific constructs (`$ARGUMENTS`, `handoffs`, `/slash-commands`).
- Expand terse descriptions to include usage triggers.
- Use imperative voice in workflow steps.
- Keep skills self-contained and portable.
- Don't add extraneous documentation files (README, CHANGELOG, etc.).

## Next Steps

After conversion:

- Review generated SKILL.md for completeness.
- Delete unused example files in `scripts/`, `references/`, `assets/`.
- Update AGENTS.md/CLAUDE.md skill inventory if applicable.
- Create symlinks for runtime integration if needed.
