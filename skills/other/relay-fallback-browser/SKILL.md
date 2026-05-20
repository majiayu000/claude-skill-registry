---
name: relay-fallback-browser
description: Relay-first browsing policy. Try Chrome Relay first; if disconnected/unavailable, automatically fall back to managed headless browser or free-search without asking user for manual toggle.
metadata: {"openclaw":{"emoji":"🧭","requires":{"bins":["openclaw","node"]}}}
---

# Relay-First Browser Fallback

Use this skill whenever the user asks for web browsing, screenshots, or web data extraction.

## Goal

- Primary path: Chrome Relay (user browser footprint; best compatibility)
- Fallback path: No manual toggle required from user
  - managed browser tool for page interaction/screenshot
  - free-search for search-only tasks

## Execution policy

1. Attempt browser path first:

```bash
openclaw --profile jarvis browser status
```

2. If browser actions fail with any relay-disconnect pattern, do NOT ask user to click extension first. Immediately run fallback path.

Relay-disconnect patterns include (examples):

- "gateway token mismatch"
- "disconnected (1008)"
- "Can't reach the OpenClaw browser control service"
- "Chrome extension relay is running, but no tab is connected"
- "Unable to connect"

3. Fallback routing:

- Search intent only (find links, headlines, references): use `free-search`
- Page interaction / screenshot / DOM extraction: use managed browser commands directly

```bash
openclaw --profile jarvis browser start
openclaw --profile jarvis browser open "<url>"
openclaw --profile jarvis browser snapshot --format md --limit 200
openclaw --profile jarvis browser screenshot --full-page
```

4. Recovery hook (only when gateway/browser service is unhealthy):

```bash
bash "$HOME/openclaw_pro/workspace/skills/self-heal-openclaw/scripts/self_heal_openclaw.sh" --profile jarvis
```

Then retry step 1 once.

## Response style

- Do the fallback automatically.
- Report outcome briefly: "Relay failed, switched to fallback and completed." if successful.
- Ask for manual extension attach only if both relay and fallback fail.
- Do not mention Brave API/key as a blocker in user-facing messages.
- Do not answer with "can't browse"; attempt fallback and self-heal first.

## Safety

- Do not bypass auth/paywalls/captcha.
- Do not claim screenshot success unless the screenshot command actually succeeded.
