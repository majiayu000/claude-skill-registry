---
name: new-skill
description: Scaffold a new skill that follows this repo's conventions — interviews for purpose, trigger phrases, and tool needs, then writes `.claude/skills/<name>/SKILL.md` from the skill template with frontmatter and body that pass the integrity gates on first try. Use when user says "write a skill", "scaffold a skill", "create a new skill", "I keep doing X, make it a skill", "new slash command", or "turn this workflow into a skill". NOT for capturing a one-off session discovery — that is `/learn`.
argument-hint: "[skill-name (kebab-case)] [--from-learn] [--dry-run]"
allowed-tools: ["Read", "Write", "Glob", "Grep", "Bash"]
disable-model-invocation: true
effort: medium
---

# /new-skill — Author a Convention-Compliant Skill

Scaffold a new skill the way this template's gold-standard skills are written: a **deep module behind a simple interface** (Ousterhout, *A Philosophy of Software Design* — "deep modules": a small surface that hides substantial implementation). The user supplies a fuzzy intent; this skill interviews it into a tight spec, then writes `.claude/skills/<name>/SKILL.md` with frontmatter and body that are mutually consistent — so `check-skill-integrity.py` and `check-surface-sync.sh` pass without a second pass.

Adapted from the *write-a-skill* pattern in [mattpocock/skills](https://github.com/mattpocock/skills), reshaped to this repo's frontmatter, section, and gate conventions.

## When to use

- You keep re-explaining the same 3+ step workflow to Claude and want it captured as a reusable slash command.
- You need a domain-specific check or output format (citation style, replication gate, a new review lens).
- You want a new skill that is consistent with the 40+ siblings in `.claude/skills/` — same sections, same cross-reference style, same gate-passing frontmatter.

**Use `/learn` instead** when you just discovered something non-obvious *this session* and want it preserved — `/learn` captures a discovery; `/new-skill` deliberately designs an interface. With `--from-learn`, this skill upgrades a `/learn`-shaped stub into a full convention-compliant skill.

## Phases

### Phase 0 — Resolve the name and check for collisions

1. Take the kebab-case name from `$0` (or ask). Reject non-kebab-case, names that collide with an existing `.claude/skills/<name>/`, or names that shadow a built-in (`commit`, `learn`, …) — `ls .claude/skills/` and stop if taken.
2. Read [`templates/skill-template.md`](../../../templates/skill-template.md) for the canonical structure and the frontmatter-field reference.
3. Skim 2-3 sibling skills near the intended domain (e.g. `Glob .claude/skills/*/SKILL.md`, then `Read` the closest matches) so the new skill borrows real conventions, not invented ones.

### Phase 1 — Interview (collect everything *before* writing)

A skill cannot stop to ask mid-write, so gather all interactivity up front (the [orchestrator-protocol.md](../../rules/orchestrator-protocol.md) RUN_CONFIG discipline). Ask, in one batch:

1. **Purpose** — one sentence: what does it accomplish and why does it exist?
2. **Trigger phrases** — the 4-7 quoted phrases a user would actually say. These become the `description`'s "Use when…" clause and are what makes the skill auto-discoverable.
3. **Inputs / arguments** — positional args and any **flags** (each must become a documented `--token`).
4. **Tools** — does the body Read? Write? Grep/Glob? run `Bash`? fan out to a subagent (the `Task` tool)? hit the web via `WebSearch`/`WebFetch`? Only declare what it actually uses.
5. **Output** — a written file (where?), a chat report, or an in-place edit? Should it be read-only?
6. **Scope boundary** — the one or two things it explicitly does NOT do (and which sibling owns those).

Echo a one-paragraph **design brief** back for confirmation before writing.

### Phase 2 — Write the SKILL.md (deep module, simple interface)

Write `.claude/skills/<name>/SKILL.md` from the template, with these gold-standard sections:

- Frontmatter: `name`, `description` (third person, with the quoted trigger phrases), `argument-hint`, `allowed-tools`, `effort`. Add `disable-model-invocation: true` if it writes a persistent, load-bearing file (template's "when to disable" rule).
- Body sections: **When to use**, numbered **Phases** (or Steps), an **Output / report format**, **Exit behavior**, **Cross-references** (to real sibling files), **What this skill does NOT do**, and a **## Flags** section if any flags are advertised.
- Keep the *interface* small (a few args) and the *implementation* deep (the phases carry the weight) — resist exposing a knob for every internal choice.

### Phase 3 — Enforce parity so the gates pass first try

`check-skill-integrity.py` enforces two parities this phase must satisfy (`.claude/scripts/` hosts the gate runners; `scripts/check-skill-integrity.py` is the checker):

- **Flag parity (both directions).** Every flag in `argument-hint` MUST appear in the body as a bare-backticked token, and every flag documented in the body MUST appear in `argument-hint`. So `--from-learn` and `--dry-run` are listed in the hint *and* described under `## Flags`. A stale hint flag fails the gate as surely as a missing one.
- **allowed-tools parity.** The body may only invoke tools listed in `allowed-tools`. If a phase fans out to a subagent (the `Task` tool), that tool must be in the list; if it never does, do not list it. This skill lists exactly `Read, Write, Glob, Grep, Bash` — the tools its phases use, and no subagent fan-out.
- **Anchor resolution.** Internal `[text](path#anchor)` links must resolve — only link to headings that exist.

Run `python3 scripts/check-skill-integrity.py --verbose` and fix any P0/P1 before declaring done.

### Phase 4 — Remind: register the surface (table-row gate)

The skill is NOT discoverable to a reader until it is listed. `check-surface-sync.sh` runs a **table-row gate**: the `<!-- surface-sync-table: skills -->` tables in `README.md` and `CLAUDE.md` must have exactly one data row per skill on disk. Adding a skill without a row fails the gate.

REMIND the user to:

1. Add a row to the **CLAUDE.md** "Skills Quick Reference" table: `` | `/<name> [args]` | <what it does> | ``.
2. Add a row to the **README.md** skills table: `` | `/<name>` | <what it does> | ``.
3. Run `./scripts/check-surface-sync.sh` and `python3 scripts/check-skill-integrity.py` — both must exit 0.

Print the two ready-to-paste rows so the user can drop them in.

## Output / report format

- A new file at `.claude/skills/<name>/SKILL.md`.
- A chat summary: the resolved name, the design brief, the gate results (integrity + a reminder that surface-sync still needs the two table rows), and the two paste-ready table rows.
- With `--dry-run`: emit the proposed SKILL.md to chat only and write nothing.

## Exit behavior

- **Skill written, gates green:** exit 0 with the path, the two table rows, and the explicit "now add those rows + run the two checks" reminder.
- **Name collision or non-kebab-case:** stop in Phase 0 with the conflict named; write nothing.
- **`check-skill-integrity.py` reports P0/P1:** fix in-place and re-run before returning; never hand back a skill that fails its own gate.
- **`--dry-run`:** print the draft, write nothing, exit 0.

## Flags

- `--from-learn` — Seed the interview from an existing `/learn`-style stub (or the current session's discovery) and upgrade it into a full convention-compliant skill rather than starting blank.
- `--dry-run` — Produce the SKILL.md content in chat for review without writing it to disk or touching any surface table.

## Cross-references

- [`templates/skill-template.md`](../../../templates/skill-template.md) — the canonical structure, frontmatter-field reference, and the "when to set `disable-model-invocation`" rule this skill follows.
- [`.claude/skills/learn/SKILL.md`](../learn/SKILL.md) — capture a session discovery (the lighter sibling); `--from-learn` upgrades its output.
- [`.claude/skills/coauthor-brief/SKILL.md`](../coauthor-brief/SKILL.md) — a gold-standard skill to imitate (interview → write → flags → exit-behavior shape).
- [`.claude/rules/orchestrator-protocol.md`](../../rules/orchestrator-protocol.md) — why the interview collects all interactivity *before* writing.
- `.claude/scripts/` and `scripts/check-skill-integrity.py` / `scripts/check-surface-sync.sh` — the gates this skill is built to pass on the first try.

## What this skill does NOT do

- **Capture a session discovery** — that is [`/learn`](../learn/SKILL.md). This skill designs an interface; `/learn` records a finding.
- **Edit the README / CLAUDE.md surface tables for you.** It *prints* the two rows and reminds you; registering them (and re-running `./scripts/check-surface-sync.sh`) is a deliberate human step so the surface gate is never silently satisfied.
- **Write agents, rules, or hooks.** It scaffolds a skill only; an agent goes in `.claude/agents/`, a rule in `.claude/rules/`.
- **Commit anything.** Branch / PR / merge is [`/commit`](../commit/SKILL.md)'s job.
