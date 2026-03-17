---
name: creating-podcast-show-notes
description: Generates timestamped show notes, key takeaways, and formatted transcripts from podcast episodes. Use when the user asks about podcast show notes, episode summaries, timestamps, transcriptions, or podcast publishing.
---

# Podcast Show Notes & Transcription Assistant

## When to use this skill

- User asks to create podcast show notes
- User needs episode timestamps
- User wants transcript formatting
- User mentions podcast publishing
- User needs episode summaries

## Workflow

- [ ] Process transcript or audio
- [ ] Identify key segments
- [ ] Create timestamps
- [ ] Extract takeaways
- [ ] Format guest information
- [ ] Prepare multi-platform output

## Instructions

### Step 1: Episode Information Gathering

Collect episode details: show name, episode number, title, duration, host(s), guest(s), episode type (solo/interview/panel), and source material (audio, video, transcript).

### Step 2: Transcript Processing

Clean transcripts by adding speaker labels, removing filler words (um, uh, like), cleaning false starts, adding timestamps at topic changes, and marking inaudible sections.

### Step 3: Timestamp Creation

| Platform       | Format   | Example  |
| -------------- | -------- | -------- |
| YouTube        | HH:MM:SS | 01:23:45 |
| Apple Podcasts | MM:SS    | 23:45    |
| Spotify        | MM:SS    | 23:45    |
| Show notes     | [MM:SS]  | [23:45]  |

**What to timestamp (priority order):**

1. Episode intro (required)
2. Guest introduction (required)
3. Major topic shifts (required)
4. Key insights/quotes (high)
5. Actionable advice (high)
6. Resource mentions (medium)
7. Outro/CTA (required)

### Step 4: Key Takeaways

Extract 3-5 takeaways with:

- Headline summarizing the insight
- 2-3 sentence explanation
- Direct quote from episode

**Include:** Actionable advice, unique insights, memorable quotes, data/statistics
**Exclude:** Small talk, common knowledge, rambling explanations

### Step 5: Guest Information

Create guest bio with: name, title, company, website, 2-3 sentence authority statement, and social links (Twitter, LinkedIn, website, book/product).

Extract resources mentioned: books, tools, people, websites/articles.

### Step 6: Multi-Platform Output

Generate platform-specific descriptions for:

- **Apple Podcasts** (4000 char limit)
- **Spotify** (concise with emojis)
- **YouTube** (SEO-optimized with hashtags)

See [examples/platform-templates.md](examples/platform-templates.md) for full templates.

### Step 7: Content Repurposing

Create additional content:

- **Blog post**: SEO-optimized written version
- **Social clips**: 3 audiogram suggestions with timestamps
- **Social posts**: Twitter thread, LinkedIn post, Instagram caption
- **Newsletter**: Episode announcement email

See [examples/repurposing-templates.md](examples/repurposing-templates.md) for full templates.

## Output Format

```markdown
# [Podcast Name] - Episode [###]

## [Episode Title]

**Published:** [Date]
**Duration:** [Length]
**Guest:** [Name, Title at Company]

---

## Episode Summary

[2-3 paragraph summary]

---

## Timestamps

[Full timestamp list]

---

## Key Takeaways

[3-5 numbered takeaways with quotes]

---

## Guest Bio & Links

[Bio and social links]

---

## Resources Mentioned

[Categorized resource list]

---

## Platform Descriptions

[Apple, Spotify, YouTube versions]

---

## Social & Repurposing

[Clips, posts, blog, newsletter]

---

## Full Transcript

[Cleaned, timestamped transcript]
```

## Validation

Before completing:

- [ ] All timestamps are accurate
- [ ] Guest name/title spelled correctly
- [ ] All links verified and working
- [ ] Key quotes are accurate to transcript
- [ ] Platform character limits respected
- [ ] Resources properly attributed
- [ ] Transcript cleaned of filler words

## Error Handling

- **No transcript provided**: Recommend transcription services (Descript, Otter.ai, Rev).
- **Poor audio quality**: Note [inaudible] sections; provide context where possible.
- **No guest info**: Search for guest online; ask for bio and links.
- **Episode too long**: Prioritize top 5-7 timestamps; summarize rather than exhaustive.
- **Missing timestamps from source**: Estimate based on topic flow; note as approximate.

## Resources

- [Descript](https://www.descript.com/) - Transcription and editing
- [Otter.ai](https://otter.ai/) - AI transcription
- [Headliner](https://www.headliner.app/) - Audiogram creation
- [Transistor](https://transistor.fm/) - Podcast hosting with show notes
