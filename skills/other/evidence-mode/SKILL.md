---
name: evidence-mode
user-invocable: false
description: |
  Evidence mode operational spec for the team lead. An extension of code mode that maintains a durable, observable evidence record alongside the live team conversation, with members spawned as the read-only evidence-member agent. Returns additive evidence-record rules, lead allowlist additions, and a suggest-members supplement.
keywords: evidence mode, durable record, code mode extension, evidence document
extends: swarm:code-mode
generated-by: swarm@0.4.4
---

Return the following extension spec verbatim to the team lead, then invoke the base mode (`swarm:code-mode`) and apply these overlays additively. Do not summarize or interpret.

---

# Evidence Mode (extension of Code Mode)

This is an **extension mode** (beta). It inherits Code mode's lead identity, facilitator (Principal Engineer), phase arc, and all base rules unchanged. It adds two things: a durable, human-readable **evidence record** the lead maintains alongside the live conversation, and a light member-side convention — members are spawned as the read-only `evidence-member` agent — so the team can reference settled findings in the record rather than re-stating them in full.

Honest v0 scope: v0 delivers the durable, structured, attributed, observable record, and the member convention targets **modest** noise-reduction (members cite evidence inline and reference the record rather than re-pasting). The convention is **prompt-enforced (by-degree), not mechanically guaranteed** — v0 is where we find out whether it actually drains re-statement (by reading the runs; v0 ships no measurement instrument); mechanical enforcement is a v1 concern. The record earns its keep on runs with enough findings and review depth that re-statement would otherwise accumulate; on a short run with few findings it is lightweight by design — seed it, but don't over-invest in bookkeeping a small run doesn't need. The live argument is untouched — challenge and concession stay in messages where the user witnesses them.

## Extension Contract

Per `swarm:workflow-rules`, this mode is additive-only. It does not redefine the phase arc, lead identity, or facilitator. The Mode-Specific Rules and Lead Allowlist entries below are added to Code mode's; nothing in the base is removed or contradicted. The fixed member briefing templates are **untouched** — the member-side convention lives in the `evidence-member` agent's own standing prompt (a separate surface from the briefing template, like swarm-member's existing standing guidance), and the `/swarm:evidence` command supplies the spawn override that selects that agent. The lead seeds and maintains the record.

## Mode-Specific Rules (additive)

### Evidence Record

- **The lead maintains the record; members reference it.** Members are spawned as the read-only `evidence-member` agent and converse on the wire as in Code mode, with one light habit: cite evidence inline, and reference a finding already in the record by its ID rather than re-pasting it. Only the lead writes the record.
- **Seed at the start, share the path.** Before Research begins, the lead creates `~/.claude/teams/<team-name>/evidence.md` (the Claude team directory that holds the team's `config.json` — already created with the team, and outside the user's repo) with the skeleton below, and shares its path with the team in the Research kickoff message (a runtime message, not a briefing change) so members can read and reference it.
- **Tell the user where the record is, and that it is session-local.** The record is the point of this mode, so the lead names its path to the user — at Approve and again at Deliver — in a plain runtime message (e.g., "the evidence record for this run is at `~/.claude/teams/<team-name>/evidence.md`"). The user should never have to discover it by guessing. At Deliver, the lead also surfaces the record's full contents to the user and notes that it is a **session-local** artifact: it lives in the team directory, outside the repo, and does **not** ship with the commit or PR — so the user can capture a copy if they want it preserved or portable.
- **Record landed findings only; the argument stays on the wire.** As a finding lands on the wire — a member's evidence-backed position, the chosen approach with the rejected alternatives and who raised the killing concern (append the Approach entry only when the facilitator sends CONVERGED — it is not settled before then), a review finding and its disposition — the lead appends it to the record under a stable short ID (`[R1]` for a research finding, `[V1]` for a review finding, and so on). Challenge and concession are **not** written to the record; they happen live in messages where the user can witness them. The record holds what is settled; the wire holds what is being argued.
- **IDs are for wayfinding, never a substitute for prose.** An ID labels a full prose entry (the evidence-backed position plus its evidence) so members can reference it ("re `[R1]`, still open") instead of re-pasting. An ID never replaces the readable finding.
- **Keep the NOW and OPEN bands current.** NOW is the phase·rung glance line. OPEN lists the IDs of findings still live — a research finding still contested, or a review finding whose disposition is `open`. The lead adds an ID to OPEN when a finding is recorded unresolved and removes it when the finding resolves (its review disposition becomes `fixed`/`accepted-tradeoff`, or the contest settles); an unpruned OPEN band rots into noise. Like the rest of the record, OPEN is record-after: a reviewer forms their own "what's missing" before consulting it, never the reverse.
- **Append-only, topic-organized, attributed.** Organize entries by topic/finding with the member's name and evidence references (file:line, tool output, source). Never partition the record by member. Never overwrite a prior entry — supersede by appending a new entry that names what changed.
- **The record is a projection of the wire, never a source for it.** Every entry transcribes something already stated in a message. Reviewers form their own "what is still missing" from their own read of the live conversation **before** consulting the record — the record is a record-after, never an oracle that pre-frames a review. This preserves the independent-reasoning gate.

### Evidence Record skeleton

```
# Evidence Record — <outcome>
## NOW: <phase · rung>        (the glance line — lead keeps current)
## OPEN: <finding ids>
---
## Research findings
  - [R1] <member · finding · evidence refs>
## Approach
  - chosen path; rejected alternatives + who raised the concern that killed each
## Review
  - [V1] <finding · disposition: open / fixed / accepted-tradeoff>
```

## Lead Allowlist (additions)

**Permitted (additions to Code mode):**
- The lead may create and append to the evidence record at `~/.claude/teams/<team-name>/evidence.md`. This is the only file write outside the repo's normal deliverables, and only the lead performs it.

**Forbidden (additions to Code mode):**
- Members must not write the evidence record — read-only is unchanged (members are the read-only `evidence-member` agent).
- The lead must not move challenge or concession off the wire into the record — the live argument must remain observable in messages, never replaced by a document entry.

## Suggest-Members Guidance (supplement)

Same as Code mode. No evidence-specific roles are needed — the record is a lead mechanic and the convention is carried by the member agent, not a team role.
