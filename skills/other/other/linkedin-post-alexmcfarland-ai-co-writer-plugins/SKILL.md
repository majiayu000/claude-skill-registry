---
name: linkedin-post
description: Write a long-form LinkedIn post (300-600 words). Hook line, personal story or observation, 3-5 lessons/insights, clear CTA. Professional but human — no corporate speak, no emoji spam. Use when user wants a "LinkedIn post", "LinkedIn content", or wants to share insights on LinkedIn.
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

# LinkedIn Post Writer

**Purpose:** Write long-form LinkedIn posts (300-600 words) that build authority, drive engagement, and feel human. LinkedIn rewards posts that are professional but personal — real stories, genuine insights, and clear value.

## When to Activate

Use this skill when:
- User wants to write a LinkedIn post
- User mentions "LinkedIn content" or "LinkedIn engagement"
- User has an insight, story, or lesson to share on LinkedIn
- User wants professional social content

## LinkedIn-Specific Rules

**What works on LinkedIn:**
- Personal stories with professional lessons
- Tactical advice people can use at work
- Vulnerable admissions that feel authentic
- Contrarian takes on industry norms
- Data-backed observations

**What doesn't work:**
- Corporate announcements written in third person
- Emoji-heavy formatting (🚀🔥💡 every line)
- Humble-bragging disguised as gratitude
- "Agree?" as a CTA
- Regurgitated motivational quotes

**Character limit:** 3,000 characters. Posts over ~150 words get truncated with "...see more" — the hook MUST compel the click.

## Structure

### Line 1: The Hook (Pattern Interrupt)

The first 1-2 lines must stop the scroll. They appear above the "...see more" fold.

**Hook patterns:**

1. **Bold declaration**: "I turned down a $200K offer. Here's why."
2. **Unexpected confession**: "I've been lying to my clients."
3. **Counterintuitive insight**: "The worst business advice I ever followed made me the most money."
4. **Specific result**: "3 months ago I changed one thing. Revenue doubled."
5. **Pattern break**: A single short sentence that creates curiosity.
6. **Question**: "What's the one thing you'd change about how you work?" (use sparingly)

**Rules:**
- Must work above the "see more" fold
- No greetings ("Hi LinkedIn!", "Happy Monday!")
- No emojis in the hook line
- Be specific — vague hooks get scrolled past

### Middle: The Story/Observation (150-350 words)

**Option A: Personal Story**
- Set the scene (1-2 sentences)
- The challenge or turning point
- What you did or realized
- Bridge to lessons

**Option B: Professional Observation**
- What you've noticed in your industry
- Why it matters
- The implication for your audience

**Option C: Tactical Breakdown**
- The problem your audience faces
- Your approach to solving it
- Step-by-step or principle-by-principle

**Formatting rules for LinkedIn:**
- Short paragraphs (1-3 sentences max)
- Line break between every paragraph
- Use white space aggressively — LinkedIn is mobile-first
- Bold text for key phrases (sparingly)
- Bullets for lists, but not entire posts

### The Insights (3-5 key takeaways)

After the story/observation, distill the lessons:

**Format:**
```
Here's what I learned:

1. [Insight as a bold statement]
[1-2 sentences of context]

2. [Insight as a bold statement]
[1-2 sentences of context]

3. [Insight as a bold statement]
[1-2 sentences of context]
```

**Rules:**
- Each insight should stand alone
- Be specific and actionable
- No generic wisdom ("work hard", "be consistent")

### The CTA (Final 1-2 lines)

**Effective CTAs for LinkedIn:**
- "What's your experience with [topic]?" (engagement driver)
- "If this resonated, follow me for more on [topic]" (growth driver)
- "I write about this every week → [newsletter link]" (conversion driver)
- "Repost this if you know someone who needs to hear it" (reach driver)

**CTA rules:**
- ONE call to action only
- Make it feel natural (not "SMASH that like button")
- Pull links/handles from context files
- Match the CTA to the user's current goal

## Output Format

```
# LinkedIn Post: [Topic]

**Word count:** [X] words (~[X] characters)
**Post type:** [Story / Observation / Tactical / Contrarian]

---

[Hook line — 1-2 sentences above the fold]

[Body — story, observation, or breakdown]

[3-5 numbered insights with brief context]

[CTA — 1-2 lines]

---

## Alternative Hooks

1. [Alternative hook option]
2. [Alternative hook option]
3. [Alternative hook option]
```

## Quality Checklist

- [ ] Hook works above the "...see more" fold
- [ ] 300-600 words (under 3,000 characters)
- [ ] Short paragraphs with line breaks between each
- [ ] No emoji spam (0-2 emojis max, if any)
- [ ] No corporate speak or LinkedIn clichés
- [ ] 3-5 specific, actionable insights
- [ ] One clear CTA at the end
- [ ] Reads well on mobile (the primary LinkedIn device)
- [ ] Voice matches context profiles
- [ ] Feels human and authentic, not performative

## LinkedIn Clichés to Avoid

- "I'm humbled to announce..."
- "Agree? 👇"
- "Let that sink in."
- 🚀🔥💡 on every other line
- "Who else?" / "Am I right?"
- Starting with "So..." or "Hey LinkedIn family!"
- "Thoughts?" as the entire CTA
- Any post that's really just a humble-brag wrapped in gratitude
