---
name: claude-code-statusline-development
description: This skill should be used when the user asks to "create a statusline", "customize the status line", "add a custom prompt", or mentions Claude Code statusline. Also suggest when the user wants to display git branch, context usage, model name, or session costs at the bottom of Claude Code.
---

# Claude Code Statusline Development

Create custom status lines that display contextual information at the bottom of Claude Code.

## Quick Reference

You MUST read the reference files for detailed schemas and examples:

- [JSON Schema](./references/json-schema.md) - Complete input structure documentation
- [Example: Simple](./references/example-simple.md) - Basic bash statusline
- [Example: Git-Aware](./references/example-git-aware.md) - Git branch and status
- [Example: Context Usage](./references/example-context-usage.md) - Context window percentage
- [Example: Cost Tracking](./references/example-cost-tracking.md) - Session costs and tokens

## Configuration

Add to `.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0
  }
}
```

## How It Works

- Status line updates when conversation messages change
- Updates run at most every 300ms
- First line of stdout becomes the status line text
- ANSI color codes supported
- JSON context passed via stdin

## JSON Input (Quick Reference)

| Field | Description |
|-------|-------------|
| `model.display_name` | Model name (e.g., "Opus") |
| `workspace.current_dir` | Current working directory |
| `workspace.project_dir` | Original project directory |
| `cost.total_cost_usd` | Session cost in USD |
| `cost.total_lines_added` | Lines added this session |
| `cost.total_lines_removed` | Lines removed this session |
| `context_window.context_window_size` | Max context tokens |
| `context_window.current_usage` | Current token usage object |

See [JSON Schema](./references/json-schema.md) for complete structure.

## Script Template

```bash
#!/bin/bash
input=$(cat)

# Extract values using jq
model=$(echo "$input" | jq -r '.model.display_name')
dir=$(echo "$input" | jq -r '.workspace.current_dir')

# Colors via tput
blue=$(tput setaf 4)
reset=$(tput sgr0)

echo "${blue}[$model]${reset} ${dir##*/}"
```

Make executable:

```bash
chmod +x ~/.claude/statusline.sh
```

## Tips

- Keep output concise - single line only
- Use `tput` for portable ANSI colors
- Test with mock JSON: `echo '{"model":{"display_name":"Test"}}' | ./statusline.sh`
- Cache expensive operations (git status) if needed

## Important

After creating or modifying statuslines, inform the user:

> **No restart needed.** Statusline changes take effect immediately - Claude Code reads settings fresh on each update.

## Attribution

Based on [Claude Code Status Line Configuration](https://code.claude.com/docs/en/statusline).
