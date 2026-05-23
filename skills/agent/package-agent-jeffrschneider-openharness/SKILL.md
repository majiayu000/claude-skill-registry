---
name: package-agent
description: Generate a complete OAF-compliant agent package from an Agent Case (requirements) and Agent Design (architecture). Use when asked to "package an agent", "generate an agent package", "create an agent from a design", or when you have both case/ and design/ folders and need to create the package/ folder with AGENTS.md, skills, and scripts.
---

# Package Agent

Generate a complete Open Agent Format (OAF) package from an Agent Case and Agent Design.

## Workflow

1. **Read inputs** - Load the case/README.md and design/README.md
2. **Generate AGENTS.md** - Create the main agent manifest
3. **Generate skills** - Create SKILL.md and resources for each skill in the design
4. **Generate scripts** - Create Python script stubs for each script in the design
5. **Verify structure** - Ensure all files are created correctly

## Step 1: Read Inputs

The user will provide paths to:
- `case/README.md` - Agent Case with Description, Example Session, Deliverables
- `design/README.md` - Agent Design with sub-agents, skills, scripts, MCPs, memory, tools

Read both files to understand what to generate.

## Step 2: Generate AGENTS.md

Create `package/AGENTS.md` with this structure:

```markdown
---
name: [from design identity]
slug: [from design identity]
version: [from design identity]
description: [from design identity]
tags: [from design identity]
license: MIT
---

# [Agent Name]

[Architecture overview paragraph from design section 2]

## Sub-Agents

[For each sub-agent in design section 3, create a subsection:]

### [sub-agent-name]

**Role:** [role from design]
**Tools:** [tools list]

Tasks:
- [delegated task 1]
- [delegated task 2]

## Skills

This agent uses the following skills:

| Skill | Purpose |
|-------|---------|
| [skill-name] | [purpose from design] |

## MCP Servers

[For each MCP in design section 6:]

### [mcp-name]

- **Purpose:** [description]
- **Protocol:** [protocol]
- **Auth:** [auth type]
- **Tools:** [list enabled tools]

## Memory

| Label | Purpose | Retention |
|-------|---------|-----------|
| [label] | [purpose] | [retention] |

## Tools

**Allowed:** [list from design]
**Denied:** [list from design]

## Error Handling

| Failure | Detection | Recovery |
|---------|-----------|----------|
[from design section 10]
```

## Step 3: Generate Skills

For each skill in design section 4, create:

```
package/skills/[skill-name]/
├── SKILL.md
├── resources/
│   └── [any templates mentioned]
└── scripts/
    └── [any scripts assigned to this skill]
```

### SKILL.md Template

```markdown
---
name: [skill-name]
description: [purpose from design]. Triggers when [infer trigger from purpose].
---

# [Skill Name]

## Overview

[Expand on purpose - what knowledge/procedures this skill provides]

## Usage

[Describe when and how the agent uses this skill]

## Resources

[List any files in resources/ and what they contain]

## Scripts

[List any scripts and their purpose]
```

### Resource Files

Create stub resource files based on what the design mentions:
- For templates: Create a markdown file with placeholder structure
- For reference docs: Create a markdown file with section headers

## Step 4: Generate Scripts

For each script in design section 5:

1. Determine which skill folder it belongs to (from the `path` in design)
2. Create the Python script with:
   - Docstring explaining purpose, inputs, outputs
   - Function signature matching the design
   - Basic implementation structure with TODOs
   - Dependencies noted in requirements comment

### Script Template

```python
#!/usr/bin/env python3
"""
[Script name] - [purpose from design]

Inputs:
  [list inputs from design]

Outputs:
  [list outputs from design]

Dependencies:
  [list from design]
"""

# Requirements: [dependencies]

import json
from typing import Any


def main([parameters from design inputs]) -> dict[str, Any]:
    """
    [Purpose from design]

    Args:
        [param]: [description inferred from design]

    Returns:
        dict with keys: [output keys from design]
    """
    # TODO: Implement [purpose]

    return {
        # [output structure from design]
    }


if __name__ == "__main__":
    import sys
    # TODO: Parse command line args
    result = main()
    print(json.dumps(result, indent=2))
```

## Step 5: Verify Structure

After generating all files, verify the package structure:

```
package/
├── AGENTS.md              # Main agent manifest
└── skills/
    ├── [skill-1]/
    │   ├── SKILL.md
    │   ├── resources/
    │   │   └── [templates/docs]
    │   └── scripts/
    │       └── [any scripts]
    ├── [skill-2]/
    │   └── ...
    └── ...
```

Print a summary of what was created.

## Example Invocation

```
User: Package the travel research agent. The case is in examples/travel-research/case/ and design is in examples/travel-research/design/

Claude: [Reads both files, then creates:]
- examples/travel-research/package/AGENTS.md
- examples/travel-research/package/skills/travel-planning/SKILL.md
- examples/travel-research/package/skills/travel-planning/resources/itinerary-template.md
- examples/travel-research/package/skills/travel-planning/scripts/budget-calculator.py
- [etc.]
```

## References

- See `references/oaf-structure.md` for detailed OAF package format
- See `references/agents-md-schema.md` for AGENTS.md field reference
