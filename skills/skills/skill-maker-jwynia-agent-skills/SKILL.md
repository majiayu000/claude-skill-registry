---
name: skill-maker
description: Guide agents through creating skills that follow the agentskills.io specification. This skill should be used when the user asks to "create a skill", "make a new skill", "scaffold a skill", "help with skill structure", "write a SKILL.md", "skill frontmatter", or needs help with progressive disclosure, skill validation, or skill best practices.
license: MIT
compatibility: Requires Deno for scaffold scripts. Works with any agentskills.io-compatible agent.
metadata:
  author: agent-skills
  version: "1.0"
---

# Skill Maker

Create skills that follow the agentskills.io specification. This skill provides a structured workflow for gathering requirements, scaffolding the skill structure, and validating the result.

A skill is a directory containing a `SKILL.md` file with YAML frontmatter and Markdown instructions. Skills extend agent capabilities with specialized knowledge, workflows, and bundled resources.

## Skill Creation Workflow

Follow these four phases in order:

### Phase 1: Requirements Gathering

Before writing any code, understand what the skill needs to do. Use the interactive questions in the next section to gather:
- The task or workflow the skill enables
- Concrete usage examples (what users will say)
- Required resources (scripts, references, assets)
- Trigger phrases for the description

### Phase 2: Planning

With requirements gathered, plan the skill structure:

1. Choose a name (lowercase, hyphens, max 64 chars, matches folder)
2. Draft the description (what + when + keywords, max 1024 chars)
3. Decide which optional directories are needed:
   - `scripts/` - Executable code for repetitive/deterministic tasks
   - `references/` - Documentation loaded as needed
   - `assets/` - Templates, images, data files for output
4. Outline the SKILL.md body sections

Use `assets/planning-template.md` for structured planning.

### Phase 3: Scaffolding

Create the skill structure using the scaffold script:

```bash
deno run --allow-write --allow-read scripts/scaffold.ts \
  --name "my-skill" \
  --description "What this skill does and when to use it." \
  --path "./skills/domain/" \
  --with-scripts \
  --with-references
```

This creates:
```
my-skill/
├── SKILL.md           # Starter template with frontmatter
├── scripts/           # If --with-scripts
└── references/        # If --with-references
```

Then edit the generated SKILL.md to add instructions.

### Phase 4: Validation

Validate the completed skill:

```bash
deno run --allow-read --allow-run scripts/validate-skill.ts ./path/to/skill
```

The validator checks:
- Frontmatter validity (name, description constraints)
- Name matches directory name
- Line count (warns if >500 lines)
- Referenced files exist
- Description includes trigger phrases

Fix any issues and re-validate.

## Quick Start

To create a minimal skill immediately:

1. Create the directory: `mkdir -p skills/domain/my-skill`
2. Copy the template: `cp assets/skill-md-template.md skills/domain/my-skill/SKILL.md`
3. Edit the SKILL.md frontmatter and body
4. Validate: `deno run --allow-read --allow-run scripts/validate-skill.ts ./skills/domain/my-skill`

## Interactive Requirements Gathering

When a user requests a new skill, ask these questions:

### Understanding the Task
- "What task or workflow should this skill enable?"
- "Can you give 2-3 concrete examples of how this skill would be used?"
- "What would a user say that should trigger this skill?"

### Identifying Resources
- "Will this skill need executable scripts for repetitive tasks?"
- "Is there reference documentation the skill should include?"
- "Are there templates or assets the skill needs to produce output?"

### Defining Scope
- "What should this skill NOT handle? (Out of scope)"
- "Are there related skills this should connect to?"

### Drafting the Description
Based on gathered information, draft a description following this pattern:
> "[What the skill does]. This skill should be used when the user asks to [trigger phrase 1], [trigger phrase 2], [trigger phrase 3], or [scenario]. Keywords: [relevant terms]."

## Key Principles

### Progressive Disclosure

Structure skills for efficient context usage:

| Level | Content | Size |
|-------|---------|------|
| Metadata | name + description | ~100 tokens (always loaded) |
| Instructions | SKILL.md body | <5000 tokens (loaded on activation) |
| Resources | scripts/, references/, assets/ | As needed |

Keep SKILL.md under 500 lines. Move detailed content to `references/`.

### Strong Trigger Descriptions

Write descriptions in third person with specific phrases:

```yaml
# Good
description: "This skill should be used when the user asks to 'create a PDF',
  'extract text from PDF', 'merge PDFs', or mentions PDF processing."

# Bad
description: "Helps with PDFs."
```

### Imperative Writing Style

Write instructions in imperative form, not second person:

```markdown
# Good
Run the validation script before committing changes.
Configure the API key in the environment.

# Bad
You should run the validation script.
You need to configure the API key.
```

## Scripts Reference

### scaffold.ts

Creates skill folder structure and starter files.

```bash
deno run --allow-write --allow-read scripts/scaffold.ts \
  --name "skill-name" \
  --description "Description text" \
  --path "./target/directory/" \
  [--with-scripts] [--with-references] [--with-assets]
```

**Options**:
- `--name` (required): Skill name (validated for format)
- `--description` (required): Initial description
- `--path` (required): Parent directory for the skill
- `--with-scripts`: Create scripts/ directory
- `--with-references`: Create references/ directory
- `--with-assets`: Create assets/ directory

### validate-skill.ts

Validates a skill against the agentskills.io specification.

```bash
deno run --allow-read --allow-run scripts/validate-skill.ts ./path/to/skill
```

Performs checks beyond the basic spec:
- Calls `skills-ref validate` if available
- Warns on large files (>500 lines)
- Checks for referenced file existence
- Detects second-person language patterns

## Additional Resources

### Reference Files

For detailed guidance, consult:
- **`references/spec-quick-reference.md`** - Condensed agentskills.io specification
- **`references/progressive-disclosure.md`** - Content organization strategies
- **`references/examples-gallery.md`** - Annotated examples of well-structured skills

### Asset Files

Templates for skill creation:
- **`assets/skill-md-template.md`** - Complete SKILL.md starter template
- **`assets/planning-template.md`** - Requirements gathering worksheet

### External Resources

- [agentskills.io specification](https://agentskills.io/specification)
- [skills-ref validation tool](https://github.com/agentskills/agentskills/tree/main/skills-ref)
