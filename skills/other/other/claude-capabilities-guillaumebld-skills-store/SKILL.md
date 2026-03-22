---
name: claude-capabilities
description: >
  Current Claude AI and Claude Code capabilities, features, and limits.
  Consult before making claims about what Claude can or cannot do, what
  features exist, model availability, pricing, or environment differences.
  Use when answering "can Claude do X?", comparing Claude AI vs Code,
  checking current model specs, or advising on which environment suits a task.
---

# Claude Capabilities Reference

Claude's training data goes stale within weeks of major releases. This skill provides a current reference for Claude AI (web/app) and Claude Code (terminal/IDE) capabilities. Consult these references before making claims about features, limits, or availability.

## Quick Comparison

| Capability | Claude AI | Claude Code |
|-----------|-----------|-------------|
| File system | Container sandbox (`/mnt/user-data/outputs/`) | Full local filesystem |
| Shell access | None | Bash tool |
| Skills location | Settings > Capabilities (zip upload) | `~/.claude/skills/` or `.claude/skills/` |
| MCP connection | UI connectors | `claude mcp add` / settings.json |
| Subagents | None | Explore, Plan, custom agents, Agent Teams |
| Artifacts | HTML, React, Mermaid, SVG, MD (render inline) | Not available |
| Interactive Apps | Slack, Canva, Figma, Box + 5 more | Not available |
| Web search | Built-in with citations | WebSearch tool |
| File creation | DOCX, PPTX, XLSX, PDF, code files | Any file via Write tool |
| Memory | Cross-conversation (automatic) | CLAUDE.md hierarchy + rules/ |
| Conversation search | `conversation_search` tool (internal) | Not available |
| Git integration | Not available | Full git access |
| Deployment | Not available | wrangler, vercel, etc. |

## Reference Files

| Question | Read |
|----------|------|
| What can Claude AI do? Features, limits, container | [references/claude-ai.md](references/claude-ai.md) |
| What can Claude Code do? Agent Teams, Cowork, hooks | [references/claude-code.md](references/claude-code.md) |
| Model names, pricing, context windows | [references/models.md](references/models.md) |
| What changed recently? New features by date | [references/changelog.md](references/changelog.md) |

## Maintenance

Each reference file has a "Last verified" date at the top. When information seems wrong or outdated:

1. Check the reference files first — they override training data for recent features
2. If a reference file's "Last verified" date is more than 4 weeks old, flag it to the user
3. Use web search to verify uncertain claims before stating them as fact
