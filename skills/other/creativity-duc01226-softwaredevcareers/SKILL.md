---
name: creativity
description: "Creative direction intelligence. 55 styles, 18 platforms, 12 voiceover types, 17 music genres, 30 campaign categories. Actions: create, design, plan, direct, brief creative campaigns. Projects: ads, videos, social content, commercials, brand films. Styles: minimalist, maximalist, nostalgic, cinematic, UGC, luxury, futuristic, emotional. Topics: visual style, platform specs, voiceover, music, color palette, audience targeting."
version: 2.0.0
---

# Creativity Pro Max - Creative Direction Intelligence

Comprehensive creative direction guide for digital marketing campaigns. Contains 55 styles, 18 platforms, 12 voiceover types, 17 music genres, and 30 campaign category recommendations. Searchable database with priority-based recommendations.

## When to Apply

Reference these guidelines when:
- Planning creative campaigns for any channel
- Selecting visual styles for ads/content
- Choosing voiceover/music direction
- Creating platform-specific content
- Developing creative briefs

## Core Principle

**92% prefer authentic content over polished ads.** Prioritize real, relatable content over perfection.

## Quick Style Selection

| Audience/Goal | Recommended Styles |
|---------------|-------------------|
| Premium/Luxury | Minimalist Clean, Quiet Luxury, Dark Moody Cinematic |
| Tech/SaaS | Futuristic Sci-Fi, Gradient Smooth, Minimalist Tech |
| Youth/Gen Z | Raw Unpolished, Humor Comedic, Nostalgic 90s, Neon Cyber |
| Wellness/Organic | Earthy Organic, Emotional Storytelling, Pastel Soft |
| B2B/Finance | Authoritative Expert, Data Visualization, Corporate Modern |
| Community | Authentic UGC, Conversational Casual, Behind The Scenes |

---

## How to Use This Skill

When user requests creative direction (campaign, ad, video, content), follow this workflow:

### Step 1: Analyze User Requirements

Extract key information from user request:
- **Campaign type**: Product launch, brand awareness, lead gen, etc.
- **Audience**: Gen Z, Millennials, B2B, etc.
- **Industry**: SaaS, e-commerce, healthcare, etc.
- **Platform**: TikTok, Instagram, YouTube, etc.

### Step 2: Generate Creative Brief (REQUIRED)

**Always start with `--creative-brief`** to get comprehensive recommendations:

```bash
python3 .claude/skills/creativity/scripts/search.py "<campaign_type> <audience> <industry>" --creative-brief [-c "Campaign Name"]
```

This command:
1. Searches 5 domains in parallel (style, platform, voiceover, music, reasoning)
2. Applies reasoning rules from `creative-reasoning.csv` to select best matches
3. Returns complete brief: style, platform specs, voiceover, music, effects
4. Includes anti-patterns to avoid

**Example:**
```bash
python3 .claude/skills/creativity/scripts/search.py "SaaS product launch gen z" --creative-brief -c "App Launch Campaign"
```

### Step 3: Supplement with Detailed Searches (as needed)

After getting the creative brief, use domain searches for additional details:

```bash
python3 .claude/skills/creativity/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

**When to use detailed searches:**

| Need | Domain | Example |
|------|--------|---------|
| More style options | `style` | `--domain style "minimalist luxury"` |
| Platform specs | `platform` | `--domain platform "tiktok reels"` |
| Voiceover direction | `voiceover` | `--domain voiceover "authoritative expert"` |
| Music recommendations | `music` | `--domain music "ambient electronic"` |
| Campaign guidance | `reasoning` | `--domain reasoning "e-commerce conversion"` |

### Step 4: Load Reference Details (as needed)

For detailed implementation, load relevant references:

| Reference | Content | Use When |
|-----------|---------|----------|
| [creative-styles-part1.md](references/creative-styles-part1.md) | Styles 1-25 with keywords, colors, effects | Selecting visual direction |
| [creative-styles-part2.md](references/creative-styles-part2.md) | Styles 26-55 with keywords, colors, effects | Selecting visual direction |
| [color-psychology.md](references/color-psychology.md) | Color meanings, combinations, applications | Choosing color palette |
| [voiceover-styles.md](references/voiceover-styles.md) | 5 VO categories with delivery specs | Video/audio content |
| [audio-music.md](references/audio-music.md) | Music trends, sonic branding | Video content, ads |
| [visual-trends.md](references/visual-trends.md) | 2025-26 design trends | Modern visual direction |

---

## Search Reference

### Available Domains

| Domain | Use For | Example Keywords |
|--------|---------|------------------|
| `style` | Visual aesthetics | minimalist, ugc, cinematic, retro, luxury |
| `platform` | Channel specs | tiktok, instagram, youtube, linkedin |
| `voiceover` | VO direction | conversational, authoritative, playful |
| `music` | Audio direction | ambient, upbeat, orchestral, trending |
| `reasoning` | Campaign strategy | product launch, brand awareness, gen z |

---

## Example Workflow

**User request:** "Create a TikTok campaign for Gen Z SaaS product launch"

### Step 1: Analyze Requirements
- Campaign type: Product launch
- Audience: Gen Z
- Industry: SaaS
- Platform: TikTok

### Step 2: Generate Creative Brief (REQUIRED)

```bash
python3 .claude/skills/creativity/scripts/search.py "gen z saas product tiktok" --creative-brief -c "SaaS Launch"
```

### Step 3: Supplement with Detailed Searches (as needed)

```bash
# Get TikTok-specific guidelines
python3 .claude/skills/creativity/scripts/search.py "tiktok" --domain platform

# Get Gen Z style options
python3 .claude/skills/creativity/scripts/search.py "gen z authentic raw" --domain style
```

---

## Output Formats

```bash
# ASCII box (default) - best for terminal display
python3 .claude/skills/creativity/scripts/search.py "e-commerce launch" --creative-brief

# Markdown - best for documentation
python3 .claude/skills/creativity/scripts/search.py "e-commerce launch" --creative-brief -f markdown
```

---

## Key Stats

- Humor increases recall 33% (only 33% of ads use it)
- Color drives 85% purchase decisions
- Brand recognition +80% with consistent colors
- UGC: 28% higher engagement, 4x CTR, 50% lower CPA

---

## Platform Quick Specs

| Platform | Ratio | Length | Hook | Style Note |
|----------|-------|--------|------|------------|
| TikTok | 9:16 | 15-60s | 3s | Raw, trending sounds |
| Instagram Reels | 9:16 | 15-90s | 3s | Polished-authentic |
| YouTube | 16:9 | 30s-10m | 30s | High production |
| LinkedIn | 1:1, 4:5 | 30s-2m | 5s | Professional, value-first |
| Stories | 9:16 | 15s | 1s | Immediate hook, swipe CTA |

---

## Pre-Production Checklist

- [ ] Brand guidelines reviewed
- [ ] Audience persona confirmed
- [ ] Creative style approved from search results
- [ ] Platform specs verified
- [ ] Success metrics defined
- [ ] Hook in first 3 seconds
- [ ] Sound-off optimized (captions)
- [ ] Mobile-first designed
- [ ] A/B test variables identified
