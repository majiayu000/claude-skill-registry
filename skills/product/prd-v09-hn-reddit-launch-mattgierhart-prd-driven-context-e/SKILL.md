---
name: prd-v09-hn-reddit-launch
description: >
  Build a Hacker News + Reddit launch playbook for developer-tools and community-led products
  during PRD v0.9 Go-to-Market. Triggers on requests to plan HN/Reddit launch, "Show HN" post,
  community launch, or when user asks "HN launch", "Show HN", "Reddit launch", "launch on
  /r/SaaS", "Product Hunt vs HN", "community launch", "developer launch". Outputs GTM-* with
  Type=Channel-HN / Type=Channel-Reddit entries with timing, title, story angle, and
  engagement plan.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebSearch
  - WebFetch

execution_modes:
  default: standard
  supports: [quick, standard, deep]
---

# HN + Reddit Launch Playbook

Position in workflow: v0.9 Launch Channels (ORB) → **v0.9 HN + Reddit Launch** → v0.9 Launch Metrics

## Execution Mode

Default is **standard**. See [`.claude/rules/08-skill-execution-modes.md`](../../rules/08-skill-execution-modes.md) for selection logic.

| Mode | What this skill produces |
|------|--------------------------|
| **quick** | Single Show HN post draft; title; first 4-hour engagement plan |
| **standard** | HN post + 2 Reddit cross-posts; story angle decision; comment-engagement rules; non-launch follow-up wave |
| **deep** | HN + 3–5 Reddit subreddits + Lobsters + Indie Hackers; pre-launch warm-up posts; subreddit-specific tone variants; AMA scheduling |

## What This Does

Produces a launch playbook for Hacker News and Reddit — two channels where developer-tool, technical, and community-friendly products win launches if executed well and lose them silently if executed badly. Both platforms reward authenticity, technical depth, and founder presence; both punish marketing-speak, top-of-funnel sales tactics, and absent founders.

This is a **channel-execution** skill. It assumes the ORB channel mix already includes HN/Reddit; it doesn't second-guess that choice. If positioning best-fit doesn't live on these platforms, this skill should not run.

## How It Works

1. **Decide if HN/Reddit fits** — Re-check positioning best-fit characteristics. HN/Reddit work for: developer tools, technical products, B2B with developer/PM buyer, indie/bootstrapped story, open-source. HN/Reddit are wrong for: enterprise procurement, regulated B2B with non-technical buyer, consumer products targeting non-technical users.
2. **Pick the story angle** — One of:
   - **Show HN** (product) — "Show HN: [Product] — [one-line description]" — works when product itself is interesting
   - **Ask HN** (problem) — "Ask HN: How do you handle [pain]?" — works when category needs education before product
   - **Story** — "I built X because Y" or "Why we [unusual decision]" — works when founder narrative is the hook
   - **Open source** — "[Project] is now open source" — works when there's something to release
   - **Technical writeup** — "How we built X" — works for HN; less for Reddit
3. **Craft the title** — Platform-specific:
   - **HN**: Factual, no marketing words, no emoji. Example: "Show HN: An open-source alternative to X". HN guidelines reject hype.
   - **Reddit**: Subreddit-specific. Each subreddit has tone norms. Read the subreddit's pinned rules and recent top posts.
4. **Plan timing**:
   - **HN**: Post Tue–Thu, 8–10am PT. Avoid Mondays and weekends. The first hour matters most — upvote velocity determines front-page placement.
   - **Reddit**: Subreddit-specific peak time. Read subreddit traffic patterns. Some subreddits ban "self-promotion" posts on certain days.
5. **Founder presence (first 24h)** — Founder responds to every substantive comment in the first 4 hours. No "thanks!" replies; engage with the argument. This is the difference between a 50-comment thread and a 500-comment thread.
6. **Non-launch follow-up** [standard+] — 30–60 days post-launch, return to HN/Reddit with:
   - Technical writeup of how you built it
   - "What I learned launching on HN" retrospective (if appropriate)
   - Case study or growth update
   - AMA if launch generated real interest

## Example

Developer tool launching. Best-fit = solo developers + small dev teams. ORB matrix has HN as the primary Borrowed channel.

**Story angle**: "Show HN" — product is self-evident; demo is the hook.

**Title**: `Show HN: [Product] – Type-safe contracts between your frontend and backend`

**Timing**: Tuesday 9:00 AM PT. Founder cleared calendar for the next 4 hours.

**Post body** (HN expects substance):

> Hi HN — I built this because I spent 2 years debugging "frontend says string, backend says number" issues at my last job.
> 
> [Product] generates type-safe API clients from your OpenAPI spec. It works with TypeScript, Python, Go, and Rust.
> 
> Tech stack: [...]
> 
> Some things that worked and didn't: [...]
> 
> Free for individuals; paid for teams. Source is on GitHub: [link].
> 
> Happy to answer questions.

**First 4 hours**: Founder watches `Show HN` ranking. Responds substantively to every technical question. Doesn't engage with off-topic critique. Posts updates if relevant.

**Reddit cross-post**: 24 hours later, post to `/r/programming` (technical), `/r/typescript` (community), `/r/SaaS` (founder story). Each with a subreddit-tuned title and intro.

**Follow-up wave** (Day 30): "Building [Product]: 30 days after launch" — retrospective post.

## What You Get Back

- **GTM-\* with Type=Channel-HN** (one entry) — Title, body, timing, founder-engagement plan
- **GTM-\* with Type=Channel-Reddit** (one per subreddit) — Subreddit-tuned title, body, posting time
- **GTM-\* engagement rules** — Comment-response policy, when to escalate to founder
- **GTM-\* follow-up wave** — 30/60-day post-launch content plan

## When to Use It

| Trigger | Mode |
|---------|------|
| Developer-tool launch | standard |
| Open-source release | standard |
| Indie / bootstrapped product launch (story angle) | standard |
| B2B SaaS with technical buyer | quick (just HN; skip Reddit) |
| Big technical decision worth a writeup ("how we migrated to X") | quick (one HN post, no Reddit) |
| Enterprise / non-technical buyer | **do not use** |
| Regulated category (medical, financial) | **do not use** without legal review |

## Consumes

- **GTM-\* positioning** + **PER-\* best-fit characteristics** — Anchors the story angle and confirms HN/Reddit is even appropriate
- **GTM-\* launch channels** (from v0.9 Launch Channels ORB) — HN/Reddit must already be in the mix matrix
- **GTM-\* offer card** — Determines the post's CTA (free tier, beta, open source, paid trial)
- **CFD-\* customer stories** — Anchors social proof in comments and follow-up
- **BR-POS-\* constraints** — Tone guardrails (no enterprise speak in /r/SaaS, etc.)

## Produces

- **GTM-\* with Type=Channel-HN** (one entry)
- **GTM-\* with Type=Channel-Reddit** (one per subreddit)
- **GTM-\* engagement-rules** entry — Comment policy, who escalates what
- **GTM-\* follow-up-wave** entry — Post-launch content plan (30/60 day)

## Output Template

```
GTM-XXX: Channel — Hacker News Launch
Type: Channel-HN
Layer: Borrowed
Owner: Founder (must be founder, not marketing)
Status: [Planned | Active]

Story angle: [Show HN | Ask HN | Story | Open source | Technical writeup]
Title: "[Exact title — no marketing words]"
Timing: [Day + hour, with rationale]

Post body:
  [Full body — what HN expects: substance, tech detail, honest tradeoffs]

CTA: [Free tier link | GitHub link | Beta signup link]

Founder presence:
  - Watch ranking for first 4 hours (block calendar)
  - Respond to every substantive comment
  - Update post if relevant
  - No "thanks!" replies — engage with the argument

Failure modes to avoid:
  - Marketing language in title
  - Absent founder
  - "Buy now" CTA (HN punishes)
  - Astroturf upvotes (HN detects, instantly bans)

Linked IDs: GTM-YYY (positioning), GTM-ZZZ (offer), PER-AAA (best-fit), KPI-BBB (HN→signup target)
```

```
GTM-XXX: Channel — Reddit /r/<subreddit>
Type: Channel-Reddit
Layer: Borrowed
Owner: Founder
Subreddit: /r/<name>
Status: [Planned | Active]

Subreddit norms:
  - Tone: [Pinned-rules summary]
  - Self-promotion rule: [Subreddit's specific rule]
  - Peak posting time: [Day + hour]
  - Banned formats: [e.g., no link posts, no images-only]

Title: "[Subreddit-tuned title]"
Body: [Tuned to subreddit tone]
CTA: [Whatever the subreddit allows]

Founder presence: Same as HN — engage substantively for first 4 hours

Linked IDs: GTM-YYY (positioning), PER-AAA (best-fit)
```

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| **Marketing title** | "Revolutionary AI-powered X" on HN | Rewrite as factual; HN strips marketing |
| **Absent founder** | Post goes up; founder is in a meeting | If you can't be present 4 hours, postpone the launch |
| **"Thanks!" replies** | Comment thread is full of "Thanks for the kind words!" | Engage with the argument or don't reply |
| **Astroturfing upvotes** | Asking team/friends to upvote | HN and Reddit detect coordinated voting; instant ban |
| **Cross-posting too fast** | Same post to 5 subreddits in 10 minutes | Stagger by 24+ hours; each post is rewritten for the subreddit |
| **Ignoring subreddit rules** | Banned within an hour of posting | Read the pinned rules; some subreddits ban self-promotion entirely |
| **No follow-up wave** | Launch spikes traffic, then silence | Plan 30/60-day return posts before launch day |
| **Wrong product / wrong channel** | Enterprise procurement product on /r/programming | Re-check positioning; HN/Reddit doesn't fit every product |

## Quality Gates

Before launch day:

- [ ] Best-fit segment confirmed to use HN/Reddit (not assumption)
- [ ] Story angle chosen and matches the product's actual hook
- [ ] Title drafted; passes "no marketing words" check (HN)
- [ ] Founder calendar cleared for first 4 hours
- [ ] Post body has substance (technical detail, honest tradeoffs)
- [ ] CTA matches platform norms (free / GitHub / beta — not "buy now")
- [ ] Subreddit rules read for every targeted subreddit
- [ ] Follow-up wave (30/60 day) drafted in outline
- [ ] No astroturfing plan exists or has been considered

## Downstream Connections

| Consumer | What it uses | Example |
|----------|--------------|---------|
| **Launch Channels (ORB)** | Each HN/Reddit post is a Borrowed-channel entry | Rolls into channel-mix matrix |
| **Launch Metrics** | Per-post attribution → KPI-HN-signups, KPI-Reddit-signups | UTM-tagged links per post |
| **Feedback Loop Setup** | Comments become CFD- feedback entries | Top-voted comment thread → CFD- pattern |
| **v0.9 Case Study Builder (v1.0)** | High-engagement HN/Reddit launches → case study | "How we got 800 upvotes on Show HN" |
| **v0.9 AEO Audit** | HN/Reddit threads become AI-citation sources | Hi-rank threads → AEO inclusion |

## Detailed References

- jonathimer's `hacker-news-strategy` and `reddit-engagement` skills (devmarketing-skills)
- HN guidelines: news.ycombinator.com/showhn.html
- (No bundled `references/` — HN/Reddit norms change; read current pinned rules)
