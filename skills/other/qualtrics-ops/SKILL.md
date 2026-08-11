---
name: qualtrics-ops
description: "Operate a live Qualtrics survey via the v3 APIs without breaking fielding. Publish gating, quotas, flow routing, embedded data, panel-vendor redirects, and read-back verification."
---

# Qualtrics Live-Survey Operations

## Instructions

### 1. When to use

This skill covers **operating** a survey already built and imported into
Qualtrics — publishing, quotas, flow routing, live text patches, panel-vendor
integration, security options — on an instrument that is or will be fielding
real respondents. It is not survey design or QSF construction; assume the
survey definition already exists and the question is how to change it without
breaking what respondents currently see.

### 2. Non-negotiables

**Backups first, always.** Pull and save the survey definition (and flow and
options as separate JSON) before any write. Qualtrics version restore exists
but is coarse and carries data-risk caveats; your pre-change snapshot is the
only *precise* recovery path, and the only one that covers objects (quota
counters, options) outside version history.

**Verify by read-back, never by absence of error.** A 200 response proves the
API accepted the request, not that respondents will see the result. After
every write, GET the changed object back and confirm it matches intent.

**The version list is the proof a change is live**, not the publish-state
flag. Question/block writes create no version-history entry, so publish-state
can report "in sync" while the live version still lags behind your edit. The
standard: your publish call created a NEW published version entry carrying
your own description — and, because a description proves provenance rather
than content, pair it with a read-back of the published content where the API
exposes it.

**One writer at a time.** Confirm you are on the right survey, brand, and
environment, that no one has the builder open concurrently, and that you know
the rollback path before the first write. On an actively fielding instrument,
prefer a change window; and remember the platform's own warning that deleting
or restructuring questions and choices can invalidate already-collected data.

**Assert everything untouched is unchanged**, not just that your target
changed — compare parsed structures, since the server may normalize ordering
and defaults. Several of the traps below are full-replace endpoints that
silently wipe sibling data; catching that requires diffing the whole object
against the pre-change backup, not just checking the field you meant to edit.

### 3. Publish gating — two distinct failure modes

Most flow and options edits to an active survey are **staged**, not live,
until an explicit version publish — respondents keep getting the old version
while the API happily reads back your new one. (A few option keys apply
immediately, availability among them; treat "staged until published" as the
safe default assumption and verify per key.) Question/block writes are worse: they
create no `list_versions` entry at all, so publish-state can say "in sync"
immediately after a write that hasn't actually gone anywhere near respondents.
Stage all related writes for a change as one batch, verify the batch by
read-back, then publish ONCE, deliberately (forcing the publish if your client
supports it) — publishing after every individual write can expose respondents
to internally inconsistent intermediate versions. Reload the builder UI before
trusting its Draft/Published badge — it lags the API.

Publishing an **inactive** survey activates it. Treat activation as a
separate, deliberate decision from publishing a change — have your API client
require an explicit activation flag so a routine content publish can never
launch fielding as a side effect.

### 4. Quota API

- Quota creation auto-assigns to the survey's existing quota group; there is
  no field to target a specific group on write. Regrouping is a UI-only
  operation (the "Move to…" row menu) — plan for it, don't fight the API.
- The quota-group update endpoint is a **full replace**: omit the quotas array
  and the group's membership is silently wiped. Always resend the complete
  membership plus any fields the API requires on write but omits from its own
  list payload (e.g. a match-mode flag) — write-shape and read-shape are not
  the same contract.
- Choice-based quota conditions need both the operand the evaluation engine
  reads AND the locator the editor UI renders its dropdown from. Write only
  the operand and the condition still *works* but displays as an empty
  "Select Choice…" in the UI — and a later UI-side save of that blank state
  can overwrite live quota logic with nothing.
- Confirm the exact operator enum the API expects (vendors sometimes reject a
  plausible-looking synonym) rather than assuming from REST convention.
- Via the API write path, the quota end-survey action accepted no per-quota
  redirect in our testing (the builder UI may offer a custom end-of-survey per
  quota — verify on your account). The pattern that works everywhere: bracket
  the quota-bearing block with before/after embedded-data nodes carrying the
  quota-full vs screen-out exit URLs, and let the end-of-survey redirect read
  the field.
- Quota counts can retain stale values after response deletion even when the
  deletion call requests a decrement. Before a FIRST fielding wave, zero the
  counters explicitly rather than trusting the decrement flag; mid-study,
  reconcile in-progress sessions and prior-wave records first — resetting a
  live counter is destructive and needs explicit authorization.
- Quota-list endpoints paginate at a small page size — always follow the
  next-page cursor, or an audit silently covers only the first page of quotas.

### 5. Flow mutation and routing placement

- **Anchor routing gates on block descriptions, not on a data-capture node.**
  A capture node's position can vary across instruments (some run it
  pre-consent, some post-), so a gate anchored to "wherever that node sits"
  can end up before consent on some builds — ethics-relevant if the gate is a
  termination. Anchor each gate type to a stable semantic point instead:
  consent-dependent gates immediately after the consent block; paradata-based
  gates after the point where every field they read is guaranteed to exist;
  questionnaire-anchored checks right after their own block, never held to
  end-of-survey (a late termination costs the respondent the whole length of
  interview for nothing).
- Know which multilingual architecture you have. Qualtrics' native
  translation layer keeps ONE block structure with per-language text; a
  branch-per-language build duplicates every block per arm. On the latter,
  duplicate each gate into every arm with a fresh flow-element ID — one gate
  does not cover all arms.
- **Capture-before-gate order is load-bearing.** The node that writes a field
  must precede every gate that reads it. Get the order wrong and the gate
  fails *safe* — no error, no fire, just silently dead — which is far more
  dangerous than a routing bug that throws.
- When the exit URL is carried in an embedded-data field consumed by the
  end-of-survey redirect, the node that SETS the field must precede the
  terminating element inside the gate — the termination ends flow evaluation,
  so anything ordered after it never executes.
- On paired-language (twin) instruments, never express a failure condition as
  "the correct option was not selected" — an unanswered field in the
  respondent's *other* language arm also satisfies "not selected" and routes
  out the wrong arm entirely. Express failure as positive selection of a wrong
  option instead.
- Guard any geolocation-based termination with an explicit "value present and
  not equal to the excluded value," not just "not equal to." An unresolved
  lookup (proxy, privacy relay, corporate VPN) must not silently satisfy a
  bare not-equal check and terminate a legitimate respondent.
- Reserve *live* termination for signals that cannot belong to a real,
  eligible respondent: ineligibility, duplicate device/session, a hard machine
  signature. Anything that is scored or graded on a continuum — a bot-risk
  score, a fraud score, an attention-check failure, response-speed outliers —
  belongs in analysis-side exclusion criteria, not a live termination branch,
  because a live gate can't be revisited once it has turned away a respondent.

### 6. Live text edits vs. source specs

When a survey is built from versioned source specs (YAML, a survey-builder
config, etc.), a live typo or wording fix still often needs to go directly
against the live question via a targeted patch — matching exact surrounding
text and replacing only the intended span — rather than a full spec rebuild
and repush, because a rebuild will clobber any manual formatting or ordering
that was applied directly in the live tool since the last build. When syncing
the fix back into the source spec afterward, match whitespace-insensitively:
prose in structured source formats commonly soft-wraps, so a byte-for-byte
diff against live text produces false mismatches.

Keep an explicit list of anything the build pipeline does **not** emit (e.g.
quality-routing branches, vendor-specific disclosures added live) — a rebuild
silently drops these, so they must be reapplied by hand after every rebuild
and repush.

### 7. Panel-vendor integration basics

Redirect logic for panel-vendor traffic follows a stable pattern regardless of
vendor: a pre-consent screen-out value, a terminal complete value, and an
end-of-survey redirect to whichever URL parameter carries the vendor's
completion redirect — typically piped from an embedded-data field the vendor's
entry link populated. Bracket any quota-bearing block with a quota-full
redirect variant so respondents who close out a quota mid-survey get routed to
the vendor's quota-full endpoint rather than falling through to a generic
completion or termination redirect.

**URL query parameters resolve into piped references at session start
regardless of where (or whether) the embedded-data declaration sits in the
flow** — live-verified against redirect pipes. Declare the field anyway:
declaration is what makes the value reliably typed, saved, and exported, and
downstream logic easier to read.

(Panel vendors vary — a generic panel-vendor redirect endpoint is the concept
that matters here, not any particular vendor's API shape.)

### 8. Security options

Treat the survey's security/options block as read-modify-write: fetch the
full current object, change only the target keys, and write the whole object
back — then assert every key you did not intend to touch is byte-identical to
the pre-change value. Options endpoints are as prone to full-replace semantics
as the quota-group endpoint above, and a security setting silently reset to a
default (e.g. a fraud-detection threshold, a ballot-box-stuffing prevention
flag) is the kind of regression that goes unnoticed until an incident, not at
write time.

## Quality Checks

- [ ] Pre-change backup saved (survey definition + flow + options as separate
      JSON) before any write
- [ ] Publish issued after every quota/question/flow write, with activation
      (`allow_activation`/equivalent) triggered only at deliberate launch, never
      as a side effect
- [ ] Change verified live via `list_versions` showing a version with your own
      description — not via publish-state or the builder UI badge alone
- [ ] Full object read back post-write; every untouched key confirmed
      byte-identical to the backup
- [ ] Quota-group and options writes sent as complete objects (full
      membership / full key set), never partial
- [ ] Choice-based conditions carry both the evaluation operand and the
      UI locator
- [ ] Routing gates anchored to stable block descriptions, not data-capture
      node position; capture nodes confirmed to precede every gate that reads
      them
- [ ] Live terminations limited to non-scored eligibility/fraud signals;
      anything scored or graded routed to analysis-side exclusion instead
- [ ] Twin-language gates expressed as positive wrong-selection, never as
      "not selected"
- [ ] Anything the build pipeline doesn't emit re-applied after any rebuild +
      repush
