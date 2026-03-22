---
name: content-map
description: Turn an IP map document into a 4-week content plan with topics, angles, and formats. Each piece maps back to a specific IP asset. Includes posting cadence and platform recommendations. Use when user wants a "content plan", "content calendar from IP", or to plan a month of content from existing intellectual property.
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

# Content Map

**Purpose:** Transform an IP map (or list of topics/assets) into a detailed 4-week content plan. Every piece of content maps back to a specific intellectual property asset, ensuring consistency and strategic coverage.

## When to Activate

Use this skill when:
- User has an IP map and wants a content plan built from it
- User wants a month of content planned out
- User mentions "content map", "content plan from IP", or "month of content"
- User has stories, frameworks, and topics they want to turn into a publishing calendar

## Required Input

- **IP Map** (from the ip-mapper skill) OR a list of topics, stories, and frameworks
- **Platforms** the client publishes on
- **Publishing cadence** (or let this skill recommend one)
- **Any upcoming launches, events, or themes** to plan around

## Process

### Step 1: Analyze Available IP

Review the IP map and categorize assets by:
- **Freshness** — Has this been used recently? Never? Overused?
- **Depth** — Is this a full newsletter topic or a social post?
- **Audience stage** — Does this attract new readers, nurture existing ones, or convert?
- **Platform fit** — Which format/platform suits this asset best?

### Step 2: Build the 4-Week Plan

**Each week follows a content rhythm:**
- **1 Main Piece** — Newsletter, long-form article, or video (the hub content)
- **3 Social Posts** — Platform-native posts derived from or related to the main piece
- **1 Substack Note / Quick Hit** — Short-form insight to keep presence between main pieces

**Weekly theme:** Each week anchors on one IP asset (a framework, story, or topic area) and explores it from multiple angles.

### Step 3: Map Every Piece to IP

Every content piece must trace back to:
- A specific story, framework, opinion, or topic from the IP map
- A clear angle (which content lens: story, observation, contrarian, how-to, etc.)
- A target audience stage (awareness, trust, conversion)

## Output Format

```markdown
# 4-Week Content Map: [Client Name]

> Built from: [IP Map / Topic List]
> Platforms: [List of platforms]
> Date range: [Start — End]

---

## Recommended Cadence

| Platform | Frequency | Best Days |
|----------|-----------|-----------|
| Newsletter | [1x/week] | [Day] |
| LinkedIn | [3x/week] | [Days] |
| Twitter/X | [Daily] | [Any] |
| Substack Notes | [2x/week] | [Days] |
| Instagram | [2-3x/week] | [Days] |

---

## Week 1: [Theme — tied to IP asset]

**IP Focus:** [Framework/Story/Topic being featured]
**Audience Goal:** [Awareness / Trust / Conversion]

| Day | Platform | Format | Title/Hook | IP Asset | Lens |
|-----|----------|--------|------------|----------|------|
| Mon | Newsletter | Thought Leadership | [Title] | [Framework X] | How-to |
| Tue | LinkedIn | Post | [Hook line] | [Framework X] | Observation |
| Wed | Twitter/X | Thread | [Hook tweet] | [Story Y] | Story |
| Thu | Substack | Note | [Opening line] | [Opinion Z] | Contrarian |
| Fri | LinkedIn | Post | [Hook line] | [Framework X] | Lesson |
| Sat | Twitter/X | Standalone | [Tweet] | [Framework X] | Tip |

---

## Week 2: [Theme]

**IP Focus:** [Asset]
**Audience Goal:** [Stage]

| Day | Platform | Format | Title/Hook | IP Asset | Lens |
|-----|----------|--------|------------|----------|------|
[Full table for week 2...]

---

## Week 3: [Theme]

[Same structure...]

---

## Week 4: [Theme]

[Same structure...]

---

## IP Coverage Summary

| IP Asset | Times Used | Platforms | Notes |
|----------|-----------|----------|-------|
| [Framework X] | [3] | Newsletter, LinkedIn, Twitter | Well covered |
| [Story Y] | [1] | Twitter | Could expand to newsletter |
| [Opinion Z] | [2] | Substack, LinkedIn | Strong engagement potential |
| [Topic A] | [0] | — | **Gap — schedule for next month** |

---

## Month-End Review Questions

1. Which pieces got the most engagement?
2. Which IP assets resonated most?
3. What topics should we double down on?
4. What gaps remain in the IP coverage?
5. What new stories or frameworks emerged this month?
```

## Quality Checklist

- [ ] 4 full weeks planned with daily content
- [ ] Every piece maps to a specific IP asset
- [ ] Content lenses vary (not all how-to, not all story)
- [ ] Main piece each week anchors the theme
- [ ] Social content derives from or supports the main piece
- [ ] Platform cadence is realistic for the client
- [ ] Audience stages are balanced (awareness + trust + conversion)
- [ ] IP coverage summary identifies gaps
- [ ] No IP asset overused (variety across weeks)
- [ ] Plan is actionable and ready to execute
