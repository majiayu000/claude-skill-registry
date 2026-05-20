---
name: voice-dna-creator
description: Analyze writing samples to create a comprehensive voice DNA profile. Use when the user wants to capture their unique writing voice, needs to create a voice profile for AI content, or is setting up a new writing system.
---

# Voice DNA Creator

Analyze writing samples to extract and codify a unique voice profile that AI can use to replicate your authentic writing style.

## When to Use This Skill

- Setting up a new writing system
- Creating voice profiles for clients (ghostwriting)
- Updating voice profiles after style evolution
- Onboarding into content creation workflow

## Requirements

The user must provide:
- **Minimum**: 3 writing samples (500+ words each)
- **Ideal**: 5-10 samples across different content types
- **Best**: Mix of casual (social posts) and formal (articles) content

## Analysis Process

### Step 1: Collect Samples

Ask: "Please share 3-10 writing samples that represent your authentic voice. These can be:
- Newsletter issues
- Blog posts
- Social media posts
- Emails you've written
- Any content where you feel 'this sounds like me'

Paste them here or point me to files in the knowledge folder."

### Step 2: Analyze Core Elements

For each sample, analyze:

**Personality Markers**
- What personality traits come through?
- What's the energy level?
- How does the writer relate to the reader?

**Emotional Range**
- What emotions are expressed?
- How intense are they?
- What's the dominant emotional tone?

**Communication Style**
- Formality level (casual to professional)
- Sentence length patterns
- Paragraph structure
- Use of questions, commands, statements

**Language Patterns**
- Signature phrases that repeat
- Power words used frequently
- Transition phrases
- Opening and closing patterns

**What They Avoid**
- Words or phrases never used
- Tones never taken
- Approaches avoided

**Formatting Habits**
- Emoji usage
- List usage
- Header styles
- Bold/italic patterns

### Step 3: Synthesize Findings

Combine analysis across all samples to identify:
- Consistent patterns (appear in most samples)
- Contextual variations (change based on content type)
- Core voice elements (never change)

### Step 4: Generate Voice DNA

Create the profile following this structure:

```json
{
  "voice_dna": {
    "version": "1.0",
    "last_updated": "YYYY-MM-DD",
    "core_essence": {
      "identity": "",
      "primary_role": "",
      "unique_angle": ""
    },
    "personality_traits": {
      "primary": [],
      "how_it_shows": {}
    },
    "emotional_palette": {
      "dominant_emotions": [],
      "emotional_range": {},
      "energy_level": ""
    },
    "communication_style": {
      "formality": "",
      "complexity": "",
      "sentence_structure": {},
      "paragraph_style": ""
    },
    "language_patterns": {
      "signature_phrases": [],
      "power_words": [],
      "words_to_avoid": [],
      "transitions": []
    },
    "never_say": {
      "phrases": [],
      "tones": [],
      "approaches": []
    },
    "formatting_preferences": {},
    "content_philosophy": {},
    "voice_examples": {
      "opening_lines": [],
      "closing_lines": [],
      "transitional_phrases": []
    }
  }
}
```

## Output Instructions

1. After analysis, present key findings in a summary

2. Generate the complete JSON voice profile

3. Save to `/context/voice-dna.json`

4. Provide 3 example sentences written in the captured voice for validation

5. Ask: "Does this capture your voice? What would you adjust?"

## Best Practices

- Focus on TONE and PERSONALITY, not just word choice
- Avoid creating a profile that just repeats phrases
- Capture the "feeling" of the writing, not just patterns
- Include what NOT to do (equally important)
- Make the profile actionable for content generation

## Validation Test

After creating the profile, write a short paragraph on any topic using ONLY the voice DNA as guidance. Ask the user: "Does this sound like you?"

If not, iterate on the profile based on feedback.

## Common Pitfalls to Avoid

- Don't just list frequently used words
- Don't create a parody of the voice (too exaggerated)
- Don't ignore context (social posts ≠ articles)
- Don't miss the underlying personality
- Don't forget emotional elements
