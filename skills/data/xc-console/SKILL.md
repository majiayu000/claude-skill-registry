---
name: xc-console
description: Automate F5 Distributed Cloud web console operations through browser
  automation using mcp__claude-in-chrome MCP tools. Handles multi-provider authentication
  (Azure SSO, Google, Okta, SAML, native user
---

---
name: xc-console
description: Automate F5 Distributed Cloud web console operations through browser automation using mcp__chrome-devtools MCP tools. Handles multi-provider authentication (Azure SSO, Google, Okta, SAML, native username/password), detecting session expiry and navigating login flows. Warns when VPN is required. Use when creating HTTP/TCP load balancers, origin pools, WAF policies, deploying cloud sites (AWS/Azure/GCP), managing DNS zones, configuring service policies, or executing any F5 XC GUI-based tasks. Triggers on: F5 XC console, GUI automation, browser automation, login, SSO, authenticate, tenant management, visual configuration, Web App and API Protection, WAAP.
allowed_args: true
---

# F5 Distributed Cloud Console Automation Skill

Expert in automating F5 Distributed Cloud web console operations through browser automation using the `mcp__chrome-devtools` MCP tools.

## Overview

This skill uses the `mcp__chrome-devtools__*` MCP tools which provide Chrome browser automation. These tools provide:

- ✅ Works with your existing browser session (preserves authentication)
- ✅ Provides real-time visual feedback (watch Claude navigate in real time)
- ✅ Uses natural language instructions (no low-level scripting required)
- ✅ Automatically handles existing login state and cookies
- ✅ **Multi-provider authentication** - detects Azure SSO, Google, Okta, SAML, and native login
- ✅ **VPN detection** - warns when tenant requires VPN access

### MCP Tools Available
| Tool | Purpose |
|------|---------|
| `mcp__chrome-devtools__list_pages` | List open browser pages |
| `mcp__chrome-devtools__select_page` | Select a page for interaction |
| `mcp__chrome-devtools__navigate_page` | Navigate to URLs |
| `mcp__chrome-devtools__take_snapshot` | Read page elements (accessibility tree) |
| `mcp__chrome-devtools__click` | Click elements |
| `mcp__chrome-devtools__fill` | Fill text inputs |
| `mcp__chrome-devtools__fill_form` | Fill multiple form fields |
| `mcp__chrome-devtools__take_screenshot` | Capture page screenshots |
| `mcp__chrome-devtools__hover` | Hover over elements |
| `mcp__chrome-devtools__press_key` | Press keyboard keys |

## Prerequisites

Before using this skill, ensure you have:

### 1. Chrome DevTools MCP Server
The Chrome DevTools MCP server is configured in `.mcp.json` and starts automatically:
```bash
# Verify MCP server is available:
npx -y @anthropic/mcp-server-chrome-devtools@latest

# The server provides browser automation tools
```

### 2. F5 XC API Credentials (for validation)
Set these environment variables for CLI-based verification:
```bash
export F5XC_API_URL="https://nferreira.staging.volterra.us"
export F5XC_API_TOKEN='2SiwIzdXcUTV9Kk/wURCJO+NPV8='
```

### 3. Authentication
You should already be logged into the F5 XC tenant in your Chrome browser. The skill leverages your existing session and handles authentication automatically if session expires.

## Multi-Provider Authentication

This skill automatically detects and handles multiple authentication methods:

| Auth Type | URL Pattern | Claude Can Automate? |
|-----------|-------------|---------------------|
| Native U/P | `login*.volterra.us` | ❌ User enters creds |
| Azure SSO | `login.microsoftonline.com` | ⚠️ Only if cached |
| Google SSO | `accounts.google.com` | ⚠️ Only if cached |
| Okta SSO | `*.okta.com` | ⚠️ Only if cached |
| Generic SAML | `/saml/`, `/sso/` | ⚠️ Only if cached |
| Already Logged In | `/web/workspaces/` | ✅ Yes |
| Connection Failed | timeout/error | ❌ Warn about VPN |

### Detection Triggers
The skill detects login requirements when:
- URL redirects to login page (`login*.volterra.us`, `login.microsoftonline.com`, `accounts.google.com`, `*.okta.com`)
- Page contains "Sign in", "Go to login", or "Session expired" messages
- Connection times out (may require VPN)

### Auto-Flow Sequence
```
1. Navigate to F5 XC tenant URL
2. Wait for page load (detect connection failures → warn about VPN)
3. Check URL and page content using mcp__chrome-devtools__take_snapshot
4. Identify authentication type:
   a. Native login → Inform user to enter credentials, wait
   b. SSO redirect → Find SSO button, click, wait for provider
   c. Already logged in → Skip to step 6
5. Handle SSO provider:
   - If cached session → auto-redirect back
   - If credentials needed → inform user, wait for confirmation
6. Verify F5 XC console loaded (look for workspace cards)
7. Continue with original navigation task
```

### Login Example
```
/xc:console login https://nferreira.staging.volterra.us/ and navigate to WAAP

# Claude will:
# 1. Get browser context with tabs_context_mcp
# 2. Navigate to tenant URL
# 3. Detect auth type (native, SSO, or already logged in)
# 4. Handle accordingly (inform user or auto-complete)
# 5. Navigate to Web App and API Protection workspace
# 6. Take screenshot to confirm
```

See `./authentication-flows.md` for detailed workflow steps.

## Quick Start

### Basic Navigation
```bash
# Launch Claude Code (Chrome DevTools MCP starts automatically)
claude

# Then provide natural language instructions:
"Navigate to https://nferreira.staging.volterra.us and tell me what you see on the home page"

# Claude will:
# 1. Navigate to the URL using mcp__chrome-devtools__navigate_page
# 2. Wait for page to load
# 3. Take a snapshot using mcp__chrome-devtools__take_snapshot
# 4. Describe what it sees
```

### Form Filling
```bash
claude

"Navigate to the HTTP Load Balancers page at https://nferreira.staging.volterra.us.
Then click the 'Add HTTP Load Balancer' button.
Fill in the form with:
- Name: my-test-lb
- Namespace: production
- Domains: test.example.com

But stop before submitting - I want to review first."
```

### Data Extraction
```bash
claude

"Navigate to the HTTP Load Balancers list page.
Extract all load balancer names, their namespaces, and domains.
Save the results as a JSON array."
```

## Core Capabilities

### Navigation
- Navigate to any URL within the F5 XC console
- Click menu items, buttons, and links using text or selectors
- Switch between tabs and manage tab groups
- Handle redirects automatically (including Azure SSO redirect)

### Form Interaction
- Fill text inputs, textareas
- Select dropdown options
- Check/uncheck checkboxes
- Add/remove items from lists
- Complete multi-step forms

### Content Reading
- Extract text content from pages
- Read DOM structure and elements
- Take screenshots for visual verification
- Read console logs (useful for debugging)

### Debugging
- Inspect network requests (see API calls)
- Read console errors and warnings
- Analyze page structure
- Verify element visibility and properties

### Session Management
- Automatically uses existing Chrome session
- Preserves authentication state across providers (Azure, Google, Okta, SAML)
- Handles session expiry with automatic auth type detection
- Warns when VPN connection is required
- Provides clear messages when manual authentication needed

## Common Workflows

### Workflow 1: Create HTTP Load Balancer

```bash
claude

"I want to create an HTTP load balancer in F5 XC.

Please:
1. Navigate to https://nferreira.staging.volterra.us
2. Find and click the 'HTTP Load Balancers' page
3. Click 'Add HTTP Load Balancer' button
4. Fill in:
   - Name: demo-lb
   - Namespace: production
   - Domains: demo.example.com
   - Protocol: HTTPS with Automatic Certificate
5. Look for an 'Origin Pool' field and let me know what options are available

Don't submit yet - just show me the form filled in."
```

### Workflow 2: Explore Console Structure

```bash
claude

"Help me inventory the F5 Distributed Cloud console.

Navigate to https://nferreira.staging.volterra.us and:
1. Look at the main left sidebar menu
2. For each top-level menu item, tell me:
   - The menu item name
   - Any submenus
   - What page appears when clicked

Take screenshots of key pages so I can see the structure.
Organize the results as a hierarchical list."
```

### Workflow 3: Verify with CLI Integration

```bash
# First, use the console to create something
claude

"Navigate to HTTP Load Balancers page and create a new LB named 'cli-test' in 'default' namespace.
Don't submit yet - just tell me the form is ready."

# Then verify with CLI
f5xcctl configuration list http_loadbalancer -n default

# You should see the newly created resource in the list
```

## Advanced Patterns

### Taking Screenshots for Reference
```bash
claude

"Navigate to the HTTP Load Balancers creation form and take a screenshot.
Save it so I can see the exact form layout and field names."
```

### Handling Authentication Issues
When Claude encounters a login page, CAPTCHA, or other security challenge:
- Claude will pause and describe what it sees
- You manually handle the authentication (log in, solve CAPTCHA)
- Tell Claude to continue with the task
```bash
claude

"Try to navigate to https://nferreira.staging.volterra.us"

# If you get: "I see a login page. Azure SSO button is visible."
# You manually click the SSO button or provide credentials in your browser
# Then tell Claude: "I've logged in, continue with the task"
```

### Extracting Structured Data
```bash
claude

"Navigate to the HTTP Load Balancers list page.
For each load balancer shown, extract:
- Name
- Namespace
- Status
- Created date (if visible)

Format as a JSON array and save to lb-list.json"
```

## Key Files in This Skill

| File | Purpose |
|------|---------|
| `SKILL.md` | This file - skill overview and instructions |
| `authentication-flows.md` | Multi-provider authentication handling (Azure, Google, Okta, SAML, native, VPN) |
| `browser-interaction-patterns.md` | **Deterministic patterns for Angular CDK/Material component interaction** |
| `console-navigation-metadata.json` | v2.3 metadata with stable selectors (data-testid, aria-label, text_match, css) |
| `url-sitemap.json` | Static/dynamic route mapping with workspace aliases and shortcuts |
| `crawl-workflow.md` | v2.3 crawl phases including selector, URL, and state detection |
| `detection-patterns.json` | Generalized RBAC, subscription, and module detection patterns |
| `scripts/crawl-console.js` | Crawler spec with extraction scripts and templates |
| `scripts/detect-permissions.js` | Runtime RBAC permission detection script |
| `scripts/detect-subscription.js` | Subscription tier and feature detection script |
| `scripts/detect-modules.js` | Module initialization state detection script |
| `task-workflows.md` | Master index of task automation patterns |
| `documentation-index.md` | Indexed docs.cloud.f5.com knowledge base |
| `workflows/*.md` | Specific task workflows (HTTP LB, origin pools, WAF, etc.) |

## Documentation Integration

This skill is designed to work alongside official F5 XC documentation:
- See `documentation-index.md` for links to docs.cloud.f5.com
- Consult `console-navigation-metadata.json` for detailed form field information
- Review `workflows/` directory for step-by-step task guides

## Integration with Other F5 XC Skills

This skill works seamlessly with:

### f5xc-cli Skill (Query & Verify)
Use f5xcctl to validate console actions:
```bash
# After creating something in the console:
f5xcctl configuration get http_loadbalancer demo-lb -n production

# Compare what the console shows vs what the API returns
```

### f5xc-terraform Skill (Infrastructure as Code)
Use Terraform to deploy the same resources as code:
```bash
# The console skill helps you:
# 1. Understand the UI workflow
# 2. See all available options
# 3. Learn the resource structure
# Then use f5xc-terraform to automate it
```

## Best Practices

### 1. Break Large Tasks into Smaller Steps
```bash
# Instead of asking Claude to do everything in one go:
# ❌ "Create a complete load balancer with origin pool, health checks, and WAF policy"

# ✅ Do this in phases:
claude
# Phase 1: "Create origin pool named backend-pool"

# Phase 2: "Create HTTP LB named my-app pointing to backend-pool"

# Phase 3: "Add WAF policy to my-app LB"
```

### 2. Take Screenshots for Reference
```bash
claude

"Take screenshots of these pages and save them:
1. HTTP Load Balancers list page
2. HTTP Load Balancer creation form
3. Origin Pool creation form

I want to see the exact layout and field names."
```

### 3. Verify Console State with CLI
```bash
# After using console:
f5xcctl configuration list http_loadbalancer --all-namespaces --output-format json

# Compare with what console showed to ensure consistency
```

### 4. Be Specific with Instructions
```bash
# ❌ Too vague:
# "Create a load balancer"

# ✅ Specific:
# "Create HTTP load balancer named demo-lb in namespace 'production'
#  with domain example.com pointing to origin pool backend-pool.
#  Use HTTPS with automatic certificate."
```

## Troubleshooting

### Chrome DevTools MCP Not Available
```bash
# 1. Verify MCP server is configured in .mcp.json:
cat .mcp.json

# 2. Test the server manually:
npx -y @anthropic/mcp-server-chrome-devtools@latest

# 3. Check Claude Code MCP status:
# The server should start automatically when needed
```

### Session Expired
When Claude detects session expiry:
```bash
# Claude will identify the authentication type:
# - Native login (username/password): You'll be asked to enter credentials
# - SSO (Azure, Google, Okta): Claude attempts auto-login if cached
# - Connection timeout: Claude warns about VPN requirement
# After authenticating, tell Claude to continue
```

### Form Fields Not Found
```bash
# Claude will describe what it sees
# Ask Claude to:
# 1. Take a screenshot
# 2. Describe all visible input fields
# 3. Look for the field by label text or placeholder

"Take a screenshot of the form.
Then find and fill the field labeled 'Domain' with 'example.com'."
```

### Navigation Paths Changed
The console UI may change. If Claude can't find expected buttons:
```bash
# Claude will explore and find the new location
"The button location seems to have changed.
Explore the page and find the 'Create' or 'Add' button, then click it."
```

## Security & Permissions

This skill operates within your existing Chrome browser session, so:
- ✅ Uses your existing SSO login (Azure, Google, Okta - no re-authentication if cached)
- ✅ Respects your browser's cookie storage and session state
- ✅ Cannot access other browser tabs or extensions
- ✅ Never enters credentials on your behalf (security policy)
- ⚠️ Can only interact with pages you have permission to access
- ⚠️ Should only be used with trusted instructions (avoid pasting untrusted prompts)

For sensitive operations:
- Review Claude's actions before it submits forms
- Use the preview/review step before final submission
- Verify critical operations with f5xcctl CLI afterward

## Getting Help

### Debugging Claude's Navigation
```bash
claude

"I notice you took a wrong turn. Let me help.
Take a screenshot and describe what page you're on.
Then tell me what button or link you see that matches 'HTTP Load Balancers'."
```

### Understanding Form Structure
```bash
claude

"Navigate to the form page and analyze its structure.
For each form field, tell me:
- The label text
- The input type (text, select, checkbox, etc.)
- Whether it's required
- Any visible validation hints"
```

### Learning Console Workflows
```bash
claude

"Walk me through the steps to create an HTTP load balancer from scratch.
Assume I have:
- A namespace named 'production'
- An origin pool named 'backend-pool'

Show me each page I'd need to visit and what I'd fill in."
```

## Deterministic Navigation (v2.2)

This skill uses pre-crawled metadata for deterministic browser automation. The plugin ships with pre-crawled metadata that works out of the box. Crawling is **optional** - use it to refresh stale data or update after F5 XC console UI changes.

### Selector Priority Chain

The v2.2 metadata includes **stable selectors** that work across browser sessions, not just session-specific refs:

| Priority | Selector Type | Reliability | Example |
|----------|---------------|-------------|---------|
| 1 | `data_testid` | Highest | `[data-testid="add-lb-btn"]` |
| 2 | `aria_label` | High | `[aria-label="Add Load Balancer"]` |
| 3 | `text_match` | Medium | Button containing "Add HTTP Load Balancer" |
| 4 | `css` | Medium | `.workspace-card:has-text('Web App')` |
| 5 | `ref` | Session-only | `ref_27` (requires fresh crawl) |

### How It Works

**Before v2.2 (Session-Specific Refs)**:
```
Claude: Uses ref_27 from metadata
Risk: Refs change between browser sessions
Result: ~70% success rate
```

**After v2.2 (Stable Selectors)**:
```
Claude: Uses data_testid > aria_label > text_match fallback
Uses: mcp__chrome-devtools__click with stable selector from snapshot
Result: ~95% success rate across sessions
```

### Metadata Structure (v2.2)

Each element now includes both refs and stable selectors:
```json
{
  "add_button": {
    "ref": "ref_27",
    "text": "Add HTTP Load Balancer",
    "selectors": {
      "data_testid": null,
      "aria_label": "Add HTTP Load Balancer",
      "text_match": "Add HTTP Load Balancer",
      "css": "button:has-text('Add HTTP Load Balancer')"
    }
  }
}
```

### URL Sitemap

The `url-sitemap.json` file provides complete route mapping:
- **Static routes**: Fixed paths like `/web/home`, `/web/workspaces/...`
- **Dynamic routes**: Paths with variables like `/namespaces/{namespace}/...`
- **Workspace mapping**: Shorthand aliases (`waap` → `/web/workspaces/web-app-and-api-protection`)
- **Resource shortcuts**: Quick navigation (`http-lb` → full path with namespace variable)

### Fallback Strategy

When navigating, Claude uses this priority:
1. Try `data_testid` selector (most stable)
2. Try `aria_label` selector
3. Try `text_match` with find()
4. Try `css` selector
5. Try session-specific `ref` (may be stale)
6. Report mismatch for metadata update

### Crawl Command

To refresh the metadata (optional):
```
/xc:console crawl https://nferreira.staging.volterra.us/
```

See `crawl-workflow.md` for the detailed crawl process.

## Angular CDK/Material Interaction Patterns

**CRITICAL**: The F5 XC Console uses Angular with Angular CDK/Material components. Some UI elements require specific interaction patterns that differ from standard accessibility-based clicking.

### The Overlay Problem

Action menus (⋮ buttons) open **Angular CDK overlays** whose menu items do NOT appear in accessibility snapshots. This is because:
- Overlays are rendered in a separate container (`.cdk-overlay-container`)
- The overlay content is outside the main DOM tree that snapshots capture
- Standard `click()` may not trigger Angular change detection

### Solution: JavaScript Event Dispatch

When clicking items in dropdown menus, use `evaluate_script` with full MouseEvent sequence:

```javascript
mcp__chrome-devtools__evaluate_script({
  function: `(menuText) => {
    const overlay = document.querySelector('.cdk-overlay-container');
    if (!overlay) return { success: false, error: 'No overlay' };

    const items = overlay.querySelectorAll('[role="menuitem"], button, .mat-menu-item');
    for (const item of items) {
      if (item.textContent.includes(menuText)) {
        // Full event sequence required for Angular Material
        ['mousedown', 'mouseup', 'click'].forEach(type => {
          item.dispatchEvent(new MouseEvent(type, {
            bubbles: true,
            cancelable: true,
            view: window
          }));
        });
        return { success: true, clicked: menuText };
      }
    }
    return { success: false, error: 'Not found: ' + menuText };
  }`,
  args: ["Delete"]
})
```

### When to Use Each Pattern

| UI Element | Pattern | Reason |
|------------|---------|--------|
| Primary buttons | `take_snapshot` → `click` | Visible in accessibility tree |
| Form inputs | `take_snapshot` → `fill` | Standard form interaction |
| Action menu trigger | `click` with uid | Opens the overlay |
| **Dropdown menu items** | **`evaluate_script`** | **NOT in accessibility tree** |
| Confirmation dialogs | `take_snapshot` → `click` | Dialog IS in accessibility tree |

### Full Reference

See `browser-interaction-patterns.md` for:
- Complete code examples for all patterns
- Troubleshooting common issues
- Test resource naming conventions
- E2E workflow templates

## State Detection Capabilities (v2.3)

This skill includes runtime detection scripts for discovering tenant state:

### RBAC Permission Detection

Detect read-only vs editable permissions at runtime:

```bash
# Claude automatically detects permission state when navigating
/xc:console navigate to HTTP Load Balancers in namespace p-ashworth

# Returns permission state:
# - canEdit: false
# - canDelete: false
# - canCreate: false
# - viewOnly: true
# - lockedActions: ["Add", "Edit Configuration", "Clone Object", "Delete"]
```

**Detection Patterns:**
| Pattern | Indicator | Meaning |
|---------|-----------|---------|
| `generic "Locked"` as button child | RBAC lock indicator | Action requires higher permission |
| `generic "View"` badge in dialog | Read-only mode | Configuration is view-only |
| Tooltip with "permission denied" | Access denied | User lacks required role |

**Script**: `scripts/detect-permissions.js`

### Subscription Tier Detection

Detect Standard vs Advanced subscription features:

```bash
# Claude scans workspace cards for subscription badges
/xc:console check subscription tier

# Returns subscription state:
# - tier: "standard" | "advanced" | "enterprise"
# - badges: ["Limited Availability", "New", "Early Access"]
# - gatedFeatures: ["API Discovery", "Bot Defense Advanced"]
```

**Badge Types:**
| Badge | Meaning | Access |
|-------|---------|--------|
| `Limited Availability` | Preview release | May require approval |
| `New` | Recently added | Generally available |
| `Early Access` | Beta feature | Opt-in required |
| `Upgrade` | Tier gated | Requires subscription upgrade |

**Script**: `scripts/detect-subscription.js`

### Module Initialization Detection

Detect which workspaces/modules need initialization:

```bash
# Claude checks workspace About page for service status
/xc:console check module status for web-app-scanning

# Returns module state:
# - initialized: true
# - status: "enabled"
# - action_available: "Explore"
```

**Status Indicators:**
| Text | Button | Status |
|------|--------|--------|
| "This service is enabled." | "Visit Service" | Enabled |
| "This service is not enabled." | "Enable Service" | Needs init |
| Table status: "● Enabled" | "Explore" | Active |
| Table status: "Disabled" | "Enable" | Inactive |

**Script**: `scripts/detect-modules.js`

### Detection Patterns File

All detection patterns are documented in `detection-patterns.json`:
- No PII or tenant-specific data
- Generalized patterns that work across any F5 XC tenant
- Machine-readable format for automated detection

### Usage in Workflows

Claude automatically uses state detection when:
1. Navigating to resource lists (checks RBAC)
2. Opening forms (checks if Add/Edit buttons are available)
3. Entering workspaces (checks initialization state)
4. Scanning home page (checks subscription badges)

This enables **conditional workflow execution** - Claude adapts its automation based on detected permissions and features.

## Current Status

**Metadata v2.3.0** (State Detection):
- ✅ Skill directory structure created
- ✅ SKILL.md written with comprehensive instructions
- ✅ Multi-provider authentication (Azure, Google, Okta, SAML, native)
- ✅ VPN detection and warning
- ✅ Console crawl scripts with stable selector extraction
- ✅ Crawl workflow documented (`crawl-workflow.md` v2.3)
- ✅ URL sitemap with static/dynamic routes (`url-sitemap.json`)
- ✅ Stable selectors (data-testid, aria-label, text_match, css)
- ✅ Selector priority fallback chain
- ✅ Metadata ships with plugin (crawl is optional)
- ✅ **RBAC permission detection** (`scripts/detect-permissions.js`)
- ✅ **Subscription tier detection** (`scripts/detect-subscription.js`)
- ✅ **Module initialization detection** (`scripts/detect-modules.js`)
- ✅ **Detection patterns file** (`detection-patterns.json`)
- ✅ **Crawl phases 7-10** for state detection workflow

## Next Steps

1. **Run Initial Crawl**
   ```
   /xc:console crawl https://your-tenant.volterra.us/
   ```
   Populate selectors for all elements across workspaces.

2. **Validate Cross-Session Navigation**
   Test deterministic navigation without refs (selectors only).

3. **Validate with CLI**
   ```bash
   f5xcctl configuration list http_loadbalancer --all-namespaces
   ```

---

**For detailed API-driven management**: See the `f5xc-cli` and `f5xc-terraform` skills.

**For console documentation mapping**: See `documentation-index.md` (coming soon).

**For specific task workflows**: See `workflows/` directory (coming soon).
