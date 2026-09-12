---
name: seo-machine
description: "Build an organic-traffic operating system for any site or app: a multi-phase, resumable engine that plans and ships a BATCH ROADMAP of landing pages (use-cases, playbooks, /for/ pages, roundups) on top of real keyword research, with a persistent phase tracker. Use when the user says 'SEO machine', 'build organic traffic', 'rank on Google', 'we need traffic', 'SEO roadmap', 'batch of pages', 'pages roadmap', or 'build an SEO engine'. Distinct from `seo-audit` (one-off diagnostic) and `seo-content` (single-article writer): this skill owns the multi-page roadmap, run sequencing, page generation, internal linking, and the persistent phase tracker across the whole run. For a single alternatives or vs/comparison page, see /competitor-alternatives; for programmatic SEO templates and content at scale, see /seo-content; for off-page link building, see /off-page-seo. Resumable — every invocation continues the last run."
category: seo
tier: nice-to-have
reads:
  - brand/keyword-plan.md
  - brand/positioning.md
  - brand/competitors.md
  - brand/audience.md
  - brand/stack.md
writes:
  - docs/seo-machine.md
  - .seo/brand.md
  - .seo/link-inventory.md
  - .seo/config.json
triggers:
  - seo machine
  - build organic traffic
  - rank in google
  - seo roadmap
  - batch of alternatives pages
  - batch of pages
  - pages roadmap
  - we need traffic
---

# SEO Machine

End-to-end engine for building organic search traffic. Ships dozens of programmatic landing pages — alternatives, comparisons, use-cases, playbooks — backed by real keyword research, with a persistent roadmap the user resumes across sessions.

Conversion-first (alternatives + comparisons before blogs). Publish-early (a thin page indexed today beats a perfect page indexed in three weeks). Stack-native (writes into the user's framework — Next.js, Astro, Rails+Inertia, or a portable markdown fallback).

## Two modes, auto-detected

| Mode | When | What it produces |
|---|---|---|
| **Initialize** | `docs/seo-machine.md` does not exist | Stack detection → brand context → keyword research → tech audit → roadmap + link inventory |
| **Resume** | `docs/seo-machine.md` exists | Reads the tracker, picks the next pending phase (or one the user names), executes end-to-end through the quality gates |

Detection rule on every invocation: check `docs/seo-machine.md` at repo root (or the path recorded in `.seo/config.json`). No file → Initialize. File exists → Resume. The user does not need to remember which mode they're in.

## Publishing Order (the load-bearing decision rule)

The roadmap orders patterns by **conversion intent first, traffic intent second**. This is the single most important decision the skill makes — it's why the alternatives + comparison pages ship before the playbooks + blog posts.

| Order | Pattern | Why | Cost |
|---|---|---|---|
| 1 | `/alternatives/[competitor]` (Pattern A) | Highest conversion intent — the reader is already in market | ~4 hours per page |
| 2 | `/compare/[a]-vs-[b]` (Pattern D) | Be the third option in any two-vendor comparison | ~3 hours per page |
| 3 | `/for/[use-case]` and `/for/[audience]` (Pattern B/C) | JTBD without competitor name in query — high TP/volume ratio | ~4-5 hours per page |
| 4 | `/playbooks/[topic]` (Pattern E) | Authority + AI-citation surface area + inbound link draw | ~2-3 days per page |
| 5 | `/blog/...` (out of scope here) | Lowest conversion intent; defer until ~10 indexed pages exist | — |

**Why this order matters:** alternatives pages convert 5–20× blog posts at 1/10 the search volume. Shipping one alternatives page is worth ten generic blog posts on the same topic. The roadmap should reflect this — Phase 0 (tech audit) → Phases 1–N (alternatives, then comparisons, then use-cases) → late phases (playbooks) → never (blogs, unless explicitly requested by the user).

Striking-distance boosts (pages already ranking pos 5–20 in GSC) jump the queue when they exist — fastest wins per hour of work.

---

## On Activation

1. Load brand context where present: `brand/keyword-plan.md`, `positioning.md`, `competitors.md`, `audience.md`, `stack.md`. Missing files are fine.
2. Surface what loaded:

## Backend Selection

Validate KD/competition with OpenSEO `get_keyword_metrics` / `get_serp_results` before generating pages; consume `openseo-keyword-clustering` outputs when present. Qualitative research uses Exa-stack (or manual) per the shared ordered resolver — record `research_backend` in `.seo/config.json`. Full contract: `skills/openseo/references/backend-contract.md`.

```
Brand context loaded:
├── Keyword Plan    ✓/✗  (seeds the roadmap; ✗ → generate during Initialize)
├── Positioning     ✓/✗  (drives /compare and /alternatives angles)
├── Competitors     ✓/✗  (target list for /alternatives pages)
├── Audience        ✓/✗  (intent buckets for /for/<persona> pages)
└── Stack           ✓/✗  (selects references/stacks/<framework>.md)
```

Progressive enhancement: with zero brand files the skill still works — it derives signal from the repo during Initialize Step 2. With full brand context it skips re-discovery and goes straight to research + roadmap.

Exa recipes: `references/exa-recipes.md` + `references/api-stack-recipes.md`. Manual fallback: `references/manual-research.md`. Ahrefs is an optional paid overlay only (see Exa recipes appendix).

---

## Hard prerequisites

| # | Check | Failure mode |
|---|---|---|
| 1 | `git rev-parse --is-inside-work-tree` succeeds | Stop. Tell the user this skill writes a persistent roadmap; initialize git or run from a repo. |
| 2 | A stack is detectable — one of `package.json`, `Gemfile`, `composer.json`, `requirements.txt`, `astro.config.*`, `next.config.*`, `nuxt.config.*`, `gatsby-config.*`, `_config.yml`, `config.toml`, `pyproject.toml` | Ask the user what stack they're on before continuing. |
| 3 | Research backend resolved (`skills/openseo/references/backend-contract.md`) | Never refuse to run — fall through to manual mode. |

---

## Initialize mode

Goal: end the run with a written `docs/seo-machine.md` containing keyword research, a phase tracker grouped by pattern, and technical-audit findings — plus `.seo/brand.md` and `.seo/link-inventory.md`.

### Step 1 — Detect stack + frontend convention

Read `references/stacks/detection.md`. Identify framework family, routing convention (file-based vs controller-based), component language, and existing marketing pages (`git ls-files | grep -iE 'marketing|landing|pages/(home|about|pricing)'`). Resolve ambiguity with `AskUserQuestion`. Persist to `.seo/config.json`.

### Step 2 — Detect brand + product context

Read every signal first, propose `.seo/brand.md`, then ask only about gaps. Signals: `CLAUDE.md`, `README.md`, `package.json` / `Gemfile.lock`, `tailwind.config.*` or design-token CSS, `app/views/marketing/*` or `pages/index.*`, `pricing` page.

If `brand/voice-profile.md` and `brand/positioning.md` already exist (mktg-native project), read them and skip 80% of the questions — those files already say who the buyer is and what the brand sounds like.

Otherwise use a single `AskUserQuestion` (3–4 questions max) to fill gaps. Required to know:

- **Product one-liner** (≤20 words)
- **Primary persona** (e.g. "B2B SaaS founder", "indie agency owner")
- **3–7 direct competitors** by name
- **Brand voice tags** (e.g. "honest, technical, no-jargon")
- **Free tier?** (drives the "is [brand] free" keyword strategy)
- **Anti-positioning** — what the product does NOT do (used in honest comparison sections)

Write to `.seo/brand.md` using `assets/brand-template.md` as the skeleton.

### Step 3 — Keyword research (Exa-native stack)

Follow `references/exa-recipes.md` — 7 Exa-native recipes that replace the Ahrefs cookbook:

| Recipe | Purpose | Primary API |
|---|---|---|
| A. Domain baseline | DR estimate from indexed-page count + brand mentions + GitHub stars (OSS) | Exa `company_research_exa` + `web_search_advanced_exa` + `gh` |
| B. Competitor reverse-lookup | What competitors rank for | Exa `web_search_advanced_exa` `site:<competitor>` + AI summary |
| C. Use-case sweep | `/for/` and `/playbooks/` topic discovery | Exa `deep_search_exa` + Firecrawl autocomplete + `/last30days` |
| D. Comparison volume | Validate demand for `/compare/[a]-vs-[b]` before writing | Exa `web_search_advanced_exa` + Firecrawl SERP scrape |
| E. SERP saturation | Replaces Ahrefs KD with SERP-composition-derived signal | Exa search + per-result `company_research_exa` |
| F. Backlink prospecting | Referring-domain proxy via Exa | Exa search + DR proxy (see `off-page-seo` skill) |
| G. Content gap | Their indexed keywords − ours, ranked by DR-cap fit | Recipes B + own-site Exa lookup |

Then pull cross-API compound recipes from `references/api-stack-recipes.md` for moves Ahrefs alone can't do — pain-point cluster discovery (`/last30days` + `mktg-x` + Exa deep search), OSS competitor teardown (`gh` + DeepWiki + Exa), outreach prospect discovery (Exa Websets + people-research), newcomer surveillance (Exa Websets cron).

When Exa is unavailable, fall back to `references/manual-research.md` (paste-from-UI workflow). When the user has paid Ahrefs, layer it on top per the appendix in `exa-recipes.md` — don't replace.

Cache the raw output to `.seo/keyword-research.json`. Curate the decision-ready summary into the **Keyword Research Appendix** section of `docs/seo-machine.md`.

### Step 4 — Technical foundations audit

Run `scripts/tech_audit.py` (sitemap, robots, meta-tag uniqueness, schema). Whatever it finds becomes **Phase 0** in the roadmap. Day-0 crawl shapes Google's understanding of the site for months — retroactive fixes are harder.

### Step 5 — Generate the roadmap

Fill `assets/roadmap-template.md` with:

- **Site facts** (domain, DR, stack, brand colors, fonts) from steps 1–2
- **Reference data** — paths to controllers / page files this skill will edit
- **Keyword Research Appendix** — curated, grouped by pattern
- **Phase Status Tracker** — auto-populated:
  - Phase 0: technical foundations fixes
  - Phase 1+: one row per page candidate
  - Group by pattern. Within a pattern, order by `traffic_potential` desc → `volume` desc → `KD` asc
  - Striking-distance boosts near the front (fastest wins on existing sites)
  - Off-page checklist (directories + outreach) tail-end, one phase per category

Write to the configured path (default `docs/seo-machine.md`). Print the path back and recommend a human review pass before Phase 0.

### Step 6 — Generate `.seo/link-inventory.md`

Every phase reads this file to pick internal links. Use `assets/link-inventory-template.md`. Pre-populate from existing routes (features, tools, pricing, blog posts). Each phase appends to it as new pages ship.

### Step 7 — Hand off

```
✓ Initialize complete

  Roadmap:        docs/seo-machine.md
  Brand context:  .seo/brand.md
  Keyword cache:  .seo/keyword-research.json
  Link inventory: .seo/link-inventory.md
  Config:         .seo/config.json

Next: review docs/seo-machine.md, then run me again to execute Phase 0.
```

Do not auto-execute Phase 0. Pattern priorities and competitor lists are decisions worth a human pass.

---

## Resume mode

Goal: pick the next phase from the tracker, execute end-to-end with quality gates, hand back so the user can commit/PR.

### Step 1 — Read state

Load `docs/seo-machine.md`, `.seo/brand.md`, `.seo/link-inventory.md`, `.seo/config.json`. Find the **Phase Status Tracker**, identify the next `pending` phase with the lowest number, print it back along with the two phases that follow.

### Step 2 — Confirm scope

Single `AskUserQuestion`:
- "Continue with Phase N: [title]?"
- Options: "Yes, start Phase N" / "Pick a different phase" / "Re-audit (refresh research)" / "Just show the tracker"

"Different" → list pending phases. "Re-audit" → loop back into Initialize steps 3–5. "Show" → print tracker and stop.

### Step 3 — Execute

Pattern → reference mapping:

| Phase type | Reference |
|---|---|
| Phase 0 — technical foundations | `references/technical-audit.md` |
| Pattern A — `/alternatives/[competitor]` | `references/patterns/alternatives.md` |
| Pattern B/C — `/for/[use-case]` or `/for/[audience]` | `references/patterns/use-case.md` |
| Pattern D — `/compare/[a]-vs-[b]` | `references/patterns/compare.md` |
| Pattern E — `/playbooks/[topic]` long-form | `references/patterns/playbooks.md` |
| Striking-distance boost | `references/striking-distance.md` |
| Off-page checklist phase | `references/off-page.md` |
| Internal-link spine audit | `references/quality-bars.md` (link-audit section) |

For page-generating phases, the flow is always:

1. **Re-research** — current competitor pricing, feature changes. Don't trust 60-day-old cached data on commercial-intent terms.
2. **Generate the page payload** — output format follows the stack (`references/stacks/<framework>.md`) or `references/stacks/markdown-fallback.md`.
3. **Verify** against the quality bar (word count, internal links, schema, honesty section on alts). Run `scripts/word_count.py` and `scripts/link_audit.py`. If a check fails, fix it — don't ship under-spec work.
4. **Update `.seo/link-inventory.md`** with the new page.
5. **Update the tracker row** in `docs/seo-machine.md` — status `completed`, PR ref or commit SHA. Same edit batch as the page work so reviewers see both in one diff.

### Step 4 — Hand off (do NOT auto-commit)

```
✓ Phase N complete: [title]

Files changed:
  app/controllers/marketing_controller.rb  (added entry)
  app/frontend/pages/Alternatives/Show.tsx (no change — uses existing layout)
  docs/seo-machine.md                      (tracker updated)
  .seo/link-inventory.md                   (new page registered)

Quality gates:
  ✓ Word count: 712 / 600 min
  ✓ Internal links: 2 alts, 1 feature, 1 tool
  ✓ FAQ JSON-LD attached
  ✓ Honesty section present (3 rows)

Suggested commit: "SEO Phase N: ship /alternatives/[slug]"

Next phase pending: Phase N+1 — [title]
```

Open a PR only if the user has expressed they want that cadence. Otherwise let them drive git.

---

## Interactive principles

| Rule | Why |
|---|---|
| Ask before you guess on positioning calls | The user's gut on which competitor or use-case to ship next often beats the data |
| Show the numbers, not the conclusion | "vol 400, KD 12, TP 1,800" builds more trust than "the data is good" |
| Be honest about what won't work | KD 80 at DR 8 = doomed. Say so, offer the closest winnable alternative |
| One-sentence theory max per phase | The user doesn't need a recap of SEO theory every run |
| Surface tradeoffs, not opinions | "5 thin alternatives or 2 deep ones first?" — state the tradeoff, ask |

---

## Adjacent skills (route here vs there)

| Skill | When | When NOT |
|---|---|---|
| `seo-audit` | One-off diagnostic on an existing site | Forward execution — use this skill |
| `seo-content` | Writing a single rankable article | A whole sprint — use this skill |
| `competitor-alternatives` | One `/alternatives/<x>` page, ad-hoc | Pattern A as part of a sprint — use this skill |
| `keyword-research` | Producing `brand/keyword-plan.md` | This skill consumes that artifact — chain them |
| `ai-seo` | LLM-citation optimization for a few pages | Run after this skill ships ~10 indexed pages |

---

## Anti-patterns

| Don't | Why |
|---|---|
| Target head terms when DR is low | "Social media management tool" at DR 8 is wasted work. KD ≤ DR+10 while DR is low. |
| Ship pages with no inbound internal links | A new page nobody links to is an island. ≥2 inbound links from existing pages, same phase. |
| Ship `/alternatives` pages without an "honesty" section | Three honest tradeoffs (where the competitor wins) is non-negotiable. Brand signal AND Google quality signal. |
| Skip schema markup | FAQPage JSON-LD captures snippets. Article for playbooks. SoftwareApplication for homepage + use-case. Quality gate fails without them. |
| Auto-commit | Always show diff summary; let the user commit (local conventions, hooks, branch naming). |
| Restart Initialize when partial state exists | If `.seo/config.json` exists without the roadmap, prompt before wiping — they may have aborted mid-run. |

---

## File map

| File | Purpose |
|---|---|
| `references/methodology.md` | Why-this-works theory + lessons from real phases |
| `references/exa-recipes.md` | 7 Exa-native research recipes (replaces the old Ahrefs cookbook). Ahrefs appendix at the bottom for paid-precision escalation. |
| `references/api-stack-recipes.md` | Cross-API compound recipes — pain-point mining, OSS competitor teardown, outreach prospect discovery, newcomer surveillance. Uses Exa + Firecrawl + gh + mktg-x + DeepWiki + last30days. |
| `references/manual-research.md` | L0 fallback when no MCP available |
| `references/patterns/alternatives.md` | Pattern A spec, data shape, quality bar, example |
| `references/patterns/use-case.md` | Pattern B+C spec |
| `references/patterns/compare.md` | Pattern D spec |
| `references/patterns/playbooks.md` | Pattern E spec (2,500-word bar) |
| `references/stacks/detection.md` | Stack-detection signal table |
| `references/stacks/rails-inertia.md` | Rails + Inertia adapter (reference implementation) |
| `references/stacks/nextjs.md` | Next.js App Router adapter |
| `references/stacks/astro.md` | Astro content-collection adapter |
| `references/stacks/markdown-fallback.md` | Universal markdown output format |
| `references/technical-audit.md` | Phase 0 recipes (sitemap, robots, meta, schema) |
| `references/striking-distance.md` | GSC pos 5–20 audit + boost recipe |
| `references/off-page.md` | Backlink checklist + Ahrefs referring-domains research |
| `references/quality-bars.md` | Verification spec per pattern |
| `scripts/word_count.py` | Strip markup → word count |
| `scripts/link_audit.py` | Verify internal-link minimums per page |
| `scripts/tech_audit.py` | Sitemap.xml + robots.txt + meta-tag scanner |
| `assets/roadmap-template.md` | `docs/seo-machine.md` skeleton |
| `assets/brand-template.md` | `.seo/brand.md` skeleton |
| `assets/link-inventory-template.md` | `.seo/link-inventory.md` skeleton |

---

## Outputs

The skill writes to **project paths**, not `brand/`. This is why `writes:` in `skills-manifest.json` is `[]` — the manifest declares only `brand/*.md` writes, and seo-machine's outputs live in the user's repo, not in brand memory.

| Output | Mode | Purpose |
|---|---|---|
| `docs/seo-machine.md` | Initialize (write), Resume (update phase row) | Persistent sprint roadmap — Phase Status Tracker + Reference Data + Keyword Research Appendix. Single source of truth across sessions. |
| `.seo/brand.md` | Initialize | Product context derived from repo + user answers (one-liner, persona, competitors, voice tags, anti-positioning). |
| `.seo/link-inventory.md` | Initialize (create), Resume (append per phase) | Every internal-link target the skill can use. Each phase appends new pages. |
| `.seo/keyword-research.json` | Initialize | Cached raw output from Ahrefs / Exa / manual research. Read by every phase, refreshed every 30 days. |
| `.seo/config.json` | Initialize | Stack info, research backend choice, project IDs. Persists machine-readable state. |
| Phase-specific page files | Resume (per phase) | Stack-native page files (e.g. `app/controllers/marketing_controller.rb` + `app/frontend/pages/Alternatives/Show.tsx` for Rails+Inertia; `app/[pattern]/[slug]/page.tsx` for Next.js App Router; etc.). Paths follow `references/stacks/<framework>.md`. |

This follows the **Long-Arc Sprint Persistence Pattern** documented in `AGENTS.md` — `docs/seo-machine.md` is the canonical doc that survives session interruption.

## /cmo integration

`/cmo` routes here under **Playbook #9 — SEO Authority Build, Path B (programmatic sprint)**. On a cold project /cmo first spawns `mktg-brand-researcher`, `mktg-audience-researcher`, `mktg-competitive-scanner` in parallel (foundation), runs `keyword-research` to populate `brand/keyword-plan.md`, then hands off here. After every phase, /cmo spawns `mktg-content-reviewer` + `mktg-seo-analyst` in one message to score the page batch before the user commits.

See `skills/cmo/rules/playbooks.md` and `skills/cmo/rules/sub-agents.md` for the full handoff contract.
