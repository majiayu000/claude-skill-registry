---
name: markdowntown-cli
description: Repo workflow for markdowntown CLI development and scans.
---

# markdowntown-cli

- Build the scan CLI per `cli/docs/scan-spec-v1.md`.
- Prefer `rg` for search and keep changes small and deterministic.
- Run `cd cli && make lint` and `cd cli && make test`; CI must be green before finishing.
- Avoid destructive git commands unless explicitly asked.
- For web app changes, follow `apps/web/AGENTS.md`.
