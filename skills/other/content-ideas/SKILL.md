---
name: content-ideas
description: Generate 20 content ideas from 1 topic, each pushed through a different lens — story, observation, contrarian take, listicle, past vs present, present vs future, analysis, teardown, lesson, data/research. Each idea = title + one-sentence hook. Use when user wants "content ideas", "what should I write about", "brainstorm topics", or needs to fill a content calendar.
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

# Content Ideas Generator

**Purpose:** Take one topic and produce 20 distinct content ideas by pushing it through 10 proven content lenses. Each idea comes with a title and one-sentence hook, ready to be turned into any format (newsletter, social post, video, etc.).

## When to Activate

Use this skill when:
- User wants content ideas or brainstorming help
- User mentions "what should I write about" or "content ideas"
- User provides a topic and wants multiple angles
- User needs to fill a content calendar

## The 10 Content Lenses

These lenses are the secret to saying the same thing in 20 different ways. Each lens reframes the topic for a different audience entry point and emotional trigger.

1. **Story** — Personal narrative connected to the topic. "Let me tell you about the time..."
2. **Observation** — What you've noticed about this topic in the real world. "A pattern I keep seeing..."
3. **Contrarian Take** — Argue the opposite of conventional wisdom. "Everyone says X, but actually..."
4. **Listicle** — Numbered collection of insights. "7 things I've learned about..."
5. **Past vs. Present** — How this topic has changed over time. "5 years ago X, today Y..."
6. **Present vs. Future** — Where this topic is heading. "In 2 years, X will be..."
7. **Analysis** — Break down WHY something works or doesn't. "Here's why X actually works..."
8. **Teardown** — Dissect a specific example (good or bad). "Let me break down exactly how..."
9. **Lesson** — What a specific experience taught you. "What [experience] taught me about..."
10. **Data/Research** — Lead with a surprising stat or finding. "[Stat] — here's what it means for..."

## Process

### Step 1: Identify the Core Topic

Extract the single topic from user input. If vague, ask for clarification.

### Step 2: Generate 2 Ideas Per Lens (= 20 Ideas)

For each of the 10 lenses, create 2 distinct content ideas. Each idea gets:
- **Title** — Compelling, specific, could be a subject line or headline
- **Hook** — One sentence that sets up the piece and creates curiosity
- **Best format** — Where this idea works best (newsletter, tweet, thread, LinkedIn, video)

### Step 3: Rank the Top 5

Identify the 5 strongest ideas based on:
- Relevance to the user's audience (from ICP.md)
- Uniqueness (not something everyone else is saying)
- Engagement potential (would you click/read this?)
- Feasibility (does the user have the knowledge to write it?)

## Output Format

```
# 20 Content Ideas: [Topic]

**Core topic:** [Topic]
**Target audience:** [From ICP.md or user input]

---

## 🎯 Top 5 Picks

1. **[Title]** — [Hook] → Best as: [format]
2. **[Title]** — [Hook] → Best as: [format]
3. **[Title]** — [Hook] → Best as: [format]
4. **[Title]** — [Hook] → Best as: [format]
5. **[Title]** — [Hook] → Best as: [format]

---

## All 20 Ideas by Lens

### 📖 Story Lens
1. **[Title]**
   Hook: [One sentence]
   Best format: [newsletter / thread / LinkedIn / video]

2. **[Title]**
   Hook: [One sentence]
   Best format: [format]

### 👁️ Observation Lens
3. **[Title]**
   Hook: [One sentence]
   Best format: [format]

4. **[Title]**
   Hook: [One sentence]
   Best format: [format]

### 🔥 Contrarian Take Lens
5. **[Title]**
   Hook: [One sentence]
   Best format: [format]

6. **[Title]**
   Hook: [One sentence]
   Best format: [format]

### 📋 Listicle Lens
7. **[Title]**
   Hook: [One sentence]
   Best format: [format]

8. **[Title]**
   Hook: [One sentence]
   Best format: [format]

### ⏮️ Past vs. Present Lens
9. **[Title]**
   Hook: [One sentence]
   Best format: [format]

10. **[Title]**
    Hook: [One sentence]
    Best format: [format]

### ⏭️ Present vs. Future Lens
11. **[Title]**
    Hook: [One sentence]
    Best format: [format]

12. **[Title]**
    Hook: [One sentence]
    Best format: [format]

### 🔬 Analysis Lens
13. **[Title]**
    Hook: [One sentence]
    Best format: [format]

14. **[Title]**
    Hook: [One sentence]
    Best format: [format]

### 🔧 Teardown Lens
15. **[Title]**
    Hook: [One sentence]
    Best format: [format]

16. **[Title]**
    Hook: [One sentence]
    Best format: [format]

### 💡 Lesson Lens
17. **[Title]**
    Hook: [One sentence]
    Best format: [format]

18. **[Title]**
    Hook: [One sentence]
    Best format: [format]

### 📊 Data/Research Lens
19. **[Title]**
    Hook: [One sentence]
    Best format: [format]

20. **[Title]**
    Hook: [One sentence]
    Best format: [format]

---

## Quick Calendar Fill

| Week | Main Piece | Social Content |
|------|-----------|---------------|
| 1 | Idea #[X] as newsletter | Ideas #[X], #[X] as tweets |
| 2 | Idea #[X] as newsletter | Ideas #[X], #[X] as LinkedIn |
| 3 | Idea #[X] as newsletter | Ideas #[X], #[X] as thread |
| 4 | Idea #[X] as newsletter | Ideas #[X], #[X] as notes |
```

## Quality Checklist

- [ ] 20 ideas total (2 per lens, 10 lenses)
- [ ] Each title is specific and compelling (not generic)
- [ ] Each hook creates curiosity in one sentence
- [ ] Best format recommended for each
- [ ] Top 5 picks identified and ranked
- [ ] Ideas are relevant to user's niche and audience
- [ ] No duplicate angles — each idea is genuinely different
- [ ] Ideas are feasible (user could actually write them)
- [ ] Calendar fill suggestion included
- [ ] Ideas pull from user's expertise area (from context files)
