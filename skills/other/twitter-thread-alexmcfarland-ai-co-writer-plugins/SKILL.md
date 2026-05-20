---
name: twitter-thread
description: Write an 8-12 tweet thread optimized for engagement. Hook tweet that stops the scroll, body tweets that deliver value (one idea per tweet), CTA tweet. Supports storytelling and listicle formats. Includes character counts. Use when user wants a "Twitter thread", "X thread", "tweet storm", or wants to break down an idea into a thread.
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

# Twitter/X Thread Writer

**Purpose:** Write 8-12 tweet threads that stop the scroll, deliver value, and drive engagement. Each tweet is a self-contained unit of value. The thread as a whole tells a complete story or teaches a complete lesson.

## When to Activate

Use this skill when:
- User wants to write a Twitter/X thread
- User mentions "thread", "tweet storm", or "break this down into tweets"
- User has an idea, story, or lesson they want to turn into a thread
- User wants to promote content or teach something on X

## Thread Anatomy

### Tweet 1: The Hook (MOST IMPORTANT)

This tweet determines whether anyone reads the rest. It must stop the scroll.

**Hook patterns that work:**

1. **Bold claim**: "Most [audience] fail at [thing] because they do [wrong approach]. Here's a better way: 🧵"
2. **Results-first**: "I [achieved result] in [timeframe]. Here's the exact process (step by step):"
3. **Contrarian opener**: "[Common belief] is wrong. Here's what actually works: 🧵"
4. **Curiosity gap**: "I spent [timeframe] studying [topic]. [Number] things I learned that nobody talks about:"
5. **Story opener**: "[Specific moment]. [What happened]. [What I learned]. Thread 🧵"
6. **List preview**: "[Number] [things] that [outcome]. (Most people only know #3) 🧵"

**Hook rules:**
- Must work as a standalone tweet (people see it before the thread)
- Include 🧵 emoji to signal it's a thread
- Under 200 characters ideal — shorter hooks perform better
- No "Hey guys" or "Let me tell you about" openers

### Tweets 2-10: The Body

**One idea per tweet.** This is the #1 rule. Each tweet should:
- Deliver a complete thought
- Make sense even if read in isolation
- Build on the previous tweet but not depend on it

**Body tweet formats:**

**For listicle threads:**
```
[Number]. [Bold statement]

[2-3 sentences expanding with example or reasoning]
```

**For storytelling threads:**
```
[Continue the narrative]

[Advance the plot one beat per tweet]

[Include dialogue, sensory details, or tension]
```

**For how-to threads:**
```
Step [X]: [Action]

[Why this step matters]
[Exactly what to do]
[What to expect]
```

**Body tweet rules:**
- Keep under 280 characters each
- Use line breaks for readability
- One tweet = one point, one step, one moment
- Vary tweet length (mix short punchy tweets with longer ones)
- Include specific examples, numbers, or details

### Tweet 11-12: The Close + CTA

**Second-to-last tweet: The summary or key takeaway**
Distill the entire thread into one powerful statement. This is often the most retweeted tweet.

**Final tweet: The CTA**
Options:
- "If you found this valuable, repost the first tweet to help others find it"
- "Follow me [@handle from BUSINESS.md] for more on [topic]"
- "I write about this every week in my newsletter: [link from BUSINESS.md]"
- "I'm building [product]. If this resonated, check it out: [link]"

**CTA rules:**
- Only ONE call to action (not three)
- Make it feel natural, not desperate
- Pull handle/links from context files, never hardcode

## Thread Formats

### Format A: Listicle Thread
Best for: tips, mistakes, lessons, rules

```
Tweet 1: [Number] [things] about [topic] that [outcome]: 🧵
Tweet 2: 1. [First point + explanation]
Tweet 3: 2. [Second point + explanation]
...
Tweet N-1: [Summary takeaway]
Tweet N: [CTA]
```

### Format B: Story Thread
Best for: personal experiences, case studies, transformations

```
Tweet 1: [Compelling hook that sets up the story] 🧵
Tweet 2: [The beginning / context]
Tweet 3: [The challenge / conflict]
Tweet 4-8: [The journey / attempts / turning points]
Tweet 9-10: [The resolution / results]
Tweet 11: [The lesson]
Tweet 12: [CTA]
```

### Format C: Framework Thread
Best for: teaching a system, process, or mental model

```
Tweet 1: [The framework name + what it solves] 🧵
Tweet 2: [Why this framework exists / the problem]
Tweet 3-9: [Each component of the framework]
Tweet 10: [How to implement it]
Tweet 11: [Summary]
Tweet 12: [CTA]
```

## Output Format

```
# Twitter/X Thread: [Topic]

**Format:** [Listicle / Story / Framework]
**Length:** [X] tweets
**Estimated read time:** [X] minutes

---

**Tweet 1** (XXX/280 chars)
[Tweet text]

---

**Tweet 2** (XXX/280 chars)
[Tweet text]

---

**Tweet 3** (XXX/280 chars)
[Tweet text]

---

[Continue for all tweets...]

---

**Tweet [N]** (XXX/280 chars)
[CTA tweet]

---

## Thread Stats
- Total tweets: [X]
- Avg chars per tweet: [X]
- Key insight: [One sentence]
```

## Quality Checklist

- [ ] Hook tweet stops the scroll (would YOU click "show thread"?)
- [ ] Each tweet is under 280 characters
- [ ] One idea per tweet — no cramming
- [ ] Character counts shown for every tweet
- [ ] Thread works in both listicle and narrative reading modes
- [ ] Specific examples and numbers (not vague)
- [ ] CTA is clear and singular
- [ ] 8-12 tweets total
- [ ] Voice matches context profiles
- [ ] No hardcoded names, handles, or links (pulled from context)

## Common Mistakes

- **Cramming too much into one tweet** — Split it. Always split it.
- **Hook that doesn't hook** — If tweet 1 doesn't make you want to read tweet 2, rewrite it.
- **Every tweet sounds the same** — Vary length, tone, and structure.
- **No specific examples** — Abstract advice = boring. Specific examples = engagement.
- **Multiple CTAs** — One. Just one.
- **Thread too short (3-4 tweets)** — That's not a thread, that's a post. Expand or use a different format.
- **Thread too long (20+ tweets)** — Most people drop off after 10-12. Edit ruthlessly.
