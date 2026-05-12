---
name: respira-setup-assistant
description: Diagnoses Respira MCP connections, walks through first-time setup, and resolves the most common errors (timeouts, 401s, 403s, version mismatches, missing API keys, plugin not installed). Use when user says "set up respira", "connect respira", "respira not working", "respira connection failed", or "fix respira".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: onboarding
---

# Respira Setup Assistant

**Version:** 1.0.0
**Category:** onboarding
**Status:** active
**Requires:** Respira for WordPress plugin (installs via this skill if missing)
**Telemetry endpoint:** https://www.respira.press/api/skills/track-usage

---

## Description

Diagnose your Respira MCP connection, walk through first-time setup, and fix common connection problems.

The Respira Setup Assistant checks whether the plugin is installed, whether an API key exists, and whether the MCP server version is compatible with the plugin. It gives you a clear status report, walks through any missing steps, and resolves the most common errors (timeouts, 401s, 403s, version mismatches) with plain-language instructions.

Use this skill the first time you connect Respira, after a WordPress update, or whenever Respira tools stop working.

---

## Trigger Phrases

This skill activates when the user says any of the following:

- "set up respira"
- "connect respira"
- "respira setup"
- "respira not working"
- "respira connection failed"
- "fix respira"
- "respira setup assistant"
- "check my respira connection"
- "respira health check"
- "diagnose respira"
- "respira mcp setup"
- "is respira connected"
- "respira not connecting"
- "help me set up respira"
- "respira install"

**Do NOT trigger for:** general WordPress tasks, requests that assume Respira is already working, or skill-specific requests like "build internal links" where the skill handles its own Respira check.

---

## Execution Workflow

### Step 1: Run the Doctor Check

Start by calling `respira_get_server_compatibility`. This is the single fastest way to know if the MCP server can reach the plugin.

```
Tool: respira_get_server_compatibility
Returns: plugin version, MCP server version, compatibility status, minimum requirements
```

**Interpret the result:**

| Result | Meaning |
|--------|---------|
| Returns data successfully | MCP server is connected and plugin is reachable |
| Connection refused / timeout | Plugin unreachable — URL or firewall problem |
| 401 Unauthorized | API key missing or wrong |
| 403 Forbidden | REST API blocked by security plugin or host |
| Version mismatch warning | One side needs updating |

If the call succeeds, proceed to Step 2 for a full status report.

If it fails, skip to the **Troubleshooting** section that matches the error.

---

### Step 2: Full Site Context

```
Tool: respira_get_site_context
Returns: WordPress version, PHP version, site URL, active plugins, active theme
```

From this response, check:

1. **Plugin installed and active** — look for `respira-for-wordpress` in the active plugins list
2. **API key configured** — the context response will include a flag indicating whether an API key is present
3. **WordPress version** — flag if below 6.0 (minimum supported)
4. **PHP version** — flag if below 7.4 (minimum supported)

---

### Step 3: Generate Status Report

Present a clear, scannable status report. Use this format:

```
## Respira Connection Status

### Plugin
- Installed: Yes / No
- Active: Yes / No
- Version: X.X.X (up to date / update available)

### API Key
- Configured: Yes / No

### MCP Server
- Version: X.X.X
- Compatible with plugin: Yes / No

### WordPress
- Version: X.X.X (supported / below minimum)
- PHP Version: X.X (supported / below minimum)

### Overall Status
[CONNECTED — ready to use]
  or
[ACTION NEEDED — see steps below]
```

Then branch based on status:

---

### Branch A: Everything is healthy

Output:

```
Your Respira connection is healthy.

Quick-start commands to try right now:
- respira_list_pages — see all your pages
- respira_get_builder_info — find out which page builder you're using
- respira_get_site_context — full site overview

Skills available in the marketplace:
- "WordPress Site DNA" — full site audit
- "SEO & AEO Amplifier" — SEO health check
- "Internal Link Builder" — build internal links
```

---

### Branch B: Plugin not installed or not active

Output:

```
## Respira Plugin Not Found

To connect your AI assistant to WordPress, install the Respira for WordPress plugin.

### Install steps:
1. Go to https://respira.press/releases
2. Download the latest version
3. In WordPress admin: Plugins → Add New → Upload Plugin
4. Activate the plugin
5. Go to Respira → API Keys → create a new key
6. Add the key to your MCP server configuration

### MCP server setup:
Run this in your terminal:
npx -y @respira/wordpress-mcp-server --setup

Follow the prompts — you'll need your WordPress site URL and the API key you just created.

Once done, come back and say: "check my respira connection"
```

---

### Branch C: Plugin installed but no API key

Output:

```
## API Key Missing

The Respira plugin is installed but no API key is configured. The MCP server needs a key to authenticate.

### Create an API key:
1. In WordPress admin, go to Respira → API Keys
2. Click "Add New Key"
3. Give it a name (e.g., "Claude Desktop")
4. Copy the generated key
5. Add it to your MCP server config — run:
   npx -y @respira/wordpress-mcp-server --setup
   and paste the key when prompted

Once done, say: "check my respira connection"
```

---

### Branch D: Version mismatch

Output using specific versions from the compatibility check:

```
## Version Mismatch Detected

Plugin version: X.X.X
MCP server version: X.X.X
Required: [minimum version from compatibility response]

### To fix:
```

Then give the specific update instruction based on which side is behind:

**If plugin needs updating:**
```
Update the Respira plugin:
1. Go to Respira → Settings → Updates (or check wp-admin → Updates)
2. Or download the latest version at https://respira.press/releases
3. Install and activate
```

**If MCP server needs updating:**
```
Update the MCP server:
npx -y @respira/wordpress-mcp-server@latest --update

Or in Claude Desktop settings, update the command to use the latest version.
```

---

## Troubleshooting Common Errors

If Step 1 (the doctor check) returned an error, use the guide below. Ask the user what error they are seeing if it was not explicit.

---

### Connection Timeout

**Symptoms:** Tools hang or return "connection timed out", "ECONNREFUSED", or "fetch failed"

**Checklist — work through these in order:**

1. **Check the site URL** — In your MCP server config, does the URL match your WordPress site exactly? Include the correct protocol (https:// vs http://) and no trailing slash issues.

2. **Check if the site is online** — Visit your WordPress site in a browser. If it's down, Respira can't connect either.

3. **Check firewall / server block** — Some hosting providers or firewalls block non-browser requests to the REST API. Ask your host to allow requests from your IP, or check if a firewall plugin (like Wordfence) is blocking API traffic.

4. **Check REST API access** — Visit `https://yoursite.com/wp-json/` in a browser. If you see a JSON response, the REST API is accessible. If you get a 404, the REST API may be disabled.

5. **Staging sites with HTTP Basic Auth** — If your staging site has password protection (the browser asks for a username + password before showing anything), you need to include those credentials in your MCP config. See Branch F below.

---

### 401 Unauthorized

**Symptoms:** Tools return "401", "Unauthorized", or "Invalid API key"

**Checklist:**

1. **API key exists** — Go to WordPress admin → Respira → API Keys. Confirm a key exists and is not expired.

2. **API key is correct** — API keys are shown only once when created. If you lost it, delete it and create a new one. Copy it carefully — no extra spaces.

3. **Key is in the right config field** — In your MCP server setup, the key goes in the `RESPIRA_API_KEY` field, not the WordPress username/password field.

4. **Staging site with HTTP Basic Auth** — See Branch F for how to add staging credentials.

---

### 403 Forbidden

**Symptoms:** Tools return "403", "Forbidden", or "REST API disabled"

**Checklist:**

1. **REST API is not disabled** — Some security plugins or hosting setups disable the WordPress REST API. Check your security plugin (Wordfence, iThemes Security, All-In-One WP Security) for a "Disable REST API" setting and turn it off, or add Respira's endpoint to the whitelist.

2. **Respira endpoint is whitelisted** — The REST API endpoint Respira uses is `/wp-json/respira/v1/`. Whitelist this path in any security plugin that filters REST API access.

3. **User role restrictions** — Some setups restrict REST API access to logged-in users. Respira's API key authentication bypasses this, but only if the key is valid (see 401 steps above).

4. **Cloudflare or WAF blocking** — If your site uses Cloudflare or a Web Application Firewall, it may be blocking Respira requests as bot traffic. Add a page rule or firewall rule to allow requests with Respira's user-agent.

---

### Branch F: Staging Site with HTTP Basic Auth

If accessing a staging site that requires browser-level password protection:

```
## Staging Site Setup

Your staging environment has HTTP Basic Authentication (the browser prompts for a username and password before showing the site). Respira needs these credentials in addition to the API key.

In your MCP server configuration, add these fields:
- RESPIRA_BASIC_AUTH_USER: your staging username
- RESPIRA_BASIC_AUTH_PASS: your staging password

These are separate from your WordPress login and your Respira API key.

Re-run the setup:
npx -y @respira/wordpress-mcp-server --setup

And select the option to configure Basic Auth credentials.
```

---

## Quick-Start Examples

Once connected, share these examples to help the user get started immediately:

```
## You're connected. Here's what to try:

### Explore your site
- "list my pages" → respira_list_pages
- "what page builder am I using?" → respira_get_builder_info
- "show me my site overview" → respira_get_site_context

### Make changes (safe — always uses drafts)
- "create a draft of my homepage to experiment with"
- "find the text 'Contact Us' on my site"
- "update the title of my About page"

### Run a full audit
- "analyze my site" → runs WordPress Site DNA skill
- "check my SEO" → runs SEO & AEO Amplifier skill
```

---

## Safety Notes

- This skill is read-only during diagnosis — it never modifies your site
- No changes are made unless the user explicitly approves them in a later step
- API keys are never logged or stored by this skill

---

## Tooling

**Core tools used**
- `respira_get_server_compatibility`
- `respira_get_site_context`

## Telemetry

After run completion, send fire-and-forget usage tracking to:

- `POST https://www.respira.press/api/skills/track-usage`

Include:
- `skill_slug = respira-setup-assistant`
- site/version context (if available — may not be if plugin is not connected)
- duration and outcome (connected / action_needed / error)
- which branch was taken (A / B / C / D / F / troubleshooting)

Never block user flow on telemetry failure.

## Related Skills

- WordPress Site DNA (run after setup to understand your site)
- Site Onboarding (first-run primer once connected)
- Technical Debt Audit

---

Built by Respira for WordPress
https://respira.press/skills/respira-setup-assistant
