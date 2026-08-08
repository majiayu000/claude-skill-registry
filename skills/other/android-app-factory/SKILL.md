---
name: android-app-factory
description: "Plan, build, test, and release a production-grade native Android app from a product idea through Google Play. Use for requests to create, ship, submit, monetize, or modernize an Android app. Covers Kotlin and Jetpack Compose architecture, API-level policy verification, accessibility, privacy and Data Safety, Play Billing, Play Integrity, account deletion, testing, performance, store assets, signing, staged rollout, and a release evidence gate. Not for iOS work or a review-only pass on an existing app."
---

# Android App Factory

## Gate policy — advisory, not blocking

Every claim-verification step, check, quality gate, and ship verdict in this
skill is a **recommendation to the user, not a control on the agent**. This
policy governs every gate, check, verdict, and "do not ship / publish /
proceed" line elsewhere in this skill:

- Run every check and report the results honestly. Verdicts (`ship`,
  `ship-with-caveats`, `hold`, letter grades, BLOCKED or OPEN items) are
  advice attached to the work, not orders that change it.
- Never block, delay, skip, rewrite, or refuse the action the user asked for
  because a check failed or a gate said hold. Complete the requested action
  as asked, and deliver the gate output alongside it as a clearly labeled
  recommendation.
- A failed gate changes what you report, never what you do.
- Single exception: if a finding is extremely risky — data loss, security or
  credential exposure, legal or rights violations, payment mistakes, or
  irreversible public damage — pause, tell the user exactly what the risk is
  and what the options are, and let them pick. Their choice is final.


## Principle

Build the product, policy evidence, and Play listing together. A successful
release is an installable and usable app whose claims, disclosures,
entitlements, privacy behavior, and store configuration agree.

## Source Truth and Freshness

At the start of every release-oriented run:

1. Identify the exact repo, package/application ID, branch, Play app, target
   track, and whether the checkout is dirty.
2. Read `references/play-policy-baseline.md`.
3. Re-open the linked official Google sources for any submission-sensitive
   requirement. Record the URL, observed requirement, and check time in
   `assets/android-release-gate.template.md`.
4. Treat current repo code and the live Play Console as source truth for the
   app. Treat the reference date as a baseline, not permanent policy.

On 2026-07-19, the factory default for a general phone/tablet release is
`compileSdk = 36` and `targetSdk = 36`. Google Play's announced enforcement for
new apps and updates moves to API 36 on 2026-08-31; API 35 remains the enforced
minimum before that date. Do not misstate the announced deadline as already
enforced, and recheck because form-factor exceptions and dates differ.

## Delivery Contract

Lock these before implementation:

- user and one core outcome;
- supported form factors, devices, locales, minimum SDK, and offline behavior;
- application ID, ownership, signing model, Play app/track, and release owner;
- data inventory, third-party SDKs, permissions, account model, deletion path,
  privacy policy owner, and Data Safety owner;
- monetization and entitlement source truth, or an explicit free-v1 decision;
- architecture and migration constraints;
- acceptance devices/API levels, tests, performance/accessibility targets,
  store artifacts, and release evidence;
- external mutations requiring confirmation: product creation, credential use,
  Play upload, track promotion, staged rollout, or production release.

Unknowns stay unknown. Never invent a package name, product ID, policy answer,
privacy URL, customer claim, or Play Console state.

## Production Pipeline

1. **Validate the product** — define the user outcome and evidence of demand.
   Treat keyword research as one input, not proof of product-market fit.
2. **Verify policy** — capture current target-SDK and form-factor rules, app
   access requirements, Data Safety scope, content rating, account deletion,
   billing policy, and any permission-specific declarations.
3. **Design architecture and risk** — use the smallest maintainable architecture
   that preserves unidirectional state, lifecycle safety, offline/error/loading
   states, test seams, and a least-data/least-permission posture.
4. **Scaffold** — native Kotlin + Jetpack Compose by default. Resolve current
   stable Android/Jetpack versions from official sources, lock them in a version
   catalog, and prove a debug build before feature work.
5. **Build the core loop** — implement one complete user outcome with real or
   deterministic demo data. Add history, saved state, sync, or accounts only
   when the product contract requires them.
6. **Prove quality** — unit, repository, ViewModel, Compose UI/instrumented,
   accessibility, and end-to-end core-loop tests as applicable; static analysis,
   release build, device/API matrix, baseline profile, and Macrobenchmark.
7. **Add monetization safely** — use Play Billing for covered digital goods,
   process pending purchases, verify and acknowledge purchases after entitlement
   handling, restore ownership, and keep secrets/server verification off-device.
8. **Complete trust surfaces** — privacy policy, Data Safety, SDK data behavior,
   permission rationale, in-app and web account deletion when accounts exist,
   content rating, ads declarations, app access instructions, and Play Integrity
   only where abuse risk justifies it.
9. **Build store artifacts** — truthful listing, icon/feature graphic,
   screenshots for every declared form factor, localization, support contact,
   release notes, and reviewer instructions.
10. **Release through evidence gates** — signed AAB and Play App Signing,
    internal/closed validation, pre-launch report, explicit confirmation before
    upload or promotion, staged production rollout, and post-release monitoring.

Read these before building:

- `references/android-factory-pipeline.md` — phase artifacts and release flow;
- `references/architecture-and-quality.md` — architecture, tests,
  accessibility, performance, and build checks;
- `references/privacy-billing-integrity.md` — privacy, Data Safety, account
  deletion, Billing, and Integrity controls;
- `references/play-policy-baseline.md` — dated official-policy baseline.

## Public-Safe Defaults

- Use placeholder IDs such as `com.example.product` until ownership is verified.
- Keep upload keys, passwords, service-account JSON, API secrets, and production
  identifiers outside Git; use local/CI secret stores and prove ignore rules.
- Use Play App Signing and a distinct upload key.
- Prefer a free v1 when Billing would delay validation, but do not bypass Play
  Billing for covered digital goods.
- Collect no data and request no permission without a stated product purpose,
  retention/deletion rule, disclosure path, and test.
- Treat Play Integrity as an abuse signal, not authentication and not the sole
  basis for a permanent block.
- Keep submission and rollout actions human-confirmed and reversible where the
  platform permits.

## Release Gate

Copy `assets/android-release-gate.template.md` into the app repo and complete it
with links or command output. Block release when any required item lacks
evidence, including:

- target policy was not checked live or the build targets the wrong API/form
  factor;
- a release targeting Android 15+ has not been verified for 16 KB page-size
  compatibility on 64-bit devices, including transitive native SDKs;
- `test`, lint/static analysis, `assembleRelease`, or `bundleRelease` fails;
- the core loop fails on the declared device/API matrix or offline/error path;
- accessibility checks, large text, TalkBack, keyboard/switch access, contrast,
  or reduced-motion behavior have launch-critical failures;
- performance evidence is missing for startup or the core task, or a known
  regression exceeds the product budget without approval;
- Data Safety, privacy policy, permissions, account deletion, content rating,
  ads, app access, or SDK behavior disagree;
- Billing entitlement, pending, restore/requery, acknowledgement, cancellation,
  refund/revocation, or backend verification behavior is unproven when relevant;
- secrets or signing material are committed, or Play App Signing/upload-key
  ownership, developer verification, or package registration is unresolved;
- listing claims or screenshots show behavior not present in the release build;
- a Play upload, track promotion, or rollout lacks explicit user confirmation.

Return one gate: `ship`, `ship-with-caveats`, or `hold`. A caveat must have an
owner, risk, and next action; policy, security, privacy, billing, crash, and
core-task blockers cannot be downgraded to cosmetic caveats.

## Routing

- Existing-app findings-only review → `suede-code-review`.
- CI implementation around the release evidence → `suede-ci-gate`.
- Coordinated architecture, product, policy, store, and QA lanes →
  `suede-agent-teams` with exclusive file ownership and a serialized release
  lane.
- iOS work → the relevant iOS skill, not this one.

## Boundaries

- Do not submit, create products, change pricing, promote tracks, or start a
  production rollout without explicit confirmation.
- Do not answer Play policy or Data Safety questions from memory when live
  official guidance or the Play Console is available.
- Do not claim release-ready from a debug build, screenshot, local source
  inspection, or successful upload alone.
- Do not use Play Integrity as a substitute for server authorization, purchase
  verification, rate limits, fraud operations, or an appeal path.
- Do not call a Data Safety form complete until first-party code and every
  included SDK have been inventoried against actual release behavior.
