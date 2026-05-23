---
name: voice-matching-wizard
description: Transform writing samples into a codified voice style that can be replicated consistently. This wizard guides you through analyzing samples, extracting patterns, and generating a custom voice skill.
tier: light-setup
setup_time: 15-20 minutes
requires: 2-5 writing samples (500+ words each)
outputs: voice-[your-name].skill.md
---

# Voice Matching Wizard

Create a voice skill that captures the patterns, rhythms, and sensibilities of any writing style.

## What This Does

Voice matching is the art of identifying what makes writing *recognizable*. Not just the obvious markers—vocabulary, sentence length—but the deeper patterns: how ideas unfold, where the writer pauses, what they leave unsaid.

This wizard walks you through the process of:
1. Gathering representative samples
2. Extracting patterns across multiple dimensions
3. Synthesizing a usable voice profile
4. Generating a working skill file

The output is a `voice-[name].skill.md` you can use alongside other skills (like `anti-ai-writing`) for consistent, authentic content.

---

## Before You Begin

**What makes a good sample:**
- At least 500 words
- Writing you're proud of (or writing you want to emulate)
- Representative of the voice you want to capture
- From the same medium (all newsletters, all blog posts, etc.)

**What to avoid:**
- Heavily edited committee writing
- Content written under constraints
- Mixed formats (tweets + longform together)
- Very old work that doesn't reflect current voice

**How many samples:**
- 2-3 samples: Basic patterns
- 4-5 samples: Good coverage
- 10+: Comprehensive capture

---

## Three Paths Through This Wizard

### Path A: "I have samples of my own writing"
You want to codify your existing voice so AI can match it consistently.
→ Skip to **Phase 1: Gather Your Samples**

### Path B: "I want to write like [someone I admire]"
You want to emulate an author, publication, or brand voice.
→ If the writer is well-known (major author, publication), you may be able to use their name directly in prompts. For custom or lesser-known voices, you'll still need samples.
→ Proceed to **Phase 1: Gather Your Samples**

### Path C: "I'm not sure what my voice is yet"
You want to discover and develop your voice through this process.
→ Start with **Phase 0: Voice Discovery** (below)

---

## Phase 0: Voice Discovery (Optional)

*Skip this if you already have samples or know what voice you want.*

To discover your voice, we need to understand how you naturally communicate when you're not performing.

**Answer these questions:**

1. **How do you explain things to friends?**
   - Do you use stories and examples?
   - Do you build logical arguments?
   - Do you make jokes?
   - Do you ask questions to draw them in?

2. **What writers or publications do you gravitate toward?**
   - Not who you think you *should* read—who do you actually read?
   - What about their style appeals to you?

3. **What's your natural sentence length?**
   - Short and punchy?
   - Long and flowing?
   - Variable depending on the point?

4. **How do you feel about jargon?**
   - Love it (signals expertise)?
   - Hate it (pretentious)?
   - Use it sparingly when precise?

5. **What's your relationship with your reader?**
   - Peer/friend?
   - Mentor/teacher?
   - Curious explorer?

Based on your answers, find 2-3 pieces you've written that feel authentic. Use those for Phase 1.

---

## Phase 1: Gather Samples

Collect 2-5 writing samples. Paste each one into a separate document, or note where they can be found.

**For each sample, note:**
- Source/context (blog post, newsletter, etc.)
- When it was written
- Why you chose it

---

## Phase 2: Extract Patterns

Analyze each sample across these dimensions:

### 2.1 Sentence Architecture

| Element | What to Look For |
|---------|------------------|
| **Length** | Average sentence length (short/medium/long) |
| **Variation** | Does length vary deliberately for rhythm? |
| **Complexity** | Simple declarative? Compound? Complex? |
| **Punctuation** | Em dashes? Semicolons? Minimal? |
| **Fragments** | Used for emphasis? Never? |

**Signature structures to identify:**
- Opening patterns ("Here's the thing:")
- Rhythm breaks ("But.")
- List patterns ("First... Second... Third...")
- Closing moves (questions, callbacks, calls to action)

### 2.2 Word Choice

| Element | What to Look For |
|---------|------------------|
| **Vocabulary level** | Simple/moderate/sophisticated |
| **Formality** | 1-5 scale (casual to formal) |
| **Contractions** | Always/sometimes/never |
| **Jargon** | Industry terms? Avoided? |
| **Strong language** | Profanity level/style if any |

**Identify:**
- Favorite words (appears 3+ times across samples)
- Avoided words (never appears despite opportunity)
- Signature phrases

### 2.3 Tone & Attitude

| Element | What to Look For |
|---------|------------------|
| **Emotional register** | Warm? Cool? Intense? Measured? |
| **Reader relationship** | Peer? Mentor? Friend? Expert? |
| **Humor style** | Sarcasm? Wordplay? Self-deprecation? None? |
| **Certainty level** | Definitive or exploratory? |
| **Attitude toward subject** | Passionate? Skeptical? Curious? |

### 2.4 Structural Moves

| Element | What to Look For |
|---------|------------------|
| **Openings** | Story? Question? Bold claim? Scene-setting? |
| **Transitions** | Seamless? Signposted? Abrupt? |
| **Closings** | Call to action? Question? Summary? Callback? |
| **Paragraph length** | Short punchy? Long flowing? Mixed? |

### 2.5 Distinctive Techniques

What makes this voice *recognizable*?

- Rhetorical devices (questions, analogies, callbacks)
- Signature moves unique to this writer
- How evidence is presented (data? anecdotes? logic?)
- Pattern interrupts (how does the writer surprise?)

### 2.6 What They DON'T Do

Just as important:
- Phrases never used
- Structures avoided
- Topics skipped
- Formality levels never hit

---

## Phase 3: Synthesize

### The Voice in One Paragraph

Write a single paragraph capturing the essence:

> "[Name]'s voice is [primary characteristics]. They write like [relationship to reader], using [key techniques]. Their tone is [tone], with [humor style if applicable]. Sentences tend to be [structure]. They favor [word choice] and avoid [avoidances]. The overall effect is [feeling/impact]."

### Voice Spectrum

Rate the voice on these scales (1-5):

```
Formal ←――――――――――→ Casual         [ ]
Expert ←――――――――――→ Peer           [ ]
Serious ←―――――――――→ Playful        [ ]
Reserved ←――――――――→ Opinionated    [ ]
Abstract ←――――――――→ Concrete       [ ]
```

---

## Phase 4: Generate the Voice Skill

Using your analysis, create `voice-[name].skill.md` with this structure:

```markdown
---
name: voice-[name]
description: Write in [Name]'s distinctive voice. [One sentence characterization]. Use with anti-ai-writing for authentic content.
---

# Voice: [Name]

[Your one-paragraph voice description from Phase 3]

## Voice Spectrum

- Formal/Casual: [1-5]
- Expert/Peer: [1-5]
- Serious/Playful: [1-5]
- Reserved/Opinionated: [1-5]
- Abstract/Concrete: [1-5]

## Core Characteristics

### Sentence Architecture
[Your findings from 2.1]

### Word Choice
[Your findings from 2.2]

### Tone & Attitude
[Your findings from 2.3]

### Structural Moves
[Your findings from 2.4]

### Distinctive Techniques
[Your findings from 2.5]

### Avoidances
[Your findings from 2.6]

## Example Patterns

### Signature Openings
[3-5 examples from samples with pattern explanation]

### Signature Transitions
[3-5 examples]

### Signature Closings
[3-5 examples]

### Signature Sentences
[5-10 exemplary sentences that capture the voice]

## The [Name] Test

Before publishing, ask:
- [ ] Would [Name] actually write this sentence?
- [ ] Does it match the voice spectrum above?
- [ ] Are signature patterns present?
- [ ] Are avoidances absent?
- [ ] Does it *feel* right?

## Anti-Patterns

If you see these, you've drifted from the voice:
- [List 5-10 patterns that would violate this voice]
```

---

## Phase 5: Validate

Test your voice skill:

1. Write a short piece using only the voice skill
2. Compare to original samples
3. Identify gaps or mischaracterizations
4. Refine based on testing

**Validation checklist:**
- [ ] Voice description captures the essence
- [ ] Spectrum ratings feel accurate
- [ ] Example patterns are genuinely representative
- [ ] Test output sounds like the samples
- [ ] Nothing important was missed

---

## Human Writing Fundamentals

*Every voice skill should build on these principles from `anti-ai-writing`.*

### The Energy Transfer Principle

The best writing is a transfer of energy from writer to reader. When analyzing samples, notice how the writer transfers energy:
- Do they write conversations or speeches?
- Do they speak WITH their audience or AT them?
- Where do they use specific, concrete language vs. abstract ideas?

### The SUCKS Framework

Apply this when generating voice output:

**S - Specific**: Who is the ONE reader?
**U - Unique & Useful**: Does it change how they think, feel, or act?
**C - Clear, Curious, Conversational**: Does it read like talking to a friend?
**K - Kept Simple & Structured**: Simple ideas, clear structure?
**S - Sticky**: Are there memorable phrases they'll repeat?

### Sticky Sentence Techniques

When identifying signature sentences in Phase 2, look for these techniques:

**Alliteration** — Same starting sounds
- "Specificity is the secret"
- "The best jobs are neither decreed nor degreed"

**Symmetry** — Parallel structure
- "Read for awareness. Write for understanding."
- "It's not 10,000 hours. It's 10,000 iterations."

**Contrast** — Opposing ideas
- "To be everywhere is to be nowhere."
- "Be clear, not clever. Concise, not complex."

**Rhythm** — Pleasing cadence
- Sentence length variation for effect
- Short sentences for emphasis
- Longer sentences for flow

Include the writer's use of these techniques in your voice skill.

### AI Tells to Eliminate

When using your voice skill, watch for these patterns that signal AI involvement:

**The Correlative Construction** (most common):
- ❌ "X aren't just Y - they're Z"
- ❌ "It's not about X, it's about Y"

**Forbidden Openers**:
- ❌ "In the ever-evolving world of..."
- ❌ "Gone are the days when..."
- ❌ "Let that sink in"

**Hedging Language**:
- ❌ "This might help you" → "This will help you"
- ❌ "It could be argued..." → state it directly

**Overused Softeners**:
- Too much "just" and "actually"
- Passive voice ("was determined")
- Corporate jargon

**Test:** For each sentence, ask: Would this appear in ChatGPT output? If yes, rewrite it.

---

## Using Your Voice Skill

Save to: `.claude/skills/voice-[name]/SKILL.md`

**Invoke alongside other skills:**
- `voice-[name]` + `anti-ai-writing` = Authentic, humanized content
- `voice-[name]` + `ghostwriter` = Long-form pieces in voice
- `voice-[name]` + `social-content-creation` = Platform-specific posts

**Update as needed:**
Your voice evolves. Revisit the skill quarterly or when something feels off.

---

## Related Skills

- **anti-ai-writing** — Core humanization engine (use with all voice work)
- **ghostwriter** — For long-form content in someone else's voice
- **transcript-polisher** — For interview-based content

---

*One well-crafted voice skill compounds across everything you create.*
