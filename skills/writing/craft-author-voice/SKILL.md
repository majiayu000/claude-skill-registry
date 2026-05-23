---
name: craft-author-voice
description: 'Captures writing style/voice into AUTHOR_VOICE.md so AI can write like the user. Use when asked to match tone, write like me, replicate voice, or capture writing style for content generation.'
---

**User request**: $ARGUMENTS

# Author Voice Skill

Create a maximally information-dense AUTHOR_VOICE.md document through iterative refinement. The resulting document enables any LLM to write content that authentically matches your voice.

## Overview

This skill supports both **creating a new voice doc** and **refining an existing one**. Users often come back multiple times to adjust their doc as their voice evolves or as they notice issues in generated content.

This skill guides you through:
0. **Check Existing** - Look for existing AUTHOR_VOICE.md; let user choose to refine or start fresh
1. **Discovery** - Clarifying questions about your voice characteristics and goals
2. **Initial Draft** - Generate first AUTHOR_VOICE.md based on your inputs (good enough to start!)
3. **Refinement Cycles** - Generate sample texts, collect your ratings/feedback, update the doc ⬅️ **THE REAL MAGIC**
4. **Completion** - Final honed document ready for AI content generation

**Returning users** can skip straight to Phase 3 to run more feedback cycles on their existing doc.

### Where the Value Comes From

The discovery questions give you a solid starting point - but **the real magic happens in Phase 3**. That's where you:
- See actual generated samples in your "voice"
- Judge them ("this doesn't sound like me")
- Give specific feedback ("too formal", "wrong words")
- Watch the voice doc evolve until it truly captures YOU

Each feedback cycle sharpens the doc. Most users need 3-5 cycles to get from "this is okay" to "this is actually me."

## Workflow

### Phase 0: Check for Existing Document

Before starting discovery, check if the user already has an AUTHOR_VOICE.md:

1. **Search for existing doc**: Use Glob to search for `**/AUTHOR_VOICE.md` in the current directory and common locations
2. **If found**: Read it and ask the user what they want to do

```
header: "Existing Voice Doc Found"
question: "I found an existing AUTHOR_VOICE.md. What would you like to do?"
options:
  - "Refine it - run feedback cycles to improve accuracy"
  - "Start fresh - create a new voice doc from scratch"
  - "Review it - just read through what's there"
```

**If "Refine it"**: Skip to Phase 3 (Refinement Cycles) - the user is coming back to improve their existing doc.

**If "Start fresh"**: Proceed to Phase 1 (Discovery) - will overwrite the existing doc.

**If "Review it"**: Read and display the doc, then ask what they want to do next.

3. **If NOT found**: Proceed directly to Phase 1 (Discovery)

### Phase 1: Discovery

Use AskUserQuestion tool with multi-choice options for EVERY question to minimize cognitive load. If AskUserQuestion is unavailable, present numbered options and ask the user to reply with the number(s).

**Question 1: Primary Content Type**

```
header: "Content Type"
question: "What's your PRIMARY content format?"
options:
  - "Twitter/X posts (short-form, punchy)"
  - "LinkedIn posts (professional, insights)"
  - "Blog articles (long-form, detailed)"
  - "Newsletter (conversational, regular)"
  - "Technical documentation (precise, instructional)"
  - "Mixed - I write across multiple formats"
```

**Question 2: Voice Personality**

```
header: "Voice Tone"
question: "How would you describe your voice personality?"
options:
  - "Authoritative expert - confident, direct, no-nonsense"
  - "Friendly mentor - approachable, encouraging, educational"
  - "Provocateur - contrarian, challenges assumptions, bold"
  - "Storyteller - narrative-driven, uses examples, personal"
  - "Analyst - data-driven, logical, objective"
  - "Conversational peer - casual, relatable, human"
multiSelect: true (pick up to 2)
```

**Question 3: Signature Elements**

```
header: "Signatures"
question: "What signature elements define your writing?"
options:
  - "Strong opening hooks"
  - "Numbered lists and frameworks"
  - "Personal anecdotes and stories"
  - "Contrarian takes and hot takes"
  - "Data and research citations"
  - "Metaphors and analogies"
  - "Direct calls-to-action"
  - "Questions to engage readers"
  - "Short punchy sentences"
  - "Long flowing prose"
multiSelect: true
```

**Question 4: Vocabulary Style**

```
header: "Vocabulary"
question: "What's your vocabulary style?"
options:
  - "Simple and accessible - anyone can understand"
  - "Technical jargon - domain-specific terms expected"
  - "Casual slang - internet-native, memes okay"
  - "Formal professional - polished, corporate-appropriate"
  - "Academic - precise, nuanced, scholarly"
```

**Question 5: Emotional Range**

```
header: "Emotion"
question: "What emotions do you convey in your writing?"
options:
  - "Enthusiasm and excitement"
  - "Calm confidence"
  - "Urgency and importance"
  - "Humor and wit"
  - "Empathy and understanding"
  - "Skepticism and critical thinking"
  - "Inspiration and motivation"
multiSelect: true
```

**Question 6: Target Audience**

```
header: "Audience"
question: "Who is your primary audience?"
options:
  - "Developers/Engineers"
  - "Founders/Entrepreneurs"
  - "Product managers"
  - "Executives/Leaders"
  - "General tech audience"
  - "Non-technical professionals"
  - "Students/Learners"
```

**Question 7: Writing Goals**

```
header: "Goals"
question: "What do you want your writing to achieve?"
options:
  - "Build authority and thought leadership"
  - "Drive engagement and discussion"
  - "Educate and inform"
  - "Entertain and delight"
  - "Convert/sell (subtly)"
  - "Build community and connection"
multiSelect: true
```

**Question 8: Anti-patterns**

```
header: "Avoid"
question: "What should your writing NEVER do?"
options:
  - "Use corporate buzzwords"
  - "Sound robotic or AI-generated"
  - "Be preachy or condescending"
  - "Use excessive emojis"
  - "Be overly promotional"
  - "Use clickbait tactics"
  - "Be wishy-washy or hedging"
  - "Use filler phrases"
multiSelect: true
```

**Question 9: Sample Topics** (free text acceptable here)

```
header: "Topics"
question: "List 2-3 topics you frequently write about (or paste examples of your past writing)"
```

### Phase 2: Initial Document Generation

After discovery, generate the first AUTHOR_VOICE.md. This draft is intentionally a "good enough" starting point - not perfect, but solid enough to generate samples and start the feedback loop.

Use this structure:

```markdown
# AUTHOR_VOICE.md

> This document defines [Author]'s writing voice for AI content generation.
> Feed this to any LLM before requesting content to match the author's style.

## Voice Identity

[1-2 sentences capturing the core voice essence]

## Tone Parameters

- **Primary tone**: [e.g., "Confident mentor with occasional humor"]
- **Emotional range**: [comma-separated emotions from discovery]
- **Formality level**: [1-10 scale with description]
- **Warmth level**: [1-10 scale with description]

## Structural Patterns

- **Opening style**: [how posts/articles begin]
- **Paragraph length**: [short/medium/long, typical sentence count]
- **List usage**: [when and how lists are used]
- **Closing style**: [how content ends - CTA, question, statement]

## Vocabulary Rules

### USE:
- [Specific words/phrases the author uses]
- [Technical terms that are okay]
- [Signature expressions]

### AVOID:
- [Words that feel off-brand]
- [Overused phrases to skip]
- [Tone markers to avoid]

## Content Patterns

### Hooks
[How the author grabs attention - examples of opening patterns]

### Arguments
[How the author builds points - numbered, narrative, comparison]

### Evidence
[How claims are supported - data, anecdotes, logic, authority]

### Transitions
[How ideas connect - explicit markers, implicit flow]

## Signature Moves

1. [Specific technique the author uses regularly]
2. [Another signature element]
3. [Third distinguishing characteristic]

## Anti-Patterns

NEVER:
- [Specific thing to avoid]
- [Another anti-pattern]
- [Third prohibition]

## Example Transformations

### Generic version:
"[Common way to express an idea]"

### In author's voice:
"[Same idea in the author's distinctive style]"

---

**User request**: $ARGUMENTS

## Quick Reference

**One-line voice summary**: [Author] writes like [analogy/comparison].

**Before generating content, ensure**:
- [ ] [Checklist item 1]
- [ ] [Checklist item 2]
- [ ] [Checklist item 3]
```

Write this file to the current working directory as `AUTHOR_VOICE.md`.

### Phase 3: Refinement Cycles (Where the Magic Happens)

**This is the most important phase.** The initial doc from Phase 2 captures the basics, but YOUR feedback on generated samples is what transforms it from generic to authentic. Don't skip this.

After generating the initial document, begin iterative refinement:

**Step 3.1: Generate Sample Texts**

**IMPORTANT**: Do NOT generate samples yourself. You MUST use the **voice-writer** agent to generate samples. The agent is specifically designed to read the voice doc and produce authentic samples - attempting to generate them inline will produce inferior results.

```
Use the voice-writer agent to generate 3 sample texts.
Voice doc path: [path to AUTHOR_VOICE.md]
Mode: Sample generation
```

The agent will read the voice doc and output 3 samples:
1. Short-form (~280 chars)
2. Medium-form (2-3 paragraphs)
3. Conversational reply

**Step 3.2: Collect Feedback Per Sample**

For EACH of the 3 generated samples, use AskUserQuestion tool (or numbered options if unavailable):

```
header: "Sample [N]"
question: "Rate this sample and share what's off:"
[Display the sample text]
options:
  - "Perfect - captures my voice exactly"
  - "Close - minor tweaks needed"
  - "Okay - something feels off but hard to pinpoint"
  - "Wrong - this doesn't sound like me"
```

If not "Perfect", follow up with:

```
header: "Feedback"
question: "What specifically needs adjustment in Sample [N]?"
options:
  - "Too formal/stiff"
  - "Too casual/unprofessional"
  - "Wrong vocabulary/word choices"
  - "Missing my signature style elements"
  - "Tone is off (wrong emotion)"
  - "Structure doesn't match how I write"
  - "Too long/wordy"
  - "Too short/choppy"
  - "Other - let me explain"
multiSelect: true
```

If "Other" selected or if more detail needed, prompt for free-text:
"Describe what's wrong and how you'd actually write this:"

**Step 3.3: Update Document**

Based on ALL feedback from the 3 samples:

1. Identify patterns in the feedback (what's consistently wrong?)
2. Update the AUTHOR_VOICE.md with new/refined rules
3. Add specific "instead of X, use Y" examples where needed
4. Strengthen anti-patterns if certain issues keep appearing

**Step 3.4: Check Completion**

```
header: "Continue?"
question: "Want to run another refinement cycle?"
options:
  - "Yes - generate 3 more samples with the updated doc"
  - "No - the voice doc is good enough for now"
  - "Almost done - one more cycle should perfect it"
```

If "Yes" or "Almost done", return to Step 3.1 with the updated document.

### Phase 4: Completion

When user indicates completion:

1. Add a "Version History" section noting refinement cycles completed
2. Add a "Usage Instructions" section for how to use with LLMs
3. Display final document summary
4. Remind user to keep the AUTHOR_VOICE.md with their projects

## Key Principles

### Information Density
- Every line in the doc must be actionable for an LLM
- No fluff, no explanations "for humans"
- Concrete examples over abstract descriptions
- Specific word lists over vague guidelines

### Iterative Refinement
- 3-5 refinement cycles typically needed for high accuracy
- Each cycle should fix specific issues identified
- Track what changes between versions

### Reduce Cognitive Load
- ALWAYS use AskUserQuestion tool when available - this is critical for UX
- Present multi-choice questions to minimize user typing/thinking
- Limit options to 6-8 max per question
- Use multiSelect for non-exclusive choices
- Only use free-text for examples/samples or when AskUserQuestion unavailable

## Output Location

Write `AUTHOR_VOICE.md` to the current working directory (or user-specified path).

