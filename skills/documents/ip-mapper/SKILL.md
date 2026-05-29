---
name: ip-mapper
description: Map all of a client's intellectual property into one structured document — recurring stories, signature opinions, frameworks, owned phrases, and known topics. Organized into categories with tags. Use when user wants to "map IP", "catalog client stories", "document frameworks", or build an intellectual property inventory.
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

# IP Mapper

**Purpose:** Create a comprehensive inventory of a client's intellectual property — every story they tell, opinion they hold, framework they teach, phrase they own, and topic they're known for. This becomes the content engine's source material.

## When to Activate

Use this skill when:
- User wants to map or catalog a client's intellectual property
- User mentions "IP map", "content inventory", "story bank", or "framework catalog"
- User wants to document everything a client knows and teaches
- User is setting up a ghostwriting client's content system

## Why This Matters

Most ghostwriters struggle because they run out of things to say. An IP map solves this by:
- Cataloging every reusable story, opinion, and framework
- Creating a searchable library of content raw material
- Ensuring consistency (the same story told the same way every time)
- Revealing content gaps (topics they should own but haven't addressed)

## Required Input

Ask the user for ANY of:
- Client interviews or call transcripts
- Existing content (articles, posts, newsletters, videos)
- List of topics they teach or talk about
- Their course curriculum or workshop outlines
- Podcast appearances or speaking engagements
- Social media posts that performed well

The more input, the richer the map. But even a single interview can produce a useful starting map.

## IP Categories

### Category 1: Recurring Stories & Anecdotes
Stories the client tells repeatedly — their origin story, client wins, failures, turning points, "aha moments."

**For each story, capture:**
- **Story name** (short label for reference)
- **Summary** (2-3 sentences)
- **Key characters** (who's involved)
- **Lesson/moral** (what it teaches)
- **Best used for** (what type of content it fits)
- **Tags** (topics it relates to)

### Category 2: Signature Opinions & Hot Takes
Beliefs and positions the client holds that differentiate them from others in their space.

**For each opinion, capture:**
- **The opinion** (stated clearly in their voice)
- **The conventional wisdom it challenges**
- **Their evidence/reasoning**
- **Strength level** (hill they'd die on vs. leaning toward)
- **Tags**

### Category 3: Frameworks & Methodologies
Systems, processes, and mental models the client teaches.

**For each framework, capture:**
- **Framework name**
- **What it solves** (the problem it addresses)
- **Components** (the steps or elements)
- **How they explain it** (their typical teaching flow)
- **Visual representation** (if they use one)
- **Tags**

### Category 4: Owned Phrases & Language
Specific phrases, terms, or metaphors the client uses repeatedly that are uniquely theirs.

**For each phrase, capture:**
- **The phrase**
- **What it means** (in context)
- **When they use it**
- **Origin** (if known)

### Category 5: Topic Authority Areas
Topics the client is known for and should consistently create content about.

**For each topic, capture:**
- **Topic name**
- **Authority level** (expert / experienced / emerging)
- **Sub-topics** they cover within it
- **Related stories** (link to Category 1)
- **Related frameworks** (link to Category 3)
- **Content gap?** (have they written about this enough?)

## Output Format

```markdown
# IP Map: [Client Name]

> Last updated: [Date]
> Source material: [What was analyzed]

---

## Overview

**Total inventory:**
- Stories & Anecdotes: [X]
- Signature Opinions: [X]
- Frameworks: [X]
- Owned Phrases: [X]
- Topic Areas: [X]

---

## 📖 Stories & Anecdotes

### [Story Name]
- **Summary:** [2-3 sentences]
- **Characters:** [Who's involved]
- **Lesson:** [What it teaches]
- **Best for:** [Content type — newsletter intro, social proof, case study, etc.]
- **Tags:** [topic1, topic2]

### [Story Name]
[Continue for all stories...]

---

## 🔥 Signature Opinions

### "[Opinion stated clearly]"
- **Challenges:** [The conventional wisdom it opposes]
- **Evidence:** [Their reasoning]
- **Strength:** [Core belief / Strong lean / Emerging view]
- **Tags:** [topic1, topic2]

### "[Opinion]"
[Continue for all opinions...]

---

## 🔧 Frameworks & Methodologies

### [Framework Name]
- **Solves:** [Problem it addresses]
- **Components:**
  1. [Step/Element 1]
  2. [Step/Element 2]
  3. [Step/Element 3]
- **Teaching flow:** [How they typically explain it]
- **Tags:** [topic1, topic2]

### [Framework Name]
[Continue for all frameworks...]

---

## 💬 Owned Phrases

| Phrase | Meaning | When Used |
|--------|---------|-----------|
| "[Phrase]" | [What it means] | [Context] |
| "[Phrase]" | [What it means] | [Context] |

---

## 🎯 Topic Authority Areas

### [Topic Name]
- **Authority level:** [Expert / Experienced / Emerging]
- **Sub-topics:** [List]
- **Related stories:** [Story names from above]
- **Related frameworks:** [Framework names]
- **Content gap:** [Yes/No — have they covered this enough?]

### [Topic Name]
[Continue for all topics...]

---

## Content Opportunities

Based on this IP map, the biggest untapped content opportunities are:

1. **[Opportunity]** — [Why: untold story, underdeveloped framework, etc.]
2. **[Opportunity]** — [Why]
3. **[Opportunity]** — [Why]
```

## Quality Checklist

- [ ] All 5 categories populated (even if some are thin)
- [ ] Stories have clear labels, summaries, and lessons
- [ ] Opinions are stated in the client's voice (not sanitized)
- [ ] Frameworks have all components listed
- [ ] Owned phrases captured with context
- [ ] Topic areas include content gap analysis
- [ ] Content opportunities identified
- [ ] Everything sourced from actual input (not fabricated)
- [ ] Tags applied for cross-referencing
- [ ] Output is organized and searchable
