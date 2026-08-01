---
name: ca-adr
description: Author a numbered, dated, user-attributed Architecture Decision Record under .codearbiter/decisions/.
argument-hint: "<decision title>"
---

# /ca-adr — author an ADR

Record an architectural decision as a numbered, dated ADR. Title the decision clearly — name what was
decided, not what was considered (`"Use PostgreSQL as the primary database"`, not
`"Database selection"`). This is the only sanctioned path to author an ADR.

## Routes to

The `decision-lifecycle` skill (`<plugin-root>/routines/decision-lifecycle/SKILL.md`). The skill
owns numbering, the file template, the `proposed → accepted → superseded | rejected` status lifecycle,
and writes the file to `<project-root>/.codearbiter/decisions/`. Status transitions require
explicit user instruction; the orchestrator never advances an ADR on its own.

## When NOT to use

- Check the health of existing ADRs → `/ca-adr-status`.
- Reconcile or challenge a suspect ADR → `/ca-reconcile`.
- Ask about a decision without recording it → `/ca-btw`.

## Hard gate

An ADR is authored ONLY via `/ca-adr` with explicit user attribution. MUST NOT author an ADR as the
disposition of a routine finding — decision-worthy findings surface to the user or to
`open-questions.md` as a `[CONFIRM-NN]`. MUST NOT resolve a `[CONFIRM-NN]` in the ADR by guessing.
