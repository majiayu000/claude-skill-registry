---
name: ai-seo
description: "Builds, measures, and improves an Answer Engine Optimization program across ChatGPT, Perplexity, Claude, Gemini, Google AI Overviews, and Copilot. Use for AEO, GEO, LLMO, AI search visibility, AI citations, brand mentions, answer-engine monitoring, llms.txt, AI crawler audits, or questions like 'what does AI say about us?' and 'why are competitors cited instead of us?'. Produces a durable evidence report and prioritized gameplan, not a one-shot content checklist."
category: seo
tier: nice-to-have
layer: execution
reads:
  - brand/voice-profile.md
  - brand/keyword-plan.md
  - brand/audience.md
  - brand/positioning.md
  - brand/competitors.md
  - brand/landscape.md
writes:
  - .aeo/config.json
  - .aeo/truth.md
  - .aeo/attributes.md
  - .aeo/prompts.json
  - .aeo/report.md
  - .aeo/gameplan.md
  - .aeo/worklog.md
  - .aeo/runs/
depends-on: []
triggers:
  - ai seo
  - ai search
  - perplexity
  - chatgpt ranking
  - ai overview
  - answer engine
  - llmo
  - geo
  - aeo
  - cited by ai
  - ai visibility
  - ai optimization
allowed-tools: []
---

# AI SEO — Durable AEO Program

Answer engines return synthesized verdicts, not ranked menus. This skill measures which brand attributes appear in those verdicts, identifies why gaps exist, and ships evidence-backed fixes. The unit of work is an **attribute**: one truthful thing the product should be known for in buyer language.

## On Activation

1. Read `brand/positioning.md`, `brand/audience.md`, `brand/competitors.md`, `brand/keyword-plan.md`, `brand/landscape.md`, and `brand/voice-profile.md` when present. Missing files reduce confidence but never block L0 work.
2. Check for `.aeo/config.json`, `.aeo/truth.md`, and `.aeo/runs/`.
3. Select the explicit mode, or auto-detect the next incomplete phase:

| Mode | Work |
|---|---|
| `setup` | Establish identity, truth, attributes, platforms, and prompt portfolio. |
| `audit` | Measure prompts and citations; inspect crawl/index/analytics evidence; diagnose gaps. |
| `plan` | Rebuild the prioritized gameplan from stored findings without new paid calls. |
| `fix` | Implement only approved on-page and technical items; brief off-page work. |
| `remeasure` | Re-run the frozen prompt set, compare with the previous run, and report uncertainty. |
| `report` | Regenerate report and gameplan from stored data; no network spend. |

4. State the mode, evidence sources available, degraded capabilities, and whether any call may cost money.
5. Continue autonomously except at the three human checkpoints: identity/attributes, spend approval, and gameplan execution approval.

## Durable State

Create `.aeo/` in the user's project:

```text
.aeo/
├── config.json       # schema version, site, markets, platforms, sampling policy
├── truth.md          # claim table grounded in code, docs, pricing, and changelog
├── attributes.md     # approved attributes and buyer language
├── prompts.json      # stable prompt IDs; never silently rewrite between runs
├── report.md         # dated evidence, rates, citations, gaps, and method
├── gameplan.md       # Now / Next / Later / Done actions linked to findings
├── worklog.md        # action, date, files, hypothesis, deploy/reference
└── runs/<iso-date>/  # normalized observations; raw/ contains private responses
```

During setup, add `.aeo/runs/**/raw/` to the user's `.gitignore` before storing any raw response. Keep only the minimum raw evidence needed, never store authentication/session data, and commit normalized observations only when the user wants the AEO history versioned.

The report is what someone can audit in six months. The gameplan is what the team acts on. Every recommendation links to a finding ID; every rate carries numerator, denominator, platform, and sample size.

## Program Phases

### 0 — Foundation

Detect the app/site/domain, build `.aeo/truth.md` from authoritative repository evidence, and propose 3–8 attributes. Ask the user to approve identity and attributes before measuring. Follow [foundation and prompt design](references/foundation-and-prompts.md).

### 1 — Prompt Portfolio

Turn each attribute into neutral buyer prompts spanning discovery, comparison, recommendation, use-case, objection, and factual verification. Freeze stable prompt IDs. Do not include the brand in unbranded discovery prompts or hint at the desired answer.

### 2 — Measure

Run the same portfolio across the available answer engines. Sample repeated observations because outputs are non-deterministic. Store mention, recommendation, factual accuracy, sentiment/position, citations, cited domains/pages, model/platform, timestamp, locale, account/mode, and response availability. Follow [measurement and statistics](references/measurement.md).

OpenSEO v0.1.6 supplies traditional discoverability evidence through ranked keywords, SERPs, backlinks, Search Console, GA4, URL inspection, and site audit. It does **not** currently expose AI Visibility over MCP; never report OpenSEO UI AI visibility as live MCP data. Follow [OpenSEO evidence routing](references/openseo-evidence.md).

### 3 — Diagnose

Route each gap to one primary cause:

- **Technical:** blocked crawler, indexing/canonical failure, rendering, malformed or contradictory structured data.
- **Comprehension:** the site does not state the attribute clearly, consistently, or extractably.
- **Trust/supply:** engines rely on third-party sources that omit, contradict, or outrank the first-party claim.
- **Measurement:** sample too small, platform inaccessible, prompt drift, locale/account confounder.

Use the citation supply chain before prescribing content. See [diagnosis](references/diagnosis.md).

### 4 — Gameplan

Order work by evidence strength × expected effect ÷ effort and risk. Each item must include finding ID, route, exact file/URL, owner type, expected observable effect, verification method, and status. Never promise a citation or ranking.

### 5 — Execute and Remeasure

After approval, implement repository-owned changes, show the diff, and leave outreach/listing/publishing to a human. Log every change as a hypothesis. Re-measure after an appropriate indexing window; do not attribute causality from one before/after movement. Follow [technical and content execution](references/execution.md) and [deliverables](references/deliverables.md).

## Metrics

Report per attribute and platform:

- Mention rate = mentions ÷ valid observations.
- Recommendation rate = positive recommendations ÷ valid observations.
- Citation rate = observations citing a first-party URL ÷ valid observations.
- Accuracy rate = correct factual claims ÷ scored factual claims.
- Share of voice = brand mentions ÷ all tracked brand/competitor mentions, with the exact denominator disclosed.

Do not combine platforms into one headline rate unless sample design and weighting are explicit. Never report a rate from one sample. Preserve missing/blocked/error observations separately from valid responses.

## Anti-Patterns: Non-Negotiable Safety and Honesty

1. **Never ask a leading question.** It manufactures the desired result instead of measuring buyer discovery.
2. **Never report a rate without numerator, denominator, and sample size.** One response is an anecdote.
3. **Never fabricate a quote, citation, source, statistic, crawler rule, or platform behavior.** Unknown stays `unknown`.
4. **Never manufacture consensus.** No astroturfing, fake reviews, sockpuppets, or bot-only content.
5. **Never cloak.** Serve engines and humans the same substantive content.
6. **Never auto-publish, auto-deploy, auto-submit listings, or contact people.** Prepare diffs and briefs; a human controls external state.
7. **Never spend without a preflight.** State provider, operation, count, and cost shape; wait for approval.
8. **Never claim causation from one correlation.** Log the hypothesis and test it over later runs.
9. **Never treat `llms.txt` as a ranking guarantee.** It is optional discoverability metadata, not proof of crawler support or citations.
10. **Never recommend allowing every AI crawler by default.** Training, retrieval, and user-triggered agents have different policy implications; present the tradeoff.

## Progressive Enhancement

| Level | Behavior |
|---|---|
| L0 | Repository truth, technical inspection, prompt plan, and explicit live-measurement gaps. |
| L1 | Brand memory narrows attributes and competitor set. |
| L2 | Search/crawl evidence validates discoverability and citation supply. |
| L3 | Direct platform observations produce sampled visibility metrics. |
| L4 | OpenSEO + GSC/GA4/logs connect AI visibility hypotheses to crawl, rankings, citations, and referrals. |

## Completion

Write `.aeo/report.md` and `.aeo/gameplan.md`, then record completion:

```bash
mktg run ai-seo --complete --writes .aeo/report.md,.aeo/gameplan.md --result success --json
```

Route resulting work to `seo-audit`, `seo-content`, `competitor-alternatives`, `off-page-seo`, or `seo-machine`; this skill owns measurement and prioritization, not duplicate execution playbooks.

---

Method informed by Initial Commit's public AEO program description at `initialcommit.co/library/skills/aeo`; this implementation is independently adapted to mktg's brand memory, OpenSEO boundary, safety model, and sprint-persistence contract.
