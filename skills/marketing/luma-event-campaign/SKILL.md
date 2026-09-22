---
name: luma-event-campaign
description: >-
  DRAFT. Use when running a Luma-centered GTM event campaign: pull/export guests,
  enrich and score, draft invites and social, stage email+LI sequences paused for
  approval, and wire registration sync. Not installed by deepline skills.
---

# Luma event campaign (DRAFT)

## When to use

You have (or are creating) a Luma event and need a **repeatable campaign system**:
guest acquisition → enrichment → messaging → staged outreach → registration hygiene.
Not for one-off "write me an invite tweet."

## Non-negotiables

- Keep outbound campaigns **paused** until a human approves sends.
- Pilot enrich on ≤10 rows before full waterfall.
- No invented speaker bios, titles, or company facts.
- Templates use placeholders (`{{event_name}}`, `{{city}}`, `{{speaker_1}}`).
- Prefer systems language: skills, plays, webhooks, score → approve → door — not "blast the list."

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| Luma event URL or export CSV | yes | At least name, email, status |
| ICP / TAL sheet (domains) | no | Boosts scoring |
| Brand voice notes | no | Else use `templates/voice.md` |
| Sequencer (Lemlist/Instantly/etc.) | no | Stage paused campaign only |

## Standard flow

### 1. Frame the system

Say out loud (or in the run log):

1. Source of truth for guests (Luma)
2. Enrich + score path
3. Messaging artifacts (invite email, LI DM, social)
4. Outreach object (paused)
5. Inbound sync (registration webhook — see `luma-inbound-webhook-enrich`)

### 2. Guest list hygiene

1. Export or API-pull guests.
2. Normalize emails; drop empties; flag duplicates.
3. Map ticket/status: pending / approved / waitlist / checked_in.
4. Write `guests.normalized.csv`.

### 3. Enrich + score (pilot first)

1. Run a **10-row pilot** enrich (email validation + LinkedIn URL + title/company).
2. Score segments: `hot` / `warm` / `low` / `skip` using ICP + TAL + seniority.
3. Full run only after pilot lookback.
4. Write `guests.scored.csv`.

### 4. Messaging pack

Use templates in `templates/`:

- `invite-email.md` — HubSpot or transactional invite
- `linkedin-dm.md` — short DM, no hype words
- `social-announcement.md` — X/LinkedIn announcement
- `speaker-bio.md` — only from verified sources

Fill placeholders; human-edit before publish.

### 5. Stage outreach (paused)

1. Create/update sequencer campaign from `hot`+`warm` only.
2. Import with enrichment fields needed for personalization.
3. Leave campaign **paused**; paste the campaign URL in the run report.
4. Never auto-send from this skill.

### 6. Registration sync

Hand off to `luma-inbound-webhook-enrich` for standing registration → enrich → CRM.

### 7. Day-of handoff

Hand off scored list to `event-ops-score-and-door` and optional `event-host-prep-dossiers`.

## Output checklist

- [ ] `guests.normalized.csv`
- [ ] `guests.scored.csv` (with segment)
- [ ] Messaging pack under `out/copy/`
- [ ] Paused campaign link
- [ ] Credit / provider notes for enrich pilot + full run
- [ ] Explicit "human approve before send" line in the report

## Guardrails

- Do not dunk on other tools; frame hybrid stacks honestly.
- Strip unsafe emails after validation; do not import fails into sequences.
- Anonymize any shared examples before committing to git.
