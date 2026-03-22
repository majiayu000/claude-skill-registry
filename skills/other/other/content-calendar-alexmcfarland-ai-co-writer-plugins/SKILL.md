---
name: content-calendar
description: Create a 4-week content calendar from a topic, pillar, or product. Each week includes 1 main piece (video or newsletter), 3 social posts, and 1 Substack note. Output as a clean table. Use when user wants a "content calendar", "posting schedule", "month of content", or "content plan".
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

# Content Calendar Builder

**Purpose:** Create a structured 4-week content calendar from a topic, content pillar, or product focus. Produces a ready-to-execute publishing schedule with specific titles and hooks for every piece.

## When to Activate

Use this skill when:
- User wants a content calendar or posting schedule
- User mentions "plan my month", "content schedule", or "what should I post"
- User has a topic or product they want to build content around
- User needs structure for their content production

## Required Input

- **Topic, pillar, or product** to build the calendar around
- **Platforms** they publish on (or default to: newsletter + LinkedIn + Twitter + Substack Notes)
- **Any upcoming events, launches, or themes** to incorporate

## Weekly Structure

Each week includes:
- **1 Main Piece** — Newsletter or video (the hub content for the week)
- **3 Social Posts** — Platform-native posts (LinkedIn, Twitter, or Instagram)
- **1 Substack Note** — Short-form insight

**Total monthly output:** 4 main pieces + 12 social posts + 4 notes = **20 pieces**

## Process

### Step 1: Define Weekly Themes

Each week gets a sub-topic or angle related to the main topic:
- **Week 1:** Foundation / Introduction / The Problem
- **Week 2:** The Framework / The System / The How
- **Week 3:** Advanced / Nuance / The Mistakes
- **Week 4:** Results / Case Study / What's Next

Adjust themes based on the user's specific topic and goals.

### Step 2: Fill the Calendar

For each content piece, provide:
- **Day** (suggested posting day)
- **Platform**
- **Format** (newsletter, thread, post, note, etc.)
- **Title/Hook** (specific enough to write from)
- **Status** (Not Started — for tracking)

## Output Format

```markdown
# 4-Week Content Calendar

**Topic/Pillar:** [Main topic]
**Date range:** [Start — End]
**Total pieces:** 20

---

## Week 1: [Theme]

| Day | Platform | Format | Title/Hook | Status |
|-----|----------|--------|------------|--------|
| Mon | Newsletter | Thought Leadership | [Specific title] | Not Started |
| Tue | LinkedIn | Post | [Hook line] | Not Started |
| Wed | Twitter/X | Thread | [Hook tweet] | Not Started |
| Thu | Substack | Note | [Opening line] | Not Started |
| Fri | Twitter/X | Standalone | [Tweet idea] | Not Started |

---

## Week 2: [Theme]

| Day | Platform | Format | Title/Hook | Status |
|-----|----------|--------|------------|--------|
| Mon | Newsletter | How-To Guide | [Specific title] | Not Started |
| Tue | LinkedIn | Post | [Hook line] | Not Started |
| Wed | Instagram | Caption | [Hook + concept] | Not Started |
| Thu | Substack | Note | [Opening line] | Not Started |
| Fri | Twitter/X | Thread | [Hook tweet] | Not Started |

---

## Week 3: [Theme]

| Day | Platform | Format | Title/Hook | Status |
|-----|----------|--------|------------|--------|
[Same structure...]

---

## Week 4: [Theme]

| Day | Platform | Format | Title/Hook | Status |
|-----|----------|--------|------------|--------|
[Same structure...]

---

## Monthly Overview

| Week | Theme | Main Piece | Social Pieces | Notes |
|------|-------|-----------|---------------|-------|
| 1 | [Theme] | [Newsletter: Title] | 3 posts | 1 note |
| 2 | [Theme] | [Newsletter: Title] | 3 posts | 1 note |
| 3 | [Theme] | [Newsletter: Title] | 3 posts | 1 note |
| 4 | [Theme] | [Newsletter: Title] | 3 posts | 1 note |

---

## Content Production Notes

- **Best day for newsletters:** [Recommendation based on audience]
- **Social posting times:** [Platform-specific recommendations]
- **Batch production tip:** Write all 4 newsletters first, then derive social content from them
- **Repurposing:** Each main piece should generate at least 3 of the social posts for that week
```

## Quality Checklist

- [ ] 4 full weeks with 5 pieces each (20 total)
- [ ] Each week has a clear theme that builds on the previous
- [ ] Main pieces are specific enough to write from (not "write about topic")
- [ ] Social posts have actual hooks (not placeholder text)
- [ ] Platform variety across the month
- [ ] Content format variety (not all the same type)
- [ ] Themes align with the user's business goals
- [ ] Calendar is realistic for one person to execute
- [ ] Status column included for tracking
- [ ] Production notes included for efficiency
