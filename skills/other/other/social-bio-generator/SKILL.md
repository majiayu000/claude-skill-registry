---
name: social-bio-generator
description: Generates multiple high-converting bio options for LinkedIn, X (Twitter), and Instagram based on user context. Creates platform-optimized bios with proper character limits, formatting, and conversion focus. Use when user mentions "write my bio", "LinkedIn headline", "Twitter bio", "Instagram bio", or wants to optimize social media profiles.
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

# Social Media Bio Generator

**Purpose:** Generate multiple high-converting bio options for LinkedIn, X (Twitter), and Instagram that attract the right audience and drive profile actions.

## When to Activate

Use this skill when:
- User asks to write or optimize their social media bio
- User mentions "LinkedIn headline", "Twitter bio", or "Instagram bio"
- User wants to update their professional profile descriptions
- User needs bios for multiple platforms

## Core Principles

1. **No Fabrication**: Never create personal stories, achievements, or metrics unless explicitly provided
2. **Multiple Options**: Generate 3-5 bio variations per platform
3. **Platform Optimization**: Strictly adhere to character limits and best practices
4. **Conversion Focus**: Every bio should clearly communicate value and encourage action

## Workflow

### Step 1: Gather Information

**If context profiles exist:** Use them for business details and audience info. Ask only for:
1. Which platforms need bios?
2. Primary goal for these profiles? (leads, opportunities, brand awareness)
3. Call-to-action preference? (newsletter, website, booking)

**If no context profiles:** Ask for: current role, target audience, expertise areas, unique value proposition, key achievements, and preferred tone.

### Step 2: Generate Platform-Specific Bios

## LinkedIn Bios

### Headline (220 characters max)
**Formula:** [What You Do] | [Who You Help] | [Unique Value/Differentiator]

Generate 3-5 variations:
- Focus on helping specific audience achieve measurable outcome
- Lead with biggest achievement or credential
- Emphasize unique methodology or approach
- Highlight transformation or journey
- Focus on mission/vision

**Requirements:** Start with "I help [audience] achieve [outcome]" when appropriate. Include relevant keywords. Avoid job-title-only headlines.

### About Section (2,600 characters max)
1. **Opening Hook** (1-2 sentences) — Compelling mission statement
2. **Background** (2-3 sentences) — Professional journey highlights
3. **Social Proof** (2-4 sentences) — Achievements and results
4. **Current Focus** (2-3 sentences) — What you do now and for whom
5. **CTA** (1-2 sentences) — Clear next step aligned with goals

## X (Twitter) Bios (160 characters STRICT limit)

**Essential components:** Memorable descriptor, current role/project, what followers gain, one proof point, strategic emoji (1-3 max).

Generate 3-5 variations:
- Moniker + Mission + Topics format
- Achievement-first with follower benefit
- Action-oriented "Building/Creating X" focus
- Topic expertise with credibility marker
- Minimalist high-impact statement

**Critical:** Count characters carefully. 160 is the hard limit.

## Instagram Bios (150 characters STRICT limit)

**Essential components:** Clear identity/title, benefit offered, CTA with directional emoji (👇), strategic line breaks, 3-5 emojis max.

Generate 3-5 variations using line breaks for scannability.

**Critical:** Count characters carefully. 150 is the hard limit.

## Output Format

```
# Social Media Bio Options

---

## LinkedIn Bio Options

### Option 1: [Label]
**Headline** (XXX/220 chars): [Text]
**About Section**: [Full text]

### Option 2: [Label]
[Continue for 3-5 options...]

---

## X (Twitter) Bio Options

### Option 1: [Label]
[Bio text]
Character count: XX/160

[Continue for 3-5 options...]

---

## Instagram Bio Options

### Option 1: [Label]
[Bio with line breaks]
Character count: XX/150

[Continue for 3-5 options...]

---

## Recommendations
**LinkedIn**: Option [X] — [reasoning]
**Twitter**: Option [X] — [reasoning]
**Instagram**: Option [X] — [reasoning]
```

## Quality Checklist

- [ ] All character counts within platform limits
- [ ] No fabricated achievements
- [ ] Clear value proposition in each version
- [ ] CTAs align with user's stated goals
- [ ] Keywords naturally integrated
- [ ] Specific (not vague)
- [ ] Avoid generic phrases ("passionate about", "love what I do")
- [ ] 3-5 options per platform with recommendation
