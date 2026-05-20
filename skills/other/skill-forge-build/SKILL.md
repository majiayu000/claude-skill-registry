---
name: skill-forge-build
description: >
  Scaffold and build Claude Code skills from plans or descriptions. Generates
  SKILL.md files, sub-skills, scripts, references, agents, and templates
  following the Agent Skills standard. Use when user says "build skill",
  "scaffold skill", "generate skill", "create SKILL.md", or "implement skill".
---

# Skill Builder — Scaffold & Generate

## Process

### Step 1: Gather Inputs

Determine what we're building from:
- **Plan document**: Output from `/skill-forge plan` (preferred)
- **Description**: Natural language description of the skill
- **Existing skill**: Path to a skill to use as foundation

If no plan exists, run a quick planning pass (ask 3 key questions):
1. What does the skill do? (1-2 sentences)
2. What commands should it have? (list)
3. Does it need scripts or external tools? (yes/no)

### Step 2: Generate Frontmatter

The most critical step. The description field determines activation.

**Framework for writing descriptions:**

```
[Capability statement] + [Detailed capabilities] + [Trigger phrases]
```

**Rules:**
- Under 1024 characters total
- No XML angle brackets (< >)
- Include 5-10 trigger phrases users would say
- Mention file types if relevant
- Add negative triggers if risk of over-triggering

**Use `references/description-guide.md` for the full framework.**

### Step 3: Write Main SKILL.md

Structure the body following this template:

```markdown
# [Skill Name] -- [Tagline]

[1-2 sentence overview]

## Quick Reference

| Command | What it does |
|---------|-------------|
| /name cmd1 | Description |
| /name cmd2 | Description |

## Orchestration Logic

[How commands route to sub-skills]
[Decision trees for conditional routing]

## [Domain-Specific Section]

[Core rules, thresholds, quality gates]

## Reference Files

[List of on-demand reference files]

## Sub-Skills

[List of sub-skills with one-line descriptions]
```

**Critical SKILL.md rules:**
- Under 500 lines
- Under 5000 tokens
- Actionable instructions (not vague)
- Include error handling
- Link references, don't inline them

### Step 4: Generate Sub-Skills (Tier 3-4)

For each sub-skill, generate a SKILL.md with:

```yaml
---
name: parent-child
description: >
  [What it does]. Use when user says "[trigger 1]", "[trigger 2]",
  "[trigger 3]", or "[trigger 4]".
---
```

**Sub-skill body guidelines:**
- Self-contained instructions for ONE workflow
- Cross-reference other sub-skills by name (not inline their content)
- Reference shared files in the parent skill's `references/` directory
- Include explicit input/output definitions

### Step 5: Generate Scripts (Tier 2-4)

For each script:

```python
#!/usr/bin/env python3
"""
Purpose: [What this script does]
Input: [Expected input format]
Output: [Expected output format]
Usage: python scripts/script_name.py [args]
"""

import argparse
import json
import sys
from typing import Any


def main(args: argparse.Namespace) -> dict[str, Any]:
    """Main execution function."""
    # Validate inputs
    # Do the work
    # Return structured output
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="[Script description]")
    parser.add_argument("input", help="[Input description]")
    parser.add_argument("--output", "-o", help="Output file path")
    args = parser.parse_args()

    try:
        result = main(args)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
```

**Script rules:**
- One script, one responsibility
- CLI interface with argparse
- Structured JSON output
- Clear error messages
- No dependencies beyond stdlib when possible

### Step 6: Generate Reference Files

For each reference file:
- Focus on ONE topic
- Under 200 lines
- Include concrete examples
- Use tables for thresholds and specifications
- Mark with "Load on-demand" in parent SKILL.md

### Step 7: Generate Agent Definitions (Tier 4)

Agent files use YAML frontmatter (different from skills):

```markdown
---
name: [skill-name]-[role]
description: >
  [What this agent analyzes].
  <example>User says: "[trigger]"</example>
model: inherit
color: blue
tools:
  - Read
  - Grep
  - Glob
---

You are a [role] specialist.

## Your Role
[What this agent does]

## Process
1. [Steps...]

## Output Format
Return structured markdown with findings and recommendations.
```

**Key differences from skills:** Agent `name` is 3-50 chars, descriptions CAN use
`<example>` blocks, agent-only fields include `tools`, `color`, `permissionMode`,
`maxTurns`, `memory`. Body becomes the system prompt (second person).

### Step 8: Generate Install Script

Create `install.sh` that copies files to `~/.claude/skills/` and `~/.claude/agents/`.

### Step 9: Validate

Run `python scripts/validate_skill.py <path>` on the generated skill.
Check all quality gates from the main SKILL.md.

### Step 10: Output Summary

Present the user with:
1. Generated file tree
2. Key files and their purposes
3. Installation instructions
4. Suggested test queries (3 that should trigger, 3 that should NOT)
5. Next steps (test, iterate, publish)

## Scaffolding Command

For quick scaffolding, use:
```bash
python scripts/init_skill.py <skill-name> --tier <1-4> --path <output-path>
```

This creates the full directory structure with placeholder content.
