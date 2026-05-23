---
name: de-ai-ify
context: fork
description: Rewrite AI-generated text to sound natural and human-written
model: opus
---

# /de-ai-ify

Strip AI-sounding patterns from generated text and rewrite to be natural, direct, and human.

## Usage

```
/de-ai-ify <note path>          # Rewrite a specific note
/de-ai-ify --section <heading>  # Rewrite only a specific section
/de-ai-ify --clipboard          # Rewrite text from clipboard context
```

## Instructions

1. **Read the target note** or receive the text to rewrite

2. **Identify AI patterns** — flag any of the following:

   **Filler phrases to remove:**
   - "Let's dive into...", "Let's explore..."
   - "I'd be happy to..."
   - "It's worth noting that..."
   - "It's important to understand..."
   - "In today's rapidly evolving..."
   - "This is a great question"
   - "As we can see..."
   - "Moving forward..."

   **Hedging to reduce:**
   - "It could potentially..." → state directly or remove
   - "This might suggest..." → "This suggests..." or cut
   - "It's possible that..." → state the thing or qualify once
   - Stacking qualifiers: "perhaps", "maybe", "somewhat", "arguably"

   **Structural patterns to fix:**
   - Excessive bullet points where prose would be clearer
   - Every paragraph opening with a transition word
   - Formulaic "In conclusion..." / "To summarise..." wrap-ups
   - Numbered lists for things that aren't sequential
   - Restating the question before answering it

   **Tone patterns to adjust:**
   - Overly enthusiastic ("fantastic", "incredible", "amazing")
   - Corporate-bland ("leverage", "synergise", "drive value")
   - Sycophantic agreement before every response

3. **Rewrite** the flagged sections:
   - Keep the author's intent and meaning
   - Use active voice, concrete language
   - Prefer shorter sentences
   - Let the content speak — cut throat-clearing
   - Preserve any technical accuracy and wiki-links
   - Maintain frontmatter unchanged

4. **Show the diff** — present before/after for each changed section so the user can review

5. **Apply changes** only after user confirms

## Guidelines

- Do NOT change frontmatter, wiki-links, or Dataview queries
- Do NOT remove content — only rephrase
- Do NOT add new content or expand the text
- Preserve the author's voice where it comes through
- When in doubt, cut rather than rephrase
- UK English throughout
