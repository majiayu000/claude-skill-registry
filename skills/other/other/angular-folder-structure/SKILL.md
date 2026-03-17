---
name: angular-folder-structure
description: Define, audit, and enforce an Angular 20 Feature-first + Shared + Core folder architecture with clear pages/templates/components boundaries, lazy feature routing, and deterministic data-access placement. Use when users ask to create folder structure, refactor app architecture, review Angular project organization, standardize scalable boundaries, or prepare codebases for lazy loading, microfrontends, and library extraction.
---

# Angular Folder Structure (Angular 20)

## Purpose

Apply a deterministic, scalable Angular 20 architecture that separates concerns across:

- Features (business domains)
- Pages (route containers)
- Templates (composition/layout building blocks)
- Shared UI (reusable presentational components)
- Core (app-wide infrastructure and singletons)

Use this skill when creating a new structure, auditing an existing one, or migrating from a flat/layer-only layout.

## Inputs

Collect or infer before changes:

- Angular workspace path and target app (`src/app` root)
- Current structure state (existing folders and route layout)
- Whether this is: `greenfield`, `refactor`, or `audit-only`
- Whether standalone routing is already in use
- Team constraints (for example: keep existing feature names, avoid moving tests now)

If required context is missing, ask one focused clarification question, then continue.

## Target Structure

```text
src/
  app/
    app.config.ts
    app.routes.ts

    core/                          # App-wide infrastructure (singleton, cross-cutting)
      bootstrap/
      config/
      guards/
      interceptors/
      error-handling/
      http/
      logging/
      services/                    # singleton services (not feature-specific)
      state/                       # global state (if used)
      utils/

    shared/                        # Reusable building blocks (UI + helpers)
      ui/                          # presentational components
        components/
        directives/
        pipes/
      layout/                      # app-agnostic layout building blocks
        components/
        templates/
      form/                        # form controls, validators, form utilities
        components/
        validators/
      data-access/                 # reusable API clients/repos (if not in core)
        clients/
        models/
      styles/                      # global styles: tokens, mixins, tailwind layers
      testing/                     # test utilities: mocks, factories, helpers

    features/                      # business features (vertical slices)
      auth/
        pages/                     # routed pages for this feature
        components/                # feature-only UI pieces
        templates/                 # feature compositions (list+filters+toolbar etc.)
        data-access/               # feature API, facades, state, queries
          api/
          models/
          store/
        domain/                    # pure business rules (optional)
        routes.ts                  # feature routes (lazy)
        index.ts                   # public feature exports

      dashboard/
        pages/
        components/
        templates/
        data-access/
        routes.ts

    pages/                         # optional: app-level pages without a dedicated feature
      not-found/
      forbidden/

    shell/                         # app shell (top-level layout + router outlets)
      layout/
      routes.ts

    libs/                          # optional: internal libraries inside the app
      rest-api/                    # generated OpenAPI clients
      design-tokens/               # tokens, theme adapters
      ui-kit/                      # reusable component library

  assets/
  environments/
  styles/                          # global entry styles (tailwind, theme entrypoints)
  main.ts
```

## Workflow (Must Follow)

### Step 1: Preflight and classify

1. Confirm Angular app root exists (`src/app`).
2. Detect current style:
   - feature-first
   - layer-first
   - mixed/hybrid
3. Record blockers (missing routes, ambiguous feature ownership, cyclic imports).
4. Choose mode:
   - `greenfield`: create structure in place
   - `refactor`: move folders/files with compatibility shims as needed
   - `audit-only`: produce actionable report without moving files

### Step 2: Design target map before moving files

1. Define or confirm feature list (`auth`, `dashboard`, `orders`, etc.).
2. Map each existing module/component/service to one destination folder.
3. Flag conflicts:
   - file used by multiple features
   - service incorrectly placed in `shared` or `core`
   - route container mixed with presentational component
4. Write a migration map (source -> target) before edits.

### Step 3: Enforce folder boundaries

Apply these boundary rules:

- `features/`: vertical business slices with local routes, UI, and data-access
- `shared/`: reusable presentational assets and cross-feature helpers only
- `core/`: app-wide singleton infrastructure only
- `pages/`: app-level routed pages not owned by a feature
- `shell/`: top-level application layout and router host

Never allow:

- imports from `features/` into `shared/`
- imports from any feature into `core/`
- feature-to-feature deep imports (prefer public API or shared abstraction)
- business logic inside `shared/ui`

### Step 4: Place routes and data-access deterministically

1. Keep per-feature route declarations in `features/<feature>/routes.ts`.
2. Lazy-load feature routes by default.
3. Place feature API/state/facade logic in `features/<feature>/data-access`.
4. Keep feature models local unless proven shared across features.
5. Use `shared/data-access` only for truly cross-feature clients/models.

### Step 5: Validate roles for page/template/component layers

Enforce:

- `pages`: route containers, orchestration, param handling
- `templates`: composition/layout assembly blocks
- `components`: smaller UI units, either feature-local or shared

If a file mixes concerns, split it before or during relocation.

### Step 6: Produce migration output

Provide:

- final tree snapshot (or proposed tree for audit-only)
- move list (old path -> new path)
- boundary violations fixed
- remaining risks and deferred items
- verification checklist result

## Conventions (Must Follow)

### Dependency boundaries

- Never import from `features/` into `shared/`.
- Allow features to import from `core/`, but avoid importing feature code into `core/`.
- Prefer feature-local dependencies; depend on `shared/` and `core/` instead of other features.

### Data access and state

- Place API/state/facade logic in `features/*/data-access`.
- Keep models close to usage.
- Place feature-specific models in `features/<feature>/data-access/models`.
- Place globally shared models in `shared/data-access/models` only when truly shared.

### Domain layer (optional)

Create `features/*/domain` only when real business rules exist:

- pure functions
- policies and validators
- decision logic independent of Angular

### Internal libraries (optional)

Use `libs/` only when package-like separation is needed:

- generated API clients
- design tokens and theme adapters
- reusable UI kit

## Verification Gates (Required)

A run is complete only when all checks pass:

1. Every business domain exists under `features/` with local `routes.ts` (unless explicitly exempted).
2. `shared/` contains no feature-specific business logic.
3. `core/` contains only app-wide singleton/cross-cutting concerns.
4. Route containers, templates, and components follow their defined responsibilities.
5. No forbidden import direction exists (`features -> shared` only, not inverse; no `feature -> core` reverse coupling).
6. Data-access placement is consistent with local-first model ownership.

## Assistant Portability Rules

- Base all decisions on repository structure and config files, not tool-specific project views.
- Keep migration steps explicit and reversible; do not apply broad inferred moves without a source-to-target map.
- When ownership is ambiguous, ask one focused clarification question, then continue deterministically.

## Expected Outcomes

Applying this structure should produce:

- cleaner ownership per team and feature
- easier refactors with predictable boundaries
- consistent UI decomposition (pages/templates/components)
- sustainable growth for large apps and future architecture changes

## Quick Usage Prompts

- "Refactor this Angular 20 app to feature-first structure and keep routes lazy."
- "Audit our current folder structure and list boundary violations without moving files."
- "Design an initial Angular folder architecture for auth, dashboard, and orders features."

## References

[1]: https://angular.dev/style-guide
[2]: https://angular.dev/guide/routing
[3]: https://angular.dev/guide/routing/common-router-tasks#lazy-loading
