---
name: archive-suggest
description: Daily suggestions of pre-made social posts from archive content. Scans Master Content Index for evergreen pieces worth resurfacing, generates draft posts, and posts to Slack for team triage.
---

# Archive Suggest

Generate daily social post suggestions from archive content. Surfaces evergreen gems for repurposing.

## When to Use

- Daily content suggestion routine
- When looking for easy content wins
- To keep evergreen content circulating

## Sources to Scan

1. **Master Content Index** - `.claude/references/Master_Content_Index.md`
   - 48 Blog posts
   - 286 Daily newsletters
   - 66 Podcast episodes

2. **Content Database** - `Content/Master Content Database/`
   - Full content files

3. **Podcast Transcripts** - `Studio/Podcast Studio/*/transcript.md`

---

## The Process

### Step 1: Candidate Selection

Scan Master Content Index for pieces worth resurfacing.

**Selection Criteria:**

| Criteria | Weight | Notes |
|----------|--------|-------|
| **Evergreen topic** | High | Not time-sensitive news |
| **Seasonal relevance** | High | Back-to-school (Aug), tax season (Jan-Apr), summer (May-Jun) |
| **News hook** | High | Current event relates to old content |
| **High-performing tags** | Medium | Topics with proven engagement |
| **Underutilized** | Medium | Good content not recently shared |

**Seasonal Triggers:**

| Month | Themes |
|-------|--------|
| Jan-Feb | New year resolutions, tax planning, semester start |
| Mar-Apr | Spring planning, testing season, summer prep |
| May-Jun | End of year, summer activities, deschooling |
| Jul-Aug | Back to school, curriculum planning, getting started |
| Sep-Oct | Settling in, adjustments, fall activities |
| Nov-Dec | Holidays, gift guides, year reflection |

**Output: 3-5 candidate pieces**

### Step 2: Extract Key Snippets

For each candidate, read the full content and extract:

1. **Best standalone insight** (1-2 sentences)
2. **Key quote or stat** (if applicable)
3. **Why share now** (evergreen/seasonal/news hook)

**Snippet format:**

```markdown
## Candidate: [Title]
**Published:** [Date]
**URL:** [URL]
**Type:** Blog / Daily / Podcast

**Best snippet:** "[1-2 sentence insight]"

**Why now:** [Evergreen / Seasonal: [reason] / News hook: [event]]

**Tags:** [relevant tags]
```

### Step 3: Quick Framework Fit

Load TEMPLATE_INDEX.md and generate draft posts.

**For each snippet:**
1. Match to 1-2 best templates
2. Generate LinkedIn draft
3. Generate X draft
4. Include link to original article
5. Add framing ("Still relevant:" or "From our archive:" etc.)

**Framing options:**

- "Still relevant today:"
- "From the archive:"
- "This holds up:"
- "Timely reminder:"
- [No framing - just post the content]

### Step 4: Post to Slack

Post suggestions to **#content-inbox** (C0ABV2VQQKS) using the standard format.

**Slack Message Format:**

```
*[Article Title]*
_Archive | [Type: Blog/Daily/Podcast] | Published [date]_

[Best standalone snippet - 1-2 sentences]

OpenEd angle: [Why share now - evergreen/seasonal/news hook]
Suggested: LinkedIn, X

[URL]
```

**Note:** No emojis in the main format. Reactions (`✍️` to develop, `❌` to skip) are added by users.

---

## Daily Run Checklist

- [ ] Scan Master Content Index
- [ ] Identify 3-5 candidates (mix of evergreen + seasonal)
- [ ] Extract snippets from each
- [ ] Generate draft posts (LinkedIn + X minimum)
- [ ] Post to Slack #content-inbox (C0ABV2VQQKS)
- [ ] Log selections in Performance tracking

---

## Archive Scoring Heuristics

### High Priority (Always Consider)

- **Back-to-school content** - Jul/Aug
- **Getting started guides** - Any new family influx period
- **Method explainers** - (Montessori, Classical, Unschooling) - Evergreen
- **Career prep** - High engagement topic
- **Socialization** - Evergreen FAQ

### Medium Priority

- **Curriculum guides** - Before semester starts
- **Subject-specific** - When seasonal (science fair season, etc.)
- **Tool recommendations** - When tool is in news

### Lower Priority (Rotate In)

- **Day in the life profiles** - Mix variety
- **Podcast clips** - If not recently shared
- **Announcements** - Usually not evergreen

---

## Integration Points

- **Slack MCP** - Post suggestions
- **Master Content Index** - Source database
- **GetLate** - If auto-scheduling approved posts
- **Performance tracking** - Log what gets used

---

## Related Skills

- `newsletter-to-social` - For current content
- `text-content` - Template library
- `quality-loop` - Quality gates for drafts
