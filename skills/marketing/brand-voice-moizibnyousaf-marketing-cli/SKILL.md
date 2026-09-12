---
name: brand-voice
description: "Define or extract a consistent brand voice that other skills can use. Three modes: Extract (analyze existing content), Build (interview-based), Auto-Scrape (from URL). Use when copy sounds generic, when starting any new project, when voice feels inconsistent across channels, when onboarding a new brand, or when any skill needs voice-profile.md but it doesn't exist yet. This is always the first skill to run for a new project. Make sure to use this skill whenever the user mentions tone of voice, brand personality, 'my copy all sounds the same', 'how should I sound', 'analyze my website voice', 'define my tone', or anything about making content sound more human or distinctive. Even if the user just says 'my marketing sounds generic' — that's a voice problem."
category: foundation
tier: must-have
reads:
  - brand/voice-profile.md
  - brand/positioning.md
  - brand/audience.md
writes:
  - brand/voice-profile.md
  - brand/learnings.md
triggers:
  - what's my voice
  - analyze my brand
  - define my voice
  - make this sound like me
  - voice guide
  - brand personality
  - analyze my website
  - brand voice
---

# /brand-voice -- Brand Voice Engine

Generic copy converts worse than copy with a distinct voice. Not because the
words are different -- because the reader feels like they're hearing from a
PERSON, not a marketing team.

This skill defines that voice. Either by extracting it from existing content,
building it strategically from scratch, or auto-scraping a URL to analyze a
brand's public presence.

For output formatting, see /cmo [rules/output-format.md](../cmo/rules/output-format.md).

---

## On Activation

1. Read `brand/` context:
   - **positioning.md** — If available, use market angles to inform voice differentiation. A brand positioned as "the anti-course course" needs a different voice than one positioned as "enterprise-grade."
   - **audience.md** — If available, tailor vocabulary and tone to the target reader. Technical builders get different language than busy executives.
   - If neither exists, proceed with defaults. Ask the user about their market and audience during the question sequence.
2. Check if `./brand/voice-profile.md` already exists:
   - **Exists** → Update mode: show current profile summary, ask what to change.
   - **Does not exist** → Proceed to Mode Selection below.
3. Assess the user's request to determine which mode to use (Extract, Build, or Auto-Scrape).

## Three Modes

### Mode 1: Extract (analyze existing content)

User provides 3-5 pieces of existing content (blog posts, emails, social posts, about page, etc).

**The analysis process:**

1. **Read all provided content** -- look for patterns, not individual word choices
2. **Identify the voice DNA:**
   - Sentence structure (short/punchy vs. flowing/complex)
   - Vocabulary level (everyday vs. technical vs. academic)
   - Emotional register (warm/friendly vs. authoritative vs. irreverent)
   - Perspective (first-person storytelling vs. objective analysis)
   - Rhythm (varies sentence length? staccato? musical?)
3. **Map the personality axes** (see Voice DNA Framework below)
4. **Generate the voice profile**
5. **Write to ./brand/voice-profile.md**

### Mode 2: Build (construct from scratch)

No existing content. Build voice strategically through guided questions.

**The question sequence:**

1. "If your brand were a person at a dinner party, how would they talk?"
2. "Who is your audience? Technical builders, creative professionals, busy executives, everyday consumers, or a mix?"
3. "Name 2-3 brands whose tone you admire (not their product -- their VOICE)."
4. "What words should NEVER appear in your marketing? What feels off-brand?"
5. "Show me something you've written that felt 'right' -- even a Slack message or email."

### Mode 3: Auto-Scrape (URL analysis)

User provides a URL. Skill uses Exa MCP to research the brand's public presence.

1. Use Exa MCP to search for the brand's website content, social profiles, and public-facing copy
2. Analyze homepage, about page, social bios, recent posts
3. Extract voice patterns using the same DNA framework as Mode 1
4. Present findings and ask user to confirm/adjust
5. Generate voice profile

## Mode Selection

Not sure which mode? Here's the decision tree:
- **Have 3+ pieces of existing content** (blog posts, emails, landing pages) → Mode 1: Extract
- **Starting fresh with no content** → Mode 2: Build via interview
- **Have a live website URL** → Mode 3: Auto-Scrape

If the brand has both a website AND existing content, prefer Mode 1 (Extract) — it captures the voice the brand already uses, which is more authentic than what a URL scan reveals.

---

## Voice DNA Framework

Every voice maps across these axes:

### Personality Spectrum

Rate each 1-10 with brief justification:
- Formal / Casual
- Reserved / Expressive
- Serious / Playful
- Traditional / Progressive
- Complex / Simple
- Cautious / Bold

### Voice Markers

**Sentence patterns:** Average length, variation, structure (simple/compound/fragmented)

**Vocabulary:** Jargon level (none/light/technical), power words, forbidden words

**Perspective:** Person (I/we/you), distance (intimate/conversational/professional), authority (peer/mentor/expert/challenger)

### The Do/Don't Table

Minimum 5 rows, maximum 10. Specific voice behaviors and example phrases.

### Platform Adaptation Table

| Platform | Tone Shift | Length | Special Notes |
|----------|-----------|--------|--------------|
| LinkedIn | More professional, authority-forward | Medium | Lead with insight |
| Twitter/X | Punchier, more direct | Short | Fragment sentences OK |
| Instagram | Warmer, more visual language | Short-Medium | Casual, aspirational |
| Email | Most personal, conversational | Medium-Long | First-person storytelling |
| Blog/SEO | Most detailed, structured | Long | Can be more technical |
| TikTok | Most casual, spoken-word feel | Very short | Conversational, raw |
| Threads | Thoughtful, conversational | Short-Medium | Opinion-led |
| Bluesky | Nuanced, substantive | Short | Informed, not aggressive |

---

## Output Format

### Header

```
  BRAND VOICE PROFILE
  [Brand/Person Name]
  Generated [Month Day, Year]
```

### Content

1. **Voice Summary** (2-3 sentences capturing the essence)
2. **Personality Spectrum** (rated axes)
3. **Voice Markers** (sentence patterns, vocabulary, perspective)
4. **The Do/Don't Table**
5. **Platform Adaptation Table**
6. **Sample Copy** (3 examples: short social post, email opener, landing page headline)

### Files Saved

Write to `./brand/voice-profile.md`.

### What's Next

```
  -> /positioning-angles   Find your market angle
  -> /direct-response-copy Write copy in your voice
  -> /content-atomizer     Create social content
```

---

## File Output Protocol

Write ./brand/voice-profile.md with: last updated, voice summary, personality spectrum, voice markers, do/don't table, platform adaptations, sample copy.

**If ./brand/voice-profile.md already exists:** Read existing file, show what will change, ask for confirmation before overwriting.

---

## Feedback

After the voice profile is saved and used in at least one downstream skill, collect feedback:
- "How did the voice feel in that [email/post/page]? (a) Nailed it, (b) Close but edited, (c) Off, (d) Haven't used yet"
- For (a) or (b): append what worked to `brand/learnings.md` with date and skill name.
- For (c): ask what felt wrong, adjust the voice profile, and log the change to `brand/learnings.md`.


## Voice Test Loop (Required)

After generating a voice profile from ANY mode, validate before saving. Full details in [references/voice-modes.md](references/voice-modes.md).

1. Generate 3 sample paragraphs in the brand's voice: email opening, social post, landing page hero.
2. Present with options: (1) Nails it → save, (2) Close but needs adjustment → ask what's off, revise, re-test, (3) Not quite right → ask for examples, rebuild relevant sections, re-test.
3. After 3 rounds without confirmation, offer: save current version, one more round, or restart with a different mode.

Never skip this step. Never save a profile without user confirmation.

## Anti-Patterns

| Anti-pattern | Instead | Why |
|-------------|---------|-----|
| Generating a generic "professional yet approachable" voice | Extract specific patterns from real content or deep questioning | Generic profiles are useless — every downstream skill produces the same bland output. The whole point is differentiation. |
| Skipping the Voice Test Loop | Always validate with 3 samples before saving | A profile that looks right on paper can sound wrong in practice. The test loop catches mismatches before they propagate to all other skills. |
| Copy-pasting platform adaptation template defaults | Each brand has different platform behaviors — think about each one | A casual brand might be MORE formal on LinkedIn. A formal brand might loosen up on Twitter. Defaults are wrong by definition. |
| Writing the profile without reading existing brand context | Check positioning.md and audience.md first | Voice should align with positioning and audience. Writing voice in isolation means rewriting it later when those files exist. |
| Overwriting an existing profile without showing diff | Read existing file, show what will change, get confirmation | The user may have manually tweaked the profile. Blindly overwriting loses their refinements. |
| Producing a profile with no example phrases | On-brand and off-brand examples are required | Examples are the fastest way for downstream skills to calibrate. Without them, other skills have to interpret abstract axes, which leads to drift. |

## Invocation

This skill activates when:
- User asks "what's my voice" or "analyze my brand"
- User says copy sounds "generic" or "off-brand"
- Another skill needs voice context but ./brand/voice-profile.md doesn't exist
- User provides a URL and asks to analyze the brand

## What This Skill Is NOT

- Does NOT write copy (that is /direct-response-copy)
- Does NOT define positioning (that is /positioning-angles)
- Does NOT research the audience (that is /audience-research)
- Does NOT create visual identity (that is /creative)
