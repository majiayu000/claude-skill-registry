---
name: web-artifacts-builder
description: Suite of tools for creating elaborate, multi-component web applications using modern frontend technologies (React, Tailwind CSS, shadcn/ui). Use for complex apps requiring state management, routing, or shadcn/ui components.
---

# Web Artifacts Builder

Build powerful self-contained frontend applications:
1. Initialize the project using `scripts/init-artifact.sh`
2. Develop the application by editing the generated code
3. Bundle all code into a single HTML file using `scripts/bundle-artifact.sh`
4. Deliver to user
5. (Optional) Test the output

**Stack**: React 18 + TypeScript + Vite + Parcel (bundling) + Tailwind CSS + shadcn/ui

## Design & Style Guidelines

Avoid generic "AI slop": no excessive centered layouts, purple gradients, uniform rounded corners, or Inter font.

## Quick Start

### Step 1: Initialize Project

```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

This creates a fully configured project with:
- ✅ React + TypeScript (via Vite)
- ✅ Tailwind CSS 3.4.1 with shadcn/ui theming system
- ✅ Path aliases (`@/`) configured
- ✅ 40+ shadcn/ui components pre-installed
- ✅ All Radix UI dependencies included
- ✅ Parcel configured for bundling (via .parcelrc)

### Step 2: Develop

Edit the generated files. See **Common Development Tasks** below for guidance.

### Step 3: Bundle to Single HTML File

```bash
bash scripts/bundle-artifact.sh
```

Creates `bundle.html` — a self-contained file with all JavaScript, CSS, and dependencies inlined.

**What the script does**:
- Installs bundling dependencies (parcel, html-inline)
- Creates `.parcelrc` config with path alias support
- Builds with Parcel (no source maps)
- Inlines all assets into single HTML

### Step 4: Deliver

Share the bundled HTML file with the user.

### Step 5: Testing (Optional)

Use Playwright or browser tools to verify the output. Avoid testing upfront unless issues arise.
