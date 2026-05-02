---
name: voice-extract
description: Extract writing voice from user samples using SICO comparative
  analysis. Compares user writing against Claude's default output to identify
  distinctive voice features. Use when training the system on a new writing
  voice, adding samples to an existing profile, or re-running extraction
  for improved specificity.
version: 1.9.3
globs: "**/*.{md,txt}"
alwaysApply: false
category: writing-quality
tags:
- voice
- extraction
- sico
- style-transfer
- writing
tools: []
complexity: high
model_hint: opus
estimated_tokens: 3200
progressive_loading: true
modules:
- sico-extraction
- sample-intake
- register-creation
dependencies:
- scribe:style-learner
- scribe:slop-detector
---

# Voice Extraction Skill

Extract a user's writing voice through SICO comparative analysis.

## Method: Comparative Feature Extraction

Rather than measuring surface metrics, this skill uses SICO
Phase 1: feed the model user writing samples alongside its own
default output on the same topics. The model describes what the
user does differently. This produces voice descriptions that
encode implicit structural patterns no metrics can capture.

## Key Principles (from research)

1. **Anonymize samples**: Label as "Sample 1", "Sample 2", etc.
   Context labels cause the extractor to anchor on content
   rather than reading a unified voice.

2. **Variety over volume**: 10 samples across different topics
   beats 20 on the same subject. The extraction needs to see
   what stays constant when everything else changes.

3. **Casual writing is distinctive**: Reddit comments, slack
   messages, quick emails. Polished pieces have rough edges
   edited away, and those edges are where voice lives.

4. **Pressure test for specificity**: If extraction output
   sounds generic ("uses varied sentence lengths"), run pass 2
   and force specificity. Good output reads like followable
   instructions, not a book report.

5. **Use Opus for extraction**: More nuanced feature
   descriptions, especially for registers where subtle tonal
   shifts matter.

## Required TodoWrite Items

1. `voice-extract:samples-collected` - Writing samples gathered
2. `voice-extract:samples-anonymized` - Labels stripped, numbered
3. `voice-extract:baseline-generated` - Claude's default output on same topics
4. `voice-extract:extraction-pass-1` - Broad comparative features
5. `voice-extract:extraction-pass-2` - Pressure test for specificity
6. `voice-extract:profile-written` - extraction.md created

## Step 1: Sample Intake

Load: `@modules/sample-intake`

### Directory Mode

```bash
# Scan for samples
PROFILE_DIR="$HOME/.claude/voice-profiles/{name}"
mkdir -p "$PROFILE_DIR/samples"

# Copy samples from user-provided directory
# Rename to Sample-01.md, Sample-02.md, etc.
```

### Interactive Mode

Present the user with:
```
Paste your writing sample below (minimum 200 words).
Type END on a new line when done.
```

Repeat until user says "done collecting" or reaches 10+ samples.

### Manifest

Create `manifest.json`:
```json
{
  "profile_name": "{name}",
  "created": "YYYY-MM-DD",
  "samples": [
    {
      "id": "sample-01",
      "original_source": "anonymized",
      "word_count": 450,
      "date_added": "YYYY-MM-DD"
    }
  ],
  "extraction_model": "opus",
  "extraction_date": null,
  "registers": ["default"]
}
```

### Validation

- Minimum 3 samples
- Minimum 500 words total
- Each sample minimum 100 words
- Variety check: warn if all samples share obvious topic

## Step 2: Baseline Generation

For each sample's topic/context, generate Claude's default
output on the same subject. This creates the comparison pair.

**Prompt for baseline**:
```
Write a short piece about [topic extracted from sample].
Use your natural default style. Do not try to match any
particular voice or style. Just write naturally about this
subject in approximately [word_count] words.
```

Store baselines alongside samples for comparison.

## Step 3: SICO Extraction Pass 1

Load: `@modules/sico-extraction`

The core comparative prompt:

```
I'm going to show you pairs of text. In each pair:
- Text A is written by a specific person
- Text B is your default output on the same topic

Your task: describe what the writer of Text A does
differently from your default style. Focus on:

- Structural patterns (paragraph shapes, section architecture)
- Rhetorical moves (how they build arguments, make transitions)
- Tonal devices (hedging patterns, commitment patterns)
- Sentence-level techniques (clause structure, rhythm)
- Vocabulary tendencies (physical vs abstract language,
  technical vs conversational)
- Distinctive habits (parentheticals, fragments, questions)

Do NOT describe surface metrics (average sentence length,
word count). Describe the voice in terms a writer could
follow. Be specific enough that someone could use your
description to imitate this voice.

[Pairs follow]
```

### Quality Gate

If the extraction output contains any of these generic phrases,
reject and re-run with higher specificity demand:

- "uses varied sentence lengths"
- "maintains a conversational tone"
- "balances formal and informal"
- "engages the reader"
- "creates a sense of"

## Step 4: Extraction Pass 2 (Pressure Test)

```
Review your feature description. For each characteristic
you identified, answer:

1. Could this describe 50% of writers? If yes, be more
   specific or remove it.
2. Can someone follow this as a concrete instruction?
   If not, add an example from the samples.
3. Are there patterns you noticed but didn't name?
   Writers often have unnamed habits. Look for:
   - How they use parentheticals
   - Where they commit vs hedge
   - Physical language for abstract concepts
   - Rhythm of building caution then dropping unhedged claims
   - How they anticipate reader objections

Revise your description to be more specific and followable.
```

## Step 5: Write Profile

Write the extraction to `~/.claude/voice-profiles/{name}/extraction.md`:

```markdown
# Voice Extraction: {name}

## Feature Description

[SICO extraction output here]

## Craft Rules (Detection-Neutral)

These techniques improve writing without increasing
AI detectability:

- Concrete-first: Lead with specific, physical details
- Naming: Label patterns and dynamics explicitly
- Opening moves: Start mid-thought or with a specific moment
- Human-moment anchoring: Ground abstractions in lived experience
- Aphoristic destinations: Write sentences worth repeating alone

## Banned Phrases

[Standard AI vocabulary list + user additions]

## Notes

- Extraction model: {model}
- Extraction date: {date}
- Sample count: {n}
- Total word count: {words}
```

Create default register at `registers/default.md` from the
extraction output.

## Exit Criteria

- Profile directory exists with manifest
- extraction.md contains specific, followable voice description
- Default register created
- No generic phrases in extraction output
- User has reviewed and confirmed the extraction captures
  their voice
