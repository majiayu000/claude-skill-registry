---
name: humanize
description: Reviews and edits copy to remove AI-generated patterns and make text sound natural. Use when editing drafts, reviewing copy, "humanize this", "make it less AI", "sounds too AI", "remove AI patterns", "edit my copy", "this sounds robotic", or when text feels machine-generated.
---

# Humanize

Review and edit copy to remove signs of AI-generated writing. Based on Wikipedia's "Signs of AI writing" guide maintained by WikiProject AI Cleanup. Contains 30 rules across 6 categories.

## When to Apply

- Editing AI-generated drafts
- Reviewing text that sounds robotic or corporate
- Cleaning up writing before publishing
- Making technical content sound more natural

## Constraints (Non-Negotiable)

- Preserve meaning, factual claims, and intent.
- Preserve coverage: don't drop list items, options, or qualifiers (e.g., removing one option from a list) unless they're truly redundant.
- Do not add new facts, dates, quotes, or citations that are not already present or user-provided.
- Do not imply a source ("according to…") unless you can name it from the input.
- Keep genre and audience intact (e.g., neutral encyclopedic tone vs. personal essay). Use `voice-soul` only when that voice fits.
- Don't rewrite quoted material unless the user asked to rewrite the quote itself.
- Avoid em dashes (—). Replace with commas, periods, or parentheses.
- **Don't introduce new AI patterns.** Your rewrite must pass the same rules you're applying. Common traps: "Here's the thing:", "It's not about X, it's about Y", formulaic hooks that try to sound casual.

## Rule Categories

| Category | Impact | Prefix | Rules |
|----------|--------|--------|-------|
| Content | HIGH | `content-` | 6 |
| Language | HIGH | `language-` | 8 |
| Style | MEDIUM | `style-` | 7 |
| Communication | HIGH | `comm-` | 3 |
| Filler | MEDIUM | `filler-` | 5 |
| Voice | HIGH | `voice-` | 1 |

## Quick Reference

### Content (HIGH)

- `content-significance` — Remove "pivotal moment", "testament to" inflation
- `content-notability` — Replace media name-dropping with specific claims
- `content-ing-endings` — Fix trailing "...highlighting growth" phrases
- `content-promotional` — Cut "nestled", "vibrant", "breathtaking"
- `content-vague-attribution` — Replace "experts say" with specific sources
- `content-challenges` — Remove formulaic "Despite challenges..." sections

### Language (HIGH)

- `language-ai-vocabulary` — Replace delve, showcase, leverage, foster
- `language-dual-adjectives` — Remove "innovative and comprehensive" padding
- `language-copula` — Use "is" instead of "serves as", "stands as"
- `language-contractions` — Prefer contractions when genre allows
- `language-negative-parallelism` — Cut "It's not just X, it's Y", "It's not about X, it's about Y"
- `language-rule-of-three` — Don't force ideas into groups of three
- `language-synonym-cycling` — Stop cycling through synonyms
- `language-false-ranges` — Fix fake "from X to Y" constructions

### Style (MEDIUM)

- `style-em-dash` — Replace em dashes with commas or periods
- `style-boldface` — Reduce mechanical bold emphasis
- `style-inline-headers` — Avoid mechanical **Header:** lists; keep when they improve skimming
- `style-title-case` — Use sentence case in headings
- `style-emojis` — Remove decorative emojis
- `style-curly-quotes` — Use straight quotes
- `style-rhythm` — Vary sentence/paragraph cadence

### Communication (HIGH)

- `comm-artifacts` — Remove "I hope this helps!", "Let me know if..."
- `comm-cutoff` — Remove "as of my last update" disclaimers
- `comm-sycophantic` — Cut "Great question!", "You're absolutely right!"

### Filler (MEDIUM)

- `filler-openings` — Cut "In today's fast-paced world", "Here's the thing" openings
- `filler-phrases` — Cut "in order to", "at this point in time"
- `filler-hedging` — Reduce "could potentially possibly"
- `filler-transitions` — Reduce moreover/furthermore signposting
- `filler-conclusions` — Replace "the future looks bright" with specifics

### Voice (HIGH)

- `voice-soul` — Add personality, opinions, varied rhythm

## Scoring

Score text before and after rewriting to show improvement. The score measures how human the writing sounds.

### How it works

1. Start at 100
2. Subtract points for each violation found
3. HIGH impact violations (Content, Language, Communication, Voice): -3 points each
4. MEDIUM impact violations (Style, Filler): -1 point each
5. Minimum score is 0

### Score report format

```
Category       | Before | After | Notes
---------------|--------|-------|-------------------------------
Content        |     94 |   100 | 2 violations fixed
Language       |     88 |    97 | dual-adjectives, copula
Style          |     85 |   100 | 4 em dashes, tightened headers
Communication  |    100 |   100 | —
Filler         |     95 |   100 | "Here's the thing" removed
Voice          |     91 |    94 | rhythm, contractions
---------------|--------|-------|-------------------------------
Overall        |     84 |    97 |
```

### Interpreting scores

- **95-100**: Clean, sounds human
- **85-94**: Minor issues, mostly fine
- **70-84**: Noticeable AI patterns
- **Below 70**: Needs significant work

## Process

1. If `WRITING_STYLE_GUIDE_PATH` is set, load the writing style guide before processing
2. Load relevant rules from `references/`
3. Scan text for patterns and calculate before score
4. Rewrite problem sections
5. Add voice (see `voice-soul`)
6. **Self-check**: Scan your rewrite for the same AI patterns, calculate after score
7. Read aloud, it should sound like a person wrote it

## Output

Provide:
1. Score report (before → after with category breakdown)
2. The rewritten text
3. Brief summary of changes

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `WRITING_STYLE_GUIDE_PATH` | No | Path to shared writing style guide. Loaded before processing |

## Reference

Based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
