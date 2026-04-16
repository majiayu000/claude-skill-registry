---
name: watch-upstream
description: Fetch official Anthropic/Claude Code docs, detect changes relevant to dotforge, report deltas.
---

# Watch Upstream

Detect changes in official Claude Code documentation that may require updates to dotforge.

## Step 0: Discover tools

WebFetch and WebSearch are deferred tools — they may not be loaded yet.
Run `ToolSearch("WebFetch WebSearch")` to ensure both tools are available before proceeding.
If either tool is not found, fall back to `Bash(curl -s <url>)` for fetching.

## Step 1: Fetch current documentation

Use WebFetch to read these pages directly:

1. `https://docs.anthropic.com/en/docs/claude-code/overview` — main feature list
2. `https://docs.anthropic.com/en/docs/claude-code/settings` — settings.json schema, permissions
3. `https://docs.anthropic.com/en/docs/claude-code/hooks` — hook types, events, matchers
4. `https://docs.anthropic.com/en/docs/claude-code/memory` — memory and context management
5. `https://docs.anthropic.com/en/docs/claude-code/agent-tool` — subagent capabilities
6. `https://docs.anthropic.com/en/docs/claude-code/cli` — CLI flags and options

If any URL fails, use WebSearch with query `"Claude Code" <topic> site:docs.anthropic.com` as fallback.

Then search for recent announcements:
- WebSearch: `Claude Code new features 2026`
- WebSearch: `Claude Code changelog site:anthropic.com`
- WebSearch: `Claude Code hooks settings update site:github.com/anthropics`

## Step 2: Extract and classify changes

For each finding, check if it affects dotforge:

| What to look for | Where it impacts dotforge |
|-------------------|---------------------------|
| New hook event types (beyond PreToolUse/PostToolUse/Stop) | `template/hooks/`, `stacks/*/hooks/` |
| New settings.json fields or changed schema | `template/settings.json.tmpl`, `global/settings.json.tmpl` |
| New permission categories | `stacks/*/settings.json.partial` |
| Changed deny list behavior | `template/settings.json.tmpl` deny section |
| New agent/subagent capabilities | `agents/*.md` |
| New skill/command system features | `skills/*/SKILL.md` |
| Deprecated features or breaking changes | Any affected file |
| New CLI flags relevant to automation | `skills/benchmark/SKILL.md` (uses `claude --print`) |
| MCP server changes | `global/settings.json.tmpl` |

Ignore: pricing, model releases (unless affecting tool use), marketing.

## Step 3: Compare against dotforge

For each relevant finding, check the current state:

```bash
# Search template for existing coverage
grep -r "<keyword>" template/ stacks/ global/ agents/ skills/
```

Classify each finding:
- **Gap**: dotforge doesn't cover this at all
- **Partial**: dotforge covers this but is outdated or incomplete
- **Covered**: dotforge already handles this correctly
- **Breaking**: dotforge does something that conflicts with the new behavior

## Step 4: Report

```
═══ WATCH UPSTREAM ═══
Date: {{YYYY-MM-DD}}
Sources fetched: {{N}} docs, {{N}} search results

── CHANGES DETECTED ──

🆕 NEW: {{title}}
   Source: {{url}}
   Impact: {{which dotforge files would change}}
   Priority: {{high|medium|low}}

⚠️ BREAKING: {{title}}
   Source: {{url}}
   Current dotforge behavior: {{what we do now}}
   Required change: {{what needs to change}}

📝 PARTIAL: {{title}}
   Source: {{url}}
   What's covered: {{existing coverage}}
   What's missing: {{gap}}

── SUMMARY ──
Gaps: {{N}} | Partial: {{N}} | Breaking: {{N}} | Covered: {{N}}

── NEXT STEPS ──
For each gap/partial/breaking, run:
  /forge capture "{{description}}"
Then: /forge update to evaluate and incorporate.
```

## Constraints

- DO NOT modify any dotforge files. Report only.
- DO NOT auto-create practices. Suggest `/forge capture` commands for the user.
- If web fetch fails, report clearly — don't guess or hallucinate features.
- If no changes detected, report "No relevant changes found" — this is a valid outcome.
