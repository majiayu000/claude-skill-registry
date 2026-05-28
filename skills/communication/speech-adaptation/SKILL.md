---
name: speech-adaptation
description: "Transform comprehensive written content into purposeful spoken guidance. Use when adapting for speech, converting to spoken format, optimizing for listening, or creating audio content from written material. Keywords: speech, audio, spoken, listening, adaptation, podcast."
license: MIT
metadata:
  author: jwynia
  version: "1.0"
---

# Speech Adaptation

## Purpose

Transform comprehensive written content into purposeful spoken guidance. Speech requires 3-5x compression while maintaining functional value. Apply when converting written content to audio, podcasts, presentations, or voice assistant responses.

## Core Principle

**Lead with value, earn attention.** Listeners can't skim. Front-load what matters and offer expansion rather than exhaustive delivery.

---

## Functional Intent Detection

Parse the original question/content for intent:

| Intent Type | Signals | Focus |
|-------------|---------|-------|
| **Problem-solving** | "How do I..." | Actionable steps |
| **Learning** | "What is..." | Core concepts + examples |
| **Decision-making** | "Should I..." | Key considerations + recommendation |
| **Troubleshooting** | "Why isn't..." | Likely causes + solutions |

## Context Signals

| Signal Type | Examples | Adaptation |
|-------------|----------|------------|
| **Urgency** | "today", "now", "urgent" | Compress to immediate next steps |
| **Scope** | "huge", "complex", "overwhelming" | Lead with simplification |
| **Experience** | "beginner", "new to" | Increase explanation, decrease jargon |
| **Personal stakes** | "I", "my project" | Increase specificity, decrease abstraction |

---

## Content Transformation Principles

### 1. Hierarchical Restructuring

**Written:** Lists methods 1-7 equally
**Spoken:** "There are three main approaches. Start with [most relevant]. If that doesn't work, try [backup]."

### 2. Front-Load Value

**Written:** Builds up to key insights
**Spoken:** Lead with core insight, then supporting details if needed

### 3. Compress Conceptual Space

**Written:** Seven distinct frameworks
**Spoken:** "Basically three strategies: sort by importance, limit your focus, or batch similar work"

### 4. Context-Dependent Detail

**Written:** Explains everything at same depth
**Spoken:** Start simple, indicate where more detail is available
- "Use a priority matrix - urgent versus important"
- Optional expansion cue: "I can break down those four categories if helpful"

### 5. Eliminate Structural Artifacts

**Remove in Speech:**
- Section headers read verbatim
- Bullet point enumeration
- Visual formatting cues
- Redundant category labels

**Add for Speech:**
- Transition phrases between ideas
- Purpose statements before methods
- Summary/recap statements

### 6. Progressive Revelation Strategy

1. **Core insight** (one sentence)
2. **Primary recommendation** (actionable step)
3. **Backup approach** (if primary doesn't fit)
4. **Availability cue** for additional methods

---

## Implementation Guidelines

### Pre-Processing Steps

1. Parse original question for functional intent and context signals
2. Identify 1-2 most relevant pieces for their specific need
3. Determine appropriate compression ratio based on urgency/complexity

### Content Selection Rules

| Context | Selection |
|---------|-----------|
| **High urgency** | 1 primary method + 1 backup |
| **Learning focused** | Core concept + 1 detailed example + availability of more |
| **Decision support** | Key considerations + clear recommendation |
| **Complex topic** | Simplify conceptual framework first, offer detail expansion |

### Speech-Specific Adaptations

- Replace structural language with functional language
- Add explicit transitions between ideas
- Use pronouns and referential terms to avoid repetition
- Include "escape valves" for different user needs
- End with clear next step or summary

---

## Quality Checks

| Test | Question |
|------|----------|
| **Compression** | Is this 30-50% of original length? |
| **Completeness** | Does this answer their core question? |
| **Flow** | Would this make sense heard linearly? |
| **Action** | Do they know what to do next? |

---

## Example Transformation

**Question Type:** Immediate problem-solving with overwhelm signals

**Written Response:** 7 methods with full explanations

**Spoken Adaptation:**
1. **Acknowledge state:** "When facing a huge list..."
2. **Core insight:** "The key is separating what needs doing from what feels urgent"
3. **Primary action:** "Try this: scan for things both urgent AND important"
4. **Boundary setting:** "Pick just 3 - more than that sets you up to feel behind"
5. **Escape valve:** "Other approaches available if this doesn't click"

---

## Success Metrics

- User can act immediately after listening
- Cognitive load feels manageable
- Key insights retained after single hearing
- Optional detail access feels natural when needed

---

## Integration Points

**Inbound:**
- From written documentation or articles
- From comprehensive analysis outputs
- From detailed framework content

**Outbound:**
- To audio content production
- To presentation delivery
- To voice assistant responses

**Complementary:**
- `presentation-design`: For visual + spoken coordination
- `dialogue`: For conversational delivery patterns

## Anti-Patterns

### 1. Uniform Compression
**Pattern:** Reducing all content by the same ratio regardless of importance.
**Why it fails:** Not all content is equal. Some ideas need full explanation; others can be summarized in a phrase. Equal compression buries critical insights and pads trivial ones.
**Fix:** Identify the 1-2 most important points. Protect those while ruthlessly compressing supporting material. Lead with what matters most.

### 2. Written Sentences Spoken
**Pattern:** Reading written prose aloud without restructuring for speech patterns.
**Why it fails:** Written and spoken language have different rhythms, sentence structures, and information density. Written sentences spoken sound formal, awkward, and hard to follow.
**Fix:** Restructure for oral delivery. Shorter sentences. More personal pronouns. Explicit transitions. Repetition for emphasis. Natural breathing points.

### 3. Exhaustive Completeness
**Pattern:** Including all information from the written source because "it might be important."
**Why it fails:** Listeners can't skim, reread, or control pace. Information overload in speech creates immediate cognitive overload and retention collapse.
**Fix:** Accept that spoken content is selective. Provide escape valves: "More on this if helpful." Trust that listeners can ask for expansion rather than front-loading everything.

### 4. Missing Signposts
**Pattern:** Moving between ideas without explicit verbal transitions.
**Why it fails:** Listeners can't see paragraph breaks or headings. Without verbal signposts, ideas blur together. The structure becomes invisible.
**Fix:** Add explicit transitions: "First..." "More importantly..." "Here's the key point..." "Moving on to..." Make the structure audible.

### 5. Buried Action
**Pattern:** Leaving actionable recommendations for the end after extensive context.
**Why it fails:** Listeners who zone out during context miss the action items. Those still engaged have forgotten the details by the time recommendations arrive.
**Fix:** Front-load action with context to follow. "Do X. Here's why..." rather than "Here's all the context, therefore do X."

## Integration

### Inbound (feeds into this skill)
| Skill | What it provides |
|-------|------------------|
| prose-style | Written content quality to work from |
| (written documentation) | Source material for adaptation |

### Outbound (this skill enables)
| Skill | What this provides |
|-------|-------------|
| presentation-design | Spoken content structure for slide coordination |
| (audio production) | Scripts ready for recording |
| (voice assistants) | Responses optimized for spoken delivery |

### Complementary
| Skill | Relationship |
|-------|--------------|
| presentation-design | Speech-adaptation handles the spoken component; presentation-design coordinates visual and spoken elements |
| dialogue | Speech-adaptation for informational delivery; dialogue for conversational and dramatic speech patterns |
