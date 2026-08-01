---
name: kai-client-dashboard
description: Build a white-labeled, client-facing intelligence dashboard — a live, branded reporting surface an agency stands up per client instead of sending static reports. Covers brand auto-extraction from the client's URL, a three-tier build (Basic/Standard/Advanced), an onboarding feature wizard, a 10-page inventory, public-access tradeoffs, and the retention plays that make the dashboard sticky. Use when "client dashboard", "client intelligence dashboard", "white label dashboard", "client portal", "branded dashboard for my client", "agency dashboard", "build my client a dashboard", "give the client a live view instead of a report", or any request to stand up a durable, client-facing reporting surface.
---

# kai-client-dashboard — Client Intelligence Dashboard

> **Kai root note:** `knowledge/`, `harness/`, and `scripts/` paths in this skill live in the Kai install, not the user's project. Resolve them against the first ancestor directory of this SKILL.md that contains a `knowledge/` folder (the Kai plugin root, `~/.claude/kai`, or the kai-cmo-harness repo). `MARKETING.md`, `memory/`, and any output files live in the current project. If a referenced `scripts/` command is not available in this install, say so, skip it, and continue with the file-based guidance — never fabricate its output.

A report is a snapshot the client forgets by Friday. A dashboard is a URL they bookmark. This skill builds the client-facing product: a co-branded, always-on reporting surface for one of *your* clients — separate from `/kai-data-dashboard`, which turns data you've already sourced into a spec or static handoff, and separate from `scripts/build_dashboard.py`, which builds the *operator's own* internal ops dashboard (goals, tasks, integrations — see `workspace/dashboard.html`). Use this skill when the deliverable is a durable product for someone outside your own team: onboarding wizard, brand shell, page set, data wiring, a public-access decision, and the retention program that keeps them opening it.

One client = one dashboard = one deployment. Never fold a second client into an existing client's project — a shared default (a hardcoded client ID, a fallback credential) that leaks from client A's build into client B's is the single most common failure mode in this workflow (see "Common Pitfalls").

## Non-Negotiable: Provenance And Access Before Build

Before wiring a single page:

1. Load `harness/references/audit-data-provenance.md` and declare a data mode for every metric the dashboard will show. A live client dashboard reading connected accounts is `onboarding_connected` by definition — the client has granted access. Use `internal_demo` only for an unmistakably-labeled sample shell shown before data is connected, never as a silent filler.
2. Load `knowledge/checklists/privacy-sanitizer-checklist.md` before deciding what is public. This skill defaults to a public, no-login URL for ease of access — see "Public Access" below for what that does and does not mean for PII.
3. Never fabricate a metric, review count, ranking, health score, or dollar figure to fill an empty panel. A missing source is a `data-gaps.md` entry and an empty state in the UI — not a placeholder number.

Run before handoff:

```bash
python scripts/quality_gates/audit_provenance_lint.py <dashboard-source-folder> --audit-dir
```

## Three Tiers

| Tier | Use when | Data sources | Build |
|---|---|---|---|
| **Basic** | Client only has GA4 + GSC, no CRM/ads stack yet | Google Analytics 4, Google Search Console | 3 pages: Overview, Website Traffic, Search Performance |
| **Standard** | Client runs a real marketing stack | GA4, GSC, CRM/lifecycle tool, ad platforms, reviews | Full 10-page set below, branded shell, scheduled sync |
| **Advanced** | High-value client where sales throughput or reputation is the growth lever | Standard + CRM deal data and lead scoring, or competitor review/AI-mention tracking | One additional module — Sales Intelligence or Reputation Intelligence, not both by default |

Default to Standard. Drop to Basic when Phase 1's credential list comes back mostly empty. Only add an Advanced module when both the agency and the client want the deeper build and the extra data-sensitivity surface that comes with it (deal values, individual rep performance, scored leads).

## Phase 0: Auto-Brand From The URL

If the opening request already names the client and a URL ("set up a dashboard for Acme at acme.com"), don't re-ask for it. Immediately:

1. Fetch the site (WebFetch, or the pre-installed Chromium/Playwright for JS-rendered sites) and pull: primary logo, dominant colors with hex codes, heading/body font stack, business name, tagline, and industry signals from copy or schema.
2. Apply those as the shell's theme: client logo top-left, extracted accent color on the primary UI elements, extracted fonts where feasible.
3. Pre-populate the Brand Assets page (see Phase 2) with what was extracted — mark anything guessed (e.g. a font stack inferred from a generic system-font fallback) as unconfirmed rather than presenting it as the client's real brand guide.
4. Stand up the shell — see "Build: Choose Your Path" below — and report back what was extracted before asking anything else: business name, primary color, logo source, fonts. Then move to Phase 1.

## Phase 1: Core Setup (Always Required)

Ask what Phase 0 didn't already answer:

1. Business name as it should appear on the dashboard.
2. Website URL.
3. Industry / business type (drives which review platforms and which page in "Customization By Industry" apply).
4. Logo — confirm the extracted one or get a better source; placeholder until replaced otherwise.
5. Which analytics are connected: GA4 property ID, GSC site URL exactly as registered (`https://www.example.com/` or `sc-domain:example.com`), Google Business Profile name.
6. Which CRM/lifecycle tool the client runs (GoHighLevel, HubSpot, or other) and whether the agency already has API/private-app access.
7. 5–15 target keywords to track for Google rankings and AI/LLM visibility.
8. Any competitors to benchmark against (names + URLs) — optional here, confirmed again in Phase 2.

Confirm before moving on: "I have what I need for the core build. Now a few yes/no questions on optional pages — say no to skip any of them; I won't build an empty page for something you didn't ask for."

## Phase 2: Feature Wizard (Optional — Yes/No)

Ask each feature below. On "yes," collect exactly what's listed. On "no," skip the page entirely — an empty or placeholder page for a feature the client declined is worse than not having the page.

| Feature | If yes, collect | Source in this harness |
|---|---|---|
| **Retargeting / paid remarketing** | Which platform(s) | Google/Meta already have connectors (`kai/connectors/ads/google_ads.py`, `meta_ads.py`); other platforms need a CSV export or a new connector — flag as a data gap until then |
| **Visitor identification / lead scoring** | Tool name + API key (e.g. a visitor-deanonymization tool), and whether they want basic company ID or full Hot/Warm/Cool/Cold scoring | No bundled connector — treat as a data gap until wired; never invent a score without a stated formula |
| **Competitor benchmarks** | 3–6 competitor names + URLs | Route through `/kai-competitors` and `/kai-brand-pulse` — both already produce cited, source-backed competitive data; don't hand-scrape review counts outside that provenance discipline |
| **Brand Assets page** | Existing brand files, or permission to generate from the site scrape | Phase 0 output, refined |
| **Press releases & brand visibility** | Distribution URLs (EIN Presswire, PR Newswire, etc.) as they're published | Manual entry — no credential needed |
| **Video library** | Nothing upfront — an "Add Video" flow for embed codes | Manual entry |
| **AI/LLM rankings** | Nothing beyond Phase 1's keywords | Feed it from `/kai-surround-sound`'s AI-search-visibility output — don't hand-roll a separate LLM-query mechanism |
| **Social media performance** | Platform page URLs + available API access or manual exports | `/kai-social` content log where available |
| **Email/CRM automation visibility** | Nothing beyond the Phase 1 CRM credentials | Same CRM connection |
| **Deliverables page** | A list of active services (or build it from what the agency already has on file) | Manual, see below |
| **What's Next roadmap** | 3–6 services to frame as growth opportunities | Manual, source-backed reasoning only (no invented benchmark numbers) |
| **Multi-brand / multi-location** | Each brand/location name + URL | Tabbed or sectioned view |
| **Agent Registry page** | Nothing beyond what's already running for this client | See below — populate from real scheduled work, not aspirational copy |

## Phase 3: Open Additions

After Phase 2: "Anything else — a custom page, a data source I haven't mentioned, something specific to this client's business? Describe it and I'll tell you if it's buildable and what access it needs." Confirm scope, sidebar placement, and required credentials before adding it to the plan.

## Phase 4: Build Confirmation

Before writing anything, summarize: every page that will ship, every credential collected, anything still outstanding (logo, brand assets, competitor list), and the public-access decision (see below). Get an explicit go-ahead before building.

## Build: Choose Your Path

Kai does not ship a prebuilt multi-tenant client-dashboard codebase to copy from — there is no reference client repo bundled here. Two honest paths:

**Fast path (works today, no new project).** Use `scripts/build_dashboard.py` and `scripts/templates/dashboard_template.html` as the starting shell, restyled to the white-background, co-branded look this skill requires (the shipped template is dark-themed for internal ops use — treat it as a structural starting point, not the final look). Feed it from a data contract produced by `/kai-data-dashboard` once sources are connected. This gets a client a real, live-enough surface fast, and it's the right ceiling for the Basic tier.

**Full-app path (Standard/Advanced, ongoing agency use).** Stand up your own project in whatever stack you already use for client work. Your first build becomes the reference implementation for build #2 and #3 — copy your own prior client's shell, then find-and-replace client-specific values (name, domain, IDs, credential references). Wire credentials the way the rest of this harness does: one client = one config record + one credential set, resolved through `kai/runtime/connections.py` / `kai/runtime/integrations.py` (Pipedream-backed) or your own equivalent, never a hardcoded per-client constant with a default that silently applies to the next client's build. If a Vercel connector is available in your environment, use it to deploy; otherwise hand off standard deployment steps for your own hosting.

Either path: trigger a manual sync, verify every page loads or shows a labeled empty state, and confirm the public-access decision before sharing the URL.

## Page Inventory (Standard Tier, 10 Pages)

| Route | Page | Data source in this harness |
|---|---|---|
| `/` | Dashboard Overview | All connected sources below, rolled up |
| `/visitor-id` | Smart Visitor ID *(optional)* | Visitor-identification tool, if wired |
| `/rankings` | Google Rankings | GSC + `scripts/intel/serp_tracker.py` |
| `/llm-rankings` | AI / LLM Rankings | `/kai-surround-sound` output |
| `/traffic` | Website Traffic | GA4 (`kai/connectors/analytics/ga4.py`) |
| `/adroll` | Retargeting *(optional)* | `kai/connectors/ads/google_ads.py`, `meta_ads.py`, or CSV |
| `/content` | Content & Social | CRM/ESP + `/kai-social` content log |
| `/reviews` | Reviews | `/kai-brand-pulse` (cited review/mention aggregation) |
| `/leads` | Leads | CRM form/contact data |
| `/communications` | Communications | CRM contact/message data |

Every page needs: a plain-language paragraph explaining what the data means, an Agency Recommendations block (3–4 insights in the agency's voice — specific to this client, never generic filler), and a visible "last synced" timestamp. Show a loading state, never a blank screen, while data is fetching.

### Deliverables Page

A visual checklist of every service the agency is actively delivering — green/active, yellow/in-progress, grey/available-but-not-purchased. This is the single most valuable retention page in the set: it answers "what am I paying for" before the client has to ask, and a grey card is a natural upsell without a sales call. Populate it from what the agency has on file for this client — never mark a service active that isn't running.

### Agent Registry Page

A table of every automated Kai workflow running for this client: name, purpose, trigger, how to start it manually, last run, status. This is genuinely concrete in this harness — populate it from what's scheduled: `workspace/HEARTBEAT.md` heartbeats, `agent/tasks/` scheduled tasks (e.g. the weekly `cmo_review`), or, if this session is running on Claude Code Remote, real Routines (`list_triggers`/`create_trigger`). Don't invent a schedule or a "last run" timestamp — an agent that hasn't run yet shows "not yet run," not a fabricated date.

## Public Access — What "No Login" Actually Means

The default posture for a client dashboard is a bookmarkable public URL, because a client who has to remember a password stops checking. That default is fine for aggregate marketing metrics: traffic trends, ranking positions, aggregate review scores, campaign-level spend and ROAS. It is **not** automatically fine for anything with a name, phone number, email address, or dollar figure attached to an individual person — the Leads and Communications pages above are the obvious risk, and Sales Intelligence (Advanced tier) is worse.

Before flipping a client dashboard public, run the Publication Gate in `knowledge/checklists/privacy-sanitizer-checklist.md` and pick one:

- **Split access.** Aggregate pages stay public; Leads/Communications/deal data sit behind whatever lightweight auth your stack supports.
- **Obscured + gated.** Unguessable slug, `noindex` so it never gets crawled or indexed, plus a shared passcode — acceptable only when the client has explicitly signed off on that level of exposure for that data.

Whichever pattern you pick, whatever stack you build in, check specifically for a global "redirect to login on any 401" handler — it's the most common way a page that was supposed to be public silently isn't, and the most common way a page that was supposed to be gated silently isn't either. Confirm both directions before sharing the URL.

## Retention & Upsell Plays

The dashboard is a retention asset, not just a reporting one. Build the two marked Core into every Standard+ dashboard; add the rest as the relationship deepens. None of these are automatic wins — track whether they change engagement for this client instead of assuming the pattern.

| Play | Status | What it does |
|---|---|---|
| Brand Guide (logos, colors, fonts, usage rules) | Core | The client's team returns to this asset every time they need a logo file |
| Deliverables page | Core | See above |
| Competitor Watchlist | Recommended | Clients revisit this page more than any other; every gap is a natural upsell conversation |
| What's Next roadmap | Recommended | Shows unpurchased services as opportunities, source-backed, not a sales pitch |
| Marketing Health Grade / ROI summary | Optional, provenance-gated | Only ship a letter grade or a dollar figure if you can name the formula and the source for every input — an invented "B+" or an invented "$40K in pipeline value" is precisely what `audit-data-provenance.md` exists to block |
| Review Response Center, Lead Alert Feed | Optional | Daily-use stickiness — pulls the client back weekly instead of monthly |
| "Powered By [Agency]" co-branding | Core | Client logo top-left, agency mark top-right, smaller — every time the client shows this to their own team it's a quiet referral |

## Weekly Engagement Automation (Compliance-Gated)

A dashboard only retains a client if they open it. A rotating weekly touchpoint — email, then SMS, then a call-to-action reminder, on repeat — keeps it top of mind. Build this in whatever lifecycle tool the client's CRM connects to (`kai/connectors/lifecycle/`).

Before enrolling a single contact in SMS or any prerecorded/ringless-voicemail channel: load `harness/skills/kai-sdr-operator/references/compliance-matrix.md` and confirm consent and an opt-out path for that channel. TCPA-type consent rules apply to prerecorded and autodialed voice and SMS in the US, and equivalent rules apply elsewhere — a client's own customer or lead did not necessarily consent to receive the *agency's* dashboard-engagement messages just because they're in the client's CRM. Email-only cadences don't carry this risk; SMS and voicemail drops do.

Track whether the cadence increases dashboard opens and strategy-call attendance for this client — treat that as a hypothesis to prove with this client's own numbers, not an assumed result.

## Where To Find Common Credentials

| Credential | Where to find it |
|---|---|
| GA4 Property ID | Google Analytics → Admin → Property Settings → Property ID (a number) |
| GSC Site URL | Search Console → property selector, exactly as registered |
| Google Service Account JSON | Google Cloud Console → IAM & Admin → Service Accounts → Keys → Add Key → JSON |
| GoHighLevel Location ID / API Key | GHL → Settings → Business Info (Location ID); Settings → Integrations → API Key |
| HubSpot Private App Token | HubSpot → Settings → Integrations → Private Apps → create app with CRM read scopes |
| Google Business Profile | Business Profile Manager, matched by business name for review pulls |

If a credential isn't in this table, it isn't a connector this harness ships today — collect it anyway if the client has it, but log the integration as a data gap until it's wired, and never fake its output in the meantime.

## Customization By Industry

| Industry | Review platforms | Distinctive page worth adding |
|---|---|---|
| Home Services | Google, Yelp, Houzz, Angi | Project gallery / before-after |
| Healthcare / Insurance | Google, Healthgrades | Compliance-safe lead pipeline (check `harness/references/advertising-compliance.md` before any health claim ships) |
| Hospitality | Google, TripAdvisor, Yelp | Visitor origin map + sentiment by area |
| E-commerce / Retail | Google, Yelp, Facebook | Product performance + cart abandonment |
| Professional Services | Google, LinkedIn | Proposal pipeline + retention view |
| Financial Services | Google, BBB | Deal tracker + sales leaderboard (Advanced tier only, and only with the client's sign-off on showing individual rep numbers) |

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| A hardcoded default client ID or credential from build #1 silently applies to build #2 | Treat client identity as a real config key from the start, never a code constant with a fallback |
| Public dashboard shows a login screen anyway | Look for a global "redirect on 401" handler gating an endpoint that was supposed to be public |
| PII-bearing page (Leads, Communications, deal data) left fully public | Run the Publication Gate before every public flip, not just at initial launch |
| Empty panel filled with an invented number instead of an empty state | Empty source = `data-gaps.md` entry + visible empty state, never a guess |
| Missing credential silently serves stale cache with no warning | Surface "last synced" prominently and flag when a sync has failed, not just when it succeeds |
| SMS/voicemail automation enrolls a contact who never consented to hear from the agency | Confirm consent and opt-out per `compliance-matrix.md` before enrollment, same as any cold outreach |
| Fabricated Health Grade or ROI number to make the Overview page look finished | No formula, no source per input → no panel; log the gap instead |
| Agent Registry lists automation that isn't actually scheduled | Populate only from real heartbeats/tasks/Routines, mark unscheduled items "not yet run" |

## Quality Gates

Before handoff:

1. Every metric has a source and a sync/retrieval timestamp, or is explicitly `internal_demo`-labeled.
2. No score or dollar figure (Health Grade, ROI/Value Delivered) ships without a stated formula and a source per input.
3. The public-access decision is explicit and covers every page, not just the Overview.
4. Deliverables and Agent Registry reflect real, current work — nothing aspirational.
5. Any SMS/voicemail engagement automation has a logged consent and opt-out path.
6. `python scripts/quality_gates/audit_provenance_lint.py <folder> --audit-dir` passes.

## Output Summary

Final response should include:

- Dashboard URL (or, if only the spec/shell was built, the folder path and what's left to wire).
- Tier (Basic/Standard/Advanced) and which optional features from Phase 2 shipped vs. were skipped.
- Every credential still outstanding, listed as a data gap.
- The public-access decision made and why.
- Whether the Deliverables and Agent Registry pages reflect real current state.
