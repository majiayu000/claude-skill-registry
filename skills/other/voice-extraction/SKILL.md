---
name: voice-extraction
description: "Reverse-engineer any person's writing voice from their content. Paste in posts, articles, tweets, or essays and this skill launches 10 parallel Sonnet subagents to analyze every dimension of the voice, then synthesizes into a voice file. Use when someone says 'match this voice,' 'analyze this writing,' 'extract their voice,' 'make me sound like this,' 'study this person's writing,' or pastes in content they want to learn from."
---

# /voice-extraction — Reverse-Engineer Any Voice

Paste content. Get a complete voice architecture. 10 Sonnet subagents rip apart every dimension in parallel.

This is not a summary. This is a structural teardown of how someone writes, thinks, teaches, and earns trust. The output is a voice file that any other skill can read to produce content in that voice.

---

## When to Use

- Someone pastes in posts, articles, or tweets they admire
- "Make me sound like this person"
- "Steal this voice"
- "Analyze how they write"
- "Study this and build a voice from it"
- Building a brand voice from a specific person's content (founder, competitor, inspiration)
- Replacing a generic brand-voice profile with one built from real source material

---

## On Activation

1. Confirm you have raw content to analyze. The user must paste or point to actual writing (posts, articles, tweets, essays). Minimum: 1 substantial post or 5+ tweets. More is better.

2. If the content is thin: "I need more material to extract a real voice. One post gives me patterns. Five posts give me a system. Can you paste more?"

3. If the content is rich enough: proceed immediately. Don't ask unnecessary questions. The content IS the input.

---

## Phase 1: Launch 10 Sonnet Subagents

**CRITICAL: Use `model: "sonnet"` for all 10 agents. Not opus. These run in parallel and sonnet is the right tool for focused analytical work.**

Launch ALL 10 in a SINGLE message using the Agent tool. Each agent gets the full pasted content plus a specific analytical lens.

### The 10 Dimensions

**Agent 1: Sentence Structure & Rhythm**
Analyze sentence length patterns, paragraph openers, idea sequencing within paragraphs, transitions between sections, use of questions vs statements. Look for: short-short-long triplets, myth-pivot openers, colon embeds, imperative staccato closers. Give specific examples from the content.

**Agent 2: Vocabulary & Word Choice**
Analyze verbs they reach for, adjectives they use, words they avoid, jargon level, how they handle technical terms, signature phrases, casual vs formal balance. Identify: blacklist words (what they never say), signature vocabulary, crossover vocabulary from other domains.

**Agent 3: Teaching Methodology**
Analyze how they introduce ideas, use examples, structure explanations, handle complexity, guide the reader. Look for: iteration-as-pedagogy (attempt #1, #2, #3), analogy-before-abstraction, wrong-way-first patterns, complexity escalation, "develop your intuition" closes.

**Agent 4: Emotional Register**
Map the emotional spectrum: when they show enthusiasm, when cautious, how they handle warnings, relationship to reader, confidence level, humor style. Identify: default emotional temperature, how warmth is rationed, how confidence appears, what emotions are absent.

**Agent 5: Content Structure Patterns**
Analyze macro structure of pieces: opening patterns, section organization, how arguments build, how pieces close. Identify: the meta-pattern across all pieces, theory-to-example ratio, what goes first, what gets omitted.

**Agent 6: Authority & Credibility Signals**
Analyze how they establish credibility without arrogance. Look for: "we tried/I tried" patterns, I/we splitting, epistemic framing, credentialing through specificity vs titles, how they credit others.

**Agent 7: Tweet-Length Writing**
Analyze short-form specifically: sentence structure in tweets, claim posture, compression mechanism, how they tease long-form, what makes it feel like a person vs a content machine. Identify: the thesis extraction pattern, audience selection through vocabulary.

**Agent 8: Use of Concrete Examples**
Analyze naming patterns, specificity levels, when real names vs templates, how examples serve arguments. Look for: mechanism-level vs outcome-level specificity, friction terms that signal lived experience, examples doing double duty (illustrating AND arguing).

**Agent 9: Anti-Patterns (What They Don't Do)**
Analyze what's systematically absent: hype words, corporate speak, self-promotion patterns, talking down, clickbait, empty enthusiasm, excessive hedging, summary conclusions, rhetorical questions as transitions. Evidence of absence is as important as evidence of presence.

**Agent 10: Adaptation for Target Voice**
Given all the above, how should this voice be adapted for the user's product/brand? What transfers directly? What needs modification? What should the user's unique voice add that the source doesn't do? Include example tweets/posts in the adapted voice.

### Agent Prompt Template

Each agent gets:

```
You are analyzing the writing voice of [PERSON] to reverse-engineer their complete voice architecture. Focus ONLY on [DIMENSION].

Here is their content:
[FULL PASTED CONTENT]

Additional context: [USER'S PRODUCT/BRAND if relevant]

Output a structured analysis with specific patterns and examples from the actual content. No fluff. Be specific enough that someone could replicate this voice from your analysis alone.
```

---

## Phase 2: Synthesize

Once all 10 agents report back, synthesize their findings into a single voice file. The file should be structured as:

```markdown
# [Name] Voice Guide

> Built from deep analysis of [source description]. [One sentence on what this voice is for.]

## 1. Core Identity
[Who this voice is. The guiding sentence.]

## 2. Sentence Architecture
[Patterns from Agent 1, distilled into rules with examples]

## 3. Vocabulary
[Reach for / Avoid lists from Agent 2]

## 4. Emotional Register
[Temperature map from Agent 4]

## 5. Authority & Credibility
[Patterns from Agent 6]

## 6. Teaching Style
[Patterns from Agent 3]

## 7. Tweet Voice
[Short-form patterns from Agent 7]

## 8. Content Structure
[Macro patterns from Agent 5]

## 9. What We Never Do
[Anti-patterns table from Agent 9]

## 10. The [Brand] Delta
[Adaptation from Agent 10]

## 11. Example Tweets in This Voice
[3-5 examples from Agent 10's adaptation]
```

### Where to Save

This skill extracts a *specific person's* voice (founder, competitor,
inspiration) — it does NOT overwrite the project's canonical
`brand/voice-profile.md`. Each extracted voice lives in its own file
so multiple subjects can coexist and be referenced independently.

- If inside a project with `brand/`: save to `brand/voices/[name].md`
  (create the `brand/voices/` subdirectory if it doesn't exist)
- If standalone: save to `./voices/[name].md` relative to the current
  working directory

Never write to `brand/voice-profile.md` from this skill — that path is
owned by `/brand-voice` and represents the single canonical project
voice. Use the voices subdirectory for per-subject extractions.

---

## Phase 3: Wire In

After the voice file is written:

1. Tell the user it's done and where it's saved
2. Offer to update `/cmo` or other skills to read this file instead of (or in addition to) the default `voice-profile.md`
3. Offer to write sample tweets in the new voice as a test

---

## Anti-Patterns

| Anti-pattern | Why it fails | Instead |
|-------------|-------------|---------|
| Summarizing the person's content | A summary is not a voice analysis | Analyze HOW they write, not WHAT they write about |
| Using fewer than 10 agents | Each dimension needs focused attention; combining them produces shallow analysis | Always launch all 10, always in parallel |
| Using opus for the subagents | Expensive and unnecessary; sonnet is sharp enough for focused analytical work | Always use `model: "sonnet"` |
| Launching agents sequentially | Wastes time; these are independent analyses | Launch all 10 in a SINGLE message |
| Skipping the adaptation agent (#10) | The raw analysis is academic without adaptation to the user's context | Agent 10 is what makes this actionable |
| Writing a generic "be authentic" voice guide | Useless; every voice guide says this | Every rule must have a specific pattern with a specific example |
| Analyzing without enough source material | Patterns need repetition to be patterns | Ask for more content if < 1 substantial post |

---

## Related Skills

- **/brand-voice** — builds voice from interview or website scrape (lighter weight, less precise)
- **/writing-assistant** — uses the voice file to write in the extracted personal voice
- **/cmo** — orchestrates marketing content using the voice file
- **/compound-writing** — evolves the voice over time through learnings
