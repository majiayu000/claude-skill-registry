---
name: stitch-setup
description: Step-by-step installer for the stitch-kit plugin and Stitch MCP server. Use this when setting up the plugin for the first time, diagnosing connection issues, or helping a new user get Stitch running in Claude Code or Codex CLI.
allowed-tools:
  - "Bash"
  - "Read"
  - "Write"
---

# stitch-kit Setup Guide

Walks users through two setup tasks:
1. **Stitch MCP Server** — connect your AI client to Google Stitch's remote generation API
2. **stitch-kit Plugin** — install the skills that orchestrate the Stitch workflow

---

## When to use this skill

- User says "how do I set this up", "it's not working", "Stitch isn't available"
- Agent can't find Stitch MCP tools after running `list_tools`
- First-time setup in a new environment

---

## Step 1: Verify what's already installed

Run `list_tools` (or check the tool list). Look for any of:
- `create_project`
- `generate_screen_from_text`
- `get_screen`

**If found:** Stitch MCP is working. Skip to Step 4 (plugin install).
**If not found:** Continue with MCP setup below.

---

## Step 2: Get a Stitch API Key

Stitch MCP is a **remote HTTP server** — it lives in the cloud at `stitch.googleapis.com`, not on your machine. It requires an API key to authenticate.

1. Go to [stitch.withgoogle.com/settings](https://stitch.withgoogle.com/settings)
2. Scroll to the **API Keys** section
3. Click **"Create API Key"**
4. Copy the key — you'll need it in the next step

> **Never commit your API key to a public repository.** Store it securely.

---

## Step 3: Configure Stitch MCP

### Claude Code

Using the CLI (recommended):

```bash
claude mcp add stitch --transport http https://stitch.googleapis.com/mcp \
  --header "X-Goog-Api-Key: YOUR-API-KEY" -s user
```

Or add to `~/.claude/settings.json` manually:

```json
{
  "mcpServers": {
    "stitch": {
      "type": "http",
      "url": "https://stitch.googleapis.com/mcp",
      "headers": {
        "X-Goog-Api-Key": "YOUR-API-KEY"
      }
    }
  }
}
```

### Codex CLI

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.stitch]
url = "https://stitch.googleapis.com/mcp"

[mcp_servers.stitch.headers]
X-Goog-Api-Key = "YOUR-API-KEY"
```

### Cursor

Create or edit `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "stitch": {
      "url": "https://stitch.googleapis.com/mcp",
      "headers": {
        "X-Goog-Api-Key": "YOUR-API-KEY"
      }
    }
  }
}
```

### VS Code

Open Command Palette → "MCP: Add Server" → HTTP → `https://stitch.googleapis.com/mcp` → name: "stitch". Then edit the generated mcp.json to add the header:

```json
{
  "servers": {
    "stitch": {
      "url": "https://stitch.googleapis.com/mcp",
      "type": "http",
      "headers": {
        "Accept": "application/json",
        "X-Goog-Api-Key": "YOUR-API-KEY"
      }
    }
  }
}
```

### Quick install (all platforms)

Or use the NPX installer — it prompts for the API key and configures everything:

```bash
npx @booplex/stitch-kit
```

### Manual verification

After adding, restart the client and run `list_tools`. You should see tools like `create_project`, `generate_screen_from_text`, `get_screen`, etc.

---

## Step 4: Install stitch-kit plugin (Claude Code)

```bash
/plugin marketplace add https://github.com/gabelul/stitch-kit.git
/plugin install stitch-kit@stitch-kit
```

All 34 skills in one command. The `stitch-kit` agent is included — it shows up automatically after restart.

---

## Step 5: Verify the full setup

Run the orchestrator to confirm everything works:

```
"Use Stitch to design a simple login screen"
```

Expected behavior:
1. `stitch-orchestrator` activates
2. It runs `list_tools` and finds Stitch MCP tools
3. It generates a Design Spec
4. It creates a project via `create_project`
5. It generates a screen via `generate_screen_from_text`
6. It retrieves the screen via `get_screen`
7. It asks you which framework to convert to

If this completes, you're fully set up.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `list_tools` doesn't show Stitch tools | MCP not configured or client not restarted | Redo Step 3; restart your client |
| "Unauthenticated" or 401 error | API key invalid or expired | Generate a new key at stitch.withgoogle.com/settings |
| `create_project` fails with 403 | Account doesn't have Stitch access | Visit stitch.withgoogle.com and request access |
| `generate_screen_from_text` returns empty | Bad prompt or project ID format | Use `stitch-mcp-generate-screen-from-text` skill — it includes ID format rules |
| `get_screen` returns 404 | Wrong ID format | **projectId and screenId must be numeric only** — no `projects/` prefix |
| Generated HTML won't download | GCS URL expired or requires redirects | Use `bash scripts/fetch-stitch.sh "[url]" "temp/output.html"` |
| Plugin not activating | Wrong install command or repo URL | Verify you used `@stitch-kit` — not `@stitch-pro` or `@stitch-skills` |

---

## Network requirements

Stitch MCP makes outbound requests to:
- `stitch.googleapis.com` — remote MCP server
- `storage.googleapis.com` — file downloads (HTML, screenshots)
- `accounts.google.com` — OAuth (if using OAuth instead of API key)

If you're behind a corporate proxy or VPN, ensure these domains are allowed.

---

## Offline / no-MCP mode

If you cannot configure Stitch MCP, the orchestrator still works in **prompt-only mode**:
- Steps 1–3 run normally (spec generation, prompt assembly)
- Instead of generating the screen, it outputs a ready-to-copy Stitch prompt
- You paste that prompt at stitch.withgoogle.com manually
- Then you can still use the conversion skills on the downloaded HTML

---

## Authentication alternatives

### OAuth (for restricted environments)

If you can't store API keys on disk, Stitch supports OAuth via Google Cloud:

```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project YOUR-PROJECT-ID
gcloud beta services mcp enable stitch.googleapis.com --project=YOUR-PROJECT-ID
```

Then use Bearer token auth instead of API key. See [full OAuth guide](https://stitch.withgoogle.com/docs/mcp/setup).

> Note: OAuth tokens expire hourly and need manual refresh. API keys are simpler for most users.

---

## References

- Official Stitch MCP setup: https://stitch.withgoogle.com/docs/mcp/setup
- Plugin repo: https://github.com/gabelul/stitch-kit
- Skills index: `docs/skills-index.md`
- MCP tool reference: `docs/mcp-naming-convention.md`
