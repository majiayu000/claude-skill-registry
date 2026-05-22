---
name: svelte-ui-integration
description: Implement or extend user-facing workflows in SvelteKit applications with full-stack capabilities. Specialized in SvelteKit's load functions, form actions, and progressive enhancement. Use when the feature is primarily a UI/UX change backed by existing APIs, affects only the web frontend, and requires following SvelteKit conventions.
---
# SvelteKit UI Integration

## Purpose

Implement or extend user-facing workflows in SvelteKit applications, leveraging **SvelteKit's full-stack capabilities** including load functions, form actions, and API routes. Follow **SvelteKit conventions** for routing, state management, and progressive enhancement.

## When to use this skill

- The feature is primarily a **UI/UX change** leveraging SvelteKit's architecture.
- Building progressive enhancement with server-side rendering and client-side interactivity.
- The backend contracts, auth model, and core business rules **already exist** or will be implemented as SvelteKit API routes.
- The change affects **only** the SvelteKit application (no external service changes).

## Inputs

- **Feature description**: short narrative of the user flow and outcomes.
- **Relevant APIs**: endpoints, request/response types, and links to source definitions.
- **Target routes/components**: paths, component names, or feature modules.
- **Design references**: Figma links or existing screens to mirror.
- **Guardrails**: performance limits, accessibility requirements, and any security constraints.

## Out of scope

- Creating new backend services or changing persistent data models.
- Modifying authentication/authorization flows.
- Introducing new frontend frameworks or design systems.

## Conventions

- **Framework**: SvelteKit with TypeScript.
- **Routing**: use SvelteKit's file-based routing with `+layout.svelte`, `+page.svelte`, and `+page.server.ts`.
- **Styling**: Use shadcn-svelte, Skeleton UI, or Melt UI components (via `shadcn-svelte-management` skill) or the in-house design system components.

When using UI components, invoke the `shadcn-svelte-management` skill to:
- Discover available Svelte components
- Get component installation commands
- Choose appropriate component library (shadcn-svelte, Skeleton UI, Melt UI)
- **State management**: prefer Svelte stores, reactive statements, and SvelteKit's form actions.
- **Data fetching**: use SvelteKit load functions for server-side data and progressive enhancement.

## Required behavior

1. Implement the UI changes with **strong typing** for all props, load function data, and form actions.
2. Handle loading, empty, error, and success states using SvelteKit's `$page.form` and reactive statements.
3. Ensure the UI is **keyboard accessible** and screen-reader friendly with proper ARIA attributes.
4. Leverage SvelteKit's progressive enhancement - works without JavaScript, enhanced with it.
5. Respect feature flags and rollout mechanisms where applicable.

## Required artifacts

- Updated components and actions in the appropriate feature module (`src/lib/components/`).
- **Load functions** in `+page.server.ts` or `+layout.server.ts` for server-side data.
- **Form actions** for handling form submissions with progressive enhancement.
- **Unit tests** for core presentation logic and Svelte stores.
- **Integration or component tests** for the new flow (e.g., Svelte Testing Library, Cypress, Playwright) where the repo already uses them.
- Minimal **CHANGELOG or PR description text** summarizing the behavior change (to be placed in the PR, not this file).

## Implementation checklist

1. Locate the relevant feature module and existing components in `src/lib/components/`.
2. Confirm the backend APIs and types, updating shared TypeScript types if needed.
3. Implement the UI with SvelteKit patterns:
   - Use `+page.server.ts` for server-side data loading
   - Use form actions for POST/PUT/DELETE operations
   - Leverage `+layout.svelte` for shared UI elements
   - Implement progressive enhancement
4. Add or update tests to cover the new behavior and edge cases.
5. Run the required validation commands (see below).

## Verification

Run the following (adjust commands to match the project):

- `pnpm lint`
- `pnpm test -- --runInBand --watch=false`
- `pnpm check` (SvelteKit type checking)
- `pnpm build` (to verify production build)
- `pnpm preview` (test production build locally)

The skill is complete when:

- All tests, linters, and type checks pass.
- The new UI behaves as specified across normal, error, and boundary cases.
- Progressive enhancement works (functional without JavaScript).
- Form submissions work with and without JavaScript.
- No unrelated files or modules are modified.

## Safety and escalation

- If the requested change requires external backend contract changes, **stop** and request a backend-focused task instead.
- If design references conflict with existing accessibility standards, favor accessibility and highlight the discrepancy in the PR description.
- Always implement with progressive enhancement in mind - ensure functionality works without JavaScript.
