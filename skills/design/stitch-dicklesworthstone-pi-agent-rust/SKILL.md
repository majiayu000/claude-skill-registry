---
name: stitch
description: Generate UI designs and frontend code with Google Stitch via MCP. Use when asked to create screens, mockups, UI designs, or generate frontend code from text descriptions. Supports desktop, mobile, and tablet layouts.
compatibility: Requires mcporter CLI and stitch-mcp configured (npx -y stitch-mcp)
metadata:
  homepage: https://stitch.googleapis.com
  author: Google
---

# Google Stitch — AI UI/UX Design Generation

Generate production-ready UI designs and frontend code using Google Stitch via MCP.

## Prerequisites

Verify stitch is configured:
```bash
mcporter list stitch
```

If missing, configure it:
```bash
# 1. Authenticate with Google Cloud
gcloud auth application-default login

# 2. Enable Stitch API
gcloud beta services mcp enable stitch.googleapis.com --project=YOUR_PROJECT_ID

# 3. Add to mcporter
mcporter config add stitch --stdio "npx -y stitch-mcp" --env GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
```

## Tools

| Tool | Purpose |
|------|---------|
| `list_projects` | List all projects |
| `create_project` | Create a project |
| `get_project` | Get project details |
| `list_screens` | List screens in a project |
| `get_screen` | Get screen details |
| `generate_screen_from_text` | Generate a screen from a prompt |
| `fetch_screen_code` | Download HTML/CSS code |
| `fetch_screen_image` | Download preview image |

## Workflows

### List Projects

```bash
mcporter call stitch.list_projects
mcporter call stitch.list_projects filter="view=owned"
mcporter call stitch.list_projects filter="view=shared"
```

### Create a Project

```bash
mcporter call stitch.create_project title="My App Design"
```

### Generate a Screen

```bash
mcporter call stitch.generate_screen_from_text \
  projectId="PROJECT_ID" \
  prompt="A modern dashboard with sidebar navigation, user stats cards, and a data table" \
  deviceType="DESKTOP" \
  modelId="GEMINI_3_PRO"
```

**Parameters:**
- `projectId` (required): Numeric project ID (e.g., `4651986810686364080`)
- `prompt` (required): UI description
- `deviceType`: `MOBILE` (default), `DESKTOP`, `TABLET`, or `AGNOSTIC`
- `modelId`: `GEMINI_3_FLASH` (default, 30–60s) or `GEMINI_3_PRO` (1–3min, higher quality)

**Generation takes 1–3 minutes. Do not retry.**

### List Screens

```bash
mcporter call stitch.list_screens projectId="PROJECT_ID"
```

### Get Screen Details

```bash
mcporter call stitch.get_screen projectId="PROJECT_ID" screenId="SCREEN_ID"
```

### Download Code

```bash
mcporter call stitch.fetch_screen_code projectId="PROJECT_ID" screenId="SCREEN_ID"
```

Returns self-contained HTML with Tailwind CSS.

### Download Image

```bash
mcporter call stitch.fetch_screen_image projectId="PROJECT_ID" screenId="SCREEN_ID"
```

Saves PNG to current directory; returns base64 data.

## Prompt Engineering

### Specify These Elements

- **Layout**: sidebar, header, grid, cards
- **Components**: buttons, forms, tables, modals
- **Content**: user data, charts, lists
- **Style**: minimal, corporate, playful, dark mode

### Strong Prompts

```
A settings page with a left sidebar showing navigation categories 
and a main content area with toggle switches for notifications, 
privacy settings, and account preferences. Dark mode.
```

```
An e-commerce product listing page with a search bar, filter sidebar 
on the left, and a 3-column grid of product cards showing image, 
title, price, and add-to-cart button.
```

### Weak Prompts

```
A nice website
```

```
Settings page
```

## Device Types

| Type | Resolution | Best For |
|------|------------|----------|
| `DESKTOP` | 1280×1024 | Full layouts, sidebars, wide tables |
| `MOBILE` | 390×844 | Single column, bottom nav, touch targets |
| `TABLET` | 768×1024 | Hybrid layouts |
| `AGNOSTIC` | Varies | Responsive components |

## Model Selection

- **GEMINI_3_FLASH**: 30–60 seconds. Use for iteration.
- **GEMINI_3_PRO**: 1–3 minutes. Use for final designs.

## Iteration Workflow

1. Create a project for your design system
2. Generate initial screens with FLASH for rapid iteration
3. Refine prompts based on output
4. Generate final versions with PRO
5. Extract code with `fetch_screen_code`

### Maintain Consistency

Reference existing designs in subsequent prompts:

```
Following the same design system as the dashboard (dark mode, 
Inter font, blue accent #137fec, rounded-lg corners), 
create a user profile page with...
```

## Response Handling

### generate_screen_from_text

Returns:
- `screenId`: Generated screen ID
- `output_components`: Feedback or suggestions

If `output_components` contains suggestions (e.g., "Yes, make them all"), present them to the user. If accepted, call `generate_screen_from_text` again with the suggestion as the prompt.

### Code Structure

Generated HTML includes:
- Tailwind CSS via CDN
- Custom Tailwind config (colors, fonts)
- Responsive classes
- Inline SVG icons

## Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `HTTP 401` | Expired auth | `gcloud auth application-default login` |
| `HTTP 403` | API disabled | `gcloud beta services mcp enable stitch.googleapis.com` |
| Timeout | Slow generation | Wait; check status with `get_screen` |
| `Project ID not found` | Missing env var | Set `GOOGLE_CLOUD_PROJECT` |

## Examples

### Complete Design Flow

```bash
# Create project
mcporter call stitch.create_project title="SaaS Dashboard"

# Generate dashboard
mcporter call stitch.generate_screen_from_text \
  projectId="NEW_PROJECT_ID" \
  prompt="A SaaS analytics dashboard: header with logo and user avatar, left sidebar with nav (Dashboard, Analytics, Users, Settings), main area with 4 stat cards (Revenue, Users, Orders, Growth) and a line chart" \
  deviceType="DESKTOP" \
  modelId="GEMINI_3_PRO"

# List screens
mcporter call stitch.list_screens projectId="NEW_PROJECT_ID"

# Download code
mcporter call stitch.fetch_screen_code projectId="NEW_PROJECT_ID" screenId="SCREEN_ID"
```

### Quick Mobile Mockup

```bash
mcporter call stitch.generate_screen_from_text \
  projectId="PROJECT_ID" \
  prompt="Mobile login screen: app logo at top, email and password fields, 'Forgot password?' link, primary 'Sign In' button, 'Don't have an account? Sign up' at bottom" \
  deviceType="MOBILE" \
  modelId="GEMINI_3_FLASH"
```
