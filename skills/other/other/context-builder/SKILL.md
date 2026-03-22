---
name: context-builder
description: Build BUSINESS.md and ICP.md context files for a ghostwriting client from raw info, notes, a website, or a call transcript. Asks clarifying questions if info is missing. Use when user wants to "build context files", "set up a new client", or create BUSINESS.md and ICP.md from scratch.
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

# Context Builder

**Purpose:** Create BUSINESS.md and ICP.md files for a ghostwriting client from raw information. These files power every other skill — they're the foundation of the entire co-writer system.

## When to Activate

Use this skill when:
- User wants to build context files for a new client
- User says "set up a new client" or "build context profiles"
- User provides raw info (website, notes, transcript) and needs it structured
- User needs BUSINESS.md and/or ICP.md created

## Required Input

Accept ANY of these input types:
- Website URL
- Call transcript or notes
- Raw text description of the business
- Existing marketing materials
- Social media profiles
- Combination of the above

## Process

### Step 1: Extract Information

From whatever the user provides, extract and organize:

**For BUSINESS.md:**
- Business name and entity type
- What they do (elevator pitch)
- Products/services offered
- Target market
- Positioning statement
- Key differentiators
- Brand voice description
- Content strategy (if any)
- Social links and domains
- Revenue model
- Origin story or founding context

**For ICP.md:**
- Who their ideal customer is (demographics + psychographics)
- Common roles/titles
- The problems they face
- Their fears and frustrations
- Their aspirations and desired outcomes
- What convinces them to buy
- Common objections
- Language they use (actual words and phrases)
- Where they hang out online
- What they've already tried

### Step 2: Identify Gaps

After extraction, identify what's missing. Ask targeted questions — not a wall of 20 questions, but the 3-5 most important gaps.

**Priority gaps (ask about these first):**
1. Target audience clarity (who specifically?)
2. Key differentiator (what makes them different?)
3. Products/pricing (what do they sell and for how much?)
4. ICP pain points (what problems does their customer have?)
5. Brand voice (how do they want to sound?)

### Step 3: Generate Files

## BUSINESS.md Template

```markdown
# BUSINESS.md — [Business Name]

> Last updated: [Date]

## Overview
- **Business name:** [Name]
- **Type:** [Personal brand / Agency / SaaS / etc.]
- **Founded:** [Year or context]
- **Location:** [If relevant]

## What They Do
[2-3 sentence description of the business]

## Products & Services

### [Product/Service 1]
- **Type:** [Product type]
- **Price:** [Pricing]
- **Description:** [What it is and who it's for]

### [Product/Service 2]
[Continue for all offerings]

## Positioning
**One-liner:** [How they describe themselves in one sentence]
**Differentiators:**
- [What makes them different #1]
- [What makes them different #2]
- [What makes them different #3]

## Brand Voice
- **Tone:** [Formal/Casual/Professional/Edgy/etc.]
- **Personality traits:** [3-5 adjectives]
- **They sound like:** [Description of their communication style]
- **They never sound like:** [What to avoid]

## Content Strategy
- **Primary platform:** [Where they publish most]
- **Content types:** [Newsletter, social, video, etc.]
- **Posting cadence:** [How often]
- **Content themes:** [What they talk about]

## Online Presence
| Platform | URL |
|----------|-----|
| Website | [URL] |
| Newsletter | [URL] |
| Social | [URLs] |

## Revenue Model
[How the business makes money — subscriptions, one-time, retainers, etc.]
```

## ICP.md Template

```markdown
# ICP.md — Ideal Customer Profile

> For: [Business Name]
> Last updated: [Date]

## Who They Are
**The [Descriptor]** — [One sentence capturing who this person is]

### Demographics
- **Roles:** [Job titles, positions]
- **Industry:** [Fields they work in]
- **Experience level:** [Junior/Mid/Senior/Founder]
- **Technical comfort:** [Description]
- **Income range:** [If relevant]

### Psychographics
- **Values:** [What they care about]
- **Mindset:** [How they think about their work]
- **Motivation:** [What drives them]

## Their Problems
1. [Specific problem #1 — described in their language]
2. [Specific problem #2]
3. [Specific problem #3]
4. [Specific problem #4]
5. [Specific problem #5]

## Their Fears
- [Fear #1]
- [Fear #2]
- [Fear #3]

## Their Aspirations
- [What they want #1]
- [What they want #2]
- [What they want #3]

## What They've Already Tried
- [Common solution they've attempted]
- [Why it didn't work]

## The Core Shift
**From:** [Where they are now — described in their words]
**To:** [Where they want to be — the transformation]

## What Convinces Them to Buy
- [Buying trigger #1]
- [Buying trigger #2]
- [Buying trigger #3]

## Common Objections
- **"[Objection 1]"** → [How to address it]
- **"[Objection 2]"** → [How to address it]
- **"[Objection 3]"** → [How to address it]

## Their Language
**Words they use:**
- [Actual phrases and words the ICP uses to describe their problems]

**Words they respond to:**
- [Language that resonates with them]

**Words that turn them off:**
- [Language that feels wrong or corporate to them]
```

## Quality Checklist

- [ ] BUSINESS.md covers all major sections
- [ ] ICP.md includes problems, fears, AND aspirations
- [ ] Language section uses actual words the ICP would use
- [ ] Objections are real (not strawmen)
- [ ] Missing info is flagged with [TBD] rather than guessed
- [ ] Files are ready to save and use immediately
- [ ] Information comes from user input (not fabricated)
- [ ] Follow-up questions are prioritized (most important gaps first)
