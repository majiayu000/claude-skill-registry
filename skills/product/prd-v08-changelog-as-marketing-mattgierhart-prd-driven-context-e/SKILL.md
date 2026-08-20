---
name: prd-v08-changelog-as-marketing
description: >
  Design the changelog as a distribution surface bridging engineering releases (DEP-/FEA-) to
  marketing channels (GTM-) during PRD v0.8 Deployment & Ops. Triggers on requests to set up a
  changelog system, publish releases, or when user asks "how should we publish releases?",
  "changelog as marketing", "release notes", "Stripe-style changelog", "what to do with our
  release notes", "ship and tell". Outputs MON-CHG-* changelog entries and per-channel formats.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep

execution_modes:
  default: standard
  supports: [quick, standard, deep]
---

# Changelog as Marketing

Position in workflow: v0.8 Release Planning → **v0.8 Changelog as Marketing** → v0.9 Launch Channels (ORB)

## Execution Mode

Default is **standard**. See [`.claude/rules/08-skill-execution-modes.md`](../../rules/08-skill-execution-modes.md) for selection logic.

| Mode | What this skill produces |
|------|--------------------------|
| **quick** | One release format (markdown for site); one channel mapping; minimum-viable changelog page |
| **standard** | Release categorization + 2–3 channel mappings; per-channel format templates; publish cadence; attribution plan |
| **deep** | Full categorization taxonomy; format templates for all relevant channels (email, blog, Twitter, LinkedIn, RSS, Slack); cadence + voice guide; KPI- attribution per channel |

## What This Does

Treats the changelog as a **distribution surface**, not an engineering record. Each shipped release becomes a content artifact that lands across Owned and Rented channels with minimal extra effort. This is the bridge between v0.8 (what shipped) and v0.9 (where it gets told).

Done well, this is one of the highest-leverage Owned-channel investments — Stripe, Linear, Vercel, and Sentry have shown that an opinionated changelog drives ongoing inbound that compounds over years. Done badly, it's a dumping ground for "fixed bug X" that nobody reads.

## How It Works

1. **Define the changelog audience(s)** — Engineering changelogs (for users running self-hosted or integrating an API), customer-facing changelogs (for end-users), and internal changelogs (for the team) have different shapes. Anchor to the Positioning best-fit segment.
2. **Categorize release content** — Each shipped item gets a category:
   - **New feature** (publish loudly)
   - **Improvement** (publish, briefly)
   - **Breaking change** (publish, prominently, with migration path)
   - **Deprecation** (publish, with timeline)
   - **Fix** (publish only if user-visible)
   - **Internal** (don't publish externally)
3. **Map categories to channels** — Each category gets a channel destination from the ORB mix:
   - New feature → Blog post + email + Twitter + LinkedIn
   - Breaking change → Email (high-priority) + RSS + blog
   - Improvement → Blog (digest) + Twitter (digest)
   - Fix → Changelog page only
4. **Build per-channel format templates** — Each channel has a length/tone constraint:
   - Email: subject line + 2-paragraph body + CTA
   - Blog: full writeup, screenshots, code samples
   - Twitter/X: 280 chars, one image
   - LinkedIn: 1,000-1,500 chars, professional voice
   - Slack/Discord: short with link to blog
   - RSS: full content for engineering audiences
5. **Set publish cadence** — Per-release (every shipped release publishes immediately) vs. digest (weekly/monthly roll-up). Most teams need both: per-release for big things, digest for the rest.
6. **Plan attribution** — Every channel-published release gets a UTM. Track changelog → signup conversion to identify which categories convert.

## Example

A developer-tools product ships:

| Item | Category | Channels |
|------|----------|----------|
| New `/api/v2/webhooks` endpoint | New feature | Blog (full), email, Twitter, LinkedIn, RSS |
| `/api/v1/webhooks` deprecation (sunset in 6mo) | Deprecation | Email (high-priority), blog, RSS |
| 30% faster response time on heavy queries | Improvement | Twitter, weekly digest |
| Fixed: webhook signing edge case | Fix | Changelog page only |
| Internal: refactored auth middleware | Internal | (none) |

Tuesday publish:
- Blog post: "Webhooks v2 is live — here's what changed and how to migrate"
- Email to API customers (segment-targeted, not full list): "Action needed: webhook v1 sunset"
- Twitter: "Webhooks v2 ships today. v1 is sunset in 6 months. Migration guide: [link]"
- Changelog page: all five items (including the fix and internal note marked appropriately)

## What You Get Back

- **MON-CHG-\* changelog entries** (one per shipped release) — Master record with category, audience, channel mapping, links to per-channel publications
- **GTM-CHG-\* per-channel formats** (one per channel) — Templates and example content
- **Publish cadence schedule** — Per-release vs. digest decisions
- **KPI attribution plan** — UTMs and conversion tracking

## When to Use It

| Trigger | Mode |
|---------|------|
| First release post-launch (no changelog system yet) | quick |
| Standard launch cadence stabilizing | standard |
| Pre-investor / pre-Series A — changelog as proof of velocity | deep |
| API or developer-tool product | deep (changelog is a primary surface) |
| One-time announcements (acquisition, big feature) | standard |

## Consumes

- **DEP-\* release entries** (from v0.8 Release Planning) — What's being released, when
- **FEA-\* features** (from v0.3) — What new features exist; categorization input
- **GTM-\* channel mix** (from v0.9 Launch Channels ORB, when available) — Where to publish
- **GTM-\* positioning** (from v0.9 Positioning, when available) — Voice and tone constraints
- **PER-\* best-fit characteristics** — Audience tone calibration
- **KPI-\* baselines** — Attribution targets

> When this skill runs before v0.9 has executed, channel mapping uses placeholder channels and is reconciled when v0.9 channels are finalized.

## Produces

- **MON-CHG-\* entries** in `SoT/SoT.DEPLOYMENT.md` (or a dedicated `SoT/SoT.CHANGELOG.md` if release volume warrants)
- **GTM-CHG-\* entries** with `Type=Channel-Changelog` (per-channel format templates)
- **CFD-\* gaps surfaced** — If a release category lacks an obvious channel mapping, log as research gap

## Output Template

```
MON-CHG-XXX: Release — [Release name / version]
Type: Changelog
Date: YYYY-MM-DD
Owner: [Person / role]
Status: [Drafted | Reviewed | Published]

Released items:
  - [Item 1] — Category: [New feature | Improvement | Breaking change | Deprecation | Fix | Internal]
  - [Item 2] — Category: ...

Audience: [API customers | All users | Internal team | Mixed]

Channel publications:
  - Blog: [URL or "scheduled YYYY-MM-DD"]
  - Email: [Segment + scheduled date]
  - Twitter: [Scheduled date]
  - LinkedIn: [Scheduled date]
  - Changelog page: [Updated YYYY-MM-DD]

Attribution: utm_campaign=changelog-<version>

Linked IDs: DEP-AAA (release), FEA-BBB (features shipped), GTM-CHG-CCC (channel formats), KPI-DDD (attribution)
```

```
GTM-CHG-XXX: Channel Format — [Channel name]
Type: Channel-Changelog
Channel: [Blog | Email | Twitter | LinkedIn | RSS | Slack]
Owner: [Person / role]

Format constraints:
  Length: [chars / words / sections]
  Tone: [Conversational | Technical | Formal — anchored in Positioning voice]
  Visuals: [Required / optional]
  CTA: [Specific action expected]

Template:
  [Reusable template for this channel, with variable placeholders]

Example (most recent use):
  [Concrete example from MON-CHG-XXX]

Publish trigger: [Per-release | Weekly digest | Monthly digest]

Linked IDs: MON-CHG-AAA (latest use), GTM-YYY (positioning voice)
```

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| **Dumping internal commits** | Changelog reads like `git log` | Categorize; publish only what users care about |
| **Same content everywhere** | Same blog post copy-pasted to Twitter and LinkedIn | Each channel has its own format constraints; honor them |
| **Vague feature claims** | "Various improvements" | Name the specific change; "30% faster heavy queries" beats "performance improvements" |
| **Engineering-only voice** | Customer changelog uses internal jargon | Tone-shift per audience; engineer changelog ≠ end-user changelog |
| **No attribution** | Changelog publishes but no idea what converts | UTM every link; track per-channel conversion |
| **Sporadic cadence** | Publish heavily for 2 months, then quiet for 6 | Pick per-release or digest cadence; commit to it |
| **Breaking change buried** | Hidden in a sea of small items | Breaking changes get a dedicated, prominent slot |

## Quality Gates

Before publishing the first release:

- [ ] Audience(s) defined (engineering, customer-facing, internal — separately if needed)
- [ ] Categorization scheme exists (at minimum: new / improvement / breaking / fix)
- [ ] Channel mapping table exists (categories → channels)
- [ ] Per-channel format templates exist
- [ ] Publish cadence committed
- [ ] Attribution plan (UTM convention) defined
- [ ] Voice/tone honors GTM- positioning (if v0.9 is done)

## Downstream Connections

| Consumer | What it uses | Example |
|----------|--------------|---------|
| **Launch Channels (ORB)** | Changelog is an Owned channel; rolls into mix matrix | Blog-changelog = Owned-content |
| **Launch Metrics** | Per-channel changelog conversion targets | KPI-changelog-blog-signups |
| **Feedback Loop Setup** | Changelog reader comments become CFD- | Blog comment threads → CFD- pattern |
| **AEO Audit** | High-traffic changelog posts become AI citation sources | Changelog entries cited by AI search |
| **v1.0 Case Study Builder** | Shipped features in changelog feed case study material | "How we use [feature] at [customer]" |

## Detailed References

- Stripe changelog: [stripe.com/changelog](https://stripe.com/changelog) — the canonical example
- Linear changelog: [linear.app/changelog](https://linear.app/changelog) — opinionated voice
- Vercel changelog: [vercel.com/changelog](https://vercel.com/changelog) — visual-heavy
- jonathimer's `changelog-updates` skill (devmarketing-skills)
- (No bundled `references/` — read the source examples for current best practice)
