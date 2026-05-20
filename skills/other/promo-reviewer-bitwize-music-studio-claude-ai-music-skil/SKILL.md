---
name: promo-reviewer
description: Reviews and iterates on social media copy in album promo/ files. Use after populating promo templates and before release to polish platform-specific posts.
argument-hint: <album-name> [platform]
model: claude-sonnet-4-6
allowed-tools:
  - Read
  - Edit
  - Glob
  - Grep
---

# Promo Reviewer Skill

Interactive review and polish of social media copy in album `promo/` files. Walk through each post, approve or revise, and write polished results back to the file.

## Purpose

After promo templates are populated with platform-specific copy, this skill provides structured review before release. Each post is presented with character counts, hashtag counts, and platform limit compliance. The user chooses actions (approve, revise, shorten, punch up, etc.) and polished copy is written back.

## When to Use

- After `/bitwize-music:promo-writer` generates initial copy
- After populating promo/ templates (manually or during release prep)
- Before release — final polish pass on social media copy
- User says "review promo copy" or "polish the twitter posts for [album]"
- When promo copy exists but hasn't been reviewed

## Position in Workflow

```
Promo Videos (optional) → [Promo Writer] (or manual) → **[Promo Review]** → Release
```

Between populating promo templates and release-director.

## Supporting Files

- **[platform-rules.md](platform-rules.md)** — Per-platform character limits, hashtag rules, tone guidelines

---

## Workflow

### 1. Album Resolution

**Resolve the album from arguments:**

Use MCP `find_album` with the album name from `$ARGUMENTS`. If no album specified, check `get_session` for last album context.

**Locate promo directory:**
```
{content_root}/artists/{artist}/albums/{genre}/{album}/promo/
```

**Check which promo files exist and have content:**

Glob for `promo/*.md` in the album directory. For each file, check if it contains populated content (not just template placeholders). A file is "populated" if it contains text beyond the template markers — look for content inside code blocks that isn't `[placeholder text]`.

**Report status:**
```
## Promo Copy Status

| Platform | File | Status |
|----------|------|--------|
| Campaign | campaign.md | Populated |
| Twitter/X | twitter.md | Populated |
| Instagram | instagram.md | Template only |
| TikTok | tiktok.md | Not found |
| Facebook | facebook.md | Populated |
| YouTube | youtube.md | Template only |

3 of 6 platforms have copy ready for review.
```

If no promo files are populated:
```
No promo copy found to review.

Options:
1. Generate promo copy: /bitwize-music:promo-writer <album-name>
2. Populate promo templates manually (fill in promo/ files)
3. Skip promo review and proceed to release
```

### 2. Platform Selection

**If platform specified in arguments**, review only that platform.

**Otherwise, ask:**
```
Which platforms to review?

[A] All populated platforms (campaign, twitter, facebook)
[1] Campaign strategy
[2] Twitter/X posts
[3] Facebook posts
```

List only populated platforms as numbered options.

### 3. Section Parsing

For each selected platform file:

1. **Read the full file** using the Read tool
2. **Split at heading boundaries** — `##` and `###` headings delineate sections
3. **Extract code blocks** — content inside ``` fences is the actual post copy
4. **Identify reviewable sections** — sections with code blocks containing non-placeholder text
5. **Count metrics** for each post:
   - Character count (hashtags count toward the limit on all platforms)
   - Hashtag count
   - Line count
   - Platform limit compliance (from platform-rules.md)
6. **Thread detection** — if a code block contains numbered tweets (1/, 2/, 3/), split into individual tweets and review each separately with per-tweet char counts

### 4. Per-Post Review Loop

For each reviewable section, present the post with context:

```
## Twitter/X — Track 01: Track Title
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Track one tells the story of [concept].

Listen now: [link]

#NewMusic #HipHop

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Chars: 87/280 | Hashtags: 2 | Status: Within limits
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Actions:
  [A] Approve — keep as-is
  [R] Revise — give feedback for rewrite
  [S] Shorten — make more concise
  [P] Punch up — make more engaging/attention-grabbing
  [H] Add hashtags — suggest relevant hashtags
  [T] Rewrite tone — specify tone (casual, professional, hype, etc.)
  [K] Skip — move to next without changes
```

**After any revision action (R, S, P, H, T):**

1. Generate the revised version
2. Present it with updated metrics
3. Offer follow-up:
```
Revised version:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[revised copy here]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Chars: 142/280 | Hashtags: 3 | Status: Within limits
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  [A] Approve this version
  [R] Revise again — more feedback
  [D] Discard — revert to original
```

### 5. Campaign.md Special Handling

Campaign files contain strategy tables and messaging, not code-block posts. Adjust the review approach:

- **Present each section** (Overview, Key Messages, Schedule, etc.) as a reviewable unit
- **Replace "Punch up"** with **"[M] Strengthen messaging"** — tighten the strategic language
- **Skip character limits** — campaign docs have no platform limits
- **Focus on**: clarity, consistency with album themes, actionable schedule entries, complete metadata fields

### 6. Write-Back

After all sections for a platform are reviewed:

1. **Reconstruct the file** with approved/revised content in place
2. **Use the Edit tool** to apply changes to the promo file
3. **Confirm write:**
```
Updated twitter.md — 4 posts revised, 2 approved as-is, 1 skipped
```

Only write back if at least one section was revised. If all sections were approved as-is or skipped, skip the write step.

### 7. Progress Tracking

Between platforms, show a running summary:

```
## Review Progress

| Platform | Approved | Revised | Skipped | Limit Issues |
|----------|----------|---------|---------|--------------|
| Twitter  | 4        | 2       | 1       | 0            |
| Facebook | —        | —       | —       | —            |

Next: Facebook (5 sections to review)
Continue? [Y/n]
```

### 8. Session Summary

After all platforms reviewed:

```
## Promo Review Complete

| Platform | Approved | Revised | Skipped |
|----------|----------|---------|---------|
| Campaign | 3        | 1       | 0       |
| Twitter  | 4        | 2       | 1       |
| Facebook | 3        | 2       | 0       |
| **Total** | **10** | **5** | **1** |

Char limit compliance: All posts within platform limits

Files updated:
  - promo/campaign.md (1 revision)
  - promo/twitter.md (2 revisions)
  - promo/facebook.md (2 revisions)

Next steps:
  1. Review any skipped posts if needed
  2. Add streaming links when available (replace [Streaming Link] placeholders)
  3. Ready for release: /bitwize-music:release-director <album>
```

---

## Revision Guidelines

When revising posts, follow these principles:

### Shorten (S)
- Cut filler words ("really", "very", "just")
- Combine sentences where possible
- Prioritize the hook — lead with the most compelling element
- Respect platform limits (see platform-rules.md)

### Punch Up (P)
- Stronger verbs, more vivid language
- Add urgency or curiosity
- Open with a hook, not a description
- Keep the core message — just make it hit harder

### Add Hashtags (H)
- Suggest 3-5 relevant hashtags based on genre, album themes, platform norms
- Present options — user picks which to include
- Follow platform-specific hashtag conventions (see platform-rules.md)
- Never exceed platform maximum

### Rewrite Tone (T)
- Ask user for target tone before rewriting
- Common tones: casual, professional, hype, mysterious, storytelling, urgent
- Preserve factual content — only change voice and style
- Match tone to platform expectations

### Strengthen Messaging (M) — Campaign only
- Tighten strategic language
- Make key messages more memorable and quotable
- Ensure schedule entries are specific and actionable
- Verify consistency between messaging and album themes

---

## Platform-Specific Review Focus

### Twitter/X
- Every post under 280 chars (hard limit)
- Thread tweets: each tweet standalone but connected
- 1-2 hashtags max (more looks spammy)
- Streaming link in release posts

### Instagram
- Caption can be long (2,200 chars) but first 125 visible before "more"
- Hook in first line — it's the only thing people see
- Hashtags as separate block at end
- 15-20 hashtags is optimal (30 max)

### TikTok
- Under 150 chars ideal (visible without tap)
- 4,000 char max but shorter is better
- 3-5 hashtags, trending ones if applicable
- Casual, authentic tone

### Facebook
- Longer storytelling works well
- First 2-3 lines visible before "See more"
- 3-5 hashtags (less hashtag-driven platform)
- Include call to action

### YouTube
- Description supports timestamps, credits, links
- First 2-3 lines visible in collapsed view
- Include streaming links, social links, credits
- 3-5 hashtags (shown above title)

---

## Remember

1. **Read platform-rules.md** at invocation start for current limits
2. **Present one post at a time** — don't batch review
3. **Show metrics with every post** — chars, hashtags, limit compliance
4. **Never auto-approve** — every post gets user review
5. **Write back only changed files** — don't touch files with no revisions
6. **Track progress** — running counts between platforms
7. **Campaign is different** — strategy doc, not social posts
8. **Preserve user voice** — revisions should enhance, not replace the user's style
9. **Flag limit violations** — highlight posts over platform char limits
10. **Placeholder detection** — flag remaining `[placeholder]` text that needs real content
