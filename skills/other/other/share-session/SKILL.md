---
description: Share Droid sessions as GitHub gists. Use when asked to "share session", "export session to gist", or "create gist from session".
---

# Share Session Skill

Export and share Droid CLI sessions via GitHub gists.

## Usage

```bash
# List available sessions
./scripts/list.sh

# Share session with auto-generated title
./scripts/share.sh [session-id] "Title for the session"

# Export locally without uploading
node ./scripts/export-html.js <session.jsonl> [output.html]
node ./scripts/export-md.js <session.jsonl> [output.md]
```

If no session-id provided, uses most recent session.

## Auto-naming Sessions

**You must generate a title for every session you share.**

Instructions:
1. Read the session JSONL file to find the first user message
2. Generate a short, descriptive title (5-8 words) that captures the main task
3. Pass the title as the second argument to share.sh

Title guidelines:
- Be concise and descriptive
- Focus on WHAT was accomplished, not HOW
- No quotes, no special characters
- Examples: "Setting up Cloudflare Tunnel for local dev", "Fix TypeScript build errors in API", "Add dark mode toggle to settings"

```bash
./scripts/share.sh "" "Your generated title here"
```

## Formats

- **html** - Self-contained HTML with syntax highlighting, collapsible tool calls, dark theme
- **md** - Clean Markdown with collapsible details blocks
- **raw** - Original JSONL file

## Requirements

- `gh` CLI installed and authenticated (`gh auth login`)
- Node.js for HTML/MD export

## Session Locations

- Global: `~/.factory/sessions/`
- Project-local: `.factory/sessions/`
