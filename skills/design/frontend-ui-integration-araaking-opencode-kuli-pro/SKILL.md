---
name: frontend-ui-integration
description: Implement or extend a user-facing workflow in a web application, integrating with existing backend APIs. Use when the feature is primarily a UI/UX change backed by existing APIs, affects only the web frontend, and requires following design system, routing, and testing conventions.
---
# Skill: Frontend UI integration

## Purpose

Implement or extend a user-facing workflow in our primary web application, integrating with **existing backend APIs** and following our **design system, routing, and testing conventions**.

## When to use this skill

- The feature is primarily a **UI/UX change** backed by one or more existing APIs.
- The backend contracts, auth model, and core business rules **already exist**.
- The change affects **only** the web frontend (no schema or service ownership changes).

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

- **Framework**: React with TypeScript.
- **Routing**: use the existing router and route layout patterns.
- **Styling**: use the in-house design system components (Buttons, Inputs, Modals, Toasts, etc.).
- **State management**: prefer the existing state libraries (e.g., React Query, Redux, Zustand) and follow established patterns.

## Required behavior

1. Implement the UI changes with **strong typing** for all props and API responses.
2. Handle loading, empty, error, and success states using existing primitives.
3. Ensure the UI is **keyboard accessible** and screen-reader friendly.
4. Respect feature flags and rollout mechanisms where applicable.

## Required artifacts

- Updated components and hooks in the appropriate feature module.
- **Unit tests** for core presentation logic.
- **Integration or component tests** for the new flow (e.g., React Testing Library, Cypress, Playwright) where the repo already uses them.
- Minimal **CHANGELOG or PR description text** summarizing the behavior change (to be placed in the PR, not this file).

## Implementation checklist

1. Locate the relevant feature module and existing components.
2. Confirm the backend APIs and types, updating shared TypeScript types if needed.
3. Implement the UI, wiring in API calls via the existing data layer.
4. Add or update tests to cover the new behavior and edge cases.
5. Run the required validation commands (see below).

## Verification

Run the following (adjust commands to match the project):

- `pnpm lint`
- `pnpm test -- --runInBand --watch=false`
- `pnpm typecheck` (if configured separately)

The skill is complete when:

- All tests, linters, and type checks pass.
- The new UI behaves as specified across normal, error, and boundary cases.
- No unrelated files or modules are modified.

## Safety and escalation

- If the requested change requires backend contract changes, **stop** and request a backend-focused task instead.
- If design references conflict with existing accessibility standards, favor accessibility and highlight the discrepancy in the PR description.
