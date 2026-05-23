---
name: export-skills
description: Export SpecWeave skills to Agent Skills open standard format (agentskills.io) for cross-platform portability. Use when converting skills to GitHub Copilot, VS Code, Gemini CLI, or Cursor format. Creates portable SKILL.md files compatible with any Agent Skills-supported tool.
visibility: public
allowed-tools: Read, Write, Glob, Bash
---

# Export Skills to Agent Skills Standard

## Overview

Export SpecWeave skills to the [Agent Skills](https://agentskills.io) open standard format. This enables skill portability across:

- **GitHub Copilot** (VS Code integration)
- **Gemini CLI**
- **Cursor**
- **Claude Code**
- Other Agent Skills-compatible tools

## Usage

```
/sw:export-skills [options]
```

### Options

| Option | Description |
|--------|-------------|
| `--output <dir>` | Output directory (default: `.agent-skills/`) |
| `--plugin <name>` | Export specific plugin (default: all) |
| `--skill <name>` | Export specific skill (default: all) |
| `--dry-run` | Preview without writing files |
| `--validate` | Validate output against Agent Skills spec |

## Output Structure

```
.agent-skills/
├── architect/
│   └── SKILL.md
├── security/
│   └── SKILL.md
├── qa-lead/
│   └── SKILL.md
└── pm/
    └── SKILL.md
```

## Field Mapping

| SpecWeave Field | Agent Skills Field | Notes |
|-----------------|-------------------|-------|
| `name` | `name` | Direct mapping |
| `description` | `description` | Direct mapping (max 1024 chars) |
| `allowed-tools` | `allowed-tools` | Convert comma to space-delimited |
| N/A | `license` | Add `Apache-2.0` by default |
| N/A | `compatibility` | Add `"Designed for Claude Code"` |
| N/A | `metadata.author` | Use plugin manifest author |
| N/A | `metadata.source` | Add `"SpecWeave"` |
| `visibility` | (not mapped) | Agent Skills uses file placement |
| `invocableBy` | (not mapped) | Agent Skills discovery is implicit |

## Execution Steps

### Step 1: Discover Skills

```bash
# Find all SKILL.md files in plugins
find plugins -name "SKILL.md" -type f
```

### Step 2: Convert Each Skill

For each SKILL.md:

1. Parse YAML frontmatter
2. Extract description (truncate to 1024 chars if needed)
3. Convert `allowed-tools` from comma to space-delimited
4. Generate Agent Skills-compliant frontmatter
5. Preserve markdown body content

### Step 3: Validate Output

Each exported skill must:
- Have `name` matching directory name
- Have `description` between 1-1024 characters
- Have `name` using only `a-z` and `-`
- Not have `--` in name
- Not start/end with `-`

### Step 4: Write Files

Write to output directory with structure:
```
{output}/{skill-name}/SKILL.md
```

## Conversion Script

```typescript
interface SpecWeaveSkill {
  name: string;
  description: string;
  'allowed-tools'?: string;
  visibility?: string;
  invocableBy?: string[];
  context?: string;
  model?: string;
}

interface AgentSkill {
  name: string;
  description: string;
  license?: string;
  compatibility?: string;
  metadata?: Record<string, string>;
  'allowed-tools'?: string;
}

function convertSkill(specweave: SpecWeaveSkill, pluginName: string): AgentSkill {
  return {
    name: specweave.name,
    description: specweave.description.slice(0, 1024),
    license: 'Apache-2.0',
    compatibility: 'Designed for Claude Code (or similar products)',
    metadata: {
      author: 'specweave',
      source: 'SpecWeave',
      plugin: pluginName
    },
    'allowed-tools': specweave['allowed-tools']?.replace(/,\s*/g, ' ')
  };
}
```

## Example Output

Input (`plugins/specweave/skills/architect/SKILL.md`):
```yaml
---
name: architect
description: System Architect expert...
allowed-tools: Read, Write, Edit
context: fork
model: opus
---
```

Output (`.agent-skills/architect/SKILL.md`):
```yaml
---
name: architect
description: System Architect expert...
license: Apache-2.0
compatibility: Designed for Claude Code (or similar products)
metadata:
  author: specweave
  source: SpecWeave
  plugin: sw
allowed-tools: Read Write Edit
---
```

## Post-Export Actions

After exporting:

1. **Commit to repo**: Skills can be discovered from any subdirectory
2. **Push to GitHub**: Enable Copilot skill discovery
3. **Publish**: Consider publishing to skill registries

## Limitations

- SpecWeave-specific fields (`context`, `model`, `invocableBy`) are not exported
- Progressive disclosure phases (sub-files) are not included
- Skill memory files are not exported (they're runtime state)

## Project-Specific Learnings

**Before starting work, check for project-specific learnings:**

```bash
# Check if skill memory exists for this skill
cat .specweave/skill-memories/export-skills.md 2>/dev/null || echo "No project learnings yet"
```

Project learnings are automatically captured by the reflection system when corrections or patterns are identified during development. These learnings help you understand project-specific conventions and past decisions.

