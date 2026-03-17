---
name: linkedin-post-creator
description: |
  Creates high-engagement LinkedIn posts optimized for algorithm reach and audience engagement.
  This skill should be used when users want to write LinkedIn posts, create content for personal branding,
  share technical insights, promote business/products, or craft career-related content. Handles hook writing,
  formatting, CTAs, and provides engagement optimization tips.
---

# LinkedIn Post Creator

Create viral-worthy LinkedIn posts with proven engagement patterns.

## Before Creating Post

| Gather | From |
|--------|------|
| Topic/message | User's request |
| Target audience | Ask if unclear |
| Post type | Detect from context or ask |
| Tone preference | Professional, Conversational, Educational |

## Post Creation Workflow

```
1. Clarify → 2. Hook → 3. Body → 4. CTA → 5. Format → 6. Optimize
```

### Step 1: Clarify Requirements

Ask user (if not clear):
- What's the main message/insight?
- Who's the target audience?
- Any specific goal? (engagement, leads, awareness)

### Step 2: Write the Hook (CRITICAL)

First 2 lines decide if people click "see more". See `references/hooks-library.md`.

**Hook Formulas:**
| Type | Formula | Example |
|------|---------|---------|
| Contrarian | "Unpopular opinion: [statement]" | "Unpopular opinion: Your resume doesn't matter." |
| Story | "[Failure/Success] + Number" | "I failed 47 interviews before landing Google." |
| Question | "Why do [audience] struggle with [problem]?" | "Why do developers mass fail system design?" |
| List | "[Number] things [outcome]" | "5 habits that 10x'd my productivity" |
| Bold claim | "[Surprising statement]" | "Your LinkedIn profile is losing you jobs." |

### Step 3: Write Body

**Structure (choose based on content):**

**Story Format:**
```
[Hook]

[Setup - 2 lines]

[Conflict/Challenge - 2-3 lines]

[Resolution - 2 lines]

[Lesson - 1-2 lines]

[CTA]
```

**List Format:**
```
[Hook]

Here's what I learned:

1. [Point] - [Brief explanation]

2. [Point] - [Brief explanation]

3. [Point] - [Brief explanation]

[Takeaway]

[CTA]
```

**Insight Format:**
```
[Hook]

[Context - why this matters]

[The insight/framework]

[How to apply it]

[CTA]
```

### Step 4: Add Call-to-Action

End with engagement driver. See `references/hooks-library.md#ctas`.

**CTA Types:**
| Goal | CTA Example |
|------|-------------|
| Comments | "What's your experience with this?" |
| Shares | "Share if this resonated." |
| Follows | "Follow for more [topic] insights." |
| Saves | "Save this for later." |
| DMs | "DM me [keyword] for [resource]." |

### Step 5: Format for Readability

See `references/formatting-guide.md` for complete rules.

**Key Rules:**
- Short sentences (max 12 words)
- One idea per line
- Lots of white space
- Use → • 1. for lists
- NO walls of text

### Step 6: Optimize for Algorithm

See `references/algorithm-hacks.md` for full details.

**Quick Checklist:**
- [ ] Hook is compelling (first 2 lines)
- [ ] No external links in post body
- [ ] Ends with question/CTA
- [ ] 1200-1500 characters ideal
- [ ] 0-3 hashtags max (or none)
- [ ] Easy to read on mobile

## Post Types

| Type | Key Elements | Reference |
|------|--------------|-----------|
| Personal Story | Vulnerability, lesson, relatability | `post-templates.md#story` |
| Technical/Tutorial | Steps, code blocks, practical value | `post-templates.md#technical` |
| Career Advice | Experience-based, actionable tips | `post-templates.md#career` |
| Business/Promo | Value-first, soft sell, social proof | `post-templates.md#business` |
| Engagement Bait | Polls, questions, debates | `post-templates.md#engagement` |

## Output Format

When creating a post, provide:

```
## Your LinkedIn Post

[The formatted post ready to copy-paste]

---

**Optimization Tips:**
- Best posting time: [recommendation]
- Suggested hashtags: [if any]
- First comment strategy: [if link needed]
- Expected engagement: [based on type]
```

## What NOT to Do

- No external links in post body (kills reach 50%)
- No more than 3 hashtags
- No generic motivation quotes
- No walls of text
- No asking for likes directly
- No tagging random people

## Reference Files

| File | Content |
|------|---------|
| `references/hooks-library.md` | 50+ hook templates, CTA examples |
| `references/algorithm-hacks.md` | LinkedIn algorithm secrets, timing, reach |
| `references/formatting-guide.md` | Mobile-first formatting rules |
| `references/post-templates.md` | Complete templates for each post type |
