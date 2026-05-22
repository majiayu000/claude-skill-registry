---
name: docker-next-config-mounts
description: Use when asked to fix Docker Compose bind mounts for Next.js config so they mount next.config.mjs (not next.config.js) and avoid the next.config.js/ directory bug.
---

Goal: ensure Docker Compose mounts the correct Next.js config file and avoid Docker creating a `next.config.js/` directory when a bind source path is missing.

Workflow:

1. Confirm the repo uses `next.config.mjs`
   - Check that `next.config.mjs` exists at the expected path.

2. Fix compose files
   - Replace mounts of `next.config.js` with `next.config.mjs`.
   - Prefer read-only mounts: `:ro`.

3. Prevent recurrence
   - Ensure the mounted source file exists in the repo.
   - Optionally add `next.config.js/` to `.gitignore` to prevent accidental commits if it was created previously.

4. Validate
   - Rebuild or restart dev containers as needed.

