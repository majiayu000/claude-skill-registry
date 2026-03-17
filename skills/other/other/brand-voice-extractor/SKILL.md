---
name: brand-voice-extractor
description: "Extract or build a distinct brand voice profile that AI agents can use to produce on-brand content every time. Two modes: Extract (analyze content you're proud of) or Build (construct a voice from scratch). Outputs a complete voice profile with personality traits, tone spectrum, vocabulary guide, rhythm patterns, and example phrases. Use this before any content creation skill for consistent, human-sounding output."
version: "1.1.0"
price: "$9"
author: "@BrianRWagner"
slug: "brw-brand-voice-extractor"
---

# Brand Voice Extractor

## Mode

Detect from context or ask: *"Quick snapshot, full Voice Guide, or full guide with AI training examples?"*

| Mode | What you get | Best for |
|------|-------------|----------|
| `quick` | Top 5 voice traits + 3 core do/don't rules | Fast reference before a single piece |
| `standard` | Complete Voice Guide: personality, tone, vocabulary, rhythm, phrases | AI training, ghostwriting, brand docs |
| `deep` | Full Voice Guide + 10 before/after rewrites + AI prompt template + onboarding guide | Content team onboarding, agency handoff |

**Default: `standard`** — use `quick` for a fast reference. Use `deep` if you're onboarding writers or building a content system.

---

## Runtime Context
**Platform:** Claude Code / OpenClaw  
**File system:** Available. Read prior outputs before starting. Save all outputs to the paths specified in Memory Protocol.  
**Cross-skill dependencies:**
- Upstream: None required — this is the starting point
- Downstream: This skill produces a complete VOICE-PROFILE.md ready for use in any content generation workflow.

---

## Memory Protocol

**Save output to:** `voice/[name]-voice-profile-YYYY-MM-DD.md`

**At session start:** Check if a prior voice profile file exists for this person/brand. If yes:
- Load it into context
- Note this is a re-run / refinement session
- Compare new samples to prior profile — flag if voice has evolved or if patterns conflict

**Cross-session rule:** If a prior voice profile exists, always load it before starting — do not treat every run as a cold start. Reference what was previously extracted and ask if anything has changed since.

---

Generic copy converts worse than copy with a distinct voice.

Not because the words are different — because the reader feels like they're hearing from a *person*, not a marketing team.

This skill defines that voice. Either by extracting it from content you're already proud of, or building it strategically from the ground up. The output is a reusable voice profile that every content skill can reference — so your AI never sounds like everyone else's AI.

---

## What You Get

A complete **voice profile document** containing:

- Voice summary (2-3 sentences capturing the essence)
- Core personality traits with real-world implications
- Tone spectrum across 5 key dimensions
- Vocabulary guide: words to use, words to kill
- Rhythm & structure patterns
- Example phrases (on-brand vs. off-brand)
- Do's and Don'ts for any writer (human or AI)

**Result:** Anyone — or any AI agent — can read this profile and produce content that sounds unmistakably like you.

---

## Two Modes

### Mode 1: Extract
**Use when:** You have existing content that already sounds right.

Feed the skill 3-5 pieces of content you're proud of — website copy, emails, posts, newsletter editions, anything where you thought *"yes, this is me."*

The skill analyzes patterns across tone, vocabulary, rhythm, structure, and POV, then codifies what makes your writing distinctive.

**Best inputs:**
- Your About page or homepage copy
- Your top-performing social posts
- Emails where you nailed the tone
- Newsletter editions you felt good about
- Video or podcast transcripts

### Mode 2: Build
**Use when:** You're starting fresh, your existing content is generic, or you want to evolve your voice strategically.

The skill asks 10-15 targeted questions about your personality, audience, positioning, and aspirations — then constructs a voice aligned with who you are and who you're talking to.

**How to choose:**

> "Do you have existing content that represents how you want to sound?"
> - Yes → **Extract mode**
> - No / Not sure → **Build mode**

---

## How to Use This Skill

### Step 1: Choose your mode
Tell the agent: *"Run the brand-voice-extractor in Extract mode"* or *"Build mode."*

### Step 2: Provide inputs
- **Extract:** Paste 3-5 pieces of content
- **Build:** Answer the 10-15 questions the agent asks

### Step 3: Receive your voice profile
The agent outputs a complete, formatted voice profile document.

### Step 4: Save it
Store the profile somewhere accessible (e.g., `brand/VOICE-PROFILE.md` in your workspace). Reference it in every future content task.

### Step 5: Reference it in other skills
> "Write 5 LinkedIn posts using this voice profile: [paste profile]"
> "Draft an email sequence. Use my voice profile for tone and style."
> "Rewrite this landing page to match my voice."

---

## Extract Mode: What the Agent Analyzes

### Extraction Reasoning Chain

Before outputting patterns, follow this process explicitly:

> **Analyze samples → Extract signals per dimension → Synthesize conflicts (when patterns contradict, weight 3 most recent samples 2x) → Validate against quality bar → Output**

Do not skip steps. Each stage informs the next. Surfacing the reasoning process catches extraction errors before they lock into the profile.

### Input Constraints

- **Minimum sample length:** If total sample content < 500 words, request more before proceeding. A profile built on too little material will be too general to be useful.
- **Corporate/committee voice detection:** If samples read as committee-written (passive voice >30%, no personal opinions, heavy hedging throughout), flag this to the user before proceeding: *"These samples may reflect corporate/edited voice rather than your authentic voice. For best results, share something you wrote quickly and unfiltered — an email, a Slack message, a quick post."*

---

**Tone patterns**
- Formal ↔ Casual (contractions? fragments? slang?)
- Serious ↔ Playful (humor? gravity?)
- Reserved ↔ Bold (strong claims vs. hedging?)
- Distant ↔ Intimate (I/you vs. we/they?)

**Vocabulary patterns**
- Jargon level (heavy, translated, or light)
- Signature words and phrases
- Words you seem to avoid
- Everyday vs. formal vocabulary

**Rhythm patterns**

*Technical HOW:* Count average words per sentence across all samples. Measure sentence length variance (do most sentences cluster around the same length, or does it range widely?). Flag if >40% of sentences are similar length — that signals a monotone rhythm that may need to be intentional, not accidental.

- Average sentence and paragraph length
- Mix of short/punchy vs. longer/flowing
- Fragment use
- List frequency

**Transition patterns**

*Technical HOW:* Scan for bridge phrases appearing 3+ times across samples. Extract the exact wording — not paraphrases, the literal phrases. These become the transition fingerprints. Examples: "Here's the thing...", "What that means is...", "The reality is..."

- Recurring bridge phrases (extract verbatim)
- How they move between ideas (abrupt? flowing? with a pivot?)
- Signature openers and closers

**Structural patterns**
- How you open (story? question? bold claim?)
- How you transition between ideas
- How you close (CTA? summary? open loop?)
- Headers, formatting, whitespace use

**Personality signals**
- Self-deprecating or confident?
- Teacher or peer?
- Polished or raw?
- Optimistic or realistic?

### Conflict Resolution

When patterns contradict across samples (e.g., some samples are formal, some are casual):
1. Weight the 3 most recent samples 2x in your analysis
2. Flag the conflict explicitly in the profile: *"Voice is inconsistent across [dimension] — recent samples lean [X], older samples lean [Y]. Profile reflects recent direction."*
3. Ask the user: "I'm seeing tension in [dimension]. Which direction is closer to where you want to go?"

---

## Build Mode: Questions the Agent Asks

**Identity (who you are)**
1. What are 3-5 words that describe your personality?
2. What do you stand for? What's your core belief about your industry?
3. What's your background? What shaped how you see things?
4. What makes you genuinely different from others in your space?

**Audience (who you're talking to)**
5. Who are you talking to? (Be specific — not "entrepreneurs")
6. What tone resonates with them? What do they respond to?
7. What would make them trust you? What would turn them off?

**Positioning (how you show up)**
8. Are you the expert, the peer, the rebel, the guide, the insider?
9. Where do you sit on accessible ↔ exclusive?
10. Where do you sit on approachable ↔ authoritative?

**Aspiration (what you want to sound like)**
11. Name 2-3 people or brands whose voice you admire. What specifically?
12. What do you NOT want to sound like?
13. Any signature words or phrases that feel like "you"?
14. Any words you hate or want to avoid?
15. How do you feel about humor? Profanity? Hot takes?

---

## Voice Profile Output Format

```
# [Your Name] Voice Profile

## Voice Summary
[2-3 sentences. What does this voice FEEL like to encounter?]

## Core Personality Traits
- **[Trait]:** [What this means in practice]
- **[Trait]:** [What this means in practice]
- **[Trait]:** [What this means in practice]

## Tone Spectrum
| Dimension | Position | Notes |
|-----------|----------|-------|
| Formal ↔ Casual | [position] | [specifics] |
| Serious ↔ Playful | [position] | [specifics] |
| Reserved ↔ Bold | [position] | [specifics] |
| Simple ↔ Sophisticated | [position] | [specifics] |
| Warm ↔ Direct | [position] | [specifics] |

## Vocabulary
**USE:** [words, phrases, signature openers]
**AVOID:** [words, corporate-speak, AI-sounding phrases]
**Jargon level:** [Heavy / Light / Translated]

## Rhythm & Structure
**Sentences:** [pattern]
**Paragraphs:** [pattern]
**Openings:** [signature moves]
**Formatting:** [headers, bullets, whitespace]

## Example Phrases
**On-brand:** [3 examples]
**Off-brand:** [3 examples + why wrong]

## Do's and Don'ts
**DO:** [3-5 rules]
**DON'T:** [3-5 rules]
```

---

## Quality Bar

A good voice profile passes this test:

✅ **Recognizable** — Could someone identify content as "yours" without a byline?
✅ **Actionable** — Could a writer (human or AI) produce on-brand content using only this profile?
✅ **Differentiated** — Does it sound different from competitors?
✅ **Authentic** — Does it feel true to who you are?
✅ **Consistent** — Can it apply across formats (social, email, long-form)?

If any answer is no, the profile needs more specificity.

---

## After Delivering the Profile

Once the voice profile is output, always offer the next step:

```
Your voice profile is complete. What's next?

A) Test it — Generate 3 sample sentences in this voice to validate it feels right
B) Refine it — Tell me what's off; I'll diagnose which pattern needs adjustment
C) Strengthen it — I'll identify the weakest dimension and deepen it with more sample analysis
D) Done — Save to voice profile file; it's ready for use in any content generation workflow
```

Just reply with a letter or describe where you want to go.

---

## How This Connects to Other Skills

This skill produces a complete VOICE-PROFILE.md ready for use in any content generation workflow.

Voice profile → **direct-response-copy:** "Write landing page copy using this voice profile."
Voice profile → **content-atomizer:** "Repurpose this using my voice profile for tone."
Voice profile → **email-sequences:** "Draft this sequence. Match my voice."
Voice profile → **lead-magnet:** "Frame the lead magnet to match this voice."

**The workflow:** Run brand-voice-extractor first → Save the profile → Reference it in everything else.

---

## Available on Claw Mart

→ [Get Brand Voice Extractor on Claw Mart](https://www.clawhub.ai/skills/brw-brand-voice-extractor) — $9
