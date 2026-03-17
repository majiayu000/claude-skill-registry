---
name: social-card-gen
description: Generate platform-specific social post variants (Twitter/X, LinkedIn, Reddit) from one source input. Works with or without Node.js script. Includes platform reasoning, quality review, and guardrails against cross-posting spam.
---

# Social Card Generator

Transform one source message into platform-ready social copy for Twitter/X, LinkedIn, and Reddit.

This skill works two ways:
- **With Node.js:** Use `generate.js` for deterministic, automated output
- **Without Node.js:** Manual generation path built directly into this skill (no dependencies required)

---

## ⚠️ MANDATORY: 4-Question Intake Before Generating

Ask these before writing a single word of copy:

> 1. **Source message:** What's the core idea, update, or story? (Paste raw text or describe it.)
> 2. **Tone goal:** Informative? Provocative? Humble brag? Conversational? Educational?
> 3. **Audience:** Who needs to see this? (Founders, marketers, developers, general public?)
> 4. **CTA:** What do you want readers to do? (Visit link, reply, follow, share, start a conversation?)

Without these answers, you'll get generic output that won't land on any platform.

---

## Platform Reasoning Rules (Built In — No External Script Needed)

### 🐦 Twitter/X
- **Character limit:** 280 characters (single tweet) or threaded for long-form
- **Tone:** Punchy, direct, opinionated. Twitter rewards brevity and conviction.
- **Hook structure:** Lead with the most surprising or specific claim. No warm-up.
- **Hashtags:** Max 1-2 directly relevant tags. Never stuff.
- **CTA style:** Short and embedded. "What's your take?" or "Link in reply."
- **What kills Twitter posts:** Long intros, passive voice, corporate speak, hashtag walls.
- **Example hook pattern:** "[Counterintuitive claim]. Here's why: [1-2 sentence reason]. [Engaging question]."

### 💼 LinkedIn
- **Character limit:** 3,000 characters for posts. First 2 lines before "See more" are critical.
- **Tone:** Professional but personal. Thought leadership with a human angle.
- **Hook structure:** First line must create curiosity or state a bold truth — not "excited to share."
- **Hashtags:** 3-5 max, at the end. Never in the body copy.
- **CTA style:** Invite discussion. "What's your experience with this?" works well.
- **Opener rule:** NEVER start with self-promotional language. Lead with a lesson, story, or observation.
- **What kills LinkedIn posts:** Cringe openers ("I'm humbled to announce..."), excessive hashtags, no line breaks.
- **Format tip:** Short paragraphs (1-2 lines). White space is your friend.

### 🔵 Reddit
- **Character limit:** No hard limit, but long posts need clear structure with headers.
- **Tone:** Authentic, curious, community-first. Reddit readers have a finely tuned BS detector.
- **Hook structure:** Situational — frame as a question, lesson learned, or genuine experience.
- **Hashtags:** Never. Not a thing on Reddit.
- **CTA style:** End with an open question that invites the community to share their take.
- **Self-promotion rule:** Never lead with your own promotion. Frame everything as a contribution to the community.
- **What kills Reddit posts:** Obvious marketing, lack of genuine insight, "check out my [thing]" openers.

---

## Manual Generation Path (No Node.js Required)

**Follow this process exactly:**

### Step 1: Distill the Core Message
From the source input, extract:
- The ONE key insight or fact
- The "so what" — why does this matter to the audience?
- The evidence or story behind it

### Step 2: Generate 3 Platform Variants

**Twitter/X variant:**
```
[Bold claim or surprising fact — max 1 sentence]

[1-2 sentences of supporting context]

[Engaging question or CTA]

[1-2 relevant hashtags max]
```
*Check: Under 280 chars for single tweet? If not, decide: cut or thread.*

**LinkedIn variant:**
```
[First line hook — create curiosity, not announcement]

[1-2 line context paragraph]

[Core insight or framework — 2-4 short paragraphs]

[Personal angle or reflection]

[Discussion CTA — question for the audience]

[3-5 hashtags at the end only]
```
*Check: Does the first line work before "See more"? Does it NOT start with "I'm excited to..."?*

**Reddit variant:**
```
[Title: specific, searchable, not clickbaity]

[Opening: frame as experience, question, or lesson — community-first]

[Body: genuine story or insight with specifics]

[Closing question to invite community input]
```
*Check: Would this feel at home in the target subreddit? No hashtags?*

---

## With Node.js (Automated Path)

```bash
npm install

# text input
node generate.js --text "We reduced onboarding time by 35% with a checklist." --stdout

# file input
node generate.js --file examples/input-example.md --outdir examples

# URL input (when network is available)
node generate.js --url https://example.com/post --platforms twitter,linkedin --stdout
```

If `generate.js` is unavailable, use the Manual Generation Path above — same quality, just manual.

---

## Quality Self-Review Pass (REQUIRED After Generating)

After generating all 3 variants, run this review before delivering:

| Check | Twitter | LinkedIn | Reddit |
|---|---|---|---|
| Hook strong? (Would you stop scrolling?) | ✅/❌ | ✅/❌ | ✅/❌ |
| CTA present and clear? | ✅/❌ | ✅/❌ | ✅/❌ |
| Platform fit? (Tone matches platform norms) | ✅/❌ | ✅/❌ | ✅/❌ |
| Guardrails pass? (See below) | ✅/❌ | ✅/❌ | ✅/❌ |

**Flag the weakest variant** and explain why: "The Reddit variant is the weakest because it still reads like a LinkedIn post — too polished, not community-first."

---

## Guardrails (Never Violate)

❌ **No identical copy cross-posted** — every platform variant must be meaningfully different in tone and structure
❌ **No hashtag spam on LinkedIn** — max 5, always at the end, never in the body
❌ **No self-promotional openers on Reddit** — community value first, always
❌ **No vague hooks** — "I have some thoughts on X" is not a hook
❌ **No copy that assumes platform context** — Reddit readers don't know your LinkedIn audience

---

## Iteration Loop

After delivering the 3 variants:
1. Ask: "Which variant feels most off? What's not landing?"
2. If hook is weak → rewrite the first line using a different angle (counterintuitive, numerical, story-led)
3. If CTA is weak → try a question instead of a directive
4. If platform fit is off → re-read the platform rules and rewrite from scratch for that platform

---

## Output Format

Deliver:

```
## Twitter/X
[Final copy — ready to paste]
Character count: [X]/280

## LinkedIn
[Final copy — ready to paste]

## Reddit
Title: [Post title]
[Body — ready to paste]

## Quality Review
- Strongest variant: [Platform] — because [reason]
- Weakest variant: [Platform] — [what to improve if needed]
- All guardrails passed: Yes / No — [note any issues]
```

---

*Skill by Brian Wagner | AI Marketing Architect | brianrwagner.com*
