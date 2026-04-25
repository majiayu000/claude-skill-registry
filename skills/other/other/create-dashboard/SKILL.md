---
name: create-dashboard
description: >
  Create a custom web dashboard (React + Vite + Express) inside your sandbox to visualize
  the agent's Turso database. The dashboard is served on port 3847 and the user sees it
  live in the "App" tab in Gooseworks. Use when the user asks for a dashboard,
  visualization, chart, metric view, or any custom UI powered by their agent's data.
tags: [content, design]
---

You are helping the user build a custom dashboard from the Gooseworks dashboard template.
The app must run on port `3847` from a single Express process that serves both API routes
and the built React UI so it appears in the Gooseworks App tab.

## Non-negotiable constraints

1. Always use the template workflow (React + Vite + Tailwind + Express). Do not rebuild this in another framework.
2. Use sandbox-agnostic paths via `$HOME` and `$HOME/workspace` only.
3. Keep the active project in `$HOME/dashboard` (outside the workspace mount).
4. Mirror only source files to `$HOME/workspace/dashboard-src` for persistence.
5. Never place dependencies, build output, or VCS metadata in the mirror.
6. Use one runtime port (`3847`) and one server process. No separate frontend dev server.

## State handling

Before editing, inspect:
- whether `$HOME/dashboard` exists
- whether `$HOME/workspace/dashboard-src` exists
- whether dependencies are already installed in `$HOME/dashboard`

Then follow this decision flow:
- Dashboard exists with dependencies: move to customization.
- Dashboard missing but mirror exists: restore from mirror into `$HOME/dashboard`, install deps, build, start server, verify health.
- Both missing: initialize from the official Gooseworks dashboard template, install deps, then continue.
- Dashboard exists without dependencies: install deps, then continue.

If template initialization fails because the template source is unavailable, tell the user to retry once it is available. Do not hand-roll a replacement template.

## Discovery and planning

Before coding:
1. Clarify what the user wants to visualize if unclear.
2. Inspect database schema with `query_database`:
   - list tables
   - inspect columns for relevant tables
3. If the request is vague, confirm a one-sentence implementation plan.

## Implementation guidance

Template structure to use:
- `server.js` for API routes and static serving.
- `src/App.tsx` for route registration.
- `src/components/Layout.tsx` for sidebar navigation entries.
- `src/pages/*` for page implementations.
- `src/lib/api.ts` (`runQuery`) for data access from pages.

For each new page:
1. Create a page component in `src/pages`.
2. Pull data using `runQuery` or a dedicated read-only API route when SQL becomes complex.
3. Add route wiring in `src/App.tsx`.
4. Add navigation in `src/components/Layout.tsx`.

Keep all dashboard endpoints read-only.

## Visual style rules

- Use the stone palette only (for example: `text-stone-*`, `border-stone-*`, `bg-stone-*`).
- Prefer compact typography (`text-xs` or `text-sm`) with `font-normal`.
- Keep borders minimal and avoid heavy shadows.
- For Recharts lines/grids, stay within the stone color family.

## Build, run, and verify

After changes:
1. Run a production build.
2. Restart the existing dashboard server process cleanly.
3. Start the server that serves both API and UI on `3847`.
4. Verify health via `/api/health`.

Interpret health:
- `ok=true` and `db=true`: dashboard is live.
- `db=false`: inform the user that agent DB credentials/config are missing and stop further DB-dependent work.

## Persistence to workspace mirror

After each successful change:
1. Ensure mirror destination is `$HOME/workspace/dashboard-src`.
2. Sync source files from `$HOME/dashboard` into the mirror.
3. Exclude dependency/build/VCS folders and files (for example dependency directory, build directory, and `.git`).
4. Verify mirror size stays small (roughly under 1 MB; if it grows very large, clean leaked heavy folders and sync again).

The mirror should include source and config files needed to recreate the project quickly after restart.

## Completion message

End with a direct status message that the dashboard is live in the App tab and ready for further edits.

## Iteration loop

For every follow-up tweak:
1. Edit relevant files in `$HOME/dashboard`.
2. Rebuild and restart the single server on `3847`.
3. Re-sync source-only files to `$HOME/workspace/dashboard-src`.
4. Tell the user the update is done and that the App tab will refresh.
