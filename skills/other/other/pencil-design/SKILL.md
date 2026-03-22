---
name: pencil-design
description: >
  MANDATORY for ALL .pen file and Pencil MCP operations. The main agent must NEVER call any
  mcp__pencil__* tool directly — all Pencil work MUST go through this skill which delegates
  to a subagent. This prevents Pencil MCP's massive outputs from flooding the main context window.
  Triggers: any mention of .pen files, Pencil editor, "design in Pencil", "open pen file",
  "edit the design", "update the pen file", "screenshot the design", "check the layout",
  batch_get, batch_design, get_screenshot, snapshot_layout, get_editor_state, open_document,
  get_variables, set_variables, or ANY request that would touch the Pencil MCP server.
  CRITICAL: If you are tempted to call mcp__pencil__* directly, STOP and use this skill instead.
---

# Pencil Design Agent

## ABSOLUTE RULE — NO EXCEPTIONS

**The main agent (you) must NEVER directly call any `mcp__pencil__*` tool.** Not even once. Not
even to "quickly check" something. Not even `get_editor_state`. Every single Pencil MCP
interaction goes through a subagent via the Agent tool. This is non-negotiable — Pencil MCP
outputs are enormous and will destroy the main conversation's context window.

If you find yourself about to call `mcp__pencil__*` directly: **STOP. Spawn a subagent instead.**

## How It Works

When the user requests any .pen file work, you MUST:

1. **Spawn an Agent** (subagent) with a clear, detailed prompt describing the design task
2. The subagent has access to all Pencil MCP tools and will do the actual work
3. The subagent returns a **concise summary** of what it did (under 300 words)
4. You relay that summary to the user — this is all that enters the main context

## Subagent Prompt Template

When spawning the subagent, include ALL of the following in the prompt:

```
You are a Pencil design specialist working with .pen files via the Pencil MCP server.

## Your Task
{describe the user's request in detail}

## Available Pencil MCP Tools
You have access to these tools (use ToolSearch to load them first):
- mcp__pencil__get_editor_state - Check current editor state (start here)
- mcp__pencil__open_document - Open a .pen file or create new one
- mcp__pencil__get_guidelines - Get design guidelines for a topic
- mcp__pencil__get_style_guide_tags - Get available style guide tags
- mcp__pencil__get_style_guide - Get a style guide by tags or name
- mcp__pencil__batch_get - Read nodes by pattern or ID
- mcp__pencil__batch_design - Insert/copy/update/replace/move/delete nodes
- mcp__pencil__snapshot_layout - Check computed layout rectangles
- mcp__pencil__get_screenshot - Take a screenshot of a node
- mcp__pencil__get_variables - Get current variables and themes
- mcp__pencil__set_variables - Add or update variables
- mcp__pencil__find_empty_space_on_canvas - Find empty space for new content
- mcp__pencil__search_all_unique_properties - Search unique properties in node tree
- mcp__pencil__replace_all_matching_properties - Replace matching properties in node tree

## Critical Rules
1. ALWAYS start by calling get_editor_state to understand current context
2. Use ToolSearch with "select:mcp__pencil__<tool_name>" to load each tool before first use
3. Contents of .pen files are encrypted - ONLY use Pencil MCP tools, never Read/Grep
4. When designing, use get_guidelines and get_style_guide for best results
5. Use get_screenshot periodically to validate your design visually
6. Keep batch_design operations to max 25 per call
7. After completing work, use get_screenshot to capture the final result

## Response Format
Return a concise summary (under 300 words) containing:
- What you did (actions taken)
- Current state of the design
- Any issues or decisions that need user input
- If you took screenshots, mention what they show
```

## When to Use This Skill

This skill MUST be triggered for ANY of these scenarios:
- User mentions .pen files
- User asks to create, edit, or view a design in Pencil
- User asks to open the Pencil editor
- User wants to update variables, styles, or nodes in a .pen file
- User asks for a screenshot or layout check of a .pen design
- Any task that would require calling mcp__pencil__* tools

## Important Notes

- **Never call Pencil MCP tools directly** from the main conversation - always delegate to a subagent
- If the task is complex (multiple screens, full app design), break it into multiple subagent calls
- The subagent should use `get_screenshot` at the end so the user can see the result
- If the subagent needs user input (e.g., design choices), relay the question back to the user and spawn a new subagent (or resume the previous one) with their answer
- You can resume a previous subagent using its agent ID if follow-up work is needed on the same design
