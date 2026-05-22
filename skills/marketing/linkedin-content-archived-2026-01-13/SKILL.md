---
name: linkedin-content
description: Transform source content (podcast clips, blog posts, newsletters) into LinkedIn posts using framework-fitting method. Matches concepts to proven format categories, then adapts templates based on animating principles rather than rigid fill-in-the-blank.
---

# LinkedIn Content Creator

## Purpose

Transform OpenEd source content into high-performing LinkedIn posts by matching concepts to proven frameworks, then adapting freely based on the principles that make each format work.

## When to Use

Use this skill when:
- Creating LinkedIn posts from podcast episodes or clips
- Transforming daily/weekly newsletter content for LinkedIn
- Repurposing blog posts or deep dives for social
- Building Ela's or OpenEd's LinkedIn presence

## The Workflow

```
SOURCE → CONCEPT → CATEGORY → FRAMEWORK → ADAPT → POST → MULTIPLY (SCAMPER)
```

### Step 1: Discern the Concept

Before choosing a format, deeply understand what you're working with.

**From the source content, extract:**
- The core insight or idea (one sentence)
- The emotional hook (what feeling does this evoke?)
- The target reader (who needs to hear this?)
- The transformation (what changes for the reader after consuming this?)

**Example:**
- Source: Podcast clip where guest describes letting her 18-month-old use a butter knife
- Core insight: Low-stakes failures early build confident kids later
- Emotional hook: Permission to let go of perfectionism
- Target: Parents who helicopter out of love but sense it's backfiring
- Transformation: Relief + actionable framework for calculated risk-taking

### Step 2: Match to Category

Each category works for different psychological reasons. Match your concept to the category whose *principle* fits best.

| Category | Animating Principle | Best For |
|----------|---------------------|----------|
| **Engagement** | People want to participate, not just consume | Opinions, debates, community input |
| **Story** | Emotion drives sharing; vulnerability builds trust | Personal experiences, transformations, failures |
| **List/Tips** | Scannable value feels more actionable | How-to content, frameworks, mistakes to avoid |
| **Contrarian** | Pattern interrupts grab attention; controversy creates engagement | Challenging conventional wisdom, hot takes |
| **Authority** | Demonstrated expertise builds credibility | Research, data, professional insights |
| **Community** | People want to belong and be recognized | Celebrations, connections, welcomes |

**Selection question:** "What's the primary job this post needs to do?"

- Start a conversation → **Engagement**
- Make them feel something → **Story**
- Give them something useful → **List/Tips**
- Challenge what they believe → **Contrarian**
- Establish credibility → **Authority**
- Build relationships → **Community**

### Step 3: Load the Right Reference File

**IMPORTANT: Only load ONE category file at a time.** Each is 3-6k words. Don't load all of them.

Once you've matched a category in Step 2, load ONLY that reference file:

| If the job is... | Load this file |
|------------------|----------------|
| Drive comments/participation | `references/engagement-frameworks.md` |
| Make them feel something | `references/story-frameworks.md` |
| Give scannable value | `references/list-frameworks.md` |
| Challenge what they believe | `references/contrarian-frameworks.md` |
| Establish credibility | `references/authority-frameworks.md` |
| Build relationships | `references/community-frameworks.md` |

**To search across all categories without loading:**
```bash
grep -i "keyword" references/*.md
```

**Framework counts:**
- Engagement (16) - polls, agree/disagree, crowdsource, fill-in-blank
- Story (24) - failure, transformation, day-in-life, values
- List (17) - tips, 10 ideas, DOs/DONTs, skills lists
- Contrarian (20) - hot takes, call BS, state opposite, rants
- Authority (26) - how-to, quotes, screenshots, secret sauce
- Community (15) - shoutouts, connect, welcome, comedy

### Step 4: Adapt Based on Principles

**Templates are starting points, not constraints.**

Each framework reference includes:
- **The template** - The structural skeleton
- **Why it works** - The psychological principle
- **Example** - How it's been executed

**Your job:** Use the principle to adapt the template to your specific content. Combine elements from multiple frameworks if that serves the message better.

**Adaptation questions:**
- Does this template amplify my core insight, or dilute it?
- What would I cut? What would I add?
- Does this sound like OpenEd/Ela, or like a template?

### Step 5: Apply OpenEd Voice

Before posting, run through the voice checklist:

- [ ] No correlative constructions ("isn't just X, it's Y")
- [ ] Hyphens with spaces for breaks - like this - not em dashes
- [ ] No emojis (or minimal, strategic use only)
- [ ] Specific details over generic claims
- [ ] Permission-giving tone, not preachy
- [ ] Would Sarah (our target reader) feel seen?

For deeper voice guidance, invoke `ghostwriter` skill.

---

## Framework Quick Index

### Engagement (drive participation)
| Framework | Hook Type | Best For |
|-----------|-----------|----------|
| Agree or Disagree | Statement + vote | Opinions, values |
| Run a Poll | 4 options | Data gathering, trends |
| Which Would You Rather | Binary choice | Trade-offs, priorities |
| Crowdsource | Ask for input | Community wisdom |
| Fill-in-the-Blank | Complete the sentence | Easy engagement |

### Story (emotional connection)
| Framework | Hook Type | Best For |
|-----------|-----------|----------|
| Failure Story | I failed at X | Vulnerability, lessons |
| Transformation | Before → After | Results, change |
| Movie Script | Scene-by-scene | Drama, tension |
| I Was Fired | Career setback | Resilience |
| Birthday Reflections | X things I've learned | Milestones |

### List/Tips (scannable value)
| Framework | Hook Type | Best For |
|-----------|-----------|----------|
| 10 Ideas | Numbered list | Comprehensive value |
| Tips Post | Quick wins | Actionable advice |
| DOs and DONTs | Contrast format | Clear guidance |
| Mistakes Listicle | What not to do | Cautionary |
| Things They Won't Teach | Hidden knowledge | Insider tips |

### Contrarian (pattern interrupt)
| Framework | Hook Type | Best For |
|-----------|-----------|----------|
| I Call BS | Challenge norm | Strong opinions |
| State The Opposite | Flip expectation | Counterintuitive takes |
| Dark Side Of | Hidden downside | Nuanced critique |
| Name Thy Enemy | Common villain | Solidarity |
| Call Out The Unspoken | Say what others think | Catharsis |

### Authority (build credibility)
| Framework | Hook Type | Best For |
|-----------|-----------|----------|
| How-To Series | Step-by-step | Teaching |
| Study Summary | Research + insight | Data-backed |
| PRO TIP | Single expert move | Quick credibility |
| Reveal Your Process | Behind the scenes | Transparency |
| Answer Common Question | FAQ format | Helpful authority |

### Community (relationship building)
| Framework | Hook Type | Best For |
|-----------|-----------|----------|
| Shoutout | Celebrate someone | Generosity |
| Let's Connect | Invitation | Network growth |
| Welcome Newbies | Beginner content | Inclusivity |
| Give Away | Free resource | Lead generation |

---

## Example Transformation

**Source:** Daily newsletter about letting kids fail at low-stakes tasks

**Step 1 - Concept:**
- Core insight: Helicopter parenting backfires; kids need early failures
- Emotional hook: Permission to stop protecting
- Target: Anxious parents who over-help
- Transformation: Framework for calculated risk-taking

**Step 2 - Category Match:**
This is a **Contrarian** take (challenges helicopter parenting norm) with **Story** elements (the guest's example).

**Step 3 - Framework Options:**
- "State The Opposite" - "Stop helping your kids"
- "I Call BS" - "I call BS on 'safety first' parenting"
- "Transformation" - "From helicopter to landing pad"

**Step 4 - Adapted Post:**

```
Unpopular opinion: Your kid should fail more.

Not at the big stuff. At the small stuff.

Let the 3-year-old spill the milk.
Let the 7-year-old burn the toast.
Let the 12-year-old miss the deadline.

Here's what I've learned from talking to hundreds of homeschool families:

The parents who "protect" their kids from every small failure?
They're raising adults who can't handle any failure.

The parents who let kids stumble early - when the stakes are low?
They're raising adults who know how to recover.

One mom on our podcast let her 18-month-old use a butter knife.
Her kids are now confident, capable teenagers.

Coincidence? I don't think so.

What's one thing you let your kid fail at this week?
```

**Step 5 - Voice Check:**
- ✓ No correlatives
- ✓ Hyphens with spaces
- ✓ No emojis
- ✓ Specific details (18-month-old, butter knife)
- ✓ Permission-giving tone
- ✓ Sarah would feel seen

---

## Step 6: Multiply with SCAMPER (Optional)

One good post can become seven. Use SCAMPER to generate variations:

| Letter | Transformation | Question to Ask |
|--------|----------------|-----------------|
| **S - Substitute** | Swap the example, data, or subject | "What if I used a different story to make the same point?" |
| **C - Combine** | Merge with personal story or another concept | "What if I added my own experience to this?" |
| **A - Adapt** | Expand to thread, carousel, or different format | "What if this was a thread instead of a single post?" |
| **M - Modify** | Make punchier, longer, or more extreme | "What if I cut this in half?" or "What if I 10x'd the stakes?" |
| **P - Purpose** | Angle for different audience segment | "What if this was for teachers instead of parents?" |
| **E - Eliminate** | Remove context, simplify radically | "What's the one-sentence version?" |
| **R - Reverse** | Flip the frame or argue the opposite | "What if I made the case for the other side first?" |

**Example - Original post:**
> "The NYT published two articles 3 weeks apart. One asks if schools cause mental health crises. The other calls for more homeschool oversight. The Times is arguing with itself."

**SCAMPER variations:**

- **S:** Replace NYT with "mainstream media" pattern
- **C:** Add "When my mother-in-law sent me this article..."
- **A:** Turn into 4-part thread with screenshots
- **M:** "NYT: 'Schools might hurt kids.' Also NYT: 'Watch the homeschoolers.' Pick one."
- **P:** Reframe for teachers who are questioning the system
- **E:** "The NYT is arguing with itself. Read Nov 24. Then Dec 14."
- **R:** "What if the homeschool critic accidentally proved the opposite?"

**When to use SCAMPER:**
- After a post performs well - multiply the winner
- When you need volume - 7 posts from 1 concept
- When testing angles - see which frame resonates

---

## Related Skills

- `ghostwriter` - Voice and anti-AI patterns
- `hook-and-headline-writing` - Opening lines and headlines
- `social-content-creation` - Multi-platform content (includes SCAMPER deep dive, Human Desires, Vision/Anti-Vision)
- `video-caption-creation` - For video posts with captions
