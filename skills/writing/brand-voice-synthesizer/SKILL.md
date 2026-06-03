---
name: brand-voice-synthesizer
description: "Read 5-10 published posts and extract the brand voice — tone, lexicon, sentence patterns, person used, formality, signature phrases, phrases the site never uses. Persist it so every future content-writing skill produces copy that sounds like the brand, not like generic AI."
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: intelligence
---

# Brand Voice Synthesizer

**Version:** 1.0.0
**Updated:** 2026-05-24
**Category:** intelligence
**Status:** stable
**Requires:** Respira for WordPress plugin 7.1+ + MCP server

---

## Description

Read 5–10 published posts on a WordPress site and extract the **brand voice** — tone, lexicon, sentence patterns, person used, formality, signature phrases, phrases the site never uses. Persist it to the site so every future content-writing skill produces copy that sounds like the brand, not like generic AI.

This is the verbal counterpart to the [Design System Synthesizer](https://respira.press/skills/design-system-synthesizer). The two together form a complete brand foundation that every future content-generation skill references.

---

## What it produces

A structured `brand_voice` artifact stored at the site level. Schema:

```json
{
  "version": "1.0.0",
  "synthesized_at": "2026-05-24T14:30:00Z",
  "synthesized_from": ["/blog/post-a/", "/blog/post-b/", "..."],
  "n_samples": 8,
  "total_words_sampled": 12450,
  "person": "we",
  "formality": "approachable_professional",
  "sentence_length_avg_words": 14,
  "sentence_length_median_words": 12,
  "sentence_length_p90_words": 28,
  "paragraph_length_avg_sentences": 3.2,
  "reading_grade_avg": 8.4,
  "tone_descriptors": ["confident", "direct", "lightly playful", "evidence-driven"],
  "signature_phrases": [
    "the short version is",
    "here's what we learned",
    "let's break that down"
  ],
  "common_openers": ["here's", "the", "we"],
  "common_closers": ["that's the lesson", "more soon", "questions welcome"],
  "lexicon_preferred": ["ship", "wire", "land", "tighten", "lean into"],
  "lexicon_avoided": ["leverage", "synergy", "best-in-class", "world-class", "innovative", "cutting-edge", "revolutionary"],
  "punctuation_patterns": {
    "em_dash_usage": "frequent",
    "exclamation_marks": "never",
    "oxford_comma": true,
    "ellipsis_usage": "rare",
    "parenthetical_asides": "frequent"
  },
  "structural_patterns": {
    "opens_with_question": "sometimes",
    "uses_headings": "every_post",
    "uses_bullet_lists": "often",
    "uses_code_blocks": "for_technical_posts",
    "uses_blockquotes": "rare",
    "ends_with_call_to_action": "never"
  },
  "examples": {
    "good_paragraph": "We shipped the redesign last week. The short version is: fewer pages, more density, one CTA per screen. Conversion is up 18% on the new pricing page so far. We'll know more by end of month.",
    "bad_paragraph": "We are thrilled to announce the launch of our revolutionary new design! This best-in-class experience leverages cutting-edge UX innovations to deliver unparalleled value!"
  }
}
```

The artifact is stored via `respira_update_option('respira_brand_voice', ...)` for v7.1. Same migration path to `respira_intelligence_artifacts` in v7.2 as the design system.

---

## When to Use

- First time setting up an AI workflow for a content-heavy site
- Before running any content-generation skill that produces written copy
- After a brand voice update (new style guide, new chief content officer, rebrand)
- Quarterly refresh — voice drifts; resynthesize to catch it

---

## Trigger Phrases

- "extract my brand voice"
- "what's my writing style"
- "analyze my tone"
- "build a voice guide"
- "synthesize my voice"
- "capture my writing style"
- "what's the voice of this site"

---

## Execution Workflow

### Step 1 — Confirm site

Call `respira_get_active_site` + `respira_get_site_context`.

### Step 2 — Pick representative posts

Call `respira_list_posts` with status=publish, limit=20. From the list, pick 5–10 posts that should represent the voice:

- Prefer recent posts (last 6 months) over older ones — voice drifts
- Prefer the site owner's posts over guest posts (look at `author`)
- Mix lengths: include short posts and long-form
- Skip auto-generated content (release notes if they're templated, automated changelogs)
- Skip translated content (the translator's voice contaminates the analysis)

If fewer than 5 posts exist, use whatever's there but note `n_samples` honestly.

### Step 3 — Extract each post's content

For each picked post, call `respira_read_post(post_id)` or `respira_extract_builder_content(post_id)` depending on the active builder. Strip:

- Code blocks (keep the descriptor but exclude the code from voice analysis)
- Embed shortcodes
- Image captions (usually different voice from body)
- Auto-generated footers (linkbacks, "subscribe" CTAs, etc.)

### Step 4 — Analyze

For the corpus of cleaned text, compute:

1. **Person:** Most-used pronoun (I / we / you / no-pronoun). If mixed, note the mix.
2. **Formality:** Read 5–10 random paragraphs. Place on a scale: casual / approachable_professional / formal / academic.
3. **Sentence length:** average, median, p90.
4. **Paragraph length:** average sentences per paragraph.
5. **Reading grade:** Flesch-Kincaid or similar.
6. **Tone descriptors:** 3–5 adjectives based on the corpus. Confident? Cautious? Playful? Direct? Evidence-driven? Storyteller?
7. **Signature phrases:** Repeated multi-word phrases that show up across multiple posts. These are the writer's tells.
8. **Common openers/closers:** How do paragraphs typically start and end?
9. **Lexicon preferred:** Verbs and nouns this writer reaches for. ("ship" instead of "release"; "wire" instead of "integrate"; "land" instead of "launch")
10. **Lexicon avoided:** Words *conspicuously absent* from the corpus that competitors or generic AI would use. ("leverage", "synergy", "best-in-class", "innovative", "revolutionary".) The absence is the signal.
11. **Punctuation patterns:** em dashes? exclamation marks? oxford comma? parenthetical asides?
12. **Structural patterns:** Do posts open with a question? Use headings? Bullet lists? End with a CTA?

### Step 5 — Show the synthesized voice to the user

Output a human-readable summary:

```markdown
## Brand voice synthesized for {site_url}

Based on {n_samples} published posts ({total_words_sampled:,} words sampled, mostly from the last 6 months).

**Person:** {person} ("we" / "I" / "you" / mixed)
**Formality:** {formality}
**Sentence length:** ~{sentence_length_avg_words} words avg ({sentence_length_p90_words}-word p90)
**Reading grade:** {reading_grade_avg}
**Tone:** {tone_descriptors joined}

**Signature phrases this site uses repeatedly:**
{signature_phrases as bulleted list}

**Words this site reaches for:**
{lexicon_preferred as inline list}

**Words this site conspicuously avoids:**
{lexicon_avoided as inline list}

**Punctuation quirks:**
- em dashes: {em_dash_usage}
- exclamation marks: {exclamation_marks}
- oxford comma: {oxford_comma}

**Structural patterns:**
- Opens with a question? {opens_with_question}
- Uses headings? {uses_headings}
- Ends with a CTA? {ends_with_call_to_action}

**A paragraph that sounds like you:**
> {examples.good_paragraph from the corpus}

**A paragraph that does NOT sound like you (generic AI):**
> {examples.bad_paragraph as a constructed counter-example}
```

Ask the user: *"Does this match how you'd describe your voice? Anything to add or correct?"*

### Step 6 — Persist

After confirmation, call `respira_update_option('respira_brand_voice', <json>)`. Confirm with `respira_get_option('respira_brand_voice')`.

Output: *"Brand voice saved. Every Respira content-writing skill from this point forward will reference this voice. The avoided-words list is the strongest signal — the agent will refuse to use those words even if the prompt suggests them."*

---

## How other skills use the brand voice

Once persisted, future content-writing skills (page generators, blog post drafters, social post composers) call `respira_get_option('respira_brand_voice')` at the top of their workflow. They use the voice to:

- Pick pronouns matching the site's person
- Match sentence length and reading grade
- Reach for the preferred lexicon
- Refuse to use the avoided lexicon
- Match punctuation patterns
- Match structural patterns (open with question? end with CTA?)

The **avoided lexicon** is the strongest signal. When the agent is about to write "revolutionary" or "best-in-class," the voice artifact says *"this site never uses that word"* and the agent picks a more honest verb.

---

## Hard rules

- The voice is observed, not designed. Don't invent. Every descriptor traces to evidence in the corpus.
- The avoided lexicon is the **inverse signal** — words conspicuously absent. Don't include common stop words ("the", "and", "is"). Include words that competitor sites would use heavily but this site doesn't.
- The "good paragraph" example must be a real paragraph from the corpus, quoted verbatim. The "bad paragraph" example is a constructed counter-example using the avoided lexicon.
- Never overwrite an existing brand voice silently. Show the diff before saving.
- If the corpus is mixed-author (multiple writers' voices), say so honestly: *"This site has 3 distinct voices in the sampled posts. Pick one author to synthesize from, or capture all 3 as separate voices."*

---

## Telemetry

Records: site URL hash, number of posts sampled, total words analyzed, person detected, formality detected, success/failure. No actual phrases, no avoided words, no example paragraphs are sent.

Endpoint: `POST https://www.respira.press/api/skills/track-usage`
