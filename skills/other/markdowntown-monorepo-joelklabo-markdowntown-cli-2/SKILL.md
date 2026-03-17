---
name: markdowntown-monorepo
description: Monorepo workflow for coordinating CLI + web changes, tests, and docs in markdowntown.
---

# markdowntown-monorepo

- Follow root `AGENTS.md` for repo-wide workflow and test expectations.
- For CLI changes: `cd cli && make lint` and `cd cli && make test`.
- For web changes: `pnpm -C apps/web lint`, `pnpm -C apps/web compile`, `pnpm -C apps/web test:unit`.
- For docs-only changes: `pnpm -C apps/web lint:md` and `cd cli && make lint` if CLI docs change.
- Keep CLI scan/audit specs canonical under `cli/docs/` and link from web docs.
- Use prompt templates in `codex/prompts/` for common scan/test flows.
