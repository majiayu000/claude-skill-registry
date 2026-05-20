---
name: voice-extractor
description: Extract and document someone's authentic writing voice from samples. Use when someone needs a "voice guide," wants to capture their writing DNA, or needs to train AI to write in their style. Also useful for ghostwriting, brand voice documentation, or onboarding writers.
---

# Voice Extractor

AI-generated content all sounds the same. The fix isn't better prompts — it's teaching the AI how you actually communicate.

This skill extracts your communication DNA from writing samples and produces a Voice Guide: documented, tested, and ready to use.

---

## Context Loading Gates

**Before extracting, collect:**

- [ ] **Writing samples** — minimum 3 samples OR 500 total words (see priority list below)
- [ ] **Purpose of voice guide** — AI training? Ghostwriter onboarding? Team alignment?
- [ ] **Confidence zones** — Any topics where they want to sound more/less authoritative?
- [ ] **Known anti-patterns** — Any words or phrases they already know they want to avoid?

**Sample priority (most → least authentic):**
1. Casual Slack or email (raw, unedited voice)
2. Podcast or call transcript
3. LinkedIn posts or articles
4. Website copy (often edited, less authentic)

**Minimum sample gate:** If samples total under 500 words, stop:
> "These samples are too short to extract reliable patterns. Please add 2-3 more — emails, Slack messages, or transcripts work best. The messier and more casual, the better."

Do not attempt full extraction from under 500 words. Offer quick mode instead.

---

## Phase 1: Sample Quality Assessment

Before extracting, reason through:

1. **Sample authenticity:** Are these samples from edited/polished contexts (website, press) or raw contexts (Slack, email)? More polish = less authentic voice.
2. **Sample variety:** Do the samples cover different contexts (professional, casual, educational)? Single-context samples produce single-dimension voice guides.
3. **Exclusion check:** Identify and flag patterns that are NOT the authentic voice:
   - Platform formatting tics (LinkedIn line breaks, Twitter brevity forcing)
   - Typos and autocorrect errors
   - Phrases borrowed from others (quotes, retweets)
   - Unusually formal writing (legal docs, press releases)
4. **Sample size adequacy:** Is there enough material for full mode, or should I use quick mode?

Output a sample assessment:
> "I have [X samples / Y words] to work with. Quality: [high/medium — why]. I'll use [full/quick] mode. Excluding: [any patterns and why]."

---

## Phase 2: Core Energy Extraction

Identify the fundamental communication mode:

**Role:**
- Teacher (breaks things down systematically)
- Challenger (pushes back on assumptions)
- Cheerleader (builds confidence and momentum)
- Straight-shooter (cuts through BS efficiently)

**Default energy:**
- Calm authority ("Here's what works.")
- High enthusiasm ("This is exciting — let me show you.")
- Understated confidence ("I've seen this a hundred times.")

**Recurring themes:** What topics appear unprompted across samples? These are the things they actually care about.

---

## Phase 3: Phrase Extraction (Systematic)

Scan all samples and extract:

**Transition phrases** (how they shift topics):
- Quote exact examples from samples
- Pattern: "Here's the thing...", "What I've learned...", "Let me put it differently..."

**Emphasis phrases** (how they land a point):
- Quote exact examples
- Pattern: "The reality is...", "This is the part people miss...", "Here's the actual problem..."

**Closers** (how they wrap up):
- Quote exact examples
- Pattern: "That's the move.", "Start there.", "You've got this."

---

## Phase 4: Confidence Zone Mapping

| Zone | Description | Language Markers |
|---|---|---|
| Full authority | Topics they're an expert in | No hedging, definitive statements, "here's what works" |
| Earned perspective | Topics with experience but not mastery | "In my experience...", "What I've found..." |
| Active exploration | Topics they're learning now | "I'm testing this...", "What I'm seeing..." |

Map their stated expertise areas to each zone. This calibration is what makes the voice feel real vs. one-dimensional.

---

## Phase 5: Anti-Pattern Documentation

Extract what they'd NEVER say:
- Words that would feel wrong in their voice
- Phrases that make them cringe
- Tones they naturally avoid
- Industry jargon they hate

Source these from sample evidence where possible: "You never used [word] across [X samples] — it doesn't fit your voice."

---

## Phase 6: Validation Test (REQUIRED)

After extracting the full profile, generate 2 test sentences on the same topic:

**Version A** (using the extracted voice profile):
> "[Sample sentence in their voice]"

**Version B** (wrong voice — contrasting example):
> "[Same content, different voice — shows what to avoid]"

Ask the user: "Does Version A actually sound like you when you're not overthinking it? What feels off?"

This validation catches extraction errors before the guide is put into production.

---

## Quick Mode (`--quick`)

When samples are thin (300–500 words) or time is short:

1. Read 3 samples fast
2. Pull 10 signature phrases
3. Note 3 things they'd never say
4. Write 1 sentence describing their energy

**Output:** Minimum viable voice guide.

**Difference from full mode:**
- Quick: ~10 phrases, 3 anti-patterns, 1-sentence energy descriptor
- Full: Complete profile with confidence calibration, validated test sentences, and source-cited examples

---

## Phase 7: Self-Critique Pass (REQUIRED)

After generating the Voice Guide:

- [ ] Are the extracted phrases actually from the samples, or am I inferring them?
- [ ] Does the anti-pattern list include specific words/phrases, or just vague categories?
- [ ] Do the validation test sentences demonstrate a real difference between in-voice and out-of-voice?
- [ ] Is the confidence zone mapping specific to named topics, or just generic?
- [ ] Would a ghostwriter be able to use this guide without asking follow-up questions?

Flag any issues: "The anti-pattern section only has 2 entries — not enough for a usable guide. I need more samples or direct input from the user."

---

## Output Structure

```markdown
## Voice Guide: [Name] — [Date]

### Sample Assessment
- Samples: [count, types]
- Total words: [count]
- Quality: [high/medium — reason]
- Mode: [quick/full]
- Excluded: [patterns excluded + why]

---

### Core Energy
- Role: [teacher/challenger/cheerleader/straight-shooter]
- Default energy: [description]
- Recurring themes: [list]

### Signature Phrases
**Transitions:**
- "[Phrase]" (source: [email/post])
- "[Phrase]"

**Emphasis:**
- "[Phrase]" (source: [email/post])

**Closers:**
- "[Phrase]"

### Confidence Calibration
**Full authority (no hedging):**
Topics: [list]
Sounds like: "[example sentence]"

**Earned perspective:**
Topics: [list]
Sounds like: "[example sentence]"

**Active exploration:**
Topics: [list]
Sounds like: "[example sentence]"

### Anti-Patterns (Never Use)
- [Word/phrase] — why: [evidence from samples]
- [Word/phrase] — why: [evidence]

### Validation Test
**This sounds like you:**
"[Version A]"

**This doesn't:**
"[Version B — contrast]"

### Self-Critique Notes
[Any gaps, things to validate with user]

### Usage Instructions
- For AI: Paste this guide into your system prompt
- For ghostwriter: Share on day 1 — cuts revision cycles in half
- For team: This is the benchmark for "on brand"
```

---

*Skill by Brian Wagner | AI Marketing Architect | brianrwagner.com*
