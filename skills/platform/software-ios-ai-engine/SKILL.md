---
name: software-ios-ai-engine
description: "Design local AI engines for iOS. Use when wiring Apple Foundation Models, local classifiers, extraction, summarization, grounded answers, and cloud fallbacks."
version: "1.1"
last_validated: 2026-07-11
---

# Local AI Engine on iOS

Use this skill when an iOS app should run useful AI behavior locally before spending cloud quota: Apple Foundation Models, deterministic local NLG, local retrieval stitching, local classifiers, extraction, summarization, tagging, rewrite helpers, and tool calls into app state. The common constraint is not "make chat smarter"; it is **pick the right local engine, shape the data contract, gate capability correctly, and keep cloud as an explicit upgrade or fallback**.

A major scenario is a rich, per-user structured context bundle (chart, Human Design, planning cache, knowledge chunks, activity ratings, dream themes, mood/energy, etc.) that needs to produce a real answer without cloud quota. In that case, the fix is never "make the reject card nicer." The fix is adding a local **Composer** tier between intent routing and cloud fallback.

This skill is for iOS product surfaces and local app-engine design. For pure retrieval/chunking/grounding strategy upstream of the local engine, route to `ai-rag`. For model serving/quantization tradeoffs beyond Apple platform APIs, route to `ai-llm-inference`. For evaluation of generated or extracted output, route to `ai-evals-observer`.

## Quick Reference

### Local Engine Patterns

| Pattern | Local engine | Best for | Fallback |
|---|---|---|---|
| **Structured generation** | Apple Foundation Models + `@Generable` | Short prose, extraction, classification, tagging, typed transformations | Deterministic local logic or cloud opt-in |
| **Deterministic NLG** | Sentence bank / templates / rules | Auditable answers, safety copy, older devices, per-locale consistency | Retrieval stitch or cloud opt-in |
| **Retrieval stitch** | Local top-k chunks + wrappers | Grounded explanations from existing knowledge chunks | Sentence bank or cloud opt-in |
| **Local classifier** | Regex, NaturalLanguage, embeddings, FM enum output | Routing, intent, entity extraction, safety boundaries | Conservative default route |
| **Tool-backed local model** | FM tool calling into app state | Model decides when it needs app data | Pre-fetch compact data if tool overhead is too high |
| **Reusable app AI foundation** | `LocalAIEngine` facade + deterministic fallback + optional Foundation Models | New iOS app skeletons that need AI-ready architecture before the first AI feature ships | No-op or sentence-bank engine |
| **Local semantic/vector search** | Natural Language embeddings, local vector table, or bundled retrieval units | User notes, settings, local knowledge, short document sets, app help, offline search | Server vector brain when corpus or sharing exceeds device scope |

For non-answer tasks, use [references/local-ai-task-patterns.md](references/local-ai-task-patterns.md) before reaching for the answer-composer references.
For reusable app foundations, use [references/foundation-models-app-skeleton.md](references/foundation-models-app-skeleton.md) and [references/on-device-vector-retrieval-ios.md](references/on-device-vector-retrieval-ios.md).

### The Three-Tier Architecture for Answer Surfaces

| Tier | Engine | Responsibility | Cost / latency |
|---|---|---|---|
| **0. Intent router** | Deterministic regex + lightweight classifier | Detect archetype (`reflect` / `interpret` / `guide` / `clarify` / `check_in`), extract slots, assemble evidence bundle | ~1 ms, free |
| **1. Composer** | One of: Foundation Models (A), sentence bank (B), retrieval stitch (C) | Render the bundle into 40–70-word grounded prose | 0–200 ms, free |
| **2. Cloud LLM** | Any cloud model your backend calls, chosen per product policy (not this skill's concern) | Deeper synthesis, multi-turn reasoning, novel question types | ~800 ms, counts against quota |

The Data-first pill owns Tiers 0 + 1. The cloud pill is Tier 2. When the user in your screenshot saw "Core works best with one specific angle", your product was doing Tier 0 *correctly* — but Tier 1 did not exist, so the answer became a rejection. See [references/three-tier-architecture.md](references/three-tier-architecture.md).

### Pick the Composer Strategy

Three engines. You usually ship more than one, with a fallback chain.

| | Option A — Foundation Models | Option B — Sentence Bank | Option C — Retrieval Stitch |
|---|---|---|---|
| **Engine** | Apple `FoundationModels` on-device ~3B LLM (iOS 26+) | Hand-curated prose fragments keyed by `(archetype, anchor, mood)` | Top-k retrieval over your knowledge chunks + boilerplate wrappers |
| **Voice quality** | Natural, conversational, feels personal | Curated, brand-consistent, can feel patterned over time | Mechanical, readable, "summary-ish" |
| **Ship time** | ~1 week (framework + prompt design + eval) | 1–3 days (fragment authoring dominates) | 1–2 days (retrieval already exists) |
| **Deterministic** | No — sampling | Yes — fully auditable | Mostly — retrieval is stable |
| **Offline** | Yes | Yes | Yes if retrieval is local |
| **Free / no-quota** | Yes (compute-free for users) | Yes | Yes |
| **Localization** | Needs multilingual prompt + per-locale QA | Per-locale fragment files (standard l10n flow) | Depends on knowledge chunks' language coverage |
| **Device requirement** | Apple Intelligence-capable: A17 Pro+/M-series with **8 GB+ unified memory** (iPhone 15 Pro+, all M-series iPads/Macs) | Any | Any |
| **Risk** | Hallucination if prompt underconstrained | Repetition; "feels canned" after N sessions | Chunk quality leaks into answer quality |
| **Deep dive** | [references/option-a-foundation-models.md](references/option-a-foundation-models.md) | [references/option-b-sentence-bank.md](references/option-b-sentence-bank.md) | [references/option-c-retrieval-stitch.md](references/option-c-retrieval-stitch.md) |

**Default recommendation for consumer iOS apps (2026):** Ship a deterministic local baseline plus Apple Foundation Models as an upgrade on capable devices. For answer surfaces, that usually means **B + A together, with B as universal fallback.** B closes the reject-card bug immediately; A then upgrades voice quality on iOS 26+ devices using the same bundle and the same `{ answer, grounding }` output shape. C is useful as a last-chance Tier-1 before falling through to Tier 2 or to deterministic safety copy. Rationale: [references/three-tier-architecture.md](references/three-tier-architecture.md#default-deployment).

### On-Device vs. Server: the Judgment Call

Don't default to "on-device because it's private" or "cloud because it's smarter" — decide per feature against four axes, in this order:

1. **Privacy ceiling.** If the product promise is "your data never leaves the device" (health, journaling, financial detail), on-device is not a preference, it's the requirement. Cloud — even Apple's own Private Cloud Compute — is disqualified regardless of quality, unless the user explicitly opts in per-request.
2. **Capability ceiling.** The on-device ~3B model (`AFM Core`, shipped in `FoundationModels` since iOS 26) is genuinely good at short structured generation, classification, and bundle-grounded prose — not at long multi-document reasoning, open-ended agentic planning, or tasks needing broad world knowledge outside the bundle. If the task exceeds that ceiling, no amount of prompt engineering fixes it; route to Tier 2 as an explicit upgrade, don't fight the model.
3. **Latency and cost.** On-device composition (Option A/B/C) is 0–250 ms and free; cloud is 600–1200 ms and metered. For a feature used dozens of times per session, on-device is the only shape that keeps the product usable and the margin sane. Reserve cloud for the minority of turns where depth matters more than speed.
4. **Device-fleet reality.** Roughly a third to a half of an app's iOS install base at any time is on hardware or an OS setting that cannot run Apple Intelligence at all (pre-A17 Pro chips, Apple Intelligence disabled, unsupported region/language, or `.modelNotReady`). A local engine that only works on capable devices is not a local engine — it's a feature flag with unclear rollback. Option B (or a deterministic non-AI path) is the actual floor.

**Memory ceilings, concretely (2026):** Apple Intelligence and the `FoundationModels` on-device model require **8 GB+ unified memory** (A17 Pro / M-series). Do not hardcode a device-model allowlist — check `SystemLanguageModel.default.availability`, because Apple has already shipped one exception that breaks naive device lists (base iPhone 16e ships 8 GB and qualifies; base iPhone 15/15 Plus have 6 GB and do not, despite being newer-adjacent hardware in some markets).

**Thermal and battery reality.** On-device inference competes with everything else running on the SoC. Under thermal throttling or low-battery mode, generation latency can jump from ~200 ms to multiple seconds, and in rare cases the session can time out. Put a hard latency ceiling on user-facing calls (see [references/option-a-foundation-models.md](references/option-a-foundation-models.md#performance-budget)) and fall through to Option B rather than let the UI hang.

**Graceful degradation is not optional.** Every feature that uses Option A needs a tested B/C path for: OS below 26, Apple Intelligence disabled, region/language not yet supported, model asset still downloading, and thermal/latency ceiling exceeded. Ship the fallback first; layer A on top.

### Non-Negotiables (apply to every local AI engine)

- **Typed output contract.** The UI or caller reads a Swift value, not raw model prose. For answer composers that means `{ answer, grounding, followUps[], safetyBoundary }`; for extraction/classification it means a typed enum/struct.
- **Capability gate before use.** Apple Foundation Models requires `SystemLanguageModel.default.availability == .available`; local fallbacks must work when the model is unavailable, disabled, not ready, or unsupported for the active language.
- **Context-window budget is real.** Count instructions, prompts, tools, schemas, outputs, and transcript against the on-device session window.
- **Local does not mean unvalidated.** Run post-processors or validators after model output: schema, anchors, enum membership, safety boundaries, word count, locale, and forbidden phrases as applicable.
- **Cloud is explicit unless product policy says otherwise.** Do not silently spend quota or transmit sensitive context after promising Data-first/offline behavior.
- **Do not make AI own deterministic chrome.** Fixed labels, chart controls, gate/channel names, and help-sheet UI copy belong in the app localization pipeline, not in runtime model output. The engine can return structured facts or prose; SwiftUI still owns localized fixed UI and visual inspection behavior.

For answer composers specifically:

- **Answer shape is the same contract across A / B / C.** The UI reads `{ answer, grounding, followUps[], safetyBoundary }` — composers differ only in how they fill it.
- **Grounding line is mandatory and concrete.** "Grounded in your Cancer Sun · Progressed Moon in Cancer · Generator Sacral" — names the actual anchors, not section labels like "Natal chart anchors · Plan snapshot."
- **Feel acknowledgment must land before astrology / interpretation.** For any archetype whose Tier 0 intent is `emotional_support`, the first sentence acknowledges the user's stated feeling. No composer is allowed to skip this.
- **No invented facts.** The composer can only reference signs, planets, numbers, themes, or chunks that appear in the evidence bundle. A composer that writes "Uranus influences your Mars" when no such transit is in the bundle is broken — this applies equally to Foundation Models, sentence banks, and retrieval stitchers.
- **Safety boundary overrides everything.** Crisis-pattern detection in Tier 0 redirects to a static supportive message with help-line resources; no composer runs. Clinical-adjacent language downgrades tone but does not bypass astrology. See [references/intent-router-patterns.md](references/intent-router-patterns.md#safety).
- **Word budget is hard.** 40–70 words for a chat bubble. Short paragraph, not a dashboard. No section headers inside the answer. No bullet lists.
- **Grounded observability.** Every composed answer emits a structured trace: which archetype routed, which evidence refs were selected, which composer ran, confidence, latency. Required for eval-observer regression gates.
- **Structured visualization contract.** If the answer surface feeds a deterministic diagram, return typed anchors and explanation IDs separately from prose. Do not ask the composer to decide zoom, filters, chart labels, or localized UI strings; those are native UI responsibilities with their own tests.

*(Full catalogs of patterns, anti-patterns, known traps, and scenarios live in the four sections below. Reflects July 2026 practice on shipped iOS 26 / Apple Intelligence and the `FoundationModels` framework. WWDC26 (June 2026) announced a third-generation Foundation Models lineup — an on-device `AFM Core Advanced` (20B, sparse, 12 GB+ unified memory), a `LanguageModel` protocol letting third-party providers back a `LanguageModelSession`, image/Vision input, and free Private Cloud Compute access for smaller developers — all scoped to **iOS/iPadOS/macOS 27, currently in developer beta and not yet shipped to users**. Treat those as roadmap, not as APIs to ship against, until 27 GAs; the shipped ~3B on-device model and the 4096-token session window described throughout this skill are unchanged in the current release.)*

## App Store Review For AI-Generated Content

A local AI engine generates user-facing content, which puts the app inside several App Store Review Guidelines that have nothing to do with model quality. Treat these as build-time constraints, not a pre-submission afterthought. Full pass/fail map: [../software-ios-design/references/app-review-guidelines-map.md](../software-ios-design/references/app-review-guidelines-map.md).

- **4.3(b) saturated-category gate — run this before scoping the engine.** Apple's Guideline 4.3(b) names categories it rejects "unless they provide a unique, high-quality experience," and the list explicitly includes **fortune telling** — i.e. astrology, horoscopes, tarot, numerology, palmistry, and dream interpretation. Adding AI does **not** clear this bar; it raises it. Do **not** propose, and do not let an operator ship, an app whose pitch reduces to "an AI horoscope/tarot reader" with generic readings and a Day-1 paywall. To pass: ship genuinely interactive, personalized, native functionality (ephemeris-accurate computation, on-device interpretation grounded in the user's own data, journaling/history, data-tied notifications), give substantial free value before any paywall, and differentiate from category clones in a way a reviewer sees in 30 seconds. If asked to scope a divination or spiritual-guidance app, say up front that the category is named in 4.3(b) and state the unique/high-quality requirement before proposing features.
- **1.2 applies to model output.** Any surface that emits content to the user needs a safety filter; surfaces where users can share generated content also need a report path. The Tier 0 safety boundary and refusal/crisis copy must be content that was actually reviewed — not free-form model prose. This is why safety copy is static and pre-authored, never composed (see the safety-boundary non-negotiable above).
- **2.5.2 — what you may and may not download.** Shipping or updating model weights, prompts, `@Generable` schemas, sentence-bank fragments, writing-style adapters, and retrieval data is allowed. Downloading executable code that changes the app's features or UI after review is not. A composer that pulls new *content* is fine; one that pulls new *behavior* is a rejection.
- **5.1.1 — generated content is still data.** If generated answers are stored or transmitted (cloud Tier 2), the App Privacy labels and permission strings must reflect it, and account-bearing apps need in-app account deletion (5.1.1(v)).
- **5.1.2(i) — disclose third-party AI, including your own Tier 2.** Apple's guidelines require clear disclosure, and explicit permission, before sharing personal data with third parties — a category that explicitly names third-party AI. If Tier 2 forwards the evidence bundle or question text to any cloud model (yours or a vendor's), the consent flow and privacy copy must say so before the first send, not just in a buried privacy-policy paragraph.

## Patterns, Anti-Patterns, Known Traps, and Scenarios

Full catalog (P1–P28, A1–A22, T1–T25, S1–S13) in [references/patterns-antipatterns-traps-scenarios.md](references/patterns-antipatterns-traps-scenarios.md). Key entries inline:

**Architecture (P1–P6, A4–A7):** every composer emits a single shared Swift value type; compose from a typed `EvidenceBundle`, never raw text; run the universal post-processor (anchor validator → word-count trimmer → forbidden-phrase filter) after every composer including Option A.

**Option A (P13–P17, P27–P28):** gate on `SystemLanguageModel.default.availability`, not OS version; token-budget counts instructions + prompt + tool defs + schemas + response against the 4096-token window; probe any FM capability beyond `@Generable` + plain completion before shipping it; write A's prompt from scratch for the bundle-first contract — never port a cloud prompt.

**Safety (P23–P24, A2, A16):** crisis patterns bypass all composers; cloud Tier 2 is an explicit user-visible CTA, never a silent fallback; safety routing is a Tier-0 decision, not a prompt instruction to the FM.

**Persistence (A21–A22):** `answerSource` and `grounding` must live inside the persisted jsonb row, not only in the HTTP envelope. Integration test: no successful compose row has `answerSource IS NULL` or empty `grounding`.

**Top traps by day-cost:** T2 (simulator lies about FM availability — always test on physical device); T6a (tool/schema overhead omitted from 4096-token budget); T13 (trimmer removes grounding line); T19 (fallback-chain silent regression when feature flag flips); T25 (cohort ramp built before any users exist).

## Core Workflow

1. **Name the local task.** Is it classification, extraction, summarization, rewrite, tagging, grounded answer composition, or tool-backed action planning? Do not start with "chat" unless the user-facing surface is actually chat.
2. **Choose the smallest reliable local engine.** Regex/rules for high-precision routing, NaturalLanguage/embeddings for lightweight semantic matching, sentence bank for audited prose, retrieval stitch for existing knowledge chunks, Apple Foundation Models for structured generation or natural language synthesis.
   - For reusable app skeletons, create the `LocalAIEngine` interface and deterministic fallback even if Foundation Models ships later.
3. **Lock the typed contract.** Write the Swift struct / enum the caller consumes. Use `@Generable` for Foundation Models where the model should emit the type directly; use deterministic structs for rule/template paths. For non-answer examples, see [references/local-ai-task-patterns.md](references/local-ai-task-patterns.md).
4. **Build routing and bundle assembly first.** Classifier, slot extraction, evidence bundler, safety boundary, and locale run unchanged whether A / B / C composes. [references/intent-router-patterns.md](references/intent-router-patterns.md).
5. **Ship a deterministic local fallback.** Even if Apple Foundation Models is primary, local rules/sentence bank/retrieval stitch must cover unavailable devices, model-not-ready states, validation failures, and older OS versions.
6. **Layer Apple Foundation Models on capable devices.** Same input bundle, same output contract, availability gated by `SystemLanguageModel.default.availability`. [references/option-a-foundation-models.md](references/option-a-foundation-models.md).
7. **Use retrieval stitch where knowledge already exists.** For long-tail interpretation or documentation-backed answers, prefer local top-k chunks plus wrappers over asking the model to invent missing knowledge. [references/option-c-retrieval-stitch.md](references/option-c-retrieval-stitch.md).
8. **Wire cloud as explicit opt-in or documented policy fallback.** Tier 2 spend/transmission must be visible when Data-first/offline is a product promise.
9. **Instrument the eval loop.** Per local task: engine used, latency, validation result, fallback reason, safety boundary, locale, and task-specific quality metrics.

## ASCII Flow

```text
iOS local AI request
  -> Name task: classify, extract, summarize, rewrite, tag, answer, or plan
  -> Choose smallest reliable local engine before cloud
  -> Lock typed Swift contract and fallback behavior
  -> Assemble evidence bundle, safety boundary, and locale inputs
  -> Gate Foundation Models by availability and validation
  -> Instrument latency, engine, fallback, and quality metrics
```

## Craft Checklist

Before marking a local AI engine pass as complete, verify:

1. **Contract conformance** — output matches the locked Swift type; no composer-specific fields leak into the UI.
2. **Anchor count** — every answer names at least 2 concrete anchors from the evidence bundle (sign, planet, phase, Personal Day, HD type/authority, specific knowledge chunk). No generic "the stars align" filler.
3. **Feel-first for emotional intent** — first sentence acknowledges the stated mood before any astrological framing.
4. **Ordinal formatting** — house references use "1st / 2nd / 3rd / 4th" never "1th / 21th". Centralize via a single `formatOrdinal` helper (server *and* client); invariant-test it.
5. **No forbidden phrases** — blocklist "invites you to approach this thoughtfully," "trust the universe," "the stars are aligning," and any composer-specific stock phrasing that shows up too often in logs.
6. **No invented transits / placements** — assert the answer text only mentions signs, planets, houses, or HD attributes present in the bundle. An offline validator should catch this before the text reaches the UI.
7. **Word count within 40–70** — hard trim with a structured "too long, retry" step rather than rendering an over-limit bubble.
8. **Locale cleanliness** — every user-facing string goes through l10n. Composer output generated in the user's locale (not translated post-hoc).
9. **Determinism knob** — sampled composers (Option A) include a request ID + seed where the platform allows, so "Retry" produces a meaningfully different answer rather than the same one re-rolled.
10. **Safety routes mapped** — crisis patterns bypass all composers; clinical patterns soften tone; emotional patterns trigger the feel-first rule.
11. **Grounding line passes the "anchor test"** — if you strip it out of the answer, could a careful reader reconstruct "which two or three facts this was based on"? If it's ambiguous ("your chart energy"), it fails.
12. **Accessibility** — answer bubble + grounding line combine as one VoiceOver element; action row items announce individually; follow-up chips announce as buttons with hint. See [software-ios-design](../software-ios-design/SKILL.md) craft patterns.
13. **Deterministic replay in tests** — every composer has a pure function at its core (bundle in → answer out); UI integration is a thin wrapper. No network, no random state, no global clock inside the composer itself.
14. **Non-answer task coverage** — classification, extraction, summarization, tagging, rewrite, search, and tool-backed actions use the smallest reliable local engine, typed outputs, validators, and fallback rules from [local-ai-task-patterns.md](references/local-ai-task-patterns.md).
15. **Persistence parity with the contract** — every field the UI reads (`answerSource`, `grounding`, `bestTime`, `followUpSuggestions`) is also written inside the persisted row, not just the outer HTTP envelope. Integration test asserts no successful compose stores `answerSource IS NULL` or an empty `grounding` for a bundle that had anchors.

## Fact-Checking

- Verify Apple Foundation Models behavior against current Apple Developer Documentation before claiming availability, language support, context-window size, tool-calling behavior, or safety/error semantics.
- Treat community reports and app-store anecdotes as signals only. Convert them into local repros or Apple-doc-backed constraints before adding a "known trap."
- For current iOS point-release regressions, cite the exact OS, device class, Xcode version, and physical-device/simulator status in the trace or recommendation.
- Recheck `data/sources.json` at least quarterly and whenever Apple ships a major iOS/FoundationModels update.

## Route Elsewhere

- [`software-ios-design`](../software-ios-design/SKILL.md) — for the *surface* that renders the answer (bubble, grounding line, action row, follow-up chips, detents).
- [`software-ios-native`](../software-ios-native/SKILL.md) — for broader SwiftUI architecture, Observation, concurrency, and release gates around the composer layer.
- [`ai-rag`](../ai-rag/SKILL.md) — for the retrieval stage feeding the evidence bundle (chunking, hybrid search, reranking, freshness).
- `ai-context-layer` — for the durable per-user context store that assembles the bundle.
- [`ai-prompt-engineering`](../ai-prompt-engineering/SKILL.md) — for the prompt contract inside Option A (voice, anchor rules, anti-hallucination).
- [`ai-llm-inference`](../ai-llm-inference/SKILL.md) — for deeper model-choice tradeoffs (Apple FM vs an MLX-served open-weight model vs cloud), tokenization, and inference perf.
- `ai-evals-observer` agent/team — for regression gates and trace grading of composer output when available.
- [`software-ios-runtime-debugging`](../software-ios-runtime-debugging/SKILL.md) — when composer output doesn't match source after a build (stale install, not a composer bug).

## Navigation

### Architecture

- [references/patterns-antipatterns-traps-scenarios.md](references/patterns-antipatterns-traps-scenarios.md) — full pattern catalog (P1–P28), anti-patterns (A1–A22), known traps (T1–T25 as decision tables), and scenarios (S1–S13)
- [references/local-ai-task-patterns.md](references/local-ai-task-patterns.md) — non-answer local AI tasks: classification, extraction, summarization, tagging, rewrite helpers, semantic search, tool-backed actions, traps, and scenarios
- [references/three-tier-architecture.md](references/three-tier-architecture.md) — Tier 0 / 1 / 2 decision framework, fallback chain, cost model, default deployment
- [references/intent-router-patterns.md](references/intent-router-patterns.md) — archetype classification, slot extraction, evidence bundling, safety routing
- [references/composition-with-rag-context-vector.md](references/composition-with-rag-context-vector.md) — end-to-end composition with `ai-rag` + `ai-context-layer` + `ai-vector-brain` for natural conversational surfaces, Path A (Apple Foundation Models) and Path B (vector-DB-only) for three generic domain shapes (consumer reflection, regulated copilot, multi-turn emotional companion)
- [references/foundation-models-app-skeleton.md](references/foundation-models-app-skeleton.md) — reusable `LocalAIEngine` facade, Foundation Models service, typed contracts, fallback behavior, and App Intents/tool-call boundaries for generic iOS apps
- [references/on-device-vector-retrieval-ios.md](references/on-device-vector-retrieval-ios.md) — local semantic search and vector retrieval options for iOS: Natural Language embeddings, SQLite/vector tables, bundle mirrors, eval gates, and when to route to `ai-vector-brain`

### Composer Options

- [references/option-a-foundation-models.md](references/option-a-foundation-models.md) — Apple `FoundationModels` framework composer, `@Generable` output, availability gating, guardrails
- [references/option-b-sentence-bank.md](references/option-b-sentence-bank.md) — deterministic fragment composer, authoring workflow, l10n, anti-repetition
- [references/option-c-retrieval-stitch.md](references/option-c-retrieval-stitch.md) — glass-box retrieval-stitching composer, scoring, safety wrappers

### Integration

- [references/swiftui-composer-integration.md](references/swiftui-composer-integration.md) — wiring composers behind a shared protocol, fallback chain, capability gates, observability

### Templates

- [assets/template-foundation-models-service.md](assets/template-foundation-models-service.md) — capability-gated Foundation Models service behind a deterministic fallback
- [assets/template-local-retrieval-tool.md](assets/template-local-retrieval-tool.md) — local retrieval service/tool contract for semantic search and Foundation Models tool calls

### Foundations

- [references/nlg-fundamentals.md](references/nlg-fundamentals.md) — content determination → sentence planning → surface realization, why templates alone fail, why LLM alone over-invents

### Data

- [data/sources.json](data/sources.json) — primary research + vendor-doc sources backing this skill

## Verification Gate

Before concluding a local iOS AI engine recommendation or implementation:

- Verify the local task has a typed output contract and a deterministic fallback.
- Verify Apple Foundation Models availability is gated by API status, not OS version or device guesses.
- Verify prompt + tool + schema + response budget fits the on-device context window.
- Verify the target Data-first path answers an emotional / open question with real prose, not a reject card.
- Verify the answer contract is shared across all composers and the UI renders from a single type.
- Verify every answer names ≥ 2 concrete anchors from the evidence bundle in both the `answer` and the `grounding` fields.
- Verify the ordinal helper is used everywhere a house number could reach a template (no `${n}th` concats anywhere).
- Verify Apple Foundation Models availability is gated, and unavailable devices have a working B/C fallback path.
- Verify the safety router catches crisis patterns *before* any composer runs, and emotional patterns *before* the voice contract is selected.
- Verify word count is bounded — soft trim at the composer, hard retry if the trimmed answer loses anchors.
- Verify no user-facing string (answer, grounding, follow-ups, safety copy) bypasses l10n.
- Verify observability emits per-answer `{ archetype, composerUsed, anchorCount, wordCount, latencyMs, groundingScore, refusalReason? }`.
- Verify the "cloud upgrade" affordance is explicit, not silent fallback.
- Verify every persisted answer row carries `answerSource` and `grounding` inside the jsonb — not just in the HTTP response envelope — so evals, audits, and head-to-head replays can attribute every row to a composer.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
