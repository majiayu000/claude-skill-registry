---
name: agent-protocol
description: Human and agent coordination protocol for repos using .agentprotocol. Use to manage TODO intake, open and archived work items, and plan/build docs with deterministic indexes.
metadata:
  init: bun ./skills/agent-protocol/scripts/init.ts
  create: bun ./skills/agent-protocol/scripts/create.ts
  reindex: bun ./skills/agent-protocol/scripts/reindex.ts
  templates: ./skills/agent-protocol/assets
  references: ./skills/agent-protocol/references
---

# Agent Protocol

Coordinate work in repos that use `.agentprotocol/`. Keep work items self-contained and minimize follow-up questions.

## Always load first
- Read `.agentprotocol/README.md` at the start of any session.
- If `.agentprotocol/` is missing, offer to initialize with `bun ./skills/agent-protocol/scripts/init.ts`.

## Core structure
- `.agentprotocol/README.md`: protocol contract and Active Work Index.
- `.agentprotocol/TODO.md`: intake queue.
- `.agentprotocol/open/<ID>-<slug>/`: active work items.
- `.agentprotocol/archive/<ID>-<slug>/`: completed or cancelled items (moved as a whole).

## Workflow
1. Intake work in `.agentprotocol/TODO.md`.
2. Create a work item with `create.ts` (build-only by default; add `--plan` for plan + build).
3. Write or refine `plan.md` if needed; keep it flexible (PRDs, user stories, specs).
4. Execute from `build.md` with tasks, verification, and append-only log.
5. Archive by moving the whole directory to `.agentprotocol/archive/`.

## Work selection
- If the user names a path or ID, use it.
- If not, suggest up to 3 candidates from the Active Work Index and TODO. The user chooses.
- Never auto-select.

## plan.md
- Optional design surface. May include PRDs, user stories, acceptance criteria, constraints, and invariants.
- Frontmatter: `id`, `title`, `status`, `created_at`, `updated_at`, optional `refs`.
- `status` values: `draft | ready | done | cancelled`.
- `ready` means Open Questions is empty (or risks explicitly accepted).

## build.md
- Execution surface with tasks, verification, and append-only log.
- May exist without a plan (ad-hoc).
- Frontmatter: `id`, `status`, `created_at`, `updated_at`, optional `plan_id`.
- `status` values: `todo | in_progress | blocked | done | cancelled`.
- If `build/` exists, include a Build File Index table listing all `build/*.md` (sorted by path).
- `build/*.md` files are plain markdown by default (no required frontmatter).

## Active Work Index
- `.agentprotocol/README.md` contains a markdown table of all open work item directories.
- Update with `bun ./skills/agent-protocol/scripts/reindex.ts` (deterministic; avoids manual edits).
- Use `--next` to include next-action extraction when desired.

## IDs and timestamps
- `ID` is Crockford base32 encoding of UUIDv7 bytes.
- Uppercase, fixed 26 chars, left-padded with `0`.
- Alphabet: `0123456789ABCDEFGHJKMNPQRSTVWXYZ`.
- No zero padding in body identifiers (use `US-1`, not `US-001`).
- `created_at` / `updated_at` use RFC3339 with timezone (recommend UTC `Z`).

## Archiving
- When a work item is `done | cancelled`, move the entire directory from `open/` to `archive/`.
- Remove the row from the Active Work Index.

## Migration
- For old `context/` repos, follow `references/migration.md`.
