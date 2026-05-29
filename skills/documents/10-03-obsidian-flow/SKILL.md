---
name: 10-03-obsidian-flow
description: How documentation stays aligned with code using AGENTS.md, open questions, tk tickets, and Johnny Decimal structure.
---

# 10.03 Obsidian Documentation Flow

How documentation stays aligned with code.

- `AGENTS.md` in code/source folders for folder-level rules
- `docs/playbook/` for process/tooling
- `docs/reference/` for architecture and research
- `docs/features/` for documenting work/spec

## Core Rules

1. **AGENTS in code folders.** Every top-level code/source folder needs an `AGENTS.md` describing purpose, boundaries, entry points, and tests.
2. **Open questions live in docs.** Use `🙋‍♂️/🤖/✅` comments with block IDs. See [[playbook/10-docs/10-01-open-questions-system/SKILL]].
3. **Use `tk` + `tinychange`.** Create a `tk` ticket for non-trivial work and update the changelog via `tinychange`. Use the standard ticket template. Don't manually update the changelog.
4. **Johnny Decimal (two-digit).** Use `NN.NN` for playbook/reference IDs.

## One-Shot Usage (LLM)

1. Read `docs/AGENTS.md` and the closest folder `AGENTS.md`.
2. Update playbook/reference docs, not sidecars.
3. Use open-questions format with block IDs.
4. Record a `tk` ticket for non-trivial work.
5. Log changes: `tinychange -I new -k <fix|test|chore|security|feat|docs|refactor|perf> -m "message" -a AUTHOR`

## When Updating Code

1. Read the nearest `AGENTS.md` in the code folder.
2. Update or add `AGENTS.md` if the folder's purpose/boundaries changed. (ONLY ALLOWED AFTER `[OK]` from the Hooman.)
3. If behavior changes, update the relevant docs in `docs/reference/`.
4. Log the change via `tinychange`.

## Where to Document

- **Process/tooling** → `docs/playbook/`
- **Research** → `docs/reference/`
- **Feature specs/plans** → `docs/features/`
- **Architecture** → `**/AGENTS.md`
