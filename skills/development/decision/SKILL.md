---
name: decision
description: Capture a project decision as an ADR-style record in decisions/NNNN-slug.md — context, options considered, the call, consequences, status. Use when the user makes or reports a design, code, zoning, or procurement choice ("we're going with...", "the client decided..."), when an analysis surfaces options that force a choice, or to supersede an earlier decision. Records reasoning — current facts live in PROJECT.md via /project-dossier.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - AskUserQuestion
---

# /decision — Project Decision Records

You capture decisions the way software teams capture ADRs (Architecture Decision Records) — except these are for actual architecture. One file per decision, numbered, in `decisions/` at the project root. The record survives the email thread, the meeting, and the personnel change that would otherwise lose it.

## Usage

```
/decision                          → interview for a decision in the air, then record it
/decision we're going with X       → record it, asking only for what's missing
/decision supersede 0003           → mark 0003 superseded, record its replacement
/decision list                     → show the index with statuses
```

## Hard rules

1. **One decision per record.** "Schemes B and code edition 2022" is two records.
2. **Never renumber, never delete.** Numbers are permanent references. Wrong decisions get `superseded`, not removed — the reasoning trail is the point.
3. **Capture options honestly.** A record with one option isn't a decision, it's an announcement. Ask what else was considered, even briefly.
4. **Keep the dossier index in sync.** Every create/supersede updates the Decisions table in `PROJECT.md` (create the dossier via `/project-dossier init` first if it doesn't exist).
5. **Brevity.** Context in 2–4 sentences, options as one line each, consequences as bullets. A record nobody reads records nothing.

## Recording flow

1. Find the next number: `Glob decisions/*.md`, take max + 1, zero-padded to 4 digits.
2. Gather the pieces — from the conversation first, ask only for gaps (one grouped question): what was decided, what options were on the table, why, who made the call.
3. Write `decisions/NNNN-{kebab-slug}.md` from the template.
4. Update the Decisions index in `PROJECT.md`.
5. Confirm with the path and a one-line restatement of the decision.

## Template

```markdown
# NNNN — {Decision title, stated as the choice made}

- **Status:** decided
- **Date:** {YYYY-MM-DD}
- **Deciders:** {who made the call}

## Context

{2–4 sentences: the situation that forced a choice. Link the analysis that surfaced it if one exists.}

## Options considered

1. **{Option A}** — {one line: what it would mean}
2. **{Option B}** — {one line}

## Decision

{The choice, and the load-bearing reason in 1–3 sentences.}

## Consequences

- {What this enables, costs, or constrains downstream}
- {What must now happen as a result}
```

Statuses: `proposed` (on the table, not yet made — record it so the options aren't lost), `decided`, `superseded by NNNN`.

## On `supersede`

1. Read the old record. Set its status to `superseded by NNNN` (naming the new record) — touch nothing else in it.
2. Record the new decision normally; its Context section names what it replaces and why the reversal.
3. Update both rows in the dossier index.

## When analysis skills propose a decision

Skills in this marketplace surface choice points (zoning paths, code editions, GWP thresholds) and suggest running `/decision`. When that happens, the analysis is your Context — quote its numbers with their source rather than re-deriving them.

## Collaboration

Records are plain files in the project folder — share them the way the project is already shared (git, Drive, Dropbox). Review happens in version control or in conversation; this skill imposes no workflow beyond the files.
