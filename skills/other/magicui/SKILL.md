---
name: magicui
description: Use for Magic UI React components, animations, text effects, buttons, backgrounds, device mocks. Includes bento-grid, marquee, globe, animated buttons, shimmer effects, particle backgrounds. 8 tools for beautiful UI components.
version: 1.0.0
title: "Magicui"
status: active
---

# Magic UI Skill

Magic UI component library for React. Get implementation details for animated components, text effects, special effects, buttons, backgrounds, and device mockups.

## Context Efficiency

Traditional MCP approach:
- All 8 tools loaded at startup
- Estimated context: 4000 tokens

This skill approach:
- Metadata only: ~100 tokens
- Full instructions (when used): ~5k tokens
- Tool execution: 0 tokens (runs externally)

## How This Works

Instead of loading all MCP tool definitions upfront, this skill:
1. Tells you what tools are available (just names and brief descriptions)
2. You decide which tool to call based on the user's request
3. Generate a JSON command to invoke the tool
4. The executor handles the actual MCP communication

## Available Tools

- `getUIComponents`: Provides a comprehensive list of all Magic UI components.
- `getComponents`: Provides implementation details for marquee, terminal, hero-video-dialog, bento-grid, animated-list, dock, globe, tweet-card, client-tweet-card, orbiting-circles, avatar-circles, icon-cloud, animated-circular-progress-bar, file-tree, code-comparison, script-copy-btn, scroll-progress, lens, pointer components.
- `getDeviceMocks`: Provides implementation details for safari, iphone-15-pro, android components.
- `getSpecialEffects`: Provides implementation details for animated-beam, border-beam, shine-border, magic-card, meteors, neon-gradient-card, confetti, particles, cool-mode, scratch-to-reveal components.
- `getAnimations`: Provides implementation details for blur-fade components.
- `getTextAnimations`: Provides implementation details for text-animate, line-shadow-text, aurora-text, number-ticker, animated-shiny-text, animated-gradient-text, text-reveal, hyper-text, word-rotate, typing-animation, scroll-based-velocity, flip-text, box-reveal, sparkles-text, morphing-text, spinning-text components.
- `getButtons`: Provides implementation details for rainbow-button, shimmer-button, shiny-button, interactive-hover-button, animated-subscribe-button, pulsating-button, ripple-button components.
- `getBackgrounds`: Provides implementation details for warp-background, flickering-grid, animated-grid-pattern, retro-grid, ripple, dot-pattern, grid-pattern, interactive-grid-pattern components.

## Usage Pattern

When the user's request matches this skill's capabilities:

**Step 1: Identify the right tool** from the list above

**Step 2: Generate a tool call** in this JSON format:

```json
{
  "tool": "tool_name",
  "arguments": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

**Step 3: Execute via bash:**

```bash
python .claude/skills/mcp-skills/executor.py --skill magicui --call 'YOUR_JSON_HERE'
```


## Getting Tool Details

If you need detailed information about a specific tool's parameters:

```bash
python .claude/skills/mcp-skills/executor.py --skill magicui --describe tool_name
```

This loads ONLY that tool's schema, not all tools.

## Examples

### Example 1: Simple tool call

User: "Get Magic UI button components"

Your workflow:
1. Identify tool: `getButtons`
2. Generate call JSON
3. Execute:

```bash
python .claude/skills/mcp-skills/executor.py --skill magicui --call '{"tool": "getButtons", "arguments": {}}'
```

### Example 2: Get tool details first

```bash
python .claude/skills/mcp-skills/executor.py --skill magicui --describe getTextAnimations
```

Returns the full schema, then you can generate the appropriate call.

## Error Handling

If the executor returns an error:
- Check the tool name is correct
- Verify required arguments are provided
- Ensure the MCP server is accessible

## Performance Notes

Context usage comparison for this skill:

| Scenario | MCP (preload) | Skill (dynamic) |
|----------|---------------|-----------------|
| Idle | 4000 tokens | 100 tokens |
| Active | 4000 tokens | 5k tokens |
| Executing | 4000 tokens | 0 tokens |

Savings: ~-25% reduction in typical usage

---

*This skill was auto-generated from an MCP server configuration.*
*Generator: mcp_to_skill.py*
