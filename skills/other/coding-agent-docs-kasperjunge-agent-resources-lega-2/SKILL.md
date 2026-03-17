---
name: coding-agent-docs
description: Stay current with how OpenCode, OpenAI Codex, and Claude Code implement extensibility features (skills, slash commands, subagents, custom prompts). Use when comparing implementations across AI coding assistants, researching how a specific tool implements a feature, or syncing knowledge about agent extensibility patterns. Triggers include questions like "how does X implement skills?", "compare slash commands across tools", "what's the latest on Claude Code sub-agents?", or requests to understand agent extensibility approaches.
---

# AI Coding Agent Documentation Sync

Track and compare extensibility features across OpenCode, Codex, and Claude Code.

## Quick Reference

See [references/documentation-urls.md](references/documentation-urls.md) for all documentation URLs organized by tool and feature type.

## Workflows

### Fetch Current Documentation

1. Read `references/documentation-urls.md` to get relevant URLs
2. Use WebFetch for each URL with a targeted prompt:
   - For overview: "Summarize the main concepts and how this feature works"
   - For comparison: "Extract the key configuration options, file structure, and capabilities"
   - For implementation details: "List the required files, syntax, and examples"

### Compare Implementations Across Tools

1. Identify the concept to compare (skills, commands, agents)
2. Fetch documentation from each tool using the feature mapping table
3. Structure comparison around:
   - **Triggering**: How is the feature invoked?
   - **Structure**: What files/config are required?
   - **Capabilities**: What can it do?
   - **Limitations**: What constraints exist?

### Research Specific Feature

1. Identify which tool(s) to research
2. Fetch the relevant documentation URL(s)
3. Extract:
   - Core concepts and terminology
   - Required file structure
   - Configuration options
   - Example implementations

## Concept Mapping

| Concept | OpenCode | Codex | Claude Code |
|---------|----------|-------|-------------|
| Reusable workflows | Skills | Skills, Custom Prompts | Skills |
| User commands | Commands | - | Slash Commands |
| Autonomous tasks | Agents | - | Sub-agents |

## Important Notes

- Documentation URLs may change; verify links still work before relying on them
- Each tool uses different terminology for similar concepts
- Features evolve rapidly; always fetch current docs rather than relying on cached knowledge
