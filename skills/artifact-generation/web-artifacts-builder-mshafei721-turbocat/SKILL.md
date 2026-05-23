---
name: web-artifacts-builder
description: Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use for complex artifacts requiring state management, routing, or shadcn/ui components - not for simple single-file HTML/JSX artifacts.
---

# Web Artifacts Builder

## Overview

Build sophisticated web artifacts using React, TypeScript, Tailwind CSS, and shadcn/ui components.

## Technology Stack

- React 18
- TypeScript
- Vite
- Parcel (bundling)
- Tailwind CSS
- shadcn/ui components

## Workflow

### 1. Initialize Project

```bash
scripts/init-artifact.sh <project-name>
```

Creates a fully configured React project with all dependencies.

### 2. Develop

Modify generated files using the pre-configured stack:
- React components in `src/`
- Tailwind styles
- shadcn/ui components

### 3. Bundle

```bash
scripts/bundle-artifact.sh
```

Consolidates the React application into a single self-contained HTML file with all dependencies inlined.

### 4. Deploy

Share the bundled HTML as a claude.ai artifact.

## Design Guidance

**Avoid "AI slop" aesthetics:**
- No excessive centered layouts
- No purple gradients
- No uniform rounded corners
- No Inter font everywhere

**Instead:**
- Bold, intentional design choices
- Context-specific styling
- Unique typography
- Purposeful color choices

## Features

- TypeScript path aliases support
- Asset inlining for self-contained output
- All dependencies bundled
- Production-ready artifacts

## When to Use

Use this skill for:
- Complex multi-component artifacts
- State management requirements
- Routing needs
- shadcn/ui component integration

**NOT for:**
- Simple single-file HTML
- Basic JSX without state
