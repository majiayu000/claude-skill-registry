# Task tracker connectors

Task trackers are the single most important signal for automation audits after ActivityWatch. Where AW shows what the user IS doing, the tracker shows what they are *trying* to do — the backlog, the priorities, the recurring items that come up week after week. A recurring task that appears in someone's ClickUp every Monday is the textbook definition of "automate me."

FlowHunt supports several task trackers via MCP or native connectors. The intake question in `setup.md` Step 1c asks the user which one they use and records it. This file is the branch-per-tracker instructions.

## Supported trackers and their paths

| Tracker | Claude Code | Codex | Gemini CLI | OpenCode | Source-of-truth |
|---|---|---|---|---|---|
| **Linear** | native at `https://claude.ai/settings/connectors` | ChatGPT apps at `https://chatgpt.com/apps` | `gemini mcp add linear http https://mcp.linear.app/sse -t sse` | add Linear MCP block to `opencode.json` | `https://mcp.linear.app/` |
| **Notion** | native connector at `https://claude.ai/settings/connectors` | ChatGPT apps at `https://chatgpt.com/apps` (Notion connector ships with ChatGPT) | `gemini mcp add notion ...` via Notion official MCP | Notion official MCP in `opencode.json` | `https://developers.notion.com/docs/mcp` |
| **Jira / Confluence** | native Atlassian connector at `https://claude.ai/settings/connectors` | Atlassian Rovo MCP via ChatGPT apps | `gemini mcp add atlassian ...` via Rovo | Rovo MCP in `opencode.json` | `https://www.atlassian.com/platform/remote-mcp-server` |
| **Asana** | native connector at `https://claude.ai/settings/connectors` | ChatGPT apps if Asana enabled | community MCP, check `github.com/modelcontextprotocol/servers` | same MCP in `opencode.json` | verify source at install time |
| **ClickUp** | no native connector — use community MCP via `npx skills add` or manual MCP config | same | same | same | verify latest active repo — this space churns |
| **Todoist** | no native connector — community MCP | same | same | same | verify latest active repo |
| **Trello** | no native connector — community MCP (low priority, Trello use is declining) | same | same | same | verify source |

**Important rule (same as Slack/Gmail):** do not invent MCP URLs or package names. Before you (the agent) instruct the user to paste a snippet, confirm the repo/URL exists. If the user is on Claude Code, prefer the native connector at `https://claude.ai/settings/connectors` over any community MCP — one click, OAuth'd, maintained by Anthropic, no GCP/API-keys dance.

## Detection flow (per agent)

### Claude Code / Claude Desktop

Before asking the user to install anything, check if they already have a task-tracker MCP loaded. Look at your available tools for anything matching `mcp__claude_ai_Linear__*`, `mcp__claude_ai_Notion__*`, `mcp__claude_ai_Atlassian__*`, `mcp__claude_ai_Asana__*`. If present, the user already connected at `claude.ai/settings/connectors` — skip install, skip straight to verify.

If not present, ask the user to visit `https://claude.ai/settings/connectors`, pick the tracker they use, click Connect. Wait for confirmation, then verify by making a list-projects or list-workspaces tool call.

### Codex

Codex reuses ChatGPT apps via the same OAuth flow. If the user signed into Codex with ChatGPT Plus, open `https://chatgpt.com/apps` in their browser and ask them to enable the matching app (Linear, Notion, Atlassian). Verify by running the agent's tool listing inside Codex and looking for tracker-related tools.

### Gemini CLI

Use `gemini mcp add`. Linear has a first-party remote MCP at `https://mcp.linear.app/sse` (SSE transport). Notion publishes `github.com/makenotion/notion-mcp-server` — install via `gemini mcp add notion stdio -- npx -y @notionhq/notion-mcp-server`. Atlassian Rovo is the official path for Jira/Confluence — follow `https://www.atlassian.com/platform/remote-mcp-server` docs for the current install command (it changes as Rovo evolves).

### OpenCode

Add the MCP block to `~/.config/opencode/opencode.json` under the `mcp` key. Same structure as Slack/Gmail — pick `"type": "remote"` for URL-based MCPs, `"type": "local"` with `command` for stdio MCPs. Tell the user to edit the file themselves, show them the exact block to paste.

## Fallback: user pastes tasks manually

If the user says "I don't use any of those trackers" or "I use Notes / a text file / paper", do NOT skip this connector. Instead, ask:

> "OK, zero trackera — też działa. Wkleić tutaj listę zadań które teraz próbujesz pchać (z notatnika, maila, gdziekolwiek)? Audit przeczyta to jako twoje priorytety i podniesie rangę rekomendacji dotyczących tych tematów. Format dowolny: bullets, numerki, luzem — ja sobie poradzę."

Take whatever the user pastes and write it to `~/.flowhunt/tasks.md` verbatim. If the file already exists, overwrite (setup is idempotent — a new setup run refreshes the task list). If the user pastes nothing, write an empty `~/.flowhunt/tasks.md` so audit.md knows it was offered and declined.

The audit procedure will read `~/.flowhunt/tasks.md` if it exists and treat its content as **second-highest priority input** (after live tracker data if present, before ActivityWatch patterns).

## What FlowHunt audit reads from a task tracker

During audit, the agent calls the tracker's MCP to collect:

- Active/open tasks assigned to the user, with titles, descriptions, due dates, and project/space names
- Recently completed tasks in the last 30 days (same fields)
- Recurring tasks if the tracker exposes them (most do — look for `recurrence` or `due.recurring` fields)
- Task comments the user wrote in the last 30 days, if the tracker returns them via list APIs (don't make extra per-task fetches, too expensive)

Content, not just titles. A task called "weekly report" with a description starting "Compile metrics from 4 dashboards and write 2 paragraphs" is 10x more actionable than just the title. For the top 20 most-repeated task patterns (same title recurring weekly, or variations like "client X monthly check-in"), include the full description.

Do NOT read private/archived workspaces unless the user explicitly asked. Respect the tracker's own privacy scoping.
