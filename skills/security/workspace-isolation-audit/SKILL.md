---
name: workspace-isolation-audit
description: Use when asked to audit or fix Supabase queries to ensure every query filters by workspace_id and workspace access is validated.
---

Goal: ensure multi-tenant isolation by enforcing `workspace_id` filtering everywhere it applies.

Workflow:

1. Identify affected scope
   - Ask which feature/agent/API route is in scope if unclear.
   - Prefer targeted fixes over repo-wide refactors.

2. Find candidate queries
   - Search for `.from(` usage in the relevant area.
   - Look for missing `.eq("workspace_id", workspaceId)` (or equivalent RLS-safe filter).

3. Verify workspace context
   - API routes: read `workspaceId` from `req.nextUrl.searchParams`, validate via `validateUserAndWorkspace`.
   - Agents: use `task.workspace_id` (required); do not derive workspace from auth user id.
   - Server helpers: ensure functions accept `workspaceId` explicitly rather than importing globals.

4. Fix and harden
   - Add the required filter.
   - Add or update targeted tests for the modified behavior.

5. Validate
   - Run `npm run typecheck`.
   - Run the most targeted tests that cover the change (Vitest/Playwright depending on area).

