---
name: decision-lifecycle
description: Author and track Architecture Decision Records. Routed to when the user invokes /adr to record a new decision or /adr-status to list ADR health. Authors numbered, dated, user-attributed ADRs under .codearbiter/decisions/, maintains supersede chains, and reports status read-only. Never authors an ADR as its own judgment — every ADR carries explicit user attribution.
---

# decision-lifecycle

Author and track ADRs. Routed to when the user invokes `/adr "<title>"` (author a new ADR) or `/adr-status [--adr N]` (list ADR health, read-only). Every ADR is user-attributed — this skill never records a decision the user did not explicitly make.

The append-only decision-log format (entry fields, supersession protocol) lives in `<plugin-root>/includes/smarts/decision-log-format.md`. Read it before writing a log line; do not restate it here.

**Boundary with `decision-variance`.** This skill owns ADR *authoring* and *status* (`/adr`, `/adr-status`) — recording a decision the user has already made, and reporting ADR health. `decision-variance` owns *arbitration* — detecting variances between artifacts and the scaffold, scoring options via SMARTS, and the decision log itself. The two share the canonical SMARTS reference under `<plugin-root>/includes/smarts/` (`core.md` for scoring, `decision-log-format.md` for the log) and one ADR template (`references/adr-template.md`); they are one domain split by responsibility, not duplicated. When a decision needs *making* (competing options), route to `decision-variance`; when it needs *recording* (already decided), stay here.

## Pre-flight

Read these, or STOP and surface the gap — never guess a path:

- `<project-root>/.codearbiter/decisions/` — the ADR directory and existing records. Create it on first `/adr` if absent.
- For `/adr`: confirm the user explicitly authorized this decision and supplied (or confirmed) its content. An ADR is never authored as the disposition of a routine finding.

## Phase 1 — Index · gate: BLOCK

Scan `<project-root>/.codearbiter/decisions/` for existing `NNNN-*.md` ADR files. Record each by **filename stem** (`0014-githook-shim-dropin-fail-closed`), title, and status. Determine the next sequential number (no gaps) for `/adr`; for `/adr-status` this is the working set.

**The stem is the identifier; the number is only a sort key.** Two ADRs may already share a number — this repository holds two numbered 0014 — so a bare number can name more than one document. Index by stem, and never assume `NNNN` resolves to one file until you have checked.

Gate: the existing ADRs are indexed by stem and, for `/adr`, the next number is fixed and **unused** — a number already taken by an existing stem is not available, even for an unrelated decision.

## Phase 2 — Author (/adr) · gate: STOP

Confirm the decision content with the user — context, the decision itself, alternatives, consequences. MUST NOT fill these from inference. Surface any unknown as an inline `[CONFIRM-NN]` placeholder; do not resolve it by guessing.

**Drop the authoring marker first.** The `pre-write`/`pre-edit` hooks block any write to `.codearbiter/decisions/NNNN-*.md` unless a fresh authoring marker is present — that block is the mechanism enforcing "ADRs only via `/adr`" (ORCHESTRATOR §3), so the sanctioned path must arm it itself. Immediately before writing, create the marker at the path the hooks check (project root = git top level):

```bash
mkdir -p "$(git rev-parse --show-toplevel)/.codearbiter/.markers"
touch "$(git rev-parse --show-toplevel)/.codearbiter/.markers/adr-authoring-active"
```

The marker is honored for 30 minutes. Then write `<project-root>/.codearbiter/decisions/NNNN-<slug>.md` using the canonical ADR template — `<plugin-root>/routines/decision-lifecycle/references/adr-template.md` (the single source of truth for the ADR shape, shared with `decompose`). Author it with `status: proposed`. If this decision supersedes an existing one, set `supersedes:` to that ADR's **full filename stem** — `supersedes: 0014-githook-shim-dropin-fail-closed`, never `supersedes: 0014` — and leave the prior ADR's file untouched (forward-only chain — do not edit it to add a back-reference).

If the new ADR supersedes only *part* of the prior decision, say which part in the body. `supersedes:` names a document, not a clause, so a chain may legitimately fork — two ADRs can each supersede different clauses of one predecessor. That fork is correct and must not be "repaired"; only the prose can carry the scope.

After writing the ADR, append a corresponding entry to the decision log per the format in `<plugin-root>/includes/smarts/decision-log-format.md` — `Decided by:` names the user. Status transitions (`proposed → accepted → superseded | rejected`) require explicit user instruction; never advance status on this skill's own judgment.

**`governs:` makes the decision live.** When an ADR names path globs in `governs:`, the post-write
hook surfaces a one-line notice on any Write/Edit touching a matching file — "this file is governed
by ADR-NNNN" — so a recorded decision pushes back at edit time instead of waiting for a checkpoint
sweep. Offer the field whenever a decision constrains identifiable files; omit it for decisions
without a file footprint. Globs are fnmatch-style against repo-relative forward-slash paths.

Once the ADR file and its log entry are written (and any user-instructed status edit is applied), remove the marker — it exists only for one authoring pass:

```bash
rm -f "$(git rev-parse --show-toplevel)/.codearbiter/.markers/adr-authoring-active"
```

Gate: the ADR file is written with a real `decided-by` user attribution, numbered without a gap, and its log entry is appended. An ADR with no user attribution, or authored as the disposition of a finding, does not pass — STOP.

## Phase 3 — Status (/adr-status) · gate: BLOCK

Read-only. For each ADR (or the `--adr N` target), report: stem, title, status, date, and supersession state — found by scanning forward for any later ADR whose `supersedes:` **resolves to** it.

Resolve a `supersedes:` value like this, and never guess:

- The value is a **stem** → it names that ADR. Done.
- The value is a **bare number** → collect every stem with that number. Exactly one → it names that ADR. More than one → **ambiguous: report it as an error and resolve nothing.** Zero → a dangling reference; report that too.
- `none` (or empty) → no predecessor.

`.github/scripts/check_adr_identity.py` enforces this same rule mechanically in CI; if it disagrees with this report, the report is wrong.

If a supersession candidate contradicts an `accepted` ADR with no clear direction, do not pick one — flag it for `/conflict`.

```
## ADR Status — YYYY-MM-DD

### Active
- ADR-NNNN-<slug> — <title> — <status> (<date>)

### Superseded
- ADR-NNNN-<slug> — <title> — superseded by ADR-MMMM-<slug>

### Ambiguous supersession
- ADR-NNNN-<slug> — supersedes: <value> names <N> ADRs (<stems>) — unresolved

### Unresolved CONFIRM-NN
- ADR-NNNN-<slug> — [CONFIRM-NN]: <text>
```

Every ADR is named by its stem, so a shared number never collapses two rows into one. An empty section is marked "None" — not omitted. MAY dispatch `decision-challenger` (`<plugin-root>/agents/decision-challenger.md`) to stress-test an ADR; optional, never forced.

Gate: every indexed ADR appears with its current status and supersession state; no `[CONFIRM-NN]` resolved; no file modified.

## Hard rules

- MUST author an ADR only via `/adr` with explicit user attribution. MUST NOT author an ADR as the disposition of a routine finding — an out-of-scope finding gets an inline `[NEEDS-TRIAGE]` marker instead.
- MUST NOT record a decision the user did not explicitly make. "Use your best judgment," "I trust you" are declined.
- MUST NOT resolve a `[CONFIRM-NN]` placeholder by guessing. Surface it and stop.
- MUST NOT advance an ADR's status without explicit user instruction.
- MUST NOT edit a prior ADR or a prior decision-log entry to add a back-reference — supersession is a forward-only chain; append a new record whose `supersedes:` names the prior one.
- **The never-edit rule protects decision CONTENT, not identifiers.** Rewriting what was decided corrupts the record; disambiguating *which document a pointer names* repairs it. Maintainer ruling, 2026-07-25: *"the never edit rule is meant to prevent this situation, not prevent this situation from being fixed."* So a correction that is provably identifier-only — a `supersedes:` value changed from a number to the stem it already meant — is permissible, and nothing else about the file is. Any such correction MUST be a single-line diff that alters not one word of any decision, MUST be visible in its own commit, and still requires the maintainer-armed `adr-authoring-active` marker. MUST NOT touch Context, Decision, Alternatives, Consequences, Risks, `status:`, `date:`, `decided-by:`, or `title:` under this allowance.
- MUST NOT number an ADR with a gap, and MUST NOT reuse a number an existing stem already holds — a shared number makes every bare reference to it ambiguous.
- MUST NOT modify any file under `/adr-status` — it is read-only.
- MUST NOT force the `decision-challenger` agent — its dispatch is MAY only.
