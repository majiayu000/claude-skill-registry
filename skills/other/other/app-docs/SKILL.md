---
name: app-docs
description: "Generate complete user documentation for a web app with screenshots. Browses the app via browser automation, screenshots every screen, and produces a structured user guide with step-by-step instructions. Supports quick (key screens only), standard (all pages), and thorough (all states, mobile, every workflow) depths. Triggers: 'document the app', 'user guide', 'app documentation', 'screenshot docs', 'generate user docs', 'help docs', 'how-to guide'."
compatibility: claude-code-only
---

# App Documentation Generator

Browse a running web app, screenshot every screen, and produce a complete user guide. The documentation is generated from the **actual app**, not from specs or assumptions.

## Browser Tool Detection

Before starting, detect available browser tools:

1. **Chrome MCP** (`mcp__claude-in-chrome__*`) — preferred for authenticated apps
2. **Playwright MCP** (`mcp__plugin_playwright_playwright__*`) — for public apps
3. **playwright-cli** — for scripted flows

If none are available, inform the user and suggest installing Chrome MCP or Playwright.

## Depth Levels

| Depth | Screenshots | Coverage | Duration |
|-------|------------|----------|----------|
| **quick** | ~10 | Main 3-5 screens, happy path | 10-15 min |
| **standard** | ~30 | All pages, primary workflows | 30-60 min |
| **thorough** | ~80+ | All pages, all states, mobile views, every CRUD flow | 1-3 hours |

Default: **standard**

## Workflow

### 1. Get App Details

Ask the user:
- **App URL** (required)
- **App name** (for the guide title)
- **Auth** — do they need to log in? Chrome MCP uses their session; Playwright needs credentials
- **Depth** — quick, standard, or thorough
- **Audience** — who will read this guide? (end users, admins, new team members)

### 2. Discover All Routes

Navigate the app and build a page inventory:
- Read the sidebar/navigation menu
- Click through all top-level items
- Note sub-pages and nested navigation
- Check for settings, profile, admin areas
- Record the URL and purpose of each page

Create a task list to track documentation progress.

### 3. Document Each Page

For each page in the inventory:

#### a. Navigate and Orient
- Navigate to the page
- Wait for data to load (no skeleton/spinner in screenshot)
- Resize browser to 1280x720 for consistent screenshots

#### b. Screenshot Default State
- Take a clean screenshot showing the page with realistic data
- Save to `docs/screenshots/` with descriptive names: `01-dashboard.png`, `02-contacts-list.png`

#### c. Describe the Page
Write a section covering:
- **What this page is for** — one sentence
- **What the user can see** — key data, status indicators, navigation elements
- **What the user can do** — actions available (buttons, forms, filters)

#### d. Document Key Workflows
For interactive pages, document step-by-step:
1. Screenshot the starting state
2. Perform the action (click button, fill form)
3. Screenshot each significant step
4. Screenshot the result/confirmation
5. Write numbered steps matching the screenshots

#### e. Depth-Specific Extras

| Extra | quick | standard | thorough |
|-------|-------|----------|----------|
| Empty states | Skip | Note if present | Screenshot and document |
| Error states | Skip | Note if present | Trigger and screenshot |
| Dark mode | Skip | Skip | Screenshot every page |
| Mobile view (375px) | Skip | Skip | Screenshot every page |
| All CRUD operations | Skip | Primary only | Every operation with screenshots |
| Settings/config pages | Skip | Document | Document all options |

### 4. Organise the Guide

Group pages into logical sections. Common groupings:

```markdown
# [App Name] User Guide

## Getting Started
- Accessing the app (URL, login)
- Dashboard overview
- Navigation guide

## [Core Feature 1: e.g. Contact Management]
### Viewing contacts
### Adding a new contact
### Editing contact details
### Deleting a contact
### Searching and filtering

## [Core Feature 2: e.g. Reports]
### Viewing reports
### Creating a report
### Exporting data

## [Core Feature 3: e.g. Settings]
### Profile settings
### Team management
### Preferences

## Tips and Shortcuts
- Keyboard shortcuts (if any)
- Bulk actions
- Filters and search tips

## Troubleshooting
- Common issues noticed during documentation
- Error messages and what they mean
```

### 5. Write the Output

**Screenshots**: `docs/screenshots/NN-description.png` (numbered for order)

**User guide**: `docs/USER_GUIDE.md` with:
- Relative image paths: `![Dashboard](screenshots/01-dashboard.png)`
- Step-by-step numbered lists for workflows
- Tables for reference data (keyboard shortcuts, settings options)
- Admonitions for important notes: `> **Note:** ...`

**Optional HTML version**: If the user wants a hosted version, generate a single HTML file with embedded images (base64) or relative image paths, styled with Tailwind CDN.

## Screenshot Conventions

- **Resolution**: 1280x720 (desktop), 375x812 (mobile if thorough)
- **Naming**: `NN-section-description.png` (e.g. `01-dashboard-overview.png`, `05-contacts-add-form.png`)
- **Content**: Wait for data to load. No spinners, no skeleton screens in final shots.
- **Annotations**: If a screenshot needs callouts, describe them in the markdown text below the image rather than editing the image
- **Save location**: `docs/screenshots/` in the project root

## Autonomy Rules

- **Just do it**: Navigate pages, take screenshots, read page content
- **Brief confirmation**: Before writing docs to files
- **Ask first**: Before submitting forms, before clicking delete, before entering credentials
- **Thorough mode**: Same as above but skip confirmation for writing files and filling forms with test data

## Quality Rules

1. **Document what the app actually does**, not what you think it should do
2. **Every screenshot must have context** — don't just dump images without explanation
3. **Write for the audience** — admin docs are different from end-user docs
4. **Number screenshots chronologically** — so they make sense when viewed in a file browser
5. **Note gaps** — if a feature seems incomplete or confusing, note it (this is feedback for the developer)
6. **Keep steps atomic** — one action per numbered step
