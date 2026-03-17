---
name: using-webctl
description: Browser automation via webctl CLI in Claude.ai containers with authenticated proxy support. Use when users mention webctl, browser automation, Playwright browsing, web scraping, or headless Chrome in container environments.
metadata:
  version: 0.0.1
---

# Using webctl in Claude.ai Containers

Browser automation using webctl CLI with automatic proxy authentication handling for Claude.ai's egress-controlled environment.

## When This Skill Applies

- User requests browser automation, web scraping, or page interaction
- webctl commands fail with `ERR_TUNNEL_CONNECTION_FAILED`
- Playwright/Chromium needs to work through authenticated HTTP proxy

## Core Problem

Claude.ai containers route traffic through an authenticated egress proxy (`HTTP_PROXY` env var with JWT credentials). Chromium doesn't properly handle proxy authentication for HTTPS CONNECT tunnels, causing all HTTPS navigation to fail even though curl works.

## Solution

A local forwarding proxy (port 18080) intercepts Chromium connections and injects `Proxy-Authorization` headers before forwarding to the real egress proxy.

## Setup Procedure

### 1. Install webctl

```bash
pip install webctl --break-system-packages
webctl setup  # Downloads Chromium if needed
```

### 2. Deploy Auth Proxy Module

Copy `scripts/auth_proxy.py` to webctl's daemon directory:

```bash
cp /mnt/skills/user/using-webctl/scripts/auth_proxy.py \
   /usr/local/lib/python3.12/dist-packages/webctl/daemon/
```

### 3. Patch Session Manager

Apply this patch to `/usr/local/lib/python3.12/dist-packages/webctl/daemon/session_manager.py`:

Find the context creation block (around line 104):
```python
# Create context
context = await browser.new_context(
    storage_state=storage_state, viewport={"width": 1280, "height": 720}
)
```

Replace with:
```python
# Create context with proxy from env (with auth handling)
from .auth_proxy import get_local_proxy_url
proxy_url = get_local_proxy_url()
proxy_config = {"server": proxy_url} if proxy_url else None

context = await browser.new_context(
    storage_state=storage_state, 
    viewport={"width": 1280, "height": 720},
    proxy=proxy_config
)
```

### 4. Verify

```bash
webctl start --mode unattended
webctl --quiet navigate "https://github.com"
webctl snapshot --interactive-only --limit 10
webctl stop --daemon
```

## Quick Reference

### Session Management
```bash
webctl start --mode unattended    # Headless browser
webctl stop --daemon              # Full shutdown
webctl status                     # Current state + console error counts
```

### Navigation
```bash
webctl navigate "https://..."
webctl back / webctl forward / webctl reload
```

### Observation
```bash
webctl snapshot --interactive-only --limit 30   # Buttons, links, inputs
webctl snapshot --within "role=main"            # Scope to container
webctl query "role=button name~=Submit"         # Debug queries
webctl screenshot --path shot.png
```

### Interaction
```bash
webctl click 'role=button name~="Submit"'
webctl type 'role=textbox name~="Email"' "user@example.com"
webctl type 'role=textbox name~="Search"' "query" --submit
webctl select 'role=combobox name~="Country"' --label "Germany"
```

### Query Syntax
- `role=button` — By ARIA role
- `name~="partial"` — Contains (preferred, more robust)
- `name="exact"` — Exact match
- `nth=0` — Select first when multiple matches

### Wait Conditions
```bash
webctl wait network-idle
webctl wait 'exists:role=button name~="Continue"'
webctl wait 'url-contains:"/dashboard"'
```

## Troubleshooting

### ERR_TUNNEL_CONNECTION_FAILED
Auth proxy not loaded. Verify:
1. `auth_proxy.py` exists in webctl daemon directory
2. Session manager is patched
3. Restart daemon: `webctl stop --daemon && webctl start --mode unattended`

### Multiple matches error
Add specificity or use `nth=0`:
```bash
webctl click 'role=link name="Sign in" nth=0'
```

### Verify proxy is running
```bash
netstat -tlnp | grep 18080
```

## Limitations

- Patch is session-local (container resets clear it)
- Only allowed domains in network config are accessible
- No Firefox support (download blocked by egress policy)

## Domain Restrictions

Check `<network_configuration>` in system prompt for allowed domains. Common allowed: `*.github.com`, `*.bsky.app`, allowed API endpoints.

## Output Filtering

Reduce context consumption:
```bash
webctl snapshot --interactive-only --limit 30    # Cap elements
webctl snapshot | grep -i "submit"               # Unix filtering
webctl --quiet navigate "..."                    # Suppress events
```
