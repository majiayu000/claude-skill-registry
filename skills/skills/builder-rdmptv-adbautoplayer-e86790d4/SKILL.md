---
name: builder:generate-skill
description: "Generate new skill with SKILL.md structure and proper integration"
argument-hint: "[skill-name] [description]"
allowed-tools:
  - Task
  - AskUserQuestion
  - Read
model: haiku
skills: moai-foundation-core, builder-workflow, moai-foundation-claude
---

## Pre-execution Context

!git status --porcelain
!git branch --show-current

## Essential Files

@.moai/config/config.json

---

# Generate Skill

> **Architecture**: Commands → Agents → Skills. This command orchestrates through `Task()` tool.
> **Delegation Model**: Skill creation delegated to `builder-skill` agent.

**Workflow Integration**: Creates new skills with proper SKILL.md structure and MoAI integration.

---

## Command Purpose

Generate complete skill structure with:
- SKILL.md with YAML frontmatter
- scripts/ directory (optional)
- Proper naming convention
- Color coding (yellow for custom)
- Integration with agent ecosystem

**Run on**: `$ARGUMENTS` (skill-name [description])

**Variables**:
- `$1`: Skill name (e.g., moai-connector-slack)
- `$2+`: Optional description

---

## Execution Philosophy

`/builder:generate-skill` creates skills through agent delegation:

```
User Command: /builder:generate-skill [name] [description]
    ↓
Phase 1: Validate skill name format
    ↓
Phase 2: Determine skill tier
    ↓
Phase 3: Task(subagent_type="builder-skill")
    → Create directory structure
    → Generate SKILL.md
    → Configure integration
    ↓
Output: Complete skill structure
```

---

## Associated Agents & Skills

| Agent/Skill | Purpose |
|------------|---------|
| builder-skill | Skill structure creation |
| moai-foundation-claude | Claude Code skill standards |
| moai-foundation-core | MoAI integration patterns |

---

## PHASE 1: Skill Name Validation

**Goal**: Ensure skill name follows conventions

### Step 1.1: Parse Arguments

```python
args = $ARGUMENTS.split(maxsplit=1)
skill_name = args[0] if len(args) > 0 else None
description = args[1] if len(args) > 1 else None
```

### Step 1.2: Validate Name Format

Skill names should follow pattern: `{category}-{domain}` or `{prefix}-{category}-{domain}`

Valid prefixes:
- `moai-` - MoAI ecosystem skills
- `builder-` - Builder ecosystem skills
- No prefix - General skills

### Step 1.3: Clarify Requirements

```python
AskUserQuestion({
    "questions": [{
        "question": "What type of skill are you creating?",
        "header": "Skill Category",
        "multiSelect": false,
        "options": [
            {
                "label": "Foundation",
                "description": "Core framework skill (moai-foundation-*)"
            },
            {
                "label": "Connector",
                "description": "External service integration (moai-connector-*)"
            },
            {
                "label": "Library",
                "description": "Utility library skill (moai-library-*)"
            },
            {
                "label": "Workflow",
                "description": "Process automation skill (moai-workflow-*)"
            }
        ]
    }]
})
```

---

## PHASE 2: Skill Tier Assessment

**Goal**: Determine appropriate skill tier

### Skill Tiers

| Tier | Complexity | Scripts | Use Case |
|------|------------|---------|----------|
| 1 | Minimal | 0 | Documentation only |
| 2 | Basic | 1-3 | Simple automation |
| 3 | Standard | 4-10 | Full feature set |
| 4 | Enterprise | 10+ | Complex workflows |

---

## PHASE 3: Skill Generation

**Goal**: Create complete skill structure

### Step 3.1: Delegate to builder-skill

```yaml
Tool: Task
Parameters:
- subagent_type: "builder-skill"
- description: "Generate new skill structure"
- prompt: """You are the builder-skill agent creating a new skill.

**Task**: Create complete skill with SKILL.md and directory structure.

**Context**:
- Skill Name: {skill_name}
- Description: {description}
- Conversation Language: {{CONVERSATION_LANGUAGE}}

**Directory Structure**:
```
.claude/skills/{skill_name}/
├── SKILL.md
├── scripts/           # Optional
│   └── (scripts here)
└── modules/           # Optional
    └── (submodules here)
```

**SKILL.md Template**:
```yaml
---
name: {skill_name}
description: {description}
version: 1.0.0
modularized: false
scripts_enabled: false
last_updated: {today}
auto_trigger_keywords:
  - {keyword1}
  - {keyword2}
color: yellow
---

---

## Quick Reference (30 seconds)

**{Skill Title}**

**What It Does**: {Brief description}

**Core Capabilities**:
- Capability 1
- Capability 2

**When to Use**:
- Use case 1
- Use case 2

---

## Detailed Documentation

[Full skill documentation here]

---

**Version**: 1.0.0
**Status**: Active
**Last Updated**: {today}
```

**Requirements**:
1. Create directory structure
2. Generate SKILL.md with proper frontmatter
3. Set color to yellow (custom)
4. Add auto_trigger_keywords based on skill domain
5. Include Quick Reference section

**Output**:
- Skill directory at: .claude/skills/{skill_name}/
- SKILL.md with YAML frontmatter
- Ready for script addition via /builder:generate-script
"""
```

---

## Summary: Execution Checklist

- [ ] **Name Validated**: Follows naming convention
- [ ] **Tier Determined**: Appropriate complexity level
- [ ] **Agent Delegated**: builder-skill invoked
- [ ] **Directory Created**: .claude/skills/{skill-name}/
- [ ] **SKILL.md Generated**: With proper frontmatter
- [ ] **Color Set**: Yellow for custom skills

---

## Quick Reference

| Scenario | Command | Expected Outcome |
|----------|---------|------------------|
| Connector skill | `/builder:generate-skill moai-connector-slack "Slack MCP integration"` | Slack connector skill |
| Library skill | `/builder:generate-skill moai-library-redis "Redis caching patterns"` | Redis library skill |
| Workflow skill | `/builder:generate-skill moai-workflow-deploy "Deployment automation"` | Deploy workflow skill |

**Output Location**: `.claude/skills/{skill-name}/`

---

## Final Step: Next Action Selection

```python
AskUserQuestion({
    "questions": [{
        "question": "Skill created successfully. What would you like to do next?",
        "header": "Next Steps",
        "multiSelect": false,
        "options": [
            {
                "label": "Add Scripts",
                "description": "Run /builder:generate-script to add UV scripts"
            },
            {
                "label": "Create Another Skill",
                "description": "Generate another skill"
            },
            {
                "label": "View SKILL.md",
                "description": "Display generated skill documentation"
            },
            {
                "label": "Continue Development",
                "description": "Return to main workflow"
            }
        ]
    }]
})
```

---

## EXECUTION DIRECTIVE

**You must NOW execute the command following the "Execution Philosophy" described above.**

1. Parse `$ARGUMENTS` to extract skill-name and description.
2. Validate skill name follows conventions.
3. Determine skill tier based on requirements.
4. Call the `Task` tool with `subagent_type="builder-skill"`.
5. Verify skill creation.
6. Offer next step options.

**Version**: 1.0.0
**Last Updated**: 2025-12-01
