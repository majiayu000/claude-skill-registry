---
name: threadwriter
description: "Topic in, optimized X thread out. Takes your rough idea and turns it into a high-engagement Twitter thread with hooks, pacing, and CTAs. Use when: sharing insights on X/Twitter, building thought leadership, or creating viral-ready content. NOT for: automated posting bots, spam generation, or mass-scheduled content campaigns."
homepage: https://pawhub.ai/threadwriter
metadata:
  {
    "openpaw":
      {
        "emoji": "✍️",
        "requires": { "bins": ["node"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@pawhub/threadwriter",
              "bins": ["threadwriter"],
              "label": "Install ThreadWriter (npm)",
            },
          ],
      },
  }
---

# ThreadWriter ✍️

Turn rough ideas into polished X threads. Paw writes the hooks, nails the pacing, and adds CTAs. You just approve and post.

## When to Use

✅ **USE this skill when:**

- You have insights but hate formatting threads
- Building thought leadership on X/Twitter
- Sharing technical content in digestible chunks
- Announcing product launches
- Breaking down complex topics
- Creating viral-ready content
- Repurposing blog posts into threads
- Maximizing engagement on X

## When NOT to Use

❌ **DON'T use this skill when:**

- Building automated posting bots → violates platform TOS
- Generating spam or low-quality content
- Mass-scheduling content campaigns → use Buffer, Hootsuite
- Creating threads without actual insights (garbage in = garbage out)
- Impersonating others
- Generating misleading content

## Setup

```bash
npm install -g @pawhub/threadwriter
threadwriter setup
```

## Example Interactions

### Quick Thread

**You:** Write a thread about why AI agents are the next big thing

**Paw:** *starts drafting*

**Working on:** "Why AI agents are the next big thing"
**Style:** Thought leadership
**Target length:** 7-10 tweets

*15 seconds later...*

✅ **Thread ready** (9 tweets)

**Preview:**

1/ AI agents aren't just better chatbots.

They're the first software that gets things done *for* you, not *with* you.

And most people still don't see what's coming.

---

2/ Here's the thing: every previous AI breakthrough made you faster at doing tasks.

GPT-4 made you write faster. DALL-E made you design faster.

But you were still doing the work.

---

3/ Agents are different.

You say "book me a flight to NYC, cheapest option under $400, window seat."

And it's done. No tabs. No comparison shopping. No booking forms.

The computer did the task.

---

4/ This is the shift from *tools* to *delegation*.

Tools make you more productive. Agents make you more powerful.

Different game entirely.

(continues...)

**Engagement optimizations:**
- ✅ Hook in tweet 1 (grabs attention)
- ✅ Pattern interrupt (tweet 2)
- ✅ Concrete example (tweet 3)
- ✅ Clear thesis (tweet 4)
- ✅ CTA at end (tweet 9)

**Want to:**
- Review full thread? (yes/edit/rewrite)
- Post now? (requires X auth)
- Save draft? (for later posting)

---

**You:** Review full thread

**Paw:** **Full thread:**

1/ AI agents aren't just better chatbots.

They're the first software that gets things done *for* you, not *with* you.

And most people still don't see what's coming.

---

2/ Here's the thing: every previous AI breakthrough made you faster at doing tasks.

GPT-4 made you write faster. DALL-E made you design faster.

But you were still doing the work.

---

3/ Agents are different.

You say "book me a flight to NYC, cheapest option under $400, window seat."

And it's done. No tabs. No comparison shopping. No booking forms.

The computer did the task.

---

4/ This is the shift from *tools* to *delegation*.

Tools make you more productive. Agents make you more powerful.

Different game entirely.

---

5/ Why now?

Three things converged:

• LLMs got good enough to understand complex instructions
• APIs became ubiquitous (every service has one now)
• Context windows got huge (remember entire workflows)

The pieces were always there. Now they fit.

---

6/ What this means practically:

In 2024, you had an assistant that answered questions.

In 2026, you have an employee that executes tasks.

By 2028? You'll have a team.

---

7/ The companies winning here aren't building better chatbots.

They're building:
• Reliable execution (it does what you ask)
• Tool ecosystems (integrates with everything)
• Memory systems (learns your preferences)

Product =! Interface anymore.

---

8/ And this is where it gets wild:

Once agents can reliably execute tasks, they can chain tasks together.

Book flight → reserve hotel → add to calendar → notify team.

Zero clicks. Just intent.

---

9/ We're at the "1995 of AI agents."

Most people see chatbots. A few see what's really happening.

What are you building with them?

Drop a comment. I'm curious what use cases people are exploring. 👇

---

**Analysis:**
- 📊 Thread length: 9 tweets (optimal for engagement)
- 🎯 Hook strength: Strong (tweet 1)
- 📈 Pacing: Good (builds logically)
- 💡 Value: High (actionable insights)
- 🔚 CTA: Clear (tweet 9 asks for engagement)

**Estimated engagement:** Medium-High (if your audience is tech/startup-focused)

**Edits needed?** Or ready to post? ✍️

---

**You:** Change tweet 7, remove the product ≠ interface line, too jargony

**Paw:** *updates tweet 7*

✅ **Updated tweet 7:**

7/ The companies winning here aren't building better chatbots.

They're building:
• Reliable execution (it does what you ask)
• Tool ecosystems (integrates with everything)
• Memory systems (learns your preferences)

The interface is just the starting point.

---

Better? (yes/keep editing)

---

**You:** Yes, post it

**Paw:** *Connects to X API*

🚀 **Posted!**

Thread is live: [X.com link]

**What I'll track:**
- Engagement (likes, retweets, replies)
- Peak engagement time
- Which tweet got the most interaction
- Reply sentiment

I'll send you a performance summary in 24 hours. Want real-time alerts for viral tweets? 📊

---

### Repurposing Content

**You:** Turn this blog post into a thread: [URL]

**Paw:** *fetches and analyzes*

**Blog post:** "How We Scaled to 1M Users"
**Length:** 2,400 words
**Key points:** 7 main sections

*analyzing...*

This is dense. I can turn it into:
1. **Long thread** (15-20 tweets, keeps all details)
2. **Medium thread** (10-12 tweets, highlights only)
3. **Teaser thread** (5-7 tweets, drives traffic to blog)

Which approach? Most people do #2 (highlights thread). 🎯

---

**You:** Highlights thread

**Paw:** *extracts key points*

✅ **Thread created** (11 tweets)

**Hook (tweet 1):**
"We scaled from 0 to 1M users in 18 months.

Here's what worked (and what almost killed us) 🧵"

**Structure:**
- Tweet 1: Hook
- Tweets 2-4: Early growth tactics
- Tweets 5-7: Scaling challenges
- Tweets 8-10: Key lessons
- Tweet 11: CTA (link to full blog post)

**Link placement:** Tweet 11 (best practice for engagement)

Review? (yes/edit)

---

### Voice-to-Thread

**You:** *[voice message]* "I just realized something about product-market fit. Everyone talks about finding it, but nobody talks about maintaining it. Your market shifts. Your product evolves. PMF isn't a destination, it's a moving target. And if you stop moving, you lose it. We learned this the hard way when our core user base changed but our product didn't adapt fast enough."

**Paw:** *transcribes and analyzes*

Great insight. Converting to thread format...

✅ **Thread ready** (6 tweets)

**Preview:**

1/ Everyone talks about *finding* product-market fit.

Nobody talks about *maintaining* it.

And that's where most companies fail.

---

2/ PMF isn't a destination.

It's a moving target.

Your market shifts. Your product evolves. Competitors emerge.

If you stop moving, you lose fit.

---

3/ We learned this the hard way.

Our core user base changed, but our product didn't adapt fast enough.

We had PMF in 2024. By 2025, we didn't. Same product. Different market.

---

(continues...)

**Style:** Personal/authentic (based on your voice)
**Engagement potential:** High (relatable struggle)

Want to post this? 🎯

---

### Thread Analytics

**Paw:** 📊 **Thread Performance (24h)**

**Thread:** "Why AI agents are the next big thing"
**Posted:** Yesterday, 9:14 AM

**Engagement:**
- 🔄 Retweets: 342
- ❤️ Likes: 1,847
- 💬 Replies: 94
- 👁️ Impressions: 87,230

**Top-performing tweet:**
Tweet 3 (the flight booking example) — 2,103 likes

**Engagement pattern:**
- Peak: 2-4 hours after posting (typical)
- Drop-off: tweet 7 (might be too technical)
- Recovery: tweet 9 (CTA worked)

**Reply sentiment:**
- 87% positive
- 8% questions (mostly "what tools?" )
- 5% critical (healthy skepticism)

**Compared to your average thread:**
- +127% retweets 🔥
- +89% likes
- +65% replies

This one hit. The flight booking example is resonating.

**Action:** Want me to write a follow-up thread expanding on that example? 📈

## Commands

```bash
# Quick thread from prompt
threadwriter create "topic here"

# Thread from blog post URL
threadwriter from-url https://blog.example.com/post

# Thread from voice memo
threadwriter from-voice audio.m4a

# Thread from existing text file
threadwriter from-file notes.txt

# Post thread directly (requires X auth)
threadwriter post thread-draft-123

# Save thread as draft
threadwriter save thread-draft-123

# Analytics for posted thread
threadwriter stats TWEET_ID

# List all drafts
threadwriter drafts list
```

## Style Configuration

```bash
# Set default tone
threadwriter config set tone "authentic" # casual, professional, authentic, technical

# Set default length
threadwriter config set length "medium" # short (5-7), medium (8-12), long (13-20)

# Enable/disable CTAs
threadwriter config set auto-cta true

# Set hook style
threadwriter config set hook-style "pattern-interrupt" # direct, pattern-interrupt, question, story
```

## Telegram Integration

**Quick thread:**

**You:** `/thread "AI agents topic"`

**Paw:** *drafts thread*

Thread ready (9 tweets). Preview first 2:

1/ AI agents aren't just better chatbots...
2/ Here's the thing: every previous AI...

React with ✅ to post, ✏️ to edit, 💾 to save draft.

## Tips from Paw

> "The hook is everything. If tweet 1 doesn't grab attention, the rest doesn't matter. I optimize for pattern interrupts."

> "Threads under 10 tweets perform better. People's attention is finite. Say more with less."

> "Always end with a CTA. Ask a question, request engagement, link to something. Don't just trail off."

> "The flight booking example in that AI agents thread? That's specificity. Concrete examples > abstract concepts."

> "Post between 9-11 AM EST or 2-4 PM EST. That's when tech Twitter is most active."

## Pricing

- **Free tier:** 5 threads/month, basic optimization
- **Pro:** $10/month — unlimited threads, voice-to-thread, analytics, priority generation
- **Team:** $29/month — multiple accounts, brand voice training, A/B testing

Install from PawHub: [pawhub.ai/threadwriter](https://pawhub.ai/threadwriter)

## Notes

- Threads are optimized for X/Twitter (280 char limit)
- Analytics require X API access (read-only)
- Posting requires X OAuth (secure, revocable)
- Voice transcription uses Whisper API
- Thread drafts stored locally (encrypted)
- All content remains yours (no rights transfer)

---

Built for people with insights but no patience for thread formatting. ✍️🐾
