---
name: youtube-description
description: Write YouTube video descriptions optimized for SEO and conversion. Creates hook-driven descriptions with timestamps, CTAs, and hashtags. Use when publishing a new YouTube video or when user asks for a "YouTube description", "video description", or needs to write copy for a YouTube upload.
---
## Load Context First

Before executing this skill, read the following files from the project folder if they exist:

1. **USER.md** — who the user is, how they think, how they work, what they care about
2. **BUSINESS.md** — their business, products, positioning, brand voice, content strategy
3. **ICP.md** — their ideal customer, their language, their fears, what makes them buy
4. **Voice skill** — if the user has a voice skill installed globally in Claude Desktop, it will be auto-loaded. Do not attempt to read it as a file path.
5. Any additional context provided by the user in this session

Use all of this context silently to inform everything you produce. Do not reference or summarize the files unless asked.

---

# YouTube Description

Generate high-converting YouTube video descriptions that improve discoverability and drive action.

## Context Guidelines

- **Business context, audience, and other details:** Refer to any context profiles provided

---

## When to Use

- User is publishing a new YouTube video
- User asks for a "YouTube description" or "video description"
- User has a video transcript or outline and needs upload copy
- User mentions timestamps or YouTube SEO

---

## Description Philosophy

YouTube descriptions serve multiple purposes:
1. **Hook viewers** who read before clicking
2. **Improve SEO** through keywords and context
3. **Drive action** with links and CTAs
4. **Provide value** with timestamps and resources

Most descriptions fail by being either too generic or too long. The goal is punchy, scannable, and action-driving.

---

## Input Analysis

When you receive input, extract:

1. **Video topic** — What's being taught or shown?
2. **Key hook** — What's the surprising/provocative angle?
3. **Who it's for** — Target audience roles
4. **What they'll learn/get** — Specific outcomes
5. **Timestamps** — Section breakdowns (if provided)
6. **Resources mentioned** — Links, downloads, paid content
7. **CTAs** — What action should viewers take?

---

## Output Structure

```markdown
[LINKS SECTION - User's key links and CTAs]
---

[HOOK STATEMENT - One punchy line that stops the scroll]

[MAIN DESCRIPTION - 2-3 sentences covering what, who, outcome]

[WHERE TO GET RESOURCES - If applicable]

⏳ TIMESTAMPS

0:00 [Section name]
[Continue for all sections...]

[HASHTAGS - 10-15 relevant tags]
```

---

## Section Guidelines

### Links Section

Start with the user's most important links:
- Newsletter signup
- Website or product
- Free resource mentioned in video
- Social media handles

Format:
```
📬 [Primary CTA link]
🔗 [Secondary link]
📥 [Download/resource link]

[Optional: Brief note about where resources live]
---
```

### Hook Statement

**Goal:** Stop the scroll. Challenge an assumption.

**Format:** One punchy line that reframes what people think.

**Examples:**
- "Most people do [X] completely wrong."
- "This changed everything about how I [approach topic]."
- "You don't need [common thing]. You need [better thing]."

**Rules:**
- One sentence
- Challenges common belief or creates curiosity
- No fluff or setup
- No "In this video..." openings

### Main Description

**Structure:**
1. "In this [video type], I'm showing you [specific thing]—and [what you're giving them]."
2. "This is for [roles], and anyone who wants to [outcome] without [pain]."
3. Brief mention of where resources live (if applicable).

**Keep it tight:** 2-3 sentences max after the hook.

### Timestamps Section

**Format:**
```
⏳ TIMESTAMPS

0:00 Intro
1:11 [Section name]
3:46 [Section name]
...
```

**Rules:**
- Always include `⏳ TIMESTAMPS` header
- Start with `0:00 Intro`
- Use sentence case for section names
- Keep names short and scannable
- Include all major sections from the video

### Hashtags

**Format:** Single line at the end, 10-15 tags

**Include mix of:**
- Topic tags (specific to video subject)
- Platform/tool tags (if applicable)
- Audience tags (who this is for)
- Broader category tags

**Rules:**
- All lowercase
- No spaces in tags
- Relevant to actual content
- Don't overstuff with generic tags

---

## Quality Checklist

**Links:**
- [ ] Primary CTA link included
- [ ] All mentioned resources linked
- [ ] Links are functional

**Hook:**
- [ ] One sentence
- [ ] Challenges assumption or creates curiosity
- [ ] No fluff

**Main Description:**
- [ ] Clear "In this [type]" opening
- [ ] Specific audience listed
- [ ] Outcome + anti-pain point mentioned
- [ ] Resource location mentioned (if applicable)

**Timestamps:**
- [ ] Header with emoji included
- [ ] Starts with 0:00 Intro
- [ ] All major sections covered
- [ ] Sentence case, scannable

**Hashtags:**
- [ ] 10-15 tags
- [ ] Mix of specific and broader tags
- [ ] Single line
- [ ] All relevant to content

---

## Common Mistakes

| Mistake | Wrong | Right |
|---------|-------|-------|
| Weak hook | "In this video I'll show you..." | "[Topic] isn't what you think." |
| Too long | Multiple paragraphs of context | 2-3 tight sentences after hook |
| Generic audience | "content creators" | "newsletter writers, YouTubers, marketers" |
| Missing timestamps | No section breakdown | Full timestamp list with emoji header |
| Wrong hashtag format | #YouTube #Video #Content | #youtubestrategy #videomarketing #contentcreator |
| No CTA | Just description text | Clear links and action steps |

---

## Example Output

```
📬 Subscribe to my newsletter → [link]
🚀 Get the free starter kit → [link]

Resources mentioned in this video are available for subscribers.
---
Everyone's overcomplicating this.

In this tutorial, I'm breaking down the exact system I use for [topic]—and I'm giving you every template and resource you need to do it yourself.

This is for [role 1], [role 2], [role 3], and anyone who wants to [outcome] without [common struggle].

The starter kit and all resources are linked above.

⏳ TIMESTAMPS

0:00 Intro
1:30 Why most approaches fail
4:15 The core framework
8:30 Setting up your system
15:00 Live walkthrough
22:45 Common mistakes to avoid
28:00 Next steps and resources

#[topic] #[tool] #[audience] #[category] #[subtopic] #[platform] #[skill] #[approach] #[niche] #tutorial
```

---

## SEO Tips

- **First 150 characters matter most** — They show in search results
- **Include primary keyword** in first sentence
- **Timestamps improve watch time** — YouTube rewards this
- **Hashtags are searchable** — Use them strategically
- **Links drive traffic** — But don't spam
