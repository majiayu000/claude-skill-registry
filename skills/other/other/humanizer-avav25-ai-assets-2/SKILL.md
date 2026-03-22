---
name: humanizer
description: Remove signs of AI-generated writing from text. Use when editing, reviewing, or producing any public-facing text — blog posts, social media, UI copy, emails, landing pages, documentation. Detects and fixes AI patterns including inflated symbolism, promotional language, vague attributions, em dash overuse, rule of three, AI vocabulary, negative parallelisms, sycophantic tone, and filler phrases.
user-invocable: false
---

# Humanizer

Identifies and removes signs of AI-generated text. Makes writing sound natural and human. Based on Wikipedia's "Signs of AI writing" guide maintained by WikiProject AI Cleanup.

## When to Use

- Writing or editing blog posts, social media posts, emails, landing pages
- Writing UI copy, microcopy, error messages, onboarding text
- Reviewing any text before publication
- Any content that will be read by humans outside the team

## Process

1. **Identify AI patterns** — scan for the patterns listed below
2. **Rewrite problematic sections** — replace AI-isms with natural alternatives
3. **Preserve meaning** — keep the core message intact
4. **Maintain voice** — match the intended tone (formal, casual, technical)
5. **Add soul** — inject actual personality, not just remove bad patterns
6. **Anti-AI audit** — ask "What makes this obviously AI generated?", list remaining tells, then revise

## Adding Soul

Avoiding AI patterns is half the job. Sterile, voiceless writing is just as obvious.

**Signs of soulless writing:**
- Every sentence same length and structure
- No opinions, just neutral reporting
- No uncertainty or mixed feelings acknowledged
- No first-person perspective when appropriate
- No humor, edge, or personality

**How to fix:**
- Have opinions — react to facts, do not just report them
- Vary rhythm — short punchy sentences mixed with longer ones
- Acknowledge complexity — "impressive but unsettling" beats "impressive"
- Use "I" when it fits — first person is honest, not unprofessional
- Let some mess in — tangents and asides are human
- Be specific about feelings — not "concerning" but "unsettling that agents churn away at 3am"

See `ai-writing-patterns.md` for the full pattern catalog with before/after examples.

## Quick Reference — Pattern Categories

| # | Pattern | Signal Words |
|---|---|---|
| 1 | Inflated significance | stands as, testament, pivotal, vital role, broader, indelible mark |
| 2 | Notability inflation | independent coverage, active social media presence |
| 3 | Superficial -ing phrases | highlighting, ensuring, reflecting, symbolizing, showcasing |
| 4 | Promotional language | boasts, vibrant, profound, nestled, groundbreaking, renowned, stunning |
| 5 | Vague attributions | experts argue, industry reports, some critics |
| 6 | Formulaic challenges sections | despite challenges... continues to thrive |
| 7 | AI vocabulary words | additionally, delve, foster, garner, intricate, landscape, tapestry, underscore |
| 8 | Copula avoidance | serves as, stands as, marks, represents, boasts, features |
| 9 | Negative parallelisms | not only... but, not just about... it's |
| 10 | Rule of three | forced groups of three ideas |
| 11 | Synonym cycling | protagonist → main character → central figure → hero |
| 12 | False ranges | from X to Y where X and Y are not on a meaningful scale |
| 13 | Em dash overuse | — used more than humans would |
| 14 | Boldface overuse | mechanical bold emphasis on terms |
| 15 | Inline-header lists | **Header:** description pattern |
| 16 | Title case in headings | Strategic Negotiations And Global Partnerships |
| 17 | Emoji decoration | emoji + bold header patterns |
| 18 | Curly quotation marks | curly quotes instead of straight |
| 19 | Chatbot artifacts | I hope this helps, Certainly!, Would you like... |
| 20 | Knowledge-cutoff disclaimers | as of, based on available information |
| 21 | Sycophantic tone | Great question!, You're absolutely right! |
| 22 | Filler phrases | in order to, due to the fact that, it is important to note |
| 23 | Excessive hedging | could potentially possibly be argued |
| 24 | Generic positive conclusions | the future looks bright, exciting times |
| 25 | Hyphenated word pair overuse | cross-functional, data-driven, high-quality used uniformly |

## Output Format

When humanizing text, provide:

1. **Draft rewrite** — cleaned version
2. **AI tells audit** — brief bullets listing remaining AI signals
3. **Final rewrite** — revised after the audit
4. **Changes summary** — what was fixed (optional, if helpful)

## Integration

- **Guardrail**: All public-facing content must pass a humanizer review before finalization
- **Used by workflows**: `/blog-post`, `/marketing`, `/docs` (public-facing content)
- **Used by skill**: `content-creation` (Gate 7: Humanization)
- **Companion resource**: `ai-writing-patterns.md` (full pattern catalog with examples)
