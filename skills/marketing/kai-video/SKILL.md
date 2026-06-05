---
name: kai-video
description: Produce video scripts and clipping plans for TikTok, YouTube Shorts, Instagram Reels, and long-form YouTube. Generates hook-first scripts optimized for each platform's algorithm, plus a clipping plan to extract short-form from long-form content. Use when "video script", "TikTok script", "YouTube script", "Reels script", "Shorts script", "video content", "clipping plan", "video ideas", or any request to create video content for social platforms.
---

Produce platform-optimized video scripts and clipping plans. Hook-first, algorithm-aware.

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## Phase 1: Video Discovery

Read from `MARKETING.md`. Only ask about things not covered there:

1. **Topic/product** — what's the video about?
2. **Platform(s)** — TikTok, YouTube Shorts, Reels, YouTube long-form?
3. **Format** — talking head, screen recording, b-roll, animation?
4. **Length** — short-form (15-60s) or long-form (5-15min)?
5. **Goal** — awareness, education, conversion, engagement?
6. **Existing content** — any blog posts or scripts to adapt from?

## Phase 2: Script Production

Load these before writing:
- `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\video-content-creation.md`
- `E:\Dev2\kai-cmo-harness-work\knowledge\channels\tiktok-algorithm.md` (if TikTok)
- `E:\Dev2\kai-cmo-harness-work\knowledge\channels\youtube.md` (if YouTube)
- `E:\Dev2\kai-cmo-harness-work\knowledge\channels\instagram.md` (if Reels)

### Short-Form Script Structure (15-60 seconds)

```markdown
# [Title]

**Platform:** TikTok / Reels / Shorts
**Length:** [X] seconds
**Format:** [talking head / screen / b-roll]

## HOOK (0-3 seconds)
[Pattern interrupt — question, bold claim, or visual surprise]
[This is the most important part. 80% of viewers decide here.]

## BODY (3-45 seconds)
[Main content — one idea, one takeaway]
[Visual direction notes in brackets]

## CTA (last 3-5 seconds)
[What should they do? Follow, comment, visit link, share]

## On-Screen Text
- [0s]: "[text overlay]"
- [3s]: "[text overlay]"
- [15s]: "[text overlay]"

## Hashtags
[Platform-appropriate, 3-5 relevant tags]

## Trending Audio
[Suggest trending sound if applicable, or "original audio"]
```

### Long-Form Script Structure (5-15 minutes)

```markdown
# [Title]

**Platform:** YouTube
**Length:** [X] minutes
**Format:** [format]

## HOOK (0-30 seconds)
[Preview the payoff — what will they know/be able to do?]
[Pattern interrupt opening]

## INTRO (30s-1min)
[Brief context, establish credibility, promise the structure]
"In this video, I'll show you [3 things]..."

## SECTION 1: [Topic]
[Content with visual direction]

## SECTION 2: [Topic]
[Content with visual direction]

## SECTION 3: [Topic]
[Content with visual direction]

## RECAP + CTA
[Summarize key points]
[Clear CTA — subscribe, link in description, comment]

## TIMESTAMPS
- 0:00 Hook
- 0:30 [Section 1]
- X:XX [Section 2]
- X:XX [Section 3]
- X:XX Recap

## THUMBNAIL CONCEPT
[Title text (3-5 words max), facial expression, key visual element]
```

### Hook Formulas (use different ones across videos)

| Hook Type | Formula | Example |
|-----------|---------|---------|
| **Question** | "Did you know [surprising fact]?" | "Did you know 73% of leads call after hours?" |
| **Bold claim** | "[Contrarian statement]" | "Cold email is dead. Here's what replaced it." |
| **Problem** | "If you're struggling with [X]..." | "If your landing page converts under 3%..." |
| **Result** | "We went from [bad] to [good] in [time]" | "We went from 2% to 11% conversion in 3 weeks" |
| **List** | "[Number] [things] that [outcome]" | "5 emails every SaaS needs on day one" |

### Quality Gates (per script)

1. **Hook in first 3 seconds** (no intros, no "hey guys", no logos)
2. **One idea per short-form video** (don't cram)
3. **Zero banned words / AI slop**
4. **CTA present** (but not forced — natural close)
5. **Visual direction included** (not just words)
6. **Platform-appropriate length**

## Phase 3: Clipping Plan (long-form → short-form)

If the user has long-form content, generate a clipping plan:

Load: `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\video-clipping-automation-workflow.md`

| Clip # | Timestamp | Hook | Platform | Length | Script Adaptation |
|--------|-----------|------|----------|--------|-------------------|
| 1 | 2:30-3:15 | [hook] | TikTok | 45s | [adapt for vertical] |
| 2 | 5:00-5:30 | [hook] | Reels | 30s | [adapt for IG] |
| 3 | 8:15-9:00 | [hook] | Shorts | 45s | [adapt for YT] |

### Clip Scoring

Score each candidate before scripting:

| Factor | Score | Question |
|--------|-------|----------|
| Hook | 1-5 | Does the first 3 seconds create a clear reason to keep watching? |
| Standalone clarity | 1-5 | Can the viewer understand the moment without the full source? |
| Proof | 1-5 | Does it include a concrete example, result, quote, or demo moment? |
| Tension | 1-5 | Does it contain contrast, surprise, objection, stakes, or a reveal? |
| Source safety | 1-5 | Is the claim attributable and cleared for use? |

Use clips scoring **18/25+** for production candidates. Put lower-scoring clips in `workspace/video/clipping-plan/_kill-list.md` with the reason.

Every clip row must include a source timestamp or file locator. If the source is a guest, customer, or third-party show, mark approval status before export. Generate clip plans as a dry run first; publishing or upload requires approval.

## Phase 4: Output

```
workspace/video/
├── _video-plan.md              # Overview of all scripts
├── short-form/
│   ├── tiktok-script-1.md
│   ├── tiktok-script-2.md
│   ├── reels-script-1.md
│   └── shorts-script-1.md
├── long-form/
│   └── youtube-full-script.md
├── clipping-plan/
│   └── clips-from-[source].md
└── _quality-report.md
```
