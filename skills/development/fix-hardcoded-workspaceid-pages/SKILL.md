---
name: fix-hardcoded-workspaceid-pages
description: Use when asked to remove hardcoded workspaceId values from client pages and replace them with useWorkspace() + friendly loading/error states.
---

Goal: remove hardcoded `workspaceId` values from client-side pages and use `useWorkspace()` instead.

Workflow:

1. Locate hardcoded workspace IDs
   - Search for `workspaceId =` and the sentinel UUID `00000000-0000-0000-0000-000000000000`.

2. Replace with `useWorkspace()`
   - Import `useWorkspace` from `@/hooks/useWorkspace`.
   - Destructure `{ workspaceId, loading: workspaceLoading, error: workspaceError }`.

3. Ensure safe fetch execution
   - Guard data loads: do not call APIs until `workspaceId` is available.
   - Add dependencies so effects re-run when `workspaceId` changes.

4. Add friendly UI states
   - While `workspaceLoading`: show "Loading workspace…"
   - If `workspaceError` or missing `workspaceId`: show a clear error card/message

5. Validate
   - Run `npm run typecheck`.
   - Run the smallest tests that exercise the changed pages or helper logic.

