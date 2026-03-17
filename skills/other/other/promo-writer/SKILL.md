---
name: promo-writer
description: Generates platform-specific social media copy from album themes, track concepts, and lyrics. Use when promo/ templates need to be populated before release.
argument-hint: <album-name> [platform]
model: claude-sonnet-4-6
prerequisites:
  - lyric-writer
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Promo Writer Skill

Generate social media copy for album promotion across Twitter/X, Instagram, TikTok, Facebook, and YouTube. Produces native-feeling content for each platform from album context — themes, track concepts, and streaming lyrics.

## Purpose

Populate the `promo/` directory with platform-specific copy ready for review. Each platform gets content shaped to its format, tone, and conventions — not the same text cross-posted everywhere.

## When to Use

- After track concepts and lyrics are written (need material to pull from)
- Before release — generate copy to fill promo/ templates
- User says "write promo copy", "create social media posts", or "fill in the promo templates"
- When promo/ files exist but are still template placeholders

## Position in Workflow

```
Lyrics Written → Promo Videos (optional) → **[Promo Writer]** → [Promo Review] → Release
```

Between content completion and promo-reviewer. The promo-reviewer polishes what this skill generates.

## Supporting Files

- **[copy-formulas.md](copy-formulas.md)** — Hook formulas, CTA templates, post structures, hashtag recipes
- **[/reference/promotion/social-media-best-practices.md](/reference/promotion/social-media-best-practices.md)** — Platform strategy and content guidance
- **[/skills/promo-reviewer/platform-rules.md](/skills/promo-reviewer/platform-rules.md)** — Character limits and hashtag rules

---

## Workflow

### 1. Album Resolution

**Resolve the album from arguments:**

Use MCP `find_album` with the album name from `$ARGUMENTS`. If no album specified, check `get_session` for last album context.

**Verify readiness:**
- Album must have track concepts written
- At least some tracks should have streaming lyrics (for quotable hooks)
- If no streaming lyrics exist, warn: "No streaming lyrics found — using track concepts only. Hooks will be less specific."

### 2. Data Gathering

Gather album context in batch to minimize round-trips:

1. **Album data**: `get_album_full(album_slug, "concept,streaming,musical-direction")` — album narrative + track content
2. **Track list**: from album data — all track names, concepts, statuses
3. **Streaming lyrics**: from album data sections — pull quotable hooks from streaming lyrics (NOT Suno lyrics, which contain phonetic spellings)
4. **User preferences**: `load_override("promotion-preferences.md")` — tone, platform priorities, messaging themes, hashtag preferences, AI positioning

**Critical**: Use **streaming lyrics** for quotable hooks. Suno lyrics contain phonetic spellings (`bit-wize`, `Luh-rock-uh`) that must never appear in public-facing copy.

### 3. Generate Campaign Strategy (campaign.md)

Generate `campaign.md` first — it's the strategy foundation that informs all platform copy.

**Content to generate:**

| Section | What to Write |
|---------|---------------|
| Campaign Overview | Album name, release date (or TBD), primary platform, campaign duration |
| Key Messages | 3 core messages derived from album themes — the "why should anyone care" |
| Target Audience | 2-3 audience segments based on genre and themes |
| Schedule | Pre-release, release week, post-release calendar with specific content types |
| Hashtags | Primary (discovery + genre) and secondary (album-specific, AI if applicable) |

**Derive key messages from album data:**
- What is the album about? → Message 1 (concept hook)
- What makes it different? → Message 2 (unique angle)
- Why listen now? → Message 3 (urgency/relevance)

**Present to user for approval before proceeding to platform copy.**

### 4. Platform Selection

**If platform specified in arguments**, generate only that platform.

**If override exists**, follow platform priority list and skip list from `promotion-preferences.md`.

**Otherwise, ask:**
```
Which platforms should I generate copy for?

[A] All platforms (Twitter, Instagram, TikTok, Facebook, YouTube)
[1] Twitter/X
[2] Instagram
[3] TikTok
[4] Facebook
[5] YouTube
```

### 5. Per-Platform Generation

For each selected platform, generate native content following the structures in [copy-formulas.md](copy-formulas.md) and best practices from the reference guide.

**Read the promo template** for the platform first (`templates/promo/{platform}.md` or existing `promo/{platform}.md`) to match the expected heading structure.

**Per-platform content to generate:**

#### Twitter/X (`twitter.md`)
- Release announcement tweet (1-2 tweets or thread)
- Per-track promo tweets (one per track — hook + concept + link placeholder)
- Behind-the-scenes tweet (process/making-of angle)
- Engagement tweet (question or poll)
- Each tweet: show character count, verify under 280
- 1-2 hashtags per tweet, never starting with a hashtag

#### Instagram (`instagram.md`)
- Release announcement caption (hook in first 125 chars)
- 2-3 track highlight captions (story angle, personal)
- Behind-the-scenes caption
- Hashtag block (15-20 tags, separated from caption)
- Show character count for each caption

#### TikTok (`tiktok.md`)
- Release announcement caption (under 150 chars)
- Per-track captions (short, casual, under 150 chars)
- Behind-the-scenes caption
- 3-5 hashtags per post
- Note: video content does the heavy lifting — captions are secondary

#### Facebook (`facebook.md`)
- Release announcement (longer storytelling format, 150-300 words)
- Track highlight posts (2-3, with personal angle)
- Behind-the-scenes story post
- 3-5 hashtags per post, at end

#### YouTube (`youtube.md`)
- Album/track description template (hook in first 2-3 lines)
- Credits section
- Social links section
- 3-5 hashtags

### 6. Present for Approval

Present each platform's generated copy with metrics:

```
## Twitter/X — Generated Copy

### Release Announcement
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Generated tweet text]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Chars: 187/280 | Hashtags: 2 | Status: Within limits
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Track 01: [Track Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Generated tweet text]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Chars: 214/280 | Hashtags: 2 | Status: Within limits
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[... more posts ...]

Actions:
  [A] Approve all — write to promo/twitter.md
  [R] Revise specific posts — tell me which ones and what to change
  [N] Next platform — skip this platform
```

### 7. Write Approved Copy

Write approved copy to the `promo/` directory in the album path:

```
{content_root}/artists/{artist}/albums/{genre}/{album}/promo/
```

**Match the file structure expected by promo-reviewer:**
- Use `##` and `###` headings to delineate sections
- Put post copy inside ``` code blocks
- Include any platform-specific metadata (character counts not written to file)

**If promo/ directory doesn't exist**, create it.
**If files already exist**, ask before overwriting:
```
promo/twitter.md already has content. Overwrite? [Y/n]
```

### 8. Summary and Next Steps

After all platforms are written:

```
## Promo Copy Generated

| Platform | Posts | Status |
|----------|-------|--------|
| Campaign | 1 | Written |
| Twitter  | 8 | Written |
| Instagram | 5 | Written |
| TikTok | 6 | Written |
| Facebook | 4 | Written |
| YouTube | 1 | Written |

Files written to: {album_path}/promo/

Next steps:
  1. Review and polish: /bitwize-music:promo-reviewer <album-name>
  2. Replace [Streaming Link] placeholders with actual URLs when available
  3. When ready to release: /bitwize-music:release-director <album-name>
```

---

## Content Rules

### Streaming Lyrics Only
Pull quotable hooks from **streaming lyrics** sections. Never use Suno lyrics — they contain phonetic spellings meant for the AI, not human readers.

### Campaign First
Always generate `campaign.md` before platform copy. The strategy document establishes key messages, audience, and schedule that inform every platform's content.

### Native Content
Each platform gets content shaped to its conventions:
- Twitter: punchy, under 280 chars, 1-2 hashtags
- Instagram: visual-first, hook in first 125 chars, hashtag block
- TikTok: ultra-casual, under 150 chars, video does the work
- Facebook: storytelling, longer form, community-building
- YouTube: informative, structured, SEO-aware

Never write the same text for multiple platforms.

### Match Promo-Reviewer Structure
The promo-reviewer skill expects specific file structure:
- `##` headings for major sections
- `###` headings for individual posts
- Post copy inside ``` code blocks
- This structure enables section-by-section review

### Hashtag Rules
Follow the researched best practices:
- **Twitter**: 1-2 per tweet, never start with hashtag, rotate sets
- **Instagram**: 15-20 per post, separate block, mix volume levels
- **TikTok**: 3-5 per post, include trending if applicable
- **Facebook**: 3-5, at end, for categorization
- **YouTube**: 3-5, first 3 shown above title
- **Never use**: #MusicPromotion, #SoundCloudPromotion, #FollowBack, #Like4Like

### Override Respect
If `promotion-preferences.md` override exists:
- Follow tone and voice preferences
- Respect platform skip list
- Apply messaging theme preferences (always/never mention)
- Use hashtag preferences (always include, avoid list)
- Follow AI positioning guidance

---

## Remember

1. **Read copy-formulas.md** at invocation — it has the hook formulas and post structures
2. **Streaming lyrics only** — never Suno phonetic lyrics in public copy
3. **Campaign.md first** — strategy before platform copy
4. **Present before writing** — show generated copy with metrics for approval
5. **Native per platform** — different tone, length, structure for each
6. **Match promo-reviewer format** — headings + code blocks for section-by-section review
7. **Check override** — load `promotion-preferences.md` for tone, platforms, messaging
8. **Suggest promo-reviewer next** — always end with the recommendation to review
9. **Placeholder links** — use `[Streaming Link]` where real URLs will go
10. **Preserve album voice** — the copy should feel consistent with the album's themes and tone

**Your deliverable**: Populated `promo/` directory with platform-specific copy ready for review.

**Workflow integration**: You fill the gap between content completion and promo-reviewer — generating what was previously a manual creative step.
