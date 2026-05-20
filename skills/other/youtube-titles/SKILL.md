---
name: youtube-titles
description: Generate click-worthy YouTube titles optimized for CTR without being clickbait. Creates multiple title variations using proven patterns. Use when user needs "YouTube title", "video title", or wants title options for their content.
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

# YouTube Titles

Generate high-CTR YouTube titles that make people click without misleading them.

## Context Guidelines

- **Business context, audience, and other details:** Refer to any context profiles provided

---

## When to Use

- User needs a title for a YouTube video
- User asks for "title ideas" or "YouTube title"
- User wants to test different title angles
- User mentions wanting better CTR or more clicks

---

## Title Philosophy

### The Click Equation

**Click = Curiosity + Relevance + Credibility**

- **Curiosity:** They need to know more
- **Relevance:** It's clearly about something they care about
- **Credibility:** They believe you can deliver

All three must be present. Missing one = weak title.

### Clickbait vs. Click-Worthy

**Clickbait:** Promise something the video doesn't deliver
**Click-worthy:** Create curiosity about something the video actually covers

The difference: Can you deliver on the title's implicit promise?

---

## Title Patterns That Work

### 1. The Challenge Pattern
Challenge what they think they know.

- "Stop [Common Action] - Do This Instead"
- "[Thing] is Broken. Here's the Fix."
- "Why [Popular Approach] Doesn't Work"
- "The [Topic] Advice Everyone Gets Wrong"

### 2. The Result Pattern
Lead with an outcome or transformation.

- "I [Did Thing] and [Result Happened]"
- "How I [Achieved Result] in [Timeframe]"
- "[X] Changed How I [Do Thing]"
- "From [Before State] to [After State]"

### 3. The Discovery Pattern
Reveal something they don't know.

- "The [Hidden/Secret/Real] Reason [Thing Happens]"
- "What [Experts/Pros] Know About [Topic] That You Don't"
- "[Number] Things I Wish I Knew Before [Starting Thing]"
- "The Truth About [Topic]"

### 4. The Specificity Pattern
Be surprisingly specific.

- "The Exact [Process/Method] I Use to [Result]"
- "My [Specific Number] Step System for [Outcome]"
- "[Specific Tool/Thing] That [Specific Benefit]"
- "How to [Do Thing] in [Specific Timeframe]"

### 5. The Comparison Pattern
Frame choices for them.

- "[Option A] vs [Option B] - Which is Better?"
- "I Tested [X Things] So You Don't Have To"
- "The Best [Category] for [Specific Use Case]"
- "[This] is Better Than [That] for [Purpose]"

### 6. The Story Pattern
Tease a narrative.

- "I [Did Risky/Bold Thing] and Here's What Happened"
- "Why I Quit [Thing] After [Timeframe]"
- "The [Mistake/Lesson] That [Changed Everything]"
- "What Happened When I [Tried/Stopped/Started Thing]"

---

## Title Optimization Rules

### Length
- **Ideal:** 40-60 characters
- **Maximum:** 70 characters (gets truncated on mobile)
- Front-load important words

### Capitalization
- Title Case or Sentence Case (pick one, be consistent)
- ALL CAPS sparingly, for one word max
- Never all lowercase

### Numbers
- Odd numbers often outperform even
- Specific numbers beat round numbers (17 vs 20)
- "7" and "3" historically perform well
- But don't force it if unnatural

### Power Words
Use sparingly but effectively:
- Urgency: Now, Today, Quick, Fast
- Exclusivity: Secret, Hidden, Little-Known
- Emotion: Shocking, Surprising, Amazing
- Results: Proven, Exact, Complete

### What to Avoid
- Vague titles ("My Thoughts on X")
- Questions that can be answered "no"
- Excessive punctuation!!!???
- Emojis in titles (save for thumbnails)
- Starting with "How to" every time

---

## Input Analysis

When you receive input, identify:

1. **Core topic** — What's the video actually about?
2. **Key insight** — What's the main thing they'll learn/get?
3. **Viewer pain** — What problem does this solve?
4. **Transformation** — Before/after state
5. **Unique angle** — What makes your take different?
6. **Proof points** — Numbers, results, specifics to include

---

## Output Format

Generate 10+ title options across different patterns:

```markdown
# Title Options for: [Topic]

## Challenge Titles
1. [Title]
2. [Title]
3. [Title]

## Result Titles
1. [Title]
2. [Title]
3. [Title]

## Discovery Titles
1. [Title]
2. [Title]

## Specificity Titles
1. [Title]
2. [Title]

## Other Strong Options
1. [Title]
2. [Title]

---

## Recommended Top 3

Based on the content, these are likely to perform best:

1. **[Title]** — Why: [Brief reasoning]
2. **[Title]** — Why: [Brief reasoning]
3. **[Title]** — Why: [Brief reasoning]

---

## A/B Test Suggestions

Test these pairs against each other:
- [Title A] vs [Title B] — Testing: [variable being tested]
```

---

## Quality Checklist

**Clarity:**
- [ ] Viewer immediately knows the topic
- [ ] No confusion about what they'll get
- [ ] Front-loaded with important words

**Curiosity:**
- [ ] Creates a knowledge gap
- [ ] Makes them want to click
- [ ] Doesn't give away everything

**Credibility:**
- [ ] Believable claims
- [ ] Specific where possible
- [ ] Matches the actual content

**Technical:**
- [ ] Under 60 characters (ideal)
- [ ] Important words not truncated on mobile
- [ ] Consistent capitalization

---

## Common Mistakes

| Mistake | Weak Title | Strong Title |
|---------|------------|--------------|
| Too vague | "My Morning Routine" | "The 5 AM Routine That Tripled My Output" |
| No curiosity | "How to Use Notion" | "The Notion Setup I Wish I Knew 2 Years Ago" |
| Buried value | "A Deep Dive Into..." | "Why [Thing] is Costing You [Outcome]" |
| Generic numbers | "10 Tips for..." | "The 3 Things That Actually Matter for..." |
| No stakes | "Understanding X" | "The X Mistake That's Killing Your [Goal]" |
| Question they'll skip | "Do You Know About X?" | "The X Secret [Successful People] Know" |

---

## Niche-Specific Examples

### Tech/Tutorial
- Weak: "Python Tutorial for Beginners"
- Strong: "Learn Python in 60 Minutes - The Only Video You Need"

### Business/Marketing
- Weak: "How to Grow on Social Media"
- Strong: "I Gained 100K Followers Using This One Strategy"

### Lifestyle/Productivity
- Weak: "My Productivity System"
- Strong: "The System That Got Me From Overwhelmed to 4-Hour Workdays"

### Reviews/Comparisons
- Weak: "Product Review"
- Strong: "I Tested 15 [Products] - Only One is Worth Buying"

---

## Working with Video Content

If given a script or outline:

1. **Identify the hook** — What's the most clickable moment?
2. **Find the transformation** — What changes for the viewer?
3. **Extract specifics** — Numbers, timeframes, results
4. **Match the energy** — Title should reflect video tone
5. **Don't overpromise** — Title must match content
