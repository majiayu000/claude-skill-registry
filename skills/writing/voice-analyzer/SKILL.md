---
name: voice-analyzer
description: Analyze writing samples to create a codified voice style guide. This skill extracts patterns, techniques, and characteristics from example writing and generates a reusable voice skill that can be used with anti-ai-writing for consistent, authentic content creation. Use when establishing a new voice style from scratch.
---

# Voice Analyzer

Transform writing samples into a codified voice style that can be replicated consistently.

## Purpose

This skill analyzes 3-5 samples of writing to extract the patterns, techniques, and characteristics that define a distinctive voice. The output is a complete voice skill that can be used alongside `anti-ai-writing` to produce content in that voice.

**Core Philosophy:** Every distinctive writer has patterns - conscious or unconscious. By identifying and codifying these patterns, we can replicate voice authentically without losing what makes it human.

## When to Use This Skill

- Establishing your own writing voice for consistent content
- Codifying a brand voice for team use
- Creating voice guides for ghostwriting clients
- Analyzing competitors or inspirations to understand their approach
- Building a library of voice styles for different contexts

**Requires:** 3-5 writing samples of 500+ words each (more samples = better analysis)

**Output:** A complete `voice-[name]/SKILL.md` file ready for use

---

## The Analysis Process

### Phase 1: Gather Samples

**Collect 3-5 writing samples that represent the voice at its best:**

**Ideal samples:**
- Published content the author is proud of
- Writing that received strong engagement or feedback
- Pieces that "sound like" the author
- Content from the same medium (all newsletters, all blog posts, etc.)

**Avoid:**
- Heavily edited or committee-written pieces
- Content written under constraints (legal, corporate)
- Very old writing that doesn't reflect current voice
- Mixed media (don't combine tweets with long-form)

**Sample preparation:**
1. Paste each sample into a separate section
2. Note the source/context for each
3. Remove any content that was clearly written by others (quotes, etc.)

---

### Phase 2: Extract Voice Characteristics

Analyze the samples across these dimensions:

#### 2.1 Sentence Structure

**Questions to answer:**
- What's the average sentence length? (Short and punchy? Long and flowing?)
- Does the writer vary length deliberately?
- Are sentences simple or complex?
- How does the writer use punctuation?

**Patterns to identify:**
- Signature sentence structures (e.g., "X. But Y." or "Here's the thing: Z")
- Use of fragments
- Paragraph length and rhythm
- Opening and closing patterns

**Document findings as:**
```markdown
## Sentence Structure
- Average length: [short/medium/long]
- Variation pattern: [describe]
- Signature structures: [list specific patterns]
- Punctuation style: [describe]
```

#### 2.2 Word Choice

**Questions to answer:**
- Does the writer use simple or sophisticated vocabulary?
- Are there signature words or phrases that appear repeatedly?
- What's the formality level?
- Does the writer use jargon, slang, or technical terms?

**Patterns to identify:**
- Favorite words (appears 3+ times across samples)
- Avoided words (never appears despite opportunity)
- Contractions (always, never, sometimes)
- Profanity or strong language (level and style)

**Document findings as:**
```markdown
## Word Choice
- Vocabulary level: [simple/moderate/sophisticated]
- Formality: [1-5 scale, casual to formal]
- Signature words: [list]
- Avoided patterns: [list]
- Contractions: [always/sometimes/never]
```

#### 2.3 Tone & Attitude

**Questions to answer:**
- What's the overall emotional register?
- How does the writer relate to the reader?
- Is there humor? What kind?
- What's the confidence level?

**Patterns to identify:**
- Dominant tone (playful, serious, irreverent, warm, etc.)
- Relationship to reader (peer, mentor, friend, expert)
- Humor style (sarcasm, wordplay, self-deprecation, observational)
- Certainty level (definitive vs. exploratory)

**Document findings as:**
```markdown
## Tone & Attitude
- Primary tone: [describe]
- Reader relationship: [describe]
- Humor: [type and frequency]
- Certainty: [definitive/exploratory/mixed]
```

#### 2.4 Structural Patterns

**Questions to answer:**
- How does the writer open pieces?
- How do they transition between ideas?
- How do they close?
- What's the overall architecture?

**Patterns to identify:**
- Opening hooks (story, question, bold claim, etc.)
- Transition style (seamless, signposted, abrupt)
- Closing patterns (call to action, question, summary, callback)
- Section/paragraph organization

**Document findings as:**
```markdown
## Structural Patterns
- Opening style: [describe]
- Transitions: [describe]
- Closing style: [describe]
- Overall architecture: [describe]
```

#### 2.5 Distinctive Techniques

**Questions to answer:**
- What rhetorical devices appear repeatedly?
- Are there signature moves unique to this writer?
- How does the writer handle examples and evidence?
- What makes this voice recognizable?

**Patterns to identify:**
- Rhetorical devices (questions, lists, analogies, callbacks)
- Signature moves (e.g., "Let me tell you a story...")
- Evidence style (data, anecdotes, authority, logic)
- Pattern interrupts (how do they surprise the reader?)

**Document findings as:**
```markdown
## Distinctive Techniques
- Rhetorical devices: [list with examples]
- Signature moves: [describe]
- Evidence style: [describe]
- Pattern interrupts: [describe]
```

#### 2.6 What They DON'T Do

**Just as important as what they do:**

- Phrases they never use
- Structures they avoid
- Topics or approaches they skip
- Formality levels they never hit

**Document findings as:**
```markdown
## Avoidances
- Never uses: [list patterns]
- Never does: [list approaches]
- Avoids: [list topics/structures]
```

---

### Phase 3: Synthesize the Voice Profile

Combine findings into a coherent voice description:

#### The Voice in One Paragraph

Write a single paragraph that captures the essence:

> "[Name]'s voice is [primary characteristics]. They write like [relationship to reader], using [key techniques]. Their tone is [tone], with [humor style if applicable]. Sentences tend to be [structure]. They favor [word choice] and avoid [avoidances]. The overall effect is [feeling/impact]."

**Example:**
> "Mike's voice is direct and confident, with an undercurrent of irreverent humor. He writes like a smart friend who's figured something out and can't wait to share it. His tone is casual but authoritative - he'll drop an f-bomb but back it up with data. Sentences are short and punchy, often fragments. He favors concrete specifics over vague claims and avoids corporate jargon entirely. The overall effect is someone talking straight to you, cutting through the BS."

#### The Voice Spectrum

Place the voice on these spectrums:

```
Formal ←――――――――――→ Casual         [1-5]
Expert ←――――――――――→ Peer           [1-5]
Serious ←―――――――――→ Playful        [1-5]
Reserved ←――――――――→ Opinionated    [1-5]
Abstract ←――――――――→ Concrete       [1-5]
```

---

### Phase 4: Generate the Voice Skill

Create the output skill file with this structure:

```markdown
---
name: voice-[author-name]
description: Write in [Author Name]'s distinctive voice. This style is [brief description]. Use with anti-ai-writing for content that authentically matches [Author]'s approach.
---

# Voice: [Author Name]

[One paragraph voice description from Phase 3]

## Voice Spectrum

- Formal/Casual: [1-5]
- Expert/Peer: [1-5]
- Serious/Playful: [1-5]
- Reserved/Opinionated: [1-5]
- Abstract/Concrete: [1-5]

## Core Characteristics

### Sentence Structure
[From Phase 2]

### Word Choice
[From Phase 2]

### Tone & Attitude
[From Phase 2]

### Structural Patterns
[From Phase 2]

### Distinctive Techniques
[From Phase 2]

### Avoidances
[From Phase 2]

## Example Patterns

### Signature Openings
[3-5 examples from samples with pattern explanation]

### Signature Transitions
[3-5 examples from samples]

### Signature Closings
[3-5 examples from samples]

### Signature Sentences
[5-10 exemplary sentences that capture the voice]

## The [Author] Test

Before publishing, ask:
- [ ] Would [Author] actually write this sentence?
- [ ] Does it match the voice spectrum above?
- [ ] Are signature patterns present?
- [ ] Are avoidances absent?
- [ ] Does it feel like [Author] talking?

## Anti-Patterns

If you see these, you've drifted from the voice:
- [List 5-10 patterns that would violate this voice]
```

---

### Phase 5: Validate & Refine

**Test the voice skill:**

1. Write a short piece using only the voice skill
2. Compare to original samples
3. Identify gaps or mischaracterizations
4. Refine the skill based on testing

**Validation checklist:**
- [ ] Voice description captures the essence
- [ ] Spectrum ratings feel accurate
- [ ] Example patterns are genuinely representative
- [ ] Test output sounds like the samples
- [ ] Nothing important was missed

---

## Output Deliverable

Save the completed voice skill to:
```
voice-[author-name]/
├── SKILL.md         # The voice guide
└── references/
    └── samples.md   # Original samples for reference (optional)
```

**Naming convention:** Use lowercase, hyphenated names
- `voice-mike-caulfield`
- `voice-brand-acme`
- `voice-newsletter-weekly`

---

## Example Analysis Output

See `references/example-analysis.md` for a complete worked example showing:
- Raw samples
- Phase 2 analysis notes
- Phase 3 synthesis
- Phase 4 output skill

---

## Tips for Better Analysis

### More Samples = Better Results
- 3 samples: Basic patterns only
- 5 samples: Good pattern coverage
- 10+ samples: Comprehensive voice capture

### Same Context Matters
- Analyze newsletters separately from tweets
- Blog posts separate from documentation
- Different contexts may need different voice skills

### Look for Unconscious Patterns
- Writers often don't know their own patterns
- Count word frequency objectively
- Note structures that repeat across all samples

### Validate with the Source
- If analyzing someone else's voice, have them review
- Ask: "Does this sound like how you think about your writing?"
- Refine based on feedback

---

## Bundled Resources

- `references/example-analysis.md` - Complete worked example
- `references/voice-template.md` - Blank template for output skill
- `references/analysis-worksheet.md` - Structured worksheet for Phase 2

---

## Related Skills

- **anti-ai-writing** - Core engine for humanization (use with voice skills)
- **voice-[style]** - Example voice skills to reference
- **skill-creator** - For creating other types of skills

---

*Run this analysis once per voice. The output skill can then be used indefinitely for consistent content in that voice.*
