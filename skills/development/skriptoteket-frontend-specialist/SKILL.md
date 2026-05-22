---
name: skriptoteket-frontend-specialist
description: Skriptoteket frontend development (FastAPI backend + full Vue/Vite SPA) using the HuleEdu-aligned stack (Vue 3.5.x + Vite + TypeScript, Pinia, Vue Router, Tailwind CSS v4 tokens/@theme, HuleEdu design tokens, pnpm). Use for working in the `frontend/` pnpm workspace, SPA hosting/history fallback, implementing SPA features (auth, routing, state, API clients), and keeping the UI/auth model compatible with future HuleEdu teacher login integration (same entry point, no separate login).
---

# Skriptoteket Frontend Specialist

## Defaults

- SPA-only: do not re-introduce template/HTMX UI (ADR-0027 clean-break cutover).
- Use Vue 3.5 Composition API with `<script setup lang="ts">`.
- Keep the frontend HuleEdu-aligned so it can be integrated into HuleEdu later (shared design tokens and compatible auth model).
- Keep integration costs low: avoid hardcoded base paths, isolate auth transport (cookie vs bearer), and prefer token-driven styling over bespoke CSS.
- Styling is tokens-first: `tokens.css` (canonical `--huleedu-*`) + `tailwind-theme.css` (Tailwind bridge via `@theme inline`).
- Single CSS entry point: `frontend/apps/skriptoteket/src/assets/main.css` (imports Tailwind + tokens + theme once).
- Use SPA primitives from `frontend/apps/skriptoteket/src/assets/main.css` to avoid drift:
  - Buttons: `.btn-primary`, `.btn-cta`, `.btn-ghost`
  - Panels (nested): `.panel-inset`, `.panel-inset-canvas`
  - Toasts: `.toast-*` (via `ToastHost`)
  - Inline messages: `.system-message*` (via `SystemMessage`)
  - Badges: `.status-pill`
- No stacked brutal shadows: only the outermost “card/panel” gets `shadow-brutal*`. Nested panels/fields inside a
  shadowed surface use `shadow-none` + thicker, uniform borders (`panel-inset*`, or `border-2 border-navy/20`).
- No Tailwind default palette leakage in product UI: avoid `bg-slate-*`, `text-gray-*`, etc. Prefer token-mapped utilities (`bg-canvas`, `text-navy`, `shadow-brutal-sm`) or CSS variables.
- Page/editor transitions: prefer opacity-only transitions (hard borders/shadows shimmer when translated).
- Admin editor features: extract logic into `frontend/apps/skriptoteket/src/composables/editor/` and keep views UI-only.

## Repo map (Skriptoteket monolith)

- Backend (FastAPI + SPA hosting + APIs): `src/skriptoteket/web/`
  - Static assets: `src/skriptoteket/web/static/` (`/static/*`)
  - Built SPA assets: `src/skriptoteket/web/static/spa/` (served via history fallback)
- Frontend workspace (pnpm): `frontend/`
  - SPA app: `frontend/apps/skriptoteket/`
  - (Legacy) islands: `frontend/islands/`

## Workflow

1. Work from the repo root:
   - Backend dev: `pdm run dev` (or `pdm run dev-logs` for log piping)
   - Frontend install: `pdm run fe-install`
   - SPA dev server: `pdm run fe-dev` (or `pdm run fe-dev-logs` for log piping)
   - Local combo (backend + SPA): `pdm run dev-local`
   - Container dev: `pdm run dev-start` (logs: `pdm run dev-containers-logs`, rebuild: `pdm run dev-rebuild`)
   - SPA tests: `pdm run fe-test` (Vitest), `pdm run fe-type-check`, `pdm run fe-lint`
2. Implement in this order:
   - OpenAPI models (backend) -> regenerate TypeScript types (`pdm run fe-gen-api-types`)
   - API client calls in SPA
   - Pinia stores for shared state, views/components for UI
3. Keep styling token-driven and HuleEdu-compatible (ADR-0032 + `@theme inline` bridge).
4. Keep auth integration "pluggable" so HuleEdu SSO can be added without rewriting the SPA (ADR-0006/ADR-0011 + current cookie/CSRF transport).

## Patterns

### Pinia state

- Define stores with `defineStore(...)`; keep state/actions cohesive and typed.
- Avoid destructuring the store object; use `storeToRefs(store)` when you need refs.
- Centralize auth/session state in one store and let router guards depend on it.

### Routing + hosting

- Use history mode routing with server-side fallback (backend serves `index.html` for non-API routes).
- Avoid hardcoding absolute paths; keep router base aligned with Vite `base`.

### API contracts

- Treat OpenAPI as the source of truth and generate TypeScript types via `openapi-typescript`.
- Keep response/error envelopes consistent; handle 401/403 centrally.

### Auth (integration-ready)

- Current Skriptoteket reality: cookie-session auth + CSRF for mutating requests.
- Future HuleEdu integration: identity federation without shared authorization (keep Skriptoteket roles local).
- In the SPA, isolate auth transport details behind a small adapter (cookie vs bearer) so the UI can run in both modes.

### Layout + editor ergonomics

- Full-height editor routes:
  - Wrap route content in `route-stage` + `route-stage-item` (see `frontend/apps/skriptoteket/src/App.vue`).
  - Use `route-stage--editor` for editor routes so nested flex/grid children can use `min-h-0`.
  - In authenticated layout, use the editor variant (`auth-main-content--editor`) to avoid double scrollbars and let the
    editor manage its own scroll regions (see `frontend/apps/skriptoteket/src/components/layout/AuthLayout.vue`).
- Focus mode (width matters):
  - Persisted per user via `useLayoutStore` (`frontend/apps/skriptoteket/src/stores/layout.ts`).
  - Editor is the primary entry point for toggling; ensure the user is never “trapped” without an exit control.
- Drawers:
  - Reuse the existing right-side drawer surface for editor chat/history; don’t introduce a second sidebar.
  - Prefer `bg-canvas` + `border-navy` + `shadow-brutal-sm` for drawer frames (see `EditorWorkspacePanel.vue`).
- Dense toolbars:
  - Use the editor micro-typography pattern: `text-[10px] font-semibold uppercase tracking-wide text-navy/60`.
  - Use `.btn-ghost` with size/shadow overrides for 28px controls (see `EditorWorkspaceToolbar.vue`).

### Testing (Vitest)

- Config: `frontend/apps/skriptoteket/vitest.config.ts`
- Setup: `frontend/apps/skriptoteket/src/test/setup.ts`
- Tests: `frontend/apps/skriptoteket/src/**/*.spec.ts` (colocate with code)
- Commands: `pdm run fe-test` / `pdm run fe-test-watch` / `pdm run fe-test-coverage`
- Prefer testing pure helpers/composables and mocking HTTP via `vi.mock` rather than snapshot-heavy component tests.

## HuleEdu compatibility checklist

- Versions: Vue 3.5.x / Pinia 3.x / Vue Router 4.6.x / Vite 6.x (match HuleEdu minor lines).
- Paths: use `import.meta.env.BASE_URL` + relative URLs so the SPA can be hosted under a subpath.
- Auth: handle 401 centrally; do not assume a separate Skriptoteket login UI exists in "integrated" mode.
- Styling: use HuleEdu tokens as the contract; avoid hard-coded colors/fonts.

## Context7 lookups

Use Context7 when you need exact API details or version-specific behavior:

- Vue 3 docs: `/vuejs/docs` (Composition API, `<script setup>`)
- Pinia docs: `/vuejs/pinia` (setup stores, TypeScript, best practices)
- Vue Router docs: `/vuejs/vue-router` (route meta, guards)
- Vite v6 docs: `/websites/v6_vite_dev` (config, proxy, dev server)
- Tailwind v4 docs: `/websites/tailwindcss` (theme variables, `@theme`, `@reference`)
- Vitest v4 docs: `/vitest-dev/vitest/v4.0.7` (mocking, `vi.mock`, `vi.mocked`)

## References

- SPA adoption: `docs/adr/adr-0027-full-vue-vite-spa.md`
- SPA hosting + history fallback: `docs/adr/adr-0028-spa-hosting-and-history-fallback.md`
- OpenAPI + TS generation: `docs/adr/adr-0030-openapi-and-frontend-types.md`
- Tailwind v4 tokens bridge: `docs/adr/adr-0032-tailwind-4-theme-tokens.md`
- Testing runbook: `docs/runbooks/runbook-testing.md`
- SPA design system rules: `.agent/rules/045-huleedu-design-system.md`
- Testing standards: `.agent/rules/070-testing-standards.md`
