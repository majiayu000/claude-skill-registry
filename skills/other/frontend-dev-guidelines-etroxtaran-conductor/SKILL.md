---
name: frontend-dev-guidelines
description: Standards for React / TypeScript development
version: 1.1.0
tags: [react, frontend, best-practices]
owner: frontend
status: active
---

# Frontend Dev Guidelines Skill

## Overview

Provide React/TypeScript implementation standards for consistent UI behavior.

## Usage

```
/frontend-dev-guidelines
```

## Identity
**Role**: Frontend Lead
**Objective**: Guide the implementation of React components and logic to ensure consistency, performance, and accessibility.

## Tech Stack
- **Framework**: React 18+
- **Language**: TypeScript
- **State**: TanStack Query (Server State), Zustand (Client State).
- **Styling**: Tailwind CSS or CSS Modules (check `package.json`).
- **Routing**: TanStack Router or React Router.

## Rules

### 1. Component Structure
**Feature-based Folders**:
```
src/features/auth/
  ├── components/    # Dumb UI components
  ├── hooks/         # Custom hooks
  ├── api/           # Fetchers
  └── routes/        # Route defs
```
**Generic UI**: `src/components/ui` (Buttons, Inputs).

### 2. Rendering & Effects
- **No `useEffect` for Data Fetching**: Use `useQuery`.
- **No Derived State in `useState`**: Calculate it during render.
  - Bad: `const [fullName, setFullName] = useState(f + l)`
  - Good: `const fullName = firstName + " " + lastName`

### 3. Accessibility (A11y)
- **Semantic HTML**: `<button>` not `<div onClick>`.
- **Forms**: Labels are mandatory (`htmlFor`).
- **Interaction**: Keyboard navigable.

## Workflow

### Feature Implementation
1.  **Route**: Define the route.
2.  **State**: Define the data requirements (Zod Schemas).
3.  **UI**: Build components (Mobile-First responsive).
4.  **Integration**: Wire up `useQuery`.

## Error Handling
- **Boundaries**: Wrap features in `ErrorBoundary`.
- **Fallbacks**: Always have Loading and Error states in UI.

## Outputs

- Frontend implementation aligned with UI and accessibility standards.

## Related Skills

- `/ui-design-system` - Design system reference
