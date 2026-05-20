---
name: doc-visual
description: Generate visual documentation (screenshots, videos) for Momentum CMS features and flows. Use when asked to document, capture, screenshot, record, or visually demonstrate any application flow. Captures admin dashboard, auth flows, CRUD operations, responsive views, dark/light themes, Storybook components, and kitchen sink. Triggers include "document the login flow", "capture screenshots of the admin", "create visual docs", "record a video of the CRUD flow", "/doc-visual auth", "/doc-visual all".
argument-hint: <flow|all> [--theme light|dark|both] [--responsive] [--video] [--headed]
allowed-tools: Bash(agent-browser:*), Bash(nx *), Bash(mkdir *), Bash(ls *), Bash(ffmpeg *), Read, Glob, Grep, Write
---

# Visual Documentation Generator

Systematically capture screenshots, videos, and GIFs of Momentum CMS flows using `agent-browser` CLI. Outputs organized into `docs/visuals/` by feature.

## Quick Start

```bash
/doc-visual dashboard              # Capture dashboard screenshots
/doc-visual auth                   # Capture login, setup, forgot-password
/doc-visual collections            # Capture CRUD flows
/doc-visual all                    # Capture everything
/doc-visual all --responsive       # Everything + responsive breakpoints
/doc-visual all --video            # Everything + WebM recordings of flows
/doc-visual navigation --headed    # Watch the capture in a visible browser
```

## Workflow Overview

Every capture session follows 5 phases. **Do not skip phases.**

---

## Phase 0: Prerequisites

Before capturing anything, verify the environment is ready.

### 1. Dev Server

```bash
# Check if the dev server is running
agent-browser open "http://localhost:4200"
agent-browser wait --load networkidle
agent-browser get title
```

If the server is not running, start it:

```bash
nx serve example-angular &
# Wait for compilation
sleep 15
agent-browser open "http://localhost:4200"
agent-browser wait --load networkidle
```

**IMPORTANT**: The correct command is `nx serve example-angular`, NOT `nx serve cms-admin`.

### 2. Output Directory

```bash
mkdir -p docs/visuals/{auth,dashboard,collections,fields,media,navigation,plugins,theme,responsive,kitchen-sink}
```

### 3. Auth State

Check if a saved auth state exists:

```bash
if [ -f docs/visuals/.auth-state.json ]; then
    agent-browser state load docs/visuals/.auth-state.json
    agent-browser open "http://localhost:4200/admin"
    agent-browser wait --load networkidle
    # Verify we're on the dashboard, not redirected to login
    URL=$(agent-browser get url)
    if echo "$URL" | grep -q "login\|setup"; then
        echo "Auth state expired, re-authenticating..."
        # Proceed to Phase 2
    fi
fi
```

If no auth state or expired, proceed to Phase 2.

---

## Phase 1: Argument Parsing

Parse the flow argument to determine what to capture:

| Argument       | Flows Captured                                     |
| -------------- | -------------------------------------------------- |
| `all`          | Everything below                                   |
| `auth`         | Login, setup, forgot-password, reset-password      |
| `dashboard`    | Dashboard overview, empty states                   |
| `collections`  | List, create, edit, view for each collection       |
| `fields`       | Field types showcase (field-test-items collection) |
| `media`        | Media library overview                             |
| `navigation`   | Sidebar, entity sheet, mobile drawer               |
| `plugins`      | Analytics and SEO dashboards                       |
| `theme`        | Light/dark mode comparisons of primary pages       |
| `responsive`   | Primary pages at 375, 768, 1280, 1920 widths       |
| `kitchen-sink` | UI component showcase page                         |
| `storybook`    | Storybook component stories (requires port 4400)   |

### Flags

| Flag                        | Default | Effect                                 |
| --------------------------- | ------- | -------------------------------------- |
| `--theme light\|dark\|both` | `both`  | Which theme(s) to capture              |
| `--responsive`              | off     | Add responsive breakpoint captures     |
| `--video`                   | off     | Record WebM videos of multi-step flows |
| `--headed`                  | off     | Show browser window during capture     |

---

## Phase 2: Authentication

If no valid auth state exists, authenticate:

### First-Time Setup (if `/admin` redirects to `/admin/setup`)

```bash
agent-browser open "http://localhost:4200/admin"
agent-browser wait --load networkidle

# Check if we're on setup page
URL=$(agent-browser get url)
if echo "$URL" | grep -q "setup"; then
    # Capture setup page BEFORE filling
    agent-browser screenshot docs/visuals/auth/setup-light.png

    agent-browser snapshot -i
    # Fill setup form: name, email, password
    agent-browser fill @e1 "Admin User"
    agent-browser fill @e2 "admin@test.com"
    agent-browser fill @e3 "TestPassword123!"
    agent-browser click @e4  # Submit button
    agent-browser wait --load networkidle
fi
```

### Login (if redirected to `/admin/login`)

```bash
URL=$(agent-browser get url)
if echo "$URL" | grep -q "login"; then
    # Capture login page BEFORE filling
    agent-browser screenshot docs/visuals/auth/login-light.png

    agent-browser snapshot -i
    agent-browser fill @e1 "admin@test.com"
    agent-browser fill @e2 "TestPassword123!"
    agent-browser click @e3  # Login button
    agent-browser wait --load networkidle
fi
```

### Save Auth State

```bash
agent-browser state save docs/visuals/.auth-state.json
```

The `.auth-state.json` file is gitignored and contains session tokens.

---

## Phase 3: Capture Execution

For each requested flow, follow the capture pattern:

### Standard Capture Pattern

```bash
# 1. Navigate
agent-browser open "<url>"
agent-browser wait --load networkidle

# 2. Set viewport (desktop default)
agent-browser set viewport 1280 800

# 3. Wait for rendering
agent-browser wait 500

# 4. Capture light mode
agent-browser screenshot docs/visuals/<category>/<name>-light.png

# 5. Toggle dark mode
agent-browser snapshot -i
# Find and click theme toggle, or use JS:
agent-browser eval "document.documentElement.classList.add('dark')"
agent-browser wait 500

# 6. Capture dark mode
agent-browser screenshot docs/visuals/<category>/<name>-dark.png

# 7. Reset to light mode
agent-browser eval "document.documentElement.classList.remove('dark')"
```

### Responsive Capture Pattern

```bash
# Mobile (iPhone)
agent-browser set viewport 375 812
agent-browser wait 500
agent-browser screenshot docs/visuals/<category>/<name>-mobile.png

# Tablet (iPad)
agent-browser set viewport 768 1024
agent-browser wait 500
agent-browser screenshot docs/visuals/<category>/<name>-tablet.png

# Desktop
agent-browser set viewport 1280 800
agent-browser wait 500
agent-browser screenshot docs/visuals/<category>/<name>-desktop.png

# Large Desktop
agent-browser set viewport 1920 1080
agent-browser wait 500
agent-browser screenshot docs/visuals/<category>/<name>-desktop-lg.png
```

### Video Recording Pattern

```bash
agent-browser record start docs/visuals/<category>/<name>-flow.webm

# Perform steps with pauses for visibility
agent-browser open "<url>"
agent-browser wait --load networkidle
agent-browser wait 1000  # Pause for viewer

agent-browser snapshot -i
agent-browser click @e1
agent-browser wait 1000  # Pause for viewer

# ... more steps ...

agent-browser record stop
```

### Flow-Specific Instructions

See [references/flow-catalog.md](references/flow-catalog.md) for the complete catalog of every flow with exact URLs, steps, and expected screenshot filenames.

---

## Phase 4: Post-Processing

### Generate Visual Index

After all captures are complete, generate `docs/visuals/README.md`:

```bash
./templates/generate-visual-index.sh
```

Or manually create it — the index should:

1. List all captured images organized by category
2. Use inline markdown image syntax: `![Alt text](category/filename.png)`
3. Show light/dark comparisons side-by-side using HTML tables
4. Link to WebM videos (note: WebM doesn't render inline on GitHub)

### Optional: Convert WebM to GIF

If `ffmpeg` is available:

```bash
ffmpeg -i docs/visuals/auth/login-flow.webm \
  -vf "fps=10,scale=800:-1:flags=lanczos" \
  -loop 0 \
  docs/visuals/auth/login-flow.gif
```

Install ffmpeg if needed: `brew install ffmpeg`

### Optional: Update Existing Docs

Embed screenshots in the relevant documentation files:

| Doc File                              | Visuals to Add                 |
| ------------------------------------- | ------------------------------ |
| `docs/auth/overview.md`               | Login and setup screenshots    |
| `docs/admin/overview.md`              | Dashboard, sidebar screenshots |
| `docs/collections/overview.md`        | Collection list, create, edit  |
| `docs/storage/overview.md`            | Media library                  |
| `docs/plugins/analytics.md`           | Analytics dashboard            |
| `docs/plugins/seo.md`                 | SEO dashboard                  |
| `docs/admin/theme.md`                 | Light/dark comparison          |
| `docs/getting-started/quick-start.md` | Dashboard "what you get" hero  |
| `README.md`                           | Hero dashboard screenshot      |

Use relative paths from the doc file:

```markdown
![Admin Dashboard](../visuals/dashboard/dashboard-light.png)
```

---

## Phase 5: Verification

After all captures, verify the output:

Use the **Glob** tool (not `find` via Bash) to count and verify files:

1. Count screenshots: `Glob("docs/visuals/**/*.png")`
2. Count videos: `Glob("docs/visuals/**/*.webm")`
3. Count GIFs: `Glob("docs/visuals/**/*.gif")`
4. Check for zero-size files: `ls -la docs/visuals/**/*.png` and inspect sizes

Report a summary:

- Total screenshots captured
- Total videos recorded
- Any failed captures (zero-size files)
- Categories covered
- Any flows that couldn't be captured (e.g., plugin pages not enabled)

---

## Naming Conventions

| Pattern                    | Example                    | Description               |
| -------------------------- | -------------------------- | ------------------------- |
| `<subject>-light.png`      | `dashboard-light.png`      | Light theme screenshot    |
| `<subject>-dark.png`       | `dashboard-dark.png`       | Dark theme screenshot     |
| `<subject>-mobile.png`     | `dashboard-mobile.png`     | Mobile viewport (375px)   |
| `<subject>-tablet.png`     | `dashboard-tablet.png`     | Tablet viewport (768px)   |
| `<subject>-desktop.png`    | `dashboard-desktop.png`    | Desktop viewport (1280px) |
| `<subject>-desktop-lg.png` | `dashboard-desktop-lg.png` | Large desktop (1920px)    |
| `<subject>-flow.webm`      | `login-flow.webm`          | Video recording of flow   |
| `<subject>-flow.gif`       | `login-flow.gif`           | GIF (converted from WebM) |

All filenames use **kebab-case**, no spaces, no timestamps (idempotent overwrites).

---

## Browser Automation Options

### Option 1: agent-browser CLI (Default)

Best for headless, scriptable captures. Works without a GUI.

```bash
agent-browser open "http://localhost:4200/admin"
agent-browser screenshot docs/visuals/dashboard/dashboard-light.png
```

### Option 2: Claude-in-Chrome MCP

Best for interactive debugging and GIF creation (MCP has a built-in `gif_creator` tool).

```
mcp__claude-in-chrome__tabs_context_mcp({ createIfEmpty: true })
mcp__claude-in-chrome__navigate({ url: "http://localhost:4200/admin", tabId })
mcp__claude-in-chrome__computer({ action: "screenshot", tabId })
```

**Prefer agent-browser** for batch captures. Use Claude-in-Chrome when you need interactive exploration or the GIF creator.

---

## Deep-Dive Documentation

| Reference                                                              | When to Use                                        |
| ---------------------------------------------------------------------- | -------------------------------------------------- |
| [references/flow-catalog.md](references/flow-catalog.md)               | Complete catalog of every flow with URLs and steps |
| [references/capture-conventions.md](references/capture-conventions.md) | Naming, viewport sizes, format rules               |
| [references/troubleshooting.md](references/troubleshooting.md)         | Common issues and fixes                            |

## Ready-to-Use Templates

| Template                                                                 | Description                         |
| ------------------------------------------------------------------------ | ----------------------------------- |
| [templates/capture-flow.sh](templates/capture-flow.sh)                   | Generic page capture (light + dark) |
| [templates/capture-responsive.sh](templates/capture-responsive.sh)       | Capture at 4 breakpoints            |
| [templates/capture-crud-flow.sh](templates/capture-crud-flow.sh)         | Collection CRUD walkthrough         |
| [templates/record-video-flow.sh](templates/record-video-flow.sh)         | WebM video recording                |
| [templates/generate-visual-index.sh](templates/generate-visual-index.sh) | Generate docs/visuals/README.md     |

```bash
# Examples
./templates/capture-flow.sh http://localhost:4200/admin docs/visuals/dashboard dashboard
./templates/capture-responsive.sh http://localhost:4200/admin docs/visuals/responsive admin
./templates/capture-crud-flow.sh articles docs/visuals/collections
./templates/record-video-flow.sh http://localhost:4200/admin/login docs/visuals/auth login
./templates/generate-visual-index.sh
```
