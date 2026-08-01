---
name: langchain-agent
description: This document explains the custom GitHub Copilot skill created for LangChain
  agent development in this project.
---

# GitHub Copilot Custom Skills

This document explains the custom GitHub Copilot skill created for LangChain agent development in this project.

## Overview

GitHub Copilot supports **custom skills** - project-specific knowledge files that help Copilot understand domain patterns, conventions, and workflows. When you ask Copilot questions matching a skill's description, it automatically loads the skill content as context.

---

## What We Added

### Skill: `langchain-agent-development`

| Property | Value |
|----------|-------|
| **Name** | `langchain-agent-development` |
| **Location** | `.github/skills/langchain-agent-development/` |
| **Purpose** | Guide Copilot on LangChain ReAct agent patterns specific to this project |

### Directory Structure

```
.github/skills/langchain-agent-development/
├── SKILL.md                              # Main skill file (required)
└── checklists/
    ├── new_tool_checklist.md             # Step-by-step for adding tools
    └── add_semantic_route_checklist.md   # Step-by-step for adding routes
```

### File Descriptions

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill with YAML frontmatter + content. Copilot reads this when triggered. |
| `new_tool_checklist.md` | Actionable checklist for creating new CachingTool implementations |
| `add_semantic_route_checklist.md` | Actionable checklist for adding semantic router routes |

---

## Skill File Format

### Required Structure

Every skill must have a `SKILL.md` file with YAML frontmatter:

```markdown
---
name: skill-name-here
description: Description of when to use this skill (max 1024 chars)
---

# Skill Title

Content here...
```

### Frontmatter Rules

| Field | Requirements |
|-------|--------------|
| `name` | Lowercase with hyphens, max 64 characters |
| `description` | Plain text, max 1024 characters. Describes when Copilot should use this skill |

### Our Skill's Frontmatter

```yaml
---
name: langchain-agent-development
description: Build LangChain ReAct agents with tools, caching, and semantic routing for this stock investment assistant. Use for creating new tools, extending agent capabilities, adding semantic routes, debugging LangGraph issues, and following project patterns (CachingTool, ToolRegistry, AgentResponse).
---
```

---

## How to Create New Skills

### Step 1: Create Directory

```powershell
mkdir .github/skills/<skill-name>
```

### Step 2: Create SKILL.md

Create `.github/skills/<skill-name>/SKILL.md` with:

```markdown
---
name: my-skill-name
description: When to use this skill - be specific about triggers
---

# My Skill

## Overview
What this skill covers...

## Patterns
Code patterns, conventions...

## Quick Reference
Common lookups...
```

### Step 3: Add Supporting Files (Optional)

Add checklists, examples, or templates in subdirectories:

```
.github/skills/my-skill/
├── SKILL.md
├── checklists/
│   └── workflow_checklist.md
└── examples/
    └── example_code.py
```

### Step 4: Reference in Main Skill

Link to supporting files from SKILL.md:

```markdown
## Checklists
- [Workflow Checklist](checklists/workflow_checklist.md)
```

---

## How to Use Skills

### Automatic Triggering

Copilot automatically loads skills when your question matches the skill description. For our skill, these queries trigger it:

- "How do I create a new LangChain tool?"
- "Add a semantic route for portfolio analysis"
- "Debug my agent's tool execution"
- "What's the CachingTool pattern in this project?"

### Manual Invocation

You can explicitly reference the skill in Copilot Chat:

```
@workspace Use the langchain-agent-development skill to help me create a new tool
```

Or reference the skill file directly:

```
@workspace #file:.github/skills/langchain-agent-development/SKILL.md How do I add caching?
```

### Verification

To verify Copilot loaded the skill, check if responses include:
- Project-specific patterns (CachingTool, ToolRegistry, AgentResponse)
- File paths from your project (`src/core/tools/base.py`)
- Pattern names from the skill content

---

## Skill Content Summary

Our `langchain-agent-development` skill covers:

### 1. Creating New Tools
- Extending `CachingTool` base class
- Implementing `_execute()` method
- Registering with `ToolRegistry`
- Testing patterns

### 2. Agent Configuration
- ReAct agent setup with `create_react_agent`
- System prompt patterns
- AgentExecutor configuration

### 3. Semantic Routing
- `StockQueryRoute` enum values
- Adding utterances for training
- Router configuration

### 4. Response Types
- `AgentResponse` frozen dataclass
- Success, error, and fallback patterns

### 5. LangGraph Studio Integration
- `langgraph.json` configuration
- Debugging with Studio
- Tracing execution

### 6. Troubleshooting
- Common issues table
- Debug checklist

---

## Updating the Skill

### When to Update

Update the skill when:
- Adding new tool patterns
- Changing agent architecture
- Adding new route categories
- Discovering common debugging issues

### How to Update

1. Edit `.github/skills/langchain-agent-development/SKILL.md`
2. Update the "Last Updated" date at bottom
3. Increment version if significant changes
4. Add new checklists to `checklists/` directory if needed

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-01-12 | Initial skill with tools, routing, responses, LangGraph Studio |

---

## References

- **Skill Location**: [.github/skills/langchain-agent-development/SKILL.md](../../.github/skills/langchain-agent-development/SKILL.md)
- **Tool Checklist**: [new_tool_checklist.md](../../.github/skills/langchain-agent-development/checklists/new_tool_checklist.md)
- **Route Checklist**: [add_semantic_route_checklist.md](../../.github/skills/langchain-agent-development/checklists/add_semantic_route_checklist.md)
- **Backend Instructions**: [backend-python.instructions.md](../../.github/instructions/backend-python.instructions.md)
- **VS Code Copilot Docs**: [Custom Instructions](https://code.visualstudio.com/docs/copilot/copilot-customization)
