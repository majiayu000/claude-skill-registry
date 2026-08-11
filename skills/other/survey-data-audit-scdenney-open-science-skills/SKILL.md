---
name: survey-data-audit
description: Audit fielded survey response data for registered elements, data quality, bot and AI-automation screening, and sample integrity. Emits an appendix-ready quality report.
argument-hint: "[path to the response export, plus the pre-registration or data-quality SOP if one exists]"
---

# Survey Data Audit

The pass a careful survey team runs between soft launch and analysis: confirm the instrument
captured what was registered, screen for automation and low-effort responding, reconcile the
realized sample against quotas and vendor dispositions, and emit an appendix table plus a methods
paragraph. Platform-agnostic; examples name Qualtrics-style fields because that is where the
field names are standardized.

## When to use

- Soft launch has landed (~50-150 completes per market) and a go/no-go read is due before full field.
- Fielding is complete and the data-quality appendix has to exist before anyone touches the outcomes.
- A vendor, reviewer, or PI asks what the study did about bots and AI respondents.

Not for reshaping conjoint exports (that is `conjoint-cleaning`), and not for inventing exclusion
rules a study should have registered (that is `pre-registration-writing`).

## Inputs

Required: a response-level export, one row per submission, partials and screenouts included where
the platform exports them.

Optional, each unlocking a phase:

- interaction paradata (per-page event counts, honeypot indicator, automation-surface flags)
- platform fraud fields (reCAPTCHA score, duplicate/fraud identity scores)
- geoip fields, IP, per-page timings, total duration
- vendor disposition file (completes billed, screenouts, quota-fulls, terminates)
- quota targets per cell
- the pre-registration, PAP, or data-quality SOP
- the instrument definition (QSF/JSON/codebook) for the expected-field manifest

## Precedence rule

**Registered definitions win.** If the study registered a composite flag, an exclusion rule, a
speeder cutoff, or an attention-check consequence, implement it exactly as written even where this
skill's default looks better. The battery below is the default only for what was never registered,
and everything it adds is report-only. Any deviation goes in the report, labeled post hoc.

## Phase 1 - structural completeness

Build the expected-field manifest from the **instrument definition, not the export header**. The
header shows what was captured; a field whose collector never fired is invisible there, and that is
exactly the failure worth catching. Diff manifest against export and report missing, unexpected,
and present-but-always-empty separately.

- **Paradata grammar parses.** Packed paradata (a delimited `key:value` string per page) must be
  parsed strictly, with parse failures counted as their own category. Present-but-unparseable is a
  collector bug and must never silently coerce to zero.
- **Unavailable is not zero.** Treat a missing field, or an initialization marker that is false, as
  *telemetry unavailable*. Report the unavailable share by country/arm and device class. On mobile
  browsers and in privacy modes this share is often large and structural, and reading it as
  "zero interaction" manufactures automation flags out of ordinary respondents. This is the single
  most consequential coding decision in the whole audit.
- **Response bookkeeping.** Filter previews and test channels out of the analytic frame; split by
  finished/termination status and distribution channel; check start/end/recorded timestamps for
  impossible orderings; confirm consent status on every analyzed row.
- **Duplicate identifiers.** Duplicate respondent IDs, duplicate vendor `uid` values, and one
  vendor ID mapped to several completes. Vendor uid collisions usually mean a redirect or link
  reuse problem, not fraud, so inspect before flagging.
- **Force-response integrity.** On *completed* responses, item nonresponse on a question the
  instrument forces is an instrument bug, not respondent behavior (partials legitimately truncate
  at the break-off page - separate them by finished-status first). Trace it to the flow (an unreached page, a broken
  branch, a display-logic fault, a mid-field version change) before recording it as missingness.
- **Version drift.** If the instrument was edited during fielding, partition responses by version
  and check that the change is invisible in the analyzed variables. Report the split.
- **Randomization coverage.** Every registered arm, level, and cell appears at a count plausible
  under its assignment probability and exposure denominator - compute the expected count before
  calling a sparse cell a bug (small cells can be empty by chance; a zero on a high-probability
  cell is a randomizer or spec fault found while it can still be fixed).

## Phase 2 - automation composite (hard signals only)

Exactly three signals, combined by OR. Each is *designed* to be machine-specific, and each has a
known false-positive mode that must be scanned before the composite is interpreted:

1. **Honeypot** - a hidden field, non-empty after whitespace trim, on any instrumented page.
   False-positive mode: aggressive autofill, password managers, accessibility extensions.
2. **Automation surface** - the driver property (`navigator.webdriver`) recorded as Boolean true.
   Unknown or absent is not true, and must not trigger. False-positive mode: legitimate testing
   stacks and kiosk builds.
3. **Zero interaction** - on at least one instrumented page with a submitted response *and*
   initialized telemetry, mousemove + click + keypress + touch events sum to zero.
   False-positive mode: assistive input and collector failure, which is why the
   telemetry-initialized condition is non-negotiable.

Nothing scored or graded enters the composite. The moment a continuous score becomes a gate, the
study owns a cutoff it chose after seeing data. Fraud scores, untrusted-event counts, repeat-task
consistency, speed, and device context are Phase 3 and cannot change composite status.

Interpretation, both directions:

- The composite **under-detects and over-detects at once**: it misses sophisticated agents
  (the driver property is trivially suppressible; extension-based agentic browsers typically never
  set it; CDP-driven agents dispatch *trusted* events, so their untrusted-event count stays zero -
  their tell is the mousemove distribution, which is descriptive here, never a gate), and it
  falsely includes the false-positive modes above. So it is a floor on *detectable* automation,
  not a bound on automation - and absence of all three signals is never evidence of humanness.
  Run the Phase 3 false-positive scans before reporting the flagged share as automation.
- Report each constituent share alongside the union. A composite driven entirely by one signal is a
  collector-bug hypothesis before it is a fraud hypothesis.

## Phase 3 - descriptive battery (report-only, never gates)

The numeric anchors below are vendor- and era-specific (2025-2026 validations); re-check
the current vendor documentation before leaning on any of them.

- **reCAPTCHA as a continuous score.** Report the distribution plus the share below 0.5 and below
  0.9. Do not use the platform's 0.5 threshold as a classifier: in Prolific's 2025 validation human
  scores cluster near 0.98 and agent scores near 0.69, so most agents clear 0.5 while a low-scoring
  human is common. The 0.9 shoulder carries more information than the nominal cut.
- **Identity/fraud scores.** Identify the provider and its documented scale first - conventions like fraud at or above 30 and duplicate score
  at or above 75. Flag-only. First confirm the license actually returned the fields, or a zero
  share will be reported as "clean" when it means "never measured."
- **Repeat-task agreement crossed with speed and flat telemetry.** Human test-retest agreement on
  an exact repeated task runs roughly 70-85%. Report the **joint tail** - perfect repeat agreement
  AND bottom-decile duration AND near-zero movement/touch - not the margins. Perfect agreement
  alone is a respondent with strong preferences.
- **Untrusted events.** Share with any `isTrusted == false` event, which indicates script-dispatched
  input, though other page scripts also generate them.
- **Honeypot false-positive scan.** Cases with honeypot triggered *and* rich human-like telemetry
  are usually password managers, autofill, or extensions. Inspect these before interpreting the
  honeypot share.
- **GeoIP out-of-country share**, and IP/geo disagreement with the sampling frame.
- **Speeders.** Compute from the realized duration distribution. Apply a cutoff only if one was
  pre-specified; otherwise report the distribution and treat any exclusion as an explicitly post hoc
  sensitivity. Never invent a cutoff after seeing outcomes.
- **Straightlining and non-differentiation** on multi-item batteries (zero within-battery variance,
  low SD, long identical runs). Note whether the battery contains reverse-coded items, because
  without them a flat pattern is genuinely ambiguous.
- **Logical consistency.** Impossible or contradictory answer pairs, language mismatch between
  arm and open text, and missingness that differs by treatment arm or device class.
- **Open-text screening.** Three checks, in descending order of evidential value: near-duplicate
  text across respondents (strongest), gibberish or off-topic filler, then LLM-style tells. Style
  detection is noisy and biased against fluent non-native writers - it flags a case for human read
  and never excludes on its own.
- **Attention and instructed-response checks, and any AI-use self-report.** Report pass and
  affirmation rates. Keep them outside every gate unless the study registered a consequence. Their
  weakness is the point of the whole exercise: in Westwood (PNAS 2025), AI agents completing survey
  instruments passed conventional attention and quality screens at near-ceiling rates.

## Phase 4 - sample integrity

- **Realized versus target, per quota cell.** Report short cells and over-filled cells. A cell far
  over target usually means quota enforcement sat with the vendor rather than the instrument.
- **Vendor disposition reconciliation.** Completes billed against completes in the data, plus the
  screenout, quota-full, and terminate paths. A few percent of drift is normal redirect loss; a
  systematic gap means the redirect or passback is broken, which is a launch-stopper for later
  waves and a billing dispute for this one.
- **Provider-flagged cases cross-tabbed with the composite.** Report the 2x2. Agreement is
  reassuring, disagreement is informative, and neither is a validation of the other, since the two
  measure different things on different data.
- **Differential attrition and break-off by arm and by page.** A design threat rather than a
  data-quality item, but it is found here and belongs in the same appendix.

## Phase 5 - the report

Two artifacts. First, an indicator table with countries/arms/waves as columns:

| Indicator | Site A | Site B |
|---|---|---|
| Completes in data (N) | | |
| Composite automation flag, % | | |
| - honeypot / driver property / zero interaction, % each | | |
| Telemetry unavailable, % (denominator note) | | |
| reCAPTCHA below 0.5 / below 0.9, % | | |
| Fraud >= 30 / duplicate >= 75, % (or unavailable) | | |
| Perfect repeat x fast x flat joint tail, % | | |
| Straightlining / speeders / out-of-country, % | | |
| Provider-flagged, % and overlap with composite | | |

Every cell carries its own denominator, and unavailable is printed as "unavailable" rather than
left blank or rendered as 0.

Second, the appendix methods paragraph:

> Data quality was assessed with pre-specified, report-only indicators [list]. A composite
> automation flag was set when at least one hard signal was present [three signals]. Missing or
> failed telemetry was coded unavailable, never zero. [X]% of completes were composite-flagged in
> [site], which we report as an estimate of potential automation-related contamination rather than
> as AI-assistance prevalence; self-reported AI use is reported separately at [Y]%. Primary
> analyses retain all flagged respondents; exclusions are limited to [registered rule]. We report
> one sensitivity analysis, the unchanged pipeline re-run on the not-flagged subset [result].
> [Indicator] was unavailable for [share] of cases in [subgroup] and is reported as such.

**Default: exactly one sensitivity re-run** - the registered pipeline, unchanged, once, on the
not-flagged subset. Not per-indicator subsets, not a cutoff sweep: a menu of re-runs is a garden
of forking paths wearing a quality-control costume. If the registration specifies a different
sensitivity structure, the precedence rule applies and the registered structure wins.

**State what gated live and what is post hoc.** The defensible live split, given current detection
accuracy, is that a session ends in real time only on a signal that cannot be a real person -
failed eligibility, duplicate device or identity, machine signature. Everything scored or graded
is analysis-side and report-only. Write that split into the report so a reader can tell which
numbers describe respondents who were turned away and which describe respondents who were kept.

## Ethics and reporting guardrails

- The composite estimates **automation**, not AI prevalence, and not respondent dishonesty. Never
  label it as any of those.
- Self-reported AI or LLM use is a separate estimand with a separate denominator. Do not merge it
  into the composite or report the two as one number.
- Retain flagged respondents by default. Excluding on a probabilistic quality score is itself a
  researcher degree of freedom, and one that correlates with device, locale, and disability.
- Document everything unavailable, by page and indicator. A silent gap reads as a measured zero.
- Keep per-respondent IP, geo, and raw paradata out of the public replication package.
  Publish the aggregate table, the code, and - subject to a disclosure-risk read, since even a
  derived quality flag can stigmatize - a per-respondent flag column.
- Instrumented pages must sit after affirmative consent. Telemetry collected on a consent page,
  including from people who decline, is not defensible.

## Quality Checks

- [ ] Expected-field manifest built from the instrument definition, diffed against the export
- [ ] Paradata parse failures counted separately from missing and from zero
- [ ] Telemetry-unavailable share reported by site and device class, never coded as zero interaction
- [ ] Duplicate respondent IDs and vendor uid collisions checked and explained
- [ ] Forced-item nonresponse traced to the flow before being called missingness
- [ ] Composite computed from hard signals only, with each constituent share reported alongside the union
- [ ] Composite described as a lower bound, with the CDP/trusted-event limitation stated
- [ ] reCAPTCHA reported as a continuous distribution, not the 0.5 classifier
- [ ] Identity/fraud fields confirmed as actually returned before a zero share is reported
- [ ] Repeat-task tail reported jointly with speed and flat telemetry, not as marginals
- [ ] Honeypot false-positive scan run before the honeypot share is interpreted
- [ ] No cutoff (speeder, straightlining, score) applied that was not pre-specified
- [ ] Open-text style tells flagged for human read, never used to exclude
- [ ] Realized sample reconciled against quota targets and the vendor disposition file
- [ ] Provider flags cross-tabbed with the composite, both reported
- [ ] Appendix table carries per-cell denominators and prints unavailable explicitly
- [ ] Exactly one sensitivity re-run, on the not-flagged subset, with the primary analyses retaining flagged cases
- [ ] Live-gated versus analysis-side indicators stated explicitly in the report
- [ ] Audit is scripted end-to-end from the raw export, which is preserved unmodified
