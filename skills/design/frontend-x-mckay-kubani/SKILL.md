---
name: frontend
description: UI design guidelines for Kubani web interfaces. Use when building or reviewing web components, pages, or the Kubani dashboard.
---

# Frontend Development

Guidelines for building Kubani web interfaces.

## Tech Stack

- **Framework**: Next.js (React)
- **UI**: Tailwind CSS, Radix UI primitives
- **State**: React Query for server state
- **Location**: `ui/`

## Design Principles

- **Distinctive design**: Avoid generic "AI slop" aesthetics — no default Inter/Roboto, no cliched purple gradients
- **Bold choices**: Pick a clear aesthetic direction and commit to it
- **Typography**: Choose distinctive fonts that match the context
- **Motion**: Use CSS animations and transitions for micro-interactions
- **Accessibility**: Follow WCAG 2.1 AA guidelines

## Kubani Dashboard Components

The main UI provides:
- Agent monitoring (status, health, versions)
- Skill browser and management
- Learning visualization (critic evaluations, reflections)
- Deployment management
- Temporal workflow visibility

## Guidelines

When building frontend components:
1. Match existing patterns in `ui/`
2. Use Tailwind utility classes consistently
3. Keep components small and composable
4. Use server components where possible (Next.js)
5. Test with React Testing Library
