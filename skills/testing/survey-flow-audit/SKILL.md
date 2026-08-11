---
name: survey-flow-audit
description: "Pre-fielding audit of a live survey over the platform API, with an optional browser walk. Consent-before-anything gates, publish state, force-response completeness, quotas, vendor redirects, anti-bot instrumentation, language-arm symmetry."
---

# Survey Flow Audit

Audit a survey the way it will actually run, not the way its build files say it
should. Everything here reads the LIVE definition over the API and, optionally,
walks the respondent path in a real browser. The audit is **read-only on the
survey definition**: it produces findings, never fixes. The optional browser
walk (Phase H) does generate test *responses* — data-plane writes with their
own cleanup obligations, and possibly test hits on a vendor dashboard — so it
is opt-in and announced, never silent. Repairs are a separate, explicitly
authorized step (see the `qualtrics-ops` skill for how to make them without
new damage).

Fielding now happens in an environment where AI agents complete surveys at
scale and pass conventional attention checks (documented since 2025 in
peer-reviewed and platform validations), panel vendors bill on redirect
passbacks, and platforms silently stage rather than publish edits. Each of those failure classes is invisible in a casual preview
and cheap to catch here.

## When to use

Immediately before a soft launch or full launch; after any live patch to a
fielding instrument; when a vendor reports a broken redirect or "different
content"; when handed an unfamiliar survey to take over. Inputs: API
credentials and the survey id; ideally also the pre-registration or PAP (for
the report-only-vs-terminating posture), the vendor's integration sheet
(redirect URLs, ID parameter name), and the quota targets. A browser MCP
(claude-in-chrome or Playwright) enables Phase H; without it, run A–G and say
so in the report.

## Posture

- Read-only. `GET` everything; `PUT`/`POST` nothing. If the platform offers a
  no-op write check for token scope, that is the only write.
- Evidence or it didn't happen: every PASS cites the object read back (flow
  element, option key, quota logic), never the absence of an error.
- The registered design wins. Where a PAP declares an item report-only, a live
  branch that terminates on it is a **blocking** finding even if well-built.

## Phase A — identity and publish state

- Confirm the survey id, name, and active/inactive state match intent. An
  inactive instrument scheduled for launch is fine; an active one nobody meant
  to open is a finding.
- Publish state: the working definition and the published version must match.
  On Qualtrics, do not trust an `in_sync` flag alone — question- and
  quota-level writes can leave it true while respondents see an older version.
  The proof is the version list: a published entry, created by a publish call
  someone can vouch for, with the published content read back where the API
  exposes it (a description is provenance, not proof of content).
  Staged-but-unpublished edits to a fielding survey are a **blocking** finding.

- Response settings that shape the data: partial-response window, multiple-
  submission prevention, anonymization/IP recording, link type, expiration —
  and whether in-progress respondents stay pinned to the version they started.

## Phase B — consent before anything

- The first substantive screen a respondent reaches is consent (or a language
  selector whose every arm leads first to consent).
- Nothing evaluates or acts before affirmative consent: no terminating gates,
  no quality branches, no telemetry collectors on or before the consent page.
  (If the approved protocol places a minimal eligibility screener before
  consent, audit that instead for authorization, minimization, and whether
  pre-consent data are retained.)
  Location/device capture nodes may *write* earlier (platforms populate them at
  session start), but every branch that *reads* them must sit after consent.
- Decline path: declining consent must route to the vendor's screen-out (or the
  study's stated exit), not dead-end or count as a complete.
- Consent text ↔ configuration consistency, both directions: if invisible
  scoring or fingerprinting is enabled (reCAPTCHA, device checks), the text
  discloses it; if the text promises skippable questions, optional questions
  actually exist. A consent page describing a survey that isn't this one is a
  finding whichever direction the drift runs.

## Phase C — question integrity

- Force-response completeness: enumerate every question; classify descriptive
  (no answer possible), forced, requested, and unvalidated. The check is
  consistency, not a universal forced-by-default norm (optional is often the
  right call for sensitive items): every unvalidated answerable item must be
  one the design *names* optional, and if any exist, Phase B's
  consent-consistency check must see them.
- Attention and manipulation checks: present where the design says, and their
  *consequence* (terminate vs record-only) matches the registration. In the
  current environment, terminating on an attention check screens out humans
  while catching almost no agents — flag it as a design smell even when it
  matches the PAP.
- Multilingual instruments: first identify the architecture. Qualtrics'
  native translation layer keeps one block structure (audit translations for
  coverage); a branch-per-language build duplicates every block per arm — there,
  every item, choice set, validation setting, and embedded JS must exist
  symmetrically in each arm. A check present in one arm only, or logic testing
  "correct option NOT selected" on a twin build (the unanswered twin matches
  trivially and ejects the whole other arm), is a **blocking** finding.

## Phase D — flow structure

Walk the full flow tree, at every nesting depth:

- Block order matches the intended instrument; randomizers present with the
  intended settings (even presentation, subset size).
- Every embedded-data field is written before the first element that reads it
  (capture-before-gate). A guarded condition on a never-yet-written field is
  silently dead — it fails safe, which is exactly why nobody notices.
- Terminating branches: condition logic decodes to the intended trigger; inner
  flow sets the exit redirect *before* the End-of-Survey element; unique flow
  IDs throughout; the terminal "completion" redirect node is the last element.
- On branched (language/arm) instruments, structural checks run per arm, not
  once globally.

## Phase E — vendor integration

- Redirect pattern: a pre-consent default carrying the screen-out URL, a
  terminal overwrite carrying the complete URL, end-of-survey set to redirect
  to the piped field. Early leavers must exit as screen-outs, completers as
  completes, quota-fulls (if hard quotas exist) as quota-fulls — each URL
  byte-exact against the vendor's sheet.
- The vendor's respondent-ID parameter is captured as embedded data and echoed
  back on every exit path, including declines. Note: query parameters resolve
  into piped references at session start regardless of where (or whether) the
  field is declared — but declaration is what makes the value reliably saved
  and exported, so treat a missing declaration as a minor finding and a wrong
  parameter name as fatal.
- Enumerate which vendor endpoints can receive traffic and which are dead by
  design, and check that against what the vendor was told in writing. A quality
  or quota-full endpoint the vendor expects to fire, wired to nothing, is a
  relationship problem waiting for fieldwork.

## Phase F — quotas

- Decode every quota's logic against the live question's choices and audit it
  against the RATIFIED grid, not an assumed one: marginal-family designs
  should partition each frame exactly once with per-family targets summing to
  the commissioned N; interlocked or deliberately overlapping designs have
  their own intended structure (check the multiple-match setting). Screening
  categories ("I don't live here") belong to no quota either way.
- Hard vs soft actions match the ratified design; group labels say which is
  which truthfully.
- All counts are zero before fielding (test responses leave phantom counts even
  after deletion-with-decrement — read the actual counters).
- Platform-specific: on Qualtrics, choice conditions need `ChoiceLocator` as
  well as `LeftOperand` — the engine evaluates the latter, the editor renders
  from the former, and an editor save over a missing locator can blank live
  logic. Read both. Follow pagination: quota lists truncate.

## Phase G — anti-automation layer

- Platform toggles (bot-detection scoring, device fingerprinting, geo capture)
  are on if the design says so — and disclosed per Phase B.
- Behavioral instrumentation (interaction paradata, honeypots, page timers) is
  present on the pages the design instruments, in every language arm.
- The live-terminating set is restricted to signals that cannot plausibly be a
  real person: ineligibility, duplicate device, machine signature. Anything
  scored or graded (bot-score thresholds, fraud scores, speed cutoffs,
  attention items) belongs to analysis, not to a live gate — a scored live gate
  is a finding.

## Phase H — browser walk (optional, needs a browser MCP)

- Use the LIVE distribution link, never the preview (preview banners change
  rendering and skip embedded-data population). Append a test value for the
  vendor ID parameter.
- Walk at minimum: one decline (assert the screen-out redirect fires with the
  ID echoed), one complete per language arm (assert the complete redirect), one
  mobile-viewport pass (conjoint tables and stacked layouts render; nothing
  clips). Where feasible add: the quota-full path, one pass per experimental
  arm, a missing-vendor-ID entry, and validation/back-button behavior on one
  forced item.
- Confirm no screen precedes consent, and that the consent page renders in the
  right language for each arm.
- Clean up: delete the test responses with quota decrement, then re-read quota
  counts (Phase F) — and note that in-progress partials usually cannot be
  deleted via API and must expire or be cleared in the UI.

## Report

Rank findings **blocking / major / minor**, each with the evidence read back
and the phase that produced it. State explicitly: live version vs working
version; which phases ran (and that H was skipped, if it was); which findings
the registered design forces you to leave alone. End with the test-response
cleanup confirmation if Phase H ran. Hand fixes to a separate authorized
change — with its own backup, read-back, and publish-with-proof — rather than
folding them into the audit.
