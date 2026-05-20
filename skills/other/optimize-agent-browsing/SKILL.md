---
name: optimize-agent-browsing
description: Analyze an OpenClaw agent's browser usage and recommend browsy migration
---

# Optimize Agent Browsing

Analyze an OpenClaw agent's browser tool usage patterns and identify which calls can be migrated from Playwright/CDP to browsy for faster, lighter execution.

## Usage

```
/optimize-agent-browsing path/to/agent-config.yaml
```

## What it does

Reviews how an agent uses browser tools and produces a migration plan:

- **Usage audit** — scans agent configuration, tool definitions, and execution logs for browser-related tool calls (`browser`, `web_browser`, `playwright_browser`, `browse_web`)
- **Pattern classification** — categorizes each browser usage into one of five patterns:
  - **Simple navigation** (read-only page fetching) — direct browsy replacement
  - **Form interaction** (login, search, data entry) — browsy handles natively
  - **Data extraction** (tables, lists, structured content) — browsy `tables`/`find` tools
  - **JS-heavy SPA** (React/Vue rendering required) — keep Playwright
  - **Screenshot/visual** (pixel-level inspection needed) — keep Playwright
- **Tool mapping** — for each migratable call, provides the exact browsy tool equivalent
- **Performance estimate** — projects speed improvement (typically 10x) and memory savings (typically 60x) based on the migration ratio

## Workflow

1. Read agent configuration file and tool registrations
2. Scan for browser tool calls in agent code/prompts
3. Classify each call into the 5 patterns above
4. For migratable patterns, map to browsy equivalents:
   - `browser.navigate(url)` → `browsy_browse`
   - `browser.click(selector)` → `browsy_click` (by element ID instead of CSS selector)
   - `browser.type(selector, text)` → `browsy_type_text`
   - `browser.get_text(selector)` → `browsy_find`
   - `browser.screenshot()` → keep Playwright (browsy has no pixel rendering)
5. Generate migration checklist

## Example output

```
=== Agent Browser Usage Analysis ===

Agent: research-assistant
Browser tool calls found: 12

=== Classification ===

| # | Call                          | Pattern         | Migratable |
|---|-------------------------------|-----------------|------------|
| 1 | browser.navigate(url)         | Navigation      | YES        |
| 2 | browser.get_text("h1")        | Data extraction | YES        |
| 3 | browser.get_text(".results")  | Data extraction | YES        |
| 4 | browser.click(".next")        | Navigation      | YES        |
| 5 | browser.navigate(url)         | Navigation      | YES        |
| 6 | browser.get_table("table")    | Data extraction | YES        |
| 7 | browser.screenshot()          | Visual          | NO         |
| 8 | browser.navigate(url)         | Navigation      | YES        |
| 9 | browser.type("#search", q)    | Form input      | YES        |
|10 | browser.click("#submit")      | Form submit     | YES        |
|11 | browser.wait_for(".loaded")   | JS-heavy SPA    | NO         |
|12 | browser.navigate(url)         | Navigation      | YES        |

=== Summary ===

Migratable: 10/12 calls (83%)
Keep Playwright: 2/12 calls (screenshot, JS wait)

=== Estimated Impact ===

                   Before (Playwright)    After (browsy)
Avg page load:     2.8s                   0.3s
Memory per page:   ~300MB                 ~5MB
Total speedup:     ~10x for migratable calls

=== Migration Checklist ===

- [ ] Install openclaw-browsy plugin
- [ ] Set preferBrowsy: true in plugin config
- [ ] Replace browser.get_text() calls with browsy_find
- [ ] Replace browser.get_table() calls with browsy_tables
- [ ] Keep browser.screenshot() on Playwright (no browsy equivalent)
- [ ] Keep browser.wait_for() on Playwright (JS rendering needed)
- [ ] Test migrated flows with /test-browsy-flow
```

## Requirements

- Agent configuration file or source code accessible in the workspace
- `openclaw-browsy` plugin available for migration target
