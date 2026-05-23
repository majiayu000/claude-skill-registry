---
name: oe-mcp-bootstrap
description: Setup and verification for MCP tooling used in OpenEvent-AI (filesystem, Context7 docs, LSP/Pyright, Playwright). Use when onboarding a new developer/agent or when Codex/Claude cannot access LSP, browser automation, or docs.
---

# oe-mcp-bootstrap

## Codex CLI (recommended MCP set)

Add servers (examples; adjust versions as needed):

- Filesystem:
  - `codex mcp add filesystem --env npm_config_cache=/tmp/codex-npm-cache -- npx -y @modelcontextprotocol/server-filesystem@2025.12.18 .`

- Context7 (docs):
  - `codex mcp add context7 --env npm_config_cache=/tmp/codex-npm-cache -- npx -y @upstash/context7-mcp@1.0.33 --transport stdio`
  - Ensure `CONTEXT7_API_KEY` is set in your shell and allowed by `shell_environment_policy`.

- LSP (Pyright via LSP bridge):
  - Generate an LSP config JSON that points to your local repo path:
    - `python3 .codex/skills/oe-mcp-bootstrap/scripts/generate_lsp_config.py --out .codex/lsp.json --repo-root .` (or the same script under `.claude/skills/oe-mcp-bootstrap/`)
  - Add the server (example uses @axivo/mcp-lsp):
    - `codex mcp add lsp --env npm_config_cache=/tmp/codex-npm-cache --env LSP_FILE_PATH=/abs/path/to/lsp.json -- npx -y @axivo/mcp-lsp@1.0.5`

- Playwright (browser automation):
  - `codex mcp add playwright --env npm_config_cache=/tmp/codex-npm-cache -- npx -y @playwright/mcp@0.0.53`

- Web search (optional; vetted):
  - Kindly web search MCP server (Python). Requires local Chromium plus a search provider (Serper/Tavily/SearXNG). Optional `GITHUB_TOKEN` improves GitHub Issues content fetch. Use only after code review and least-privilege keys.

Verify:
- `codex mcp list --json`

## Optional MCPs for maintenance & bug triage

- GitHub MCP (issues/PRs). Use read-only or least-privilege tokens.
- Sentry MCP (prod error triage). Use separate dev/prod tokens.
- Semgrep MCP (security findings).
- Supabase MCP (DB/auth/edge functions). Prefer read-only credentials for debugging.

## Optional MCPs for codebase analysis & refactors

- RepoMapper MCP (repo map + prototypes). Requires local clone.
- FileScopeMCP (dependency-based file ranking). Requires local clone + build.
- Renamify MCP (safe multi-file renames).
- fast-filesystem-mcp: do not enable while CVE-2025-67364 is unpatched.

## Security guardrails

- Prefer official or well-maintained servers; review third-party code before enabling.
- Reference servers are for dev/test only; do not assume production hardening.
- Avoid broad shell/exec or auto-install/remote-aggregator MCPs.
- Constrain Playwright MCP with allowlist/blocklist settings if available.

## Claude Code

Use the equivalent Claude Code MCP configuration for:
- filesystem
- context7
- LSP bridge (Pyright)
- Playwright
- optional web search and triage servers above

Keep secrets out of the repo; use env vars (`CONTEXT7_API_KEY`, etc.).

## Gemini CLI

Use the same MCP set if your Gemini tooling supports MCP. Keep secrets out of the repo.
