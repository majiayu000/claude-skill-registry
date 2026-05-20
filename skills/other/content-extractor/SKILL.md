---
name: content-extractor
description: Extract content ideas from long-form content (transcripts, videos, articles) and organize them into detailed, platform-specific tables. Produces ready-to-execute briefs with titles, hooks, descriptions, and key points for newsletters, social posts, and more. Use when user has existing content and wants to "extract ideas", "repurpose content", or "get more from this piece".
---

## Load Context First

Before executing this skill, read the following files from the project folder if they exist:

1. **USER.md** — who the user is, how they think, how they work
2. **BUSINESS.md** — their business, products, positioning, brand voice, content strategy
3. **ICP.md** — their ideal customer, their language, their fears, what makes them buy
4. **Voice or brand voice skill** — look for any installed skill related to voice, tone, or brand voice and apply it automatically
5. Any additional context provided by the user in this session

Use all context silently. Do not reference or summarize files unless asked.

---

# Content Extractor

**Purpose:** Transform long-form content into a comprehensive content pipeline. Produces detailed, organized tables of content ideas tailored to specific platforms, ready for execution.

## When to Activate

Use this skill when:
- User has a transcript, video, article, or any long-form content
- User wants to extract multiple content pieces from one source
- User needs organized, actionable content ideas by platform
- User wants to maximize the value from existing content

## Process

### Step 1: Clarify Platform Targets

Ask which platforms they want content for:
- Newsletters (thought leadership, how-to guides)
- Substack Notes (short-form insights)
- Twitter/X (threads and standalone posts)
- LinkedIn (professional posts)
- YouTube Shorts / Reels (short-form video)

### Step 2: Deep Content Analysis

Analyze the source looking for:
- **Unique perspectives** not commonly shared
- **Teachable content** — processes, frameworks, how-to steps
- **Stories & examples** — personal experiences, case studies
- **Data & proof points** — statistics, results
- **Emotional hooks** — pain points, aspirations, fears

### Step 3: Map Ideas to Platforms

| Content Type | Best Platforms |
|--------------|----------------|
| Deep frameworks | Newsletter, LinkedIn article |
| Quick tips | Twitter, Substack Notes |
| Step-by-step processes | Newsletter (how-to), Twitter thread |
| Personal stories | LinkedIn, Newsletter |
| Contrarian takes | Twitter, Substack Notes |
| Data/stats | LinkedIn, Twitter |

### Step 4: Generate Platform Tables

For each platform, produce detailed tables with platform-specific fields.

## Output Format

```markdown
# Content Extraction Report

**Source:** [Description of source]
**Platforms:** [Platforms requested]
**Total Ideas Extracted:** [Number]

---

## Newsletter Ideas

| # | Title | Subject Line | Type | Description | Key Points | Word Count |
|---|-------|--------------|------|-------------|------------|------------|
| 1 | [Title] | [Subject] | [Type] | [2-3 sentences] | • Point 1 • Point 2 • Point 3 | 800-1200 |

**Top Pick:** Idea #[X] — [Why]

---

## Substack Notes Ideas

| # | Hook (First Line) | Note Type | Full Note Draft | Why It Works |
|---|-------------------|-----------|-----------------|--------------|
| 1 | [Opener] | [Type] | [Complete 3-6 sentence note] | [Reasoning] |

**Top Pick:** Idea #[X] — [Why]

---

## Twitter/X Ideas

### Threads
| # | Hook Tweet | Structure | Key Points | Engagement Angle |
|---|------------|-----------|------------|------------------|
| 1 | [Hook] | [X] tweets | • Point 1 • Point 2 | [Why engage] |

### Standalone Posts
| # | Tweet | Type | Why It Works |
|---|-------|------|--------------|
| 1 | [Full tweet ≤280 chars] | [Type] | [Reasoning] |

---

## LinkedIn Post Ideas

| # | Opening Line | Angle | Key Points | CTA | Post Type |
|---|--------------|-------|------------|-----|-----------|
| 1 | [Hook] | [Angle] | • Points | [CTA] | [Type] |

---

## Execution Roadmap

### Immediate (This Week)
1. **[Platform]:** [Idea] — [Why prioritize]
2. **[Platform]:** [Idea] — [Why]

### Short-Term (Next 2 Weeks)
3-5. [Continue...]
```

## Quality Checklist

- [ ] All ideas traceable to specific content in the source
- [ ] Each idea has title, hook, and key points (not just "write about X")
- [ ] Platform-native formatting (right length, right structure)
- [ ] Audience-aligned (speaks to ICP pain points)
- [ ] Top picks identified per platform
- [ ] Execution roadmap with priorities
- [ ] No ideas fabricated beyond the source material
