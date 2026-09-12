---
name: social-campaign
description: >
  End-to-end social content campaign pipeline. Takes a marketing goal and produces
  scheduled, on-brand social posts with visuals across postiz-supported platforms,
  while keeping Typefully for X/thread specialist flows and fallback coverage.
  Chains: CMO strategy, content writing with voice calibration, AI slop audit,
  selective Paper MCP visual design, and routed scheduling via postiz or Typefully.
  Each phase has a
  human gate. Use this skill whenever someone wants to plan and execute a batch of
  social posts — not just one-off tweets. Triggers include: "social campaign",
  "schedule posts", "pre-launch content", "content calendar", "social content pipeline",
  "build up content", "I need social media content for my launch", "help me build
  social presence", "plan a week of posts", "batch social content", "social media
  strategy", or any request involving multiple scheduled posts with optional visuals.
allowed-tools:
  - Bash(mktg status *)
  - Bash(*/typefully.js *)
---

# /social-campaign — Social Content Campaign Pipeline

Orchestrator that chains 5 phases into a complete social content campaign:

```
STRATEGY  →  WRITE  →  REVIEW  →  DESIGN  →  SCHEDULE
 (plan)     (draft)   (audit)   (visuals)  (postiz/typefully)
```

Each phase is an independent block. This orchestrator is one recipe that combines them. Produces N scheduled posts with selective visuals from a single marketing goal.

## When to Use

- Pre-launch content build-up (1-2 week runway)
- Ongoing content calendar creation
- Campaign bursts around announcements
- Any time you need multiple scheduled posts with visuals

## Architecture

```
Phase 1: STRATEGY   — Plan content calendar with themes, timing, platform mix
Phase 2: WRITE      — Draft posts calibrated to real voice (not brand doc voice)
Phase 3: REVIEW     — AI slop audit + voice calibration against published posts
Phase 4: DESIGN     — Selective visual creation in Paper MCP (not every post)
Phase 5: SCHEDULE   — Route each post to postiz first, with Typefully as the X/thread specialist and fallback
```

## Workflow

### Phase 0: Load Context

1. Run `mktg status --json` to check brand health
2. Read brand files in parallel:
   - `brand/voice-profile.md` (tone, vocabulary, do's/don'ts)
   - `brand/positioning.md` (angles, headlines)
3. Read `brand/landscape.md` if it exists — check the Claims Blacklist before making ecosystem or competitive claims. If stale (>14 days) or missing, warn that market claims may be outdated.
4. Check social distribution readiness: `mktg doctor --json --fields checks.postiz.configured,checks.typefully.configured`
5. If Typefully is configured, load Typefully config: check default social set, list available accounts
6. If Typefully is configured, check queue schedule:
   - `typefully.js queue:get --start-date <today> --end-date <+N days>`
   - `typefully.js queue:schedule:get` (what days/times are slots)
7. Read recent published posts:
   - Prefer Typefully history when available: `typefully.js drafts:list --status published --sort -created_at`
   - Otherwise use the project's recent post corpus or approved drafts for voice calibration

**If brand files are missing:** The skill still works. Ask the user for: (1) brand voice in 2-3 adjectives, (2) target platforms, (3) content themes. Proceed with these as lightweight context. Brand files enhance, never gate.

**If Typefully queue is empty (no available slots):** Offer the user two options: (1) create drafts without scheduling (user schedules manually in Typefully UI), or (2) use specific datetime scheduling with `--schedule "ISO_datetime"`. This only applies to posts routed to Typefully.

**Present context summary:**
```
Brand: loaded (voice, positioning) | OR: missing — using lightweight context
Postiz: configured for multi-provider social distribution | OR: missing — Typefully/file/browser fallbacks only
Typefully: connected for X/threads specialist routing and fallback | OR: missing
Queue: {N} empty Typefully slots over next {days} days ({schedule})
Last post: "{preview}" ({date})
```

### Phase 1: STRATEGY

Plan the content calendar. This is strategic thinking, not template filling.

**Inputs needed (use AskUserQuestion if not provided):**
- What's the marketing goal? (launch, awareness, engagement, authority)
- What's the timeline? (1 week, 2 weeks, ongoing)
- Any specific themes or angles to hit?

**Planning process:**
1. Analyze the goal, timeline, and available queue slots
2. Plan N posts distributed across the timeline
3. For each post, decide:
   - **Day and time slot** (from queue schedule)
   - **Platform mix** (X only, LinkedIn only, or both)
   - **Theme** (problem awareness, value education, social proof, product tease, announcement)
   - **Content type** (observation, hot take, how-to, builder update, announcement)
4. Consider pacing: build gradually, don't front-load announcements
5. Consider variety: alternate themes, don't repeat the same structure

**Present the calendar for approval:**

```
| # | Date | Platform | Theme | Hook Direction |
|---|------|----------|-------|----------------|
```

**Gate:** User must approve calendar before Phase 2.

### Phase 2: WRITE

Draft all posts, calibrated to the user's ACTUAL voice (not just the brand doc).

**Critical: Voice Calibration**

Before writing, read 5-8 recent published posts from Typefully:
```bash
typefully.js drafts:list --status published --sort -created_at
typefully.js drafts:get <id>  # for full text of top posts
```

Analyze the real voice patterns:
- Sentence length and structure
- Use of fragments vs complete sentences
- Technical specificity level
- How they open posts (fact-first? question? observation?)
- How they close (link? command? statement?)
- Personality markers (dry humor? directness? code inline?)

**Write each post matching these patterns, NOT generic brand voice.**

For each post:
1. Write the full text
2. Determine platform (X, LinkedIn, or both)
3. If cross-platform with same content, use one draft with `--platform x,linkedin`
4. If cross-platform with different content, plan as single draft with platform-specific text

**Present all posts for approval as a numbered list with the full text.**

**Gate:** User must approve posts before Phase 3.

### Phase 3: REVIEW

Two-part quality audit. This is the most important phase for authenticity.

#### 3a: AI Slop Audit

Audit every post for these AI tells. **Read each post manually, in sequence, looking at the batch as a whole** (not just individual posts). This cannot be done with regex.

**Structural patterns to catch:**
- Sentences that all follow the same rhythm (subject-verb-explanation, repeat)
- Every post opening with a question or every post opening with a bold claim — variety is key
- Numbered lists where every item has the same sentence structure
- "Sandwich" pattern: statement, elaboration, restatement in every post

**Transition filler to remove:**
- "Here's the thing:", "Let me be clear:", "The reality is:", "At the end of the day"
- "In today's [landscape/world/environment]", "When it comes to"
- "It's worth noting that", "Interestingly enough", "Not gonna lie"

**Vocabulary tells to flag:**
- "Leverage", "unlock", "game-changer", "deep dive", "robust", "streamline"
- "Landscape", "navigate", "elevate", "empower", "cutting-edge"
- Overuse of "incredibly", "absolutely", "fundamentally"

**Batch-level monotony checks:**
- Do 3+ posts start the same way? Fix it.
- Do all posts use the same CTA? Vary them.
- Is the emotional range flat? Mix insight, humor, urgency, curiosity.
- Could you shuffle the posts and not notice? Each needs a distinct angle.

If /cmo is installed, also reference `~/.claude/skills/cmo/references/ai-slop-patterns.md` for the full pattern library.

#### 3b: Voice Calibration Check

Compare each post against the published posts from Phase 2's calibration:
- Does this sound like the same person wrote it?
- Would this blend in with their real timeline?
- Is the technical specificity level right?
- Are the sentence rhythms natural?

**Fix anything that fails either audit. Present the final versions.**

**Gate:** User approves final post text.

### Phase 4: DESIGN

Selective visual creation. NOT every post gets an image — text-only posts feel more authentic for personal observations and hot takes.

For the full decision framework (which posts get images), image types, Paper MCP steps, and design system specs, see `references/paper-mcp-workflow.md`.

**Quick decision rule:** Comparisons, processes, data, and announcements get images. Personal takes, vents, and builder updates stay text-only.

**Present image plan for approval:**

```
| Post # | Image? | What It Shows |
|--------|--------|---------------|
```

**Gate:** User approves image plan. User exports PNGs from Paper after design.

### Phase 5: SCHEDULE

<!-- BEGIN POSTIZ EXTENSION (mktg v0.2+) -->

**Step 0 — Pick the scheduling backend per post.**

Before scheduling anything, detect which backends are available. This check runs once per Phase 5 entry and caches for the phase:

```bash
mktg doctor --json --fields checks.typefully.configured,checks.postiz.configured
```

Resolve the routing per post using the table below. `platform` is already tagged per post by Phase 2 and appears verbatim in the post file's YAML frontmatter.

| Platform tagged on the post | Both configured | Typefully only | Postiz only | Neither |
|---|---|---|---|---|
| `x` / Twitter (single or thread) | **Typefully** (threads are canonical here) | Typefully | Postiz (no thread support, flag it) | Skip with fix: "Set TYPEFULLY_API_KEY or POSTIZ_API_KEY" |
| `linkedin`, `threads`, `bluesky`, `mastodon` | **Postiz** (richer provider catalog) | Typefully | Postiz | Skip with fix |
| `reddit`, `instagram`, `tiktok`, `youtube`, `pinterest`, `discord`, `slack` | **Postiz** | Can't publish — write file only, instruct user to copy-paste | Postiz | Skip with fix |

**Invariant:** any post with `type: thread` stays on Typefully regardless of postiz availability. Thread UX is Typefully's canonical path; do not degrade it.

**Progressive enhancement:** if `checks.postiz.configured === false`, Phase 5 behaves exactly as the Typefully-only path below — zero behavior change for users without postiz. If both are missing, fall back to writing files into `marketing/campaigns/{campaign-name}/posts/` and surface a "copy these to the platform UI" summary.

**Fallback behavior under failure (during the phase):**
- Postiz unreachable / 5xx: retry once with exponential backoff (1s, 2s). On second failure for a Typefully-covered platform (linkedin/threads/bluesky/mastodon), fall back to Typefully. On second failure for a postiz-only platform (reddit/instagram/tiktok/youtube/pinterest/discord/slack), fail the post with `fix: "postiz unreachable — check mktg catalog info postiz --fields configured,resolved_base"`.
- Postiz 401: halt the entire phase. Bad key means the whole batch will fail; don't waste rate-limit quota.
- Postiz 429: parse `Retry-After` from the adapter's error envelope; surface to the user. Resume after the cooldown or save the batch for later.
- Typefully failure: unchanged from pre-extension behavior — fail loudly per the existing flow below.

<!-- END POSTIZ EXTENSION -->

### Case A — Typefully path (X and threads, plus Typefully-covered platforms when postiz is absent)

Upload media and schedule all posts via Typefully.

**For posts WITH images:**
1. Find exported PNGs (ask user for location if needed)
2. Upload each: `typefully.js media:upload <file_path>`
3. Create or update draft with media: `typefully.js drafts:create --platform x,linkedin --text "..." --media <media_id> --schedule <ISO_datetime>`

**For text-only posts:**
1. Create draft: `typefully.js drafts:create --platform x,linkedin --text "..." --schedule <ISO_datetime>`

**For updating existing drafts (if created earlier):**
1. Upload media: `typefully.js media:upload <file>`
2. Update draft with text AND media: `typefully.js drafts:update <draft_id> --text "..." --media <media_id> --use-default`
   (Note: `--text` is required even when only adding media)

**Scheduling options:**
- Specific time: `--schedule "2025-01-21T09:00:00Z"`
- Next queue slot: `--schedule next-free-slot`
- Publish now: `--schedule now`

**After scheduling all posts:**
1. Verify: `typefully.js drafts:list --status scheduled --sort scheduled_date`
2. Confirm each draft has correct platform, text, and media
3. Present final summary table

**Gate:** User reviews scheduled posts in Typefully UI.

### Case B — Postiz path (non-Twitter platforms when postiz is configured)

For each post whose routed backend is postiz (per Step 0 table), build a `publish.json` entry and invoke the adapter. You do NOT call the postiz API directly — always go through `mktg publish --adapter postiz`.

**For text-only posts (v1 is draft-only; scheduling lands in v2):**
1. Build `publish.json` with one item per post:
   ```json
   {
     "name": "{campaign-name}",
     "items": [{
       "type": "social",
       "adapter": "postiz",
       "content": "<post text>",
       "metadata": { "providers": ["<postiz-identifier>"] }
     }]
   }
   ```
   `providers` must be exact postiz `identifier` strings (`linkedin`, `linkedin-page`, `bluesky`, `reddit`, etc.) — resolve friendly names via `/postiz` skill's Step 2b alias logic, not inline here.

2. Dry-run: `mktg publish --adapter postiz --dry-run --input '<json>' --json`. Verify the adapter validates the providers against connected integrations.
3. Confirm: `mktg publish --adapter postiz --confirm --input '<json>' --json`. The adapter writes sent-markers to `.mktg/publish/{campaign-name}-postiz.json` on success.
4. Update the post file frontmatter: `status: scheduled`, `draft_id: <id>`.

**For posts WITH images (v2 — skip in v1):**
postiz v1 is draft-only; images hardcode to `[]`. If a post has `has_image: true`, either (a) wait for v2, or (b) downgrade to Typefully if the platform allows (X/LinkedIn). Do NOT populate `metadata.mediaPaths` in v1 — the adapter ignores it.

**After scheduling all posts (mixed Typefully + postiz):**
1. Verify Typefully side: `typefully.js drafts:list --status scheduled --sort scheduled_date`.
2. Verify postiz side: the adapter's response envelope already reports per-provider status in `results[]`. Capture draft IDs to the post file frontmatter.
3. Present the unified final summary table.

**Gate:** User reviews scheduled posts in each platform's UI (Typefully for X, postiz dashboard for everything else).

## Human-in-the-Loop Gates

```
[Phase 1] → User approves content calendar
[Phase 2] → User approves post drafts
[Phase 3] → User approves after AI slop + voice audit
[Phase 4] → User approves image plan, exports PNGs from Paper
[Phase 5] → User verifies in Typefully UI
```

Each gate is an AskUserQuestion. The user can go back to any phase.

## Output

```
marketing/campaigns/{campaign-name}/
  calendar.md              # Content calendar with themes + timing
  posts/
    post-01.md             # Each post with text, platform, schedule
    post-02.md
    ...
  images/
    post-03-comparison.png # Exported from Paper
    post-06-flow.png
    ...
  campaign-log.md          # What was scheduled, draft IDs, media IDs
```

### Post File Format

Each `post-XX.md` file uses this structure:

```yaml
---
post_number: 1
platform: x,linkedin
type: single | thread | carousel
scheduled_date: "2026-03-25T09:00:00Z"
draft_id: ""          # Populated after Typefully draft creation
media_id: ""          # Populated after media upload
has_image: false
status: draft | approved | scheduled | published
---
```

```
[Post text goes here]

[For threads, separate tweets with ---]
```

## Integration Requirements

| Integration | Required? | Check |
|-------------|-----------|-------|
| Typefully API key | Yes | `typefully.js config:show` |
| Paper MCP | Only if images needed | `mcp__paper__get_basic_info()` |
| Brand files | Recommended | `mktg status --json` |

If Typefully is not configured, guide setup before Phase 5.
If Paper MCP is not available, skip Phase 4 (text-only campaign).

## Reusable Blocks

| Block | Standalone Use |
|-------|---------------|
| Phase 1 (Strategy) | Content calendar for any channel |
| Phase 2 (Write) | Draft posts for manual publishing |
| Phase 3 (Review) | Audit any written content for AI slop |
| Phase 4 (Design) | Create visuals for any social content |
| Phase 5 (Schedule) | Schedule any drafts via Typefully |

## Anti-Patterns

| Anti-Pattern | Why It Fails | Instead |
|-------------|-------------|---------|
| Image on every post | Looks like a content calendar, not a person | Be selective; text-only posts feel authentic |
| Same card template with different text | Spam in the feed | Each image must have a unique visual concept |
| Writing from brand doc alone | Sounds like marketing copy, not the person | Calibrate against their actual published posts |
| Scheduling all at once without review | AI slop gets through | Manual line-by-line audit is non-negotiable |
| Front-loading announcements | Audience isn't warmed up | Build: awareness → value → tease → announce |

## Principles

- **Voice over brand** — Match the person's real voice, not the documented brand voice
- **Selective visuals** — Every image must earn its place; text-only is a valid choice
- **Batch coherence** — Posts should vary in structure; no two adjacent posts should use the same pattern
- **AI slop is non-negotiable** — Manual audit every time, no shortcuts
- **Skills never call skills** — This SKILL.md teaches the agent the sequence; the agent loads each skill
- **Filesystem is the bus** — Campaign state persists as files, not in conversation
- **Human gates at every phase** — No runaway agent chains
