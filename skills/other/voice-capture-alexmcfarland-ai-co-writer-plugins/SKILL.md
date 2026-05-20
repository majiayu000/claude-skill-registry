---
name: voice-capture
description: Analyze 3-5 writing samples from a client plus their interview answers to capture their unique voice. Identifies voice type, sentence patterns, vocabulary, rhythm, and what they never do. Produces a complete voice skill file (.md) ready to install. Use when user wants to "capture voice", "create a voice profile", "voice DNA", or build a ghostwriter skill for a client.
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

# Voice Capture

**Purpose:** Analyze writing samples and interview answers to create a complete voice profile skill file that enables Claude to write authentically in someone's voice. The output is a ready-to-install `.md` skill file.

## When to Activate

Use this skill when:
- User wants to capture a client's voice for ghostwriting
- User mentions "voice profile", "voice capture", "voice DNA"
- User provides writing samples and wants a voice analysis
- User needs to create a ghostwriter skill for consistent voice replication

## Required Input

### Writing Samples (3-5 pieces)
Ask for 3-5 pieces of the subject's best writing. These should be:
- Content they wrote themselves (not ghostwritten)
- Writing they're proud of and consider "on brand"
- Varied formats if possible (email, article, social post)
- At least 1 long-form piece (500+ words)

### Interview Answers (Optional but powerful)
If available, answers to voice-capture questions such as:
- How do you explain what you do to a stranger?
- What topics make you fired up?
- What's a belief you hold that most people in your industry disagree with?
- Describe your communication style in 3 words.

## Voice Analysis Framework

### Dimension 1: The Five Voice Types

Every writer leans toward one or two primary voice types:

1. **The Storyteller** — Conveys ideas through narrative and personal experience. Uses scenes, dialogue, and emotional arcs.
2. **The Opinionator** — Shares direct opinions and strong takes. "I believe..." / "Here's the truth about..." Declarative, confident, position-driven.
3. **The Fact Presenter** — Leads with data, stats, and research. "According to..." / "Research shows..." Evidence-first, analytical.
4. **The Frameworker** — Explains through systems, steps, and structures. Numbered lists, processes, mental models. Organized, systematic.
5. **The Provocateur** — Uses unconventional language, humor, or edge to cut through noise. Informal, surprising, breaks conventions.

**Most people blend 2 types** (e.g., Storyteller + Opinionator, or Frameworker + Fact Presenter). Identify the primary and secondary.

### Dimension 2: Sentence Patterns

Analyze across all samples:
- **Average sentence length** (short/punchy, medium, long/flowing)
- **Sentence variety** (do they mix lengths, or are they consistent?)
- **Opening patterns** (how do they start paragraphs? "I" statements? Questions? Declarations?)
- **Punctuation habits** (em dashes, parentheses, semicolons, periods only?)
- **Fragment usage** (do they use sentence fragments for emphasis?)

### Dimension 3: Vocabulary & Diction

- **Formality level** (casual, conversational, professional, academic)
- **Jargon usage** (industry terms they use naturally)
- **Words they overuse** (everyone has them — identify 5-10)
- **Words they NEVER use** (equally important)
- **Metaphor patterns** (sports? war? nature? building? cooking?)
- **Contractions** (always, sometimes, never)

### Dimension 4: Emotional Palette

- **Default emotional register** (enthusiastic, calm, intense, measured, playful)
- **How they express excitement** (exclamation marks? understatement? metaphor?)
- **How they express disagreement** (direct confrontation? diplomatic reframe? humor?)
- **Vulnerability level** (openly share struggles? keep it professional? strategic vulnerability?)
- **Humor style** (dry/witty? self-deprecating? observational? none?)

### Dimension 5: Structural Habits

- **Paragraph length** (short/scannable, medium, long blocks)
- **List usage** (frequent? rare? numbered or bulleted?)
- **Transition style** (smooth connectors, abrupt shifts, rhetorical questions)
- **Opening patterns** (how they start a piece — hook? question? story? declaration?)
- **Closing patterns** (how they end — CTA? question? statement? fade out?)

### Dimension 6: What They NEVER Do

This is as important as what they do:
- Phrases they would never use
- Tones they never strike (e.g., never sarcastic, never formal)
- Formats they avoid
- Topics they don't touch
- Emoji/formatting habits they reject

## Output: Voice Skill File

Generate a complete skill file in this format:

```markdown
---
name: voice-profile-[client-name]
description: Voice profile for [Client Name]. Apply this skill automatically to all content production to maintain authentic voice consistency. Activates on any writing task.
---

# Voice Profile: [Client Name]

## Voice Type
**Primary:** [Type] — [Brief description of how it manifests]
**Secondary:** [Type] — [Brief description]

## Sentence Patterns
- **Average length:** [Short/Medium/Long]
- **Variety:** [Description]
- **Opening habits:** [How they start paragraphs]
- **Punctuation:** [Habits — dashes, parentheses, etc.]
- **Fragments:** [Yes/No — how they use them]

## Vocabulary & Diction
- **Formality:** [Level]
- **Contractions:** [Always/Sometimes/Never]
- **Signature phrases:** [5-10 phrases they use repeatedly]
- **Jargon they use naturally:** [List]
- **Metaphor domain:** [Where they draw metaphors from]
- **Words to USE:** [List of words that sound like them]
- **Words to AVOID:** [List of words that don't sound like them]

## Emotional Palette
- **Default register:** [Description]
- **Excitement:** [How they show it]
- **Disagreement:** [How they express it]
- **Vulnerability:** [Level and style]
- **Humor:** [Style or absence]

## Structural Habits
- **Paragraphs:** [Length and style]
- **Lists:** [Usage pattern]
- **Transitions:** [Style]
- **Openings:** [Pattern]
- **Closings:** [Pattern]

## Rules: NEVER Do This
1. [Specific thing to never do]
2. [Specific thing to never do]
3. [Specific thing to never do]
4. [Specific thing to never do]
5. [Specific thing to never do]

## Rules: ALWAYS Do This
1. [Specific thing to always do]
2. [Specific thing to always do]
3. [Specific thing to always do]
4. [Specific thing to always do]
5. [Specific thing to always do]

## Voice Test
When writing as [Client Name], check:
- [ ] Would they actually say this out loud?
- [ ] Does it match their sentence rhythm?
- [ ] Are the word choices theirs, not generic?
- [ ] Is the emotional register right?
- [ ] Would a close colleague recognize this as their writing?
```

## Quality Checklist

- [ ] Primary and secondary voice types identified with evidence
- [ ] Sentence patterns analyzed with specific examples from samples
- [ ] Vocabulary section includes BOTH words to use and words to avoid
- [ ] Emotional palette captures their real range (not generic)
- [ ] 5+ "NEVER do this" rules (specific, not vague)
- [ ] 5+ "ALWAYS do this" rules
- [ ] Output is a complete, installable skill file
- [ ] Analysis is based on actual writing samples (not assumptions)
- [ ] Voice test checklist included
- [ ] File can be saved as `.md` and used immediately
