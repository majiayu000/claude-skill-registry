---
name: docs-skempken-plantuml-manipulator
description: This tool includes a Claude Code skill that enables Claude to automatically
  use the tool for batch PlantUML operations.
---

# Claude Code Skill Integration

This tool includes a Claude Code skill that enables Claude to automatically use the tool for batch PlantUML operations.

## What is a Claude Skill?

A **Claude Skill** is structured documentation that teaches Claude:
- When to use a specific tool
- How the tool works
- Best practices for usage

When properly configured, Claude will automatically recognize when to use this tool instead of manual editing.

## Installation

### For Claude Code CLI

1. **Create skill directory:**
   ```bash
   mkdir -p ~/.claude/skills/plantuml-manipulator
   ```

2. **Copy skill files:**
   ```bash
   cp -r docs/skill/* ~/.claude/skills/plantuml-manipulator/
   ```

   Or create a symlink (recommended for development):
   ```bash
   ln -s $(pwd)/docs/skill ~/.claude/skills/plantuml-manipulator
   ```

3. **Verify installation:**
   ```bash
   ls -la ~/.claude/skills/
   # You should see plantuml-manipulator/
   ```

## Skill Files

```
docs/skill/
├── SKILL.md        # Main documentation for Claude
└── README.md       # Installation guide (this file)
```

### SKILL.md

This is the main file that Claude reads. It contains:
- When to use this tool
- How to use each command
- Workflows and best practices
- Error handling

## How Claude Uses the Skill

When you ask Claude to make repetitive PlantUML changes, it will:

1. **Recognize the pattern**: "This is a batch operation on PlantUML files"
2. **Load the skill**: Read SKILL.md for instructions
3. **Create snippet** (if needed)
4. **Run dry-run**: Show you what would happen
5. **Execute**: Upon your approval, make the changes
6. **Validate**: Check that changes were successful
7. **Report**: Summarize what was done

### Example Interaction

```
You: "Add a validation step to all process diagrams"

Claude: "I'll use the PlantUML Manipulator tool for this batch operation.

         First, let me create a snippet for the validation step..."

         [Creates snippets/validation.puml]

         "Now I'll run a dry-run to show what would happen..."

         [Runs: plantuml-manipulator insert-after --dry-run ...]

         "The tool would modify 8 files. Shall I proceed?"

You: "Yes, go ahead"

Claude: [Runs without --dry-run]

        "✓ Successfully added validation to 8 process diagrams:
         - user_login.puml
         - payment_process.puml
         ...

         Validation passed: all files now contain the validation step."
```

## When Claude Uses the Tool

Claude will automatically use this tool when you request:

### Batch Operations
- "Add X to all process diagrams"
- "Insert validation in multiple files"
- "Update all diagrams with new participant"

### Validation
- "Check if all diagrams have X"
- "Validate consistency across diagrams"
- "Report missing structures"

### Reporting
- "List all groups in the diagrams"
- "Show me which participants are used"
- "What's the structure of diagram X?"

## When Claude Won't Use the Tool

Claude will use normal editing for:
- Single file changes
- Complex contextual modifications
- 1-2 simple edits

The tool is specifically for **repetitive, structural operations**.

## Customizing the Skill

You can customize the skill for your project:

### Add Project-Specific Workflows

Edit `~/.claude/skills/plantuml-manipulator/SKILL.md`:

```markdown
## Project-Specific Workflows

### Add Payment Validation
All payment processes must include validation:

\```bash
plantuml-manipulator insert-after \
  --pattern "payment/*.puml" \
  --after-group "Process Payment" \
  --block-file snippets/payment-validation.puml \
  --only-if-has-participant "PaymentService"
\```
```

### Add Custom Validation Rules

```markdown
## Custom Validations

### Payment Processes
All payment processes must have:
- "Validate Payment" group
- "PaymentService" participant
- "AuditLog" participant

\```bash
plantuml-manipulator validate \
  --pattern "payment/*.puml" \
  --require-group "Validate Payment" \
  --require-participant "PaymentService" \
  --require-participant "AuditLog"
\```
```

## Without the Skill

If the skill is not installed, Claude will:
- Use normal Read/Edit tools
- Process files individually
- Take longer
- Be more error-prone

The skill makes Claude **significantly more efficient** at batch operations.

## Troubleshooting

### Claude doesn't use the tool

**Check installation:**
```bash
ls ~/.claude/skills/plantuml-manipulator/SKILL.md
```

**Verify tool is available:**
```bash
which plantuml-manipulator
# or
python -m plantuml_manipulator --help
```

### Skill not loading

Claude loads skills at startup. If you updated the skill:
1. The changes are effective immediately (no reload needed)
2. Ensure SKILL.md has valid YAML frontmatter

### Tool errors

Check the tool documentation:
```bash
plantuml-manipulator --help
plantuml-manipulator insert-after --help
```

## Advanced Usage

### Multiple Projects

You can create project-specific variants:

```bash
# Copy and customize for project
cp -r ~/.claude/skills/plantuml-manipulator \
      ~/.claude/skills/plantuml-manipulator-projectx

# Edit project-specific workflows
code ~/.claude/skills/plantuml-manipulator-projectx/SKILL.md
```

### Development Mode

For tool development:

```bash
# Symlink for live updates
ln -s $(pwd)/docs/skill ~/.claude/skills/plantuml-manipulator-dev

# Test changes immediately
```

## Further Reading

- [Specification](specification.md) - Technical details
- [API Reference](api-reference.md) - Complete command reference
- [Claude Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
