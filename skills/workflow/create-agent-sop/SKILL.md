---
name: create-agent-sop
description: Create agent-ready Standard Operating Procedure (SOP) skills that autonomous agents can execute deterministically. Use when creating workflow skills, procedural skills, or any skill that needs to be unambiguous, idempotent, robust, and observable. Triggers on "create SOP", "new workflow skill", "agent-ready procedure".
---

# Create Agent SOP

Meta-skill for generating SOP skills that autonomous agents can execute without human intervention.

## When to Use

- Creating workflow skills (e.g., feature-development-loop, weekly-review)
- Procedural skills with clear start/end states
- Skills requiring deterministic, repeatable execution

## Process

### 1. Gather Requirements

Ask user for:
- **Workflow name** (hyphen-case, e.g., `feature-development-loop`)
- **Trigger phrases** (when should this SOP activate?)
- **Steps** (what are the major phases?)
- **Success criteria** (how do we know it's done?)

### 2. Initialize Skill

```bash
pnpm exec tsx .claude/skills/create-agent-sop/scripts/init_sop_skill.ts <name> --path .claude/skills
```

### 3. Write SKILL.md

Follow the template in `references/sop-template.md`. Key sections:

```markdown
---
name: <skill-name>
description: <what + when to use>
---

# <Skill Name>

## Prerequisites
[Tools, permissions, state requirements]

## Input Schema
[Typed parameters with defaults]

## Procedure
[Numbered steps with @command tags]

## Success Criteria
[Verification checks]

## Error Recovery
[Fallback paths]
```

### 4. Add Tools (Optional)

Before adding scripts, evaluate if the functionality should be a **CLI tool** instead:

| Consider CLI Tool When | Use Script When |
|------------------------|-----------------|
| Multiple clients could use it | Skill-specific logic only |
| Reusable across skills | Simple validation/checks |
| Complex logic worth maintaining | Glue code between tools |
| Would simplify the script significantly | One-off operations |

**CLI tools** go in `packages/cli/` and are invoked via `sp` or tool-specific commands.
Skills can then call these tools, keeping scripts minimal.

**Scripts** go in `scripts/` for skill-specific operations:

```bash
scripts/validate.sh      # Prerequisite checks
scripts/check-state.ts   # Skill-specific state validation
```

### 5. Validate

Run the validation script to check against the 10 SOP characteristics:

```bash
pnpm exec tsx .claude/skills/create-agent-sop/scripts/validate_sop_skill.ts <skill-path>
```

Output shows pass/fail for each characteristic. See `references/sop-characteristics.md` for details.

### 6. Package

Create a distributable `.skill` file:

```bash
pnpm exec tsx .claude/skills/create-agent-sop/scripts/package_sop_skill.ts <skill-path> [output-dir]
```

Validates first, then creates `<skill-name>.skill` (zip format).

## References

- `references/sop-characteristics.md` - The 10 characteristics explained
- `references/sop-template.md` - SKILL.md template for SOPs
